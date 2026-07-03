# Day 34: RAG 评估

> **培训阶段**: 第三阶段 RAG 应用开发 | **第 6 周 | **学习时长**: 约 6-8 小时  
> **今日关键词**: Ragas、Faithfulness、Answer Relevancy、Context Precision、评估流水线

---

## 📍 课程导航

### 上节回顾

**Day 32-33** 你学习了全套高级 RAG 技术：
- Query Rewriting / Multi-Query / HyDE
- BM25 + 向量混合检索
- Rerank 重排序
- Parent Document Retriever

今天解决一个关键问题：**怎么知道这些技术是否真的提升了效果？** 答案是 **RAG 评估框架 Ragas**。

### 本节学习目标

完成本日学习后，你将能够：

1. 理解 RAG 评估的必要性与指标体系
2. 安装配置 Ragas 评估框架
3. 使用核心指标：Faithfulness、Answer Relevancy、Context Precision/Recall
4. 构建测试数据集（问题 + 标准答案 + 参考上下文）
5. 建立自动化 RAG 评估流水线
6. 用评估结果驱动 RAG 系统迭代优化

### 与后续课程的衔接

- **Day 35** LlamaIndex 也有自己的评估模块，理念相通
- **Day 36-37** 企业项目需要评估报告作为交付物
- **Day 38** 项目答辩时用 Ragas 数据支撑你的设计决策

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：RAG 评估体系

#### 1.1 为什么需要评估？

```
没有评估的 RAG 调优 = 盲人摸象

"感觉变好了" ≠ 真的好
"这个技术很酷" ≠ 适合你的场景
```

#### 1.2 RAG 评估指标全景

```
RAG 评估
├── 检索质量
│   ├── Context Precision  检索结果中相关的比例
│   └── Context Recall     相关文档被检索到的比例
├── 生成质量
│   ├── Faithfulness       回答是否忠于检索内容（无幻觉）
│   └── Answer Relevancy   回答与问题的相关程度
└── 端到端
    └── Answer Correctness  回答与标准答案的一致性
```

| 指标 | 衡量什么 | 低分意味着 | 优化方向 |
|------|----------|-----------|----------|
| Context Precision | 检索精准度 | 检索到无关文档 | Rerank / 调 k 值 |
| Context Recall | 检索召回率 | 漏掉相关文档 | 混合检索 / Multi-Query |
| Faithfulness | 无幻觉 | 编造信息 | Prompt 约束 / 降低 temperature |
| Answer Relevancy | 回答相关性 | 答非所问 | Prompt 优化 |
| Answer Correctness | 答案正确性 | 事实错误 | 综合优化 |

---

### 9:45 - 10:30 | 模块二：Ragas 框架入门

#### 2.1 安装与配置

```bash
pip install ragas datasets -i https://pypi.tuna.tsinghua.edu.cn/simple
```

```python
# day34/01_ragas_basics.py
"""Ragas 基础评估"""
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
from datasets import Dataset
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

# 构建评估数据集
eval_data = {
    "question": [
        "年假有多少天？",
        "报销流程是什么？",
        "远程办公政策？",
    ],
    "answer": [
        "入职满一年享受10天年假，满三年15天。",
        "填写报销单，经部门经理审批，财务部审核后打款。",
        "每周最多2天远程办公，需提前在OA申请。",
    ],
    "contexts": [
        ["员工年假制度：入职满一年享受10天年假，满三年15天，满五年20天。"],
        ["报销流程：填写报销单→部门经理审批→财务部审核→3个工作日内打款。"],
        ["远程办公政策：每周最多2天远程，需提前在OA系统申请。"],
    ],
    "ground_truth": [
        "入职满一年10天，满三年15天，满五年20天。",
        "填写报销单，部门经理审批，财务审核，3个工作日内打款。",
        "每周最多2天远程办公，需OA申请。",
    ],
}

dataset = Dataset.from_dict(eval_data)

llm = ChatOpenAI(model="deepseek-chat", temperature=0)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

result = evaluate(
    dataset,
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
    llm=llm,
    embeddings=embeddings,
)

print("=== Ragas 评估结果 ===")
print(result)
```

#### 2.2 指标详解

```python
# day34/02_metrics_explained.py
"""Ragas 指标详解与单独计算"""
from ragas.metrics import faithfulness, answer_relevancy
from ragas import SingleTurnSample
from ragas.llms import LangchainLLMWrapper
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = LangchainLLMWrapper(ChatOpenAI(model="deepseek-chat", temperature=0))

# Faithfulness: 回答是否基于上下文（无幻觉）
faith_sample = SingleTurnSample(
    user_input="年假有多少天？",
    response="入职满一年享受10天年假。",
    retrieved_contexts=["员工年假制度：入职满一年享受10天年假，满三年15天。"],
)
faith_scorer = faithfulness
faith_score = faith_scorer.single_turn_score(faith_sample, llm=llm)
print(f"Faithfulness: {faith_score:.4f}")

# 幻觉样本
hallucination_sample = SingleTurnSample(
    user_input="公司成立于哪一年？",
    response="公司成立于2018年。",  # 编造的！
    retrieved_contexts=["公司考勤制度：标准工时9:00-18:00。"],  # 上下文无此信息
)
halluc_score = faith_scorer.single_turn_score(hallucination_sample, llm=llm)
print(f"幻觉样本 Faithfulness: {halluc_score:.4f}")
```

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：构建评估数据集

#### 3.1 测试数据设计原则

| 类型 | 数量建议 | 示例 |
|------|----------|------|
| 直接匹配 | 30% | "年假多少天" |
| 语义变换 | 30% | "休假制度是怎样的" |
| 口语化 | 20% | "咋请假啊" |
| 多跳推理 | 10% | "工作三年能休几天假" |
| 无答案 | 10% | "公司上市计划" |

#### 3.2 评估数据集构建

```python
# day34/03_eval_dataset.py
"""构建 RAG 评估数据集"""
import json

eval_dataset = [
    {
        "question": "入职满一年能休几天年假？",
        "ground_truth": "10天年假",
        "category": "直接匹配",
    },
    {
        "question": "员工休假制度是怎样的？",
        "ground_truth": "入职满一年10天，满三年15天，满五年20天",
        "category": "语义变换",
    },
    {
        "question": "咋请假啊",
        "ground_truth": "需在OA系统提前3天申请",
        "category": "口语化",
    },
    {
        "question": "工作了三年能休多少天假？",
        "ground_truth": "15天年假",
        "category": "多跳推理",
    },
    {
        "question": "公司上市计划是什么？",
        "ground_truth": "无法回答，资料中无此信息",
        "category": "无答案",
    },
    {
        "question": "报销需要多长时间？",
        "ground_truth": "3个工作日内打款",
        "category": "直接匹配",
    },
    {
        "question": "费用报销的审批流程",
        "ground_truth": "填写报销单→部门经理审批→财务部审核→打款",
        "category": "语义变换",
    },
    {
        "question": "能不能在家办公？",
        "ground_truth": "每周最多2天远程办公，需OA申请",
        "category": "口语化",
    },
    {
        "question": "迟到怎么处罚？",
        "ground_truth": "迟到15分钟内扣50元",
        "category": "直接匹配",
    },
    {
        "question": "公司的福利待遇有哪些？",
        "ground_truth": "年假、远程办公、技术培训等",
        "category": "多跳推理",
    },
]

with open("eval_dataset.json", "w", encoding="utf-8") as f:
    json.dump(eval_dataset, f, ensure_ascii=False, indent=2)

print(f"评估数据集: {len(eval_dataset)} 条")
for item in eval_dataset:
    print(f"  [{item['category']}] {item['question']}")
```

---

## 🌆 下午课程（14:00 - 17:00）

### 14:00 - 15:30 | 模块四：自动化评估流水线

#### 4.1 端到端评估

```python
# day34/04_eval_pipeline.py
"""自动化 RAG 评估流水线"""
import json
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision
from datasets import Dataset
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()


class RAGEvaluator:
    def __init__(self):
        self.llm = ChatOpenAI(model="deepseek-chat", temperature=0)
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.vectorstore = Chroma(
            collection_name="knowledge_base",
            embedding_function=self.embeddings,
            persist_directory="./chroma_db",
        )
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
        self.rag_chain = (
            {"context": self.retriever | (lambda d: [x.page_content for x in d]),
             "question": RunnablePassthrough()}
            | RunnablePassthrough.assign(
                answer=ChatPromptTemplate.from_template(
                    "基于资料回答：\n{context}\n\n问题：{question}"
                ) | self.llm | StrOutputParser()
            )
        )

    def run_rag(self, question: str) -> dict:
        docs = self.retriever.invoke(question)
        contexts = [d.page_content for d in docs]
        answer = (
            ChatPromptTemplate.from_template(
                "基于资料回答：\n{context}\n\n问题：{question}"
            ) | self.llm | StrOutputParser()
        ).invoke({"context": "\n".join(contexts), "question": question})
        return {"answer": answer, "contexts": contexts}

    def evaluate(self, dataset_path: str = "eval_dataset.json"):
        with open(dataset_path, encoding="utf-8") as f:
            test_data = json.load(f)

        questions, answers, contexts_list, ground_truths = [], [], [], []
        for item in test_data:
            result = self.run_rag(item["question"])
            questions.append(item["question"])
            answers.append(result["answer"])
            contexts_list.append(result["contexts"])
            ground_truths.append(item["ground_truth"])

        eval_dataset = Dataset.from_dict({
            "question": questions,
            "answer": answers,
            "contexts": contexts_list,
            "ground_truth": ground_truths,
        })

        result = evaluate(
            eval_dataset,
            metrics=[faithfulness, answer_relevancy, context_precision],
            llm=self.llm,
            embeddings=self.embeddings,
        )

        print("\n=== RAG 评估报告 ===")
        for metric, score in result.items():
            if isinstance(score, (int, float)):
                bar = "█" * int(score * 20) + "░" * (20 - int(score * 20))
                print(f"  {metric:25s} {bar} {score:.4f}")

        return result


if __name__ == "__main__":
    evaluator = RAGEvaluator()
    evaluator.evaluate()
```

#### 4.2 A/B 对比评估

```python
# day34/05_ab_comparison.py
"""A/B 对比：基础 RAG vs 高级 RAG"""
import json
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision
from datasets import Dataset
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()


def run_eval(name, retriever, test_data, llm, embeddings):
    questions, answers, contexts_list, ground_truths = [], [], [], []

    for item in test_data:
        docs = retriever.invoke(item["question"])
        contexts = [d.page_content for d in docs]
        answer = (
            ChatPromptTemplate.from_template("基于资料回答：\n{context}\n\n问题：{question}")
            | llm | StrOutputParser()
        ).invoke({"context": "\n".join(contexts), "question": item["question"]})

        questions.append(item["question"])
        answers.append(answer)
        contexts_list.append(contexts)
        ground_truths.append(item["ground_truth"])

    dataset = Dataset.from_dict({
        "question": questions, "answer": answers,
        "contexts": contexts_list, "ground_truth": ground_truths,
    })

    result = evaluate(
        dataset, metrics=[faithfulness, answer_relevancy, context_precision],
        llm=llm, embeddings=embeddings,
    )
    print(f"\n=== {name} ===")
    for metric, score in result.items():
        if isinstance(score, (int, float)):
            print(f"  {metric}: {score:.4f}")
    return result


def main():
    llm = ChatOpenAI(model="deepseek-chat", temperature=0)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma(
        collection_name="knowledge_base", embedding_function=embeddings,
        persist_directory="./chroma_db",
    )

    with open("eval_dataset.json", encoding="utf-8") as f:
        test_data = json.load(f)

    # A: 基础检索 k=3
    retriever_basic = vectorstore.as_retriever(search_kwargs={"k": 3})
    run_eval("基础 RAG (k=3)", retriever_basic, test_data, llm, embeddings)

    # B: 更多检索 k=5
    retriever_more = vectorstore.as_retriever(search_kwargs={"k": 5})
    run_eval("扩展 RAG (k=5)", retriever_more, test_data, llm, embeddings)


if __name__ == "__main__":
    main()
```

---

### 15:30 - 15:45 | 课间休息

---

### 15:45 - 17:00 | 模块五：下午实操——评估报告生成

```python
# day34/06_eval_report.py
"""下午实操：生成 RAG 评估报告"""
import json
from datetime import datetime
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision
from datasets import Dataset
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()


def generate_report():
    llm = ChatOpenAI(model="deepseek-chat", temperature=0)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma(
        collection_name="knowledge_base", embedding_function=embeddings,
        persist_directory="./chroma_db",
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    with open("eval_dataset.json", encoding="utf-8") as f:
        test_data = json.load(f)

    questions, answers, contexts_list, ground_truths = [], [], [], []
    details = []

    for item in test_data:
        docs = retriever.invoke(item["question"])
        contexts = [d.page_content for d in docs]
        answer = (
            ChatPromptTemplate.from_template("基于资料回答：\n{context}\n\n问题：{question}")
            | llm | StrOutputParser()
        ).invoke({"context": "\n".join(contexts), "question": item["question"]})

        questions.append(item["question"])
        answers.append(answer)
        contexts_list.append(contexts)
        ground_truths.append(item["ground_truth"])
        details.append({
            "question": item["question"],
            "category": item["category"],
            "answer": answer,
            "ground_truth": item["ground_truth"],
        })

    dataset = Dataset.from_dict({
        "question": questions, "answer": answers,
        "contexts": contexts_list, "ground_truth": ground_truths,
    })

    result = evaluate(
        dataset, metrics=[faithfulness, answer_relevancy, context_precision],
        llm=llm, embeddings=embeddings,
    )

    report = {
        "timestamp": datetime.now().isoformat(),
        "total_questions": len(test_data),
        "metrics": {k: float(v) for k, v in result.items() if isinstance(v, (int, float))},
        "details": details,
        "recommendations": [],
    }

    for metric, score in report["metrics"].items():
        if score < 0.7:
            report["recommendations"].append(f"{metric} 偏低 ({score:.2f})，需要优化")

    with open("rag_eval_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("📊 RAG 评估报告已生成: rag_eval_report.json")
    for metric, score in report["metrics"].items():
        print(f"  {metric}: {score:.4f}")
    if report["recommendations"]:
        print("\n⚠️ 优化建议:")
        for rec in report["recommendations"]:
            print(f"  - {rec}")


if __name__ == "__main__":
    generate_report()
```

---

## 🌙 晚自习（19:00 - 21:00）

### 19:00 - 20:00

1. 运行完整评估流水线，生成报告
2. 针对低分指标制定优化方案
3. 扩展评估数据集到 20 条

### 20:00 - 21:00

- 讨论：Ragas 指标的局限性
- 如何向非技术人员展示评估结果

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | RAG 评估指标体系 | |
| 2 | Ragas 框架安装与使用 | |
| 3 | Faithfulness / Answer Relevancy | |
| 4 | Context Precision / Recall | |
| 5 | 评估数据集设计原则 | |
| 6 | 自动化评估流水线 | |
| 7 | A/B 对比评估 | |
| 8 | 评估报告生成 | |

---

## 📝 课后作业

### 必做题

1. **完整评估**：对 Day 30 RAG 系统运行 Ragas 评估，提交报告
2. **优化迭代**：根据评估结果优化一个低分指标，重新评估对比
3. **Git 提交**：`git commit -m "Day 34: RAG 评估"`

### 选做题

4. 对比 Day 32 四种检索策略的 Ragas 分数
5. 设计 30 条评估数据，覆盖 5 种问题类型

---

## 💡 常见问题 FAQ

**Q1: Ragas 评估需要多少条测试数据？**

A: 最少 10 条可跑通，推荐 20-50 条有统计意义，生产环境 100+ 条。

**Q2: Faithfulness 低怎么办？**

A: 加强 Prompt 约束（「只根据资料回答」）、降低 temperature、检查检索结果是否包含所需信息。

**Q3: Context Precision 和 Recall 的区别？**

A: Precision = 检索到的有多少是相关的（查准率）。Recall = 相关的有多少被检索到（查全率）。

**Q4: Ragas 评估本身需要调 LLM，成本如何？**

A: 每条数据约 3-5 次 LLM 调用。10 条数据约 0.1-0.5 元（DeepSeek）。可接受。

**Q5: 没有 ground_truth 能评估吗？**

A: 可以。Faithfulness 和 Answer Relevancy 不需要 ground_truth。Context Precision/Recall 和 Answer Correctness 需要。

---

## 🔮 明日预习

**Day 35: LlamaIndex 框架**

- LlamaIndex vs LangChain 定位差异
- Index / Query Engine 核心概念
- 用 LlamaIndex 重建 RAG 系统
- 两个框架的选择建议

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 34*
