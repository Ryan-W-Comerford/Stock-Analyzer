# Stock Analyzer

## Description
This is a simple stock predictor, it will call an API to get raw financial data for a particular ticker, clean the data, calculate a feature value based on the financials, and predict the price based on that feature value. It will then show the model's results in graphical form. 

This is a high-level design and implementation meant to show my understanding of python, the libraries involved (such as pandas, sklearn, flask, and more), and other development topics like APIs.

To run the local project, you can either set the api flag as "yes" and contact the API to get the most up-to-date data or you can set the api flag as "no" and rely on the local CSV data that exists in this repository.

If api flag is "no" the given ticker's CSV data must exist to be successful. If api flag is "yes" you must get a free api key from the Alpha Vantage website. To create your own free key visit their website https://www.alphavantage.co/. This API does have per day limits and can halt the program if limit is exceeded.

## How To Run
``` python
#If using the API
python3 main.py --api_flag yes --api_key YOUR_ALPHA_API_KEY
#If using Local Data
python3 main.py --api_flag no
```
