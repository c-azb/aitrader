


from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from src.MAIN_GRAPH.main_graph import MainGraph,LLMs,State

class AnalyseAssetModel(BaseModel):
    # query:str
    ticker_symbol:str


graph_router = APIRouter(
    prefix='/trader_agent'
)

@graph_router.post('')
async def analyze_asset(user_input:AnalyseAssetModel):
    llms = LLMs(researcher_llm=LLMs.get_default('agent'),
            charting_llm=LLMs.get_default('vision'),
            manager_llm=LLMs.get_default('manager') )
    main_graph = MainGraph(llms)

    initial_state = State.get_initial_state(f'Analyze {user_input.ticker_symbol}',user_input.ticker_symbol)
    res = main_graph.graph.invoke( initial_state )

    if len(res['messages']) >= 4 and 'graph_generator' in res:
        return {
            # 'msgs': [msg.content for msg in res['messages'][1:-1]],
            'manager_response': res['messages'][-1].content,
            'chart_img': res['graph_generator'].get_chart_img()
        }

    # return {'graph_error':'agent has failed to generate analysis'}
    return HTTPException(status_code=500,detail='graph has failed to generate analysis')