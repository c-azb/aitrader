
from datetime import datetime,timedelta,timezone

import mplfinance as mpf
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import io
import base64

from src.TA_GRAPH.researcher_agent import ResearcherResponse


class GraphGenerator:
    def __init__(self, graph_setup: ResearcherResponse,ticker_symbol:str):

        start_date = self.get_start_date(graph_setup.time_frame)
        end_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        df = yf.download(ticker_symbol, start=start_date, end=end_date,interval=graph_setup.time_frame,auto_adjust=False)
        df.columns =[c[0].lower() for c in df.columns]

        self.add_plots = []

        self.add_technical_indicators(graph_setup.indicators,df)

        self.df = df

        
    
    def get_start_date(self,time_frame):
        
        if time_frame == '1m': past_time = 2
        else: past_time = {'h':30,'d':300}.get( time_frame[-1].lower(),7)

         
        date = datetime.now(timezone.utc) - timedelta(days=past_time)
        return date.strftime('%Y-%m-%d')
    
    def add_technical_indicators(self,indicators,df):

        width=0.7

        for indicator in indicators:

            col_name = indicator['Name'] + '(' + ','.join( [str(v) for k,v in indicator.items() if k != 'Name'] ) + ')'

            if indicator['Name'] == 'SMA':
                df[col_name] = ta.sma(df.close,int(indicator['length']) )
                self.add_plots.append(mpf.make_addplot(df[col_name], panel=0, label=col_name,width=width))

            elif indicator['Name'] == 'EMA':
                df[col_name] = ta.ema(df.close,int(indicator['length']) )
                self.add_plots.append(mpf.make_addplot(df[col_name], panel=0, label=col_name,width=width))

            elif indicator['Name'] == 'RSI':
                df[col_name] = ta.rsi(df.close,int(indicator['length']) )
                self.add_plots += [
                    mpf.make_addplot(df[col_name], panel=2, color='blue', ylabel=col_name,width=width),
                    mpf.make_addplot([70]*len(df), panel=2, color='red', linestyle='--', width=width,secondary_y=False), # Overbought line
                    mpf.make_addplot([30]*len(df), panel=2, color='green', linestyle='--', width=width,secondary_y=False) # Oversold line
                ]

            # elif indicator['Name'] == 'BB':
            #     df[col_name] = ta.bbands(df.close,int(indicator['length']),float(indicator['std']),float(indicator['std']) )
            # elif indicator['Name'] == 'MACD':
            #     df[col_name] = ta.macd(df.close,int(indicator['fast']),int(indicator['slow']),int(indicator['signal']) )
            else:
                print('unknown',indicator['Name'])

    def plot_chart(self):
        mpf.plot(self.df, type='candle',style='yahoo',addplot=self.add_plots,volume=True)
    
    def get_chart_img(self):
        buffer = io.BytesIO()
        mpf.plot(self.df, type='candle', style='yahoo', addplot=self.add_plots,volume=True, 
                 savefig=dict(fname=buffer, format='jpeg'))#figscale=1.5,
        
        buffer.seek(0)
        image_data = buffer.read()
        return base64.b64encode(image_data).decode('utf-8')