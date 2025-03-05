from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

import os
from googlesearch import search
import json
from openai import OpenAI
from load_csv import load_csv
import datetime

# Load prompt from file
with open("prompt2.txt") as f:
    prompt = f.read()

import requests
import os
from openai import OpenAI
# Replace with your OpenRouter API key
symbol = "MSFT"
news = "[' Microsoft (NASDAQ: MSFT) recently announced plans to spend $80 billion this year building out AI data centers to support training advanced AI models and\xa0... ', ' MSFT has a High Technical Rating by Nasdaq Dorsey Wright. Discover why technical analysis matters. $408.21. -7.92. -1.90%. Feb 22, 2025. ', ' Get Microsoft Corp (MSFT:NASDAQ) real-time stock quotes, news, price and financial information from CNBC. ', ' This year, our flagship conference, ESPC, will bring the Microsoft 365 community together from 1 – 4 Dec, 2025 in the CCD Dublin. ', ' Explore our biggest and most spectacular events, with industry thought leaders, innovative ideas, and chances to connect with the worldwide community. ', ' Feb 3, 2025  ·  Here's your guide to all the IT training sessions, partner meet-ups and annual Microsoft conferences you won\'t want to miss. ']"
daily_data = load_csv('daily_stock_data.csv')
min15_data = load_csv('intraday_stock_data.csv')

json_schema = {
    "type": "object",
    "properties": {
        "2_week_prediction": {"type": "string"},
        "1_month_prediction": {"type": "string"},
        "expected_price_range": {
            "type": "object",
            "properties": {
                "2_weeks": {"type": "string"},
                "1_month": {"type": "string"}
            }
        },
        "options_suggestion": {
            "type": "object",
            "properties": {
                "strategy": {"type": "string"},
                "details": {
                    "type": "object",
                    "properties": {
                        "call_option": {"type": "string"},
                        "put_option": {"type": "string"}
                    }
                },
                "message": {"type": "string"}
            }
        }
    }
}

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY"),
)
today = datetime.datetime.now().strftime("%Y-%m-%d")

completion = client.chat.completions.create(
  extra_headers={
    "HTTP-Referer": "https://stockmeme.com", # Optional. Site URL for rankings on openrouter.ai.
    "X-Title": "StockMeme", # Optional. Site title for rankings on openrouter.ai.
  },
  extra_body={},
  model="deepseek/deepseek-r1:free",
            messages=[

                {"role": "user", "content": f"Prompt: {prompt}\nStock: {symbol}\nDate: {today}\nNews: {news}\nDaily Data: {daily_data}\n15min Data: {min15_data}"}
            ],
            response_format={
    "type": "object",
    "properties": {
        "2_week_prediction": {"type": "string"},
        "1_month_prediction": {"type": "string"},
        "expected_price_range": {
            "type": "object",
            "properties": {
                "2_weeks": {"type": "string"},
                "1_month": {"type": "string"}
            }
        },
        "options_suggestion": {
            "type": "object",
            "properties": {
                "strategy": {"type": "string"},
                "details": {
                    "type": "object",
                    "properties": {
                        "call_option": {"type": "string"},
                        "put_option": {"type": "string"}
                    }
                },
                "message": {"type": "string"}
            }
        }
    }
}
)

response = completion.choices[0].message.content
print(response)
try:
    # Handle possible markdown code block formatting
    if response.startswith('```json'):
        # Extract JSON from code block
        json_str = '\n'.join(response.split('\n')[1:-1])
    else:
        json_str = response
        
    # Parse the JSON
    analysis = json.loads(json_str)
    print("Successfully parsed JSON:")
    print(json.dumps(analysis, indent=2))
    
except json.JSONDecodeError as e:
    print(f"Failed to parse JSON: {e}")
    print("Raw response:")
    print(response)
