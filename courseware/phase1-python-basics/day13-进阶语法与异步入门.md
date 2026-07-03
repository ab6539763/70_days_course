# Day 13: 进阶语法与异步入门

> **培训阶段**: 第一阶段 Python 编程基础 | **第 2 周** | **学习时长**: 约 6-8 小时  
> **今日关键词**: 装饰器、生成器、typing、asyncio、python-dotenv、重试装饰器

---

## 📍 课程导航

### 上节回顾
在 **Day 12** 中，你首次成功调用了大模型 API，完成了「命令行 AI 问答」项目。今天学习 Python **进阶语法**——装饰器、生成器、类型注解，以及 **异步编程入门** 和 **环境变量管理**。

### 本节学习目标
完成本日学习后，你将能够：

1. 理解并使用装饰器增强函数功能
2. 使用生成器处理大数据流
3. 使用 typing 模块进行类型注解
4. 了解 asyncio 异步编程基础
5. 使用 python-dotenv 管理 API Key
6. 实现 API 调用的重试装饰器

### 与后续课程的衔接
- **Day 14** 阶段考核将综合运用所有技能
- **Day 30+** FastAPI 框架大量使用装饰器和 async
- **Day 39+** Agent 开发中的 Tool 注册使用装饰器模式
- 生产环境中 API Key 管理必须使用 dotenv

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：装饰器

#### 1.1 函数是对象

```python
# day13/function_as_object.py

def greet(name):
    return f"Hello, {name}!"

# 函数可以赋值给变量
say_hello = greet
print(say_hello("AI"))  # Hello, AI!

# 函数可以作为参数
def execute(func, arg):
    return func(arg)

print(execute(greet, "World"))  # Hello, World!
```

#### 1.2 装饰器本质

装饰器是一个接收函数、返回新函数的高阶函数：

```python
# day13/decorator_basic.py
import time

def timer(func):
    """计时装饰器"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"⏱️ {func.__name__} 耗时 {elapsed:.3f}s")
        return result
    return wrapper

# 手动装饰
def slow_function():
    time.sleep(1)
    return "完成"

slow_function = timer(slow_function)

# 使用 @ 语法糖（推荐）
@timer
def fetch_data():
    time.sleep(0.5)
    return {"data": "..."}

result = fetch_data()
# ⏱️ fetch_data 耗时 0.501s
```

#### 1.3 带参数的装饰器

```python
# day13/decorator_with_args.py
import time
import functools

def retry(max_attempts=3, delay=1):
    """重试装饰器"""
    def decorator(func):
        @functools.wraps(func)  # 保留原函数的元信息
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        print(f"❌ {func.__name__} 失败 {max_attempts} 次: {e}")
                        raise
                    print(f"⚠️ 第 {attempt} 次失败，{delay}s 后重试...")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=2)
def unstable_api_call():
    """模拟不稳定的 API 调用"""
    import random
    if random.random() < 0.7:
        raise ConnectionError("网络超时")
    return "成功！"

# unstable_api_call()
```

#### 1.4 实用装饰器

```python
# day13/useful_decorators.py
import functools
import time

def log_call(func):
    """记录函数调用"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"📞 调用 {func.__name__}(args={args}, kwargs={kwargs})")
        result = func(*args, **kwargs)
        print(f"📤 返回: {str(result)[:50]}")
        return result
    return wrapper

def cache_result(func):
    """简单缓存装饰器"""
    cached = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cached:
            cached[args] = func(*args)
        return cached[args]
    return wrapper

@cache_result
def expensive_calculation(n):
    time.sleep(1)  # 模拟耗时计算
    return n ** 2

print(expensive_calculation(5))  # 慢（1秒）
print(expensive_calculation(5))  # 快（缓存）
```

---

### 9:45 - 10:30 | 模块二：生成器与 typing

#### 2.1 生成器

```python
# day13/generator.py

# 生成器函数：使用 yield 代替 return
def count_up(n):
    """生成 0 到 n-1 的数字"""
    for i in range(n):
        yield i  # 暂停并返回值，下次从这儿继续

gen = count_up(5)
print(next(gen))  # 0
print(next(gen))  # 1
for num in gen:
    print(num)      # 2, 3, 4

# 生成器表达式（类似列表推导式）
squares = (x**2 for x in range(10))  # 注意是圆括号
print(sum(squares))  # 285

# 实用：逐行读取大文件（节省内存）
def read_large_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            yield line.strip()

# 实用：分批处理数据
def batch_items(items, batch_size=10):
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]

data = list(range(25))
for batch in batch_items(data, 10):
    print(f"处理批次: {batch}")
```

#### 2.2 typing 类型注解

```python
# day13/typing_demo.py
from typing import List, Dict, Optional, Union, Callable

def greet(name: str) -> str:
    """类型注解：参数和返回值类型"""
    return f"Hello, {name}!"

def process_messages(
    messages: List[Dict[str, str]],
    temperature: float = 0.7,
) -> Optional[str]:
    """处理消息列表，返回回复或 None"""
    if not messages:
        return None
    return messages[-1].get("content", "")

def apply_func(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)

# 类型注解不影响运行，但 IDE 会提供更好的提示
# 可以用 mypy 进行静态类型检查
```

| typing 类型 | 含义 | 示例 |
|-------------|------|------|
| `List[str]` | 字符串列表 | `["a", "b"]` |
| `Dict[str, int]` | 字符串键整数值的字典 | `{"a": 1}` |
| `Optional[str]` | str 或 None | `None` |
| `Union[int, str]` | int 或 str | `42` 或 `"42"` |
| `Callable` | 可调用对象 | 函数 |
| `Tuple[str, int]` | 固定类型元组 | `("a", 1)` |

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：dotenv 与 asyncio 入门

#### 3.1 python-dotenv 环境变量管理

```bash
pip install python-dotenv
```

```python
# day13/dotenv_demo.py
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 读取环境变量
api_key = os.getenv("DEEPSEEK_API_KEY")
model = os.getenv("MODEL_NAME", "deepseek-chat")  # 带默认值
base_url = os.getenv("BASE_URL", "https://api.deepseek.com")

print(f"API Key: {'已设置' if api_key else '未设置'}")
print(f"Model: {model}")
```

**.env 文件（不提交到 Git！）：**

```env
# .env
DEEPSEEK_API_KEY=sk-your-actual-api-key
MODEL_NAME=deepseek-chat
BASE_URL=https://api.deepseek.com
TEMPERATURE=0.7
MAX_TOKENS=2048
```

**.gitignore 中添加：**

```
.env
```

#### 3.2 asyncio 异步编程入门

```python
# day13/asyncio_basic.py
import asyncio

# 异步函数
async def fetch_data(name, delay):
    print(f"开始获取 {name}...")
    await asyncio.sleep(delay)  # 非阻塞等待
    print(f"完成 {name}")
    return f"{name} 的数据"

# 运行单个异步函数
async def main():
    result = await fetch_data("API-1", 1)
    print(result)

asyncio.run(main())

# 并发执行多个任务
async def main_concurrent():
    tasks = [
        fetch_data("API-1", 1),
        fetch_data("API-2", 2),
        fetch_data("API-3", 1.5),
    ]
    results = await asyncio.gather(*tasks)
    print(results)

# asyncio.run(main_concurrent())
# 三个任务并发执行，总耗时约 2 秒（而非 4.5 秒）
```

> 💡 asyncio 在 Day 30+ 的 FastAPI 和 Day 39+ 的 Agent 并发调用中会深入使用。今天了解基本概念即可。

#### 3.3 API 重试装饰器（综合应用）

```python
# day13/api_retry.py
import time
import functools
import requests
from typing import Callable, Any

def api_retry(max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """
    API 调用重试装饰器
    - max_retries: 最大重试次数
    - delay: 初始延迟（秒）
    - backoff: 延迟倍增因子
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            current_delay = delay
            last_exception = None

            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except (requests.exceptions.Timeout,
                        requests.exceptions.ConnectionError) as e:
                    last_exception = e
                    if attempt < max_retries:
                        print(f"⚠️ 第 {attempt} 次请求失败，{current_delay:.1f}s 后重试...")
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        print(f"❌ 已达最大重试次数 ({max_retries})")

            raise last_exception
        return wrapper
    return decorator


@api_retry(max_retries=3, delay=1, backoff=2)
def call_llm_api(url, headers, body):
    response = requests.post(url, headers=headers, json=body, timeout=30)
    response.raise_for_status()
    return response.json()
```

---

## 🌇 下午实操（14:00 - 17:30）

### 14:00 - 17:00 | 实操项目：增强版 AI 客户端

#### 项目需求

整合 Day 12-13 的知识：
1. 使用 dotenv 管理 API Key
2. 使用装饰器添加日志、计时、重试
3. 使用 typing 类型注解
4. 使用生成器处理流式响应（了解）

#### 参考代码

创建文件 `day13/enhanced_client.py`：

```python
"""
Day 13 实操项目：增强版 AI 客户端
整合：dotenv + 装饰器 + typing + 重试
"""

import os
import time
import functools
import requests
from typing import List, Dict, Optional, Tuple
from dotenv import load_dotenv

load_dotenv()


# ===== 装饰器 =====

def log_api_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"📡 API 调用: {func.__name__}")
        start = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            print(f"✅ 成功 ({elapsed:.2f}s)")
            return result
        except Exception as e:
            elapsed = time.time() - start
            print(f"❌ 失败 ({elapsed:.2f}s): {e}")
            raise
    return wrapper


def retry_on_failure(max_retries=3, delay=1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except (requests.exceptions.Timeout,
                        requests.exceptions.ConnectionError) as e:
                    if attempt == max_retries:
                        raise
                    wait = delay * attempt
                    print(f"⚠️ 重试 {attempt}/{max_retries}，等待 {wait}s...")
                    time.sleep(wait)
        return wrapper
    return decorator


# ===== AI 客户端 =====

class EnhancedAIClient:
    """增强版 AI 客户端"""

    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY", "")
        self.model = os.getenv("MODEL_NAME", "deepseek-chat")
        self.base_url = os.getenv("BASE_URL", "https://api.deepseek.com")
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "2048"))
        self.total_tokens = 0
        self.call_count = 0

        if not self.api_key:
            raise ValueError("请在 .env 文件中设置 DEEPSEEK_API_KEY")

    @log_api_call
    @retry_on_failure(max_retries=3, delay=1.0)
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
    ) -> Tuple[str, Dict]:
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        body = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature or self.temperature,
            "max_tokens": self.max_tokens,
        }

        response = requests.post(url, headers=headers, json=body, timeout=60)
        response.raise_for_status()
        data = response.json()

        content = data["choices"][0]["message"]["content"]
        usage = data["usage"]
        self.total_tokens += usage["total_tokens"]
        self.call_count += 1

        return content, usage

    def get_stats(self) -> Dict:
        return {
            "model": self.model,
            "calls": self.call_count,
            "total_tokens": self.total_tokens,
        }


def main():
    print("=" * 50)
    print("   🚀 增强版 AI 客户端")
    print("=" * 50)

    try:
        client = EnhancedAIClient()
    except ValueError as e:
        print(f"❌ 配置错误: {e}")
        print("请创建 .env 文件并设置 DEEPSEEK_API_KEY")
        return

    messages = [
        {"role": "system", "content": "你是一个简洁的 AI 助手。"},
    ]

    print(f"模型: {client.model}")
    print("输入消息对话，/quit 退出\n")

    while True:
        user_input = input("你: ").strip()
        if user_input.lower() in ("/quit", "/exit", "q"):
            break
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        try:
            reply, usage = client.chat(messages)
            messages.append({"role": "assistant", "content": reply})
            print(f"AI: {reply}")
            print(f"   [{usage['total_tokens']} tokens]")
        except Exception as e:
            print(f"❌ 错误: {e}")
            messages.pop()  # 移除失败的用户消息

    stats = client.get_stats()
    print(f"\n📊 统计: {stats['calls']} 次调用, {stats['total_tokens']} tokens")


if __name__ == "__main__":
    main()
```

**创建 .env 文件：**

```env
DEEPSEEK_API_KEY=sk-your-api-key
MODEL_NAME=deepseek-chat
BASE_URL=https://api.deepseek.com
TEMPERATURE=0.7
MAX_TOKENS=2048
```

**更新 requirements.txt：**

```
requests>=2.31.0
python-dotenv>=1.0.0
```

---

### 17:00 - 17:30 | 知识串联

```
Day 1-6:  Python 基础语法
Day 7:    第一周复习
Day 8-9:  面向对象 → ChatMessage, BaseModel
Day 10:   模块包 → llm_toolkit
Day 11:   文件操作 → 配置/日志
Day 12:   API 调用 → requests
Day 13:   进阶语法 → 装饰器 + dotenv ← 今天
Day 14:   阶段考核 → 综合项目 ← 明天
```

---

## 🌙 晚自习（19:00 - 21:00）

- 完成增强版 AI 客户端
- 创建 .env 文件（确保不提交到 Git）
- 测试重试装饰器（可临时断开网络模拟）
- 预习 Day 14 阶段考核要求
- Git 提交：`git commit -m "Day 13: 进阶语法与增强AI客户端"`

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | 装饰器概念与 @语法 | |
| 2 | 带参数的装饰器 | |
| 3 | functools.wraps | |
| 4 | 生成器 yield | |
| 5 | typing 类型注解 | |
| 6 | python-dotenv 用法 | |
| 7 | .env 文件管理密钥 | |
| 8 | asyncio 基础概念 | |
| 9 | API 重试装饰器 | |
| 10 | 增强版 AI 客户端项目 | |

---

## 📝 课后作业

### 必做题

1. 完成增强版 AI 客户端项目
2. 创建 .env 文件并确保 .gitignore 包含 .env
3. 实现 `@rate_limit` 装饰器，限制每分钟最多 10 次调用

### 选做题

4. 用生成器实现对话历史的惰性加载
5. 了解 `httpx` 库的 async 用法

---

## 💡 常见问题 FAQ

**Q1: 装饰器的执行顺序？**

A: 多个装饰器从下往上包装：`@a @b def f` 等价于 `f = a(b(f))`。执行时从上往下。

**Q2: .env 文件和环境变量有什么区别？**

A: `.env` 是本地配置文件，方便开发；生产环境通常直接设置系统环境变量。两者通过 `os.getenv()` 读取。

**Q3: 生成器和列表有什么区别？**

A: 生成器惰性求值、节省内存，适合大数据流。列表一次性加载全部数据到内存。

**Q4: 现在需要深入学 asyncio 吗？**

A: 今天了解概念即可。Day 30+ 使用 FastAPI 时会实际需要 async/await。

---

## 🔮 明日预习

**Day 14: 阶段考核项目一** — 命令行多轮对话 AI 助手完整项目

明天的项目是第一阶段总结考核，将综合运用 Day 1-13 的所有技能。今晚请：
1. 回顾所有项目代码
2. 确保 API Key 和 .env 配置正确
3. 准备好 GitHub 仓库

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 13*
