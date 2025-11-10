
from langchain.tools import tool#,BaseTool
import yfinance as yf
from pydantic import Field

# class YFinanceTools(BaseTool):
#     name:str='stocks fundamentals'
#     description:str = "Retrieve fundamentals data about a stock ticker symbol"
    
#     def _run(ticker_symbol,data=[]):



@tool
def get_ticker_info(ticker_symbol:str = Field(description='ticker symbol')):
    ''' Returns ticker fundamentals information like ratios, prices, sector, etc... '''

    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info

    del_keys = ['zip','website','industryKey','industryDisp','irWebsite','tradeable','financialCurrency','language','region','typeDisp',
               'quoteSourceName','displayName','cryptoTradeable','market','address1','city','state','phone','sectorKey','sectorDisp',
                'shortName','esgPopulated','hasPrePostMarketData','firstTradeDateMilliseconds',
                 'companyOfficers' ]
    for k in del_keys:
        info.pop(k,None)
    
    return info


@tool
def get_eps_trend(ticker_simbol:str = Field(description='ticker symbol')):
    ''' Returns a dictionary of the earnings per share trend '''
    ticker = yf.Ticker(ticker_simbol)
    return ticker.get_eps_trend(as_dict=True)

# @tool
# def get_calendar(ticker_simbol):
#     ''' Returns a dictionary of events, earnings, and dividends for the ticker '''
#     ticker = yf.Ticker(ticker_simbol)
#     return ticker.calendar

# @tool
# def get_analyst_price_targets(ticker_simbol):
#     ticker = yf.Ticker(ticker_simbol)
#     return ticker.analyst_price_targets