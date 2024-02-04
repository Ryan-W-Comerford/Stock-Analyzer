from sarissa import Sarissa

if __name__ == "__main__":
    print("Welcome to Sarissa Solutions!")
    ticker = input("Please enter a valid ticker... ")
    sarissa = Sarissa(ticker)
    sarissa.train_model()
