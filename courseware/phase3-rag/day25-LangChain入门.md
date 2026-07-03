# Day 25: LangChain 入门

> **培训阶段**: 第三阶段 RAG 应用开发 | **第 5 周** | **学习时长**: 约 6-8 小时  
> **今日关键词**: LangChain、Model I/O、PromptTemplate、OutputParser、Chain 基础

---

## 📍 课程导航

### 上节回顾

**Day 24** 你完成了 FastAPI 后端开发与前后端联调，搭建了可对外提供服务的 Web API。你已经具备：
- RESTful API 设计与 FastAPI 路由编写能力
- 异步请求处理与 CORS 跨域配置
- 将大模型调用封装为 HTTP 接口的经验

今天开始 **第三阶段：RAG 应用开发**（Day 25-38）。RAG（Retrieval-Augmented Generation，检索增强生成）是大模型应用开发的核心技能之一，而 **LangChain** 是构建 RAG 系统最常用的 Python 框架。

### 本节学习目标

完成本日学习后，你将能够：

1. 理解 LangChain 的设计哲学与核心架构
2. 安装并配置 LangChain 开发环境
3. 使用 `ChatOpenAI` 对接 DeepSeek / 通义千问等 OpenAI 兼容 API
4. 掌握 `PromptTemplate` 与 `ChatPromptTemplate` 的用法
5. 使用 `StrOutputParser` 解析模型输出
6. 理解 Chain（链）的概念，搭建第一个简单问答链
7. 了解 LangChain 生态中的其他核心模块（为后续课程铺垫）

### 与后续课程的衔接

- **Day 26** 将深入学习 **LCEL（LangChain Expression Language）**——用管道符 `|` 组合组件的现代写法
- **Day 27** 将学习 **Memory 记忆机制**——让对话具备上下文记忆
- **Day 28-30** 将依次学习文档加载、向量数据库、完整 RAG 系统搭建
- 今天搭建的「Prompt → Model → Parser」三件套，是后续所有 LangChain 应用的基石

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：LangChain 全景与架构

#### 1.1 为什么需要 LangChain？

直接调用大模型 API 看似简单，但实际项目中很快会遇到痛点：

| 痛点 | 直接调 API | 使用 LangChain |
|------|-----------|----------------|
| Prompt 管理 | 字符串硬编码，难以复用 | `PromptTemplate` 模板化 |
| 多步流程 | 手动拼接，代码臃肿 | Chain 链式组合 |
| 文档检索 | 从零实现向量检索 | 内置 RAG 全套组件 |
| 对话记忆 | 手动维护 messages 列表 | Memory 模块开箱即用 |
| 工具调用 | 自行解析 function call | Agent 框架标准化 |
| 可观测性 | 无 | LangSmith 集成追踪 |

**LangChain 是什么？**

LangChain 是一个用于开发大语言模型应用的 **开源框架**，提供：
- 标准化的组件接口（Model、Prompt、Parser、Retriever 等）
- 可组合的链式调用（LCEL）
- 丰富的第三方集成（100+ 模型、50+ 向量库）
- 活跃的社区与文档

```
┌─────────────────────────────────────────────────────┐
│                   你的 RAG 应用                      │
├──────────┬──────────┬──────────┬──────────┬─────────┤
│  Prompt  │  Model   │  Parser  │ Retriever│  Memory │
│  模板    │  模型    │  解析器  │  检索器  │  记忆   │
├──────────┴──────────┴──────────┴──────────┴─────────┤
│              LangChain 核心抽象层                      │
├─────────────────────────────────────────────────────┤
│   DeepSeek API  │  Chroma  │  HuggingFace  │  ...   │
└─────────────────────────────────────────────────────┘
```

#### 1.2 LangChain 版本与生态

> ⚠️ **重要**：LangChain 在 2024 年进行了重大重构（v0.2 → v0.3），API 有较大变化。本课程使用 **LangChain 0.3.x** 版本。

**核心包结构**

| 包名 | 作用 | 安装命令 |
|------|------|----------|
| `langchain-core` | 核心抽象（Runnable、Prompt 等） | 随 langchain 安装 |
| `langchain` | 主包，链与高级功能 | `pip install langchain` |
| `langchain-openai` | OpenAI / 兼容 API 集成 | `pip install langchain-openai` |
| `langchain-community` | 社区集成（文档加载器等） | `pip install langchain-community` |
| `langchain-chroma` | Chroma 向量库集成 | `pip install langchain-chroma` |
| `langgraph` | 有状态 Agent 编排（Day 39+） | 后续安装 |

#### 1.3 环境搭建

**Step 1：创建项目目录**

```bash
cd ~/llm-course
mkdir -p day25-langchain
cd day25-langchain

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

**Step 2：安装依赖**

```bash
pip install langchain langchain-openai langchain-community python-dotenv -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**Step 3：配置 API Key**

创建 `.env` 文件：

```bash
# .env
# DeepSeek API（OpenAI 兼容格式）
OPENAI_API_KEY=sk-your-deepseek-api-key
OPENAI_API_BASE=https://api.deepseek.com/v1

# 或使用通义千问
# OPENAI_API_KEY=sk-your-qwen-api-key
# OPENAI_API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1
```

> 💡 **安全提示**：`.env` 文件包含密钥，务必加入 `.gitignore`，不要提交到 Git！

```bash
echo ".env" >> .gitignore
echo "venv/" >> .gitignore
```

**Step 4：验证安装**

```python
# day25/verify_install.py
import langchain
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

print(f"LangChain 版本: {langchain.__version__}")

llm = ChatOpenAI(model="deepseek-chat", temperature=0)
response = llm.invoke("用一句话介绍 LangChain")
print(f"模型回复: {response.content}")
```

```bash
python3 verify_install.py
# 期望输出:
# LangChain 版本: 0.3.x
# 模型回复: LangChain 是一个用于开发大语言模型应用的开源框架...
```

---

### 9:45 - 10:30 | 模块二：Model I/O 三大件

LangChain 的 Model I/O 模块包含三个核心组件，构成最基本的 LLM 调用链路：

```
PromptTemplate  →  ChatOpenAI  →  StrOutputParser
   (输入格式化)      (模型调用)       (输出解析)
```

#### 2.1 ChatOpenAI：统一模型接口

```python
# day25/01_chat_model.py
"""ChatOpenAI 基础用法"""
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# 创建模型实例
llm = ChatOpenAI(
    model="deepseek-chat",      # 模型名称
    temperature=0.7,            # 创造性：0=确定性，1=创造性
    max_tokens=1024,            # 最大输出 token 数
    timeout=30,                 # 超时秒数
)

# 方式一：invoke 单条消息
response = llm.invoke("什么是 RAG？")
print("=== invoke 单条 ===")
print(response.content)

# 方式二：invoke 消息列表（多轮对话格式）
from langchain_core.messages import HumanMessage, SystemMessage

messages = [
    SystemMessage(content="你是一个专业的 AI 技术讲师，回答简洁准确。"),
    HumanMessage(content="用三句话解释什么是向量数据库。"),
]
response = llm.invoke(messages)
print("\n=== invoke 消息列表 ===")
print(response.content)

# 方式三：batch 批量调用
responses = llm.batch([
    "Python 的优点是什么？",
    "JavaScript 的优点是什么？",
])
print("\n=== batch 批量 ===")
for i, resp in enumerate(responses):
    print(f"Q{i+1}: {resp.content[:50]}...")
```

**常用参数说明**

| 参数 | 类型 | 说明 | 推荐值 |
|------|------|------|--------|
| `model` | str | 模型名称 | `deepseek-chat` / `qwen-plus` |
| `temperature` | float | 随机性，0-2 | RAG 场景用 0-0.3 |
| `max_tokens` | int | 最大输出长度 | 512-2048 |
| `streaming` | bool | 是否流式输出 | 聊天界面用 True |

#### 2.2 PromptTemplate：提示词模板

硬编码 Prompt 是初学者最常犯的错误。`PromptTemplate` 让你将 Prompt 参数化：

```python
# day25/02_prompt_template.py
"""PromptTemplate 基础与进阶"""
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)

# ===== 基础 PromptTemplate =====
basic_template = PromptTemplate(
    input_variables=["product", "audience"],
    template="请为{product}写一段面向{audience}的产品介绍，100字以内。",
)

prompt = basic_template.format(product="智能手表", audience="运动爱好者")
print("=== 基础模板 ===")
print(prompt)

# ===== ChatPromptTemplate（推荐） =====
chat_template = ChatPromptTemplate.from_messages([
    ("system", "你是{role}，请用{style}的风格回答问题。"),
    ("human", "{question}"),
])

messages = chat_template.format_messages(
    role="资深 Python 工程师",
    style="通俗易懂",
    question="什么是装饰器？",
)
print("\n=== Chat 模板 ===")
for msg in messages:
    print(f"[{msg.type}] {msg.content}")

# ===== 带对话历史的模板 =====
conversation_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个有帮助的 AI 助手。"),
    MessagesPlaceholder(variable_name="chat_history"),  # 插入历史消息
    ("human", "{input}"),
])
print("\n=== 带历史占位符的模板 ===")
print(conversation_template.input_variables)
# 输出: ['chat_history', 'input']
```

**PromptTemplate 最佳实践**

| 实践 | 说明 | 示例 |
|------|------|------|
| 角色设定放 system | 稳定的行为约束 | `("system", "你是法律顾问...")` |
| 用户问题放 human | 动态输入 | `("human", "{question}")` |
| 历史用 MessagesPlaceholder | 多轮对话 | `MessagesPlaceholder("chat_history")` |
| 模板存文件 | 便于非技术人员修改 | `PromptTemplate.from_file("prompt.txt")` |

#### 2.3 OutputParser：输出解析器

模型返回的是 `AIMessage` 对象，OutputParser 将其转换为你需要的格式：

```python
# day25/03_output_parser.py
"""OutputParser 常用类型"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import (
    StrOutputParser,
    JsonOutputParser,
)
from langchain_core.pydantic_v1 import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", temperature=0)

# ===== StrOutputParser：最常用 =====
parser = StrOutputParser()

prompt = ChatPromptTemplate.from_messages([
    ("system", "简洁回答。"),
    ("human", "{question}"),
])

# 手动串联
chain = prompt | llm | parser
result = chain.invoke({"question": "LangChain 的核心价值是什么？"})
print("=== StrOutputParser ===")
print(type(result))  # <class 'str'>
print(result)

# ===== JsonOutputParser：结构化输出 =====
class MovieReview(BaseModel):
    title: str = Field(description="电影名称")
    rating: float = Field(description="评分 1-10")
    summary: str = Field(description="一句话评价")

json_parser = JsonOutputParser(pydantic_object=MovieReview)

json_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是影评人。{format_instructions}"),
    ("human", "评价电影《肖申克的救赎》"),
])

json_chain = json_prompt | llm | json_parser
review = json_chain.invoke({
    "format_instructions": json_parser.get_format_instructions(),
})
print("\n=== JsonOutputParser ===")
print(f"电影: {review['title']}")
print(f"评分: {review['rating']}")
print(f"评价: {review['summary']}")
```

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：Chain 链式调用入门

#### 3.1 什么是 Chain？

Chain（链）是 LangChain 的核心概念：将多个组件串联，形成完整的处理流水线。

```
用户输入 → [PromptTemplate] → [LLM] → [OutputParser] → 最终结果
```

在 LangChain 0.3 中，推荐使用 **LCEL 管道符** `|` 来构建链（Day 26 深入讲解），今天先掌握基本用法。

#### 3.2 第一个完整 Chain

```python
# day25/04_first_chain.py
"""第一个 LangChain 问答链"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

# 1. 定义组件
llm = ChatOpenAI(model="deepseek-chat", temperature=0.3)

prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一个专业的技术文档写作助手。
请根据用户提供的主题，生成结构清晰的技术文档大纲。
要求：
- 使用 Markdown 格式
- 包含 3-5 个主要章节
- 每个章节下列出 2-3 个子要点"""),
    ("human", "请为以下主题生成文档大纲：{topic}"),
])

parser = StrOutputParser()

# 2. 用 LCEL 管道符组合（预告 Day 26）
chain = prompt | llm | parser

# 3. 调用
result = chain.invoke({"topic": "RAG 检索增强生成技术"})
print(result)
```

#### 3.3 流式输出

对于聊天应用，流式输出能显著提升用户体验：

```python
# day25/05_streaming.py
"""流式输出示例"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", temperature=0.7, streaming=True)
prompt = ChatPromptTemplate.from_messages([
    ("human", "用 200 字介绍 LangChain 的核心模块。"),
])
chain = prompt | llm | StrOutputParser()

print("=== 流式输出 ===")
for chunk in chain.stream({}):
    print(chunk, end="", flush=True)
print()  # 换行
```

#### 3.4 Runnable 接口预览

LangChain 中所有可组合组件都实现了 `Runnable` 接口，提供统一的方法：

| 方法 | 作用 | 使用场景 |
|------|------|----------|
| `invoke(input)` | 同步单次调用 | 普通问答 |
| `batch(inputs)` | 同步批量调用 | 批量处理 |
| `stream(input)` | 流式输出 | 聊天界面 |
| `ainvoke(input)` | 异步单次调用 | FastAPI 集成 |

```python
# day25/06_runnable_preview.py
"""Runnable 接口方法预览"""
import asyncio
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", temperature=0)
prompt = ChatPromptTemplate.from_template("用一句话解释：{concept}")
chain = prompt | llm | StrOutputParser()

# invoke
print("invoke:", chain.invoke({"concept": "Chain"}))

# batch
results = chain.batch([
    {"concept": "Prompt"},
    {"concept": "Parser"},
])
print("batch:", results)

# ainvoke（异步，FastAPI 中常用）
async def async_demo():
    result = await chain.ainvoke({"concept": "Runnable"})
    print("ainvoke:", result)

asyncio.run(async_demo())
```

---

## 🌆 下午课程（14:00 - 17:00）

### 14:00 - 15:30 | 模块四：LangChain 核心模块概览

#### 4.1 六大核心模块

```
LangChain 架构
├── Model I/O        ← 今天已学：Prompt、Model、Parser
├── Retrieval        ← Day 28-30：文档加载、向量检索、RAG
├── Memory           ← Day 27：对话记忆
├── Chains           ← Day 26：LCEL 表达式
├── Agents           ← Day 39+：工具调用与自主决策
└── Callbacks        ← 可观测性与调试
```

#### 4.2 Document Loaders 预览

```python
# day25/07_loaders_preview.py
"""文档加载器预览（Day 28 详学）"""
from langchain_community.document_loaders import TextLoader, PyPDFLoader

# 创建测试文件
with open("sample.txt", "w", encoding="utf-8") as f:
    f.write("LangChain 是一个强大的 LLM 应用开发框架。\n")
    f.write("它提供了文档加载、向量检索、链式调用等核心能力。\n")
    f.write("RAG 是检索增强生成的缩写，结合了检索与生成。")

# 加载文本文件
loader = TextLoader("sample.txt", encoding="utf-8")
documents = loader.load()

print(f"加载了 {len(documents)} 个文档")
print(f"文档内容:\n{documents[0].page_content}")
print(f"元数据: {documents[0].metadata}")
# 元数据: {'source': 'sample.txt'}
```

#### 4.3 综合实战：技术问答助手

```python
# day25/08_qa_assistant.py
"""综合实战：可配置的技术问答助手"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()


def create_qa_chain(role: str = "AI 技术专家", temperature: float = 0.3):
    """创建可配置的问答链"""
    llm = ChatOpenAI(model="deepseek-chat", temperature=temperature)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """你是{role}。
回答要求：
1. 准确、专业、有条理
2. 适当使用 Markdown 格式
3. 如果问题超出你的知识范围，诚实说明
4. 回答长度控制在 300 字以内"""),
        ("human", "{question}"),
    ])

    return prompt | llm | StrOutputParser()


def main():
    chain = create_qa_chain(role="RAG 技术专家")

    questions = [
        "什么是 LangChain？它解决了什么问题？",
        "RAG 和 Fine-tuning 有什么区别？各适合什么场景？",
        "向量数据库在 RAG 中扮演什么角色？",
    ]

    for q in questions:
        print(f"\n{'='*60}")
        print(f"❓ {q}")
        print(f"{'='*60}")
        answer = chain.invoke({"role": "RAG 技术专家", "question": q})
        print(answer)


if __name__ == "__main__":
    main()
```

---

### 15:30 - 15:45 | 课间休息

---

### 15:45 - 17:00 | 模块五：下午实操项目

#### 5.1 项目：多角色 Prompt 工厂

**需求**：创建一个「Prompt 工厂」，根据不同场景（客服、技术文档、代码审查）生成不同风格的回答。

```python
# day25/09_prompt_factory.py
"""下午实操：多角色 Prompt 工厂"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

# 预定义角色配置
ROLES = {
    "customer_service": {
        "role": "专业客服代表",
        "style": "亲切、耐心、以解决问题为导向",
        "constraints": "不使用技术术语，回答简洁明了",
    },
    "tech_writer": {
        "role": "技术文档工程师",
        "style": "严谨、结构化、使用 Markdown",
        "constraints": "包含代码示例时需标注语言，分步骤说明",
    },
    "code_reviewer": {
        "role": "资深代码审查员",
        "style": "直接、指出问题、给出改进建议",
        "constraints": "按严重程度分类问题：Critical / Warning / Info",
    },
}

PROMPT_TEMPLATE = ChatPromptTemplate.from_messages([
    ("system", """你是{role}。
回答风格：{style}
约束条件：{constraints}"""),
    ("human", "{question}"),
])


def create_role_chain(role_key: str):
    """根据角色 key 创建对应的链"""
    if role_key not in ROLES:
        raise ValueError(f"未知角色: {role_key}，可选: {list(ROLES.keys())}")

    config = ROLES[role_key]
    llm = ChatOpenAI(model="deepseek-chat", temperature=0.5)
    return PROMPT_TEMPLATE | llm | StrOutputParser(), config


def main():
    question = "用户反馈登录页面加载很慢，有时还会超时。"

    for role_key in ROLES:
        chain, config = create_role_chain(role_key)
        print(f"\n{'='*60}")
        print(f"🎭 角色: {config['role']}")
        print(f"{'='*60}")

        answer = chain.invoke({**config, "question": question})
        print(answer)


if __name__ == "__main__":
    main()
```

**运行与验证**

```bash
python3 09_prompt_factory.py
```

期望看到三种角色对同一问题的不同风格回答。

#### 5.2 项目结构规范

```
day25-langchain/
├── .env                    # API 密钥（不提交 Git）
├── .gitignore
├── requirements.txt
├── verify_install.py
├── 01_chat_model.py
├── 02_prompt_template.py
├── 03_output_parser.py
├── 04_first_chain.py
├── 05_streaming.py
├── 06_runnable_preview.py
├── 07_loaders_preview.py
├── 08_qa_assistant.py
└── 09_prompt_factory.py    # 下午项目
```

**requirements.txt**

```
langchain>=0.3.0
langchain-openai>=0.2.0
langchain-community>=0.3.0
python-dotenv>=1.0.0
```

---

## 🌙 晚自习（19:00 - 21:00）

### 19:00 - 20:00 | 自习与练习

1. **跑通所有示例代码**，确保每个文件无报错
2. **阅读 LangChain 官方文档** Model I/O 章节：https://python.langchain.com/docs/concepts/
3. **尝试切换模型**：将 `deepseek-chat` 改为通义千问 `qwen-plus`，观察输出差异
4. **扩展 Prompt 工厂**：新增「产品经理」和「数据分析师」两个角色

### 20:00 - 21:00 | 答疑与讨论

**讨论话题**：
- LangChain vs 直接调 API，什么场景下必须用框架？
- `temperature` 参数如何影响 RAG 场景的答案质量？
- 如何管理多个 Prompt 模板？（提示：可以用 YAML/JSON 配置文件）

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | LangChain 架构与生态 | |
| 2 | LangChain 0.3 环境安装与配置 | |
| 3 | ChatOpenAI 模型调用（invoke/batch/stream） | |
| 4 | PromptTemplate 与 ChatPromptTemplate | |
| 5 | MessagesPlaceholder 对话历史占位 | |
| 6 | StrOutputParser 与 JsonOutputParser | |
| 7 | LCEL 管道符 `\|` 基础链式组合 | |
| 8 | Runnable 接口（invoke/batch/stream/ainvoke） | |
| 9 | 流式输出实现 | |
| 10 | Document Loader 预览 | |
| 11 | 多角色 Prompt 工厂项目 | |

---

## 📝 课后作业

### 必做题

1. **环境搭建**：完成 LangChain 环境安装，运行 `verify_install.py` 截图
2. **Prompt 工厂扩展**：在下午项目基础上新增至少 2 个角色，提交到 GitHub
3. **自定义问答链**：创建一个「Python 学习导师」链，要求：
   - 使用 ChatPromptTemplate 设定导师角色
   - temperature 设为 0.5
   - 支持流式输出
   - 能回答 3 个不同难度的 Python 问题

### 选做题

4. **JsonOutputParser 实战**：设计一个「代码审查结果」的结构化输出，包含 `issues`（列表）、`score`（1-10）、`suggestion`（字符串）
5. **异步链**：用 `ainvoke` 实现并发调用 5 个不同问题，比较与串行 `invoke` 的耗时差异

---

## 💡 常见问题 FAQ

**Q1: `ModuleNotFoundError: No module named 'langchain_openai'`**

A: 需要单独安装集成包：
```bash
pip install langchain-openai
```

**Q2: API 调用报 `AuthenticationError`**

A: 检查 `.env` 文件：
- `OPENAI_API_KEY` 是否正确
- `OPENAI_API_BASE` 是否与 API Key 对应（DeepSeek / 通义千问地址不同）
- 确认 `load_dotenv()` 在代码开头被调用

**Q3: `prompt | llm | parser` 中的 `|` 是什么语法？**

A: 这是 LCEL（LangChain Expression Language）的管道操作符，类似 Unix 管道。Day 26 会系统讲解。今天先理解它表示「将前一个组件的输出传给后一个组件」。

**Q4: LangChain 0.1 的老教程代码跑不通怎么办？**

A: LangChain 在 0.2/0.3 版本做了大量 API 变更：
- `from langchain.chat_models import ChatOpenAI` → `from langchain_openai import ChatOpenAI`
- `LLMChain` 已废弃 → 使用 LCEL `prompt | llm | parser`
- 本课程所有代码基于 0.3.x，请以此为准

**Q5: 如何选择 temperature 值？**

A:
| 场景 | 推荐 temperature |
|------|-----------------|
| RAG 问答（要求准确） | 0 - 0.3 |
| 创意写作 | 0.7 - 1.0 |
| 代码生成 | 0 - 0.2 |
| 头脑风暴 | 0.8 - 1.2 |

---

## 🔮 明日预习

**Day 26: LCEL 表达式与链**

明天你将深入学习 LangChain 的核心语法 LCEL：

- `Runnable` 接口完整方法族（invoke / batch / stream / ainvoke）
- 管道符 `|` 的组合规则与类型推断
- `RunnableParallel` 并行执行
- `RunnablePassthrough` 与 `RunnableLambda` 自定义逻辑
- `RunnableWithMessageHistory` 注入对话历史
- 条件分支 `RunnableBranch`
- 实战：构建多步骤文档处理流水线

**预习建议**：回顾今天的 `prompt | llm | parser` 写法，思考如果要加入「查询改写」步骤，链会变长什么样？

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 25*
