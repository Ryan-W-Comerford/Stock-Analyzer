import keras
import tensorflow as tf
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from alpha_vantage.timeseries import TimeSeries
import quandl
import yfinance
import requests
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import json_normalize

ALPHA_API_KEY = 'DRARW0D5KAPAPOVY' 

class Sarissa: 
    def __init__(self, ticker):
        self.ticker = ticker
        self.EARNINGS_URL = "https://www.alphavantage.co/query?function=EARNINGS&symbol=" + self.ticker + "&apikey=" + ALPHA_API_KEY 

    def call_API(self):
        ts = TimeSeries(key=ALPHA_API_KEY, output_format='pandas')
        try:
            stock_data, stock_meta_data = ts.get_daily(symbol=self.ticker, outputsize='full')

            earnings_request = requests.get(self.EARNINGS_URL)
            earings_json = earnings_request.json()
            earings_json = earings_json['quarterlyEarnings']
            earnings_data = json_normalize(earings_json)

        except Exception as e:
            raise Exception(e)
        print(stock_data)
        print(earnings_data)
        return stock_data, earnings_data
    
    def retrieve_data(self):
        stock_data, earnings_data = self.call_API()

        stock_data.index = pd.to_datetime(stock_data.index)
        earnings_data['date'] = pd.to_datetime(earnings_data['reportedDate'])
        
        merged_df = pd.merge(stock_data, earnings_data, left_on=stock_data.index, right_on='date', how='inner')
        print(merged_df)

        merged_df['date']= pd.to_datetime(merged_df['date'])

        train_data = merged_df[merged_df['date'] <= '2020-12-31']
        test_data = merged_df[merged_df['date'] >= '2021-01-01']

        num_rows_train = len(train_data)
        num_rows_test = len(test_data)

        if num_rows_test != num_rows_train:
            train_data = train_data.sample(n=num_rows_test, random_state=42)

        print(train_data)
        print(test_data)
        return train_data, test_data

    def train_model(self):
        target_column = 'reportedEPS' 
        feature_columns = ['1. open', '2. high', '3. low', '4. close', '5. volume', 'surprise'] 

        train_data, test_data = self.retrieve_data()

        X = train_data[feature_columns]
        y = test_data[target_column]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = LinearRegression()
        model.fit(X_train, y_train)
        prediction = model.predict(X_test)
        mse = mean_squared_error(y_test, prediction)

        rmse = np.sqrt(mse)
        print(rmse)

        self.plot(y_test, prediction)

    def plot(self, y_test, y_pred):
        plt.scatter(y_test, y_pred)
        plt.xlabel("Actual Values")
        plt.ylabel("Predicted Values")
        plt.title("Actual vs. Predicted Values")
        plt.show()