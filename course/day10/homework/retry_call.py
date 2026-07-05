# =============================================
# Day 10 作业 · 编程题 3:retry_call(可指定"只对哪些异常重试")
# 对比 Day 09 的 RetryWrapper:增加 retry_on 白名单——
# 军规"只捕获你能处理的"落到重试场景 = 只重试"重试有用的"
# =============================================
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code", "week2_project"))

from chatlib import FakeModel, RateLimitError, AuthError


def retry_call(func, max_retries: int = 3, retry_on: tuple = (Exception,)):
    """调用 func;白名单内的异常重试,白名单外立刻上抛。

    retry_on 是异常类型元组:except 语法天然支持元组匹配,
    所以白名单机制几乎不用额外代码——语言特性顺水推舟。
    """
    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            return func()
        except retry_on as e:               # 只接白名单内的
            last_error = e
            print(f"第 {attempt} 次失败({e}),重试中……")
        # 白名单外的异常没有被 except 匹配,自动向上传播——一行都不用写!
    raise last_error


if __name__ == "__main__":
    msgs = [{"role": "user", "content": "hi"}]

    # 场景 1:对 RateLimitError 重试 → 三次内成功
    flaky = FakeModel(fail_times=2)
    result = retry_call(lambda: flaky.chat(msgs), max_retries=5,
                        retry_on=(RateLimitError,))
    assert result == "这是测试回答。"
    print("场景 1 通过:限流重试成功\n")

    # 场景 2:白名单只有 AuthError → 第一次 RateLimitError 就直接上抛
    flaky2 = FakeModel(fail_times=2)
    try:
        retry_call(lambda: flaky2.chat(msgs), max_retries=5,
                   retry_on=(AuthError,))
        assert False, "应该直接上抛"
    except RateLimitError:
        print("场景 2 通过:白名单外的异常不重试,直接上抛")

    print("✓ retry_call 全部测试通过")
