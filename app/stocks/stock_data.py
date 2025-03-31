from pandas import json_normalize
import pandas as pd
import requests
import json

class StockData: 
    def __init__(self, alpha_api_key, ticker, api_flag):
        self.ticker = ticker
        self.api_flag = api_flag
        self.URL = 'https://www.alphavantage.co'
        self.STOCK_URL = self.URL + "/query?function=TIME_SERIES_DAILY&symbol=" + self.ticker + "&apikey=" + alpha_api_key + "&outputsize=full"
        self.EARNINGS_URL = self.URL + "/query?function=EARNINGS&symbol=" + self.ticker + "&apikey=" + alpha_api_key 
        self.INFO_URL = self.URL + "/query?function=OVERVIEW&symbol=" + self.ticker + "&apikey=" + alpha_api_key
        self.INCOME_URL = self.URL + "/query?function=INCOME_STATEMENT&symbol=" + self.ticker + "&apikey=" + alpha_api_key 
        self.BALANCE_URL = self.URL + "/query?function=BALANCE_SHEET&symbol=" + self.ticker + "&apikey=" + alpha_api_key 
        self.CASH_URL = self.URL + "/query?function=CASH_FLOW&symbol=" + self.ticker + "&apikey=" + alpha_api_key  

    def retrieve_data(self):
        return self.api_data() if self.api_flag.lower() == 'yes' else self.local_data()

    def local_data(self):
        try:
            path = 'data/InputData/' + self.ticker + '.csv'
            data = pd.read_csv(path)
        except Exception as e:
            raise Exception(f"Error reading local data for ticker '{self.ticker}'...Please ensure that ticker's data exists")

        return data

    def api_data(self):
        try:
            stock_request = requests.get(self.STOCK_URL)
            stock_json = stock_request.json()
            print(stock_json)
            if "Information" in stock_json:
                if "rate limit" in stock_json["Information"]:
                    raise Exception("API Limit Has Been Reached for this API Key. Try Re-Running App using Local Data.")
            stock_json = stock_json['Time Series (Daily)']
            stock_data = pd.DataFrame(stock_json).T
            stock_data.reset_index(inplace=True)
            stock_data.rename(columns={'index': 'date'}, inplace=True)
            stock_data.index = range(1, len(stock_data) + 1)
            raw_stock_file = f'Data/RawData/{self.ticker}_Stock_Price.csv'
            stock_data['Date'] = pd.to_datetime(stock_data['date'])
            stock_data['Quarter'] = stock_data['Date'].dt.to_period('Q')
            stock_data.drop('date', axis=1, inplace=True)
            stock_data.drop('Date', axis=1, inplace=True)
            for column in stock_data.columns:
                if column != 'Quarter':
                    stock_data[column] = pd.to_numeric(stock_data[column], errors='coerce')
            stock_data =  stock_data.groupby('Quarter').mean().reset_index()
            stock_data.to_csv(raw_stock_file)

            earnings_request = requests.get(self.EARNINGS_URL)
            earings_json = earnings_request.json()
            earings_json = earings_json['quarterlyEarnings']
            earnings_data = json_normalize(earings_json)
            raw_earnings_file = f'Data/RawData/{self.ticker}_Earnings.csv'
            earnings_data['Quarter'] = pd.to_datetime(earnings_data['reportedDate']).dt.to_period('Q')
            earnings_data.drop(columns=['reportedDate'], inplace=True)
            earnings_data.drop(columns=['fiscalDateEnding'], inplace=True)
            earnings_data.to_csv(raw_earnings_file)

            income_request = requests.get(self.INCOME_URL)
            income_json = income_request.json()
            income_json = income_json['quarterlyReports']
            income_data = json_normalize(income_json)
            raw_income_file = f'Data/RawData/{self.ticker}_Income.csv'
            income_data['Quarter'] = pd.to_datetime(income_data['fiscalDateEnding']).dt.to_period('Q')
            income_data.drop(columns=['fiscalDateEnding'], inplace=True)
            income_data.to_csv(raw_income_file)

            balance_request = requests.get(self.BALANCE_URL)
            balance_json = balance_request.json()
            balance_json = balance_json['quarterlyReports']
            balance_data = json_normalize(balance_json)
            raw_balance_file = f'Data/RawData/{self.ticker}_Balance.csv'
            balance_data['Quarter'] = pd.to_datetime(balance_data['fiscalDateEnding']).dt.to_period('Q')
            balance_data.drop(columns=['fiscalDateEnding'], inplace=True)
            balance_data.to_csv(raw_balance_file)

            cash_request = requests.get(self.CASH_URL)
            cash_json = cash_request.json()
            cash_json = cash_json['quarterlyReports']
            cash_data = json_normalize(cash_json)
            raw_cash_file = f'Data/RawData/{self.ticker}_Cash.csv'
            cash_data['Quarter'] = pd.to_datetime(cash_data['fiscalDateEnding']).dt.to_period('Q')
            cash_data.drop(columns=['fiscalDateEnding'], inplace=True)
            cash_data.to_csv(raw_cash_file)
        except Exception as e:
            raise Exception(e)
        
        print("The Raw Stock Price Info is...")
        print(stock_data)

        print("The Raw Earnings Info is...")
        print(earnings_data)

        print("The Raw Income Info is...")
        print(income_data)

        print("The Raw Balance Info is...")
        print(balance_data)

        print("The Raw Cash Info is...")
        print(cash_data)

        data = pd.merge(stock_data, earnings_data, on='Quarter', how='outer', sort=True)
        data = pd.merge(data, income_data, on='Quarter', how='outer', sort=True)
        data = pd.merge(data, balance_data, on='Quarter', how='outer', sort=True)
        data = pd.merge(data, cash_data, on='Quarter', how='outer', sort=True)
        
        data = data.dropna()

        print("Merge Data is...")
        print(data)

        merged_file_name = f'data/InputData/{self.ticker}.csv'
        data.to_csv(merged_file_name)

        print("Final Training Data is...")
        print(data)

        return data