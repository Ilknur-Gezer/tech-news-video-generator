# fetch_news.py

import os
import requests
import json
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")

# Safety check
if not API_KEY:
    raise ValueError("NEWS_API_KEY not found in .env")

# Setup NewsAPI request
url = "https://newsapi.org/v2/everything"
params = {
    "q": "artificial intelligence OR AI",
    "language": "en",
    "sortBy": "publishedAt",
    "pageSize": 5,
    "apiKey": API_KEY
}

# Make the request
response = requests.get(url, params=params)
data = response.json()

# Save to output/news.json
os.makedirs("output", exist_ok=True)
with open("output/news.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

# Print summary
if data["status"] == "ok":
    print(f"\n✅ Fetched {len(data['articles'])} articles:\n")
    for i, article in enumerate(data["articles"], 1):
        print(f"{i}. {article['title']}")
        print(f"   {article['description']}")
        print(f"   Source: {article['source']['name']}")
        print(f"   URL: {article['url']}\n")
else:
    print("❌ Failed to fetch news:", data.get("message", "Unknown error"))
