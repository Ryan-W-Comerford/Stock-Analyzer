from Model.ModelTrainer import ModelTrainer
from Stocks.StockInfo import StockInfo

if __name__ == "__main__":
    print("Welcome to Sarissa Solutions!")

    ticker = input("Please enter a valid ticker... ")
    API_flag = input("Where will this data come from (API or Local (Default))?... ")

    stock_data = StockInfo(ticker, API_flag)
    data = stock_data.retrieve_data()

    model_trainer = ModelTrainer(data)
    y_test, prediction, rmse = model_trainer.run_model()

    print("The RMSE is...")
    print(rmse)

    model_trainer.plot(y_test, prediction, ticker)
