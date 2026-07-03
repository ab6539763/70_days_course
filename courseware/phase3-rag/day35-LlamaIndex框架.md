# Day 35: LlamaIndex 框架

> **培训阶段**: 第三阶段 RAG 应用开发 | **第 7 周 | **学习时长**: 约 6-8 小时  
> **今日关键词**: LlamaIndex、Index、Query Engine、VectorStoreIndex、与 LangChain 对比

---

## 📍 课程导航

### 上节回顾

**Day 25-34** 你使用 LangChain 构建了完整的 RAG 技术栈：
- LangChain / LCEL / Memory 框架层
- 文档处理 / 向量库 / RAG 流水线
- 高级 RAG 技术（Query Rewriting、混合检索、Rerank）
- Ragas 评估框架

今天学习另一个主流 RAG 框架——**LlamaIndex**。两个框架各有所长，优秀工程师应两者兼修。

### 本节学习目标

完成本日学习后，你将能够：

1. 理解 LlamaIndex 的设计哲学与核心概念
2. 安装配置 LlamaIndex 开发环境
3. 使用 `VectorStoreIndex` 构建索引
4. 使用 `QueryEngine` 进行问答查询
5. 理解 LlamaIndex 的 Document / Node / Index 层次
6. 用 LlamaIndex 重建企业知识库问答系统
7. 对比 LangChain 与 LlamaIndex，做出框架选择

### 与后续课程的衔接

- **Day 36-37** 企业级项目可选择 LangChain 或 LlamaIndex
- **Day 39+** Agent 开发主要用 LangChain/LangGraph，但数据层可用 LlamaIndex
- 毕业设计可根据场景灵活选择框架

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：LlamaIndex 全景

#### 1.1 LlamaIndex vs LangChain

| 维度 | LangChain | LlamaIndex |
|------|-----------|------------|
| 核心定位 | 通用 LLM 应用框架 | 数据索引与 RAG 专精 |
| 优势场景 | Agent、Chain 编排、工具调用 | 数据索引、查询、RAG |
| 抽象层次 | Runnable / LCEL 管道 | Index / Query Engine |
| 学习曲线 | 较陡（组件多） | 较平缓（专注 RAG） |
| 社区生态 | 更大 | 专注 RAG 更深 |
| 本课程主力 | Day 25-50 主力框架 | 补充参考 |

```
LangChain 视角:  Prompt → LLM → Parser → Chain → Agent
LlamaIndex 视角: Data → Index → Query Engine → Response
```

#### 1.2 核心概念

```
Documents（原始文档）
    ↓ 分割
Nodes（节点/chunks）
    ↓ 嵌入 + 索引
Index（索引结构）
    ↓ 查询
Query Engine（查询引擎）
    ↓
Response（回答 + 来源）
```

| 概念 | 类比 LangChain | 说明 |
|------|----------------|------|
| Document | Document | 原始文档 |
| Node | Document (chunk) | 索引的最小单元 |
| Index | VectorStore | 索引结构 |
| Query Engine | RAG Chain | 查询 + 生成 |
| Chat Engine | RAG Chain + Memory | 多轮对话 |

#### 1.3 环境搭建

```bash
pip install llama-index llama-index-llms-openai llama-index-embeddings-openai \
    llama-index-vector-stores-chroma -i https://pypi.tuna.tsinghua.edu.cn/simple
```

```python
# day35/01_verify_install.py
"""验证 LlamaIndex 安装"""
import llama_index
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_API_BASE", "")

print(f"LlamaIndex 版本: {llama_index.__version__}")

llm = OpenAI(model="deepseek-chat", temperature=0)
response = llm.complete("用一句话介绍 LlamaIndex")
print(f"LLM 回复: {response}")
```

---

### 9:45 - 10:30 | 模块二：Document 与 Index

#### 2.1 加载文档

```python
# day35/02_documents.py
"""LlamaIndex 文档加载"""
from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_API_BASE", "")

Settings.llm = OpenAI(model="deepseek-chat", temperature=0)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

documents = [
    Document(text="员工年假制度：入职满一年享受 10 天年假，满三年 15 天。", metadata={"dept": "hr"}),
    Document(text="报销流程：填写报销单，经部门经理审批后提交财务部审核。", metadata={"dept": "finance"}),
    Document(text="远程办公政策：每周最多 2 天远程办公，需提前在 OA 申请。", metadata={"dept": "hr"}),
    Document(text="考勤制度：标准工时 9:00-18:00，迟到 15 分钟内扣 50 元。", metadata={"dept": "hr"}),
]

index = VectorStoreIndex.from_documents(documents)
print(f"索引创建完成，包含 {len(documents)} 个文档")
```

#### 2.2 从文件加载

```python
# day35/03_file_loading.py
"""从文件加载文档"""
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_API_BASE", "")

Settings.llm = OpenAI(model="deepseek-chat", temperature=0)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

os.makedirs("llama_docs", exist_ok=True)
with open("llama_docs/policy.txt", "w", encoding="utf-8") as f:
    f.write("公司成立于 2020 年，专注于 AI 技术研发。\n" * 3)
    f.write("目前有 200 名员工，分布在北京和上海。\n" * 3)

documents = SimpleDirectoryReader("llama_docs").load_data()
print(f"加载了 {len(documents)} 个文档")

index = VectorStoreIndex.from_documents(documents)
```

#### 2.3 自定义分割

```python
# day35/04_custom_splitting.py
"""自定义 Node 分割"""
from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_API_BASE", "")

Settings.llm = OpenAI(model="deepseek-chat", temperature=0)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

long_text = "RAG 技术指南。" * 100
documents = [Document(text=long_text)]

node_parser = SentenceSplitter(chunk_size=200, chunk_overlap=50)
nodes = node_parser.get_nodes_from_documents(documents)
print(f"分割为 {len(nodes)} 个 nodes")

index = VectorStoreIndex(nodes)
```

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：Query Engine 查询引擎

#### 3.1 基础查询

```python
# day35/05_query_engine.py
"""Query Engine 基础查询"""
from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_API_BASE", "")

Settings.llm = OpenAI(model="deepseek-chat", temperature=0)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

documents = [
    Document(text="员工年假制度：入职满一年享受 10 天年假，满三年 15 天。"),
    Document(text="报销流程：填写报销单，经部门经理审批后提交财务部。"),
    Document(text="远程办公政策：每周最多 2 天远程办公，需提前申请。"),
]

index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine(similarity_top_k=3)

questions = ["年假有多少天？", "报销流程是什么？", "能在家办公吗？"]
for q in questions:
    response = query_engine.query(q)
    print(f"\nQ: {q}")
    print(f"A: {response}")
    print(f"来源: {[node.metadata for node in response.source_nodes]}")
```

#### 3.2 流式查询

```python
# day35/06_streaming.py
"""流式查询"""
from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_API_BASE", "")

Settings.llm = OpenAI(model="deepseek-chat", temperature=0)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

documents = [Document(text="LangChain 和 LlamaIndex 是两大 RAG 框架。" * 10)]
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine(streaming=True)

response = query_engine.query("介绍 LlamaIndex")
print("流式输出: ", end="")
for text in response.response_gen:
    print(text, end="", flush=True)
print()
```

#### 3.3 Chat Engine 多轮对话

```python
# day35/07_chat_engine.py
"""Chat Engine 多轮对话"""
from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_API_BASE", "")

Settings.llm = OpenAI(model="deepseek-chat", temperature=0)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

documents = [
    Document(text="员工年假：满一年10天，满三年15天，满五年20天。"),
    Document(text="报销流程：填单→经理审批→财务审核→3个工作日打款。"),
]
index = VectorStoreIndex.from_documents(documents)
chat_engine = index.as_chat_engine(chat_mode="context", similarity_top_k=3)

print(chat_engine.chat("年假有多少天？"))
print(chat_engine.chat("那工作满三年呢？"))  # 有上下文记忆
```

---

## 🌆 下午课程（14:00 - 17:00）

### 14:00 - 15:30 | 模块四：LlamaIndex 高级特性

#### 4.1 持久化索引

```python
# day35/08_persistence.py
"""索引持久化"""
from llama_index.core import Document, VectorStoreIndex, StorageContext, load_index_from_storage, Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_API_BASE", "")

Settings.llm = OpenAI(model="deepseek-chat", temperature=0)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

PERSIST_DIR = "./llama_index_storage"

if not os.path.exists(PERSIST_DIR):
    documents = [Document(text="持久化测试文档内容。" * 5)]
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=PERSIST_DIR)
    print("索引已持久化")
else:
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)
    print("索引已加载")

query_engine = index.as_query_engine()
print(query_engine.query("文档内容是什么？"))
```

#### 4.2 自定义 Prompt

```python
# day35/09_custom_prompt.py
"""自定义 Query Engine Prompt"""
from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.core.prompts import PromptTemplate
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_API_BASE", "")

Settings.llm = OpenAI(model="deepseek-chat", temperature=0)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

documents = [
    Document(text="员工年假制度：入职满一年享受 10 天年假。"),
    Document(text="报销流程：填写报销单，经部门经理审批。"),
]
index = VectorStoreIndex.from_documents(documents)

qa_prompt = PromptTemplate(
    "你是企业知识库助手。基于以下资料回答问题。\n"
    "如果资料中没有相关信息，请说'无法回答'。\n\n"
    "资料：\n{context_str}\n\n"
    "问题：{query_str}\n"
    "回答："
)

query_engine = index.as_query_engine(
    text_qa_template=qa_prompt,
    similarity_top_k=3,
)

response = query_engine.query("年假制度是什么？")
print(response)
```

#### 4.3 与 Chroma 集成

```python
# day35/10_chroma_integration.py
"""LlamaIndex + Chroma 集成"""
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import Document, VectorStoreIndex, StorageContext, Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_API_BASE", "")

Settings.llm = OpenAI(model="deepseek-chat", temperature=0)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

db = chromadb.PersistentClient(path="./chroma_llama")
chroma_collection = db.get_or_create_collection("llama_kb")

vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

documents = [
    Document(text="LlamaIndex 可以使用 Chroma 作为向量存储后端。"),
    Document(text="Chroma 支持持久化和元数据过滤。"),
]

index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
query_engine = index.as_query_engine()
print(query_engine.query("LlamaIndex 用什么向量库？"))
```

---

### 15:30 - 15:45 | 课间休息

---

### 15:45 - 17:00 | 模块五：下午实操——LlamaIndex 知识库系统

```python
# day35/11_llamaindex_kb.py
"""下午实操：LlamaIndex 企业知识库"""
from llama_index.core import (
    SimpleDirectoryReader, VectorStoreIndex, Settings,
    StorageContext, load_index_from_storage,
)
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_API_BASE", "")

Settings.llm = OpenAI(model="deepseek-chat", temperature=0)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

PERSIST_DIR = "./llama_kb_storage"
DOCS_DIR = "knowledge_base"


class LlamaIndexKB:
    def __init__(self):
        self.index = None
        self.query_engine = None
        self.chat_engine = None

    def build_index(self):
        if os.path.exists(PERSIST_DIR):
            storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
            self.index = load_index_from_storage(storage_context)
            print("📂 加载已有索引")
        else:
            documents = SimpleDirectoryReader(DOCS_DIR).load_data()
            print(f"📂 加载 {len(documents)} 个文档")
            self.index = VectorStoreIndex.from_documents(documents)
            self.index.storage_context.persist(persist_dir=PERSIST_DIR)
            print("💾 索引已持久化")

        qa_prompt = PromptTemplate(
            "你是企业知识库助手。基于资料回答，无相关信息请说明。\n\n"
            "资料：\n{context_str}\n\n问题：{query_str}\n回答："
        )
        self.query_engine = self.index.as_query_engine(
            text_qa_template=qa_prompt, similarity_top_k=3,
        )
        self.chat_engine = self.index.as_chat_engine(
            chat_mode="context", similarity_top_k=3,
        )

    def ask(self, question: str) -> str:
        response = self.query_engine.query(question)
        return str(response)

    def chat(self, message: str) -> str:
        response = self.chat_engine.chat(message)
        return str(response)


def main():
    kb = LlamaIndexKB()
    kb.build_index()

    print("\n=== 单轮问答 ===")
    print(kb.ask("年假有多少天？"))

    print("\n=== 多轮对话 ===")
    print(kb.chat("报销流程是什么？"))
    print(kb.chat("需要多长时间？"))


if __name__ == "__main__":
    main()
```

#### 5.2 LangChain vs LlamaIndex 代码对比

| 功能 | LangChain | LlamaIndex |
|------|-----------|------------|
| 加载文档 | `DirectoryLoader` | `SimpleDirectoryReader` |
| 分割 | `RecursiveCharacterTextSplitter` | `SentenceSplitter` |
| 向量库 | `Chroma.from_documents()` | `VectorStoreIndex.from_documents()` |
| 问答 | `chain.invoke()` | `query_engine.query()` |
| 多轮 | `RunnableWithMessageHistory` | `chat_engine.chat()` |
| 代码量 | 较多（显式链） | 较少（高层抽象） |

---

## 🌙 晚自习（19:00 - 21:00）

### 19:00 - 20:00

1. 用 LlamaIndex 重建 Day 30 的知识库系统
2. 对比两个框架的开发体验和代码量
3. 阅读 LlamaIndex 官方文档 Getting Started

### 20:00 - 21:00

- 讨论：什么场景选 LangChain，什么场景选 LlamaIndex
- 两个框架能否混用？

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | LlamaIndex 核心概念 | |
| 2 | LlamaIndex 环境安装 | |
| 3 | Document / Node / Index | |
| 4 | VectorStoreIndex 构建 | |
| 5 | Query Engine 查询 | |
| 6 | Chat Engine 多轮对话 | |
| 7 | 索引持久化 | |
| 8 | 自定义 Prompt | |
| 9 | LlamaIndex + Chroma 集成 | |
| 10 | LangChain vs LlamaIndex 对比 | |

---

## 📝 课后作业

### 必做题

1. **LlamaIndex 知识库**：完成下午项目，能回答 5 个测试问题
2. **框架对比报告**：从代码量、易用性、功能丰富度三个维度对比
3. **Git 提交**：`git commit -m "Day 35: LlamaIndex 框架"`

### 选做题

4. 用 LlamaIndex 的 `SubQuestionQueryEngine` 实现多步推理
5. 探索 LlamaIndex 的 `Evaluation` 模块

---

## 💡 常见问题 FAQ

**Q1: 应该学 LangChain 还是 LlamaIndex？**

A: 都要学。LangChain 是主力（Agent/Chain），LlamaIndex 是 RAG 专精补充。企业项目中常混用。

**Q2: LlamaIndex 能做 Agent 吗？**

A: 可以但不如 LangChain/LangGraph 强大。推荐 LlamaIndex 做数据层，LangChain 做编排层。

**Q3: 两个框架的向量库数据能共享吗？**

A: 可以。都用 Chroma 作为后端，共享同一个 collection。

**Q4: LlamaIndex 的 Settings 是什么？**

A: 全局配置单例，设置默认 LLM 和 Embedding 模型，避免每次手动传入。

**Q5: Query Engine 和 Chat Engine 区别？**

A: Query Engine 单轮无状态；Chat Engine 自动管理对话历史，类似 LangChain 的 Memory。

---

## 🔮 明日预习

**Day 36: 阶段项目二（上）——企业级知识库问答系统 Day 1**

- 项目需求分析与技术选型
- 系统架构设计
- 后端 API 开发
- 文档管理与索引服务

**预习建议**：回顾 Day 24 FastAPI 和 Day 30 RAG 系统，明天将两者结合为生产级项目。

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 35*
