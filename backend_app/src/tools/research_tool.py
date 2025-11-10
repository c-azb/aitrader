
# from langchain.tools import BaseTool
# import yfinance as yf

# class YFinanceSearch(BaseTool):
#     name:str = 'YahooFinanceSearch'
#     description:str = 'Search for finance news in the yahoo finance platform.'
#     news_count:int = 3

#     def _run(self, query):
#         full_data = ''
#         news_results = yf.Search(query=query,news_count = self.news_count).news

#         for result in news_results:
#             full_data += (
#                 f"Title: {result['title']}"
#             )
