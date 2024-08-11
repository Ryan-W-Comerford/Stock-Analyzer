from flask import Flask, render_template, request, redirect, url_for
import plotly
import json
from Model.ModelTrainer import ModelTrainer
from Stocks.StockData import StockData
import argparse

application = Flask(__name__)

@application.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ticker = request.form.get('ticker')
        return redirect(url_for('analysis', ticker=ticker))
    return render_template('index.html')

@application.route('/analysis/<ticker>')
def analysis(ticker):
    stock_data = StockData(alpha_key, ticker, api_flag)
    data = stock_data.retrieve_data()

    model_trainer = ModelTrainer(data)
    y_test, prediction, accuracy, value, strength = model_trainer.run_model()

    fig = model_trainer.plot(y_test, prediction, ticker)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder) 

    return render_template('analysis.html', graphJSON=graphJSON, value=value, ticker=ticker, accuracy=accuracy, strength=strength)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--api_flag', required=True)
    parser.add_argument('--alpha_key')
    args = parser.parse_args()

    api_flag = args.api_flag
    alpha_key = args.alpha_key if args.alpha_key else ""

    application.run(port=5001, debug=True)