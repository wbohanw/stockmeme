# Filename - server.py

# Import flask, CORS, and datetime module for showing date and time
from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
from search import search_google
from load_csv import load_csv
from search import ask_chatgpt

# Initializing flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


# Route for seeing a data
@app.route('/result/<path:query>')
def get_result(query):
    # Flask automatically URL-decodes the query parameter
    # Now handles spaces (%20) and special characters properly
    symbol = query
    # Example Usage
    news = search_google(symbol)
    daily_data = load_csv('daily_stock_data.csv')
    min15_data = load_csv('intraday_stock_data.csv')
    response = ask_chatgpt(symbol, news, daily_data, min15_data)
    return jsonify(response)

# Running app
if __name__ == '__main__':
    app.run(debug=True)