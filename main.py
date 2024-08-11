from Stocks.ApiInfo import ApiInfo
from app import app
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--api_flag', required=True)
    parser.add_argument('--api_key')
    args = parser.parse_args()

    ApiInfo.api_flag = args.api_flag
    ApiInfo.api_key = args.api_key

    app.run(port=5001, debug=True)