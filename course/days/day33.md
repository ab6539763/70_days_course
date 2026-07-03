# Day 33: 高级 RAG 技术（下）

> **零基础大模型应用开发 70 天培训课程** | 第 33/70 天 | LangChain 与 RAG 开发


——————





## 深度讲义

### 33.1 混合检索

```python
# BM25 关键词检索 + 向量语义检索
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

bm25_retriever = BM25Retriever.from_documents(docs)
vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.4, 0.6],
)
```

### 33.2 Rerank

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker

reranker = CrossEncoderReranker(model="BAAI/bge-reranker-base", top_n=3)
compression_retriever = ContextualCompressionRetriever(
    base_compressor=reranker,
    base_retriever=ensemble_retriever,
)
```


## 常见错误与避坑

- ⚠️ 只看不练 — 必须动手敲代码
- ⚠️ 跳过基础直接调 API — 每天知识环环相扣
- ⚠️ 不写注释 — 企业级代码必须可读

## 课堂练习

- 📝 复习 Day 32 的核心知识点
- 📝 完成今日实操项目并提交 Git
- 📝 用 3 句话总结今天学到了什么


## 课程衔接说明



### ⬅️ 昨日回顾

**Day 32** 学习了「高级 RAG 技术（上）」，今天的知识直接建立在昨天之上。

### 🔗 今日定位

承接 Day 32，为 Day 36-37 企业级项目提供核心技术。

### ➡️ 明日预告

**Day 34** 将学习「RAG 评估」，今天务必打牢基础。


### 今日时间安排

| 时段 | 内容 |
|------|------|
| 09:00-12:00 上午 | 混合检索(BM25 + 向量检索)、RRF 融合排序 |
| 09:00-12:00 上午 | Rerank 重排序模型(bge-reranker 实战)、父文档检索器 |
| 14:00-17:30 下午 | 🛠️ 构建「混合检索 + 重排」的增强 RAG 流水线 |
| 19:00-21:00 晚自习 | 对比纯向量 vs 混合检索的 Hit@5 |



## 一、今日学习目标



完成今天的学习后，你将能够:

- 混合检索(BM25 + 向量检索)、RRF 融合排序
- Rerank 重排序模型(bge-reranker 实战)、父文档检索器

### 核心技能点

- **BM25**
- **RRF**
- **Rerank**

### 与课程主线的关系

今天是 **第 3 阶段（LangChain 与 RAG 开发）** 的第 9 天。

> 今日主题「高级 RAG 技术（下）」是整条 70 天学习路径中的关键一环。请对照总路线图理解今天学什么、为什么学、后面哪里会用到。



## 二、理论精讲（纳米级拆解）


### 2.1 混合检索(BM25 + 向量检索)、RRF 融合排序

#### RAG 完整链路

```
文档 → 加载 → 分割 → 向量化 → 存储 → 检索 → 增强生成 → 回答
```

#### 核心公式（通俗版）

> 用户问题 → 转成向量 → 在知识库中找最相似的文本块 → 塞进 Prompt → 大模型生成回答

#### 关键参数

| 参数 | 作用 | 调优建议 |
|------|------|----------|
| chunk_size | 每个文本块大小 | 300-1000 字符 |
| chunk_overlap | 块之间重叠 | chunk_size 的 10-20% |
| top_k | 检索返回数量 | 3-10 |
| similarity_threshold | 相似度阈值 | 0.5-0.8 |

### 2.2 Rerank 重排序模型(bge-reranker 实战)、父文档检索器

#### 核心概念

**Rerank 重排序模型(bge-reranker 实战)、父文档检索器** 是今日学习的重要内容。

#### 为什么学？

在大模型应用开发中，这个知识点将在后续项目中直接用到:
- 与 Day 31 的知识形成递进
- 为 Day 36 的实操项目提供基础

#### 学习要点

1. 理解概念定义（用自己的话复述）
2. 跟着课件代码敲一遍（不要复制粘贴）
3. 完成课后练习巩固

#### 常见错误

- 只看不练 → 必须动手写代码
- 跳过基础 → 每天知识环环相扣，不要跳天

## 三、下午实操预告

今日下午核心项目: **混合检索 + Rerank 流水线**
- 构建「混合检索 + 重排」的增强 RAG 流水线



## 下午实操：项目实战



### 项目名称

**混合检索 + Rerank 流水线**

### 推荐项目目录结构（企业级标准）

```text
day33_project/
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
# 文件名: day33_main.py
# 主题: Day 33 — 混合检索 + Rerank 流水线
# ================================

"""
Day 33 实操项目入口。

学习要点:
1. 复习昨天所学
2. 完成今日「混合检索 + Rerank 流水线」核心功能
3. 添加必要注释，提交 Git
"""


def main():
    """主函数 — 按今日课纲逐步实现"""
    print("Day 33: 混合检索 + Rerank 流水线")
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
5. **提交**: `git add . && git commit -m "Day 33: 混合检索 + Rerank 流水线"`



## 知识小测




**Q1.** 请用自己的话解释「BM25」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 30-33 所学填写）
- 后续应用: 将在 Day 40 左右用到

</details>

**Q2.** 请用自己的话解释「RRF」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 30-33 所学填写）
- 后续应用: 将在 Day 40 左右用到

</details>

**Q3.** 请用自己的话解释「Rerank」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 30-33 所学填写）
- 后续应用: 将在 Day 40 左右用到

</details>


### 上机题

请不看课件，独立完成今日「实操项目」的核心功能。限时 60 分钟。



## 课后作业



### 必做

1. 完成今日实操项目「混合检索 + Rerank 流水线」
2. 提交代码到 GitHub（commit message: `Day 33: 混合检索 + Rerank 流水线`）
3. 在学习笔记中记录 3 个今天学到的新知识点

### 晚自习

- 对比纯向量 vs 混合检索的 Hit@5

### 选做

1. 阅读官方文档中与今日主题相关的章节
2. 尝试优化今日代码（更优雅的错误处理、更清晰的注释）


——————

**第 33/70 天 · 零基础大模型应用开发 70 天培训课程**

> 坚持每一天，70 天后你将成为一名合格的大模型应用开发者。
