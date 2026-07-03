# Day 39: Agent 概念与 ReAct

> **培训阶段**: 第四阶段 Agent 开发 | **第 7 周** | **学习时长**: 约 6-8 小时  
> **今日关键词**: Agent、ReAct、Thought-Action-Observation、工具调用、自主推理

---

## 📍 课程导航

### 上节回顾

在 **Day 38** 中，你完成了 RAG 阶段的综合项目与复盘，掌握了检索增强生成的完整链路：文档加载 → 分块 → 向量化 → 检索 → 重排序 → 生成。RAG 解决了「知识从哪来」的问题，但面对需要**多步推理、调用外部工具、动态决策**的复杂任务，单纯的 RAG 链式调用就显得力不从心了。

**Day 38 核心收获回顾：**
- 构建了完整的 RAG 应用（知识库问答 + 引用溯源）
- 理解了 RAG 的局限：无法执行操作、无法多步规划
- 为 Agent 阶段打下了检索与 Prompt 工程的基础

### 本节学习目标

完成本日学习后，你将能够：

1. 理解 Agent 与传统 LLM 应用（Prompt / RAG / Chain）的本质区别
2. 掌握 ReAct（Reasoning + Acting）框架的核心思想与执行循环
3. 手写一个最小可用的 ReAct Agent（不依赖框架）
4. 理解 Tool、Action、Observation 的设计原则
5. 分析 Agent 失败模式并设计基础防护策略
6. 为 Day 40 的 LangChain Agent 框架学习做好准备

### 与后续课程的衔接

- **Day 40** 将使用 LangChain 的 `create_react_agent` 和 `@tool` 装饰器，把今天手写的逻辑框架化
- **Day 41-42** 将用 LangGraph 实现更复杂的状态机与循环控制——ReAct 是 LangGraph 节点的典型模式
- **Day 43** 多 Agent 系统中，每个子 Agent 内部仍遵循 ReAct 循环
- **Day 48-49** 阶段项目三将综合运用 RAG + Agent，今天学的 ReAct 是项目核心架构

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：什么是 Agent？

#### 1.1 从 Chain 到 Agent 的演进

在大模型应用开发中，我们经历了三个阶段的演进：

```
阶段 1: Prompt 工程（Day 15-19）
  用户提问 → 单次 LLM 调用 → 返回答案

阶段 2: RAG / Chain（Day 25-38）
  用户提问 → 检索知识库 → 拼接上下文 → LLM 生成

阶段 3: Agent（Day 39 起）← 今天
  用户提问 → LLM 思考 → 选择工具 → 执行 → 观察结果 → 再思考 → ... → 最终答案
```

**Agent 的定义**

> Agent（智能体）= LLM（大脑）+ 工具（手脚）+ 记忆（经验）+ 规划（策略）

与传统应用的核心区别：

| 维度 | RAG / Chain | Agent |
|------|-------------|-------|
| 决策权 | 开发者预设流程 | LLM 自主决定下一步 |
| 工具使用 | 固定调用顺序 | 动态选择工具 |
| 错误处理 | 通常直接失败 | 可观察错误并重试 |
| 任务复杂度 | 单步或固定多步 | 开放域多步推理 |
| 可控性 | 高 | 需要额外工程化（Day 46） |

#### 1.2 Agent 的核心组件

```
┌─────────────────────────────────────────────────────┐
│                    Agent 系统                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │  LLM     │  │  Tools   │  │  Memory  │          │
│  │  推理引擎 │  │  外部能力 │  │  上下文   │          │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘          │
│       │             │             │                 │
│       └─────────────┼─────────────┘                 │
│                     ▼                               │
│              ┌──────────────┐                       │
│              │   Planner    │                       │
│              │  规划与决策   │                       │
│              └──────────────┘                       │
└─────────────────────────────────────────────────────┘
```

**四大组件详解：**

1. **LLM（大脑）**：负责理解任务、推理决策、生成行动计划
2. **Tools（工具）**：搜索引擎、计算器、数据库、API、代码执行器等
3. **Memory（记忆）**：短期（对话历史）、长期（向量存储的用户偏好）
4. **Planner（规划器）**：决定何时停止、何时调用哪个工具（ReAct 是最经典的规划模式）

#### 1.3 Agent 的典型应用场景

| 场景 | 为什么需要 Agent | 示例工具 |
|------|------------------|----------|
| 数据分析助手 | 需要多步查询、计算、可视化 | SQL、Python、图表 API |
| 客服机器人 | 需要查订单、改地址、退款 | CRM API、支付 API |
| 代码助手 | 需要读文件、运行测试、修复 | 文件系统、终端、Git |
| 研究助手 | 需要搜索、阅读、总结、引用 | 搜索 API、RAG、浏览器 |
| 办公自动化 | 需要发邮件、建日程、填表格 | Gmail、Calendar、Excel |

> 💡 **关键洞察**：不是所有任务都需要 Agent。如果任务流程固定（如固定 RAG 问答），用 Chain 更简单、更稳定、更便宜。Agent 适合**流程不确定、需要动态决策**的场景。

#### 1.4 Agent 的挑战与风险

在进入实战前，必须正视 Agent 的固有挑战（Day 46 将深入工程化解决方案）：

| 挑战 | 表现 | 初步应对 |
|------|------|----------|
| 幻觉行动 | 调用不存在的工具 | 工具白名单校验 |
| 无限循环 | 反复调用同一工具 | 最大步数限制 |
| 成本失控 | 多轮 LLM 调用 | Token 预算、早停 |
| 安全风险 | 执行危险命令 | 沙箱、权限隔离 |
| 不可预测 | 同样输入不同输出 | 日志、评估、人工审核 |

---

### 9:45 - 10:30 | 模块二：ReAct 框架深度解析

#### 2.1 ReAct 论文背景

ReAct 由 Yao et al. 在 2022 年提出（论文：*ReAct: Synergizing Reasoning and Acting in Language Models*），核心思想是：

> 让 LLM **交替进行推理（Reasoning）和行动（Acting）**，而不是先想完再做，或先做再想。

**为什么「交替」更好？**

```
纯推理（Chain-of-Thought）：
  问题 → 思考思考思考... → 答案
  缺点：无法获取外部信息，容易幻觉

纯行动（Action-only）：
  问题 → 行动行动行动... → 答案
  缺点：缺乏全局规划，容易走弯路

ReAct（推理 + 行动交替）：
  问题 → 思考 → 行动 → 观察 → 思考 → 行动 → 观察 → ... → 答案
  优点：推理指导行动，观察修正推理
```

#### 2.2 ReAct 循环详解

```
用户输入: "北京今天天气怎么样？如果下雨，推荐室内活动"

┌─────────────────────────────────────────────────────────┐
│ Thought 1: 我需要先查询北京今天的天气                    │
│ Action 1:  search_weather                             │
│ Action Input 1: {"city": "北京"}                      │
│ Observation 1: 北京今天多云，下午有雷阵雨，气温 28°C     │
├─────────────────────────────────────────────────────────┤
│ Thought 2: 天气预报有雷阵雨，属于下雨天气，需要推荐室内活动 │
│ Action 2:  search_activities                          │
│ Action Input 2: {"city": "北京", "type": "室内"}       │
│ Observation 2: 国家博物馆、798艺术区、三里屯书店...      │
├─────────────────────────────────────────────────────────┤
│ Thought 3: 我已经获取了天气和活动信息，可以给出完整回答了  │
│ Final Answer: 北京今天有雷阵雨...推荐您去国家博物馆...   │
└─────────────────────────────────────────────────────────┘
```

**三个关键元素：**

| 元素 | 格式 | 作用 |
|------|------|------|
| Thought | 自然语言推理 | 解释当前策略和下一步计划 |
| Action | 工具名称 + 输入 | 执行具体操作 |
| Observation | 工具返回结果 | 为下一轮 Thought 提供事实依据 |

#### 2.3 ReAct Prompt 模板设计

标准的 ReAct Prompt 结构：

```python
REACT_PROMPT = """你是一个有用的 AI 助手，可以使用以下工具来回答问题。

可用工具：
{tool_descriptions}

请严格按照以下格式回答：

Question: 用户的问题
Thought: 你对当前情况的分析和下一步计划
Action: 要使用的工具名称（必须是 [{tool_names}] 之一）
Action Input: 工具的输入参数（JSON 格式）
Observation: 工具返回的结果（由系统填充，你不要生成）
... (Thought/Action/Action Input/Observation 可以重复 N 次)
Thought: 我现在知道最终答案了
Final Answer: 给用户的最终回答

重要规则：
1. 每次只能调用一个工具
2. Action 必须是可用工具之一，不要编造工具名
3. 如果不需要工具就能回答，直接给出 Final Answer
4. 最多执行 {max_iterations} 轮

开始！

Question: {question}
Thought:"""
```

#### 2.4 停止条件设计

Agent 循环何时结束？

```python
# 停止条件（按优先级）
STOP_CONDITIONS = [
    "LLM 输出包含 'Final Answer:'",      # 正常完成
    "达到最大迭代次数 max_iterations",    # 防止无限循环
    "连续 N 次调用同一工具",              # 检测死循环
    "工具执行抛出不可恢复异常",            # 错误兜底
    "累计 Token 超过预算",                # 成本控制
]
```

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：手写 ReAct Agent 原理

#### 3.1 最小 Agent 架构

```python
"""
Day 39: 手写 ReAct Agent（教学版，不依赖框架）
文件: day39/react_agent.py
"""

import re
import json
from typing import Callable

# ===== 工具定义 =====
def calculator(expression: str) -> str:
    """安全计算器：仅支持基本四则运算"""
    allowed = set("0123456789+-*/.() ")
    if not all(c in allowed for c in expression):
        return "错误：表达式包含不允许的字符"
    try:
        result = eval(expression)  # 教学用，生产环境需更安全方案
        return str(result)
    except Exception as e:
        return f"计算错误: {e}"

def search_knowledge(query: str) -> str:
    """模拟知识库搜索（Day 38 RAG 的简化版）"""
    knowledge_base = {
        "python": "Python 是一种高级编程语言，由 Guido van Rossum 于 1991 年发布。",
        "langchain": "LangChain 是一个用于开发 LLM 应用的框架，支持 Chain、Agent、RAG 等模式。",
        "react": "ReAct 是一种让 LLM 交替进行推理和行动的框架，由 Yao et al. 2022 年提出。",
        "agent": "Agent 是大模型应用的高级形态，具备自主规划和使用工具的能力。",
    }
    query_lower = query.lower()
    for key, value in knowledge_base.items():
        if key in query_lower:
            return value
    return f"未找到关于 '{query}' 的信息"

# 工具注册表
TOOLS: dict[str, Callable] = {
    "calculator": calculator,
    "search_knowledge": search_knowledge,
}

TOOL_DESCRIPTIONS = """
- calculator: 计算数学表达式。输入: 数学表达式字符串，如 "2+3*4"
- search_knowledge: 搜索知识库。输入: 搜索关键词，如 "python"
""".strip()
```

#### 3.2 Agent 主循环实现

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

def call_llm(prompt: str) -> str:
    """调用大模型 API"""
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return response.choices[0].message.content

def parse_action(text: str) -> tuple[str, str] | None:
    """从 LLM 输出中解析 Action 和 Action Input"""
    action_match = re.search(r"Action:\s*(\w+)", text)
    input_match = re.search(r"Action Input:\s*(.+?)(?:\n|$)", text, re.DOTALL)
    if action_match:
        action = action_match.group(1).strip()
        action_input = input_match.group(1).strip() if input_match else ""
        # 清理 JSON 引号
        action_input = action_input.strip('"').strip("'")
        return action, action_input
    return None

def run_react_agent(question: str, max_iterations: int = 5) -> str:
    """ReAct Agent 主循环"""
    tool_names = ", ".join(TOOLS.keys())
    
    prompt = f"""你是一个有用的 AI 助手，可以使用以下工具：

{TOOL_DESCRIPTIONS}

可用工具名: [{tool_names}]

请严格按以下格式回答：
Thought: [你的推理]
Action: [工具名]
Action Input: [工具输入]
Observation: [系统填充，你不要写]

或者当你有足够信息时：
Thought: 我现在知道最终答案了
Final Answer: [最终回答]

Question: {question}
"""
    
    history = prompt
    
    for i in range(max_iterations):
        print(f"\n{'='*50}")
        print(f"第 {i+1} 轮迭代")
        print(f"{'='*50}")
        
        # 调用 LLM
        response = call_llm(history + "\nThought:")
        print(response)
        history += "\nThought:" + response
        
        # 检查是否完成
        if "Final Answer:" in response:
            final = re.search(r"Final Answer:\s*(.+)", response, re.DOTALL)
            return final.group(1).strip() if final else response
        
        # 解析并执行 Action
        parsed = parse_action(response)
        if parsed is None:
            history += "\nObservation: 格式错误，请按 Thought/Action/Action Input 格式回答"
            continue
        
        action, action_input = parsed
        if action not in TOOLS:
            observation = f"错误：工具 '{action}' 不存在。可用工具: {tool_names}"
        else:
            print(f"\n>>> 执行工具: {action}({action_input})")
            observation = TOOLS[action](action_input)
            print(f">>> 观察结果: {observation}")
        
        history += f"\nObservation: {observation}"
    
    return "抱歉，在最大迭代次数内未能完成任务。"


if __name__ == "__main__":
    # 测试用例
    questions = [
        "ReAct 框架是什么时候提出的？",
        "计算 (15 + 25) * 3 等于多少？",
        "LangChain 是什么？它和 Agent 有什么关系？",
    ]
    
    for q in questions:
        print(f"\n\n{'#'*60}")
        print(f"问题: {q}")
        print(f"{'#'*60}")
        answer = run_react_agent(q)
        print(f"\n✅ 最终答案: {answer}")
```

#### 3.3 运行前准备

```bash
# 创建项目目录
mkdir -p ~/llm-course/day39
cd ~/llm-course/day39

# 安装依赖
pip install openai

# 配置 API Key（使用 Day 12 配置的 DeepSeek Key）
export DEEPSEEK_API_KEY="your-api-key-here"

# 运行
python react_agent.py
```

#### 3.4 预期输出示例

```
############################################################
问题: 计算 (15 + 25) * 3 等于多少？
############################################################

==================================================
第 1 轮迭代
==================================================
我需要计算这个数学表达式
Action: calculator
Action Input: (15 + 25) * 3

>>> 执行工具: calculator((15 + 25) * 3)
>>> 观察结果: 120

==================================================
第 2 轮迭代
==================================================
计算结果是 120，我可以给出最终答案了
Final Answer: (15 + 25) * 3 = 120

✅ 最终答案: (15 + 25) * 3 = 120
```

---

## 🌇 下午实操（14:00 - 17:30）

### 14:00 - 15:30 | 实操项目：扩展 ReAct Agent 工具集

#### 项目需求

在上午的基础 Agent 上，扩展以下能力：

1. **新增 `get_current_time` 工具**：返回当前日期时间
2. **新增 `web_search` 工具**：模拟网页搜索（可用固定数据模拟）
3. **改进 Prompt**：支持中文问答，优化工具选择准确率
4. **添加日志**：将每轮 Thought/Action/Observation 写入 `agent_log.txt`

#### 参考代码：扩展工具

```python
# day39/extended_tools.py

from datetime import datetime

def get_current_time(dummy: str = "") -> str:
    """获取当前日期时间"""
    now = datetime.now()
    return now.strftime("%Y年%m月%d日 %H:%M:%S")

def web_search(query: str) -> str:
    """模拟网页搜索（生产环境替换为真实搜索 API）"""
    mock_results = {
        "天气": "北京今天晴，气温 15-25°C，空气质量良。",
        "新闻": "2026年7月3日科技要闻：大模型 Agent 技术持续升温。",
        "股价": "示例公司(ABC)当前股价 128.50 元，涨幅 +2.3%。",
    }
    for keyword, result in mock_results.items():
        if keyword in query:
            return result
    return f"搜索 '{query}' 未找到相关结果，请尝试其他关键词。"

# 日志工具
class AgentLogger:
    def __init__(self, log_file: str = "agent_log.txt"):
        self.log_file = log_file
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write(f"=== Agent 运行日志 {datetime.now()} ===\n\n")
    
    def log(self, iteration: int, thought: str, action: str = "", 
            action_input: str = "", observation: str = ""):
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"--- 第 {iteration} 轮 ---\n")
            f.write(f"Thought: {thought}\n")
            if action:
                f.write(f"Action: {action}\n")
                f.write(f"Action Input: {action_input}\n")
            if observation:
                f.write(f"Observation: {observation}\n")
            f.write("\n")
```

#### 项目验收标准

| 验收项 | 标准 |
|--------|------|
| 工具调用 | 3 个以上工具均可被正确调用 |
| 多步推理 | 能完成需要 2+ 步的任务 |
| 错误处理 | 调用不存在工具时给出友好提示 |
| 日志完整 | agent_log.txt 记录完整执行过程 |
| 代码规范 | 有注释、有类型提示、可独立运行 |

---

### 15:30 - 15:45 | 课间休息

---

### 15:45 - 17:30 | 扩展练习：Agent 调试与 Prompt 优化

#### 练习 1：Prompt 变体对比

测试不同 Prompt 策略对 Agent 行为的影响：

```python
# 策略 A：强调逐步思考
PROMPT_A = "在每一步都要仔细思考，确保选择正确的工具..."

# 策略 B：提供 Few-shot 示例
PROMPT_B = """
示例：
Question: 1+1等于几？
Thought: 这是简单计算，用计算器
Action: calculator
Action Input: 1+1
Observation: 2
Thought: 我知道答案了
Final Answer: 1+1=2

现在请回答：
Question: {question}
"""

# 策略 C：限制工具使用场景
PROMPT_C = """
工具使用规则：
- 纯数学计算 → 必须用 calculator
- 概念/知识问题 → 必须用 search_knowledge
- 时间相关问题 → 必须用 get_current_time
"""
```

记录每种策略在 5 个测试问题上的成功率和平均迭代次数。

#### 练习 2：死循环检测

```python
def detect_loop(action_history: list[str], threshold: int = 3) -> bool:
    """检测是否陷入死循环：连续调用同一工具"""
    if len(action_history) < threshold:
        return False
    recent = action_history[-threshold:]
    return len(set(recent)) == 1  # 最近 N 次都是同一工具

# 在 Agent 主循环中使用
action_history = []
# ... 每次执行 action 后
action_history.append(action)
if detect_loop(action_history):
    return "检测到可能的死循环，已终止执行。"
```

#### 练习 3：与 RAG 结合思考

设计一个混合架构（为 Day 48 项目预热）：

```
用户问题
    │
    ▼
┌─────────────┐     是      ┌─────────────┐
│ 需要实时信息？├────────────►│ ReAct Agent │
└──────┬──────┘             └─────────────┘
       │ 否
       ▼
┌─────────────┐
│  RAG 检索   │  ← Day 38 的知识库
└─────────────┘
```

思考：什么类型的问题走 RAG？什么类型走 Agent？写 5 个例子分类。

---

## 🌙 晚自习（19:00 - 21:00）

### 19:00 - 20:00 | 阅读与拓展

#### 必读材料

1. **ReAct 论文摘要**：https://arxiv.org/abs/2210.03629
   - 重点阅读 Section 3（ReAct Prompting）和 Figure 1
2. **LangChain Agent 概念文档**（预习 Day 40）：https://python.langchain.com/docs/concepts/agents/
3. **Andrew Ng 的 Agentic AI 课程**（选修）：了解行业对 Agent 的定义

#### 思考题

1. ReAct 和 Chain-of-Thought 的本质区别是什么？
2. 为什么 Agent 需要 `temperature=0`？如果用 0.7 会怎样？
3. 你写的 Agent 在哪些问题上失败了？如何改进 Prompt？

### 20:00 - 21:00 | 自习答疑

- 确保 `react_agent.py` 三个测试用例全部通过
- 完成扩展工具项目
- 预习 Day 40 LangChain Agent 文档
- Git 提交：`git commit -m "Day 39: ReAct Agent 手写实现"`

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | Agent 与 Chain/RAG 的区别 | |
| 2 | Agent 四大组件（LLM/Tools/Memory/Planner） | |
| 3 | ReAct 框架 Thought-Action-Observation 循环 | |
| 4 | ReAct Prompt 模板设计 | |
| 5 | Agent 停止条件与死循环防护 | |
| 6 | 手写 ReAct Agent 主循环 | |
| 7 | 工具注册与解析 Action 输出 | |
| 8 | Agent 日志与调试方法 | |
| 9 | Agent 适用场景判断 | |
| 10 | Agent 固有风险与初步应对 | |

---

## 📝 课后作业

### 必做题

1. **完成手写 ReAct Agent**：实现至少 3 个工具，通过 5 个测试问题
2. **编写测试报告**：记录每个问题的迭代次数、是否成功、失败原因
3. **Prompt 优化实验**：对比 2 种 Prompt 策略，写 200 字总结
4. **Git 提交**：`day39/` 目录下所有代码推送到 GitHub

### 选做题

5. **实现 `max_tokens` 预算控制**：累计 Token 超限时优雅终止
6. **添加对话记忆**：支持多轮对话，Agent 能引用之前的 Observation
7. **阅读 ReAct 论文 Figure 3**：复现论文中的一个示例

### 测试问题集（用于自测）

```
1. Python 是什么时候发布的？
2. 计算 123 * 456 + 789 的结果
3. 现在几点了？
4. ReAct 和 LangChain 分别是什么？
5. 北京今天天气怎么样？（测试 web_search）
```

---

## 💡 常见问题 FAQ

**Q1: Agent 和 Chain 应该怎么选择？**

A: 遵循「简单优先」原则。如果任务流程固定（检索→生成），用 Chain/RAG；如果任务需要动态决策（不知道要查几次、用什么工具），用 Agent。Agent 更强大但也更贵、更不稳定。

**Q2: LLM 不按格式输出 Action 怎么办？**

A: 三种策略：(1) 在 Prompt 中强调格式并提供示例；(2) 解析失败时将错误信息作为 Observation 反馈给 LLM 重试；(3) 使用支持 Function Calling 的模型（Day 40 会学）。今天的手写版本用策略 (2)。

**Q3: `eval()` 用于计算器安全吗？**

A: 教学演示可以，**生产环境绝对不行**。应使用 `ast.literal_eval` 或专门的数学解析库。Day 46 会讲 Agent 安全。

**Q4: 为什么设置 `temperature=0`？**

A: Agent 需要确定性地选择工具，`temperature=0` 让输出更稳定。创意写作类任务可以用更高 temperature，但 Agent 的 Action 选择建议用 0。

**Q5: ReAct 是最先进的 Agent 架构吗？**

A: 不是，但是最经典、最易理解的。后续会学 Plan-and-Execute、Reflexion、LangGraph 状态机等更高级架构。ReAct 是理解所有 Agent 的基础。

**Q6: 手写 Agent 和用框架有什么区别？**

A: 手写帮你理解底层原理，框架（LangChain/LangGraph）提供生产级功能：并行工具、流式输出、检查点、可观测性。两者都要学——先手写，再框架。

---

## 🔮 明日预习

**Day 40: LangChain Agent 与工具**

明天你将学习：

- LangChain 的 `@tool` 装饰器和 Tool 类
- `create_react_agent` 和 `AgentExecutor`
- Structured Tool 与 Pydantic 参数校验
- 内置工具生态：DuckDuckGo、Wikipedia、Python REPL
- 用 LangChain 重写今天的 ReAct Agent，代码量减少 70%

**预习建议**：
1. 安装 LangChain：`pip install langchain langchain-openai langchain-community`
2. 浏览官方 Agent 快速入门文档
3. 思考：今天手写的哪些逻辑可以被框架替代？

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 39 · 第四阶段 Agent 开发*
