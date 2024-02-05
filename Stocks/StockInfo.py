from alpha_vantage.timeseries import TimeSeries
from pandas import json_normalize
import pandas as pd
import requests
import json
import yfinance as yf

ALPHA_API_KEY = 'G19UUP8U9FI78HPZ'

class StockInfo: 
    def __init__(self, ticker, API_flag):
        self.ticker = ticker
        self.API_flag = API_flag
        self.URL = 'https://www.alphavantage.co'
        self.EARNINGS_URL = self.URL + "/query?function=EARNINGS&symbol=" + self.ticker + "&apikey=" + ALPHA_API_KEY 

    def Local_Data(self):
        path = 'InputData/' + self.ticker + '.csv'
        try:
            data = pd.read_csv(path)
        except Exception as e:
            raise Exception(e)

        return data

    def API_Data(self):
        ts = TimeSeries(key=ALPHA_API_KEY, output_format='pandas')
        try:
            stock_data, stock_meta_data = ts.get_daily(symbol=self.ticker, outputsize='full')
            raw_stock_file = f'RawData/{self.ticker}_Stock_Price.csv'
            stock_data.to_csv(raw_stock_file)

            earnings_request = requests.get(self.EARNINGS_URL)
            earings_json = earnings_request.json()
            earings_json = earings_json['quarterlyEarnings']
            earnings_data = json_normalize(earings_json)
            raw_earnings_file = f'RawData/{self.ticker}_Earnings.csv'
            earnings_data.to_csv(raw_earnings_file)
        except Exception as e:
            raise Exception(e)
        
        print("The Raw Stock Price Info is...")
        print(stock_data)

        print("The Raw Earnings Info is...")
        print(earnings_data)

        earnings_data['date'] = pd.to_datetime(earnings_data['reportedDate'])

        data = pd.merge(stock_data, earnings_data, left_on=stock_data.index, right_on='reportedDate', how='inner')
        print("Merge Data is...")
        print(data)

        merged_file_name = f'InputData/{self.ticker}.csv'
        data.to_csv(merged_file_name)

        print("Final Training Data is...")
        print(data)

        return data

    def retrieve_data(self):
        if self.API_flag.lower() == 'api':
            data = self.API_Data()
        else:
            data = self.Local_Data()

        return data