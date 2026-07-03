# Day 30: 完整 RAG 系统搭建（核心日！）

> **零基础大模型应用开发 70 天培训课程** | 第 30/70 天 | LangChain 与 RAG 开发


——————




## 深度讲义


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
RAG_PROMPT = """
你是一个企业知识库助手。请基于以下检索到的上下文回答用户问题。

规则:
1. 只根据上下文回答，不要编造
2. 如果上下文不足以回答，说"我不知道"
3. 在回答末尾标注引用来源

上下文:
{context}

用户问题: {question}

回答:
"""
```

### 30.3 兜底策略

```python
def answer_with_fallback(question, retriever, llm, threshold=0.5):
    docs = retriever.get_relevant_documents(question)
    if not docs or docs[0].metadata.get("score", 1) < threshold:
        return "抱歉，我在知识库中没有找到相关信息。请尝试换个问法或联系人工客服。"
    # 正常 RAG 流程...
```


## 完整项目代码（可直接运行）

### 文件: `day30_rag_qa.py`

```python
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
        return "\n".join(f"- {d.page_content}" for d in docs)

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
        q = input("\n请输入问题 (quit退出): ").strip()
        if q.lower() == "quit":
            break
        answer = chain.invoke(q)
        print(f"\n回答: {answer}")


if __name__ == "__main__":
    main()
```

### 运行步骤

```bash
cd course/code/day30
pip install -r requirements.txt  # 如有依赖
python day30_rag_qa.py
```


## 常见错误与避坑

- ⚠️ 只看不练 — 必须动手敲代码
- ⚠️ 跳过基础直接调 API — 每天知识环环相扣
- ⚠️ 不写注释 — 企业级代码必须可读

## 课堂练习

- 📝 复习 Day 29 的核心知识点
- 📝 完成今日实操项目并提交 Git
- 📝 用 3 句话总结今天学到了什么


## 课程衔接说明



### ⬅️ 昨日回顾

**Day 29** 学习了「向量数据库」，今天的知识直接建立在昨天之上。

### 🔗 今日定位

RAG 核心日。能力将扩展到 Day 32-37 进阶项目。

### ➡️ 明日预告

**Day 31** 将学习「周测 + RAG 效果调优实验日」，今天务必打牢基础。


### 今日时间安排

| 时段 | 内容 |
|------|------|
| 09:00-12:00 上午 | RAG 完整链路: 加载 → 分割 → 向量化 → 存储 → 检索 → 增强生成 |
| 09:00-12:00 上午 | RAG Prompt 模板设计、引用来源标注、'我不知道'的兜底处理 |
| 14:00-17:30 下午 | 🛠️ 搭建一个完整的企业知识库问答系统（命令行版） |
| 19:00-21:00 晚自习 | 测试 10 个问题并记录回答质量 |



## 一、今日学习目标



完成今天的学习后，你将能够:

- RAG 完整链路: 加载 → 分割 → 向量化 → 存储 → 检索 → 增强生成
- RAG Prompt 模板设计、引用来源标注、'我不知道'的兜底处理

### 核心技能点

- **RAG 全链路**
- **引用溯源**
- **兜底策略**

### 与课程主线的关系

今天是 **第 3 阶段（LangChain 与 RAG 开发）** 的第 6 天。

> 今日主题「完整 RAG 系统搭建（核心日！）」是整条 70 天学习路径中的关键一环。请对照总路线图理解今天学什么、为什么学、后面哪里会用到。



## 二、理论精讲（纳米级拆解）


### 2.1 RAG 完整链路: 加载 → 分割 → 向量化 → 存储 → 检索 → 增强生成

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

### 2.2 RAG Prompt 模板设计、引用来源标注、'我不知道'的兜底处理

#### Prompt 设计四要素

| 要素 | 说明 | 示例 |
|------|------|------|
| 指令 | 告诉模型做什么 | "请将以下文本翻译成英文" |
| 上下文 | 背景信息 | "这是一份医疗科普文章" |
| 输入 | 待处理内容 | 用户提供的原文 |
| 输出格式 | 约束返回形式 | "请以 JSON 格式返回" |

#### Zero-shot vs Few-shot

```python
# Zero-shot: 直接给指令
prompt_zero = "判断以下评论的情感（正面/负面）: 这个产品太好用了！"

# Few-shot: 给几个示例
prompt_few = '''
判断评论情感，示例:
评论: 太差了 → 负面
评论: 非常满意 → 正面
评论: 这个产品太好用了！ →
'''
```

#### 与大模型岗位的关系

Prompt 工程是大模型应用开发**第一天就要用、每一天都在用**的技能。

## 三、下午实操预告

今日下午核心项目: **企业知识库问答系统（命令行版）**
- 搭建一个完整的企业知识库问答系统（命令行版）



## 下午实操：项目实战



### 项目名称

**企业知识库问答系统（命令行版）**

### 推荐项目目录结构（企业级标准）

```text
day30_project/
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
# 文件名: day30_main.py
# 主题: Day 30 — 企业知识库问答系统（命令行版）
# ================================

"""
Day 30 实操项目入口。

学习要点:
1. 复习昨天所学
2. 完成今日「企业知识库问答系统（命令行版）」核心功能
3. 添加必要注释，提交 Git
"""


def main():
    """主函数 — 按今日课纲逐步实现"""
    print("Day 30: 企业知识库问答系统（命令行版）")
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
5. **提交**: `git add . && git commit -m "Day 30: 企业知识库问答系统（命令行版）"`



## 知识小测




**Q1.** 请用自己的话解释「RAG 全链路」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 27-30 所学填写）
- 后续应用: 将在 Day 37 左右用到

</details>

**Q2.** 请用自己的话解释「引用溯源」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 27-30 所学填写）
- 后续应用: 将在 Day 37 左右用到

</details>

**Q3.** 请用自己的话解释「兜底策略」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 27-30 所学填写）
- 后续应用: 将在 Day 37 左右用到

</details>


### 上机题

请不看课件，独立完成今日「实操项目」的核心功能。限时 60 分钟。



## 课后作业



### 必做

1. 完成今日实操项目「企业知识库问答系统（命令行版）」
2. 提交代码到 GitHub（commit message: `Day 30: 企业知识库问答系统（命令行版）`）
3. 在学习笔记中记录 3 个今天学到的新知识点

### 晚自习

- 测试 10 个问题并记录回答质量

### 选做

1. 阅读官方文档中与今日主题相关的章节
2. 尝试优化今日代码（更优雅的错误处理、更清晰的注释）


——————

**第 30/70 天 · 零基础大模型应用开发 70 天培训课程**

> 坚持每一天，70 天后你将成为一名合格的大模型应用开发者。
