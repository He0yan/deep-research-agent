import requests
import os
from dotenv import load_dotenv

load_dotenv()

response = requests.post(
    "https://api.deepseek.com/v1/tools/search",
    headers={
        "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
    },
    json={
        "query": "DeepSeek V4 模型 发布",
        "count": 5,
        "need_content": True,
    },
)
response.raise_for_status()

for result in response.json()["results"]:
    print(result["title"], result["url"])
    print(result["summary"])