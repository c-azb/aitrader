
from langchain_tavily import TavilySearch
from langchain.tools import tool

@tool
def tavily_search_tool(query:str):#,date:str
    ''' Search the internet for information about finance topics '''
    tavily_search = TavilySearch(max_results=1,topic="general")#finance

    results = tavily_search.invoke(query)

    data = 'no results found' if len(results['results']) == 0 else ''

    for result in results['results']:
        data += (
            f"Title: {result['title']}\n"
            f"{result['content']}\n\n"
        )
    
    return data.strip()
        
    

