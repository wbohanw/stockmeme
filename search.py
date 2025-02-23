import openai
import os
from googlesearch import search
import json
with open("prompt2.txt") as f:
    prompt = f.read()
from load_csv import load_csv
import datetime
# Set your API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


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

        # print(results)

        return results
    except Exception as e:
        print(f"Search error: {e}")
        return ["Search service unavailable."]
    

def ask_chatgpt(query, news, day_data, min15_data):
    """Queries OpenAI GPT model to summarize or enhance the search results."""
    openai.api_key = OPENAI_API_KEY
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    response = openai.ChatCompletion.create(
        model="o3-mini",
        messages=[{"role": "system", "content": prompt},
                  {"role": "user", "content": f"Stock: {query}\ncurrent date: {today}\nLatest News: {news}\nPrice Data: {day_data}\n15-Minute Price Data: {min15_data}"}]
    )
    
    return response["choices"][0]["message"]["content"]

# def chatgpt_search(query):
#     """Combines real-time search and ChatGPT response to provide the best answer."""
#     search_results = search_google(query)
#     formatted_results = "\n".join(search_results)
    
#     prompt = f"Summarize the following search results for '{query}':\n{formatted_results}"
    
#     chatgpt_response = ask_chatgpt(prompt)
#     return chatgpt_response

if __name__ == "__main__":
    symbol = "TSLA"
    # Example Usage
    news = search_google(symbol)
    daily_data = load_csv('daily_stock_data.csv')
    min15_data = load_csv('intraday_stock_data.csv')
    response = ask_chatgpt(symbol, news, daily_data, min15_data)
    print(response)
    
