# =============================================
# Day 09 作业 · 编程题 3:RetryWrapper(Day 13 装饰器的前传)
# 考点:__call__ 让对象携带配置地"当函数用"
# 后天学函数版装饰器时对照本文件看,装饰器就不神秘了
# =============================================


class RetryWrapper:
    """重试包装器:包住任何函数,失败自动重试。"""

    def __init__(self, func, max_retries: int = 3):
        self.func = func                   # 被包装的函数:函数是一等公民,存起来
        self.max_retries = max_retries

    def __call__(self, *args, **kwargs):
        """执行被包装的函数;失败重试,最终失败原样抛出。

        *args/**kwargs 原样转发:包装器不关心也不限制函数的签名——
        这正是 Day 13 装饰器的标准转发姿势,今天先练手。
        """
        last_error = None
        for attempt in range(1, self.max_retries + 1):
            try:
                return self.func(*args, **kwargs)      # 成功:直接返回
            except Exception as e:                      # 失败:记下异常,下一轮
                last_error = e
                print(f"第 {attempt} 次失败({e}),重试中……")
        raise last_error                                # 次数用尽:原样抛出


# ---- 测试:前两次必失败、第三次成功 ----
attempt_count = 0


def flaky_api():
    """模拟不稳定的 API:前两次抛错,第三次成功。"""
    global attempt_count                    # 教学演示用 global,记住它的坏(Day 06)
    attempt_count += 1
    if attempt_count < 3:
        raise ConnectionError(f"网络抖动 #{attempt_count}")
    return "调用成功!"


safe_api = RetryWrapper(flaky_api, max_retries=5)      # 包装:像造对象
result = safe_api()                                     # 使用:像调函数(__call__)
print(result)
assert result == "调用成功!"
assert attempt_count == 3
print("✓ RetryWrapper 测试通过")
