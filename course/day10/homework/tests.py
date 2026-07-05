# =============================================
# Day 10 作业 · 编程题 2:chatlib 集中测试
# 放置位置:week2_project/tests.py(与 chatlib 同级),从项目根运行
# 本文件为独立可运行版:自动把 week2_project 加入路径
# =============================================
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code", "week2_project"))

from chatlib import (
    ChatMessage, ChatSession, DeepSeekModel, FakeModel,
    InvalidMessageError, RateLimitError,
)


def assert_raises(exc_type, func, *args, **kwargs):
    """断言 func(*args) 必须抛出 exc_type,否则测试失败。

    这就是 pytest.raises 的手工版——Day 34 用上专业测试框架时,
    你已经理解它在替你做什么。
    """
    try:
        func(*args, **kwargs)
    except exc_type:
        return                              # 正确地抛了:测试通过
    except Exception as e:
        raise AssertionError(
            f"抛错了类型:期望 {exc_type.__name__},实际 {type(e).__name__}")
    raise AssertionError(f"没有抛出 {exc_type.__name__}")


def main() -> None:
    # ① 非法 role
    assert_raises(InvalidMessageError, ChatMessage, "admin", "越权")

    # ② 空内容
    assert_raises(InvalidMessageError, ChatMessage, "user", "   ")

    # ③ FakeModel 注入失败:前两次限流,第三次成功
    flaky = FakeModel(fail_times=2)
    msgs = [{"role": "user", "content": "hi"}]
    assert_raises(RateLimitError, flaky.chat, msgs)
    assert_raises(RateLimitError, flaky.chat, msgs)
    assert flaky.chat(msgs) == "这是测试回答。"

    # ④ 空消息列表:编程错误,该崩
    assert_raises(ValueError, DeepSeekModel().chat, [])

    # ⑤ 加载不存在的存档:优雅兜底不崩
    session = ChatSession.load("绝对不存在的存档.json")
    assert len(session) == 0

    print("✓ chatlib 集中测试全部通过")


if __name__ == "__main__":
    main()
