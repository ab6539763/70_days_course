# Day 25: LangChain 入门

> **零基础大模型应用开发 70 天培训课程** | 第 25/70 天 | LangChain 与 RAG 开发


——————




## 本周学习路线图

> **第 5 周: LangChain 框架**

```
LangChain 入门 → LCEL → Memory → 文档分割 → 向量库
                    ↓
            周末项目: 企业知识库问答
```

本周每一天环环相扣，请按顺序学习，不要跳天。



## 深度讲义

### 25.1 LangChain 统一模型调用

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是助手"),
    ("user", "{input}"),
])
chain = prompt | llm | StrOutputParser()
result = chain.invoke({"input": "你好"})
```

### 25.2 为什么需要框架？

| 纯 API | LangChain |
|--------|-----------|
| 手动拼 JSON | 统一 ChatModel 接口 |
| 手动管理 messages | 内置 Memory |
| 手动解析输出 | OutputParser |
| 难以切换模型 | 一行代码切换 |


## 常见错误与避坑

- ⚠️ 只看不练 — 必须动手敲代码
- ⚠️ 跳过基础直接调 API — 每天知识环环相扣
- ⚠️ 不写注释 — 企业级代码必须可读

## 课堂练习

- 📝 复习 Day 24 的核心知识点
- 📝 完成今日实操项目并提交 Git
- 📝 用 3 句话总结今天学到了什么


## 课程衔接说明



### ⬅️ 昨日回顾

**Day 24** 学习了「FastAPI 后端开发（下）+ 数据库」，今天的知识直接建立在昨天之上。

### 🔗 今日定位

第三阶段起点。承接 Day 9 多模型类和 Day 14 对话项目。

### ➡️ 明日预告

**Day 26** 将学习「LCEL 表达式与链」，今天务必打牢基础。


### 今日时间安排

| 时段 | 内容 |
|------|------|
| 09:00-12:00 上午 | LangChain 架构总览、为什么需要框架、生态介绍(LangChain/LangGraph/LangSmith) |
| 09:00-12:00 上午 | ChatModel 接口、统一调用不同厂商模型、PromptTemplate / ChatPromptTemplate |
| 14:00-17:30 下午 | 🛠️ 用 LangChain 重写之前的对话应用 |
| 19:00-21:00 晚自习 | 对比纯 API 版与 LangChain 版代码量 |



## 一、今日学习目标



完成今天的学习后，你将能够:

- LangChain 架构总览、为什么需要框架、生态介绍(LangChain/LangGraph/LangSmith)
- ChatModel 接口、统一调用不同厂商模型、PromptTemplate / ChatPromptTemplate

### 核心技能点

- **LangChain**
- **ChatModel**
- **PromptTemplate**

### 与课程主线的关系

今天是 **第 3 阶段（LangChain 与 RAG 开发）** 的第 1 天。

> 今日主题「LangChain 入门」是整条 70 天学习路径中的关键一环。请对照总路线图理解今天学什么、为什么学、后面哪里会用到。



## 二、理论精讲（纳米级拆解）


### 2.1 LangChain 架构总览、为什么需要框架、生态介绍(LangChain/LangGraph/LangSmith)

#### Agent vs Chain

| | Chain | Agent |
|---|-------|-------|
| 执行方式 | 固定步骤 | 自主决策 |
| 灵活性 | 低 | 高 |
| 适用场景 | 翻译、摘要 | 复杂任务、多步推理 |

#### ReAct 循环

```
Thought（思考）→ Action（行动）→ Observation（观察）→ Thought → ...
```

#### 核心组件

1. **LLM**: 大脑，负责推理
2. **Tools**: 手脚，负责执行（搜索、计算、查数据库）
3. **Memory**: 记忆，维护上下文
4. **Planner**: 规划器（LangGraph 中实现）

### 2.2 ChatModel 接口、统一调用不同厂商模型、PromptTemplate / ChatPromptTemplate

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

今日下午核心项目: **LangChain 对话应用**
- 用 LangChain 重写之前的对话应用



## 下午实操：项目实战



### 项目名称

**LangChain 对话应用**

### 推荐项目目录结构（企业级标准）

```text
day25_project/
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
# 文件名: day25_main.py
# 主题: Day 25 — LangChain 对话应用
# ================================

"""
Day 25 实操项目入口。

学习要点:
1. 复习昨天所学
2. 完成今日「LangChain 对话应用」核心功能
3. 添加必要注释，提交 Git
"""


def main():
    """主函数 — 按今日课纲逐步实现"""
    print("Day 25: LangChain 对话应用")
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
5. **提交**: `git add . && git commit -m "Day 25: LangChain 对话应用"`



## 知识小测




**Q1.** 请用自己的话解释「LangChain」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 22-25 所学填写）
- 后续应用: 将在 Day 32 左右用到

</details>

**Q2.** 请用自己的话解释「ChatModel」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 22-25 所学填写）
- 后续应用: 将在 Day 32 左右用到

</details>

**Q3.** 请用自己的话解释「PromptTemplate」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 22-25 所学填写）
- 后续应用: 将在 Day 32 左右用到

</details>


### 上机题

请不看课件，独立完成今日「实操项目」的核心功能。限时 60 分钟。



## 课后作业



### 必做

1. 完成今日实操项目「LangChain 对话应用」
2. 提交代码到 GitHub（commit message: `Day 25: LangChain 对话应用`）
3. 在学习笔记中记录 3 个今天学到的新知识点

### 晚自习

- 对比纯 API 版与 LangChain 版代码量

### 选做

1. 阅读官方文档中与今日主题相关的章节
2. 尝试优化今日代码（更优雅的错误处理、更清晰的注释）


——————

**第 25/70 天 · 零基础大模型应用开发 70 天培训课程**

> 坚持每一天，70 天后你将成为一名合格的大模型应用开发者。
