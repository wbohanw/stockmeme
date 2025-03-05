# Filename - server.py

# Import necessary modules
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from search import search_google, ask_chatgpt, preprocess_news, process_json
from load_csv import get_daily_stock_data, get_intraday_stock_data

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Route for retrieving data
@app.route('/result/<path:query>/<model>')
def get_result(query, model):
    symbol = query

    try:
        news = search_google(symbol)
        processed_news = preprocess_news(news)
        print("--------------------------------news processed--------------------------------")

        daily_data = get_daily_stock_data(symbol)
        print("--------------------------------daily data fetched--------------------------------")

        min15_data = get_intraday_stock_data(symbol)
        print("--------------------------------intraday data fetched--------------------------------")

        response = ask_chatgpt(symbol, processed_news, model, daily_data, min15_data)
        print("--------------------------------response fetched--------------------------------")
        print(response)

        analysis = process_json(response)
        print("--------------------------------analysis fetched--------------------------------")
        print(analysis)
        return analysis

    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        print("Raw response:")
        print(analysis)
        return {"error": "Failed to parse JSON"}


@app.route('/test/<model>')
def test(model):
    symbol = "MSFT"
    try:
        news = search_google(symbol)
        processed_news = preprocess_news(news)
        print("--------------------------------news processed--------------------------------")

        with open('daily_stock_data.csv', 'r') as daily_file:
            daily_data = daily_file.read()
        print("--------------------------------daily data fetched--------------------------------")

        with open('intraday_stock_data.csv', 'r') as intraday_file:
            min15_data = intraday_file.read()
        print("--------------------------------intraday data fetched--------------------------------")

        response = ask_chatgpt(symbol, processed_news, model, daily_data, min15_data)
        print("--------------------------------response fetched--------------------------------")
        print(response)

        analysis = process_json(response)
        print("--------------------------------analysis fetched--------------------------------")
        print(analysis)
        return analysis

    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        print("Raw response:")
        print(analysis)
        return {"error": "Failed to parse JSON"}
# Run the app
if __name__ == '__main__':
    app.run(debug=True)