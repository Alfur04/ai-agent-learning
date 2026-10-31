import json
import os
from dotenv import load_dotenv
from openai import OpenAI
import math


def cosine_similarity(vec_a, vec_b):
    dot = sum(x * y for x, y in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(x * x for x in vec_a))
    norm_b = math.sqrt(sum(y * y for y in vec_b))
    return dot / (norm_a * norm_b)

load_dotenv()

chat_client = OpenAI(                                    # ← 新增
      api_key=os.getenv("DEEPSEEK_API_KEY"),
      base_url="https://api.deepseek.com",
  )

embed_client = OpenAI(
    api_key=os.getenv("SILICONFLOW_API_KEY"),
    base_url="https://api.siliconflow.cn/v1",
)

with open("knowledge_base.json", "r", encoding="utf-8") as f:
    kb = json.load(f)

print(f"知识库已加载：{len(kb)} 条")


def retrieve(question, top_k=5, threshold=0.5):
    # 问题转向量
    q_vec = embed_client.embeddings.create(
        model="BAAI/bge-m3", input=question
    ).data[0].embedding

    # 和每一条算相似度
    scored = []
    for item in kb:
        score = cosine_similarity(q_vec, item["vector"])
        scored.append((score, item))

    scored.sort(key=lambda x: x[0], reverse=True)

    # 阈值过滤
    results = [(s, it) for s, it in scored if s >= threshold]
    return results[:top_k]

def build_context(results):
    parts = []
    for i, (score, item) in enumerate(results, start=1):
        parts.append(
            f"[{i}]（来源：{item['source']} 第 {item['chunk_index']} 段）\n{item['text']}"
        )
    return "\n\n".join(parts)

RAG_PROMPT = """你是一个严谨的助手。请只根据下面提供的资料回答问题。

【资料】
{context}

【问题】
{question}

【要求】
1. 只能使用资料中的信息，不要补充资料以外的知识
2. 在关键事实或结论后标注来源编号，如 [1]；同一来源的连续内容只在段末标注一次即可
3. 如果资料里没有答案，直接回答"根据现有资料无法回答"，不要猜测"""


def answer(question):
    results = retrieve(question)

    if not results:
        return "没有找到相关资料。"

    context = build_context(results)
    prompt = RAG_PROMPT.format(context=context, question=question)

    response = chat_client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content

if __name__ == "__main__":
      print("知识库问答已启动，输入 exit 退出\n")
      while True:
          q = input("你：").strip()
          if not q:
              continue
          if q.lower() in ("exit", "quit", "退出"):
              break
          print(f"\nAI：{answer(q)}\n")