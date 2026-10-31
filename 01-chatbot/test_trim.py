# 模拟历史裁剪，验证"裁剪位置"对消息顺序的影响
MAX_HISTORY = 20


def simulate(trim_after_user):
    """
    trim_after_user=True  : 在追加用户消息后裁剪（错误做法）
    trim_after_user=False : 在追加助手回复后裁剪（正确做法）
    """
    messages = [{"role": "system", "content": "sys"}]
    bad_rounds = []

    for round_no in range(1, 41):
        # 1. 用户提问
        messages.append({"role": "user", "content": f"u{round_no}"})

        if trim_after_user and len(messages) > MAX_HISTORY + 1:
            messages = [messages[0]] + messages[-MAX_HISTORY:]
            if messages[1]["role"] != "user":
                bad_rounds.append(round_no)

        # 2. 模型回复（这里假装调用）
        messages.append({"role": "assistant", "content": f"a{round_no}"})

        if not trim_after_user and len(messages) > MAX_HISTORY + 1:
            messages = [messages[0]] + messages[-MAX_HISTORY:]
            if messages[1]["role"] != "user":
                bad_rounds.append(round_no)

    return bad_rounds


# ===== 做法 A：追加用户消息后裁剪（你原来的写法）=====
print("=== 做法A：追加用户消息后裁剪 ===")
bad = simulate(trim_after_user=True)
print(f"出现 assistant 开头的轮次：{bad}")
print(f"总共 {len(bad)} 次")
print()

# ===== 做法 B：追加助手回复后裁剪（修正后）=====
print("=== 做法B：追加助手回复后裁剪 ===")
bad = simulate(trim_after_user=False)
print(f"出现 assistant 开头的轮次：{bad}")
print(f"总共 {len(bad)} 次")

messages = [{"role": "system", "content": "sys"}]
for round_no in range(1, 12):
  messages.append({"role": "user", "content": f"u{round_no}"})
  if len(messages) > MAX_HISTORY + 1:
      messages = [messages[0]] + messages[-MAX_HISTORY:]
      print(f"--- 第 {round_no} 轮裁剪后 ---")
      for m in messages[:5]:
          print(f"  {m['role']:10s} {m['content']}")
      print("  ...")
  messages.append({"role": "assistant", "content": f"a{round_no}"})