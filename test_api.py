from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

import requests
import os
from openai import OpenAI
# Replace with your OpenRouter API key

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY"),
)

completion = client.chat.completions.create(
  extra_headers={
    "HTTP-Referer": "https://stockmeme.com", # Optional. Site URL for rankings on openrouter.ai.
    "X-Title": "StockMeme", # Optional. Site title for rankings on openrouter.ai.
  },
  extra_body={},
  model="deepseek/deepseek-r1-distill-llama-70b:free",
  messages=[
    {
      "role": "user",
      "content": "What is the meaning of life?"
    }
  ]
)
print(completion.choices[0].message.content)
