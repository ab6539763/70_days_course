# Day 32: 高级 RAG 技术上

> **培训阶段**: 第三阶段 RAG 应用开发 | **第 6 周 | **学习时长**: 约 6-8 小时  
> **今日关键词**: Query Rewriting、Multi-Query、HyDE、查询增强

---

## 📍 课程导航

### 上节回顾

**Day 31** 你完成了第 5 周周测与 RAG 基础调优：
- chunk_size / Prompt / 检索 k 值调优
- RAG 问题诊断决策树
- 调优实验记录方法

今天学习 **高级 RAG 技术（上）**——解决 RAG 最核心的问题：**用户的问题和文档的表述方式不匹配**，导致检索不到相关内容。

### 本节学习目标

完成本日学习后，你将能够：

1. 理解 Query Rewriting 的原理与适用场景
2. 实现查询改写链，优化用户原始问题
3. 使用 Multi-Query Retriever 生成多个查询视角
4. 理解并实现 HyDE（Hypothetical Document Embeddings）
5. 对比三种技术的检索效果提升
6. 将查询增强技术集成到 Day 30 的 RAG 系统

### 与后续课程的衔接

- **Day 33** 混合检索 + Rerank + 父文档检索，进一步优化检索质量
- **Day 34** Ragas 评估将量化今天技术的效果提升
- **Day 36-37** 企业项目默认启用 Query Rewriting

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：查询增强问题分析

#### 1.1 为什么检索会失败？

```
用户问: "咋请假啊"          文档写: "员工休假申请流程"
用户问: "AI 怎么落地"       文档写: "人工智能在企业中的实施路径"
用户问: "报销要多久"       文档写: "费用报销审批时效为 3 个工作日"
```

**根本原因**：用户查询（Query）与文档内容（Document）之间存在 **语义鸿沟**：
- 口语 vs 书面语
- 缩写 vs 全称
- 问题形式 vs 陈述形式

#### 1.2 三大查询增强技术

| 技术 | 思路 | 成本 | 效果 |
|------|------|------|------|
| Query Rewriting | 改写查询使其更规范 | 1 次 LLM 调用 | ⭐⭐⭐ |
| Multi-Query | 生成多个查询视角 | 1 次 LLM 调用 | ⭐⭐⭐⭐ |
| HyDE | 生成假想答案再检索 | 1 次 LLM 调用 | ⭐⭐⭐⭐ |

```
原始查询 ──→ [Query Rewriting] ──→ 规范化查询 ──→ 检索
原始查询 ──→ [Multi-Query]    ──→ 查询1 ──→ 检索 ──→ 合并
                              ──→ 查询2 ──→ 检索 ──→ 结果
                              ──→ 查询3 ──→ 检索 ──→
原始查询 ──→ [HyDE]           ──→ 生成假想文档 ──→ 用假想文档检索
```

---

### 9:45 - 10:30 | 模块二：Query Rewriting 查询改写

#### 2.1 基础查询改写

```python
# day32/01_query_rewriting.py
"""Query Rewriting 查询改写"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", temperature=0)

rewrite_prompt = ChatPromptTemplate.from_template("""你是一个查询优化专家。
将用户的口语化/模糊问题改写为清晰、规范的知识库检索查询。

要求：
1. 保留原意，不添加假设
2. 使用书面语和专业术语
3. 只输出改写后的查询，不要解释

原始问题：{question}
改写后查询：""")

rewrite_chain = rewrite_prompt | llm | StrOutputParser()

test_questions = [
    "咋请假啊",
    "报销要多久才能到账",
    "能不能在家办公",
    "入职需要带啥",
]

print("=== Query Rewriting ===")
for q in test_questions:
    rewritten = rewrite_chain.invoke({"question": q})
    print(f"  原始: {q}")
    print(f"  改写: {rewritten}")
    print()
```

#### 2.2 改写 + 检索完整链

```python
# day32/02_rewrite_and_retrieve.py
"""Query Rewriting + 检索"""
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", temperature=0)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma(
    collection_name="knowledge_base", embedding_function=embeddings,
    persist_directory="./chroma_db",
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

rewrite_chain = (
    ChatPromptTemplate.from_template(
        "将以下问题改写为规范的知识库检索查询，只输出查询：{question}"
    ) | llm | StrOutputParser()
)

def compare_retrieval(question: str):
    print(f"\n原始问题: {question}")

    # 直接检索
    direct_results = retriever.invoke(question)
    print(f"  直接检索 top-1: {direct_results[0].page_content[:60]}...")

    # 改写后检索
    rewritten = rewrite_chain.invoke({"question": question})
    rewrite_results = retriever.invoke(rewritten)
    print(f"  改写查询: {rewritten}")
    print(f"  改写检索 top-1: {rewrite_results[0].page_content[:60]}...")

compare_retrieval("咋请假啊")
compare_retrieval("报销多久到账")
```

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：Multi-Query 多查询检索

#### 3.1 Multi-Query Retriever

```python
# day32/03_multi_query.py
"""Multi-Query Retriever"""
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_chroma import Chroma
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig()
logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)

llm = ChatOpenAI(model="deepseek-chat", temperature=0)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma(
    collection_name="knowledge_base", embedding_function=embeddings,
    persist_directory="./chroma_db",
)

retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    llm=llm,
)

question = "公司的休假和报销政策是什么？"
docs = retriever.invoke(question)

print(f"=== Multi-Query: {question} ===")
print(f"检索到 {len(docs)} 个文档（去重后）")
for i, doc in enumerate(docs):
    print(f"  [{i+1}] {doc.page_content[:60]}...")
```

#### 3.2 手动实现 Multi-Query

```python
# day32/04_multi_query_manual.py
"""手动实现 Multi-Query"""
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", temperature=0.3)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma(
    collection_name="knowledge_base", embedding_function=embeddings,
    persist_directory="./chroma_db",
)
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

generate_queries_prompt = ChatPromptTemplate.from_template("""你是一个 AI 助手。根据用户问题，生成 3 个不同视角的检索查询。
每行一个查询，不要编号，不要解释。

原始问题：{question}""")

def parse_queries(text: str) -> list[str]:
    return [line.strip() for line in text.strip().split("\n") if line.strip()]

def multi_query_retrieve(question: str) -> list:
    queries_text = (generate_queries_prompt | llm | StrOutputParser()).invoke({"question": question})
    queries = parse_queries(queries_text)
    queries.insert(0, question)

    print(f"生成了 {len(queries)} 个查询:")
    seen = set()
    unique_docs = []
    for q in queries:
        print(f"  - {q}")
        docs = base_retriever.invoke(q)
        for doc in docs:
            content_hash = hash(doc.page_content)
            if content_hash not in seen:
                seen.add(content_hash)
                unique_docs.append(doc)

    return unique_docs

docs = multi_query_retrieve("员工福利和假期政策")
print(f"\n去重后共 {len(docs)} 个文档")
```

---

## 🌆 下午课程（14:00 - 17:00）

### 14:00 - 15:30 | 模块四：HyDE 假想文档嵌入

#### 4.1 HyDE 原理

传统 RAG：用 **问题** 的向量去匹配 **文档** 的向量——但问题和答案的表述方式不同！

HyDE 的思路：
1. 用 LLM 根据问题 **生成一个假想的答案**
2. 用假想答案的向量去检索（答案 vs 文档，语义更接近！）

```
问题: "年假有多少天？"
  ↓ LLM 生成假想答案
假想: "根据公司规定，员工入职满一年可享受10天年假..."
  ↓ Embedding
假想向量 → 匹配文档向量（更精准！）
```

#### 4.2 HyDE 实现

```python
# day32/05_hyde.py
"""HyDE: Hypothetical Document Embeddings"""
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", temperature=0.3)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma(
    collection_name="knowledge_base", embedding_function=embeddings,
    persist_directory="./chroma_db",
)

hyde_prompt = ChatPromptTemplate.from_template("""请根据以下问题，写一段可能出现在企业知识库中的文档段落。
直接输出文档内容，不要说明这是假想的。

问题：{question}
文档段落：""")

hyde_chain = hyde_prompt | llm | StrOutputParser()

def hyde_retrieve(question: str, k: int = 3):
    hypothetical_doc = hyde_chain.invoke({"question": question})
    print(f"假想文档: {hypothetical_doc[:100]}...")

  # 用假想文档的向量检索
    results = vectorstore.similarity_search(hypothetical_doc, k=k)
    return results

def compare_methods(question: str):
    print(f"\n问题: {question}")

    direct = vectorstore.similarity_search(question, k=1)
    print(f"直接检索: {direct[0].page_content[:60]}...")

    hyde_results = hyde_retrieve(question, k=1)
    print(f"HyDE 检索: {hyde_results[0].page_content[:60]}...")

compare_methods("工作满三年休假天数")
compare_methods("费用报销需要多长时间")
```

#### 4.3 LangChain 内置 HyDE

```python
# day32/06_hyde_builtin.py
"""LangChain 内置 HyDE Retriever"""
from langchain.chains import HypotheticalDocumentEmbedder
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

base_embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
llm = ChatOpenAI(model="deepseek-chat", temperature=0.3)

hyde_embeddings = HypotheticalDocumentEmbedder.from_llm(
    llm=llm,
    base_embeddings=base_embeddings,
    prompt_key="web_search",  # 内置 prompt 模板
)

vectorstore = Chroma(
    collection_name="knowledge_base",
    embedding_function=hyde_embeddings,
    persist_directory="./chroma_db",
)

results = vectorstore.similarity_search("远程办公政策", k=3)
for doc in results:
    print(doc.page_content[:60])
```

---

### 15:30 - 15:45 | 课间休息

---

### 15:45 - 17:00 | 模块五：下午实操——查询增强 RAG 系统

```python
# day32/07_enhanced_rag.py
"""下午实操：集成查询增强的 RAG 系统"""
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_chroma import Chroma
from dotenv import load_dotenv
from enum import Enum

load_dotenv()


class RetrievalStrategy(Enum):
    DIRECT = "direct"
    REWRITE = "rewrite"
    MULTI_QUERY = "multi_query"
    HYDE = "hyde"


class EnhancedRAG:
    def __init__(self, strategy: RetrievalStrategy = RetrievalStrategy.REWRITE):
        self.llm = ChatOpenAI(model="deepseek-chat", temperature=0)
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.vectorstore = Chroma(
            collection_name="knowledge_base",
            embedding_function=self.embeddings,
            persist_directory="./chroma_db",
        )
        self.strategy = strategy
        self._setup_retriever()

    def _setup_retriever(self):
        base = self.vectorstore.as_retriever(search_kwargs={"k": 3})
        if self.strategy == RetrievalStrategy.MULTI_QUERY:
            self.retriever = MultiQueryRetriever.from_llm(
                retriever=base, llm=self.llm
            )
        else:
            self.retriever = base

    def _rewrite_query(self, question: str) -> str:
        chain = (
            ChatPromptTemplate.from_template(
                "将问题改写为规范检索查询，只输出查询：{question}"
            ) | self.llm | StrOutputParser()
        )
        return chain.invoke({"question": question})

    def _hyde_query(self, question: str) -> str:
        chain = (
            ChatPromptTemplate.from_template(
                "根据问题写一段可能出现在知识库中的文档：{question}"
            ) | ChatOpenAI(model="deepseek-chat", temperature=0.3) | StrOutputParser()
        )
        return chain.invoke({"question": question})

    def retrieve(self, question: str):
        if self.strategy == RetrievalStrategy.REWRITE:
            rewritten = self._rewrite_query(question)
            print(f"  [改写] {question} → {rewritten}")
            return self.retriever.invoke(rewritten)
        elif self.strategy == RetrievalStrategy.HYDE:
            hypo = self._hyde_query(question)
            print(f"  [HyDE] 假想文档: {hypo[:60]}...")
            return self.vectorstore.similarity_search(hypo, k=3)
        else:
            return self.retriever.invoke(question)

    def ask(self, question: str) -> str:
        docs = self.retrieve(question)
        context = "\n".join(d.page_content for d in docs)

        chain = (
            ChatPromptTemplate.from_template(
                "基于资料回答。资料：\n{context}\n\n问题：{question}"
            ) | self.llm | StrOutputParser()
        )
        return chain.invoke({"context": context, "question": question})


def benchmark():
    question = "咋请假啊"
    for strategy in RetrievalStrategy:
        print(f"\n{'='*50}")
        print(f"策略: {strategy.value}")
        rag = EnhancedRAG(strategy=strategy)
        answer = rag.ask(question)
        print(f"回答: {answer[:150]}...")


if __name__ == "__main__":
    benchmark()
```

---

## 🌙 晚自习（19:00 - 21:00）

### 19:00 - 20:00

1. 对 5 个口语化问题测试 4 种检索策略
2. 记录哪种策略效果最好
3. 阅读 HyDE 原论文摘要

### 20:00 - 21:00

- 讨论：Query Rewriting vs HyDE，什么场景用哪个？
- 成本分析：每种技术增加 1 次 LLM 调用，值得吗？

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | 查询-文档语义鸿沟问题 | |
| 2 | Query Rewriting 原理与实现 | |
| 3 | Multi-Query Retriever | |
| 4 | 手动 Multi-Query 实现 | |
| 5 | HyDE 原理与实现 | |
| 6 | LangChain 内置 HyDE | |
| 7 | 查询增强 RAG 系统集成 | |
| 8 | 检索策略对比实验 | |

---

## 📝 课后作业

### 必做题

1. **策略对比实验**：5 个问题 × 4 种策略，提交对比表格
2. **集成到 RAG 系统**：将最优策略集成到 Day 30 系统
3. **Git 提交**：`git commit -m "Day 32: 高级 RAG 技术上"`

### 选做题

4. 实现「策略自动选择」：根据问题长度/口语化程度自动选策略
5. 组合 Query Rewriting + Multi-Query

---

## 💡 常见问题 FAQ

**Q1: 三种技术可以组合使用吗？**

A: 可以但成本叠加。推荐：开发阶段选一种测试，生产环境用 Query Rewriting（性价比最高）。

**Q2: HyDE 生成的假想文档不准确怎么办？**

A: HyDE 的优势在于「向量方向」而非内容准确性。即使假想文档有错误，其向量仍可能比原始问题更接近真实文档。

**Q3: Multi-Query 生成了重复查询怎么办？**

A: 检索后做去重（按 page_content 哈希）。LangChain 内置的 MultiQueryRetriever 已包含去重。

**Q4: 查询增强会增加多少延迟？**

A: 每种技术增加 1 次 LLM 调用（约 0.5-2 秒）。可用更快的小模型做改写，主模型做生成。

**Q5: 口语化不严重还需要查询增强吗？**

A: 如果直接检索效果已经很好，不必强行使用。先用 Day 34 的 Ragas 评估再决定。

---

## 🔮 明日预习

**Day 33: 高级 RAG 技术下**

- 混合检索（BM25 + 向量）
- Rerank 重排序
- 父文档检索（Parent Document Retriever）
- 这些技术解决「检索结果排序不优」和「chunk 上下文不足」问题

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 32*
