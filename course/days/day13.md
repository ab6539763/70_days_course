# Day 13: 进阶语法与异步入门

> **零基础大模型应用开发 70 天培训课程** | 第 13/70 天 | Python 编程基础


——————





## 深度讲义

### 13.1 装饰器

```python
import time
import functools

def retry(max_attempts=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"重试 {attempt+1}/{max_attempts}: {e}")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3)
def call_api():
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()
```

### 13.2 环境变量

```python
# .env 文件（不要提交到 Git！）
# DEEPSEEK_API_KEY=sk-xxxx

from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
```

### 13.3 asyncio 入门

```python
import asyncio

async def fetch_data():
    await asyncio.sleep(1)  # 模拟 IO 等待
    return "data"

async def main():
    result = await fetch_data()
    print(result)

asyncio.run(main())
```


## 常见错误与避坑

- ⚠️ 只看不练 — 必须动手敲代码
- ⚠️ 跳过基础直接调 API — 每天知识环环相扣
- ⚠️ 不写注释 — 企业级代码必须可读

## 课堂练习

- 📝 复习 Day 12 的核心知识点
- 📝 完成今日实操项目并提交 Git
- 📝 用 3 句话总结今天学到了什么


## 课程衔接说明



### ⬅️ 昨日回顾

**Day 12** 学习了「网络请求与 API 调用（关键日！）」，今天的知识直接建立在昨天之上。

### 🔗 今日定位

承接 Day 12 API 调用，为 Day 23 FastAPI 异步接口埋伏笔。

### ➡️ 明日预告

**Day 14** 将学习「阶段考核 —— 项目一：命令行多轮对话 AI 助手」，今天务必打牢基础。


### 今日时间安排

| 时段 | 内容 |
|------|------|
| 09:00-12:00 上午 | 装饰器原理与应用、生成器与 yield |
| 09:00-12:00 上午 | 类型注解 typing、asyncio 异步编程入门(理解 async/await) |
| 09:00-12:00 上午 | 环境变量管理(python-dotenv，保护 API Key) |
| 14:00-17:30 下午 | 🛠️ 给 API 调用加上重试装饰器与超时控制 |
| 19:00-21:00 晚自习 | 用 dotenv 管理多环境 API Key |



## 一、今日学习目标



完成今天的学习后，你将能够:

- 装饰器原理与应用、生成器与 yield
- 类型注解 typing、asyncio 异步编程入门(理解 async/await)
- 环境变量管理(python-dotenv，保护 API Key)

### 核心技能点

- **装饰器**
- **asyncio**
- **dotenv**

### 与课程主线的关系

今天是 **第 1 阶段（Python 编程基础）** 的第 13 天。

> 今日主题「进阶语法与异步入门」是整条 70 天学习路径中的关键一环。请对照总路线图理解今天学什么、为什么学、后面哪里会用到。



## 二、理论精讲（纳米级拆解）


### 2.1 装饰器原理与应用、生成器与 yield

#### 核心概念

**装饰器原理与应用、生成器与 yield** 是今日学习的重要内容。

#### 为什么学？

在大模型应用开发中，这个知识点将在后续项目中直接用到:
- 与 Day 11 的知识形成递进
- 为 Day 16 的实操项目提供基础

#### 学习要点

1. 理解概念定义（用自己的话复述）
2. 跟着课件代码敲一遍（不要复制粘贴）
3. 完成课后练习巩固

#### 常见错误

- 只看不练 → 必须动手写代码
- 跳过基础 → 每天知识环环相扣，不要跳天

### 2.2 类型注解 typing、asyncio 异步编程入门(理解 async/await)

#### 核心概念

**类型注解 typing、asyncio 异步编程入门(理解 async/await)** 是今日学习的重要内容。

#### 为什么学？

在大模型应用开发中，这个知识点将在后续项目中直接用到:
- 与 Day 11 的知识形成递进
- 为 Day 16 的实操项目提供基础

#### 学习要点

1. 理解概念定义（用自己的话复述）
2. 跟着课件代码敲一遍（不要复制粘贴）
3. 完成课后练习巩固

#### 常见错误

- 只看不练 → 必须动手写代码
- 跳过基础 → 每天知识环环相扣，不要跳天

### 2.3 环境变量管理(python-dotenv，保护 API Key)

#### HTTP 协议基础

| 方法 | 用途 | 大模型场景 |
|------|------|-----------|
| GET | 获取资源 | 查询模型列表 |
| POST | 提交数据 | **调用 Chat API（最常用）** |

#### 关键概念

- **URL**: 接口地址，如 `https://api.deepseek.com/v1/chat/completions`
- **Header**: 请求头，携带 `Authorization: Bearer <API_KEY>`
- **Body**: 请求体，JSON 格式，包含 `model`、`messages` 等
- **Status Code**: 200=成功, 401=密钥错误, 429=频率限制

#### 大模型 API 请求结构

```python
import requests

API_KEY = "your-api-key"
URL = "https://api.deepseek.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

payload = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "system", "content": "你是一个有帮助的助手。"},
        {"role": "user", "content": "你好！"},
    ],
    "temperature": 0.7,
}

response = requests.post(URL, headers=headers, json=payload)
result = response.json()
print(result["choices"][0]["message"]["content"])
```

> 这段代码将在今天下午的实操中完整实现。

## 三、下午实操预告

今日下午核心项目: **带重试与超时的 API 客户端**
- 给 API 调用加上重试装饰器与超时控制



## 下午实操：项目实战



### 项目名称

**带重试与超时的 API 客户端**

### 推荐项目目录结构（企业级标准）

```text
day13_project/
├─ src/
│  ├─ __init__.py
│  └─ main.py
├─ data/
├─ outputs/
├─ tests/
├─ requirements.txt
└─ README.md
```

### 代码骨架

```python
# ================================
# 文件名: day13_main.py
# 主题: Day 13 — 带重试与超时的 API 客户端
# ================================

"""
Day 13 实操项目入口。

学习要点:
1. 复习昨天所学
2. 完成今日「带重试与超时的 API 客户端」核心功能
3. 添加必要注释，提交 Git
"""


def main():
    """主函数 — 按今日课纲逐步实现"""
    print("Day 13: 带重试与超时的 API 客户端")
    # TODO: 按课件逐步实现
    pass


if __name__ == "__main__":
    main()
```

### 实现步骤（纳米级拆解）

1. **需求确认**: 阅读今日课纲，明确输入/输出
2. **环境准备**: 激活 venv，`pip install` 今日所需依赖
3. **核心实现**: 按上午所学知识点逐步编码
4. **自测**: 手动运行 3 个以上测试用例
5. **提交**: `git add . && git commit -m "Day 13: 带重试与超时的 API 客户端"`



## 知识小测




**Q1.** 请用自己的话解释「装饰器」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 10-13 所学填写）
- 后续应用: 将在 Day 20 左右用到

</details>

**Q2.** 请用自己的话解释「asyncio」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 10-13 所学填写）
- 后续应用: 将在 Day 20 左右用到

</details>

**Q3.** 请用自己的话解释「dotenv」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 10-13 所学填写）
- 后续应用: 将在 Day 20 左右用到

</details>


### 上机题

请不看课件，独立完成今日「实操项目」的核心功能。限时 60 分钟。



## 课后作业



### 必做

1. 完成今日实操项目「带重试与超时的 API 客户端」
2. 提交代码到 GitHub（commit message: `Day 13: 带重试与超时的 API 客户端`）
3. 在学习笔记中记录 3 个今天学到的新知识点

### 晚自习

- 用 dotenv 管理多环境 API Key

### 选做

1. 阅读官方文档中与今日主题相关的章节
2. 尝试优化今日代码（更优雅的错误处理、更清晰的注释）


——————

**第 13/70 天 · 零基础大模型应用开发 70 天培训课程**

> 坚持每一天，70 天后你将成为一名合格的大模型应用开发者。
