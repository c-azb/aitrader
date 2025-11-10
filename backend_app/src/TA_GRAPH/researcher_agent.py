



from langchain.agents import create_agent
from src.LLMs.llms import LLMs
from src.tools.tavily_search_tool import tavily_search_tool
from pydantic import BaseModel,Field
from langchain.agents.middleware import ToolCallLimitMiddleware
from langchain.agents.structured_output import ToolStrategy


class ResearcherAgent:

    def __init__(self,llms:LLMs):
        
        self.researcher_agent = create_agent(
            model=llms.llm_researcher,
            tools=[ tavily_search_tool ],
            system_prompt=self.get_researcher_prompt(),
            response_format=ToolStrategy(ResearcherResponse),
            middleware=[ToolCallLimitMiddleware(thread_limit=5,run_limit=5)]
        )
    
    def get_researcher_prompt(self):
        return (
            "You are a technical analysis researcher working with a team of analysts.\n"
            "Your job is to search about the requested asset and define which " \
            "chart time frame it should be used, how much past data we should look at from today, " \
            "which technical indicators we should add to the chart and a final summary of your research to your partner.\n" \
            "Your answer will be used to create a candlestick chart to be analysed.\n"
            "Here is the units you should use for each parameter:\n" \
            "time_frame: [1m,5m,15m,1h,4h,1d]\n" \
           # "past_data: X where X is the number of days (it can be decimal also)\n" \
            "indicators: Write the technical indicators and their respective parameters you recommend to be added.\n"
            "Indicators options are the following:"
            "Simple moving average, format: {'Name': 'SMA', 'length': x}\n"
            "Exponential moving average, format: {'Name': 'EMA', 'length': x}\n"
            "Relative Strength Index, format: {'Name': 'RSI', 'length': x}\n"
            "Make sure to pick only indicators that adds relevant information avoiding picking multiple indicators that gives the same information."
            #"Bollinger Bands, format: {'Name': 'BB', 'length': x, 'std': y}\n"
            #"Moving Average Convergence Divergence, format: {'Name': 'MACD', 'fast': x, 'slow': y, 'signal': z}\n"
          #  "Stochastic RSI, format: {'Name': 'stochrsi','length':x,'rsi_length':y,'k':z,'d':a}\n"
            
        )

class ResearcherResponse(BaseModel):
    time_frame: str = Field(description='each candle stick time representation')
    #past_data: float = Field(description='how much data from today we should look at in days?')

    indicators: list[dict] = Field(description='Indicators to be added to the chart')
    research_summary: str = Field(description='Research summary')



