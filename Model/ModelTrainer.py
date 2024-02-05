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

class ModelTrainer:     
    def __init__(self, data):
        self.data = data
        self.target_columns = 'reportedEPS' 
        self.feature_columns = ['4. close', '5. volume', 'surprise', 'surprisePercentage'] 

    def run_model(self):
        self.data.replace('None', pd.NA, inplace=True)
        self.data.dropna(subset=[self.target_columns] + self.feature_columns, inplace=True)

        #set feature (X) and target (y) columns -> y is what you want to predict
        X = self.data[self.feature_columns]
        y = self.data[self.target_columns]

        #set the test data and then temp data to be paritioned more
        X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.2, random_state=random.randint(1,1000))

        #now set the train variables and validation variables to prevent overfitting
        X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.25, random_state=random.randint(1,1000)) 
        
        #Fit with training data
        linear_model = LinearRegression()
        linear_model.fit(X_train, y_train)
        
        #predict on the validation data again to prevent overfitting
        val_prediction = linear_model.predict(X_val)
        
        #calculate MSE/RMSE for validation
        val_mse = mean_squared_error(y_val, val_prediction)
        val_rmse = np.sqrt(val_mse)
        print(f"Validation RMSE: {val_rmse}")

        #predict for the final test
        prediction = linear_model.predict(X_test)

        #calculate MSE/RMSE for testing
        test_mse = mean_squared_error(y_test, prediction)
        test_rmse = np.sqrt(test_mse)
        print(f"Test RMSE: {test_rmse}")
            
        return y_test, prediction, test_rmse

    @staticmethod
    def plot(y_test, y_pred, ticker):
        plt.scatter(y_test, y_pred)
        plt.xlabel("Actual EPS")
        plt.ylabel("Predicted EPS")
        plt.title(f"Actual vs. Predicted EPS for {ticker}")
        plt.show()