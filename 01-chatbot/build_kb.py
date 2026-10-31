import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("SILICONFLOW_API_KEY"),
    base_url="https://api.siliconflow.cn/v1",
)

def split_document(path, target=400, min_len=20, max_len=500, overlap=50):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    raw_chunks = text.split("\n\n")

    #清洗
    chunks = []
    for c in raw_chunks:
        c = c.strip()
        if c:
            chunks.append(c)

    #过滤+合并
    merged = []
    buf = ""

    for c in chunks:
        if len(c) < min_len:  # 噪音（分隔线、单字标题）
            continue
        buf += c + "\n"  # 攒起来
        if len(buf) >= target:  # 攒够了
            merged.append(buf.strip())
            buf = ""  # 清空，重新开始攒

    if buf:  # 最后没攒满的也要
        merged.append(buf.strip())

    #超长再切
    final_chunks = []
    for c in merged:
        if len(c) <= max_len:
            final_chunks.append(c)
        else:
            for start in range(0, len(c), max_len - overlap):
                final_chunks.append(c[start:start + max_len])

    return final_chunks

chunks = split_document("E:/ai-agent/学习与项目规划.md")

records = []

for i, c in enumerate(chunks):
      vec = client.embeddings.create(
          model="BAAI/bge-m3",
          input=c,
      ).data[0].embedding

      records.append({
          "id": i,
          "text": c,
          "source": "学习与项目规划.md",
          "chunk_index": i,
          "vector": vec,
      })

      print(f"[{i + 1}/{len(chunks)}] 已向量化")

with open("knowledge_base.json", "w", encoding="utf-8") as f:
    json.dump(records, f, ensure_ascii=False, indent=2)

print("已保存 knowledge_base.json")

with open("knowledge_base.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)

print("条数：", len(loaded))
print("第一条文本前50字：", loaded[0]["text"][:50])
print("第一条向量长度：", len(loaded[0]["vector"]))