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

embed_client = OpenAI(api_key=os.getenv("SILICONFLOW_API_KEY"), base_url="https://api.siliconflow.cn/v1")

chat_client  = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"),  base_url="https://api.deepseek.com")

sentences = [
      "最低还款按日息万分之五计息，折合年化约18.25%。",
      "逾期超过90天会影响个人征信记录，且可能被银行起诉。",
      "建议优先偿还利率最高的债务，这种策略叫雪崩法。",
      "信用卡分期手续费按月收取，折算真实年化利率通常在13%以上。",
      "短期无法还清时，应主动联系银行协商个性化分期方案。",
      "猫是一种很可爱的动物，很多人喜欢养。",
]

vectors = []

for s in sentences:
    vec = embed_client.embeddings.create(model="BAAI/bge-m3", input=s).data[0].embedding
    vectors.append(vec)

# for i in range(len(sentences)):
#     for j in range(len(sentences)):
#         score = cosine_similarity(vectors[i], vectors[j])
#         print(f"{score:.2f}", end="  ")
#     print()

question = "我还不上钱了"

q_vec = embed_client.embeddings.create(model="BAAI/bge-m3", input=question).data[0].embedding

scores = []

for i, chunk_vec in enumerate(vectors):
    score = cosine_similarity(q_vec, chunk_vec)
    scores.append((score, sentences[i]))

scores.sort(key=lambda x: x[0], reverse=True)

# 阈值过滤：低于阈值视为不相关，不进入 top-k
THRESHOLD = 0.5

print("=== 检索结果（原始分数）===")
for score, text in scores:
    mark = "✓" if score >= THRESHOLD else "✗"
    print(f"  {mark} {score:.3f}  {text}")
print()

relevant = [(score, text) for score, text in scores if score >= THRESHOLD]
top3 = relevant[:3]

# 一条都没检索到：直接结束，不浪费一次模型调用
if not top3:
    print("没有找到相关资料")
    exit()

context = ""
for i, (score, text) in enumerate(top3, start=1):
    context += f"[{i}] {text}\n"

print("=== 材料 ===")
print(context)

RAG_PROMPT = """你是一个严谨的助手。请只根据下面提供的资料回答问题。

【资料】
{context}

【问题】
{question}

【要求】
1. 只能使用资料中的信息，不要补充资料以外的知识
2. 回答中标注引用的来源编号，如 [1]、[2]
3. 如果资料里没有答案，直接回答"根据现有资料无法回答"，不要猜测"""

prompt = RAG_PROMPT.format(context=context, question=question)
print("=== 最终 prompt ===")
print(prompt)

response = chat_client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": prompt}],
)

answer = response.choices[0].message.content

print("\n=== AI 回答 ===")
print(answer)