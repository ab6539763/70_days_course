# Day 27: Memory 记忆机制

> **培训阶段**: 第三阶段 RAG 应用开发 | **第 5 周 | **学习时长**: 约 6-8 小时  
> **今日关键词**: Memory、ConversationBuffer、SummaryMemory、RunnableWithMessageHistory

---

## 📍 课程导航

### 上节回顾

**Day 26** 你系统学习了 LCEL 表达式语言：
- `Runnable` 接口完整方法族
- `RunnableParallel` 并行、`RunnablePassthrough` 状态累积
- `RunnableLambda` 自定义逻辑、`RunnableBranch` 条件分支
- 构建了多步骤文档处理流水线

今天解决一个关键问题：**大模型本身无状态，如何让对话具备上下文记忆？** 这就是 LangChain Memory 模块的使命。

### 本节学习目标

完成本日学习后，你将能够：

1. 理解大模型无状态特性及 Memory 的必要性
2. 使用 `ConversationBufferMemory` 保存完整对话历史
3. 使用 `ConversationBufferWindowMemory` 控制上下文窗口
4. 使用 `ConversationSummaryMemory` 压缩长对话
5. 使用 `RunnableWithMessageHistory` 为任意 LCEL 链注入记忆
6. 实现多种 Session 存储后端（内存、文件、Redis）
7. 构建带记忆的多轮技术问答助手

### 与后续课程的衔接

- **Day 30** 完整 RAG 系统中，Memory 与 Retriever 配合实现「记住用户 + 检索知识库」
- **Day 36-37** 企业级知识库问答系统需要会话管理与历史记录
- **Day 39+** Agent 中的 Memory 用于记住工具调用历史

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：为什么需要 Memory？

#### 1.1 大模型的无状态本质

```python
# 无 Memory 的对话——每次都是「第一次见面」
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", temperature=0)

# 第一轮
print(llm.invoke("我叫小明，今年 25 岁").content)
# 第二轮——模型不记得你叫什么！
print(llm.invoke("我叫什么名字？").content)
# 输出：我不知道你的名字...
```

**问题根源**：每次 `invoke` 都是独立的 API 调用，模型不会自动记住之前的对话。

**解决方案**：在每次调用时，将历史消息一并传入：

```python
from langchain_core.messages import HumanMessage, AIMessage

messages = [
    HumanMessage(content="我叫小明，今年 25 岁"),
    AIMessage(content="你好小明！很高兴认识你。"),
    HumanMessage(content="我叫什么名字？"),
]
print(llm.invoke(messages).content)
# 输出：你叫小明。
```

Memory 模块就是自动管理这个 `messages` 列表的工具。

#### 1.2 Memory 类型概览

| 类型 | 类名 | 策略 | 适用场景 |
|------|------|------|----------|
| 完整缓冲 | `ConversationBufferMemory` | 保存全部历史 | 短对话（<10 轮） |
| 滑动窗口 | `ConversationBufferWindowMemory` | 只保留最近 k 轮 | 中等长度对话 |
| 摘要记忆 | `ConversationSummaryMemory` | LLM 压缩历史为摘要 | 长对话（>20 轮） |
| 摘要缓冲 | `ConversationSummaryBufferMemory` | 近期完整 + 远期摘要 | 长短兼顾 |
| 实体记忆 | `ConversationEntityMemory` | 提取并记住实体信息 | 人物/地点追踪 |
| 向量记忆 | `VectorStoreRetrieverMemory` | 向量检索相关历史 | 超长对话 |

```
对话轮次增加 →
┌────────────────────────────────────────────────┐
│ Buffer:     [全部历史]           token 爆炸！   │
│ Window:     [最近 k 轮]          丢失远期信息   │
│ Summary:    [摘要]               丢失细节      │
│ Summary+Buffer: [摘要] + [最近k轮]  最佳平衡    │
└────────────────────────────────────────────────┘
```

---

### 9:45 - 10:30 | 模块二：基础 Memory 类型

#### 2.1 ConversationBufferMemory

```python
# day27/01_buffer_memory.py
"""ConversationBufferMemory 完整历史记忆"""
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", temperature=0)
memory = ConversationBufferMemory(return_messages=True)

# 手动管理 Memory
memory.save_context(
    {"input": "我叫小明，是一名 Python 开发工程师"},
    {"output": "你好小明！作为一名 Python 开发工程师，有什么我可以帮你的吗？"},
)
memory.save_context(
    {"input": "我正在学习 LangChain"},
    {"output": "LangChain 是构建 LLM 应用的强大框架，祝你学习顺利！"},
)

# 查看记忆内容
print("=== 记忆中的消息 ===")
history = memory.load_memory_variables({})
for msg in history["history"]:
    print(f"  [{msg.type}] {msg.content[:50]}...")

# 在 Prompt 中使用 Memory
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个友好的 AI 助手。"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])

chain = (
    RunnablePassthrough.assign(
        history=lambda x: memory.load_memory_variables(x)["history"]
    )
    | prompt
    | llm
    | StrOutputParser()
)

response = chain.invoke({"input": "我叫什么名字？我的职业是什么？"})
print(f"\n回答: {response}")

# 保存本轮对话
memory.save_context(
    {"input": "我叫什么名字？我的职业是什么？"},
    {"output": response},
)
```

#### 2.2 ConversationBufferWindowMemory

```python
# day27/02_window_memory.py
"""滑动窗口记忆：只保留最近 k 轮"""
from langchain.memory import ConversationBufferWindowMemory

memory = ConversationBufferWindowMemory(k=2, return_messages=True)

conversations = [
    ("你好", "你好！有什么可以帮你的？"),
    ("今天天气怎么样", "抱歉，我无法获取实时天气信息。"),
    ("我叫张三", "你好张三！很高兴认识你。"),
    ("我喜欢编程", "编程是很有创造力的活动！"),
    ("我叫什么名字？", None),  # 测试记忆
]

for user_input, ai_output in conversations:
    if ai_output is None:
        history = memory.load_memory_variables({})
        print(f"\n当前窗口内的历史（k=2，共 {len(history['history'])} 条消息）:")
        for msg in history["history"]:
            print(f"  [{msg.type}] {msg.content}")
        print("\n⚠️ 注意：「你好」和「天气」已被挤出窗口！")
        print("⚠️ 「我叫张三」仍在窗口内，模型应该能记住名字。")
    else:
        memory.save_context({"input": user_input}, {"output": ai_output})
```

#### 2.3 ConversationSummaryMemory

```python
# day27/03_summary_memory.py
"""摘要记忆：用 LLM 压缩历史"""
from langchain.memory import ConversationSummaryMemory
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", temperature=0)
memory = ConversationSummaryMemory(llm=llm, return_messages=True)

# 模拟长对话
dialogues = [
    ("我叫李华，在阿里巴巴做后端开发", "你好李华！阿里后端开发经验丰富。"),
    ("我主要负责订单系统", "订单系统是电商核心，涉及高并发和分布式事务。"),
    ("最近在学习 RAG 技术", "RAG 是很好的方向，结合你的后端经验会很有优势。"),
    ("我想用 LangChain 搭建一个知识库问答", "很好的项目！可以从文档加载和向量检索开始。"),
    ("公司用的是 Milvus 向量数据库", "Milvus 是生产级向量库，LangChain 有良好集成。"),
]

for user_input, ai_output in dialogues:
    memory.save_context({"input": user_input}, {"output": ai_output})

history = memory.load_memory_variables({})
print("=== 摘要记忆内容 ===")
for msg in history["history"]:
    print(f"[{msg.type}]")
    print(f"  {msg.content}")
    print()
```

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：RunnableWithMessageHistory

#### 3.1 现代 Memory 注入方式

LangChain 0.3 推荐使用 `RunnableWithMessageHistory` 为任意链注入记忆，而非旧的 `ConversationChain`。

```python
# day27/04_message_history.py
"""RunnableWithMessageHistory 标准用法"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from dotenv import load_dotenv

load_dotenv()

# Session 存储
store = {}

def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# 构建基础链
llm = ChatOpenAI(model="deepseek-chat", temperature=0.5)
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个友好的 AI 助手，能记住对话内容。"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])

chain = prompt | llm | StrOutputParser()

# 注入 Memory
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# 多轮对话
config = {"configurable": {"session_id": "user_001"}}

print("=== 第一轮 ===")
r1 = chain_with_history.invoke({"input": "我叫王芳，是产品经理"}, config=config)
print(f"AI: {r1}")

print("\n=== 第二轮 ===")
r2 = chain_with_history.invoke({"input": "我在做什么工作？"}, config=config)
print(f"AI: {r2}")

print("\n=== 第三轮 ===")
r3 = chain_with_history.invoke({"input": "我叫什么名字？"}, config=config)
print(f"AI: {r3}")

# 新 Session——没有历史
config2 = {"configurable": {"session_id": "user_002"}}
r4 = chain_with_history.invoke({"input": "我叫什么名字？"}, config=config2)
print(f"\n=== 新用户 ===")
print(f"AI: {r4}")
```

#### 3.2 Session 存储后端

```python
# day27/05_session_backends.py
"""多种 Session 存储后端"""
from langchain_community.chat_message_histories import (
    ChatMessageHistory,       # 内存（默认）
    FileChatMessageHistory,   # 文件
    # RedisChatMessageHistory,  # Redis（需安装 redis）
)
import os

# 1. 内存存储——开发测试用
memory_store = ChatMessageHistory()
memory_store.add_user_message("你好")
memory_store.add_ai_message("你好！")
print(f"内存存储: {len(memory_store.messages)} 条消息")

# 2. 文件存储——单机生产用
os.makedirs("chat_histories", exist_ok=True)
file_store = FileChatMessageHistory("chat_histories/session_001.json")
file_store.add_user_message("文件存储测试")
file_store.add_ai_message("消息已保存到文件")
print(f"文件存储: {file_store.file_path}")

# 3. 工厂函数模式（推荐）
def create_history_backend(backend_type: str, session_id: str):
    if backend_type == "memory":
        if session_id not in _memory_store:
            _memory_store[session_id] = ChatMessageHistory()
        return _memory_store[session_id]
    elif backend_type == "file":
        return FileChatMessageHistory(f"chat_histories/{session_id}.json")
    else:
        raise ValueError(f"不支持的后端: {backend_type}")

_memory_store = {}
```

---

## 🌆 下午课程（14:00 - 17:00）

### 14:00 - 15:30 | 模块四：Memory 策略选择与实践

#### 4.1 混合 Memory 策略

```python
# day27/06_hybrid_memory.py
"""混合策略：摘要 + 滑动窗口"""
from langchain.memory import ConversationSummaryBufferMemory
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", temperature=0)

# 当历史超过 max_token_limit 时，自动摘要旧消息
memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=200,  # 超过 200 token 触发摘要
    return_messages=True,
)

# 模拟对话
for i in range(8):
    memory.save_context(
        {"input": f"这是第 {i+1} 轮对话，讨论 RAG 技术的第 {i+1} 个方面"},
        {"output": f"第 {i+1} 方面的详细解答..."},
    )

history = memory.load_memory_variables({})
print(f"混合记忆消息数: {len(history['history'])}")
for msg in history["history"]:
    print(f"  [{msg.type}] {msg.content[:80]}...")
```

#### 4.2 Memory + RAG 预览

```python
# day27/07_memory_rag_preview.py
"""Memory + RAG 组合预览（Day 30 详学）"""
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_chroma import Chroma
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from dotenv import load_dotenv

load_dotenv()

# 简易知识库
docs = [
    "公司年假制度：入职满一年享受 10 天年假，满三年 15 天。",
    "报销流程：填写报销单 → 部门经理审批 → 财务部审核 → 打款。",
    "远程办公政策：每周最多 2 天远程，需提前在 OA 系统申请。",
]

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma.from_texts(docs, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

llm = ChatOpenAI(model="deepseek-chat", temperature=0)

def format_docs(docs):
    return "\n".join(doc.page_content for doc in docs)

# RAG + Memory 链
rag_prompt = ChatPromptTemplate.from_messages([
    ("system", "基于以下参考资料回答问题。如果资料中没有相关信息，请说明。\n\n参考资料：{context}"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])

def retrieve_and_answer(inputs):
    context = format_docs(retriever.invoke(inputs["input"]))
    return {**inputs, "context": context}

rag_chain = (
    RunnablePassthrough.assign(output=retrieve_and_answer)
    | rag_prompt
    | llm
    | StrOutputParser()
)

# 注入 Memory
store = {}
def get_history(session_id):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

chain_with_memory = RunnableWithMessageHistory(
    rag_chain, get_history,
    input_messages_key="input",
    history_messages_key="history",
)

config = {"configurable": {"session_id": "employee_001"}}

print(chain_with_memory.invoke({"input": "年假有多少天？"}, config=config))
print(chain_with_memory.invoke({"input": "报销需要什么流程？"}, config=config))
print(chain_with_memory.invoke({"input": "刚才问的年假问题，答案是什么？"}, config=config))
```

---

### 15:30 - 15:45 | 课间休息

---

### 15:45 - 17:00 | 模块五：下午实操——带记忆的技术问答助手

```python
# day27/08_memory_qa_assistant.py
"""下午实操：带记忆的多轮技术问答助手"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import FileChatMessageHistory
from dotenv import load_dotenv
import os

load_dotenv()

SYSTEM_PROMPT = """你是一位资深 AI 技术顾问，专门解答关于大模型应用开发的问题。

回答要求：
1. 准确、专业、有条理
2. 能联系之前对话的上下文
3. 适当使用 Markdown 格式
4. 如果用户提到之前讨论过的内容，要能正确引用

当前对话主题：{topic}"""

os.makedirs("sessions", exist_ok=True)

def get_session_history(session_id: str) -> FileChatMessageHistory:
    return FileChatMessageHistory(f"sessions/{session_id}.json")

class TechQAAssistant:
    def __init__(self):
        self.llm = ChatOpenAI(model="deepseek-chat", temperature=0.3)
        self.current_topic = "通用技术咨询"
        self._build_chain()

    def _build_chain(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
        ])
        base_chain = prompt | self.llm | StrOutputParser()
        self.chain = RunnableWithMessageHistory(
            base_chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="history",
        )

    def chat(self, message: str, session_id: str = "default") -> str:
        config = {"configurable": {"session_id": session_id}}
        response = self.chain.invoke(
            {"input": message, "topic": self.current_topic},
            config=config,
        )
        return response

    def set_topic(self, topic: str):
        self.current_topic = topic
        print(f"📌 对话主题已切换为: {topic}")


def interactive_demo():
    assistant = TechQAAssistant()
    session_id = "demo_session"
    assistant.set_topic("LangChain Memory 机制")

    demo_conversation = [
        "LangChain 有哪些 Memory 类型？",
        "它们各适合什么场景？",
        "如果对话超过 50 轮，推荐用哪种？",
        "刚才你提到的第一种 Memory 是什么？",  # 测试记忆
    ]

    for msg in demo_conversation:
        print(f"\n👤 用户: {msg}")
        response = assistant.chat(msg, session_id)
        print(f"🤖 助手: {response}")


if __name__ == "__main__":
    interactive_demo()
```

---

## 🌙 晚自习（19:00 - 21:00）

### 19:00 - 20:00 | 自习与练习

1. 跑通所有 Day 27 示例
2. 实现一个简单的命令行聊天程序，支持 `exit` 退出、`clear` 清空记忆
3. 对比 Buffer / Window / Summary 三种 Memory 在 10 轮对话后的 token 消耗

### 20:00 - 21:00 | 答疑与讨论

- Memory 中的历史消息会占用 context window，如何权衡？
- 生产环境中 Session 存储推荐用什么方案？

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | 大模型无状态特性与 Memory 必要性 | |
| 2 | ConversationBufferMemory | |
| 3 | ConversationBufferWindowMemory | |
| 4 | ConversationSummaryMemory | |
| 5 | ConversationSummaryBufferMemory | |
| 6 | RunnableWithMessageHistory | |
| 7 | Session 存储后端（内存/文件） | |
| 8 | Memory + RAG 组合预览 | |
| 9 | 带记忆的技术问答助手 | |

---

## 📝 课后作业

### 必做题

1. **命令行聊天程序**：实现支持多轮对话、记忆保持、清空记忆的 CLI 工具
2. **Memory 对比实验**：用 15 轮对话测试三种 Memory，记录最终 prompt 的 token 数
3. **Git 提交**：`git commit -m "Day 27: Memory 记忆机制"`

### 选做题

4. 实现「话题检测」：当用户切换话题时自动清空旧 Memory
5. 用 `FileChatMessageHistory` 实现会话持久化，重启程序后能恢复历史

---

## 💡 常见问题 FAQ

**Q1: Memory 和直接传 messages 列表有什么区别？**

A: 功能上等价，但 Memory 模块提供了自动管理（保存、加载、裁剪、摘要）的抽象，避免手动维护 messages 列表的繁琐和出错。

**Q2: 对话历史太长导致 token 超限怎么办？**

A: 按优先级尝试：
1. `ConversationBufferWindowMemory(k=5)` 只保留最近 5 轮
2. `ConversationSummaryBufferMemory` 摘要 + 近期完整
3. 在 Prompt 中明确告知模型「只关注最近对话」

**Q3: 多个用户如何隔离 Memory？**

A: 通过 `session_id` 隔离。每个用户/会话使用不同的 `session_id`，`get_session_history` 函数根据 id 返回独立的 `ChatMessageHistory`。

**Q4: `RunnableWithMessageHistory` 和旧的 `ConversationChain` 有什么区别？**

A: `ConversationChain` 已废弃。`RunnableWithMessageHistory` 是装饰器模式，可以为 **任意 LCEL 链** 注入 Memory，更灵活。

**Q5: 生产环境 Session 存储推荐？**

A: | 规模 | 推荐方案 |
|------|----------|
| 开发测试 | `ChatMessageHistory`（内存） |
| 小型应用 | `FileChatMessageHistory` |
| 中型应用 | `RedisChatMessageHistory` |
| 大型应用 | 数据库 + 定期归档 |

---

## 🔮 明日预习

**Day 28: 文档加载与分割**

明天进入 RAG 的核心环节——数据处理：

- `TextLoader`、`PyPDFLoader`、`WebBaseLoader` 等文档加载器
- `RecursiveCharacterTextSplitter` 递归字符分割
- `TokenTextSplitter` 按 token 分割
- 分割参数 `chunk_size` 和 `chunk_overlap` 的选择
- 实战：处理 PDF 企业文档并分割为 chunks

**预习建议**：准备 1-2 个 PDF 文件（如产品手册、技术文档），明天将用于实操。

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 27*
