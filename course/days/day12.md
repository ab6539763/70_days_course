# Day 12: 网络请求与 API 调用（关键日！）

> **零基础大模型应用开发 70 天培训课程** | 第 12/70 天 | Python 编程基础


——————




## 深度讲义


### 12.1 HTTP 协议纳米级拆解

#### 一次 API 调用的完整过程

```
你的 Python 程序                大模型服务器
      │                              │
      │  1. 建立 TCP 连接             │
      │ ─────────────────────────→   │
      │  2. 发送 HTTP POST 请求       │
      │  (Header + JSON Body)        │
      │ ─────────────────────────→   │
      │                              │ 3. 处理请求
      │                              │ 4. 生成回复
      │  5. 返回 HTTP 响应            │
      │  (Status Code + JSON Body)   │
      │ ←─────────────────────────   │
      │  6. 解析 JSON，提取回复       │
```

#### 请求结构

```
POST /v1/chat/completions HTTP/1.1
Host: api.deepseek.com
Authorization: Bearer sk-xxxx
Content-Type: application/json

{
  "model": "deepseek-chat",
  "messages": [
    {"role": "user", "content": "你好"}
  ]
}
```

#### 响应结构

```json
{
  "choices": [{
    "message": {
      "role": "assistant",
      "content": "你好！有什么可以帮你的？"
    }
  }]
}
```

### 12.2 API Key 安全

- ❌ 不要把 API Key 写在代码里
- ❌ 不要把 API Key 提交到 GitHub
- ✅ 使用环境变量（Day 13 学 dotenv）
- ✅ 使用 `.gitignore` 排除 `.env` 文件

### 12.3 获取免费 API Key

1. **DeepSeek**: https://platform.deepseek.com/ （注册送额度）
2. **通义千问**: https://dashscope.aliyun.com/ （免费额度）
3. **智谱 AI**: https://open.bigmodel.cn/ （GLM 系列）


## 完整项目代码（可直接运行）

### 文件: `day12_ai_chat.py`

```python
"""Day 12: 命令行 AI 问答小程序 — 首次调用大模型 API"""
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("DEEPSEEK_API_KEY", "your-api-key-here")
API_URL = "https://api.deepseek.com/v1/chat/completions"
MODEL = "deepseek-chat"


def chat(user_message: str, system_prompt: str = "你是一个有帮助的 AI 助手。") -> str:
  headers = {
      "Authorization": f"Bearer {API_KEY}",
      "Content-Type": "application/json",
  }
  payload = {
      "model": MODEL,
      "messages": [
          {"role": "system", "content": system_prompt},
          {"role": "user", "content": user_message},
      ],
      "temperature": 0.7,
  }
  response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
  response.raise_for_status()
  data = response.json()
  return data["choices"][0]["message"]["content"]


def main():
    print("🤖 AI 问答小程序（输入 quit 退出）")
    while True:
        user_input = input("\n你: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            print("再见！")
            break
        if not user_input:
            continue
        try:
            reply = chat(user_input)
            print(f"AI: {reply}")
        except requests.exceptions.HTTPError as e:
            print(f"API 错误: {e}")
        except Exception as e:
            print(f"发生错误: {e}")


if __name__ == "__main__":
    main()
```

### 运行步骤

```bash
cd course/code/day12
pip install -r requirements.txt  # 如有依赖
python day12_ai_chat.py
```


## 常见错误与避坑

- ⚠️ 只看不练 — 必须动手敲代码
- ⚠️ 跳过基础直接调 API — 每天知识环环相扣
- ⚠️ 不写注释 — 企业级代码必须可读

## 课堂练习

- 📝 复习 Day 11 的核心知识点
- 📝 完成今日实操项目并提交 Git
- 📝 用 3 句话总结今天学到了什么


## 课程衔接说明



### ⬅️ 昨日回顾

**Day 11** 学习了「文件操作与常用标准库」，今天的知识直接建立在昨天之上。

### 🔗 今日定位

承接 Day 5 JSON + Day 8 ChatMessage，正式进入大模型开发主线。

### ➡️ 明日预告

**Day 13** 将学习「进阶语法与异步入门」，今天务必打牢基础。


### 今日时间安排

| 时段 | 内容 |
|------|------|
| 09:00-12:00 上午 | HTTP 协议基础(GET/POST、状态码、Header、Body) |
| 09:00-12:00 上午 | requests 库详解 |
| 09:00-12:00 上午 | 首次调用大模型 API（DeepSeek 或通义千问免费额度） |
| 09:00-12:00 上午 | 理解 API Key、请求体结构、messages 格式、解析返回结果 |
| 14:00-17:30 下午 | 🛠️ 写一个命令行 AI 问答小程序 |
| 19:00-21:00 晚自习 | 阅读 API 文档，整理请求/响应字段表 |



## 一、今日学习目标



完成今天的学习后，你将能够:

- HTTP 协议基础(GET/POST、状态码、Header、Body)
- requests 库详解
- 首次调用大模型 API（DeepSeek 或通义千问免费额度）
- 理解 API Key、请求体结构、messages 格式、解析返回结果

### 核心技能点

- **HTTP**
- **requests**
- **大模型 API**
- **messages**

### 与课程主线的关系

今天是 **第 1 阶段（Python 编程基础）** 的第 12 天。

> 今日主题「网络请求与 API 调用（关键日！）」是整条 70 天学习路径中的关键一环。请对照总路线图理解今天学什么、为什么学、后面哪里会用到。



## 二、理论精讲（纳米级拆解）


### 2.1 HTTP 协议基础(GET/POST、状态码、Header、Body)

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

### 2.2 requests 库详解

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

### 2.3 首次调用大模型 API（DeepSeek 或通义千问免费额度）

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

### 2.4 理解 API Key、请求体结构、messages 格式、解析返回结果

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

今日下午核心项目: **命令行 AI 问答小程序**
- 写一个命令行 AI 问答小程序



## 下午实操：项目实战



### 项目名称

**命令行 AI 问答小程序**

### 推荐项目目录结构（企业级标准）

```text
day12_project/
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
# 文件名: day12_main.py
# 主题: Day 12 — 命令行 AI 问答小程序
# ================================

"""
Day 12 实操项目入口。

学习要点:
1. 复习昨天所学
2. 完成今日「命令行 AI 问答小程序」核心功能
3. 添加必要注释，提交 Git
"""


def main():
    """主函数 — 按今日课纲逐步实现"""
    print("Day 12: 命令行 AI 问答小程序")
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
5. **提交**: `git add . && git commit -m "Day 12: 命令行 AI 问答小程序"`



## 知识小测




**Q1.** 请用自己的话解释「HTTP」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 9-12 所学填写）
- 后续应用: 将在 Day 19 左右用到

</details>

**Q2.** 请用自己的话解释「requests」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 9-12 所学填写）
- 后续应用: 将在 Day 19 左右用到

</details>

**Q3.** 请用自己的话解释「大模型 API」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 9-12 所学填写）
- 后续应用: 将在 Day 19 左右用到

</details>

**Q4.** 请用自己的话解释「messages」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 9-12 所学填写）
- 后续应用: 将在 Day 19 左右用到

</details>


### 上机题

请不看课件，独立完成今日「实操项目」的核心功能。限时 60 分钟。



## 课后作业



### 必做

1. 完成今日实操项目「命令行 AI 问答小程序」
2. 提交代码到 GitHub（commit message: `Day 12: 命令行 AI 问答小程序`）
3. 在学习笔记中记录 3 个今天学到的新知识点

### 晚自习

- 阅读 API 文档，整理请求/响应字段表

### 选做

1. 阅读官方文档中与今日主题相关的章节
2. 尝试优化今日代码（更优雅的错误处理、更清晰的注释）


——————

**第 12/70 天 · 零基础大模型应用开发 70 天培训课程**

> 坚持每一天，70 天后你将成为一名合格的大模型应用开发者。
