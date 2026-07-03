# Day 35: LlamaIndex 框架

> **零基础大模型应用开发 70 天培训课程** | 第 35/70 天 | LangChain 与 RAG 开发


——————





## 深度讲义

### 35.1 LangChain vs LlamaIndex

| 维度 | LangChain | LlamaIndex |
|------|-----------|------------|
| 定位 | 通用 LLM 应用框架 | 数据索引与 RAG 专精 |
| 优势 | 生态全、Agent 强 | RAG 开箱即用、索引丰富 |
| 适合 | Agent、复杂链 | 知识库问答、数据检索 |
| 学习曲线 | 较陡 | 较平缓 |

### 35.2 LlamaIndex 快速上手

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("公司的年假政策是什么？")
print(response)
```


## 常见错误与避坑

- ⚠️ 只看不练 — 必须动手敲代码
- ⚠️ 跳过基础直接调 API — 每天知识环环相扣
- ⚠️ 不写注释 — 企业级代码必须可读

## 课堂练习

- 📝 复习 Day 34 的核心知识点
- 📝 完成今日实操项目并提交 Git
- 📝 用 3 句话总结今天学到了什么


## 课程衔接说明



### ⬅️ 昨日回顾

**Day 34** 学习了「RAG 评估」，今天的知识直接建立在昨天之上。

### 🔗 今日定位

承接 Day 25-34 LangChain RAG，拓宽技术视野。

### ➡️ 明日预告

**Day 36** 将学习「阶段项目二（上）—— 企业级知识库问答系统」，今天务必打牢基础。


### 今日时间安排

| 时段 | 内容 |
|------|------|
| 09:00-12:00 上午 | LlamaIndex 核心概念、与 LangChain 的对比与选型 |
| 09:00-12:00 上午 | 用 LlamaIndex 快速重建知识库问答 |
| 14:00-17:30 下午 | 🛠️ 两个框架各自实现同一需求，写对比笔记 |
| 19:00-21:00 晚自习 | 整理 LangChain vs LlamaIndex 选型决策树 |



## 一、今日学习目标



完成今天的学习后，你将能够:

- LlamaIndex 核心概念、与 LangChain 的对比与选型
- 用 LlamaIndex 快速重建知识库问答

### 核心技能点

- **LlamaIndex**
- **框架选型**

### 与课程主线的关系

今天是 **第 3 阶段（LangChain 与 RAG 开发）** 的第 11 天。

> 今日主题「LlamaIndex 框架」是整条 70 天学习路径中的关键一环。请对照总路线图理解今天学什么、为什么学、后面哪里会用到。



## 二、理论精讲（纳米级拆解）


### 2.1 LlamaIndex 核心概念、与 LangChain 的对比与选型

#### 为什么需要 LangChain？

纯 API 调用的痛点:
- 多模型切换需要改大量代码
- Prompt 管理混乱
- 链式调用难以维护
- 缺少 Memory、Retriever 等开箱即用组件

#### LCEL 管道语法

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

chain = prompt | model | StrOutputParser()
result = chain.invoke({"input": "你好"})
```

#### 生态全景

- **LangChain**: 组件库 + 链式编排
- **LangGraph**: 图结构 Agent 编排
- **LangSmith**: 调试追踪平台

### 2.2 用 LlamaIndex 快速重建知识库问答

#### 核心概念

**用 LlamaIndex 快速重建知识库问答** 是今日学习的重要内容。

#### 为什么学？

在大模型应用开发中，这个知识点将在后续项目中直接用到:
- 与 Day 33 的知识形成递进
- 为 Day 38 的实操项目提供基础

#### 学习要点

1. 理解概念定义（用自己的话复述）
2. 跟着课件代码敲一遍（不要复制粘贴）
3. 完成课后练习巩固

#### 常见错误

- 只看不练 → 必须动手写代码
- 跳过基础 → 每天知识环环相扣，不要跳天

## 三、下午实操预告

今日下午核心项目: **双框架对比实现**
- 两个框架各自实现同一需求，写对比笔记



## 下午实操：项目实战



### 项目名称

**双框架对比实现**

### 推荐项目目录结构（企业级标准）

```text
day35_project/
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
# 文件名: day35_main.py
# 主题: Day 35 — 双框架对比实现
# ================================

"""
Day 35 实操项目入口。

学习要点:
1. 复习昨天所学
2. 完成今日「双框架对比实现」核心功能
3. 添加必要注释，提交 Git
"""


def main():
    """主函数 — 按今日课纲逐步实现"""
    print("Day 35: 双框架对比实现")
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
5. **提交**: `git add . && git commit -m "Day 35: 双框架对比实现"`



## 知识小测




**Q1.** 请用自己的话解释「LlamaIndex」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 32-35 所学填写）
- 后续应用: 将在 Day 42 左右用到

</details>

**Q2.** 请用自己的话解释「框架选型」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 32-35 所学填写）
- 后续应用: 将在 Day 42 左右用到

</details>


### 上机题

请不看课件，独立完成今日「实操项目」的核心功能。限时 60 分钟。



## 课后作业



### 必做

1. 完成今日实操项目「双框架对比实现」
2. 提交代码到 GitHub（commit message: `Day 35: 双框架对比实现`）
3. 在学习笔记中记录 3 个今天学到的新知识点

### 晚自习

- 整理 LangChain vs LlamaIndex 选型决策树

### 选做

1. 阅读官方文档中与今日主题相关的章节
2. 尝试优化今日代码（更优雅的错误处理、更清晰的注释）


——————

**第 35/70 天 · 零基础大模型应用开发 70 天培训课程**

> 坚持每一天，70 天后你将成为一名合格的大模型应用开发者。
