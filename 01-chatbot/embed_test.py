import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("SILICONFLOW_API_KEY")

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.siliconflow.cn/v1",
)

response = client.embeddings.create(
      model="BAAI/bge-m3",
      input="我今天心情不好",
)

vector = response.data[0].embedding

print(f"向量长度：{len(vector)}")
print(f"前 5 个值：{vector[:5]}")
print(f"数据类型：{type(vector)}")

