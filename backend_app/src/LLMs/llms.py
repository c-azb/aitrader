
# from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from typing import Literal



class LLMs:
    def __init__(self,researcher_llm,charting_llm,manager_llm):
        self.llm_researcher = researcher_llm
        self.llm_charting = charting_llm
        self.llm_manager = manager_llm
    

    @staticmethod
    def get_model(model,reasoning='none',source='groq',temperature=0.7):
        if source=='groq':
            return ChatGroq(model=model,temperature=temperature,reasoning_effort=reasoning,reasoning_format='hidden' if reasoning else None)
        # elif source=='ollama':
        #     return ChatOllama(base_url='localhost:11434',model=model,reasoning=reasoning,temperature=temperature)
        return None

    @staticmethod
    def get_default(id:Literal['agent','vision','manager','agent2','vision2','manager2']):
        if id == 'agent':
            return LLMs.get_model(model='qwen/qwen3-32b')
        elif id=='vision':
            return LLMs.get_model(model='meta-llama/llama-4-scout-17b-16e-instruct',reasoning=None)
        elif id=='manager':
            return LLMs.get_model(model='llama-3.1-8b-instant')
        if id == 'agent2':
            return LLMs.get_model(model='qwen3:8b',reasoning=False,source='ollama')
        elif id=='manager2':
            return LLMs.get_model(model='qwen3:8b',reasoning=False,source='ollama')
        elif id=='vision2':
            return LLMs.get_model(model='llava:7b',reasoning=False,source='ollama')
            
