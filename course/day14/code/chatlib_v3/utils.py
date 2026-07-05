"""chatlib 通用工具:类型别名 + 重试装饰器(Day 13 新增模块)。"""
import functools
import time

Message = dict[str, str]                 # 类型别名:一条消息
Messages = list[Message]                 # 消息列表——全库统一用它注解


def retry(max_retries: int = 3, retry_on: tuple = (Exception,), base_delay: float = 1.0):
    """重试装饰器工厂:指数退避 + 异常白名单。

    三层结构:retry(参数) → decorator(func) → wrapper(调用)。
    白名单机制:只重试"重试有用的"异常(如限流);
    白名单外的异常(如 AuthError、ValueError)第一次抛出就直接上抛。
    """
    def decorator(func):
        @functools.wraps(func)                       # 保住原函数名与 docstring
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except retry_on as e:
                    last_error = e
                    if attempt < max_retries:
                        delay = base_delay * (2 ** (attempt - 1))    # 1, 2, 4...
                        print(f"[retry] 第 {attempt} 次失败({e}),{delay:.1f}s 后重试")
                        time.sleep(delay)
            raise last_error                         # 次数用尽:原样上抛
        return wrapper
    return decorator
