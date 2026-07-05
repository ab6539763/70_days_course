# =============================================
# Day 12 作业 · 编程题 4:qa_app 加"对话导出"
# 关键区分(写在注释里的思考):
#   记忆 = 历史进入 messages 发给模型,影响模型的回答(Day 14 做);
#   留痕 = 只存在本地列表/文件,模型完全不知道(本题做的)。
# =============================================
import json
import sys
import os
import time
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from chatlib_v2 import DeepSeekModel, FakeModel, ChatLibError, RateLimitError, AuthError


def main() -> None:
    use_fake = "--fake" in sys.argv
    try:
        model = FakeModel() if use_fake else DeepSeekModel()
    except AuthError:
        print("请先设置 DEEPSEEK_API_KEY")
        return

    print(f"AI 问答(模型:{model.model_name})  /export 导出  /exit 退出")
    records: list = []                               # 本地留痕(不是记忆!)
    total_tokens = 0

    while True:
        try:
            question = input("\n你问:").strip()
        except KeyboardInterrupt:
            print("\n再见!")
            break

        if not question:
            continue
        if question == "/exit":
            print("再见!")
            break
        if question == "/export":                    # 新指令:导出留痕
            name = f"qa_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(name, "w", encoding="utf-8") as f:
                json.dump(records, f, ensure_ascii=False, indent=2)
            print(f"已导出 {len(records)} 条 → {name}")
            continue

        messages = [
            {"role": "system", "content": "你是一个简洁的AI助手,回答不超过150字"},
            {"role": "user", "content": question},
        ]
        try:
            answer = model.chat(messages)
        except RateLimitError:
            print("(限流,3 秒后重试)")
            time.sleep(3)
            try:
                answer = model.chat(messages)
            except ChatLibError as e:
                print(f"重试仍失败:{e}")
                continue
        except ChatLibError as e:
            print(f"服务异常:{e}")
            continue

        used = model.count_usage()["tokens"] - total_tokens
        total_tokens = model.count_usage()["tokens"]
        print(f"\nAI 答:{answer}")

        # ── 本地留痕:记录不进 messages,模型不知道 ──
        records.append({
            "question": question,
            "answer": answer,
            "tokens": used,
            "time": datetime.now().isoformat(timespec="seconds"),
        })


if __name__ == "__main__":
    main()
