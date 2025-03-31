from model.model_trainer import ModelTrainer
from stocks.stock_data import StockData
from stocks.api_info import ApiInfo
from flask import Flask, render_template, request, redirect, url_for
import plotly
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ticker = request.form.get('ticker')
        return redirect(url_for('analysis', ticker=ticker))
    return render_template('index.html')

@app.route('/analysis/<ticker>')
def analysis(ticker):
    api_flag, api_key = ApiInfo.get_api_info()
    print(api_key, ticker, api_flag)
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