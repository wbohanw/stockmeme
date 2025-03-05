from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

import threading
import os
from googlesearch import search
import json
from openai import OpenAI
from load_csv import load_csv
import datetime

import itertools
import sys
import time
# Load prompt from file
with open("prompt2.txt") as f:
    prompt = f.read()

# Initialize Deepseek client at the top level
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Initialize another client for preprocessing search results
client2 = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY"),
)

def search_google(query):
    """Fetches real-time search results from Google using the googlesearch library."""
    q1 = f"what is the latest news and of {query}"
    q2 = f"{query} events(meeting, conference) happening in future"
    results = []
    try:
        search_results = search(q1, advanced=True, num_results=5)
        search_results2 = search(q2, advanced=True, num_results=5)
        results.extend([result.description for result in search_results])
        results.extend([result.description for result in search_results2 if result.description not in results])
        return results
    except Exception as e:
        print(f"Search error: {e}")
        return ["Search service unavailable."]

def preprocess_news(news_list):
    """Preprocesses news into bullnews and bearnews with each news summarized to 2-3 words."""
    response = client2.chat.completions.create(
  model="deepseek/deepseek-chat:free",
        messages=[
            {"role": "user", "content": f"Preprocess the following news and events into bull and bear, summarizing each to 4-6 words and return in json format, if there is dates, include them: {news_list}"}
        ],
    )
    return response.choices[0].message.content

def ask_chatgpt(symbol, news, model, daily_data, min15_data):
    if model == "deepseek-r1":
        model = "deepseek/deepseek-r1:free"
    elif model == "deepseek-v3":
        model = "deepseek/deepseek-chat:free"


    elif model == "gemini-flash-lite-2.0":
        model="google/gemini-2.0-flash-lite-preview-02-05:free"
    elif model == "gemini-flash-thinking-exp":
        model="google/gemini-2.0-flash-thinking-exp:free"
    elif model == "gemini-pro-2.0":
        model="google/gemini-2.0-pro-exp-02-05:free",
    
    else:
        model = "deepseek/deepseek-chat:free"
    """Queries Deepseek model for stock analysis."""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    news = "it is a good stock"
    response = client.chat.completions.create(
    extra_headers={
        "HTTP-Referer": "https://stockmeme.com", # Optional. Site URL for rankings on openrouter.ai.
        "X-Title": "StockMeme", # Optional. Site title for rankings on openrouter.ai.
    },
    extra_body={},
  model="deepseek/deepseek-r1:free",
                messages=[

                    {"role": "user", "content": f"Prompt: {prompt}\nStock: {symbol}\nDate: {today}\nNews: {news}\nDaily Data: {daily_data}\n15min Data: {min15_data}"}
                ],
                response_format="json"
    )
    json_str = response.choices[0].message.content

    return json_str

def process_json(json_str):
    try:
        # Handle possible markdown code block formatting
        if json_str.startswith('```json'):
            # Extract JSON from code block
            json_str = '\n'.join(json_str.split('\n')[1:-1])
        else:
            json_str = json_str
            
        # Parse the JSON
        analysis = json.loads(json_str)
        print("Successfully parsed JSON:")

        # Extract and map the information to a JSON type
        extracted_info = {
            '2_week_prediction': analysis.get('2_week_prediction', ''),
            '1_month_prediction': analysis.get('1_month_prediction', ''),
            'expected_price_range': {
                '2_weeks': analysis.get('expected_price_range', {}).get('2_weeks', ''),
                '1_month': analysis.get('expected_price_range', {}).get('1_month', '')
            },
            'options_suggestion': {
                'strategy': analysis.get('options_suggestion', {}).get('strategy', ''),
                'details': {
                    'call_option': analysis.get('options_suggestion', {}).get('details', {}).get('call_option', ''),
                    'put_option': analysis.get('options_suggestion', {}).get('details', {}).get('put_option', '')
                },
                'message': analysis.get('options_suggestion', {}).get('message', '')
            }
        }

        print(json.dumps(extracted_info, indent=2))
    
        return extracted_info
    
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        print("Raw response:")
        print(json_str)
        return {"error": "Failed to parse JSON"}

def loading_effect(message):
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if loading_done:
            break
        sys.stdout.write(f'\r{message} {c}')
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r')

if __name__ == "__main__":
    symbol = "NVDA"
    
    loading_done = False
    loading_thread = threading.Thread(target=loading_effect, args=("Fetching news",))
    loading_thread.start()
    news = search_google(symbol)
    loading_done = True
    loading_thread.join()
    print("\nNews fetched successfully.")
    
    loading_done = False
    loading_thread = threading.Thread(target=loading_effect, args=("Processing news",))
    loading_thread.start()
    processed_news = preprocess_news(news)
    loading_done = True
    loading_thread.join()
    print("\nNews processed successfully.")
    
    loading_done = False
    loading_thread = threading.Thread(target=loading_effect, args=("Loading data",))
    loading_thread.start()
    daily_data = load_csv('daily_stock_data.csv')
    min15_data = load_csv('intraday_stock_data.csv')
    loading_done = True
    loading_thread.join()
    print("\nData loaded successfully.")
    
    loading_done = False
    loading_thread = threading.Thread(target=loading_effect, args=("Asking ChatGPT",))
    loading_thread.start()
    response = ask_chatgpt(symbol, processed_news, "deepseek-r1", daily_data, min15_data)
    loading_done = True
    loading_thread.join()
    print("\nChatGPT response received.")
    print(response)
    analysis = process_json(response)
    # print(analysis)
