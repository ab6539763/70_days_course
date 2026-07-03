# Day 33: 高级 RAG 技术下

> **培训阶段**: 第三阶段 RAG 应用开发 | **第 6 周 | **学习时长**: 约 6-8 小时  
> **今日关键词**: 混合检索、BM25、Rerank、父文档检索、Ensemble Retriever

---

## 📍 课程导航

### 上节回顾

**Day 32** 你学习了查询增强技术：
- Query Rewriting 查询改写
- Multi-Query 多查询检索
- HyDE 假想文档嵌入

今天学习 **高级 RAG 技术（下）**——在检索结果层面进一步优化：混合检索提升召回率、Rerank 提升精确度、父文档检索解决 chunk 上下文不足。

### 本节学习目标

完成本日学习后，你将能够：

1. 理解稀疏检索（BM25）与稠密检索（向量）的互补性
2. 使用 `BM25Retriever` 实现关键词检索
3. 使用 `EnsembleRetriever` 融合 BM25 + 向量检索
4. 使用 Rerank 模型对检索结果重排序
5. 实现 Parent Document Retriever 父文档检索
6. 构建融合所有高级技术的完整 RAG 系统

### 与后续课程的衔接

- **Day 34** Ragas 评估将量化混合检索和 Rerank 的效果
- **Day 35** LlamaIndex 提供了类似功能的不同实现
- **Day 36-37** 企业项目将使用今天的全套高级技术

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：混合检索原理

#### 1.1 稀疏 vs 稠密检索

| 特性 | BM25（稀疏） | 向量（稠密） |
|------|-------------|-------------|
| 原理 | 关键词匹配 + TF-IDF | 语义向量相似度 |
| 擅长 | 精确关键词、专有名词 | 语义理解、同义词 |
| 弱点 | 不理解语义 | 可能漏掉关键词 |
| 示例 | "年假10天" 精确匹配 | "休假制度" ≈ "放假规定" |

```
用户问: "DNS 解析失败怎么办"
  BM25:  ✅ 精确匹配 "DNS" 关键词
  向量:  ✅ 语义匹配 "网络故障排查"
  混合:  ✅✅ 两者优势结合
```

#### 1.2 BM25 检索器

```bash
pip install rank-bm25 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

```python
# day33/01_bm25_retriever.py
"""BM25 关键词检索"""
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document

docs = [
    Document(page_content="员工年假制度：入职满一年享受 10 天年假，满三年 15 天。", metadata={"id": 1}),
    Document(page_content="报销流程：填写报销单，经部门经理审批后提交财务部。", metadata={"id": 2}),
    Document(page_content="远程办公政策：每周最多 2 天远程办公，需提前申请。", metadata={"id": 3}),
    Document(page_content="考勤制度：标准工时 9:00-18:00，迟到 15 分钟内扣 50 元。", metadata={"id": 4}),
    Document(page_content="DNS 服务器配置：主 DNS 8.8.8.8，备用 DNS 114.114.114.114。", metadata={"id": 5}),
]

bm25_retriever = BM25Retriever.from_documents(docs)
bm25_retriever.k = 2

queries = ["年假天数", "DNS 配置", "在家办公"]
for q in queries:
    results = bm25_retriever.invoke(q)
    print(f"\nQ: {q}")
    for doc in results:
        print(f"  [{doc.metadata['id']}] {doc.page_content[:50]}...")
```

---

### 9:45 - 10:30 | 模块二：Ensemble 混合检索

#### 2.1 融合 BM25 + 向量

```python
# day33/02_ensemble_retriever.py
"""Ensemble Retriever: BM25 + 向量混合检索"""
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

docs = [
    Document(page_content="员工年假制度：入职满一年享受 10 天年假，满三年 15 天。"),
    Document(page_content="报销流程：填写报销单，经部门经理审批后提交财务部。"),
    Document(page_content="远程办公政策：每周最多 2 天远程办公，需提前申请。"),
    Document(page_content="考勤制度：标准工时 9:00-18:00，迟到 15 分钟内扣 50 元。"),
    Document(page_content="技术培训：公司每年提供 2 次外部技术培训机会。"),
]

# BM25 检索器
bm25_retriever = BM25Retriever.from_documents(docs)
bm25_retriever.k = 3

# 向量检索器
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma.from_documents(docs, embeddings)
vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 混合检索器
ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.4, 0.6],  # BM25 40%, 向量 60%
)

query = "休假和报销政策"
print(f"=== 混合检索: {query} ===")

print("\n仅 BM25:")
for doc in bm25_retriever.invoke(query):
    print(f"  {doc.page_content[:50]}...")

print("\n仅向量:")
for doc in vector_retriever.invoke(query):
    print(f"  {doc.page_content[:50]}...")

print("\n混合 Ensemble:")
for doc in ensemble_retriever.invoke(query):
    print(f"  {doc.page_content[:50]}...")
```

#### 2.2 权重调优

| 场景 | BM25 权重 | 向量权重 | 原因 |
|------|-----------|----------|------|
| 技术文档（多专有名词） | 0.5 | 0.5 | 关键词重要 |
| 自然语言 FAQ | 0.3 | 0.7 | 语义理解重要 |
| 法律合同 | 0.6 | 0.4 | 精确匹配重要 |
| 通用企业知识库 | 0.4 | 0.6 | 默认推荐 |

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：Rerank 重排序

#### 3.1 为什么需要 Rerank？

```
检索阶段（召回）：快速但粗糙，返回 top-20
    ↓
Rerank 阶段（精排）：慢但精准，从 20 中选 top-3
    ↓
送入 LLM 生成
```

**Rerank 模型**专门训练用于判断「查询-文档」的相关性，比通用 Embedding 更精准。

#### 3.2 Cohere Rerank（API 方式）

```python
# day33/03_cohere_rerank.py
"""Cohere Rerank API"""
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CohereRerank
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma(
    collection_name="knowledge_base", embedding_function=embeddings,
    persist_directory="./chroma_db",
)

base_retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

compressor = CohereRerank(model="rerank-multilingual-v3.0", top_n=3)
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=base_retriever,
)

query = "年假制度"
docs = compression_retriever.invoke(query)
print(f"=== Rerank 后 top-3 ===")
for doc in docs:
    print(f"  {doc.page_content[:60]}...")
```

#### 3.3 本地 Rerank 模型

```bash
pip install sentence-transformers -i https://pypi.tuna.tsinghua.edu.cn/simple
```

```python
# day33/04_local_rerank.py
"""本地 Rerank 模型（BGE-Reranker）"""
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma(
    collection_name="knowledge_base", embedding_function=embeddings,
    persist_directory="./chroma_db",
)

base_retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

model = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-v2-m3")
compressor = CrossEncoderReranker(model=model, top_n=3)

compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=base_retriever,
)

docs = compression_retriever.invoke("报销流程")
print(f"=== 本地 Rerank top-3 ===")
for doc in docs:
    print(f"  {doc.page_content[:60]}...")
```

---

## 🌆 下午课程（14:00 - 17:00）

### 14:00 - 15:30 | 模块四：父文档检索

#### 4.1 Parent Document Retriever 原理

```
问题: chunk 太小，上下文不足
解决: 用小 chunk 检索，返回大 chunk（父文档）

小 chunks (100字) ──检索──→ 匹配！
    ↓ 找到父文档
大 chunks (1000字) ──返回──→ 更完整的上下文
```

```python
# day33/05_parent_document_retriever.py
"""Parent Document Retriever"""
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv
import uuid

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# 父文档分割器（大块）
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
# 子文档分割器（小块，用于检索）
child_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)

vectorstore = Chroma(collection_name="parent_child", embedding_function=embeddings)
store = InMemoryStore()

retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
)

# 添加文档
sample_docs = [
    Document(page_content="""第一章 考勤制度
    1.1 上班时间：标准工时 9:00-18:00，午休 12:00-13:00。
    1.2 弹性制度：允许 30 分钟弹性，9:30 前到岗不算迟到。
    1.3 迟到处理：迟到 15 分钟内扣 50 元，超过 15 分钟按旷工半天处理。
    1.4 加班制度：工作日加班按 1.5 倍工资，周末按 2 倍。

    第二章 年假制度
    2.1 入职满 1 年：享受 10 天带薪年假。
    2.2 入职满 3 年：享受 15 天带薪年假。
    2.3 入职满 5 年：享受 20 天带薪年假。
    2.4 年假需提前 3 天在 OA 系统申请。""", metadata={"source": "员工手册"}),
]

retriever.add_documents(sample_docs)

# 用小 chunk 检索，返回大 chunk
query = "迟到怎么处罚"
results = retriever.invoke(query)
print(f"=== 父文档检索: {query} ===")
for doc in results:
    print(f"来源: {doc.metadata.get('source', '?')}")
    print(f"内容长度: {len(doc.page_content)} 字")
    print(f"内容: {doc.page_content[:200]}...")
```

---

### 15:30 - 15:45 | 课间休息

---

### 15:45 - 17:00 | 模块五：下午实操——终极 RAG 系统

```python
# day33/06_ultimate_rag.py
"""下午实操：融合所有高级技术的 RAG 系统"""
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers import EnsembleRetriever, ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.retrievers import BM25Retriever
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_chroma import Chroma
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()


class UltimateRAG:
    def __init__(self, use_hybrid=True, use_rerank=True, use_rewrite=True):
        self.llm = ChatOpenAI(model="deepseek-chat", temperature=0)
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.use_hybrid = use_hybrid
        self.use_rerank = use_rerank
        self.use_rewrite = use_rewrite
        self._setup()

    def _setup(self):
        try:
            self.vectorstore = Chroma(
                collection_name="knowledge_base",
                embedding_function=self.embeddings,
                persist_directory="./chroma_db",
            )
            self.all_docs = None
        except Exception:
            self.all_docs = []
            self.vectorstore = None

        if self.vectorstore:
            if self.use_hybrid and self.all_docs:
                bm25 = BM25Retriever.from_documents(self.all_docs)
                bm25.k = 10
                vector_ret = self.vectorstore.as_retriever(search_kwargs={"k": 10})
                self.retriever = EnsembleRetriever(
                    retrievers=[bm25, vector_ret], weights=[0.4, 0.6]
                )
            else:
                self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 10})

            if self.use_rerank:
                try:
                    model = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-v2-m3")
                    compressor = CrossEncoderReranker(model=model, top_n=3)
                    self.retriever = ContextualCompressionRetriever(
                        base_compressor=compressor, base_retriever=self.retriever,
                    )
                except Exception as e:
                    print(f"Rerank 不可用，跳过: {e}")
                    self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})

    def _rewrite(self, question: str) -> str:
        if not self.use_rewrite:
            return question
        chain = (
            ChatPromptTemplate.from_template("改写为规范检索查询：{q}")
            | self.llm | StrOutputParser()
        )
        return chain.invoke({"q": question})

    def ask(self, question: str) -> dict:
        rewritten = self._rewrite(question)
        docs = self.retriever.invoke(rewritten)
        context = "\n".join(d.page_content for d in docs)

        answer = (
            ChatPromptTemplate.from_template(
                "基于资料回答。资料：\n{context}\n\n问题：{question}"
            ) | self.llm | StrOutputParser()
        ).invoke({"context": context, "question": question})

        return {
            "question": question,
            "rewritten": rewritten,
            "answer": answer,
            "sources": [d.metadata.get("source", "?") for d in docs],
            "retrieved_count": len(docs),
        }


def main():
    rag = UltimateRAG(use_hybrid=False, use_rerank=False, use_rewrite=True)
    result = rag.ask("年假有多少天？")
    print(f"问题: {result['question']}")
    print(f"改写: {result['rewritten']}")
    print(f"检索: {result['retrieved_count']} 个文档")
    print(f"回答: {result['answer']}")


if __name__ == "__main__":
    main()
```

---

## 🌙 晚自习（19:00 - 21:00）

### 19:00 - 20:00

1. 测试混合检索 vs 纯向量检索的效果差异
2. 如有 GPU，测试本地 Rerank 模型
3. 对比父文档检索与普通检索的上下文完整性

### 20:00 - 21:00

- 讨论：生产环境 Rerank 用 API 还是本地模型？
- 总结 Day 32-33 全部高级技术的选择决策

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | BM25 稀疏检索原理 | |
| 2 | EnsembleRetriever 混合检索 | |
| 3 | 混合检索权重调优 | |
| 4 | Cohere Rerank API | |
| 5 | 本地 CrossEncoder Rerank | |
| 6 | Parent Document Retriever | |
| 7 | 终极 RAG 系统集成 | |

---

## 📝 课后作业

### 必做题

1. **混合检索实验**：对比纯向量 vs BM25 vs 混合，5 个问题测试
2. **Rerank 效果验证**：对比 Rerank 前后的 top-3 相关性
3. **Git 提交**：`git commit -m "Day 33: 高级 RAG 技术下"`

### 选做题

4. 实现完整的「父文档检索 + 混合检索 + Rerank」流水线
5. 测试不同 BM25/向量权重比例的效果

---

## 💡 常见问题 FAQ

**Q1: BM25 支持中文吗？**

A: `rank-bm25` 默认按空格分词，中文效果差。中文需先分词（如 jieba），或使用 Elasticsearch 的 BM25。

**Q2: Rerank 值得额外的计算成本吗？**

A: 当检索结果 > 5 条且精确度要求高时，值得。Rerank 可将 top-10 精确排序到 top-3，显著提升回答质量。

**Q3: 父文档检索的父文档存在哪里？**

A: `InMemoryStore`（内存）或自定义 `ByteStore`（文件/Redis）。生产环境推荐 Redis。

**Q4: 所有高级技术都加上会不会过度工程？**

A: 会。推荐渐进式：基础 RAG → +Query Rewriting → +Rerank → +混合检索。每加一层用 Ragas 验证收益。

**Q5: Cohere Rerank 免费吗？**

A: 有免费额度。本地 `bge-reranker` 完全免费但需要 GPU 加速。

---

## 🔮 明日预习

**Day 34: RAG 评估（Ragas）**

- 为什么需要量化评估
- Ragas 框架安装与核心指标
- Faithfulness、Answer Relevancy、Context Precision
- 建立 RAG 评估流水线

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 33*
