"""Day 14: 命令行多轮对话 AI 助手 — 阶段项目一"""
import os, json, requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/v1/chat/completions"
HISTORY_DIR = Path("chat_histories")
HISTORY_DIR.mkdir(exist_ok=True)


class ChatAssistant:
    def __init__(self):
        self.messages = [
            {"role": "system", "content": "你是一个有帮助的 AI 助手。"}
        ]

    def chat(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        payload = {"model": "deepseek-chat", "messages": self.messages, "temperature": 0.7}
        resp = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        reply = resp.json()["choices"][0]["message"]["content"]
        self.messages.append({"role": "assistant", "content": reply})
        return reply

    def clear(self):
        self.messages = [self.messages[0]]

    def save(self, filename: str = None):
        if not filename:
            filename = f"chat_{datetime.now():%Y%m%d_%H%M%S}.json"
        path = HISTORY_DIR / filename
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.messages, f, ensure_ascii=False, indent=2)
        return path


def main():
    assistant = ChatAssistant()
    print("🤖 多轮对话 AI 助手")
    print("指令: /clear 清空 | /save 保存 | /exit 退出")

    while True:
        user_input = input("\n你: ").strip()
        if not user_input:
            continue
        if user_input == "/exit":
            break
        if user_input == "/clear":
            assistant.clear()
            print("✅ 对话已清空")
            continue
        if user_input == "/save":
            path = assistant.save()
            print(f"✅ 已保存到 {path}")
            continue
        try:
            reply = assistant.chat(user_input)
            print(f"AI: {reply}")
        except Exception as e:
            print(f"❌ 错误: {e}")


if __name__ == "__main__":
    main()
