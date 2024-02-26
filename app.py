from flask import Flask, render_template, request, redirect, url_for
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import plotly
import json
from Model.ModelTrainer import ModelTrainer
from Stocks.StockData import StockData

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ticker = request.form.get('ticker')
        return redirect(url_for('analysis', ticker=ticker))
    return render_template('index.html')

@app.route('/analysis/<ticker>')
def analysis(ticker):
    API_flag = 'no'
    stock_data = StockData(ticker, API_flag)
    data = stock_data.retrieve_data()

    model_trainer = ModelTrainer(data)
    y_test, prediction, accuracy, value, strength = model_trainer.run_model()

    fig = model_trainer.plot(y_test, prediction, ticker)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder) 

    return render_template('analysis.html', graphJSON=graphJSON, value=value, ticker=ticker, accuracy=accuracy, strength=strength)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
