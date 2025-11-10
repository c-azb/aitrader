
from langchain.agents import create_agent
# from langchain.agents.middleware import ToolCallLimitMiddleware
from src.LLMs.llms import LLMs
from src.tools.send_message import SendMessageTool

class ChartAgent:

    def __init__(self,llms:LLMs):

        send_message_tool = SendMessageTool(
                    description= (
                        'Send a message to the researcher technical analyst to request information to enhance your chart analysis.'
                        #'\nagent_id options: [RESEARCHER]'
                    ) )

        self.chart_agent = create_agent(
            model=llms.llm_charting,
            # tools=[send_message_tool],
            system_prompt=self.get_prompt()
        )
    
    def get_prompt(self):
        return (
            "You are a technical analysis analyst working with a researcher.\n"
            "Your job is to analyse a financial candle stick chart image and provide a complete technical analysis report with "
            "possible entries, exits or wait until something happens, etc...\n"
            "Your report together with other analysts reports will be reviwed by the manager to take investement decisions."
        )
    


    




