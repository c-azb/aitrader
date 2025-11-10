

from pydantic import BaseModel, Field
from src.FUNDAMENTALS_AGENT.fundamentals_agent import FundamentalsAgent
from src.TA_GRAPH.ta_graph import TAGraph,GraphGenerator
from src.LLMs.llms import LLMs
from typing import TypedDict,Annotated,Literal
from langgraph.graph import add_messages, StateGraph,START
from langgraph.types import Command
from langchain_core.messages import AnyMessage,SystemMessage,HumanMessage,AIMessage

class State(TypedDict):
    messages:Annotated[ list[AnyMessage], add_messages ]
    ta_messages:Annotated[ list[AnyMessage], add_messages ]  #ta and fundamentals agents were isolated from each other
    fund_messages:Annotated[ list[AnyMessage], add_messages ]
    ticker_symbol:str
    graph_generator:GraphGenerator
    is_recall:bool #only if usinc sync system due to gpu limitations


    @staticmethod
    def get_initial_state(user_input,ticker_symbol):
        return State( messages= [HumanMessage(user_input)],ticker_symbol=ticker_symbol,ta_messages=[],fund_messages=[],is_recall=False )

class MainGraph:
    def __init__(self,llms:LLMs,use_async=False):
        self.llms=llms
        self.fundamentals_agent = FundamentalsAgent(llms)
        self.ta_graph = TAGraph(llms)

        graph = StateGraph(State)
        graph.add_node('fundamentals_agent_node',self.fundamentals_agent_node)
        graph.add_node('ta_graph_node',self.ta_graph_node)
        graph.add_node('manager_node',self.manager_node)

        if use_async:
            graph.add_edge(START,'fundamentals_agent_node')
            graph.add_edge(START,'ta_graph_node')
            graph.add_edge('fundamentals_agent_node','manager_node')
            graph.add_edge('ta_graph_node','manager_node')
        else:
            graph.set_entry_point('fundamentals_agent_node')
            graph.add_conditional_edges('fundamentals_agent_node', 
                                        lambda x: 'manager_node' if x['is_recall'] else 'ta_graph_node',
                                        {'manager_node':'manager_node','ta_graph_node':'ta_graph_node'} )
            # graph.add_edge('fundamentals_agent_node','ta_graph_node')
            graph.add_edge('ta_graph_node','manager_node')
        self.graph = graph.compile()

    
    def fundamentals_agent_node(self,state:State):
        fundamentals_messages = [state['messages'][0]] + state['fund_messages']
        res = self.fundamentals_agent.fundamentals_agent.invoke( {'messages':fundamentals_messages} )
        # return {'messages':[ res['messages'][-1] ] }
        return {'fund_messages':[ res['messages'][-1] ] }


    def ta_graph_node(self,state:State):
        ta_messages = [state['messages'][0]] + state['ta_messages']
        res = self.ta_graph.graph.invoke( {'messages':ta_messages,'ticker_symbol':state['ticker_symbol']} )

        # return {'messages':[ res['messages'][-1] ],'graph_generator':res['graph_generator'] }
        return {'ta_messages':[ res['messages'][-1] ],'graph_generator':res['graph_generator'],'is_recall':True }
    
    def manager_node(self,state:State) -> Command[Literal['fundamentals_agent_node','ta_graph_node','__end__']]:
        fundamentals_msg = [state['fund_messages'][-1]] if len(state['fund_messages']) == 1 else state['fund_messages'][-2:]
        ta_msg = [state['ta_messages'][-1]] if len(state['ta_messages']) == 1 else state['ta_messages'][-2:]

        msgs = [
            SystemMessage((
                'You are a financial manager, you will analyse reports and take investment decisions.\n' \
                'The finance advises are for education purposes only.\n'
                'The analysis came from two analysts, a fundamentals analyst and a technical analysis analyst. ' \
                'Your goal is to provide a final report based on the analysts analysis.\n' \
                'For that you can make your answer destination as:\n'
                'fundamentals: Request something to the fundamentals analyst\n'
                'technical: Request something to the technical analyst\n'
                'report: Provide your final report in markdown format'
                 )
            ),
            state['messages'][0],*fundamentals_msg,*ta_msg,
            HumanMessage('Analyse the reports from the technical analyst and the fundamentals analyst and provide investment decisions.')
        ]
        res = self.llms.llm_manager.with_structured_output(ManagerResponse).invoke(msgs)#.content
        # res = self.llms.llm_manager.invoke(msgs)#.content

        print(res.next_decision)

        if res.next_decision == 'fundamentals':
            return Command(goto='fundamentals_agent_node',update={'fund_messages':[ HumanMessage(f'Manager request to fundamentals analyst: {res.content}') ]})
        elif res.next_decision == 'technical':
            return Command(goto='ta_graph_node',update={'ta_messages':[ HumanMessage(f'Manager request to technical analyst: {res.content}') ]})

        return Command(goto='__end__',
                       update={'messages':[fundamentals_msg[-1],ta_msg[-1], AIMessage(res.content) ]})
    
class ManagerResponse(BaseModel):
    next_decision:Literal['fundamentals','technical','report'] = Field(description='Answer destination')
    content:str = Field(description='your message related to the answer destination')