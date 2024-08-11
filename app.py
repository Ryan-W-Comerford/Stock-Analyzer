from flask import Flask, render_template, request, redirect, url_for
import plotly
import json
from Model.ModelTrainer import ModelTrainer
from Stocks.StockData import StockData
import argparse

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ticker = request.form.get('ticker')
        return redirect(url_for('analysis', ticker=ticker))
    return render_template('index.html')

@app.route('/analysis/<ticker>')
def analysis(ticker):
    stock_data = StockData(api_key, ticker, api_flag)
    data = stock_data.retrieve_data()

    model_trainer = ModelTrainer(data)
    y_test, prediction, accuracy, value, strength = model_trainer.run_model()

    fig = model_trainer.plot(y_test, prediction, ticker)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder) 

    return render_template('analysis.html', graphJSON=graphJSON, value=value, ticker=ticker, accuracy=accuracy, strength=strength)

@app.errorhandler(Exception)
def handle_exception(e):
    return render_template("error.html", e=e), 500

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--api_flag', required=True)
    parser.add_argument('--api_key')
    args = parser.parse_args()

    api_flag = args.api_flag
    api_key = args.api_key if args.api_key else ""

    app.run(port=5001, debug=True)