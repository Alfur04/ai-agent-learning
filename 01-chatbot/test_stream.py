import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
  api_key=os.getenv("DEEPSEEK_API_KEY"),
  base_url="https://api.deepseek.com",
)

stream = client.chat.completions.create(
  model="deepseek-chat",
  messages=[{"role": "user", "content": "用五句话讲讲复利是什么"}],
  stream=True,          # ← 只加了这一个参数
)

for chunk in stream:
  print(chunk)