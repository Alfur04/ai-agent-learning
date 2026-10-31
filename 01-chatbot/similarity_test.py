import math
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def cosine_similarity(vec_a, vec_b):
    #点积
    dot = sum(x * y for x, y in zip(vec_a, vec_b))

    #各自的模
    norm_a = math.sqrt(sum(x * x for x in vec_a))
    norm_b = math.sqrt(sum(y * y for y in vec_b))

    #相除
    return dot / (norm_a * norm_b)

API_KEY = os.getenv("SILICONFLOW_API_KEY")

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.siliconflow.cn/v1",
)

sentences = [
      "我欠了很多钱，还不上怎么办",
      "债务逾期了应该怎么处理",
      "今天天气真好，适合出去玩",
      "信用卡最低还款的利息怎么算",
      "猫是一种很可爱的动物",
]

vectors = []

for s in sentences:
    vec = client.embeddings.create(model="BAAI/bge-m3", input=s).data[0].embedding
    vectors.append(vec)

# for i in range(len(sentences)):
#     for j in range(len(sentences)):
#         score = cosine_similarity(vectors[i], vectors[j])
#         print(f"{score:.2f}", end="  ")
#     print()

query = "我还不上信用卡的钱了"

query_vec = client.embeddings.create(model="BAAI/bge-m3", input=query).data[0].embedding

scores = []

for i, chunk_vec in enumerate(vectors):
  score = cosine_similarity(query_vec, chunk_vec)
  scores.append((score, sentences[i]))

scores.sort(key=lambda x: x[0], reverse=True)

for score, text in scores[:3]:
    print(f"{score:.2f}  {text}")