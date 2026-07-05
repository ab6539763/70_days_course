# =============================================
# 项目一 · 自动化冒烟测试(讲师提供,交叉测试前先跑它)
# 测试对象:assistant.py 里可独立测试的纯函数与流程零件
# 原则:业务逻辑测试全用 FakeModel(Day 09 测试替身工作流)
# =============================================
from chatlib_v3 import ChatSession, FakeModel

from assistant import parse_command, do_clear, save_session, load_latest_session_path


def test_parse_command():
    """指令解析:含大小写与带空格参数(交叉测试击破点预演)。"""
    assert parse_command("/exit") == ("/exit", "")
    assert parse_command("  /SAVE my chat.json ") == ("/save", "my chat.json")   # 大写也认!
    assert parse_command("今天天气") == ("", "今天天气")
    print("✓ parse_command")


def test_memory_flow():
    """F1 多轮记忆的机制验证:历史随轮数增长,发送的是完整历史。"""
    session = ChatSession("测试", system_prompt="你是助手")
    model = FakeModel()

    for i, q in enumerate(["我叫小林", "我叫什么?"], start=1):
        session.add_user(q)
        reply = model.chat(session.to_api_format())
        session.add_assistant(reply)
        # 每轮消息数:system(1) + 轮数×2
        assert len(session) == 1 + i * 2, f"第{i}轮历史长度不对"
    print("✓ 多轮记忆机制(历史随轮增长)")


def test_rollback():
    """F5-e 失败回滚:异常后历史里不能留孤儿 user 消息。"""
    from chatlib_v3 import RateLimitError
    session = ChatSession("测试", system_prompt="你是助手")
    model = FakeModel(fail_times=99)               # 必失败

    session.add_user("这条会失败")
    try:
        model.chat(session.to_api_format())
    except RateLimitError:
        session.messages.pop()                     # 主循环里的回滚动作
    assert len(session) == 1                       # 只剩 system:无孤儿
    print("✓ 失败回滚(无孤儿消息)")


def test_clear_keeps_system():
    """F3 /clear 保人设。"""
    session = ChatSession("测试", system_prompt="你是海盗助手")
    session.add_user("hi")
    session.add_assistant("ahoy")
    do_clear(session)
    assert len(session) == 1 and session[0].role == "system"
    print("✓ /clear 保留人设")


def test_save_and_latest():
    """F4 存档 + 最新存档定位。"""
    import shutil
    session = ChatSession("测试", system_prompt="你是助手")
    session.add_user("存档测试")

    path = save_session(session)                   # 时间戳自动命名
    assert load_latest_session_path() is not None

    restored = ChatSession.load(path)
    assert restored.messages[1].content == "存档测试"
    shutil.rmtree("sessions")                      # 打扫现场
    print("✓ 存档与恢复")


def test_save_path_safety():
    """设计文档风险 3:防路径穿越。"""
    import shutil
    session = ChatSession("测试", system_prompt="s")
    path = save_session(session, "../../危险路径.json")
    assert "sessions" in path and ".." not in path.replace("../", "")
    shutil.rmtree("sessions")
    print("✓ 存档文件名安全")


if __name__ == "__main__":
    test_parse_command()
    test_memory_flow()
    test_rollback()
    test_clear_keeps_system()
    test_save_and_latest()
    test_save_path_safety()
    print("\n✓ 全部冒烟测试通过——可以进入交叉测试")
