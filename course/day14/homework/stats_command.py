# =============================================
# Day 14 延伸题 1:/stats 指令
# 原则:全部数据现算,不维护额外状态(状态越少 bug 越少)
# =============================================
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from chatlib_v3 import ChatSession, FakeModel


def do_stats(session: ChatSession, model) -> None:
    """会话统计:轮数/消息数/最长消息/平均每轮 token。"""
    user_msgs = [m for m in session.messages if m.role == "user"]
    ai_msgs = [m for m in session.messages if m.role == "assistant"]
    rounds = len(ai_msgs)                              # 一轮 = 一次成功的问答

    if not session.messages:
        print("暂无数据")
        return

    longest = max(session.messages, key=lambda m: len(m.content))
    tokens = model.count_usage()["tokens"]

    print(f"轮数 {rounds} | 用户消息 {len(user_msgs)} | AI 消息 {len(ai_msgs)}")
    print(f"最长消息([{longest.role}]):{longest.content[:30]}...")
    if rounds:
        print(f"平均每轮 {tokens / rounds:.0f} tokens")


if __name__ == "__main__":
    # 用 FakeModel 演示
    session = ChatSession("演示", system_prompt="你是助手")
    model = FakeModel()
    for q in ["什么是多轮记忆?它为什么是大模型应用区别于脚本的分水岭?", "谢谢"]:
        session.add_user(q)
        session.add_assistant(model.chat(session.to_api_format()))
    do_stats(session, model)
