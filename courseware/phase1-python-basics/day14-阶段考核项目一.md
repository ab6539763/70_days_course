# Day 14: 阶段考核项目一——命令行多轮对话 AI 助手

> **培训阶段**: 第一阶段 Python 编程基础 | **第 2 周** | **学习时长**: 约 6-8 小时  
> **今日关键词**: 阶段考核、多轮对话、AI 助手、综合项目、第一阶段总结

---

## 📍 课程导航

### 上节回顾
在 **Day 13** 中，你学习了装饰器、生成器、typing、asyncio 入门和 python-dotenv，完成了「增强版 AI 客户端」。今天是 **第一阶段考核日**——你将综合运用 Day 1-13 的所有技能，独立完成一个完整的「命令行多轮对话 AI 助手」。

### 本节学习目标
完成本日学习后，你将能够：

1. 独立设计和实现一个完整的多轮对话 AI 助手
2. 综合运用 OOP、模块、文件、API、装饰器等技能
3. 通过阶段考核评估（功能 + 代码质量）
4. 总结第一阶段学习成果，为第二阶段做准备

### 与后续课程的衔接
- **Day 15** 开始进入第二阶段：大模型理论与 Prompt 工程
- 本项目的代码结构将作为后续 Web 版 AI 助手（Day 20+）的基础
- 毕业时回顾 Day 14 的项目，你会惊讶于自己的进步

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：项目需求说明

#### 1.1 项目概述

**项目名称**：命令行多轮对话 AI 助手（CLI ChatBot）

**项目定位**：第一阶段结业考核项目，综合运用 Python 基础、OOP、文件操作、API 调用和进阶语法。

#### 1.2 功能需求

| 编号 | 功能 | 优先级 | 涉及知识 |
|------|------|--------|----------|
| F1 | 多轮对话（保持上下文） | 必须 | list, dict, API |
| F2 | 支持配置 API Key（.env） | 必须 | dotenv, 文件 |
| F3 | 支持切换模型 | 必须 | OOP, 多态 |
| F4 | 自定义 system prompt | 必须 | str, input |
| F5 | 对话历史查看 | 必须 | list 遍历 |
| F6 | 对话历史保存/加载 | 必须 | json, 文件 |
| F7 | 清空对话历史 | 必须 | list 操作 |
| F8 | Token 用量统计 | 必须 | dict, 变量 |
| F9 | API 调用重试 | 推荐 | 装饰器 |
| F10 | 调用日志记录 | 推荐 | 文件, datetime |
| F11 | 流式输出 | 加分 | 生成器 |
| F12 | 对话导出 Markdown | 加分 | 文件, str |

#### 1.3 技术要求

```
项目结构：
day14/
├── .env                    # API Key（不提交 Git）
├── .env.example            # 环境变量模板
├── requirements.txt        # 依赖
├── README.md               # 项目说明
├── chatbot/
│   ├── __init__.py
│   ├── config.py           # 配置管理
│   ├── message.py          # 消息类
│   ├── client.py           # API 客户端
│   ├── storage.py          # 存储管理
│   ├── decorators.py       # 装饰器
│   └── app.py              # 主应用
├── data/                   # 对话数据目录
│   └── .gitkeep
└── main.py                 # 入口
```

#### 1.4 评分标准

| 维度 | 权重 | 评分要点 |
|------|------|----------|
| 功能完整性 | 40% | 必须功能全部实现 |
| 代码质量 | 25% | 结构清晰、命名规范、有注释 |
| 异常处理 | 15% | API 错误、文件错误、输入验证 |
| 用户体验 | 10% | 界面友好、提示清晰 |
| 加分项 | 10% | 重试、日志、流式、导出等 |

---

### 9:45 - 10:30 | 模块二：架构设计

#### 2.1 类图

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  ChatMessage │     │  BaseClient   │     │ Conversation │
│─────────────│     │──────────────│     │─────────────│
│ role        │     │ api_key       │     │ messages[]  │
│ content     │     │ model         │     │ system_prompt│
│ timestamp   │     │ chat()        │     │ add_message()│
│ to_dict()   │     │ get_stats()   │     │ save()/load()│
└─────────────┘     └──────┬───────┘     └─────────────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
     ┌────────┴──┐  ┌─────┴─────┐  ┌──┴────────┐
     │ DeepSeek  │  │   Qwen    │  │   GLM     │
     │  Client   │  │  Client   │  │  Client   │
     └───────────┘  └───────────┘  └───────────┘
```

#### 2.2 数据流

```
用户输入 → ChatApp → Conversation（消息管理）
                          ↓
                    API Client（发送请求）
                          ↓
                    大模型 API（DeepSeek/Qwen）
                          ↓
                    解析响应 → 显示回复
                          ↓
                    Storage（保存历史）
```

#### 2.3 命令设计

| 命令 | 功能 |
|------|------|
| `/help` | 显示帮助 |
| `/quit` | 退出程序 |
| `/clear` | 清空对话 |
| `/history` | 查看历史 |
| `/save` | 保存对话 |
| `/load` | 加载对话 |
| `/model` | 切换模型 |
| `/system` | 设置系统提示 |
| `/stats` | 查看统计 |
| `/export` | 导出 Markdown |

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：分模块实现指导

#### 3.1 config.py — 配置管理

```python
# day14/chatbot/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """应用配置"""
    API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
    MODEL = os.getenv("MODEL_NAME", "deepseek-chat")
    BASE_URL = os.getenv("BASE_URL", "https://api.deepseek.com")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2048"))
    DATA_DIR = os.getenv("DATA_DIR", "day14/data")

    MODELS = {
        "deepseek": ("deepseek-chat", "https://api.deepseek.com"),
        "qwen": ("qwen-plus", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
    }

    @classmethod
    def validate(cls):
        if not cls.API_KEY:
            raise ValueError("请在 .env 中设置 DEEPSEEK_API_KEY")
```

#### 3.2 message.py — 消息类

```python
# day14/chatbot/message.py
from datetime import datetime
from typing import Dict, List

class ChatMessage:
    VALID_ROLES = ("system", "user", "assistant")

    def __init__(self, role: str, content: str):
        if role not in self.VALID_ROLES:
            raise ValueError(f"无效角色: {role}")
        self.role = role
        self.content = content
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        return {"role": self.role, "content": self.content}

    def to_full_dict(self) -> Dict:
        return {**self.to_dict(), "timestamp": self.timestamp}

    def __str__(self):
        icons = {"system": "⚙️", "user": "👤", "assistant": "🤖"}
        return f"{icons.get(self.role, '?')} {self.content[:60]}"


class Conversation:
    def __init__(self, system_prompt: str = ""):
        self.messages: List[ChatMessage] = []
        if system_prompt:
            self.messages.append(ChatMessage("system", system_prompt))

    def add(self, role: str, content: str):
        self.messages.append(ChatMessage(role, content))

    def get_api_messages(self) -> List[Dict]:
        return [m.to_dict() for m in self.messages]

    def clear(self, keep_system: bool = True):
        if keep_system:
            self.messages = [m for m in self.messages if m.role == "system"]
        else:
            self.messages = []

    def __len__(self):
        return len(self.messages)
```

#### 3.3 decorators.py — 装饰器

```python
# day14/chatbot/decorators.py
import time
import functools
import logging

logging.basicConfig(
    filename="day14/data/chatbot.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def log_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"调用 {func.__name__}")
        start = time.time()
        try:
            result = func(*args, **kwargs)
            logging.info(f"{func.__name__} 成功 ({time.time()-start:.2f}s)")
            return result
        except Exception as e:
            logging.error(f"{func.__name__} 失败: {e}")
            raise
    return wrapper

def retry(max_retries=3, delay=1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries:
                        raise
                    print(f"⚠️ 重试 {attempt}/{max_retries}...")
                    time.sleep(delay * attempt)
        return wrapper
    return decorator
```

---

## 🌇 下午实操（14:00 - 17:30）

### 14:00 - 17:00 | 阶段考核：独立完成项目

#### 核心模块参考实现

**client.py:**

```python
# day14/chatbot/client.py
import requests
from typing import List, Dict, Tuple, Optional
from .config import Config
from .decorators import log_call, retry

class BaseClient:
    def __init__(self, api_key: str, model: str, base_url: str):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self.total_tokens = 0
        self.call_count = 0

    @log_call
    @retry(max_retries=3)
    def chat(self, messages: List[Dict], temperature: float = 0.7) -> Tuple[str, Dict]:
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        body = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": Config.MAX_TOKENS,
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


def create_client(provider: str = "deepseek") -> BaseClient:
    model, base_url = Config.MODELS.get(provider, Config.MODELS["deepseek"])
    return BaseClient(Config.API_KEY, model, base_url)
```

**storage.py:**

```python
# day14/chatbot/storage.py
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict

class Storage:
    def __init__(self, data_dir: str = "day14/data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def save_conversation(self, messages: List[Dict], name: str = None) -> str:
        filename = name or f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.data_dir / filename
        data = {
            "saved_at": datetime.now().isoformat(),
            "message_count": len(messages),
            "messages": messages,
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return str(filepath)

    def load_conversation(self, filename: str) -> List[Dict]:
        filepath = self.data_dir / filename
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data["messages"]

    def list_conversations(self) -> List[str]:
        return [f.name for f in self.data_dir.glob("chat_*.json")]

    def export_markdown(self, messages: List[Dict], filename: str = None) -> str:
        filename = filename or f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        filepath = self.data_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("# 对话记录\n\n")
            for msg in messages:
                role = msg["role"]
                content = msg["content"]
                if role == "user":
                    f.write(f"## 👤 用户\n\n{content}\n\n")
                elif role == "assistant":
                    f.write(f"## 🤖 助手\n\n{content}\n\n")
                elif role == "system":
                    f.write(f"> **系统**: {content}\n\n")
        return str(filepath)
```

**app.py — 主应用（完整版）:**

```python
# day14/chatbot/app.py
"""
命令行多轮对话 AI 助手 — 主应用
"""

from .config import Config
from .message import Conversation
from .client import create_client, BaseClient
from .storage import Storage


class ChatApp:
    """命令行 AI 助手应用"""

    COMMANDS = {
        "/help": "显示帮助",
        "/quit": "退出",
        "/clear": "清空对话",
        "/history": "查看历史",
        "/save": "保存对话",
        "/load": "加载对话",
        "/model": "切换模型",
        "/system": "设置系统提示",
        "/stats": "查看统计",
        "/export": "导出 Markdown",
    }

    def __init__(self):
        Config.validate()
        self.conversation = Conversation()
        self.client: BaseClient = create_client("deepseek")
        self.storage = Storage(Config.DATA_DIR)

    def _handle_command(self, cmd: str) -> bool:
        """处理命令，返回 True 表示继续，False 表示退出"""
        cmd = cmd.lower().strip()

        if cmd in ("/quit", "/exit", "/q"):
            self._show_stats()
            print("\n👋 感谢使用，再见！")
            return False

        elif cmd == "/help":
            print("\n📖 可用命令:")
            for c, desc in self.COMMANDS.items():
                print(f"  {c:<12} {desc}")

        elif cmd == "/clear":
            self.conversation.clear()
            print("✅ 对话已清空")

        elif cmd == "/history":
            if not self.conversation.messages:
                print("📭 暂无对话历史")
            else:
                print(f"\n💬 对话历史 ({len(self.conversation)} 条)")
                for msg in self.conversation.messages:
                    print(f"  {msg}")

        elif cmd == "/save":
            msgs = [m.to_full_dict() for m in self.conversation.messages]
            path = self.storage.save_conversation(msgs)
            print(f"✅ 已保存到 {path}")

        elif cmd == "/load":
            files = self.storage.list_conversations()
            if not files:
                print("📭 没有已保存的对话")
                return True
            print("已保存的对话:")
            for i, f in enumerate(files, 1):
                print(f"  {i}. {f}")
            try:
                idx = int(input("选择编号: ")) - 1
                msgs = self.storage.load_conversation(files[idx])
                self.conversation = Conversation()
                for m in msgs:
                    self.conversation.add(m["role"], m["content"])
                print(f"✅ 已加载 {len(msgs)} 条消息")
            except (ValueError, IndexError):
                print("⚠️ 无效选择")

        elif cmd == "/model":
            print("可用模型: deepseek, qwen")
            provider = input("选择: ").strip().lower()
            if provider in Config.MODELS:
                self.client = create_client(provider)
                print(f"✅ 已切换到 {self.client.model}")
            else:
                print("⚠️ 无效选择")

        elif cmd.startswith("/system"):
            prompt = cmd[8:].strip() or input("系统提示: ").strip()
            if prompt:
                self.conversation.clear(keep_system=False)
                self.conversation.add("system", prompt)
                print("✅ 系统提示已设置")

        elif cmd == "/stats":
            self._show_stats()

        elif cmd == "/export":
            msgs = [m.to_full_dict() for m in self.conversation.messages]
            path = self.storage.export_markdown(msgs)
            print(f"✅ 已导出到 {path}")

        else:
            print(f"⚠️ 未知命令: {cmd}，输入 /help 查看帮助")

        return True

    def _show_stats(self):
        stats = self.client.get_stats()
        print(f"\n📊 使用统计")
        print(f"  模型: {stats['model']}")
        print(f"  API 调用: {stats['calls']} 次")
        print(f"  总 tokens: {stats['total_tokens']}")
        print(f"  对话消息: {len(self.conversation)} 条")

    def _send_message(self, user_input: str):
        self.conversation.add("user", user_input)
        print("🤖 ", end="", flush=True)

        try:
            reply, usage = self.client.chat(self.conversation.get_api_messages())
            self.conversation.add("assistant", reply)
            print(reply)
            print(f"   💰 {usage['total_tokens']} tokens "
                  f"(输入 {usage['prompt_tokens']} + 输出 {usage['completion_tokens']})")
        except Exception as e:
            self.conversation.messages.pop()  # 移除失败的用户消息
            print(f"❌ 请求失败: {e}")

    def run(self):
        print("=" * 55)
        print("     🤖 命令行多轮对话 AI 助手 v1.0")
        print("     第一阶段结业考核项目")
        print("=" * 55)
        print(f"模型: {self.client.model}")
        print("输入 /help 查看命令，直接输入文字开始对话\n")

        while True:
            try:
                user_input = input("你: ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\n")
                self._show_stats()
                print("👋 再见！")
                break

            if not user_input:
                continue

            if user_input.startswith("/"):
                if not self._handle_command(user_input):
                    break
            else:
                self._send_message(user_input)
```

**main.py — 入口:**

```python
# day14/main.py
"""Day 14 入口文件"""
from chatbot.app import ChatApp

if __name__ == "__main__":
    app = ChatApp()
    app.run()
```

**.env.example:**

```env
DEEPSEEK_API_KEY=sk-your-api-key-here
MODEL_NAME=deepseek-chat
BASE_URL=https://api.deepseek.com
TEMPERATURE=0.7
MAX_TOKENS=2048
DATA_DIR=day14/data
```

**requirements.txt:**

```
requests>=2.31.0
python-dotenv>=1.0.0
```

---

### 17:00 - 17:30 | 项目测试与提交

#### 测试清单

- [ ] 启动程序，显示欢迎信息
- [ ] 发送消息，收到 AI 回复
- [ ] 多轮对话，AI 记住上下文
- [ ] `/model` 切换模型
- [ ] `/system` 设置系统提示
- [ ] `/history` 查看对话历史
- [ ] `/save` 保存对话到 JSON
- [ ] `/load` 加载已保存对话
- [ ] `/export` 导出 Markdown
- [ ] `/stats` 显示 token 统计
- [ ] `/clear` 清空对话
- [ ] 断网时重试机制生效
- [ ] API Key 错误时友好提示

#### 提交要求

```bash
git add day14/
git commit -m "Day 14: 阶段考核 - 命令行多轮对话AI助手"
git push
```

---

## 🌙 晚自习（19:00 - 21:00）

### 19:00 - 20:00 | 第一阶段学习总结

#### 你学会了什么？

```
✅ Python 开发环境搭建与 Git 版本管理
✅ 变量、数据类型、运算符、字符串
✅ 流程控制：条件、循环
✅ 核心数据结构：列表、字典、JSON
✅ 函数与代码重构
✅ 面向对象编程：类、继承、多态
✅ 模块包与异常处理
✅ 文件操作与标准库
✅ HTTP 请求与 API 调用
✅ 装饰器、生成器、dotenv
✅ 独立完成多轮对话 AI 助手
```

#### 技能 → 应用 映射

| 技能 | 已应用 | 后续应用 |
|------|--------|----------|
| f-string | Prompt 模板 | Day 17 Prompt 工程 |
| JSON | API 交互 | 所有后续项目 |
| OOP | ChatMessage/Client | Day 25 RAG 文档类 |
| requests | 调用大模型 | Day 25+ 所有 API |
| 装饰器 | 重试/日志 | Day 39 Agent Tools |
| 文件操作 | 对话存储 | Day 25 文档加载 |

### 20:00 - 21:00 | 第二阶段预习

**Day 15 起进入新阶段：大模型理论与 Prompt 工程**

- Day 15-19: 大模型原理 + Prompt 工程
- Day 20-24: Web 开发（Flask/FastAPI）
- Day 25+: RAG 应用开发

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | 项目架构设计 | |
| 2 | 多模块协作 | |
| 3 | 多轮对话实现 | |
| 4 | 对话存储与加载 | |
| 5 | 模型切换 | |
| 6 | 装饰器应用 | |
| 7 | 异常处理完整性 | |
| 8 | 项目测试与提交 | |

---

## 📝 课后作业

### 必做题（阶段考核）

1. **完成 CLI ChatBot 项目**：所有必须功能（F1-F8）正常工作
2. **编写 README.md**：包含项目介绍、安装步骤、使用说明
3. **Git 提交**：推送到 GitHub，确保 `.env` 不在仓库中

### 加分项

4. 实现流式输出（F11）
5. 实现 Markdown 导出（F12）
6. 添加单元测试

---

## 💡 常见问题 FAQ

**Q1: 项目做不出来怎么办？**

A: 确保 Day 12-13 的代码能正常运行。考核项目本质上是 Day 12 + Day 13 的组合升级。先实现核心对话功能，再逐步添加其他功能。

**Q2: 考核不及格的标准？**

A: 无法完成多轮对话（F1）或无法调用 API（F2）视为不及格。其他功能缺失酌情扣分。

**Q3: 可以用 openai 库代替 requests 吗？**

A: 可以，但建议先用 requests 理解底层原理。openai 库在后续课程会介绍。

**Q4: 第一阶段结束后感觉还有很多不懂？**

A: 完全正常！编程是实践性技能，70 天课程会持续巩固。重要的是 Day 14 的项目能独立跑起来。

---

## 🎓 第一阶段结业

恭喜你完成 **第一阶段 Python 编程基础** 的全部 14 天学习！

从今天起，你不再只是「学 Python 的人」，而是「能调用大模型 API 的开发者」。

**Day 15 见——Prompt 工程等着你！**

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 14 · 第一阶段完结*
