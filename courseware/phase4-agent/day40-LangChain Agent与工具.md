# Day 40: LangChain Agent 与工具

> **培训阶段**: 第四阶段 Agent 开发 | **第 7 周 | **学习时长**: 约 6-8 小时  
> **今日关键词**: LangChain、@tool、AgentExecutor、create_react_agent、Structured Tool

---

## 📍 课程导航

### 上节回顾

**Day 39** 中你手写了完整的 ReAct Agent，深入理解了 Thought-Action-Observation 循环、工具注册、Action 解析和停止条件。今天将把昨天的 200 行手写代码，用 LangChain 框架以不到 50 行实现同等功能，并解锁框架带来的生产级能力。

**Day 39 核心收获回顾：**
- ReAct 循环：Thought → Action → Observation → 循环或 Final Answer
- 工具设计原则：单一职责、清晰描述、安全输入
- Agent 调试：日志、死循环检测、Prompt 优化

### 本节学习目标

完成本日学习后，你将能够：

1. 使用 `@tool` 装饰器和 `StructuredTool` 定义 LangChain 工具
2. 使用 `create_react_agent` + `AgentExecutor` 构建生产级 Agent
3. 配置 `ChatOpenAI` 连接 DeepSeek API（兼容 OpenAI 接口）
4. 使用 LangChain 内置工具（DuckDuckGo、Wikipedia、Python REPL）
5. 理解 `AgentExecutor` 的配置项：max_iterations、handle_parsing_errors
6. 对比手写 Agent 与框架 Agent 的优劣

### 与后续课程的衔接

- **Day 41** LangGraph 是 LangChain 团队推出的下一代 Agent 编排框架，今天学的 AgentExecutor 将被 StateGraph 替代
- **Day 43** 多 Agent 系统中，每个 Agent 仍基于今天的 Tool + Executor 模式
- **Day 46** Agent 工程化将深入 AgentExecutor 的中间件和回调机制
- **Day 48** 阶段项目三将使用 LangChain Agent 作为核心执行引擎

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：LangChain Agent 架构

#### 1.1 LangChain Agent 组件全景

```
┌─────────────────────────────────────────────────────────┐
│                   LangChain Agent 栈                     │
│                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌────────────┐ │
│  │   Tools     │    │   Agent     │    │  Executor  │ │
│  │  @tool      │ →  │ create_react│ →  │ max_iter   │ │
│  │  Structured │    │ _agent      │    │ callbacks  │ │
│  └─────────────┘    └─────────────┘    └────────────┘ │
│         │                  │                   │        │
│         └──────────────────┼───────────────────┘        │
│                            ▼                            │
│                   ┌─────────────┐                         │
│                   │  ChatModel  │                         │
│                   │ (DeepSeek)  │                         │
│                   └─────────────┘                         │
└─────────────────────────────────────────────────────────┘
```

**核心概念对照表（Day 39 手写 vs LangChain）：**

| Day 39 手写 | LangChain 框架 | 说明 |
|-------------|----------------|------|
| `TOOLS` 字典 | `@tool` / `StructuredTool` | 工具定义 |
| `REACT_PROMPT` | `hub.pull("hwchase17/react")` | Prompt 模板 |
| `call_llm()` | `ChatOpenAI` | 模型调用 |
| `run_react_agent()` | `AgentExecutor` | 执行循环 |
| `parse_action()` | 内置解析器 | Action 解析 |
| `agent_log.txt` | `callbacks` | 日志回调 |

#### 1.2 环境安装

```bash
# 创建 Day 40 目录
mkdir -p ~/llm-course/day40
cd ~/llm-course/day40

# 安装 LangChain 生态
pip install langchain langchain-openai langchain-community \
            langchainhub duckduckgo-search wikipedia

# 验证安装
python -c "import langchain; print(langchain.__version__)"
```

#### 1.3 配置 DeepSeek 模型

```python
# day40/config.py
import os
from langchain_openai import ChatOpenAI

def get_llm(temperature: float = 0):
    """获取 DeepSeek 聊天模型（兼容 OpenAI 接口）"""
    return ChatOpenAI(
        model="deepseek-chat",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
        temperature=temperature,
    )
```

---

### 9:45 - 10:30 | 模块二：工具（Tools）详解

#### 2.1 @tool 装饰器

最简单的工具定义方式：

```python
# day40/tools_basic.py
from langchain_core.tools import tool

@tool
def calculator(expression: str) -> str:
  """计算数学表达式。输入数学表达式字符串，返回计算结果。
  
  示例: calculator("2+3*4") 返回 "14"
  """
  allowed = set("0123456789+-*/.() ")
  if not all(c in allowed for c in expression):
      return "错误：表达式包含不允许的字符"
  try:
      return str(eval(expression))
  except Exception as e:
      return f"计算错误: {e}"

@tool
def get_word_length(word: str) -> str:
  """返回单词或句子的字符数。"""
  return f"'{word}' 的长度是 {len(word)} 个字符"

# 查看工具元信息
print(calculator.name)        # calculator
print(calculator.description) # 计算数学表达式...
print(calculator.args)        # {'expression': {'type': 'string', ...}}
```

> 💡 **关键**：`@tool` 装饰器自动从函数签名和 docstring 生成 JSON Schema，LLM 据此决定如何调用工具。docstring 的质量直接影响 Agent 的工具选择准确率！

#### 2.2 StructuredTool 与 Pydantic

复杂工具需要多参数和类型校验：

```python
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

class SearchInput(BaseModel):
    query: str = Field(description="搜索关键词")
    max_results: int = Field(default=3, description="最大返回结果数")

def _search_knowledge(query: str, max_results: int = 3) -> str:
    """知识库搜索实现"""
    kb = {
        "python": "Python 是一种高级编程语言。",
        "langchain": "LangChain 是 LLM 应用开发框架。",
        "agent": "Agent 是能自主使用工具的 AI 系统。",
    }
    results = []
    for key, value in kb.items():
        if query.lower() in key:
            results.append(f"[{key}] {value}")
    return "\n".join(results[:max_results]) or f"未找到: {query}"

search_tool = StructuredTool.from_function(
    func=_search_knowledge,
    name="search_knowledge",
    description="在知识库中搜索相关信息",
    args_schema=SearchInput,
)
```

#### 2.3 内置工具生态

```python
# day40/builtin_tools.py
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_experimental.tools import PythonREPLTool

# 网页搜索（需要网络）
search = DuckDuckGoSearchRun()
# result = search.run("2026年大模型发展趋势")

# 维基百科
wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
# result = wikipedia.run("Artificial intelligence")

# Python 代码执行（⚠️ 注意安全风险）
python_repl = PythonREPLTool()
# result = python_repl.run("print(2**10)")
```

| 内置工具 | 用途 | 风险等级 |
|----------|------|----------|
| DuckDuckGoSearchRun | 实时网页搜索 | 低 |
| WikipediaQueryRun | 百科知识查询 | 低 |
| PythonREPLTool | 执行 Python 代码 | ⚠️ 高 |
| ShellTool | 执行 Shell 命令 | 🔴 极高 |

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：构建 LangChain ReAct Agent

#### 3.1 最小 Agent 实现

```python
# day40/react_agent_langchain.py
"""
Day 40: LangChain ReAct Agent
对比 Day 39 手写版本，代码量从 200 行降至 40 行
"""
import os
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.tools import tool
from langchain import hub

# ===== 1. 定义工具 =====
@tool
def calculator(expression: str) -> str:
    """计算数学表达式。输入: 如 '2+3*4'"""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"错误: {e}"

@tool
def search_knowledge(query: str) -> str:
    """搜索知识库。输入: 搜索关键词"""
    kb = {
        "python": "Python 1991年由 Guido 发布。",
        "react": "ReAct 2022年由 Yao 等人提出。",
        "langchain": "LangChain 是最流行的 LLM 应用框架。",
    }
    for k, v in kb.items():
        if k in query.lower():
            return v
    return f"未找到关于 {query} 的信息"

tools = [calculator, search_knowledge]

# ===== 2. 初始化模型 =====
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    temperature=0,
)

# ===== 3. 获取 ReAct Prompt 模板 =====
prompt = hub.pull("hwchase17/react")

# ===== 4. 创建 Agent =====
agent = create_react_agent(llm, tools, prompt)

# ===== 5. 创建 Executor =====
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,                    # 打印 Thought/Action 过程
    max_iterations=5,                # 最大迭代次数
    handle_parsing_errors=True,      # 自动处理解析错误
    return_intermediate_steps=True,  # 返回中间步骤
)

# ===== 6. 运行 =====
if __name__ == "__main__":
    result = agent_executor.invoke({
        "input": "ReAct 框架是什么时候提出的？计算这一年距离2026年有多少年。"
    })
    print(f"\n最终答案: {result['output']}")
    print(f"\n中间步骤数: {len(result['intermediate_steps'])}")
```

#### 3.2 AgentExecutor 关键配置

```python
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    
    # 控制类
    verbose=True,              # 控制台输出执行过程
    max_iterations=10,         # 最大循环次数（防死循环）
    max_execution_time=60,     # 最大执行时间（秒）
    early_stopping_method="generate",  # 超限时的策略
    
    # 错误处理
    handle_parsing_errors=True,  # True / 自定义错误消息字符串
    # handle_parsing_errors="请按正确格式输出 Action 和 Action Input",
    
    # 返回控制
    return_intermediate_steps=True,  # 是否返回中间步骤
    
    # 回调（Day 46 深入）
    # callbacks=[my_callback_handler],
)
```

#### 3.3 流式输出

```python
# 流式获取 Agent 执行过程
for chunk in agent_executor.stream({"input": "计算 99 * 99"}):
    print(chunk)
    # 输出示例:
    # {'actions': [ToolAgentAction(...)]}
    # {'steps': [AgentStep(...)]}
    # {'output': '9801'}
```

---

## 🌇 下午实操（14:00 - 17:30）

### 14:00 - 15:30 | 实操项目：多功能研究助手 Agent

#### 项目需求

构建一个「研究助手 Agent」，具备以下能力：

1. **知识库搜索**：查询课程相关知识（自定义工具）
2. **网页搜索**：DuckDuckGo 实时搜索
3. **数学计算**：复杂计算
4. **结果总结**：自动整合多源信息

#### 完整项目代码

```python
# day40/research_assistant.py
"""
研究助手 Agent - Day 40 下午实操项目
"""
import os
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain import hub

# ===== 工具定义 =====
@tool
def search_course_knowledge(query: str) -> str:
    """搜索本课程知识库，包含 Python、RAG、Agent、微调等内容。"""
    kb = {
        "rag": "RAG(检索增强生成)通过检索外部知识增强LLM回答，本课程Day25-38覆盖。",
        "agent": "Agent是能自主规划和使用工具的AI系统，本课程Day39-50覆盖。",
        "finetune": "模型微调是在预训练模型基础上用领域数据继续训练，Day51-57覆盖。",
        "langchain": "LangChain是LLM应用开发框架，支持Chain、Agent、RAG等。",
        "react": "ReAct让LLM交替推理和行动，是Agent的基础架构。",
    }
    results = [v for k, v in kb.items() if query.lower() in k]
    return "\n".join(results) if results else f"课程知识库中未找到: {query}"

@tool
def calculator(expression: str) -> str:
    """计算数学表达式。"""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"计算错误: {e}"

@tool
def get_today_date(_: str = "") -> str:
    """获取今天的日期。"""
    return datetime.now().strftime("%Y年%m月%d日")

# 网页搜索
web_search = DuckDuckGoSearchRun(name="web_search")

tools = [search_course_knowledge, calculator, get_today_date, web_search]

# ===== Agent 构建 =====
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    temperature=0,
)

prompt = hub.pull("hwchase17/react")
agent = create_react_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=8,
    handle_parsing_errors=True,
    return_intermediate_steps=True,
)

# ===== 交互式运行 =====
def chat():
    print("=" * 50)
    print("  研究助手 Agent（输入 quit 退出）")
    print("=" * 50)
    while True:
        question = input("\n你的问题: ").strip()
        if question.lower() in ("quit", "exit", "q"):
            break
        if not question:
            continue
        try:
            result = agent_executor.invoke({"input": question})
            print(f"\n📋 答案: {result['output']}")
            print(f"📊 执行了 {len(result['intermediate_steps'])} 个步骤")
        except Exception as e:
            print(f"❌ 错误: {e}")

if __name__ == "__main__":
    chat()
```

#### 测试用例

```
1. "本课程的 Agent 部分在哪几天？"          → 应调用 search_course_knowledge
2. "计算 2026 减去 2022"                    → 应调用 calculator
3. "今天是什么日期？"                        → 应调用 get_today_date
4. "2026年大模型行业最新动态"                → 应调用 web_search
5. "RAG和Agent有什么区别？分别在哪几天学？"   → 应多次调用 search_course_knowledge
```

---

### 15:30 - 15:45 | 课间休息

---

### 15:45 - 17:30 | 扩展练习

#### 练习 1：Day 39 vs Day 40 对比实验

用相同的 5 个测试问题，分别运行：
- Day 39 手写 `react_agent.py`
- Day 40 LangChain `research_assistant.py`

记录对比表：

| 指标 | 手写版 | LangChain 版 |
|------|--------|--------------|
| 代码行数 | ~200 | ~80 |
| 平均迭代次数 | | |
| 成功率 | | |
| 平均响应时间 | | |
| 错误处理 | | |

#### 练习 2：自定义 Prompt 模板

不使用 `hub.pull`，手写 Prompt：

```python
from langchain_core.prompts import PromptTemplate

custom_prompt = PromptTemplate.from_template("""
你是一个专业的研究助手，可以使用以下工具：

{tools}

工具名称列表: {tool_names}

请用中文回答，严格遵循以下格式：
Question: 需要回答的问题
Thought: 分析当前情况
Action: 工具名称
Action Input: 工具输入
Observation: 工具返回（系统填充）

... 重复 Thought/Action/Observation ...

Thought: 我现在可以给出完整答案了
Final Answer: 最终回答

Question: {input}
Thought:{agent_scratchpad}
""")
```

#### 练习 3：工具描述优化实验

测试不同 docstring 对工具选择的影响：

```python
# 差：描述模糊
@tool
def search(q: str) -> str:
    """搜索"""
    ...

# 好：描述清晰，有示例
@tool
def search_knowledge(query: str) -> str:
    """在课程知识库中搜索相关概念和知识点。
    
    适用场景：查询课程相关内容，如 RAG、Agent、微调等。
    不适用：实时新闻、天气等时效性信息（请用 web_search）。
    
    输入: 搜索关键词，如 'RAG' 或 'agent'
    返回: 匹配的知识点描述
    """
    ...
```

---

## 🌙 晚自习（19:00 - 21:00）

### 19:00 - 20:00 | LangChain 源码导读

阅读以下源码（GitHub），理解框架设计：

1. `langchain/agents/react/agent.py` — `create_react_agent` 实现
2. `langchain/agents/agent.py` — `AgentExecutor` 主循环
3. `langchain_core/tools.py` — `@tool` 装饰器

思考：AgentExecutor 的循环和 Day 39 手写的 `for i in range(max_iterations)` 有什么异同？

### 20:00 - 21:00 | 自习答疑

- 完成研究助手 Agent 并通过 5 个测试用例
- 完成 Day 39 vs Day 40 对比实验
- Git 提交：`git commit -m "Day 40: LangChain Agent 与工具"`
- 预习 LangGraph 介绍文档

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | LangChain Agent 架构（Tool/Agent/Executor） | |
| 2 | @tool 装饰器与 docstring 最佳实践 | |
| 3 | StructuredTool + Pydantic 参数校验 | |
| 4 | create_react_agent 创建 Agent | |
| 5 | AgentExecutor 配置项 | |
| 6 | hub.pull 获取 Prompt 模板 | |
| 7 | LangChain 内置工具使用 | |
| 8 | 流式输出 agent_executor.stream() | |
| 9 | handle_parsing_errors 错误处理 | |
| 10 | 手写 vs 框架 Agent 对比 | |

---

## 📝 课后作业

### 必做题

1. **完成研究助手 Agent**：4 个工具，通过 5 个测试用例
2. **对比实验报告**：Day 39 vs Day 40，填写对比表并写 300 字总结
3. **工具描述优化**：选 1 个工具，写 3 版 docstring，测试选择准确率
4. **Git 提交**：推送 `day40/` 到 GitHub

### 选做题

5. **添加 Wikipedia 工具**：集成 WikipediaQueryRun
6. **实现 Agent 对话记忆**：使用 `ConversationBufferMemory`
7. **自定义 Callback**：打印每步 Token 消耗

---

## 💡 常见问题 FAQ

**Q1: `hub.pull("hwchase17/react")` 报错怎么办？**

A: 需要网络访问 LangSmith Hub。如果失败，使用下午学的自定义 Prompt 模板替代。也可以缓存到本地：`prompt.save("react_prompt.json")`。

**Q2: DuckDuckGo 搜索返回空结果？**

A: 检查网络连接。国内环境可能需要代理。可以用自定义 mock 搜索工具替代。

**Q3: `handle_parsing_errors=True` 做了什么？**

A: 当 LLM 输出无法解析为 Action 时，自动将错误信息作为 Observation 反馈给 LLM，让它重试。等价于 Day 39 手写版的 `history += "\nObservation: 格式错误..."`。

**Q4: 为什么工具 docstring 如此重要？**

A: LLM 靠 docstring 决定调用哪个工具。模糊的描述会导致选错工具。把 docstring 当作「给 LLM 看的 API 文档」来写。

**Q5: AgentExecutor 和 Day 41 的 LangGraph 怎么选？**

A: 简单 Agent 用 AgentExecutor 足够。复杂流程（分支、并行、人工审核）用 LangGraph。明天开始学 LangGraph。

---

## 🔮 明日预习

**Day 41: LangGraph 入门**

明天你将学习：

- 为什么需要 LangGraph：AgentExecutor 的局限
- StateGraph 核心概念：节点、边、状态
- 用 LangGraph 重写 ReAct Agent
- 条件边与循环控制
- 图可视化与调试

**预习建议**：
1. 安装：`pip install langgraph`
2. 思考：今天的 Agent 如果要加「人工审核」步骤，用 AgentExecutor 好实现吗？

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 40 · 第四阶段 Agent 开发*
