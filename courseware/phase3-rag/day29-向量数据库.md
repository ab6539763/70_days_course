# Day 29: 向量数据库

> **培训阶段**: 第三阶段 RAG 应用开发 | **第 5 周 | **学习时长**: 约 6-8 小时  
> **今日关键词**: Embedding、Chroma、Milvus、相似度搜索、元数据过滤

---

## 📍 课程导航

### 上节回顾

**Day 28** 你完成了文档加载与分割：
- 多种 Document Loader 加载不同格式
- `RecursiveCharacterTextSplitter` 分割策略
- `chunk_size` / `chunk_overlap` 参数调优
- 企业文档批量处理流水线

今天进入 RAG 的 **存储与检索** 核心——向量数据库。分割后的文本 chunks 将通过 Embedding 模型转为向量，存入向量数据库，供后续语义检索使用。

### 本节学习目标

完成本日学习后，你将能够：

1. 理解 Embedding 向量的原理与作用
2. 使用 `OpenAIEmbeddings` 生成文本向量
3. 使用 Chroma 搭建本地向量库并完成 CRUD
4. 了解 Milvus 生产级向量库的基本操作
5. 实现相似度搜索与元数据过滤
6. 对比不同距离度量（余弦、欧氏、内积）
7. 将 Day 28 的文档 chunks 完整嵌入并入库

### 与后续课程的衔接

- **Day 30** 将向量库与 LLM 串联，搭建完整 RAG 系统
- **Day 33** 混合检索（BM25 + 向量）会操作同一个向量库
- **Day 36-37** 企业知识库项目使用 Milvus 作为生产向量库

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：Embedding 嵌入原理

#### 1.1 什么是 Embedding？

Embedding 将文本映射到高维向量空间，**语义相近的文本，向量距离更近**。

```
"猫是一种宠物"     → [0.12, -0.34, 0.56, ...]  (1536维)
"狗是人类的朋友"   → [0.15, -0.31, 0.52, ...]  ← 距离较近
"今天天气很好"     → [-0.45, 0.78, -0.12, ...] ← 距离较远
```

```python
# day29/01_embedding_basics.py
"""Embedding 基础"""
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import numpy as np

load_dotenv()

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",  # 1536 维，性价比高
    # model="text-embedding-3-large",  # 3072 维，精度更高
)

# 单条嵌入
vector = embeddings.embed_query("LangChain 是一个 LLM 应用框架")
print(f"向量维度: {len(vector)}")
print(f"前 5 维: {vector[:5]}")

# 批量嵌入
texts = ["向量数据库", "关系型数据库", "大语言模型"]
vectors = embeddings.embed_documents(texts)
print(f"\n批量嵌入: {len(vectors)} 个向量")

# 计算相似度（余弦相似度）
def cosine_similarity(v1, v2):
    v1, v2 = np.array(v1), np.array(v2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

sim_01 = cosine_similarity(vectors[0], vectors[1])
sim_02 = cosine_similarity(vectors[0], vectors[2])
print(f"\n'向量数据库' vs '关系型数据库': {sim_01:.4f}")
print(f"'向量数据库' vs '大语言模型': {sim_02:.4f}")
```

**常用 Embedding 模型**

| 模型 | 维度 | 提供商 | 特点 |
|------|------|--------|------|
| `text-embedding-3-small` | 1536 | OpenAI | 性价比高，本课程主力 |
| `text-embedding-3-large` | 3072 | OpenAI | 精度更高，成本 2 倍 |
| `text-embedding-v3` | 1024 | 通义千问 | 中文优秀 |
| `bge-large-zh-v1.5` | 1024 | BAAI | 开源中文最佳 |

#### 1.2 距离度量方式

| 度量 | 公式特点 | 适用场景 |
|------|----------|----------|
| 余弦相似度 (Cosine) | 衡量方向，忽略长度 | 文本语义搜索（最常用） |
| 欧氏距离 (L2) | 衡量绝对距离 | 图像、坐标数据 |
| 内积 (IP) | 向量已归一化时等价余弦 | 特定优化场景 |

---

### 9:45 - 10:30 | 模块二：Chroma 向量数据库

#### 2.1 Chroma 入门

Chroma 是最适合学习和原型开发的向量数据库——纯 Python、零配置、支持持久化。

```bash
pip install langchain-chroma chromadb -i https://pypi.tuna.tsinghua.edu.cn/simple
```

```python
# day29/02_chroma_basics.py
"""Chroma 基础操作"""
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# 创建向量库（内存模式）
docs = [
    Document(page_content="LangChain 是 LLM 应用开发框架", metadata={"category": "framework"}),
    Document(page_content="Chroma 是轻量级向量数据库", metadata={"category": "database"}),
    Document(page_content="RAG 结合检索与生成技术", metadata={"category": "technique"}),
    Document(page_content="Milvus 是生产级向量数据库", metadata={"category": "database"}),
    Document(page_content="Embedding 将文本转为向量", metadata={"category": "technique"}),
]

vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    collection_name="rag_tutorial",
)

# 相似度搜索
results = vectorstore.similarity_search("什么是向量数据库？", k=3)
print("=== 相似度搜索 ===")
for doc in results:
    print(f"  [{doc.metadata['category']}] {doc.page_content}")

# 带分数的搜索
results_with_scores = vectorstore.similarity_search_with_score("向量数据库有哪些？", k=3)
print("\n=== 带分数搜索 ===")
for doc, score in results_with_scores:
    print(f"  分数: {score:.4f} | {doc.page_content}")
```

#### 2.2 Chroma 持久化与 CRUD

```python
# day29/03_chroma_persistence.py
"""Chroma 持久化与 CRUD"""
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# 持久化存储
vectorstore = Chroma(
    collection_name="enterprise_kb",
    embedding_function=embeddings,
    persist_directory="./chroma_db",  # 数据持久化到磁盘
)

# 添加文档
new_docs = [
    Document(page_content="公司成立于 2020 年", metadata={"dept": "hr"}),
    Document(page_content="2024 年营收增长 50%", metadata={"dept": "finance"}),
]
vectorstore.add_documents(new_docs)
print(f"文档总数: {vectorstore._collection.count()}")

# 元数据过滤搜索
filtered_results = vectorstore.similarity_search(
    "公司信息",
    k=2,
    filter={"dept": "hr"},  # 只搜索 hr 部门文档
)
print("\n=== 元数据过滤 ===")
for doc in filtered_results:
    print(f"  [{doc.metadata}] {doc.page_content}")

# 删除（通过 ID）
# vectorstore.delete(ids=["id1", "id2"])

# 重新加载已有数据库
vectorstore2 = Chroma(
    collection_name="enterprise_kb",
    embedding_function=embeddings,
    persist_directory="./chroma_db",
)
print(f"\n重新加载: {vectorstore2._collection.count()} 个文档")
```

#### 2.3 Retriever 接口

```python
# day29/04_retriever.py
"""VectorStore → Retriever"""
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma(
    collection_name="enterprise_kb",
    embedding_function=embeddings,
    persist_directory="./chroma_db",
)

# 转为 Retriever（LCEL 链中使用）
retriever = vectorstore.as_retriever(
    search_type="similarity",       # 搜索类型
    search_kwargs={"k": 3},         # 返回 top-3
)

docs = retriever.invoke("公司营收情况")
print("=== Retriever 检索 ===")
for doc in docs:
    print(f"  {doc.page_content}")

# MMR 搜索：最大边际相关性（减少结果冗余）
mmr_retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 3, "fetch_k": 10, "lambda_mult": 0.5},
)
```

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：Milvus 生产级向量库

#### 3.1 Milvus 简介

| 对比项 | Chroma | Milvus |
|--------|--------|--------|
| 定位 | 开发/原型 | 生产级 |
| 部署 | 嵌入式/本地 | 独立服务/Docker |
| 数据规模 | 百万级 | 十亿级 |
| 性能 | 中等 | 高性能 |
| 运维 | 零运维 | 需要运维 |

#### 3.2 Milvus Lite（本地开发）

```bash
pip install pymilvus langchain-milvus -i https://pypi.tuna.tsinghua.edu.cn/simple
```

```python
# day29/05_milvus_lite.py
"""Milvus Lite 本地开发"""
from langchain_milvus import Milvus
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

docs = [
    Document(page_content="员工年假 10 天", metadata={"type": "policy"}),
    Document(page_content="报销需部门经理审批", metadata={"type": "policy"}),
    Document(page_content="技术部使用 Python 和 Go", metadata={"type": "tech"}),
    Document(page_content="产品部负责需求管理", metadata={"type": "org"}),
]

# Milvus Lite 模式（无需 Docker）
vectorstore = Milvus.from_documents(
    documents=docs,
    embedding=embeddings,
    connection_args={"uri": "./milvus_demo.db"},  # 本地文件
    collection_name="company_kb",
)

results = vectorstore.similarity_search("请假制度", k=2)
print("=== Milvus 搜索 ===")
for doc in results:
    print(f"  [{doc.metadata}] {doc.page_content}")

# 元数据过滤
filtered = vectorstore.similarity_search(
    "公司政策", k=2, expr='type == "policy"'
)
print("\n=== Milvus 过滤 ===")
for doc in filtered:
    print(f"  {doc.page_content}")
```

#### 3.3 Milvus Docker 部署（了解）

```bash
# 生产环境使用 Docker 部署 Milvus Standalone
# docker compose up -d

# 连接配置
connection_args = {
    "uri": "http://localhost:19530",
}
```

---

## 🌆 下午课程（14:00 - 17:00）

### 14:00 - 15:30 | 模块四：完整入库流水线

#### 4.1 Day 28 → Day 29 串联

```python
# day29/06_full_indexing_pipeline.py
"""完整入库流水线：加载 → 分割 → 嵌入 → 存储"""
import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()


def build_vectorstore(
    docs_directory: str,
    persist_directory: str = "./chroma_db",
    collection_name: str = "knowledge_base",
    chunk_size: int = 500,
    chunk_overlap: int = 100,
) -> Chroma:
    # 1. 加载文档
    loader = DirectoryLoader(
        docs_directory, glob="**/*.{txt,md}",
        loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"},
    )
    documents = loader.load()
    print(f"📂 加载 {len(documents)} 个文档")

    # 2. 分割
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap,
    )
    chunks = splitter.split_documents(documents)
    print(f"✂️ 分割为 {len(chunks)} 个 chunks")

    # 3. 嵌入 + 存储
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name=collection_name,
    )
    print(f"💾 存入向量库: {vectorstore._collection.count()} 条记录")
    return vectorstore


# 准备测试数据
os.makedirs("knowledge_base", exist_ok=True)
policies = {
    "考勤制度.txt": "上班时间 9:00-18:00，弹性 30 分钟。迟到 15 分钟内扣 50 元。",
    "年假制度.txt": "入职满 1 年享 10 天年假，满 3 年享 15 天，满 5 年享 20 天。",
    "报销制度.txt": "填写报销单→部门经理审批→财务审核→3 个工作日内打款。",
    "远程办公.txt": "每周最多 2 天远程，需提前在 OA 申请，技术部可额外增加 1 天。",
}
for filename, content in policies.items():
    with open(f"knowledge_base/{filename}", "w", encoding="utf-8") as f:
        f.write(content * 3)

vs = build_vectorstore("knowledge_base")

# 测试检索
queries = ["年假有多少天", "怎么报销", "可以远程办公吗"]
for q in queries:
    results = vs.similarity_search(q, k=1)
    print(f"\nQ: {q}")
    print(f"A: [{results[0].metadata['source']}] {results[0].page_content[:60]}...")
```

#### 4.2 增量更新策略

```python
# day29/07_incremental_update.py
"""向量库增量更新"""
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

def get_or_create_vectorstore(persist_dir="./chroma_db"):
    return Chroma(
        collection_name="knowledge_base",
        embedding_function=embeddings,
        persist_directory=persist_dir,
    )

def add_new_documents(vectorstore, new_docs: list[Document]):
    """增量添加新文档"""
    before = vectorstore._collection.count()
    ids = vectorstore.add_documents(new_docs)
    after = vectorstore._collection.count()
    print(f"新增 {after - before} 条记录，总计 {after} 条")
    return ids

vs = get_or_create_vectorstore()
new_doc = Document(
    page_content="2025 年新政策：增加带薪病假 5 天。",
    metadata={"source": "2025_policy.txt", "year": 2025},
)
add_new_documents(vs, [new_doc])
```

---

### 15:30 - 15:45 | 课间休息

---

### 15:45 - 17:00 | 模块五：下午实操——双库对比实验

```python
# day29/08_dual_vectorstore.py
"""下午实操：Chroma vs Milvus 对比实验"""
import time
from langchain_chroma import Chroma
from langchain_milvus import Milvus
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

test_docs = [
    Document(page_content=f"测试文档内容编号 {i}：关于 RAG 技术的第 {i} 个知识点。" * 5,
             metadata={"id": i, "topic": "rag"})
    for i in range(20)
]

query = "RAG 技术知识点"


def benchmark_vectorstore(name, vectorstore):
    # 写入
    start = time.time()
    vs = vectorstore.from_documents(test_docs, embeddings)
    write_time = time.time() - start

    # 搜索
    start = time.time()
    results = vs.similarity_search(query, k=5)
    search_time = time.time() - start

    print(f"\n=== {name} ===")
    print(f"  写入 20 文档: {write_time:.2f}s")
    print(f"  搜索 top-5: {search_time:.4f}s")
    print(f"  首条结果: {results[0].page_content[:50]}...")
    return vs


chroma_vs = benchmark_vectorstore("Chroma", Chroma)
milvus_vs = benchmark_vectorstore("Milvus Lite", Milvus)

print("\n📊 小结：开发阶段推荐 Chroma，生产环境推荐 Milvus")
```

---

## 🌙 晚自习（19:00 - 21:00）

### 19:00 - 20:00 | 自习与练习

1. 将 Day 28 作业中的 chunks 完整入库
2. 测试不同 `k` 值（1/3/5/10）对检索结果的影响
3. 尝试 MMR 搜索，对比与 similarity 搜索的差异

### 20:00 - 21:00 | 答疑与讨论

- Embedding 模型选错了会怎样？
- 向量库数据如何备份和迁移？

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | Embedding 原理与向量相似度 | |
| 2 | OpenAIEmbeddings 使用 | |
| 3 | Chroma 创建、搜索、持久化 | |
| 4 | 元数据过滤搜索 | |
| 5 | Retriever 接口与 MMR 搜索 | |
| 6 | Milvus Lite 本地开发 | |
| 7 | 完整入库流水线 | |
| 8 | 增量更新策略 | |
| 9 | Chroma vs Milvus 对比 | |

---

## 📝 课后作业

### 必做题

1. **完整入库**：将 Day 28 处理的企业文档 chunks 嵌入 Chroma 并持久化
2. **检索测试**：设计 5 个问题测试检索效果，记录 top-3 结果
3. **Git 提交**：`git commit -m "Day 29: 向量数据库"`

### 选做题

4. 用 Milvus Lite 重建同一知识库，对比搜索速度
5. 实现「文档去重」：入库前检查相似度 > 0.95 的重复 chunks

---

## 💡 常见问题 FAQ

**Q1: `text-embedding-3-small` 和 `large` 怎么选？**

A: 开发阶段用 `small`（便宜、够快）。生产环境如果检索精度不够再换 `large`。中文场景可考虑通义或 BGE 模型。

**Q2: Chroma 数据存在哪里？**

A: `persist_directory` 指定的目录，默认是 SQLite + 向量文件。可以直接复制目录备份。

**Q3: 搜索返回结果不相关怎么办？**

A: 排查顺序：
1. 检查 Embedding 模型是否合适
2. 调整 chunk_size（Day 28）
3. 增加 k 值或用 MMR
4. Day 32-33 的高级 RAG 技术

**Q4: 向量库能存多少数据？**

A: Chroma 百万级没问题。Milvus 十亿级。对于企业知识库（通常几千到几万 chunks），Chroma 完全够用。

**Q5: 需要为每个项目建一个 collection 吗？**

A: 推荐按业务域分 collection（如 `hr_policies`、`tech_docs`），便于独立管理和权限控制。

---

## 🔮 明日预习

**Day 30: 完整 RAG 系统搭建**

明天是所有组件的「大汇合」：

- 文档加载 → 分割 → 嵌入 → 存储 → 检索 → 生成
- LCEL 构建完整 RAG 链
- 流式 RAG 问答
- Gradio / FastAPI 封装为 Web 服务
- 实战：搭建可交互的企业知识库问答 Demo

**预习建议**：回顾 Day 25-29 所有代码，确保向量库中已有测试数据。

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 29*
