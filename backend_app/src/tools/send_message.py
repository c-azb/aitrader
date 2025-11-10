
from langchain.tools import BaseTool
from pydantic import Field

SEND_MSG_TOOL_NAME = 'Send Message'


class SendMessageTool(BaseTool):

    name:str = SEND_MSG_TOOL_NAME
    description:str
    return_direct:bool=True

    # def _run(self, agent_id = Field(description=f'Agent to send the message'),message:str = Field('message to send to the agent')):
    #     return {'to':agent_id,'msg':message}
    def _run(self, message:str = Field('message to send to the agent')):
        return message