"""Day 12: 命令行 AI 问答小程序 — 首次调用大模型 API"""
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("DEEPSEEK_API_KEY", "your-api-key-here")
API_URL = "https://api.deepseek.com/v1/chat/completions"
MODEL = "deepseek-chat"


def chat(user_message: str, system_prompt: str = "你是一个有帮助的 AI 助手。") -> str:
  headers = {
      "Authorization": f"Bearer {API_KEY}",
      "Content-Type": "application/json",
  }
  payload = {
      "model": MODEL,
      "messages": [
          {"role": "system", "content": system_prompt},
          {"role": "user", "content": user_message},
      ],
      "temperature": 0.7,
  }
  response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
  response.raise_for_status()
  data = response.json()
  return data["choices"][0]["message"]["content"]


def main():
    print("🤖 AI 问答小程序（输入 quit 退出）")
    while True:
        user_input = input("\n你: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            print("再见！")
            break
        if not user_input:
            continue
        try:
            reply = chat(user_input)
            print(f"AI: {reply}")
        except requests.exceptions.HTTPError as e:
            print(f"API 错误: {e}")
        except Exception as e:
            print(f"发生错误: {e}")


if __name__ == "__main__":
    main()
