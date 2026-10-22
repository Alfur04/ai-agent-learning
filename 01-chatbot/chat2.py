#导入需要的库
from dotenv import load_dotenv
import os
from openai import OpenAI


#获取apikey
load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")

#创造client对象，和大模型对接
client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.deepseek.com",
)
SYSTEM_PROMPT = "你是一个友善的机器人"

MAX_HISTORY = 20

def chat():
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    print("开始聊天吧，输入exit将结束对话")
    while True:

        user_input = input("你:")

        if not user_input.strip():
            continue

        if user_input.strip().lower() in ("exit","退出","quit"):
            print("bye")
            break

        messages.append({"role": "user", "content": user_input.strip()})

        stream = client.chat.completions.create(
            model="deepseek-chat",
            messages = messages,
            stream=True,
        )

        full_reply = ""

        print("AI：", end="", flush=True)

        for chunk in stream:
            piece = chunk.choices[0].delta.content
            if piece:
                print(piece, end="",flush=True)
                full_reply += piece


        print()

        messages.append({"role": "assistant", "content": full_reply})

        if len(messages) > MAX_HISTORY + 1:
            messages = [messages[0]] + messages[-MAX_HISTORY:]
            print("历史已裁剪")

if __name__ == '__main__':
    chat()