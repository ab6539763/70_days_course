# =============================================
# Day 12 作业 · 编程题 1:AI 翻译官
# 考点:system 提示词约束输出、单轮调用的完整错误处理
# 运行:python translator.py --fake(开发)/ python translator.py(真实)
# =============================================
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from chatlib_v2 import DeepSeekModel, FakeModel, ChatLibError, AuthError

SYSTEM_PROMPT = "你是专业翻译。把用户输入的中文翻译成英文,只输出译文,不要任何解释和引号。"


def main() -> None:
    try:
        model = FakeModel() if "--fake" in sys.argv else DeepSeekModel()
    except AuthError:
        print("请先设置 DEEPSEEK_API_KEY")
        return

    print("中→英翻译官(/exit 退出)")
    while True:
        text = input("\n中文:").strip()
        if not text:
            continue
        if text == "/exit":
            break

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ]
        try:
            print(f"英文:{model.chat(messages)}")
        except ChatLibError as e:
            print(f"翻译失败:{e}")


if __name__ == "__main__":
    main()
