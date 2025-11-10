
from src.LLMs.llms import LLMs
from src.TA_GRAPH.chart_agent import ChartAgent
from src.TA_GRAPH.researcher_agent import ResearcherAgent,ResearcherResponse
from src.TA_GRAPH.graph_generator import GraphGenerator
from src.tools.send_message import SEND_MSG_TOOL_NAME

from langgraph.graph import StateGraph,MessagesState
from langgraph.types import Command
from typing import Literal
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage

class TAGraphState(MessagesState):
    ticker_symbol:str
    researcher_structured_response:ResearcherResponse
    graph_generator:GraphGenerator


class TAGraph:

    def __init__(self,llms:LLMs):
        
        self.researcher_agent = ResearcherAgent(llms)
        self.chart_agent = ChartAgent(llms)

        graph = StateGraph(TAGraphState)
        graph.add_node('researcher_node',self.researcher_node)
        graph.add_node('chart_generator_node',self.chart_generator_node)
        graph.add_node('chart_agent_node',self.chart_agent_node)

        graph.set_entry_point('researcher_node')
        graph.add_edge('researcher_node','chart_generator_node')
        graph.add_edge('chart_generator_node','chart_agent_node')

        self.graph = graph.compile()

    
    def researcher_node(self,state:TAGraphState):
        res = self.researcher_agent.researcher_agent.invoke({'messages':state['messages']})

        structured_res = res['structured_response']
        message = AIMessage(structured_res.research_summary)

        return {'messages':[message],'researcher_structured_response':structured_res}

    def chart_generator_node(self,state:TAGraphState):
        
        researcher_response = state['researcher_structured_response']

        graph_generator = GraphGenerator(researcher_response,ticker_symbol=state['ticker_symbol'])
        base64_img = graph_generator.get_chart_img()

        message = HumanMessage(
            content=[
                {"type": "text", "text": f"Analyse the following chart, here is some orientations from the researcher analyst:\n{researcher_response.research_summary}"},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"},
                },
            ],
        )

        return {'messages':[message],'graph_generator':graph_generator}
        
    def chart_agent_node(self,state:TAGraphState) -> Command[Literal['researcher_node','__end__']]:

        res = self.chart_agent.chart_agent.invoke({'messages':state['messages']})['messages'][-1]#.content

        goto = '__end__'

        if isinstance(res,ToolMessage) and res.name == SEND_MSG_TOOL_NAME:
            res = HumanMessage( res.content)
            goto = 'researcher_node'

        
        # if res.content.upper().startswith('RESEARCH'):
        #     res = HumanMessage(res.content)
        #     goto = 'researcher_node'
        # elif not res.content.upper().startswith('REPORT'):
        #     print('Agent prefix is wrong, ending...')
        
        return Command(update={'messages':[res]},goto=goto)
        
        




        