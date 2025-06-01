#generate_script.py
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import sys

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ OPENAI_API_KEY not found. Please set it in your .env file.")
    sys.exit(1)

client = OpenAI(api_key=api_key)

# Load news data
try:
    with open("output/news.json", "r", encoding="utf-8") as f:
        news_data = json.load(f)
except FileNotFoundError:
    print("❌ News file not found. Please run the fetch script first.")
    sys.exit(1)

articles = news_data.get("articles", [])[:5]  # Limit to top 5

if not articles:
    print("❌ No articles found in news.json.")
    sys.exit(1)

# Select model via CLI or default
model = "gpt-3.5-turbo"
if len(sys.argv) > 1 and sys.argv[1] == "gpt-4":
    model = "gpt-4"
print(f"🧠 Using model: {model}")

# Build prompt
system_prompt = "You are a friendly and professional tech news presenter."
user_prompt = (
    "Create an engaging script for a 3–5 minute YouTube video. Start with a short intro, "
    "then highlight the following AI news stories clearly and concisely. End with a friendly closing line.\n\n"
)

for i, article in enumerate(articles, 1):
    title = article.get('title', 'No title')
    desc = article.get('description', 'No description available.')
    user_prompt += f"{i}. Title: {title}\nDescription: {desc}\n\n"

# Generate script
try:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
    )
    script = response.choices[0].message.content.strip()

    os.makedirs("output", exist_ok=True)
    with open("output/video_script.txt", "w", encoding="utf-8") as f:
        f.write(script)

    print("✅ Script saved to output/video_script.txt")
except Exception as e:
    print("❌ Error generating script:", e)
