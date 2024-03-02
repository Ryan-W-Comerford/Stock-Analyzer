import keras
import tensorflow as tf
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.utils import shuffle
import matplotlib.pyplot as plt
import numpy as np
import random
import pandas as pd
import plotly.express as px

class ModelTrainer:     
    def __init__(self, data):
        self.data = data
        self.target_columns = '4. close'
        self.feature_columns = ['TotalValue'] 

    def calculate_value(self, row):
        eps = 3.0
        surprise = 1.5
        revenue = 1.0
        debt_asset_ratio = -1.0
        gross_profit_margin = 2.0
        
        eps_value = float(row['reportedEPS']) * eps
        surprise_value = float(row['surprisePercentage']) * surprise
        revenue_value = float(row['totalRevenue']) * revenue
        debt_asset_ratio_value = (float(row['totalLiabilities']) / max(float(row['totalAssets']), 1)) * debt_asset_ratio
        gross_profit_margin_value = (float(row['grossProfit']) / max(float(row['totalRevenue']), 1)) * gross_profit_margin
        
        total_value = (eps_value + surprise_value + revenue_value
                        + debt_asset_ratio_value + gross_profit_margin_value)

        return total_value
    
    def prepare_data(self):
        self.data.fillna(0, inplace=True)
        self.data['TotalValue'] = self.data.apply(self.calculate_value, axis=1)

    def run_model(self):
        self.prepare_data()

        #set feature (X) and target (y) columns -> y is what you want to predict
        X = self.data[self.feature_columns]
        print(X)
        y = self.data[self.target_columns]
        print(y)

        #set the test data and then temp data to be paritioned more
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=random.randint(1,1000))
        
        #Fit with training data
        linear_model = LinearRegression()
        linear_model.fit(X_train, y_train)

        print("Testing...")
        #predict for the test
        prediction = linear_model.predict(X_test)

        #calculate MSE/RMSE for testing
        test_mse = mean_squared_error(y_test, prediction)
        test_rmse = np.sqrt(test_mse)

        print(f"Test RMSE is {test_rmse}")

        print(f"Test Values are...{y_test}")
        print(f"Predicted Values are...{prediction}")

        diff = ((prediction - y_test) / y_test) * 100
        accuracy = round(diff.mean(), 2)

        if accuracy < 0:
            value = 'Over'
            if accuracy > -20:
                strength = 'Slightly'
            else:
                strength = 'Strongly'
        else:
            value = 'Under'
            if accuracy < 20:
                strength = 'Slightly'
            else:
                strength = 'Strongly'

        return y_test, prediction, accuracy, value, strength

    @staticmethod
    def plot(y_test, y_pred, ticker):
        # Create a DataFrame using x_values and y_values
        data = pd.DataFrame({
            'Actual Stock Price': y_test,
            'Predicted Stock Price': y_pred
        })

        fig = px.scatter(data, x='Actual Stock Price', y='Predicted Stock Price', title=f'Actual vs. Predicted Stock Price for {ticker}', color_discrete_sequence=['white'])

        fig.update_layout({
            'title': {
                'text': f'Actual vs. Predicted Stock Price for {ticker}',
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'color': 'white', 'family': "Exo 2, sans-serif"}
            },
            'xaxis': {
                'title': {'text': 'Actual Stock Price', 'font': {'color': 'white', 'family': "Exo 2, sans-serif"}},
                'tickfont': {'color': 'white', 'family': "Exo 2, sans-serif"},
                'showgrid': False
            },
            'yaxis': {
                'title': {'text': 'Predicted Stock Price', 'font': {'color': 'white', 'family': "Exo 2, sans-serif"}},
                'tickfont': {'color': 'white', 'family': "Exo 2, sans-serif"},
                'showgrid': False
            },
            'legend': {
                'font': {'color': 'white', 'family': "Exo 2, sans-serif"},
                'bgcolor': 'rgba(0,0,0,0)'
            },
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': 'rgba(0,0,0,0)',
        })

        return fig