# Day 31: 周测与 RAG 调优

> **培训阶段**: 第三阶段 RAG 应用开发 | **第 6 周 | **学习时长**: 约 6-8 小时  
> **今日关键词**: 周测、chunk 调优、Prompt 调优、检索参数、问题诊断

---

## 📍 课程导航

### 上节回顾

**Day 25-30** 你完成了 RAG 基础体系的搭建：
- LangChain / LCEL / Memory 框架能力
- 文档加载、分割、向量入库
- 完整 RAG 系统（CLI / Gradio / FastAPI）

今天是 **第 5 周总结日**——上午周测检验学习成果，下午系统学习 RAG 调优方法论。

### 本节学习目标

完成本日学习后，你将能够：

1. 通过第 5 周周测检验 LangChain 与 RAG 基础知识
2. 系统调优 chunk_size 和 chunk_overlap 参数
3. 优化 RAG Prompt 模板提升回答质量
4. 调整检索参数（k 值、MMR、相似度阈值）
5. 使用问题诊断清单定位 RAG 故障
6. 建立 RAG 调优实验的标准流程

### 与后续课程的衔接

- **Day 32-33** 高级 RAG 技术是今天调优方法的「升级版」
- **Day 34** Ragas 评估框架将量化今天的调优效果
- **Day 36-37** 企业项目需要今天的调优经验

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 10:30 | 模块一：第 5 周周测

#### 1.1 考试说明

| 项目 | 说明 |
|------|------|
| 考试时间 | 90 分钟 |
| 总分 | 100 分（及格 60 分） |
| 题型 | 选择题 20 题 + 填空题 5 题 + 编程题 3 题 |
| 范围 | Day 25-30 全部内容 |
| 形式 | 闭卷（编程题可查阅 LangChain 文档） |

#### 1.2 选择题（每题 3 分，共 60 分）

**1. LangChain 中 `prompt | llm | parser` 的 `|` 操作符属于？**
- A. Python 位运算符
- B. LCEL 管道操作符
- C. 逻辑或运算符
- D. 字符串拼接符

**2. 以下哪个不是 LangChain Memory 类型？**
- A. ConversationBufferMemory
- B. ConversationSummaryMemory
- C. ConversationCacheMemory
- D. ConversationBufferWindowMemory

**3. `RecursiveCharacterTextSplitter` 的 `chunk_overlap` 作用是？**
- A. 增加存储空间
- B. 避免语义在 chunk 边界断裂
- C. 加快分割速度
- D. 减少 chunk 数量

**4. Chroma 的 `persist_directory` 参数作用是？**
- A. 设置日志目录
- B. 数据持久化到磁盘
- C. 指定 Embedding 模型路径
- D. 设置缓存大小

**5. RAG 系统中，检索阶段返回的 k=3 表示？**
- A. 检索 3 秒内的文档
- B. 返回相似度最高的 3 个 chunks
- C. 最多问 3 个问题
- D. 使用 3 个 Embedding 模型

**6. `RunnableParallel` 的作用是？**
- A. 串行执行多个链
- B. 并行执行多个链
- C. 循环执行链
- D. 条件执行链

**7. `RunnableWithMessageHistory` 的核心参数 `session_id` 用于？**
- A. 设置模型版本
- B. 隔离不同用户的对话历史
- C. 指定向量库集合
- D. 控制输出长度

**8. Embedding 向量的维度通常是多少？**
- A. 10-50
- B. 128-512
- C. 768-3072
- D. 10000+

**9. MMR 搜索的全称是？**
- A. Maximum Mean Recall
- B. Maximal Marginal Relevance
- C. Minimum Match Rate
- D. Multi-Model Retrieval

**10. RAG 的「幻觉」问题是指？**
- A. 模型运行太慢
- B. 模型编造不存在的信息
- C. 向量库损坏
- D. 文档加载失败

**11-20 题**（完整版含 LangChain 组件、LCEL 语法、文档加载器、向量库操作、RAG 链构建等，共 20 题）

#### 1.3 填空题（每题 4 分，共 20 分）

**1.** LCEL 中，所有可组合组件都实现了 `______` 接口。

**2.** `ConversationBufferWindowMemory(k=5)` 中的 k=5 表示只保留最近 ______ 轮对话。

**3.** 中文文档分割推荐 `chunk_size` 范围 ______ 字符。

**4.** RAG 链中，`retriever | format_docs` 的作用是检索并 ______ 文档。

**5.** `similarity_search_with_score` 返回的分数越小表示相似度越 ______。

#### 1.4 编程题（共 20 分）

**编程题 1（8 分）**：用 LCEL 构建一个翻译链
- 输入：中文文本
- 输出：英文翻译
- 要求：使用 ChatPromptTemplate + ChatOpenAI + StrOutputParser

**编程题 2（6 分）**：实现文档分割与统计
- 输入：一段 1000 字以上的文本
- 用 RecursiveCharacterTextSplitter（chunk_size=200, overlap=50）分割
- 输出：chunks 数量、平均长度、最大/最小长度

**编程题 3（6 分）**：构建最简 RAG 链
- 加载已有 Chroma 向量库
- 实现 similarity_search
- 将检索结果 + 用户问题送入 LLM 生成回答

#### 1.5 参考答案要点

**选择题**: 1-B, 2-C, 3-B, 4-B, 5-B, 6-B, 7-B, 8-C, 9-B, 10-B

**填空题**: 1-Runnable, 2-5, 3-300到1000（或500）, 4-格式化, 5-高（Chroma 使用 L2 距离）

**编程题 1 参考**:
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()

chain = (
    ChatPromptTemplate.from_template("将以下中文翻译为英文：{text}")
    | ChatOpenAI(model="deepseek-chat", temperature=0)
    | StrOutputParser()
)
print(chain.invoke({"text": "你好世界"}))
```

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块二：周测讲评

#### 2.1 高频错题分析

| 题号 | 错误率 | 知识点 | 讲解要点 |
|------|--------|--------|----------|
| 3 | 35% | chunk_overlap | 不是减少数量，是保持语义连续 |
| 6 | 28% | RunnableParallel | 与串行管道 `\|` 区分 |
| 8 | 42% | Embedding 维度 | text-embedding-3-small 是 1536 维 |
| 10 | 25% | RAG 幻觉 | 检索不足或 Prompt 约束不够 |

#### 2.2 编程题常见失分点

- 忘记 `load_dotenv()`
- LCEL 链的输入格式错误（字典 vs 字符串）
- 分割后未检查 chunks 质量
- RAG 链缺少 `format_docs` 步骤

---

## 🌆 下午课程（14:00 - 17:00）

### 14:00 - 15:30 | 模块三：RAG 调优方法论

#### 3.1 调优金字塔

```
                    ┌─────────┐
                    │ 高级技术 │  Day 32-33: Query Rewriting, Rerank
                    ├─────────┤
                    │ 评估量化 │  Day 34: Ragas 评估
                    ├─────────┤
                    │ Prompt  │  ← 今天重点
                    ├─────────┤
                    │ 检索参数 │  ← 今天重点
                    ├─────────┤
                    │ 数据质量 │  ← 今天重点
                    └─────────┘
```

#### 3.2 chunk 参数调优实验

```python
# day31/01_chunk_tuning.py
"""chunk 参数调优实验"""
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

sample_text = open("knowledge_base/年假制度.txt", encoding="utf-8").read() \
    if __import__("os").path.exists("knowledge_base/年假制度.txt") \
    else "年假制度：入职满一年 10 天，满三年 15 天。" * 20

configs = [
    {"chunk_size": 200, "chunk_overlap": 0},
    {"chunk_size": 200, "chunk_overlap": 40},
    {"chunk_size": 500, "chunk_overlap": 100},
    {"chunk_size": 1000, "chunk_overlap": 200},
]

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
test_query = "工作满三年能休几天假"

print(f"{'chunk_size':>12} {'overlap':>8} {'chunks':>8} {'avg_len':>8} {'top1_relevant':>15}")
print("-" * 60)

for cfg in configs:
    splitter = RecursiveCharacterTextSplitter(**cfg)
    chunks = splitter.split_text(sample_text)
    avg_len = sum(len(c) for c in chunks) / len(chunks)

    from langchain_core.documents import Document
    docs = [Document(page_content=c) for c in chunks]
    vs = Chroma.from_documents(docs, embeddings)
    results = vs.similarity_search(test_query, k=1)
    relevant = "✅" if "15" in results[0].page_content or "三年" in results[0].page_content else "❌"

    print(f"{cfg['chunk_size']:>12} {cfg['chunk_overlap']:>8} {len(chunks):>8} {avg_len:>8.0f} {relevant:>15}")
```

#### 3.3 Prompt 调优

```python
# day31/02_prompt_tuning.py
"""RAG Prompt 调优对比"""
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma(
    collection_name="knowledge_base", embedding_function=embeddings,
    persist_directory="./chroma_db",
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
llm = ChatOpenAI(model="deepseek-chat", temperature=0)

prompts = {
    "v0_简单": "资料：{context}\n问题：{question}",
    "v1_约束": """基于参考资料回答问题。如果资料中没有相关信息，请明确说"无法回答"。
资料：{context}
问题：{question}""",
    "v2_详细": """你是企业知识库助手。请基于参考资料回答问题。

规则：
1. 只根据参考资料回答，不要编造
2. 无相关信息时明确说明
3. 引用来源，格式：[来源: 文件名]
4. 简洁准确，使用 Markdown

参考资料：
{context}

问题：{question}""",
}

question = "公司成立于哪一年？"

for name, template in prompts.items():
    chain = (
        {"context": retriever | (lambda d: "\n".join(x.page_content for x in d)),
         "question": RunnablePassthrough()}
        | ChatPromptTemplate.from_template(template)
        | llm | StrOutputParser()
    )
    answer = chain.invoke(question)
    print(f"\n=== {name} ===")
    print(answer[:200])
```

#### 3.4 检索参数调优

```python
# day31/03_retrieval_tuning.py
"""检索参数调优"""
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma(
    collection_name="knowledge_base", embedding_function=embeddings,
    persist_directory="./chroma_db",
)

query = "请假制度"
k_values = [1, 3, 5, 10]

for k in k_values:
    results = vectorstore.similarity_search_with_score(query, k=k)
    print(f"\n=== k={k} ===")
    for doc, score in results:
        print(f"  分数:{score:.4f} | {doc.page_content[:50]}...")

# MMR vs Similarity
print("\n=== MMR (k=3, fetch_k=10) ===")
mmr_retriever = vectorstore.as_retriever(
    search_type="mmr", search_kwargs={"k": 3, "fetch_k": 10, "lambda_mult": 0.7}
)
for doc in mmr_retriever.invoke(query):
    print(f"  {doc.page_content[:50]}...")
```

---

### 15:30 - 15:45 | 课间休息

---

### 15:45 - 17:00 | 模块四：RAG 问题诊断清单

#### 4.1 诊断决策树

```
RAG 回答质量差
├── 检索结果不相关？
│   ├── 是 → 检查 Embedding 模型 / chunk_size / 考虑 Query Rewriting (Day 32)
│   └── 否 → 继续
├── 检索到了但 LLM 没用？
│   ├── 是 → 优化 Prompt / 降低 temperature
│   └── 否 → 继续
├── LLM 编造信息？
│   ├── 是 → Prompt 加强约束 / 要求引用来源
│   └── 否 → 继续
└── 回答不完整？
    ├── 是 → 增大 k 值 / 增大 chunk_size
    └── 否 → 考虑 Rerank (Day 33)
```

#### 4.2 调优实验记录模板

```python
# day31/04_tuning_experiment.py
"""调优实验记录"""
import json
from datetime import datetime

class RAGExperiment:
    def __init__(self, name: str):
        self.name = name
        self.records = []

    def log(self, config: dict, question: str, answer: str, score: int, notes: str = ""):
        self.records.append({
            "timestamp": datetime.now().isoformat(),
            "config": config,
            "question": question,
            "answer": answer[:200],
            "score": score,  # 1-5 主观评分
            "notes": notes,
        })

    def summary(self):
        if not self.records:
            return "无记录"
        avg = sum(r["score"] for r in self.records) / len(self.records)
        best = max(self.records, key=lambda r: r["score"])
        return f"实验: {self.name}, 平均分: {avg:.1f}, 最佳: {best['config']}"

    def export(self, path: str):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.records, f, ensure_ascii=False, indent=2)


exp = RAGExperiment("chunk_size 对比")
exp.log({"chunk_size": 200}, "年假多少天", "满一年10天...", 4)
exp.log({"chunk_size": 500}, "年假多少天", "根据规定...", 5)
print(exp.summary())
```

#### 4.3 下午实操：系统调优

对 Day 30 的 RAG 系统执行完整调优：
1. 测试 3 种 chunk_size 配置
2. 对比 3 版 Prompt 模板
3. 测试 k=1/3/5/10
4. 记录实验结果，选出最优配置

---

## 🌙 晚自习（19:00 - 21:00）

### 19:00 - 20:00

1. 完成下午调优实验并导出记录
2. 复习周测错题
3. 预习 Day 32 Query Rewriting

### 20:00 - 21:00

- 分享调优实验中最意外的发现
- 讨论：「调优有没有终点？」

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | 第 5 周周测（LangChain + RAG 基础） | |
| 2 | chunk_size / overlap 调优方法 | |
| 3 | RAG Prompt 迭代优化 | |
| 4 | 检索参数 k 值 / MMR 调优 | |
| 5 | RAG 问题诊断决策树 | |
| 6 | 调优实验记录方法 | |

---

## 📝 课后作业

### 必做题

1. **调优报告**：完成 chunk / Prompt / k 值三组实验，提交对比报告
2. **周测补考**（如需要）：60 分以下需补考
3. **Git 提交**：`git commit -m "Day 31: 周测与 RAG 调优"`

### 选做题

4. 设计 20 个测试问题 + 标准答案，作为后续 Ragas 评估数据集
5. 实现自动化调优脚本：遍历参数组合，输出最优配置

---

## 💡 常见问题 FAQ

**Q1: 调优应该先改哪个参数？**

A: 按优先级：数据质量（文档内容）→ chunk 参数 → Prompt → 检索 k 值 → 高级技术。不要跳过基础直接上高级技术。

**Q2: chunk_size 越大越好吗？**

A: 不是。太大导致检索不精确（返回大量无关内容），太小导致上下文不足。中文推荐 300-800。

**Q3: 怎么判断 RAG 系统「够好了」？**

A: Day 34 的 Ragas 评估可以量化。开发阶段用 10-20 个测试问题人工打分也有效。

**Q4: MMR 的 lambda_mult 怎么设？**

A: 1.0 = 只看相似度，0.0 = 只看多样性。推荐 0.5-0.7 平衡。

**Q5: 周测编程题可以用 AI 辅助吗？**

A: 闭卷考试不行。但理解代码逻辑比手写更重要，考后可用 AI 优化实现。

---

## 🔮 明日预习

**Day 32: 高级 RAG 技术上**

- Query Rewriting 查询改写
- Multi-Query 多查询检索
- HyDE 假想文档嵌入
- 这些技术解决「用户问题与文档表述不匹配」的核心痛点

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 31*
