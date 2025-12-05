import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {os.getenv("API_KEY_REF")}",
    "Content-Type": "application/json"
}
while True:
    user_input = input(">>>>")
    if user_input == "quit" or user_input == "exit":
        break
    image_or_video_path = input("Image or Video path: ")
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"{user_input}",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"{image_or_video_path}"}}]}]

    payload = {
        "model": "google/gemini-2.0-flash-001",
        "messages": messages
    }

    get_response = requests.post(url, headers=headers, json=payload)
    data_json_response = get_response.json()
    print(data_json_response["choices"][0]["message"]["content"])
