# Day 12: 网络请求与 API 调用

> **培训阶段**: 第一阶段 Python 编程基础 | **第 2 周** | **学习时长**: 约 6-8 小时  
> **今日关键词**: HTTP 基础、requests 库、大模型 API、命令行 AI 问答

---

## 📍 课程导航

### 上节回顾
在 **Day 11** 中，你学习了文件读写、pathlib、datetime、random、re 标准库，完成了「文档关键词统计」项目。今天是里程碑日——你将 **首次真正调用大模型 API**！

### 本节学习目标
完成本日学习后，你将能够：

1. 理解 HTTP 协议基础（请求/响应、状态码）
2. 使用 `requests` 库发送 HTTP 请求
3. 调用 DeepSeek / 通义千问等大模型 API
4. 处理 API 认证、请求体和响应解析
5. 完成「命令行 AI 问答」项目

### 与后续课程的衔接
- **Day 13** 将用装饰器添加 API 重试逻辑
- **Day 14** 阶段考核将构建完整的多轮对话助手
- **Day 15+** Prompt 工程将在今天的基础上优化提示词
- **Day 25+** RAG 开发将调用 Embedding API

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：HTTP 基础

#### 1.1 什么是 HTTP？

**HTTP**（HyperText Transfer Protocol）是互联网上数据通信的基础协议。浏览器访问网页、App 调用 API，底层都是 HTTP。

```
客户端（你的程序）                    服务器（大模型 API）
      │                                      │
      │──── HTTP Request（请求）──────────→  │
      │     POST /v1/chat/completions       │
      │     Headers: Authorization: Bearer  │
      │     Body: {"model": "...", ...}       │
      │                                      │
      │←─── HTTP Response（响应）──────────  │
      │     Status: 200 OK                    │
      │     Body: {"choices": [...]}          │
```

#### 1.2 HTTP 方法

| 方法 | 用途 | 大模型开发 |
|------|------|------------|
| GET | 获取资源 | 查询模型列表 |
| POST | 提交数据 | **发送对话请求（最常用）** |
| PUT | 更新资源 | 更新配置 |
| DELETE | 删除资源 | 删除文件 |

#### 1.3 HTTP 状态码

| 状态码 | 含义 | 处理方式 |
|--------|------|----------|
| 200 | 成功 | 解析响应 |
| 400 | 请求错误 | 检查请求体格式 |
| 401 | 未授权 | 检查 API Key |
| 403 | 禁止访问 | 检查权限/余额 |
| 404 | 未找到 | 检查 URL |
| 429 | 请求过多 | 等待后重试 |
| 500 | 服务器错误 | 稍后重试 |

#### 1.4 大模型 API 通用格式

几乎所有大模型 API 都遵循 OpenAI 兼容格式：

```python
# 请求
POST https://api.deepseek.com/chat/completions
Headers:
    Authorization: Bearer sk-xxxxxxxx
    Content-Type: application/json
Body:
{
    "model": "deepseek-chat",
    "messages": [
        {"role": "system", "content": "你是一个有帮助的助手。"},
        {"role": "user", "content": "你好"}
    ],
    "temperature": 0.7,
    "max_tokens": 1024
}

# 响应
{
    "choices": [{
        "message": {
            "role": "assistant",
            "content": "你好！有什么可以帮你的吗？"
        }
    }],
    "usage": {
        "prompt_tokens": 20,
        "completion_tokens": 15,
        "total_tokens": 35
    }
}
```

---

### 9:45 - 10:30 | 模块二：requests 库

#### 2.1 安装与基本用法

```bash
pip install requests
```

```python
# day12/requests_basic.py
import requests

# GET 请求
response = requests.get("https://httpbin.org/get", params={"key": "value"})
print(response.status_code)  # 200
print(response.json())       # 解析 JSON 响应

# POST 请求
data = {"name": "张三", "age": 25}
response = requests.post("https://httpbin.org/post", json=data)
print(response.json())
```

#### 2.2 Response 对象

```python
# day12/response_demo.py
import requests

response = requests.get("https://httpbin.org/get")

print(response.status_code)     # 200
print(response.headers)         # 响应头字典
print(response.text)            # 响应文本
print(response.json())          # 解析为 Python 字典
print(response.ok)              # True（状态码 < 400）
print(response.elapsed)         # 请求耗时
```

#### 2.3 请求参数详解

```python
# day12/requests_params.py
import requests

# Headers
headers = {
    "Authorization": "Bearer sk-your-api-key",
    "Content-Type": "application/json",
}

# JSON Body
body = {
    "model": "deepseek-chat",
    "messages": [{"role": "user", "content": "你好"}],
}

response = requests.post(
    url="https://api.deepseek.com/chat/completions",
    headers=headers,
    json=body,          # 自动序列化为 JSON
    timeout=30,         # 超时时间（秒）
)

# 检查状态
if response.status_code == 200:
    data = response.json()
    print(data["choices"][0]["message"]["content"])
else:
    print(f"请求失败: {response.status_code}")
    print(response.text)
```

#### 2.4 异常处理

```python
# day12/requests_errors.py
import requests

def safe_request(url, **kwargs):
    try:
        response = requests.post(url, timeout=30, **kwargs)
        response.raise_for_status()  # 非 2xx 状态码抛出异常
        return response.json()
    except requests.exceptions.Timeout:
        print("请求超时")
    except requests.exceptions.ConnectionError:
        print("网络连接失败")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP 错误: {e.response.status_code}")
        print(e.response.text)
    except requests.exceptions.JSONDecodeError:
        print("响应不是有效 JSON")
    return None
```

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：首次调用大模型 API

#### 3.1 获取 API Key

| 平台 | 注册地址 | 模型 |
|------|----------|------|
| DeepSeek | https://platform.deepseek.com | deepseek-chat |
| 通义千问 | https://dashscope.aliyun.com | qwen-plus |
| 智谱 AI | https://open.bigmodel.cn | glm-4 |

> 💡 本课程推荐使用 **DeepSeek**（性价比高）或 **通义千问**（中文优秀）。

#### 3.2 第一次 API 调用

```python
# day12/first_api_call.py
import requests
import json

API_KEY = "sk-your-api-key-here"  # 替换为你的 API Key
BASE_URL = "https://api.deepseek.com"

def chat(message, model="deepseek-chat"):
    """发送单轮对话请求"""
    url = f"{BASE_URL}/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    body = {
        "model": model,
        "messages": [
            {"role": "user", "content": message}
        ],
        "temperature": 0.7,
        "max_tokens": 1024,
    }

    print(f"📤 发送请求到 {model}...")
    response = requests.post(url, headers=headers, json=body, timeout=60)

    if response.status_code == 200:
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        usage = data["usage"]
        print(f"📥 回复 ({usage['total_tokens']} tokens):")
        print(content)
        return content
    else:
        print(f"❌ 请求失败: {response.status_code}")
        print(response.text)
        return None

# 测试
if __name__ == "__main__":
    chat("用一句话解释什么是大语言模型")
```

#### 3.3 多轮对话

```python
# day12/multi_turn.py
import requests

API_KEY = "sk-your-api-key-here"
BASE_URL = "https://api.deepseek.com"

def chat_with_history(messages, model="deepseek-chat"):
    """支持多轮对话的 API 调用"""
    url = f"{BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    body = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
    }

    response = requests.post(url, headers=headers, json=body, timeout=60)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]

# 多轮对话示例
messages = [
    {"role": "system", "content": "你是一个简洁的 Python 导师。"},
]

# 第一轮
messages.append({"role": "user", "content": "什么是列表？"})
reply = chat_with_history(messages)
print(f"AI: {reply}")
messages.append({"role": "assistant", "content": reply})

# 第二轮（AI 记得上文）
messages.append({"role": "user", "content": "给个例子"})
reply = chat_with_history(messages)
print(f"AI: {reply}")
```

#### 3.4 封装 API 客户端类

```python
# day12/api_client.py
import requests

class DeepSeekClient:
    """DeepSeek API 客户端"""

    def __init__(self, api_key, base_url="https://api.deepseek.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.total_tokens = 0

    def chat(self, messages, model="deepseek-chat", temperature=0.7, max_tokens=2048):
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        body = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        response = requests.post(url, headers=headers, json=body, timeout=60)
        response.raise_for_status()
        data = response.json()

        content = data["choices"][0]["message"]["content"]
        usage = data["usage"]
        self.total_tokens += usage["total_tokens"]

        return content, usage

    def get_stats(self):
        return {"total_tokens": self.total_tokens}
```

---

## 🌇 下午实操（14:00 - 17:30）

### 14:00 - 17:00 | 实操项目：命令行 AI 问答

#### 项目需求

1. 支持配置 API Key 和模型选择
2. 支持多轮对话（保持上下文）
3. 支持 system prompt 设置
4. 显示 token 用量统计
5. 支持清空对话历史
6. 异常处理（网络错误、API 错误）

#### 参考代码

创建文件 `day12/ai_chat.py`：

```python
"""
Day 12 实操项目：命令行 AI 问答
首次真正调用大模型 API！
"""

import requests
import json
import sys


class AIChat:
    """命令行 AI 问答应用"""

    MODELS = {
        "1": ("deepseek-chat", "https://api.deepseek.com"),
        "2": ("qwen-plus", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
    }

    def __init__(self, api_key):
        self.api_key = api_key
        self.model = "deepseek-chat"
        self.base_url = "https://api.deepseek.com"
        self.messages = []
        self.total_tokens = 0
        self.total_requests = 0

    def set_model(self, key):
        if key in self.MODELS:
            self.model, self.base_url = self.MODELS[key]
            print(f"✅ 已切换到 {self.model}")
        else:
            print("⚠️ 无效选择")

    def set_system_prompt(self, prompt):
        self.messages = [{"role": "system", "content": prompt}]
        print(f"✅ 系统提示已设置")

    def send(self, user_message):
        """发送消息并获取回复"""
        self.messages.append({"role": "user", "content": user_message})

        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        body = {
            "model": self.model,
            "messages": self.messages,
            "temperature": 0.7,
            "max_tokens": 2048,
        }

        try:
            response = requests.post(url, headers=headers, json=body, timeout=60)
            response.raise_for_status()
            data = response.json()

            reply = data["choices"][0]["message"]["content"]
            usage = data["usage"]
            self.total_tokens += usage["total_tokens"]
            self.total_requests += 1

            self.messages.append({"role": "assistant", "content": reply})
            return reply, usage

        except requests.exceptions.HTTPError as e:
            status = e.response.status_code
            if status == 401:
                return "❌ API Key 无效，请检查配置", None
            elif status == 429:
                return "❌ 请求过于频繁，请稍后重试", None
            else:
                return f"❌ HTTP 错误 {status}: {e.response.text[:200]}", None
        except requests.exceptions.Timeout:
            return "❌ 请求超时，请检查网络", None
        except requests.exceptions.ConnectionError:
            return "❌ 网络连接失败", None
        except Exception as e:
            return f"❌ 未知错误: {e}", None

    def clear_history(self):
        system = [m for m in self.messages if m["role"] == "system"]
        self.messages = system
        print("✅ 对话历史已清空（保留 system prompt）")

    def show_stats(self):
        print(f"\n📊 使用统计")
        print(f"  模型: {self.model}")
        print(f"  请求次数: {self.total_requests}")
        print(f"  总 tokens: {self.total_tokens}")
        print(f"  对话轮数: {len([m for m in self.messages if m['role'] == 'user'])}")

    def show_history(self):
        print(f"\n💬 对话历史 ({len(self.messages)} 条)")
        for msg in self.messages:
            icon = {"system": "⚙️", "user": "👤", "assistant": "🤖"}.get(msg["role"], "?")
            content = msg["content"][:80] + "..." if len(msg["content"]) > 80 else msg["content"]
            print(f"  {icon} {content}")

    def run(self):
        print("=" * 50)
        print("     🤖 命令行 AI 问答 v1.0")
        print("=" * 50)
        print(f"当前模型: {self.model}")
        print("输入消息直接对话，输入 /help 查看命令")

        while True:
            try:
                user_input = input("\n你: ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\n再见！")
                break

            if not user_input:
                continue

            # 命令处理
            if user_input.startswith("/"):
                cmd = user_input.lower()
                if cmd in ("/quit", "/exit", "/q"):
                    self.show_stats()
                    print("再见！")
                    break
                elif cmd == "/help":
                    print("命令: /help /clear /history /stats /model /system /quit")
                elif cmd == "/clear":
                    self.clear_history()
                elif cmd == "/history":
                    self.show_history()
                elif cmd == "/stats":
                    self.show_stats()
                elif cmd == "/model":
                    print("  1. DeepSeek  2. 通义千问")
                    self.set_model(input("选择: ").strip())
                elif cmd.startswith("/system"):
                    prompt = user_input[8:].strip() or input("系统提示: ")
                    self.set_system_prompt(prompt)
                else:
                    print(f"未知命令: {user_input}")
                continue

            # 发送消息
            print("🤖 AI: ", end="", flush=True)
            reply, usage = self.send(user_input)
            print(reply)
            if usage:
                print(f"   [{usage['total_tokens']} tokens]")


def main():
    api_key = input("请输入 API Key: ").strip()
    if not api_key:
        print("❌ API Key 不能为空")
        sys.exit(1)

    chat = AIChat(api_key)

    # 可选：设置默认 system prompt
    system = input("系统提示 (回车跳过): ").strip()
    if system:
        chat.set_system_prompt(system)

    chat.run()


if __name__ == "__main__":
    main()
```

#### 运行效果

```
==================================================
     🤖 命令行 AI 问答 v1.0
==================================================
当前模型: deepseek-chat

你: 什么是 Python？
🤖 AI: Python 是一种高级、解释型的编程语言...
   [45 tokens]

你: 给我一个 Hello World
🤖 AI: 当然！Python 的 Hello World 非常简单：
```python
print("Hello, World!")
```
   [62 tokens]

你: /stats

📊 使用统计
  模型: deepseek-chat
  请求次数: 2
  总 tokens: 107
```

---

### 17:00 - 17:30 | API 调试技巧

```python
# 调试：打印完整请求和响应
import requests
import json

def debug_api_call(url, headers, body):
    print("=== 请求 ===")
    print(f"URL: {url}")
    print(f"Headers: {json.dumps({k: v[:10]+'...' if k=='Authorization' else v for k,v in headers.items()}, indent=2)}")
    print(f"Body: {json.dumps(body, ensure_ascii=False, indent=2)}")

    response = requests.post(url, headers=headers, json=body, timeout=60)

    print(f"\n=== 响应 ===")
    print(f"Status: {response.status_code}")
    print(f"Body: {response.text[:500]}")
    return response
```

---

## 🌙 晚自习（19:00 - 21:00）

- 注册 API 平台并获取 API Key
- 完成命令行 AI 问答项目并真正调用 API
- 测试 DeepSeek 和通义千问两个模型
- Git 提交：`git commit -m "Day 12: 首次调用大模型API"`

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | HTTP 请求/响应概念 | |
| 2 | HTTP 状态码含义 | |
| 3 | requests 库基本用法 | |
| 4 | POST 请求与 JSON Body | |
| 5 | API 认证（Bearer Token） | |
| 6 | 大模型 API 请求格式 | |
| 7 | 响应解析与 token 统计 | |
| 8 | 多轮对话实现 | |
| 9 | 命令行 AI 问答项目 | |

---

## 📝 课后作业

### 必做题

1. **命令行 AI 问答**：完成项目并成功调用 API
2. **双模型测试**：分别用 DeepSeek 和通义千问完成一次对话
3. **API 客户端类**：独立实现 `DeepSeekClient` 类（不参考讲义）

### 选做题

4. 添加流式输出（stream=True）支持
5. 实现对话历史自动保存到 JSON 文件

---

## 💡 常见问题 FAQ

**Q1: API Key 报错 401 怎么办？**

A: 检查：1) Key 是否正确复制；2) 是否有余额；3) Authorization 头格式是否为 `Bearer sk-xxx`。

**Q2: 请求超时怎么办？**

A: 增大 `timeout` 参数；检查网络；复杂问题可减少 `max_tokens`。

**Q3: 如何控制 API 费用？**

A: 设置 `max_tokens` 限制；监控 `usage` 中的 token 数；选择性价比高的模型。

**Q4: API Key 能写在代码里吗？**

A: 不能！明天 Day 13 会学习用 `.env` 文件安全管理密钥。

---

## 🔮 明日预习

**Day 13: 进阶语法与异步入门** — 装饰器、生成器、typing、asyncio、python-dotenv、重试装饰器

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 12*
