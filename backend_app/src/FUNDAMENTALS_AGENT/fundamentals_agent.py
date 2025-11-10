

from langchain.agents import create_agent
from src.LLMs.llms import LLMs
from src.tools.tavily_search_tool import tavily_search_tool
from src.tools.yfinance_tools import get_ticker_info,get_eps_trend

from langchain.agents.middleware import ToolCallLimitMiddleware

class FundamentalsAgent:
    def __init__(self,llms:LLMs):
        self.fundamentals_agent = create_agent(llms.llm_researcher,
                                          tools=[tavily_search_tool,get_ticker_info,get_eps_trend],
                                          middleware=[ToolCallLimitMiddleware(thread_limit=5,run_limit=5)],
                                          system_prompt=self.get_prompt())
    
    def get_prompt(self):
        return (
            "You are a finance fundamentals analyst. Your goal is to research about the requested asset and provide a " \
            "simplified and short report about investing in this asset looking at the fundamentals analysis point of view.\n" \
            "Your analysis together with other agents analysts will be reviwed by a manager to give a final decision about investing in the " \
            "financial asset."
        )

        