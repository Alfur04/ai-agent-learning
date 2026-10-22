# -*- coding: utf-8 -*-
"""
项目一：带记忆的对话机器人

这个程序做的事：
  1. 读你输入的话
  2. 把你这句话 + 之前聊过的所有内容，一起发给大模型
  3. 大模型回一句，打印出来
  4. 把 AI 的回话也存起来，下一轮继续带着

核心知识点：大模型本身是"失忆"的，是我们在代码里存历史、每次带着发过去，
它看起来才像"记得你之前说了什么"。
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. 加载 .env 文件里的配置（也就是你的 API key）
load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key or "在这里粘贴" in api_key:
    print("❌ 还没设置 API key！")
    print("   请打开 .env 文件，把你的 DeepSeek key 粘贴到等号后面，保存后重新运行。")
    exit(1)

# 2. 创建"客户端"——这是跟大模型通信的入口
#    base_url 指向 DeepSeek，所以虽然用的是 openai 库，实际调的是 DeepSeek
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com",
)

# 3. 系统提示词：给 AI 定"人设"和规则，这条信息永远在最前面
SYSTEM_PROMPT = "你是一个友善的助手。"


def chat():
    # 用列表存对话历史。每条消息是一个字典，有 role（角色）和 content（内容）。
    # role 只有三种：system（设定）/ user（用户）/ assistant（AI）
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    print("开始聊天吧！输入 exit 退出。\n")

    while True:
        # --- 第 1 步：读用户输入 ---
        user_input = input("你：")
        if user_input.strip().lower() in ("exit", "quit", "退出"):
            print("再见！")
            break

        # --- 第 2 步：把用户的话追加到历史里 ---
        messages.append({"role": "user", "content": user_input.strip()})

        # --- 第 3 步：把【整段历史】发给大模型 ---
        response = client.chat.completions.create(
            model="deepseek-chat",   # 用 DeepSeek 的模型

            messages=messages,       # 带上全部历史
        )

        # --- 第 4 步：取出 AI 的回复 ---
        reply = response.choices[0].message.content

        # --- 第 5 步：把 AI 的回复也存进历史，下一轮它才"记得" ---
        messages.append({"role": "assistant", "content": reply})
        #print("当前历史：", messages)

        print(f"AI：{reply}\n")


if __name__ == "__main__":
    chat()
