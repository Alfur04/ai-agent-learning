with open("E:/ai-agent/学习与项目规划.md", "r", encoding="utf-8") as f:
    text = f.read()

raw_chunks = text.split("\n\n")

chunks = []
for c in raw_chunks:
    c = c.strip()
    if c:                       # 非空
        chunks.append(c)

TARGET = 400        # 目标长度
MIN_LEN = 20        # 短于这个的当噪音丢掉

merged = []
buf = ""

for c in chunks:
  if len(c) < MIN_LEN:        # 噪音（分隔线、单字标题）
      continue
  buf += c + "\n"             # 攒起来
  if len(buf) >= TARGET:      # 攒够了
      merged.append(buf.strip())
      buf = ""                # 清空，重新开始攒

if buf:                         # 最后没攒满的也要
  merged.append(buf.strip())

MAX_LEN = 500

OVERLAP = 50

final_chunks = []
for c in merged:
    if len(c) <= MAX_LEN:
        final_chunks.append(c)
    else:
          # 每 MAX_LEN 字切一刀
        for start in range(0, len(c), MAX_LEN - OVERLAP):
            final_chunks.append(c[start:start + MAX_LEN])

print("片段总数：", len(final_chunks))
print("平均长度：", sum(len(c) for c in final_chunks) // len(final_chunks))
print("最长：", max(len(c) for c in final_chunks))
print("最短：", min(len(c) for c in final_chunks))
for i, c in enumerate(final_chunks[:3]):
  print(f"--- 片段 {i}（{len(c)} 字）---")
  print(c[:150], "...")