# Day 42: LangGraph 进阶

> **零基础大模型应用开发 70 天培训课程** | 第 42/70 天 | Agent 智能体开发


——————





## 深度讲义

### 42.1 Checkpointer 持久化

```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)

# 带 thread_id 运行，支持恢复
config = {"configurable": {"thread_id": "session-001"}}
result = graph.invoke(input, config)
```

### 42.2 并行节点

```python
# 多个章节并行写作
workflow.add_node("write_ch1", write_chapter_1)
workflow.add_node("write_ch2", write_chapter_2)
workflow.add_node("write_ch3", write_chapter_3)
workflow.add_node("merge", merge_chapters)

workflow.add_edge(START, "write_ch1")
workflow.add_edge(START, "write_ch2")
workflow.add_edge(START, "write_ch3")
workflow.add_edge("write_ch1", "merge")
workflow.add_edge("write_ch2", "merge")
workflow.add_edge("write_ch3", "merge")
```


## 常见错误与避坑

- ⚠️ 只看不练 — 必须动手敲代码
- ⚠️ 跳过基础直接调 API — 每天知识环环相扣
- ⚠️ 不写注释 — 企业级代码必须可读

## 课堂练习

- 📝 复习 Day 41 的核心知识点
- 📝 完成今日实操项目并提交 Git
- 📝 用 3 句话总结今天学到了什么


## 课程衔接说明



### ⬅️ 昨日回顾

**Day 41** 学习了「LangGraph 入门（重点！）」，今天的知识直接建立在昨天之上。

### 🔗 今日定位

承接 Day 41，为项目三的中断恢复能力做准备。

### ➡️ 明日预告

**Day 43** 将学习「多 Agent 系统」，今天务必打牢基础。


### 今日时间安排

| 时段 | 内容 |
|------|------|
| 09:00-12:00 上午 | 持久化(Checkpointer)、中断与恢复(Human-in-the-loop) |
| 09:00-12:00 上午 | 子图、并行节点、错误重试策略 |
| 14:00-17:30 下午 | 🛠️ 构建「写作 Agent」: 大纲 → 分章节并行写作 → 汇总润色 |
| 19:00-21:00 晚自习 | 测试中断恢复流程 |



## 一、今日学习目标



完成今天的学习后，你将能够:

- 持久化(Checkpointer)、中断与恢复(Human-in-the-loop)
- 子图、并行节点、错误重试策略

### 核心技能点

- **Checkpointer**
- **并行节点**
- **重试策略**

### 与课程主线的关系

今天是 **第 4 阶段（Agent 智能体开发）** 的第 4 天。

> 今日主题「LangGraph 进阶」是整条 70 天学习路径中的关键一环。请对照总路线图理解今天学什么、为什么学、后面哪里会用到。



## 二、理论精讲（纳米级拆解）


### 2.1 持久化(Checkpointer)、中断与恢复(Human-in-the-loop)

#### 核心概念

**持久化(Checkpointer)、中断与恢复(Human-in-the-loop)** 是今日学习的重要内容。

#### 为什么学？

在大模型应用开发中，这个知识点将在后续项目中直接用到:
- 与 Day 40 的知识形成递进
- 为 Day 45 的实操项目提供基础

#### 学习要点

1. 理解概念定义（用自己的话复述）
2. 跟着课件代码敲一遍（不要复制粘贴）
3. 完成课后练习巩固

#### 常见错误

- 只看不练 → 必须动手写代码
- 跳过基础 → 每天知识环环相扣，不要跳天

### 2.2 子图、并行节点、错误重试策略

#### 核心概念

**子图、并行节点、错误重试策略** 是今日学习的重要内容。

#### 为什么学？

在大模型应用开发中，这个知识点将在后续项目中直接用到:
- 与 Day 40 的知识形成递进
- 为 Day 45 的实操项目提供基础

#### 学习要点

1. 理解概念定义（用自己的话复述）
2. 跟着课件代码敲一遍（不要复制粘贴）
3. 完成课后练习巩固

#### 常见错误

- 只看不练 → 必须动手写代码
- 跳过基础 → 每天知识环环相扣，不要跳天

## 三、下午实操预告

今日下午核心项目: **写作 Agent 工作流**
- 构建「写作 Agent」: 大纲 → 分章节并行写作 → 汇总润色



## 下午实操：项目实战



### 项目名称

**写作 Agent 工作流**

### 推荐项目目录结构（企业级标准）

```text
day42_project/
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
# 文件名: day42_main.py
# 主题: Day 42 — 写作 Agent 工作流
# ================================

"""
Day 42 实操项目入口。

学习要点:
1. 复习昨天所学
2. 完成今日「写作 Agent 工作流」核心功能
3. 添加必要注释，提交 Git
"""


def main():
    """主函数 — 按今日课纲逐步实现"""
    print("Day 42: 写作 Agent 工作流")
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
5. **提交**: `git add . && git commit -m "Day 42: 写作 Agent 工作流"`



## 知识小测




**Q1.** 请用自己的话解释「Checkpointer」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 39-42 所学填写）
- 后续应用: 将在 Day 49 左右用到

</details>

**Q2.** 请用自己的话解释「并行节点」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 39-42 所学填写）
- 后续应用: 将在 Day 49 左右用到

</details>

**Q3.** 请用自己的话解释「重试策略」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 39-42 所学填写）
- 后续应用: 将在 Day 49 左右用到

</details>


### 上机题

请不看课件，独立完成今日「实操项目」的核心功能。限时 60 分钟。



## 课后作业



### 必做

1. 完成今日实操项目「写作 Agent 工作流」
2. 提交代码到 GitHub（commit message: `Day 42: 写作 Agent 工作流`）
3. 在学习笔记中记录 3 个今天学到的新知识点

### 晚自习

- 测试中断恢复流程

### 选做

1. 阅读官方文档中与今日主题相关的章节
2. 尝试优化今日代码（更优雅的错误处理、更清晰的注释）


——————

**第 42/70 天 · 零基础大模型应用开发 70 天培训课程**

> 坚持每一天，70 天后你将成为一名合格的大模型应用开发者。
