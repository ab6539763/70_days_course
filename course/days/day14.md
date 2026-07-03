# Day 14: 阶段考核 —— 项目一：命令行多轮对话 AI 助手

> **零基础大模型应用开发 70 天培训课程** | 第 14/70 天 | Python 编程基础


——————





## 完整项目代码（可直接运行）

### 文件: `day14_chat_assistant.py`

```python
"""Day 14: 命令行多轮对话 AI 助手 — 阶段项目一"""
import os, json, requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/v1/chat/completions"
HISTORY_DIR = Path("chat_histories")
HISTORY_DIR.mkdir(exist_ok=True)


class ChatAssistant:
    def __init__(self):
        self.messages = [
            {"role": "system", "content": "你是一个有帮助的 AI 助手。"}
        ]

    def chat(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        payload = {"model": "deepseek-chat", "messages": self.messages, "temperature": 0.7}
        resp = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        reply = resp.json()["choices"][0]["message"]["content"]
        self.messages.append({"role": "assistant", "content": reply})
        return reply

    def clear(self):
        self.messages = [self.messages[0]]

    def save(self, filename: str = None):
        if not filename:
            filename = f"chat_{datetime.now():%Y%m%d_%H%M%S}.json"
        path = HISTORY_DIR / filename
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.messages, f, ensure_ascii=False, indent=2)
        return path


def main():
    assistant = ChatAssistant()
    print("🤖 多轮对话 AI 助手")
    print("指令: /clear 清空 | /save 保存 | /exit 退出")

    while True:
        user_input = input("\n你: ").strip()
        if not user_input:
            continue
        if user_input == "/exit":
            break
        if user_input == "/clear":
            assistant.clear()
            print("✅ 对话已清空")
            continue
        if user_input == "/save":
            path = assistant.save()
            print(f"✅ 已保存到 {path}")
            continue
        try:
            reply = assistant.chat(user_input)
            print(f"AI: {reply}")
        except Exception as e:
            print(f"❌ 错误: {e}")


if __name__ == "__main__":
    main()
```

### 运行步骤

```bash
cd course/code/day14
pip install -r requirements.txt  # 如有依赖
python day14_chat_assistant.py
```


## 深度讲义

### 14.1 项目架构

```
day14_chat_assistant/
├── main.py              # 入口
├── assistant.py         # ChatAssistant 类
├── config.py            # 配置
├── .env                 # API Key（不提交）
├── .gitignore
├── requirements.txt
└── chat_histories/      # 对话历史
```

### 14.2 核心需求清单

| 功能 | 实现方式 | 对应知识点 |
|------|----------|-----------|
| 多轮对话 | messages 列表追加 | Day 4 列表 |
| 历史保存 | json.dump | Day 5 JSON |
| /clear 指令 | while + if | Day 3 流程控制 |
| /save 指令 | 文件写入 | Day 11 文件 |
| 异常处理 | try/except | Day 10 异常 |
| 代码组织 | 类 + 模块 | Day 8 OOP |

### 14.3 评分标准

- 功能完整 (40%)
- 代码规范 (20%)
- 异常处理 (20%)
- Git 提交 (10%)
- 文档 README (10%)


## 常见错误与避坑

- ⚠️ 只看不练 — 必须动手敲代码
- ⚠️ 跳过基础直接调 API — 每天知识环环相扣
- ⚠️ 不写注释 — 企业级代码必须可读

## 课堂练习

- 📝 复习 Day 13 的核心知识点
- 📝 完成今日实操项目并提交 Git
- 📝 用 3 句话总结今天学到了什么


## 课程衔接说明



### ⬅️ 昨日回顾

**Day 13** 学习了「进阶语法与异步入门」，今天的知识直接建立在昨天之上。

### 🔗 今日定位

第一阶段收官项目。能力将贯穿 Day 15-24 Prompt 与 Web 开发。

### ➡️ 明日预告

**Day 15** 将学习「大模型原理科普（无需数学基础）」，今天务必打牢基础。


### 今日时间安排

| 时段 | 内容 |
|------|------|
| 09:00-12:00 上午 | 项目需求讲解与架构设计 |
| 09:00-12:00 上午 | 多轮对话记忆(messages 列表)实现 |
| 14:00-17:30 下午 | 🛠️ 对话历史保存为 JSON |
| 14:00-17:30 下午 | 🛠️ 异常处理、支持指令(/clear、/save、/exit) |
| 14:00-17:30 下午 | 🛠️ 代码互评 + 讲师点评 |
| 19:00-21:00 晚自习 | 优化项目 README 并推送 GitHub |



## 一、今日学习目标



完成今天的学习后，你将能够:

- 项目需求讲解与架构设计
- 多轮对话记忆(messages 列表)实现

### 核心技能点

- **多轮对话**
- **JSON 持久化**
- **指令系统**
- **异常处理**

### 与课程主线的关系

今天是 **第 1 阶段（Python 编程基础）** 的第 14 天。

> 今日主题「阶段考核 —— 项目一：命令行多轮对话 AI 助手」是整条 70 天学习路径中的关键一环。请对照总路线图理解今天学什么、为什么学、后面哪里会用到。



## 二、理论精讲（纳米级拆解）


### 2.1 项目需求讲解与架构设计

#### 核心概念

**项目需求讲解与架构设计** 是今日学习的重要内容。

#### 为什么学？

在大模型应用开发中，这个知识点将在后续项目中直接用到:
- 与 Day 12 的知识形成递进
- 为 Day 17 的实操项目提供基础

#### 学习要点

1. 理解概念定义（用自己的话复述）
2. 跟着课件代码敲一遍（不要复制粘贴）
3. 完成课后练习巩固

#### 常见错误

- 只看不练 → 必须动手写代码
- 跳过基础 → 每天知识环环相扣，不要跳天

### 2.2 多轮对话记忆(messages 列表)实现

#### 核心概念

**多轮对话记忆(messages 列表)实现** 是今日学习的重要内容。

#### 为什么学？

在大模型应用开发中，这个知识点将在后续项目中直接用到:
- 与 Day 12 的知识形成递进
- 为 Day 17 的实操项目提供基础

#### 学习要点

1. 理解概念定义（用自己的话复述）
2. 跟着课件代码敲一遍（不要复制粘贴）
3. 完成课后练习巩固

#### 常见错误

- 只看不练 → 必须动手写代码
- 跳过基础 → 每天知识环环相扣，不要跳天

## 三、下午实操预告

今日下午核心项目: **命令行多轮对话 AI 助手**
- 对话历史保存为 JSON
- 异常处理、支持指令(/clear、/save、/exit)
- 代码互评 + 讲师点评



## 下午实操：项目实战



### 项目名称

**命令行多轮对话 AI 助手**

### 推荐项目目录结构（企业级标准）

```text
day14_project/
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
# 文件名: day14_main.py
# 主题: Day 14 — 命令行多轮对话 AI 助手
# ================================

"""
Day 14 实操项目入口。

学习要点:
1. 复习昨天所学
2. 完成今日「命令行多轮对话 AI 助手」核心功能
3. 添加必要注释，提交 Git
"""


def main():
    """主函数 — 按今日课纲逐步实现"""
    print("Day 14: 命令行多轮对话 AI 助手")
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
5. **提交**: `git add . && git commit -m "Day 14: 命令行多轮对话 AI 助手"`



## 知识小测




**Q1.** 请用自己的话解释「多轮对话」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 11-14 所学填写）
- 后续应用: 将在 Day 21 左右用到

</details>

**Q2.** 请用自己的话解释「JSON 持久化」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 11-14 所学填写）
- 后续应用: 将在 Day 21 左右用到

</details>

**Q3.** 请用自己的话解释「指令系统」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 11-14 所学填写）
- 后续应用: 将在 Day 21 左右用到

</details>

**Q4.** 请用自己的话解释「异常处理」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 11-14 所学填写）
- 后续应用: 将在 Day 21 左右用到

</details>


### 上机题

请不看课件，独立完成今日「实操项目」的核心功能。限时 60 分钟。



## 课后作业



### 必做

1. 完成今日实操项目「命令行多轮对话 AI 助手」
2. 提交代码到 GitHub（commit message: `Day 14: 命令行多轮对话 AI 助手`）
3. 在学习笔记中记录 3 个今天学到的新知识点

### 晚自习

- 优化项目 README 并推送 GitHub

### 选做

1. 阅读官方文档中与今日主题相关的章节
2. 尝试优化今日代码（更优雅的错误处理、更清晰的注释）


——————

**第 14/70 天 · 零基础大模型应用开发 70 天培训课程**

> 坚持每一天，70 天后你将成为一名合格的大模型应用开发者。
