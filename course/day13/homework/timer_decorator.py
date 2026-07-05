# =============================================
# Day 13 作业 · 编程题 1:@timer 计时装饰器
# =============================================
import functools
import time


def timer(func):
    """计时装饰器:打印函数执行耗时。"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)           # 干正事
        elapsed = time.time() - start
        print(f"[timer] {func.__name__} 耗时 {elapsed:.3f}s")
        return result                            # 递出去!
    return wrapper


@timer
def slow_task():
    """模拟耗时任务。"""
    time.sleep(0.5)
    return "完成"


print(slow_task())

# 叠放思考:@timer 应该在 @retry 外层——
#   @timer
#   @retry()
#   def chat(...): ...
# 这样计的是"含全部重试的总耗时"(用户真实等待时间);
# 反过来则每次重试各计一次,得到单次尝试耗时。
# 监控用户体验要总耗时,所以默认 timer 在外。
