# =============================================
# Day 13 · 上午演示代码 1:装饰器从素颜到全妆
# 文件:decorator_demo.py
# =============================================
import functools
import time


# ---- 1. 两块地基复习 ----
def shout(text):
    return text.upper() + "!"


f = shout                    # 地基 1:函数是一等公民(能存能传)
print(f("hi"))               # HI!


def make_multiplier(n):
    def inner(x):
        return x * n         # 地基 2:闭包——inner 带走了 n
    return inner


double = make_multiplier(2)
print(double(5))             # 10


# ---- 2. 手写包装(装饰器的素颜) ----
def with_log(func):
    """装饰器:接收一个函数,返回它的加强版。"""
    @functools.wraps(func)                   # 保住原函数的名字和 docstring(规范必加)
    def wrapper(*args, **kwargs):            # *args/**kwargs:原样转发,不限制签名
        print(f"[日志] 调用 {func.__name__},参数 {args}")
        result = func(*args, **kwargs)       # 干正事
        print(f"[日志] {func.__name__} 返回 {result!r}")
        return result                        # 别忘了递出去!
    return wrapper


def greet(name):
    return f"你好,{name}"


greet = with_log(greet)          # 手动包装:用加强版顶替原函数
greet("张三")


# ---- 3. @ 语法糖(与手动包装完全等价) ----
@with_log                        # 这一行 = greet2 = with_log(greet2)
def greet2(name):
    """打招呼。"""
    return f"你好,{name}"


greet2("李四")
print(greet2.__name__)           # greet2(functools.wraps 的功劳,否则是 wrapper)


# ---- 4. 带参数的装饰器:三层工厂 ----
def retry(max_retries: int = 3, retry_on: tuple = (Exception,), base_delay: float = 1.0):
    """重试装饰器工厂:失败自动重试,间隔指数退避(1s→2s→4s)。

    三层结构:retry(参数) → 返回装饰器;装饰器(func) → 返回 wrapper;
              wrapper(调用) → 真正干活。使用必带括号:@retry() 或 @retry(...)
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except retry_on as e:                    # 白名单:只重试"重试有用的"
                    last_error = e
                    if attempt < max_retries:
                        delay = base_delay * (2 ** (attempt - 1))    # 指数退避
                        print(f"[retry] 第 {attempt} 次失败({e}),{delay:.1f}s 后重试")
                        time.sleep(delay)
            raise last_error                             # 次数用尽:原样上抛
        return wrapper
    return decorator


# ---- 5. @retry 实战:前两次必失败的函数自动恢复 ----
attempt_count = 0


@retry(max_retries=4, retry_on=(ConnectionError,), base_delay=0.1)
def flaky_api():
    """模拟不稳定 API:前两次抛错,第三次成功。"""
    global attempt_count
    attempt_count += 1
    if attempt_count < 3:
        raise ConnectionError(f"网络抖动 #{attempt_count}")
    return "调用成功!"


print(flaky_api())               # 自动重试到成功,调用方全程无感
assert attempt_count == 3


# ---- 6. functools.partial:预填参数的正规军(Day 06 彩蛋兑现) ----
from functools import partial


def power(x, n):
    return x ** n


square = partial(power, n=2)
cube = partial(power, n=3)
print(square(5), cube(5))        # 25 125
