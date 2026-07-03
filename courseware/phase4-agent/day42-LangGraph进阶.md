# Day 42: LangGraph 进阶

> **培训阶段**: 第四阶段 Agent 开发 | **第 7 周** | **学习时长**: 约 6-8 小时  
> **今日关键词**: Checkpoint、Human-in-the-loop、Subgraph、并行节点、持久化状态

---

## 📍 课程导航

### 上节回顾

**Day 41** 你掌握了 LangGraph 的核心概念：StateGraph、节点、边、条件路由，并用 LangGraph 实现了 ReAct Agent 和智能问答路由图。今天将解锁 LangGraph 的生产级能力——让 Agent 可以**暂停等待人工确认、持久化状态、模块化复用**。

**Day 41 核心收获回顾：**
- StateGraph + MessagesState 构建 Agent 图
- 条件边 `add_conditional_edges` 实现动态路由
- ToolNode 预构建节点简化工具执行
- 图可视化与流式输出

### 本节学习目标

完成本日学习后，你将能够：

1. 使用 MemorySaver 实现 Agent 状态持久化（Checkpoint）
2. 实现 Human-in-the-loop：在关键步骤暂停等待人工审核
3. 使用 Subgraph 模块化复杂 Agent 工作流
4. 实现并行节点执行（fan-out / fan-in 模式）
5. 配置 thread_id 实现多用户会话隔离
6. 为 Day 46 Agent 工程化打下状态管理基础

### 与后续课程的衔接

- **Day 43** 多 Agent 系统用 Subgraph 封装每个子 Agent
- **Day 46** 将用 Checkpoint 实现 Agent 故障恢复和审计日志
- **Day 48** 阶段项目三的「人工审核」功能依赖今天的 interrupt 机制
- **Day 55** 部署时将用 PostgreSQL 替代 MemorySaver 做生产级持久化

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：Checkpoint 状态持久化

#### 1.1 为什么需要 Checkpoint？

```
没有 Checkpoint 的 Agent：
  用户 → Agent 执行 → 返回结果 → 状态销毁
  问题：无法恢复中断的执行、无法回溯历史、无法多轮对话

有 Checkpoint 的 Agent：
  用户 → Agent 执行 → 状态保存到存储 → 返回结果
  用户 → "继续" → 从上次状态恢复 → 继续执行
  优势：故障恢复、对话记忆、审计追踪
```

#### 1.2 MemorySaver 基础

```python
# day42/checkpoint_basic.py
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import HumanMessage, AIMessage

# 创建内存检查点存储
memory = MemorySaver()

# 构建简单图
def chat_node(state: MessagesState) -> dict:
    last_msg = state["messages"][-1].content
    return {"messages": [AIMessage(content=f"收到: {last_msg}")]}

graph = StateGraph(MessagesState)
graph.add_node("chat", chat_node)
graph.add_edge(START, "chat")
graph.add_edge("chat", END)

# 编译时传入 checkpointer
app = graph.compile(checkpointer=memory)

# 使用 thread_id 隔离会话
config = {"configurable": {"thread_id": "user-123"}}

# 第一轮对话
result1 = app.invoke(
    {"messages": [HumanMessage(content="你好")]},
    config=config,
)
print(result1["messages"][-1].content)

# 第二轮对话（自动加载历史）
result2 = app.invoke(
    {"messages": [HumanMessage(content="我叫小明")]},
    config=config,
)
# Agent 能看到之前的 "你好" 消息

# 查看保存的状态
state = app.get_state(config)
print(f"历史消息数: {len(state.values['messages'])}")
```

#### 1.3 查看和回溯历史

```python
# 获取所有历史 checkpoint
history = list(app.get_state_history(config))
for i, snapshot in enumerate(history):
    print(f"Checkpoint {i}: {snapshot.config['configurable']['checkpoint_id']}")
    print(f"  消息数: {len(snapshot.values.get('messages', []))}")

# 回滚到特定 checkpoint
if len(history) > 1:
    app.update_state(config, history[1].values)
```

#### 1.4 生产级存储：PostgreSQL

```python
# day42/checkpoint_postgres.py（了解即可，Day 55 部署时实操）
# pip install langgraph-checkpoint-postgres psycopg[binary]

from langgraph.checkpoint.postgres import PostgresSaver

DB_URI = "postgresql://user:pass@localhost:5432/agent_db"
with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    checkpointer.setup()  # 创建必要的表
    app = graph.compile(checkpointer=checkpointer)
```

---

### 9:45 - 10:30 | 模块二：Human-in-the-loop

#### 2.1 interrupt 机制

LangGraph 允许在特定节点**暂停执行**，等待人工输入后再继续：

```python
# day42/human_in_loop.py
"""
Human-in-the-loop 示例：敏感操作需人工确认
"""
import os
from typing import Literal
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    temperature=0,
)

@tool
def send_email(to: str, subject: str, body: str) -> str:
    """发送邮件（敏感操作，需人工确认）。"""
    return f"邮件已发送至 {to}，主题: {subject}"

@tool
def search_info(query: str) -> str:
    """搜索信息（安全操作，自动执行）。"""
    return f"关于 '{query}' 的搜索结果"

tools = [send_email, search_info]
llm_with_tools = llm.bind_tools(tools)

def agent_node(state: MessagesState) -> dict:
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

def should_continue(state: MessagesState) -> Literal["tools", "human_review", "end"]:
    last = state["messages"][-1]
    if not hasattr(last, "tool_calls") or not last.tool_calls:
        return "end"
    
    # 敏感工具需要人工审核
    sensitive_tools = {"send_email"}
    for tc in last.tool_calls:
        if tc["name"] in sensitive_tools:
            return "human_review"
    return "tools"

def human_review_node(state: MessagesState) -> dict:
    """人工审核节点：展示待执行操作，等待确认"""
    last = state["messages"][-1]
    tool_calls = last.tool_calls
    review_msg = "⚠️ 以下操作需要您的确认:\n"
    for tc in tool_calls:
        review_msg += f"  工具: {tc['name']}\n  参数: {tc['args']}\n"
    review_msg += "\n请回复 '确认' 执行，或 '取消' 中止。"
    return {"messages": [AIMessage(content=review_msg)]}

# 构建图
graph = StateGraph(MessagesState)
graph.add_node("agent", agent_node)
graph.add_node("tools", ToolNode(tools))
graph.add_node("human_review", human_review_node)

graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue, {
    "tools": "tools",
    "human_review": "human_review",
    "end": END,
})
graph.add_edge("tools", "agent")
graph.add_edge("human_review", END)  # 等待人工输入后需重新 invoke

# 使用 interrupt_before 在 human_review 前暂停
memory = MemorySaver()
app = graph.compile(
    checkpointer=memory,
    interrupt_before=["human_review"],  # 在此节点前暂停
)

# ===== 使用流程 =====
config = {"configurable": {"thread_id": "email-session-1"}}

# Step 1: 用户请求发邮件 → Agent 计划在 human_review 前暂停
result = app.invoke(
    {"messages": [HumanMessage(content="给 boss@company.com 发一封请假邮件")]},
    config=config,
)
print("Agent 计划在 human_review 前暂停")
print(f"当前状态: {app.get_state(config).next}")  # ('human_review',)

# Step 2: 人工审核后，继续执行
# 人工确认
app.invoke(None, config=config)  # 传入 None 继续执行
final_state = app.get_state(config)
print(f"最终消息: {final_state.values['messages'][-1].content}")
```

#### 2.2 实际应用场景

| 场景 | 中断点 | 人工操作 |
|------|--------|----------|
| 发送邮件/消息 | 执行前 | 确认收件人和内容 |
| 数据库写入 | 执行前 | 确认 SQL 语句 |
| 金融交易 | 执行前 | 确认金额和账户 |
| 代码部署 | 执行前 | 确认部署版本 |
| 内容发布 | 生成后 | 审核内容质量 |

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：Subgraph 与并行执行

#### 3.1 Subgraph 子图

```python
# day42/subgraph_demo.py
"""
Subgraph：将复杂 Agent 拆分为可复用模块
"""
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import HumanMessage, AIMessage

# ===== 子图 1：研究模块 =====
def research_node(state: MessagesState) -> dict:
    query = state["messages"][-1].content
    return {"messages": [AIMessage(content=f"[研究结果] 关于'{query}'的详细信息...")]}

research_graph = StateGraph(MessagesState)
research_graph.add_node("research", research_node)
research_graph.add_edge(START, "research")
research_graph.add_edge("research", END)
research_subgraph = research_graph.compile()

# ===== 子图 2：写作模块 =====
def write_node(state: MessagesState) -> dict:
    context = state["messages"][-1].content
    return {"messages": [AIMessage(content=f"[文章] 基于{context}撰写的文章...")]}

writing_graph = StateGraph(MessagesState)
writing_graph.add_node("write", write_node)
writing_graph.add_edge(START, "write")
writing_graph.add_edge("write", END)
writing_subgraph = writing_graph.compile()

# ===== 主图：编排子图 =====
def prepare_node(state: MessagesState) -> dict:
    return {"messages": [AIMessage(content="[准备] 开始处理...")]}

main_graph = StateGraph(MessagesState)
main_graph.add_node("prepare", prepare_node)
main_graph.add_node("research", research_subgraph)  # 嵌入子图
main_graph.add_node("writing", writing_subgraph)     # 嵌入子图

main_graph.add_edge(START, "prepare")
main_graph.add_edge("prepare", "research")
main_graph.add_edge("research", "writing")
main_graph.add_edge("writing", END)

app = main_graph.compile()

result = app.invoke({"messages": [HumanMessage(content="大模型发展趋势")]})
for msg in result["messages"]:
    print(msg.content)
```

#### 3.2 并行节点（Fan-out / Fan-in）

```python
# day42/parallel_nodes.py
"""
并行执行：同时调用多个工具，合并结果
"""
import operator
from typing import Annotated
from typing_extensions import TypedDict

class ParallelState(TypedDict):
    question: str
    search_results: Annotated[list, operator.add]  # 并行结果合并
    final_answer: str

def search_web(state: ParallelState) -> dict:
    return {"search_results": [f"网页: {state['question']}的相关信息"]}

def search_db(state: ParallelState) -> dict:
    return {"search_results": [f"数据库: {state['question']}的记录"]}

def search_docs(state: ParallelState) -> dict:
    return {"search_results": [f"文档: {state['question']}的说明"]}

def merge_results(state: ParallelState) -> dict:
  merged = "\n".join(state["search_results"])
  return {"final_answer": f"综合结果:\n{merged}"}

graph = StateGraph(ParallelState)
graph.add_node("search_web", search_web)
graph.add_node("search_db", search_db)
graph.add_node("search_docs", search_docs)
graph.add_node("merge", merge_results)

graph.add_edge(START, "search_web")
graph.add_edge(START, "search_db")    # 并行扇出
graph.add_edge(START, "search_docs")  # 并行扇出
graph.add_edge("search_web", "merge")  # 扇入
graph.add_edge("search_db", "merge")
graph.add_edge("search_docs", "merge")
graph.add_edge("merge", END)

app = graph.compile()
result = app.invoke({"question": "用户反馈", "search_results": [], "final_answer": ""})
print(result["final_answer"])
```

---

## 🌇 下午实操（14:00 - 17:30）

### 14:00 - 15:30 | 实操项目：带人工审核的客服 Agent

#### 项目需求

构建客服 Agent，具备：
1. 自动回答常见问题（知识库检索）
2. 查询订单（自动执行）
3. 退款操作（需人工审核）
4. 会话持久化（Checkpoint）
5. 完整执行日志

#### 完整代码

```python
# day42/customer_service_agent.py
"""
客服 Agent - 带人工审核和状态持久化
"""
import os
from typing import Literal
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    temperature=0,
)

# ===== 模拟数据 =====
FAQ = {
    "退货": "7天内无理由退货，商品需保持原包装。",
    "运费": "满99元免运费，不满收取10元运费。",
    "会员": "会员享受9.5折优惠，生日当月双倍积分。",
}
ORDERS = {"ORD001": {"status": "已发货", "amount": 299}, "ORD002": {"status": "待付款", "amount": 159}}

# ===== 工具 =====
@tool
def search_faq(query: str) -> str:
    """搜索常见问题解答。"""
    for key, answer in FAQ.items():
        if key in query:
            return answer
    return "未找到相关FAQ，建议转人工客服。"

@tool
def check_order(order_id: str) -> str:
    """查询订单状态。输入订单号如 ORD001。"""
    order = ORDERS.get(order_id.upper())
    if order:
        return f"订单 {order_id}: 状态={order['status']}, 金额={order['amount']}元"
    return f"未找到订单 {order_id}"

@tool
def process_refund(order_id: str, reason: str) -> str:
    """处理退款申请（敏感操作）。"""
    return f"退款申请已提交: 订单={order_id}, 原因={reason}"

tools = [search_faq, check_order, process_refund]
SENSITIVE = {"process_refund"}

# ===== 节点 =====
SYSTEM_PROMPT = """你是专业客服助手。规则：
1. 常见问题用 search_faq 查询
2. 订单问题用 check_order 查询
3. 退款请求用 process_refund（会触发人工审核）
4. 用中文友好回答"""

def agent_node(state: MessagesState) -> dict:
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = llm.bind_tools(tools).invoke(messages)
    return {"messages": [response]}

def review_node(state: MessagesState) -> dict:
    last = state["messages"][-1]
    info = "\n".join(f"  {tc['name']}: {tc['args']}" for tc in last.tool_calls)
    from langchain_core.messages import AIMessage
    return {"messages": [AIMessage(content=f"🔒 需人工确认:\n{info}\n回复'确认'继续")]}

def route(state: MessagesState) -> Literal["tools", "review", "end"]:
    last = state["messages"][-1]
    if not hasattr(last, "tool_calls") or not last.tool_calls:
        return "end"
    if any(tc["name"] in SENSITIVE for tc in last.tool_calls):
        return "review"
    return "tools"

# ===== 构建图 =====
graph = StateGraph(MessagesState)
graph.add_node("agent", agent_node)
graph.add_node("tools", ToolNode(tools))
graph.add_node("review", review_node)

graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", route, {"tools": "tools", "review": "review", "end": END})
graph.add_edge("tools", "agent")
graph.add_edge("review", END)

memory = MemorySaver()
app = graph.compile(checkpointer=memory, interrupt_before=["review"])

# ===== 交互测试 =====
def run_customer_service():
    thread_id = input("会话ID (直接回车新建): ").strip() or "session-new"
    config = {"configurable": {"thread_id": thread_id}}
    
    print(f"客服助手已启动 (会话: {thread_id})")
    while True:
        msg = input("\n客户: ").strip()
        if msg.lower() in ("quit", "exit"):
            break
        
        result = app.invoke({"messages": [HumanMessage(content=msg)]}, config)
        
        # 检查是否需要人工审核
        state = app.get_state(config)
        if state.next:
            print(f"\n{result['messages'][-1].content}")
            confirm = input("审核操作 (确认/取消): ").strip()
            if confirm == "确认":
                app.invoke(None, config)
                state = app.get_state(config)
            else:
                print("操作已取消")
        
        print(f"\n客服: {state.values['messages'][-1].content}")

if __name__ == "__main__":
    run_customer_service()
```

---

### 15:30 - 17:30 | 扩展练习与总结

#### 练习 1：多 thread 会话隔离测试

```python
# 验证不同 thread_id 互不影响
config_a = {"configurable": {"thread_id": "user-A"}}
config_b = {"configurable": {"thread_id": "user-B"}}

app.invoke({"messages": [HumanMessage(content="我是用户A")]}, config_a)
app.invoke({"messages": [HumanMessage(content="我是用户B")]}, config_b)

state_a = app.get_state(config_a)
state_b = app.get_state(config_b)
# 两个会话的历史应该完全独立
```

#### 练习 2：为 Day 48 项目设计图结构

画出阶段项目三（RAG + Agent 混合应用）的 LangGraph 结构：
- 入口分类 → RAG 路径 / Agent 路径
- Agent 路径含工具调用和人工审核
- 最终汇总输出

---

## 🌙 晚自习（19:00 - 21:00）

### 19:00 - 20:00 | 深度学习

1. LangGraph Checkpoint 文档
2. Human-in-the-loop 教程
3. 阅读 `langgraph/pregel/` 源码了解执行引擎

### 20:00 - 21:00 | 自习

- 完成客服 Agent 项目
- 测试人工审核流程
- Git 提交：`Day 42: LangGraph 进阶`
- 预习 Day 43 多 Agent 系统

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | MemorySaver Checkpoint 持久化 | |
| 2 | thread_id 会话隔离 | |
| 3 | get_state / get_state_history 状态查看 | |
| 4 | interrupt_before 人工介入 | |
| 5 | Human-in-the-loop 完整流程 | |
| 6 | Subgraph 子图模块化 | |
| 7 | 并行节点 fan-out/fan-in | |
| 8 | Annotated reducer 并行结果合并 | |
| 9 | 敏感操作审核模式 | |
| 10 | PostgreSQL Checkpoint（概念） | |

---

## 📝 课后作业

### 必做题

1. 完成客服 Agent（3 个工具 + 人工审核 + Checkpoint）
2. 测试 3 个 thread_id 的会话隔离
3. 实现并行搜索图（3 个搜索源 + 合并）
4. Git 提交

### 选做题

5. 添加「取消」分支：人工拒绝后 Agent 给出替代方案
6. 用 PostgreSQL 替换 MemorySaver
7. 为客服 Agent 添加执行时间统计

---

## 💡 常见问题 FAQ

**Q1: `invoke(None, config)` 是什么意思？**

A: 在 interrupt 暂停后，传入 `None` 表示「不添加新输入，继续执行下一个节点」。用于人工确认后恢复执行。

**Q2: MemorySaver 的数据存在哪里？**

A: 存在 Python 进程内存中，重启后丢失。生产环境用 PostgreSQL 或 Redis。

**Q3: 并行节点的结果如何合并？**

A: 使用 `Annotated[list, operator.add]`，每个并行节点返回的 list 会自动拼接。

**Q4: Subgraph 和直接添加 Node 有什么区别？**

A: Subgraph 是独立编译的图，可以单独测试和复用。适合 Day 43 多 Agent 场景。

---

## 🔮 明日预习

**Day 43: 多 Agent 系统**

- 多 Agent 架构模式：Supervisor、Hierarchical、Collaborative
- 用 LangGraph 实现 Supervisor 模式
- Agent 间通信与任务分配
- CrewAI 框架简介

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 42 · 第四阶段 Agent 开发*
