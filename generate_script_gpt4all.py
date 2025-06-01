from gpt4all import GPT4All
import json
import os

# Load news data
with open("/Users/igezer/ai-news-youtube-bot/output/news.json", "r", encoding="utf-8") as f:
    news_data = json.load(f)

articles = news_data.get("articles", [])

# Prepare prompt
user_prompt = "You are a friendly tech news presenter.\nSummarize the following AI news into a script for a 3-5 min YouTube video.\n\n"
for i, article in enumerate(articles, 1):
    user_prompt += f"{i}. Title: {article.get('title')}\nDescription: {article.get('description')}\n\n"

# Initialize GPT4All model
model_path = "/Users/igezer/ai-news-youtube-bot/models/gpt4all-j-v1.3-groovy.bin"
gptj = GPT4All(model_path, allow_download=False)

# Generate response
response = gptj.generate(user_prompt, max_tokens=512)
script = response.strip()

# Save the script
os.makedirs("output", exist_ok=True)
with open("output/video_script.txt", "w", encoding="utf-8") as f:
    f.write(script)

print("✅ Script saved to output/video_script.txt")
