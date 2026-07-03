# Day 39: Agent 概念与 ReAct 范式

> **零基础大模型应用开发 70 天培训课程** | 第 39/70 天 | Agent 智能体开发


——————




## 本周学习路线图

> **第 7 周: Agent 基础**

```
ReAct → LangChain Agent → LangGraph → 多 Agent → MCP
                    ↓
            周末项目: 多 Agent 办公助手
```

本周每一天环环相扣，请按顺序学习，不要跳天。


## 深度讲义


### 39.1 Agent 核心概念

**Agent = LLM + 工具 + 记忆 + 规划**

```
感知(Perceive) → 思考(Think) → 行动(Act) → 观察(Observe) → 循环
```

### 39.2 ReAct 范式

```
Question: 北京和上海的人口之和是多少？

Thought 1: 我需要分别查询北京和上海的人口
Action 1: search("北京人口")
Observation 1: 北京常住人口约2185万

Thought 2: 还需要上海的人口
Action 2: search("上海人口")
Observation 2: 上海常住人口约2487万

Thought 3: 现在可以计算了
Action 3: calculator("2185 + 2487")
Observation 3: 4672

Thought 4: 我可以给出最终答案了
Answer: 北京和上海的人口之和约为4672万
```

### 39.3 手写 ReAct Agent 核心循环

```python
def react_agent(question, llm, tools, max_steps=5):
    prompt = f"问题: {question}\n"
    for step in range(max_steps):
        response = llm.generate(prompt)
        if "Answer:" in response:
            return response.split("Answer:")[-1].strip()
        if "Action:" in response:
            action = parse_action(response)
            observation = execute_tool(action, tools)
            prompt += f"\nObservation: {observation}\n"
    return "无法在限定步数内完成"
```


## 常见错误与避坑

- ⚠️ 只看不练 — 必须动手敲代码
- ⚠️ 跳过基础直接调 API — 每天知识环环相扣
- ⚠️ 不写注释 — 企业级代码必须可读

## 课堂练习

- 📝 复习 Day 38 的核心知识点
- 📝 完成今日实操项目并提交 Git
- 📝 用 3 句话总结今天学到了什么


## 课程衔接说明



### ⬅️ 昨日回顾

**Day 38** 学习了「项目答辩与代码评审」，今天的知识直接建立在昨天之上。

### 🔗 今日定位

第四阶段起点。承接 Day 19 Function Calling。

### ➡️ 明日预告

**Day 40** 将学习「LangChain Agent 与工具」，今天务必打牢基础。


### 今日时间安排

| 时段 | 内容 |
|------|------|
| 09:00-12:00 上午 | 什么是 Agent: 感知-思考-行动循环、与 Chain 的本质区别 |
| 09:00-12:00 上午 | ReAct 论文精讲(Thought → Action → Observation) |
| 14:00-17:30 下午 | 🛠️ 纯手写一个极简 ReAct Agent(理解底层原理) |
| 19:00-21:00 晚自习 | 完成「搜索 + 计算」组合任务 |



## 一、今日学习目标



完成今天的学习后，你将能够:

- 什么是 Agent: 感知-思考-行动循环、与 Chain 的本质区别
- ReAct 论文精讲(Thought → Action → Observation)

### 核心技能点

- **Agent**
- **ReAct**
- **Thought-Action-Observation**

### 与课程主线的关系

今天是 **第 4 阶段（Agent 智能体开发）** 的第 1 天。

> 今日主题「Agent 概念与 ReAct 范式」是整条 70 天学习路径中的关键一环。请对照总路线图理解今天学什么、为什么学、后面哪里会用到。



## 二、理论精讲（纳米级拆解）


### 2.1 什么是 Agent: 感知-思考-行动循环、与 Chain 的本质区别

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

### 2.2 ReAct 论文精讲(Thought → Action → Observation)

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

## 三、下午实操预告

今日下午核心项目: **手写 ReAct Agent**
- 纯手写一个极简 ReAct Agent(理解底层原理)



## 下午实操：项目实战



### 项目名称

**手写 ReAct Agent**

### 推荐项目目录结构（企业级标准）

```text
day39_project/
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
# 文件名: day39_main.py
# 主题: Day 39 — 手写 ReAct Agent
# ================================

"""
Day 39 实操项目入口。

学习要点:
1. 复习昨天所学
2. 完成今日「手写 ReAct Agent」核心功能
3. 添加必要注释，提交 Git
"""


def main():
    """主函数 — 按今日课纲逐步实现"""
    print("Day 39: 手写 ReAct Agent")
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
5. **提交**: `git add . && git commit -m "Day 39: 手写 ReAct Agent"`



## 知识小测




**Q1.** 请用自己的话解释「Agent」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 36-39 所学填写）
- 后续应用: 将在 Day 46 左右用到

</details>

**Q2.** 请用自己的话解释「ReAct」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 36-39 所学填写）
- 后续应用: 将在 Day 46 左右用到

</details>

**Q3.** 请用自己的话解释「Thought-Action-Observation」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 36-39 所学填写）
- 后续应用: 将在 Day 46 左右用到

</details>


### 上机题

请不看课件，独立完成今日「实操项目」的核心功能。限时 60 分钟。



## 课后作业



### 必做

1. 完成今日实操项目「手写 ReAct Agent」
2. 提交代码到 GitHub（commit message: `Day 39: 手写 ReAct Agent`）
3. 在学习笔记中记录 3 个今天学到的新知识点

### 晚自习

- 完成「搜索 + 计算」组合任务

### 选做

1. 阅读官方文档中与今日主题相关的章节
2. 尝试优化今日代码（更优雅的错误处理、更清晰的注释）


——————

**第 39/70 天 · 零基础大模型应用开发 70 天培训课程**

> 坚持每一天，70 天后你将成为一名合格的大模型应用开发者。
