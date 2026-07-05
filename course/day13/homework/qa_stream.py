# =============================================
# Day 13 作业 · 编程题 2:批量问答生成器
# 生成器版的价值:边生产边交付——
#   列表版:10 个问题全部答完(30秒)才能看到第一个答案;
#   生成器版:第一个答案 3 秒就交付,用户体验质变。
# 这就是"流式思想"在批处理场景的应用,Day 24 的 SSE 是它的网络版
# =============================================
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from chatlib_v3 import FakeModel, ChatLibError


def qa_stream(model, questions: list):
    """逐个提问,逐个 yield (问题, 回答);单题失败 yield 错误标记,不中断。"""
    for q in questions:
        messages = [
            {"role": "system", "content": "简洁回答,50字以内"},
            {"role": "user", "content": q},
        ]
        try:
            yield (q, model.chat(messages))      # 答完一个交付一个
        except ChatLibError as e:
            yield (q, f"[失败:{e}]")             # 军规:单题失败不中断整批


if __name__ == "__main__":
    model = FakeModel()
    questions = ["什么是装饰器?", "什么是生成器?", "什么是异步?"]

    for q, a in qa_stream(model, questions):     # 边收边打印
        print(f"问:{q}\n答:{a}\n")
