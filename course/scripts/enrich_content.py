#!/usr/bin/env python3
"""
课件内容深度扩充器 — 为每天注入完整理论、代码、练习
参考 SVM/K-Means/PCA 课件纳米级粒度
"""

from __future__ import annotations

import re
from pathlib import Path

DAYS_DIR = Path(__file__).resolve().parent.parent / "days"
CODE_DIR = Path(__file__).resolve().parent.parent / "code"


def inject_after_day_header(content: str, injection: str) -> str:
    """在课程衔接说明之前注入内容"""
    marker = "## 课程衔接说明"
    if marker in content:
        return content.replace(marker, injection + "\n\n" + marker, 1)
    return injection + "\n" + content


# ═══════════════════════════════════════════════════════════════
# 完整项目代码库
# ═══════════════════════════════════════════════════════════════

FULL_CODES: dict[int, dict] = {
    2: {
        "filename": "day02_text_cleaner.py",
        "code": '''\
"""Day 2: 文本清洗小工具 — 去空格、统一大小写、敏感词替换"""
import re

SENSITIVE_WORDS = ["广告", "spam", "垃圾"]


def clean_whitespace(text: str) -> str:
    return re.sub(r"\\s+", " ", text).strip()


def normalize_case(text: str, mode: str = "lower") -> str:
    if mode == "lower":
        return text.lower()
    if mode == "upper":
        return text.upper()
    return text.title()


def replace_sensitive(text: str, replacement: str = "***") -> str:
    result = text
    for word in SENSITIVE_WORDS:
        result = result.replace(word, replacement)
    return result


def format_report(original: str, cleaned: str) -> str:
    return f"""原文 ({len(original)} 字符):
{original}

清洗后 ({len(cleaned)} 字符):
{cleaned}"""


def main():
    raw = input("请输入待清洗文本: ")
    step1 = clean_whitespace(raw)
    step2 = normalize_case(step1)
    step3 = replace_sensitive(step2)
    print(format_report(raw, step3))


if __name__ == "__main__":
    main()
''',
    },
    3: {
        "filename": "day03_guess_number.py",
        "code": '''\
"""Day 3: 猜数字游戏"""
import random

def guess_number_game():
    target = random.randint(1, 100)
    attempts = 0
    print("🎮 猜数字游戏！范围 1-100")

    while True:
        guess_str = input("请输入你的猜测: ")
        try:
            guess = int(guess_str)
        except ValueError:
            print("请输入有效整数！")
            continue

        attempts += 1
        if guess < target:
            print("太小了！")
        elif guess > target:
            print("太大了！")
        else:
            print(f"🎉 恭喜！用了 {attempts} 次猜对了！")
            break


def multiplication_table():
    for i in range(1, 10):
        row = "  ".join(f"{i}×{j}={i*j:2d}" for j in range(1, i + 1))
        print(row)


if __name__ == "__main__":
    guess_number_game()
''',
    },
    5: {
        "filename": "day05_json_parser.py",
        "code": '''\
"""Day 5: 解析模拟 API 返回的 JSON"""
import json

MOCK_API_RESPONSE = """
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "model": "deepseek-chat",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "你好！我是 AI 助手，有什么可以帮你的？"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 20,
    "total_tokens": 30
  }
}
"""


def parse_api_response(json_str: str) -> dict:
    data = json.loads(json_str)
    return {
        "model": data["model"],
        "reply": data["choices"][0]["message"]["content"],
        "role": data["choices"][0]["message"]["role"],
        "total_tokens": data["usage"]["total_tokens"],
    }


def main():
    result = parse_api_response(MOCK_API_RESPONSE)
    print("=" * 40)
    print(f"模型: {result['model']}")
    print(f"角色: {result['role']}")
    print(f"回复: {result['reply']}")
    print(f"Token 消耗: {result['total_tokens']}")
    print("=" * 40)


if __name__ == "__main__":
    main()
''',
    },
    12: {
        "filename": "day12_ai_chat.py",
        "code": '''\
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
        user_input = input("\\n你: ").strip()
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
''',
    },
    14: {
        "filename": "day14_chat_assistant.py",
        "code": '''\
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
        user_input = input("\\n你: ").strip()
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
''',
    },
    30: {
        "filename": "day30_rag_qa.py",
        "code": '''\
"""Day 30: 企业知识库问答系统（命令行版 RAG）"""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

SAMPLE_DOCS = [
    "公司年假政策：入职满一年享受5天年假，满三年享受10天年假。",
    "报销流程：填写报销单→部门经理审批→财务部审核→3个工作日内到账。",
    "远程办公规定：每周最多远程2天，需提前在OA系统申请。",
    "考勤制度：上班时间9:00，迟到15分钟以内扣半天年假。",
]


def build_rag_chain():
    splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
    chunks = splitter.create_documents(SAMPLE_DOCS)

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_base=os.getenv("OPENAI_API_BASE"),
    )
    vectorstore = Chroma.from_documents(chunks, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_base=os.getenv("OPENAI_API_BASE"),
    )

    template = """基于以下上下文回答问题。如果无法从上下文找到答案，请说"我不知道"。

上下文:
{context}

问题: {question}

回答（请标注引用来源）:"""

    prompt = ChatPromptTemplate.from_template(template)

    def format_docs(docs):
        return "\\n".join(f"- {d.page_content}" for d in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain


def main():
    print("📚 企业知识库问答系统")
    chain = build_rag_chain()
    while True:
        q = input("\\n请输入问题 (quit退出): ").strip()
        if q.lower() == "quit":
            break
        answer = chain.invoke(q)
        print(f"\\n回答: {answer}")


if __name__ == "__main__":
    main()
''',
    },
}


def build_enrichment(day: int) -> str:
    """为指定天生成扩充内容块"""
    parts = []

    # 全局路线图（每周第一天显示）
    if day in (1, 8, 15, 22, 25, 32, 39, 46, 51, 58):
        parts.append(_week_roadmap(day))

    # 详细知识点展开
    parts.append(_detailed_knowledge(day))

    # 完整代码（如果有）
    if day in FULL_CODES:
        fc = FULL_CODES[day]
        parts.append(f"""
## 完整项目代码（可直接运行）

### 文件: `{fc['filename']}`

```python
{fc['code'].strip()}
```

### 运行步骤

```bash
cd course/code/day{day:02d}
pip install -r requirements.txt  # 如有依赖
python {fc['filename']}
```
""")

    # 练习与常见错误
    parts.append(_exercises_and_pitfalls(day))

    return "\n".join(parts)


def _week_roadmap(day: int) -> str:
    roadmaps = {
        1: ("第 1 周", "Python 入门", "变量 → 字符串 → 流程控制 → 数据结构 → 函数", "命令行通讯录系统"),
        8: ("第 2 周", "Python 进阶", "OOP → 模块 → 文件 → API 调用 → 异步", "命令行多轮对话 AI 助手"),
        15: ("第 3 周", "大模型原理与 API", "Transformer → API 参数 → Prompt 基础 → CoT → Function Calling", "多工具 AI 助手"),
        22: ("第 4 周", "Web 开发基础", "HTML/JS → FastAPI → SSE 流式 → 数据库", "网页版 ChatGPT 克隆"),
        25: ("第 5 周", "LangChain 框架", "LangChain 入门 → LCEL → Memory → 文档分割 → 向量库", "企业知识库问答"),
        32: ("第 6 周", "RAG 进阶", "查询改写 → 混合检索 → Rerank → 评估 → LlamaIndex", "企业级知识库项目"),
        39: ("第 7 周", "Agent 基础", "ReAct → LangChain Agent → LangGraph → 多 Agent → MCP", "多 Agent 办公助手"),
        46: ("第 8 周", "Agent 进阶", "稳定性 → Text-to-SQL → 项目开发 → 答辩", "多 Agent 智能办公助手"),
        51: ("第 9 周", "微调与部署", "微调理论 → 数据集 → LLaMA-Factory → 部署 → Docker", "容器化部署"),
        58: ("第 10 周", "毕业设计", "选题 → 开发 → 答辩 → 就业冲刺", "毕业设计项目"),
    }
    if day not in roadmaps:
        return ""
    week, theme, path, project = roadmaps[day]
    return f"""
## 本周学习路线图

> **{week}: {theme}**

```
{path}
                    ↓
            周末项目: {project}
```

本周每一天环环相扣，请按顺序学习，不要跳天。
"""


def _detailed_knowledge(day: int) -> str:
    """按天返回详细知识点"""
    knowledge = KNOWLEDGE_DB.get(day, "")
    if knowledge:
        return f"\n## 深度讲义\n\n{knowledge}"
    return ""


def _exercises_and_pitfalls(day: int) -> str:
    pitfalls = PITFALLS_DB.get(day, [
        "只看不练 — 必须动手敲代码",
        "跳过基础直接调 API — 每天知识环环相扣",
        "不写注释 — 企业级代码必须可读",
    ])
    exercises = EXERCISE_DB.get(day, [
        f"复习 Day {max(1, day-1)} 的核心知识点",
        "完成今日实操项目并提交 Git",
        "用 3 句话总结今天学到了什么",
    ])

    p_md = "\n".join(f"- ⚠️ {p}" for p in pitfalls)
    e_md = "\n".join(f"- 📝 {e}" for e in exercises)

    return f"""
## 常见错误与避坑

{p_md}

## 课堂练习

{e_md}
"""


# ═══════════════════════════════════════════════════════════════
# 按天知识库（纳米级拆解）
# ═══════════════════════════════════════════════════════════════

KNOWLEDGE_DB: dict[int, str] = {}
EXERCISE_DB: dict[int, list[str]] = {}
PITFALLS_DB: dict[int, list[str]] = {}

# Day 2-7 Python 基础
KNOWLEDGE_DB[2] = """
### 2.1 运算符详解

#### 算术运算符

| 运算符 | 示例 | 结果 | 说明 |
|--------|------|------|------|
| `+` | `3 + 2` | `5` | 加法 |
| `-` | `5 - 2` | `3` | 减法 |
| `*` | `4 * 3` | `12` | 乘法 |
| `/` | `7 / 2` | `3.5` | 除法（结果是 float） |
| `//` | `7 // 2` | `3` | 整除 |
| `%` | `7 % 2` | `1` | 取余 |
| `**` | `2 ** 3` | `8` | 幂运算 |

#### 比较运算符

```python
print(3 > 2)    # True
print(3 == 3)   # True（判断相等用 ==，不是 =）
print(3 != 2)   # True
```

#### 逻辑运算符

```python
age = 20
has_id = True
can_enter = age >= 18 and has_id  # True
```

### 2.2 字符串纳米级拆解

#### 索引与切片

```python
text = "Hello, LLM!"
print(text[0])     # H（正向索引从 0 开始）
print(text[-1])    # !（负向索引从 -1 开始）
print(text[0:5])   # Hello（切片：[起始:结束)，结束不包含）
print(text[7:])    # LLM!
```

#### 常用方法

```python
"  hello  ".strip()          # "hello" — 去首尾空格
"a,b,c".split(",")           # ["a", "b", "c"]
"-".join(["a", "b"])         # "a-b"
"hello".replace("l", "L")    # "heLLo"
```

### 2.3 f-string — Prompt 模板的核心

```python
name = "张三"
role = "用户"
prompt = f"你好，我是{{role}}，我的名字是{{name}}。请回答我的问题。"
# 后续 Day 17 你将用 f-string 构建 Prompt 模板
```

> **前后衔接**: Day 1 学了变量 → 今天学字符串操作 → Day 17 用 f-string 写 Prompt 模板
"""

KNOWLEDGE_DB[3] = """
### 3.1 if/elif/else 条件判断

```python
score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 60:
    grade = "C"
else:
    grade = "D"
print(f"等级: {grade}")
```

### 3.2 循环

#### for 循环

```python
for i in range(5):       # 0, 1, 2, 3, 4
    print(i)

fruits = ["苹果", "香蕉", "橙子"]
for fruit in fruits:
    print(fruit)
```

#### while 循环

```python
count = 0
while count < 3:
    print(f"第 {count + 1} 次")
    count += 1
```

#### break 与 continue

- `break`: 立即退出循环
- `continue`: 跳过本次，进入下一次

### 3.3 简易菜单系统

```python
while True:
    print("\\n=== 菜单 ===")
    print("1. 查看")
    print("2. 添加")
    print("0. 退出")
    choice = input("请选择: ")
    if choice == "0":
        break
    elif choice == "1":
        print("查看功能")
    elif choice == "2":
        print("添加功能")
    else:
        print("无效选择")
```

> **前后衔接**: Day 14 多轮对话助手的 `/clear`、`/exit` 指令就是用 today 学的 while + if 实现的
"""

KNOWLEDGE_DB[4] = """
### 4.1 列表 list — 大模型开发最常用的数据结构

```python
# 创建
messages = []                          # 空列表
messages = ["你好", "再见"]             # 直接创建
messages = list(range(5))              # [0, 1, 2, 3, 4]

# 增删改查
messages.append("新消息")               # 尾部添加
messages.insert(0, "第一条")            # 指定位置插入
messages.remove("你好")                 # 按值删除
last = messages.pop()                  # 弹出最后一个
messages[0] = "修改后"                # 按索引修改

# 切片
print(messages[1:3])                   # 切片
print(len(messages))                   # 长度

# 排序
nums = [3, 1, 4, 1, 5]
nums.sort()                            # 原地排序
sorted_nums = sorted(nums)             # 返回新列表

# 列表推导式（Python 优雅语法）
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
```

> **关键联系**: Day 12 调用大模型 API 时，`messages` 就是一个列表:
> ```python
> messages = [
>     {"role": "system", "content": "你是助手"},
>     {"role": "user", "content": "你好"},
>     {"role": "assistant", "content": "你好！有什么可以帮你的？"},
>     {"role": "user", "content": "今天天气怎么样？"},
> ]
> ```

### 4.2 元组 tuple — 不可变的列表

```python
point = (3, 4)
# point[0] = 5  # ❌ 报错！元组不可修改
x, y = point  # 解包
```

### 4.3 集合 set — 去重利器

```python
tags = {"AI", "Python", "LLM", "AI"}  # 自动去重
print(tags)  # {"AI", "Python", "LLM"}
```
"""

KNOWLEDGE_DB[5] = """
### 5.1 字典 dict — API 交互的核心

```python
user = {
    "name": "张三",
    "age": 25,
    "skills": ["Python", "AI"],
    "address": {
        "city": "北京",
        "district": "海淀"
    }
}

# 访问
print(user["name"])           # 张三
print(user.get("email", "无")) # 安全访问，不存在返回默认值

# 修改
user["age"] = 26
user["email"] = "zhang@example.com"

# 遍历
for key, value in user.items():
    print(f"{key}: {value}")
```

### 5.2 JSON — 大模型世界的通用语言

**为什么 JSON 是重点？**

因为所有大模型 API 的请求和响应都是 JSON 格式。今天学不好 JSON，Day 12 调 API 就会卡住。

#### JSON 与 Python 的对应关系

| JSON | Python |
|------|--------|
| object `{}` | dict |
| array `[]` | list |
| string | str |
| number | int / float |
| true/false | True/False |
| null | None |

#### json 模块四个核心函数

```python
import json

# 1. dumps: Python 对象 → JSON 字符串
data = {"role": "user", "content": "你好"}
json_str = json.dumps(data, ensure_ascii=False)
# '{"role": "user", "content": "你好"}'

# 2. loads: JSON 字符串 → Python 对象
parsed = json.loads(json_str)

# 3. dump: Python 对象 → 写入 JSON 文件
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 4. load: 从 JSON 文件读取
with open("data.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
```

### 5.3 模拟 API 响应结构

```json
{
  "id": "chatcmpl-xxx",
  "model": "deepseek-chat",
  "choices": [{
    "message": {
      "role": "assistant",
      "content": "你好！"
    }
  }],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 5,
    "total_tokens": 15
  }
}
```

> **前后衔接**: 今天解析 JSON → Day 12 构造并解析真实 API 的 JSON
"""

# Continue for more days...
for d, content in {
    6: """
### 6.1 函数定义

```python
def greet(name: str, greeting: str = "你好") -> str:
    \"\"\"问候函数\"\"\"
    return f"{greeting}, {name}!"

# 位置参数
greet("张三")

# 关键字参数
greet(name="李四", greeting="Hello")

# *args: 接收任意数量的位置参数
def sum_all(*args):
    return sum(args)
sum_all(1, 2, 3, 4)  # 10

# **kwargs: 接收任意数量的关键字参数
def print_info(**kwargs):
    for k, v in kwargs.items():
        print(f"{k}: {v}")
```

### 6.2 lambda 匿名函数

```python
square = lambda x: x ** 2
print(square(5))  # 25

# 常用于排序
users = [{"name": "张三", "age": 25}, {"name": "李四", "age": 20}]
users.sort(key=lambda u: u["age"])
```

### 6.3 重构实战

把 Day 1-5 的小项目拆成函数:
- `collect_input()` → 收集用户输入
- `process_data()` → 处理数据
- `display_result()` → 展示结果
- `main()` → 主流程编排
""",
    7: """
### 7.1 第一周知识串讲

| Day | 主题 | 核心技能 | 后续应用 |
|-----|------|----------|----------|
| 1 | 变量与类型 | int/str/bool | 一切基础 |
| 2 | 字符串 | f-string | Prompt 模板 |
| 3 | 流程控制 | if/while/for | 菜单与指令 |
| 4 | 列表/元组/集合 | list 操作 | messages 列表 |
| 5 | 字典/JSON | json 模块 | API 交互 |
| 6 | 函数 | def/lambda | 代码组织 |

### 7.2 通讯录管理系统需求

功能清单:
1. 添加联系人（姓名、电话、邮箱）
2. 查看所有联系人
3. 搜索联系人（按姓名）
4. 删除联系人
5. 修改联系人
6. 数据持久化（JSON 文件）

### 7.3 参考架构

```python
import json
from pathlib import Path

class ContactBook:
    def __init__(self, filepath="contacts.json"):
        self.filepath = Path(filepath)
        self.contacts = self._load()

    def _load(self):
        if self.filepath.exists():
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def _save(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.contacts, f, ensure_ascii=False, indent=2)

    def add(self, name, phone, email=""):
        self.contacts.append({"name": name, "phone": phone, "email": email})
        self._save()

    def list_all(self):
        for i, c in enumerate(self.contacts):
            print(f"[{i}] {c['name']} - {c['phone']}")

    def delete(self, index):
        if 0 <= index < len(self.contacts):
            removed = self.contacts.pop(index)
            self._save()
            print(f"已删除: {removed['name']}")
```
""",
    8: """
### 8.1 类与对象

```python
class ChatMessage:
    \"\"\"对话消息类 — 为 Day 12/14 的对话系统做准备\"\"\"

    def __init__(self, role: str, content: str):
        self.role = role        # "system" / "user" / "assistant"
        self.content = content

    def to_dict(self) -> dict:
        return {"role": self.role, "content": self.content}

    @classmethod
    def from_dict(cls, data: dict) -> "ChatMessage":
        return cls(data["role"], data["content"])

    def __str__(self) -> str:
        return f"[{self.role}] {self.content[:50]}"

    def __repr__(self) -> str:
        return f"ChatMessage(role={self.role!r}, content={self.content[:30]!r}...)"
```

### 8.2 三种方法类型

| 类型 | 装饰器 | 第一个参数 | 用途 |
|------|--------|-----------|------|
| 实例方法 | 无 | self | 操作实例数据 |
| 类方法 | @classmethod | cls | 工厂方法、备选构造 |
| 静态方法 | @staticmethod | 无 | 工具函数 |

> **前后衔接**: ChatMessage 类将在 Day 14 项目中直接使用，Day 25 LangChain 有内置的 Message 类
""",
    12: """
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
""",
    15: """
### 15.1 NLP 发展简史

```
1950s  规则系统     →  if "天气" in text: return "查天气"
1990s  统计方法     →  贝叶斯、HMM
2013   Word2Vec    →  词向量
2017   Transformer →  注意力机制（革命！）
2018   GPT/BERT    →  预训练范式
2022   ChatGPT     →  大模型应用爆发
2024+  Agent/RAG   →  应用开发黄金期
```

### 15.2 Transformer 通俗理解

**类比**: 读一篇文章时，你会重点关注哪些词？

> "小明把**苹果**给了小红，**她**很开心。"

"她"指谁？你会根据上下文判断 → 这就是**注意力机制**。

Transformer 就是让模型自动学会"关注"输入中最重要的部分。

### 15.3 训练三阶段

| 阶段 | 名称 | 做什么 | 类比 |
|------|------|--------|------|
| 1 | 预训练 | 读海量文本，学语言 | 上大学学通识 |
| 2 | SFT | 学对话格式 | 岗前培训 |
| 3 | RLHF | 学人类偏好 | 客户反馈优化 |

### 15.4 Token 计算

```python
import tiktoken
enc = tiktoken.encoding_for_model("gpt-4")
text = "你好，世界！Hello, World!"
tokens = enc.encode(text)
print(f"Token 数: {len(tokens)}")  # 约 8-10 个
print(f"Tokens: {tokens}")
```

> 1 个中文字 ≈ 1-2 个 token
> 1 个英文单词 ≈ 1 个 token
> API 按 token 计费，所以要关注成本
""",
    17: """
### 17.1 Prompt 设计四要素

```
┌─────────────────────────────────┐
│  System: 你是一个专业的翻译官    │  ← 指令 + 角色
├─────────────────────────────────┤
│  背景: 这是一份医疗科普文章       │  ← 上下文
├─────────────────────────────────┤
│  输入: {user_text}              │  ← 用户输入
├─────────────────────────────────┤
│  输出: 请以 JSON 格式返回翻译结果  │  ← 输出格式
└─────────────────────────────────┘
```

### 17.2 Zero-shot / Few-shot / One-shot

```python
# Zero-shot: 不给示例，直接指令
prompt = "将以下文本分类为正面/负面: 这个产品太好用了"

# One-shot: 给一个示例
prompt = '''
示例: "太差了" → 负面
请分类: "这个产品太好用了" →
'''

# Few-shot: 给多个示例
prompt = '''
示例:
"太差了" → 负面
"非常满意" → 正面
"一般般" → 中性
请分类: "这个产品太好用了" →
'''
```

### 17.3 输出格式约束

```python
prompt = '''
请分析以下评论，以 JSON 格式返回:
{
  "sentiment": "正面/负面/中性",
  "confidence": 0.0-1.0,
  "keywords": ["关键词1", "关键词2"]
}

评论: {comment}
'''
```
""",
    19: """
### 19.1 Function Calling 完整流程

```
用户: "北京今天天气怎么样？"
  ↓
LLM 思考: 需要调用天气工具
  ↓
LLM 返回: tool_call {name: "get_weather", args: {city: "北京"}}
  ↓
你的代码: 执行 get_weather("北京") → "晴, 25°C"
  ↓
你的代码: 把结果发回 LLM
  ↓
LLM 生成: "北京今天天气晴朗，气温25度，适合出行！"
```

### 19.2 工具 Schema 定义

```python
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "获取指定城市的天气信息",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称，如'北京'"
                }
            },
            "required": ["city"]
        }
    }
}]
```

### 19.3 执行工具并回传

```python
def get_weather(city: str) -> str:
    # 实际项目中调用天气 API
    return f"{city}今天晴，25°C"

# 当 LLM 返回 tool_call 时:
tool_call = response.choices[0].message.tool_calls[0]
fn_name = tool_call.function.name
fn_args = json.loads(tool_call.function.arguments)
result = get_weather(**fn_args)

# 把结果发回 LLM
messages.append({"role": "tool", "content": result, "tool_call_id": tool_call.id})
```
""",
    30: """
### 30.1 RAG 完整链路图

```
┌──────────┐    ┌──────────┐    ┌──────────┐
│ 原始文档  │ →  │ 文本分割  │ →  │ 向量化    │
│ PDF/Word │    │ chunk    │    │ Embedding│
└──────────┘    └──────────┘    └────┬─────┘
                                     ↓
┌──────────┐    ┌──────────┐    ┌──────────┐
│ 生成回答  │ ←  │ LLM生成  │ ←  │ 向量检索  │
│ + 引用   │    │ + Prompt │    │ top_k    │
└──────────┘    └──────────┘    └──────────┘
                     ↑
              用户问题 → 向量化
```

### 30.2 RAG Prompt 模板

```python
RAG_PROMPT = \"\"\"
你是一个企业知识库助手。请基于以下检索到的上下文回答用户问题。

规则:
1. 只根据上下文回答，不要编造
2. 如果上下文不足以回答，说"我不知道"
3. 在回答末尾标注引用来源

上下文:
{context}

用户问题: {question}

回答:
\"\"\"
```

### 30.3 兜底策略

```python
def answer_with_fallback(question, retriever, llm, threshold=0.5):
    docs = retriever.get_relevant_documents(question)
    if not docs or docs[0].metadata.get("score", 1) < threshold:
        return "抱歉，我在知识库中没有找到相关信息。请尝试换个问法或联系人工客服。"
    # 正常 RAG 流程...
```
""",
    39: """
### 39.1 Agent 核心概念

**Agent = LLM + 工具 + 记忆 + 规划**

```
感知(Perceive) → 思考(Think) → 行动(Act) → 观察(Observe) → 循环
```

### 39.2 ReAct 范式

```
Question: 北京和上海的人口之和是多少？

Thought 1: 我需要分别查询北京和上海的人口
Action 1: search("北京人口")
Observation 1: 北京常住人口约2185万

Thought 2: 还需要上海的人口
Action 2: search("上海人口")
Observation 2: 上海常住人口约2487万

Thought 3: 现在可以计算了
Action 3: calculator("2185 + 2487")
Observation 3: 4672

Thought 4: 我可以给出最终答案了
Answer: 北京和上海的人口之和约为4672万
```

### 39.3 手写 ReAct Agent 核心循环

```python
def react_agent(question, llm, tools, max_steps=5):
    prompt = f"问题: {question}\\n"
    for step in range(max_steps):
        response = llm.generate(prompt)
        if "Answer:" in response:
            return response.split("Answer:")[-1].strip()
        if "Action:" in response:
            action = parse_action(response)
            observation = execute_tool(action, tools)
            prompt += f"\\nObservation: {observation}\\n"
    return "无法在限定步数内完成"
```
""",
    41: """
### 41.1 为什么需要 LangGraph？

LangChain Agent 的局限:
- 流程不透明（黑盒）
- 难以实现循环和条件分支
- 不支持中断和恢复
- 多 Agent 协作困难

LangGraph 用**图结构**解决这些问题:

```
        ┌─────────┐
        │  START  │
        └────┬────┘
             ↓
        ┌─────────┐
   ┌─── │  Agent  │ ←──┐
   │    └────┬────┘    │
   │         ↓         │
   │    需要工具？      │
   │    ┌────┴────┐    │
   │   Yes       No    │
   │    ↓         ↓    │
   │ ┌──────┐ ┌──────┐│
   │ │ Tool │ │ END  ││
   │ └──┬───┘ └──────┘│
   │    │              │
   └────┘              │
```

### 41.2 核心概念

| 概念 | 说明 | 类比 |
|------|------|------|
| State | 共享状态 | 黑板 |
| Node | 处理节点 | 工人 |
| Edge | 连接边 | 流水线 |
| Conditional Edge | 条件边 | 质检分流 |
"""
}.items():
    KNOWLEDGE_DB[d] = content


def enrich_all():
    """扩充所有天的课件"""
    for day in range(1, 71):
        md_path = DAYS_DIR / f"day{day:02d}.md"
        if not md_path.exists():
            continue
        content = md_path.read_text(encoding="utf-8")
        enrichment = build_enrichment(day)
        enriched = inject_after_day_header(content, enrichment)
        md_path.write_text(enriched, encoding="utf-8")

        # 写入完整代码文件
        if day in FULL_CODES:
            fc = FULL_CODES[day]
            code_dir = CODE_DIR / f"day{day:02d}"
            code_dir.mkdir(parents=True, exist_ok=True)
            (code_dir / fc["filename"]).write_text(fc["code"], encoding="utf-8")

    # 统计
    total_lines = sum(
        len((DAYS_DIR / f"day{d:02d}.md").read_text().splitlines())
        for d in range(1, 71)
    )
    total_chars = sum(
        len((DAYS_DIR / f"day{d:02d}.md").read_text())
        for d in range(1, 71)
    )
    print(f"✅ Enriched 70 days: {total_lines:,} lines, {total_chars:,} chars")


if __name__ == "__main__":
    enrich_all()
