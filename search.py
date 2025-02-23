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

# Initialize Deepseek client at the top level
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1"
)

def search_google(query):
    """Fetches real-time search results from Google using the googlesearch library."""
    q1 = f"what is the latest news and of {query}"
    q2 = f"{query} events(meeting, conference) happening in future"
    results = []
    try:
        search_results = search(q1, advanced=True, num_results=3)
        search_results2 = search(q2, advanced=True, num_results=3)
        results.extend([result.description for result in search_results])
        results.extend([result.description for result in search_results2 if result.description not in results])
        return results
    except Exception as e:
        print(f"Search error: {e}")
        return ["Search service unavailable."]

def ask_chatgpt(query, news, day_data, min15_data):
    """Queries Deepseek model for stock analysis."""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1-distill-llama-70b:free",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Stock: {query}\nDate: {today}\nNews: {news}\nDaily Data: {day_data}\n15min Data: {min15_data}"}
            ],
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Deepseek API Error: {e}")
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    symbol = "TSLA"
    news = search_google(symbol)
    daily_data = load_csv('daily_stock_data.csv')
    min15_data = load_csv('intraday_stock_data.csv')
    response = ask_chatgpt(symbol, news, daily_data, min15_data)
    print(json.dumps(json.loads(response), indent=4))
