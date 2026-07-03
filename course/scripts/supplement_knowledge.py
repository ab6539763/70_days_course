#!/usr/bin/env python3
"""第二轮知识库扩充 — 覆盖全部 70 天"""

from pathlib import Path

DAYS_DIR = Path(__file__).resolve().parent.parent / "days"

SUPPLEMENT: dict[int, str] = {}

def add(day, text):
    SUPPLEMENT[day] = text

add(9, """
### 9.1 继承与多态

```python
class BaseModel:
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        self.api_key = api_key

    def chat(self, messages: list) -> str:
        raise NotImplementedError("子类必须实现 chat 方法")

class OpenAIModel(BaseModel):
    def chat(self, messages: list) -> str:
        # 调用 OpenAI API
        return f"[OpenAI {self.model_name}] 回复..."

class QwenModel(BaseModel):
    def chat(self, messages: list) -> str:
        # 调用通义千问 API
        return f"[Qwen {self.model_name}] 回复..."

# 多态：同一接口，不同实现
models = [OpenAIModel("gpt-4", "sk-xxx"), QwenModel("qwen-max", "sk-yyy")]
for m in models:
    print(m.chat([{"role": "user", "content": "你好"}]))
```

### 9.2 魔术方法

| 方法 | 触发时机 | 用途 |
|------|----------|------|
| `__str__` | print(obj) | 用户友好显示 |
| `__repr__` | 交互式环境 | 开发者调试 |
| `__call__` | obj() | 让对象可调用 |
""")

add(10, """
### 10.1 模块与包

```
my_project/
├── main.py
├── config.py
├── models/
│   ├── __init__.py
│   ├── base.py
│   └── openai_model.py
└── utils/
    ├── __init__.py
    └── helpers.py
```

```python
# main.py
from models.openai_model import OpenAIModel
from utils.helpers import load_config

if __name__ == "__main__":
  config = load_config()
  model = OpenAIModel(**config)
```

### 10.2 异常处理

```python
try:
    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.Timeout:
    print("请求超时，请重试")
except requests.exceptions.HTTPError as e:
    print(f"HTTP 错误: {e.response.status_code}")
except json.JSONDecodeError:
    print("响应不是有效 JSON")
finally:
    print("请求完成")
```

### 10.3 虚拟环境

```bash
python -m venv venv
source venv/bin/activate
pip install requests python-dotenv
pip freeze > requirements.txt
```
""")

add(11, """
### 11.1 文件读写

```python
# 读取文本
with open("doc.txt", "r", encoding="utf-8") as f:
    content = f.read()

# 逐行读取（大文件推荐）
with open("big_file.txt", "r", encoding="utf-8") as f:
    for line in f:
        process(line.strip())

# 写入 JSON
import json
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

### 11.2 pathlib — 现代路径操作

```python
from pathlib import Path

docs_dir = Path("documents")
for file in docs_dir.glob("**/*.txt"):
    print(file.name, file.stat().st_size)
```

### 11.3 正则表达式入门

```python
import re

text = "联系方式: 13812345678, 邮箱: test@example.com"
phones = re.findall(r"1[3-9]\\d{9}", text)
emails = re.findall(r"[\\w.-]+@[\\w.-]+\\.\\w+", text)
```

> **RAG 前置技能**: Day 28 加载 PDF 文档前，需要先用今天学的技能做文本清洗
""")

add(13, """
### 13.1 装饰器

```python
import time
import functools

def retry(max_attempts=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"重试 {attempt+1}/{max_attempts}: {e}")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3)
def call_api():
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()
```

### 13.2 环境变量

```python
# .env 文件（不要提交到 Git！）
# DEEPSEEK_API_KEY=sk-xxxx

from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
```

### 13.3 asyncio 入门

```python
import asyncio

async def fetch_data():
    await asyncio.sleep(1)  # 模拟 IO 等待
    return "data"

async def main():
    result = await fetch_data()
    print(result)

asyncio.run(main())
```
""")

add(14, """
### 14.1 项目架构

```
day14_chat_assistant/
├── main.py              # 入口
├── assistant.py         # ChatAssistant 类
├── config.py            # 配置
├── .env                 # API Key（不提交）
├── .gitignore
├── requirements.txt
└── chat_histories/      # 对话历史
```

### 14.2 核心需求清单

| 功能 | 实现方式 | 对应知识点 |
|------|----------|-----------|
| 多轮对话 | messages 列表追加 | Day 4 列表 |
| 历史保存 | json.dump | Day 5 JSON |
| /clear 指令 | while + if | Day 3 流程控制 |
| /save 指令 | 文件写入 | Day 11 文件 |
| 异常处理 | try/except | Day 10 异常 |
| 代码组织 | 类 + 模块 | Day 8 OOP |

### 14.3 评分标准

- 功能完整 (40%)
- 代码规范 (20%)
- 异常处理 (20%)
- Git 提交 (10%)
- 文档 README (10%)
""")

add(16, """
### 16.1 核心参数详解

| 参数 | 范围 | 效果 | 建议 |
|------|------|------|------|
| temperature | 0-2 | 随机性 | 创意写作用 0.8-1.2，事实问答用 0-0.3 |
| top_p | 0-1 | 核采样 | 一般 0.9，与 temperature 二选一调 |
| max_tokens | 1-4096+ | 最大输出长度 | 按需求设置，影响成本 |
| frequency_penalty | -2~2 | 重复惩罚 | 避免重复用 0.5-1.0 |

### 16.2 流式输出

```python
response = requests.post(url, json={**payload, "stream": True}, stream=True)
for line in response.iter_lines():
    if line:
        line = line.decode("utf-8")
        if line.startswith("data: "):
            data = line[6:]
            if data == "[DONE]":
                break
            chunk = json.loads(data)
            content = chunk["choices"][0]["delta"].get("content", "")
            print(content, end="", flush=True)
```
""")

add(18, """
### 18.1 思维链 CoT

```python
prompt = '''
请一步步思考以下数学问题:

问题: 一个商店打八折后再减10元，最终价格是多少？原价200元。

让我们一步步思考:
1. 首先计算打八折后的价格
2. 然后减去10元
3. 得出最终价格

请按此格式回答。
'''
```

### 18.2 Prompt 注入防御

```python
def sanitize_input(user_input: str) -> str:
    dangerous_patterns = [
        "忽略之前的指令",
        "ignore previous",
        "你现在是",
    ]
    for pattern in dangerous_patterns:
        if pattern.lower() in user_input.lower():
            return "[输入已被过滤]"
    return user_input
```
""")

add(20, """
### 20.1 Embedding 原理

```
"猫" → [0.2, 0.8, 0.1, ...]   (1536维向量)
"狗" → [0.3, 0.7, 0.2, ...]   (语义相近，向量距离近)
"汽车" → [0.9, 0.1, 0.5, ...]  (语义不同，向量距离远)
```

### 20.2 余弦相似度

```python
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# 相似度范围: -1 到 1，越接近 1 越相似
```

### 20.3 相似问题匹配

```python
# 1. 预存问题库并向量化
# 2. 用户新问题向量化
# 3. 计算与所有预存问题的相似度
# 4. 返回最相似的问题及答案
```
""")

add(22, """
### 22.1 HTML 聊天界面骨架

```html
<!DOCTYPE html>
<html>
<head>
  <title>AI Chat</title>
  <style>
    #chat-box { height: 400px; overflow-y: auto; border: 1px solid #ccc; padding: 10px; }
    .user { text-align: right; color: blue; }
    .assistant { text-align: left; color: green; }
  </style>
</head>
<body>
  <div id="chat-box"></div>
  <input id="input" type="text" placeholder="输入消息...">
  <button onclick="send()">发送</button>
  <script>
    async function send() {
      const input = document.getElementById('input');
      const msg = input.value;
      // Day 24 将对接 FastAPI 后端
      appendMessage('user', msg);
      input.value = '';
    }
    function appendMessage(role, text) {
      const box = document.getElementById('chat-box');
      box.innerHTML += `<div class="${role}">${text}</div>`;
      box.scrollTop = box.scrollHeight;
    }
  </script>
</body>
</html>
```
""")

add(23, """
### 23.1 FastAPI 项目结构

```
chat_api/
├── main.py
├── models.py      # Pydantic 模型
├── services.py    # 业务逻辑
├── config.py
└── requirements.txt
```

### 23.2 Pydantic 数据校验

```python
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    session_id: str = "default"
    temperature: float = Field(0.7, ge=0, le=2)

class ChatResponse(BaseModel):
    reply: str
    session_id: str
    tokens_used: int = 0
```
""")

add(24, """
### 24.1 SSE 流式接口

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

@app.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    async def generate():
        async for chunk in llm_stream(req.message):
            yield f"data: {json.dumps({'content': chunk})}\\n\\n"
        yield "data: [DONE]\\n\\n"
    return StreamingResponse(generate(), media_type="text/event-stream")
```

### 24.2 CORS 配置

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```
""")

add(25, """
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
""")

add(26, """
### 26.1 LCEL 管道

```python
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

# 翻译 → 润色 → 摘要
translate_chain = translate_prompt | llm | StrOutputParser()
polish_chain = polish_prompt | llm | StrOutputParser()
summarize_chain = summarize_prompt | llm | StrOutputParser()

full_chain = (
    {"text": RunnablePassthrough()}
    | RunnableParallel(
        translated=translate_chain,
    )
    | polish_chain
    | summarize_chain
)
```
""")

add(27, """
### 27.1 多会话记忆

```python
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)
```
""")

add(28, """
### 28.1 文档加载

```python
from langchain_community.document_loaders import (
    PyPDFLoader, TextLoader, CSVLoader, WebBaseLoader
)

# PDF
loader = PyPDFLoader("manual.pdf")
pages = loader.load()

# 文本分割
from langchain.text_splitter import RecursiveCharacterTextSplitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\\n\\n", "\\n", "。", " "],
)
chunks = splitter.split_documents(pages)
```

### 28.2 chunk 调优实验

| chunk_size | 优点 | 缺点 |
|------------|------|------|
| 200 | 精确检索 | 上下文不完整 |
| 500 | 平衡 | 推荐起始值 |
| 1000 | 上下文丰富 | 可能引入噪声 |
""")

add(29, """
### 29.1 Chroma 向量库

```python
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db",
)

# 检索
results = vectorstore.similarity_search("年假政策", k=3)

# 带分数的检索
results_with_scores = vectorstore.similarity_search_with_score("年假政策", k=3)
for doc, score in results_with_scores:
    print(f"分数: {score:.4f} | {doc.page_content[:50]}")
```
""")

add(31, """
### 31.1 RAG 调优 checklist

- [ ] chunk_size 是否合适？（200/500/1000 对比实验）
- [ ] chunk_overlap 是否足够？（建议 10-20%）
- [ ] top_k 是否合理？（3-10）
- [ ] Embedding 模型是否匹配？（中文用 bge/m3e）
- [ ] Prompt 是否要求引用来源？
- [ ] 是否有"不知道"的兜底？
- [ ] 检索结果是否相关？（人工检查 20 条）
""")

add(32, """
### 32.1 查询改写

```python
rewrite_prompt = '''
你是一个查询优化专家。将用户的口语化问题改写为更适合检索的形式。

原始问题: {question}
改写后:
'''

multi_query_prompt = '''
根据用户问题，生成3个不同角度的检索查询:
问题: {question}
查询1:
查询2:
查询3:
'''
```
""")

add(33, """
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
""")

add(34, """
### 34.1 Ragas 评估

```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)

result = evaluate(
    dataset=test_dataset,
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
)
print(result)
```

### 34.2 评估指标

| 指标 | 衡量什么 | 目标 |
|------|----------|------|
| 忠实度 | 回答是否基于上下文 | > 0.8 |
| 答案相关性 | 回答是否切题 | > 0.8 |
| 上下文精确率 | 检索结果是否相关 | > 0.7 |
| 上下文召回率 | 是否检索到所需信息 | > 0.7 |
""")

add(35, """
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
""")

add(36, """
### 36.1 企业知识库架构

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  前端 React  │ ←→  │ FastAPI 后端 │ ←→  │  向量数据库  │
│  聊天界面    │     │  REST API   │     │  Chroma     │
└─────────────┘     └──────┬──────┘     └─────────────┘
                           ↓
                    ┌─────────────┐
                    │  LLM API    │
                    │  DeepSeek   │
                    └─────────────┘
```

### 36.2 功能清单

- [x] 多格式文档上传（PDF/Word/MD）
- [x] 混合检索 + Rerank
- [x] 多轮对话 + 会话管理
- [x] 引用溯源
- [x] 流式输出
- [x] Docker 部署
""")

add(40, """
### 40.1 @tool 装饰器

```python
from langchain_core.tools import tool

@tool
def search_web(query: str) -> str:
    \"\"\"搜索互联网获取最新信息\"\"\"
    # 调用 Tavily API
    return f"搜索结果: {query}"

@tool
def calculate(expression: str) -> str:
    \"\"\"计算数学表达式\"\"\"
    return str(eval(expression))

tools = [search_web, calculate]
```

### 40.2 AgentExecutor

```python
from langchain.agents import create_tool_calling_agent, AgentExecutor

agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
result = executor.invoke({"input": "北京今天天气怎么样？"})
```
""")

add(42, """
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
""")

add(43, """
### 43.1 Supervisor 模式

```
         ┌──────────────┐
         │  Supervisor  │ ← 分配任务
         └──────┬───────┘
    ┌──────────┼──────────┐
    ↓          ↓          ↓
┌────────┐ ┌────────┐ ┌────────┐
│ 搜索员  │ │ 分析师  │ │ 撰写员  │
└────────┘ └────────┘ └────────┘
```
""")

add(44, """
### 44.1 MCP 协议

MCP (Model Context Protocol) 是 Anthropic 推出的开放协议，让 AI 模型标准化地连接外部工具和数据源。

```
AI 客户端 ←→ MCP 协议 ←→ MCP Server ←→ 数据库/API/文件系统
```

### 44.2 Agent 记忆系统

| 类型 | 存储 | 生命周期 | 用途 |
|------|------|----------|------|
| 短期记忆 | messages 列表 | 当前会话 | 多轮对话 |
| 长期记忆 | 向量数据库 | 跨会话 | 用户偏好 |
| 工作记忆 | State | 当前任务 | Agent 推理 |
""")

add(46, """
### 46.1 Agent 失败模式

| 失败模式 | 原因 | 解决方案 |
|----------|------|----------|
| 无限循环 | 没有终止条件 | 设置 max_iterations |
| 工具调用错误 | Schema 不清晰 | 优化 description |
| 幻觉行动 | 捏造工具结果 | 输出校验 |
| 上下文溢出 | 历史太长 | 窗口记忆/摘要 |

### 46.2 LangSmith 追踪

```python
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-key"
# 自动记录每次调用的输入输出
```
""")

add(47, """
### 47.1 Text-to-SQL Agent

```python
@tool
def query_database(sql: str) -> str:
    \"\"\"执行 SQL 查询并返回结果。只能执行 SELECT 语句。\"\"\"
    if not sql.strip().upper().startswith("SELECT"):
        return "错误: 只允许 SELECT 查询"
    # 连接数据库执行
    return execute_sql(sql)

# Agent 将自然语言转为 SQL
# "上个月销售额最高的产品是什么？"
# → SELECT product, SUM(amount) FROM sales WHERE ...
```
""")

add(51, """
### 51.1 微调决策树

```
需要改变模型行为/风格/格式？
├── 是 → 有足够标注数据(>500条)？
│   ├── 是 → 有 GPU 资源？
│   │   ├── 是 → 微调 (LoRA)
│   │   └── 否 → Prompt 工程 + Few-shot
│   └── 否 → 用 LLM 生成数据 → 微调
└── 否 → 需要外部知识？
    ├── 是 → RAG
    └── 否 → Prompt 工程
```

### 51.2 LoRA 原理

```
原始模型权重 W (frozen, 不训练)
+ LoRA 适配器 ΔW = A × B (可训练, 参数量极小)
= 有效权重 W' = W + ΔW
```
""")

add(52, """
### 52.1 Alpaca 数据格式

```json
{
  "instruction": "将以下文本翻译成英文",
  "input": "今天天气很好",
  "output": "The weather is nice today."
}
```

### 52.2 Self-Instruct 数据生成

```python
prompt = '''
请为客服场景生成10条训练数据，格式为 JSON 数组:
[{"instruction": "...", "input": "...", "output": "..."}]
'''
# 用 LLM 生成 → 人工审核 → 加入训练集
```
""")

add(53, """
### 53.1 LLaMA-Factory 训练

```bash
# 安装
git clone https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory
pip install -e .

# 启动 WebUI
llamafactory-cli webui
```

### 53.2 关键训练参数

| 参数 | 建议值 | 说明 |
|------|--------|------|
| learning_rate | 1e-4 ~ 5e-5 | 学习率 |
| num_epochs | 3-5 | 训练轮数 |
| batch_size | 4-16 | 批大小 |
| lora_rank | 8-64 | LoRA 秩 |
| lora_alpha | 16-128 | LoRA 缩放 |
""")

add(55, """
### 55.1 Ollama 部署

```bash
# 安装 Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 拉取模型
ollama pull qwen2.5:7b

# 启动 API 服务（OpenAI 兼容）
# 默认 http://localhost:11434
```

### 55.2 vLLM 部署

```bash
pip install vllm
python -m vllm.entrypoints.openai.api_server \\
    --model /path/to/merged_model \\
    --port 8000
```
""")

add(56, """
### 56.1 Docker Compose 编排

```yaml
version: '3.8'
services:
  api:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://db:5432/chat
    depends_on:
      - db
      - chroma

  db:
    image: postgres:15
    volumes:
      - pg_data:/var/lib/postgresql/data

  chroma:
    image: chromadb/chroma:latest
    volumes:
      - chroma_data:/chroma/chroma

volumes:
  pg_data:
  chroma_data:
```
""")

add(57, """
### 57.1 安全清单

- [ ] API Key 不硬编码，用环境变量
- [ ] 用户输入过滤（Prompt 注入防御）
- [ ] 输出内容审核（敏感词过滤）
- [ ] 个人信息脱敏（手机号、身份证）
- [ ] 请求频率限制（防滥用）
- [ ] 成本监控与告警
- [ ] 日志不记录敏感信息
""")

add(66, """
### 66.1 简历项目描述模板

**项目一: 命令行多轮对话 AI 助手**
- 独立开发基于 DeepSeek API 的多轮对话系统，支持对话历史持久化与指令管理
- 技术栈: Python, requests, JSON, python-dotenv

**项目二: 企业级知识库问答系统**
- 基于 RAG 技术构建，支持 PDF/Word/Markdown 多格式文档，混合检索 + Rerank
- 技术栈: LangChain, Chroma, FastAPI, SSE, Docker

**项目三: 多 Agent 智能办公助手**
- 3+ Agent 协作，5+ 工具，支持任务中断恢复
- 技术栈: LangGraph, MCP, FastAPI
""")

add(67, """
### 67.1 高频面试题精选

**Q: 什么是 RAG？为什么需要 RAG？**
A: RAG(检索增强生成)通过检索外部知识库增强 LLM 回答。需要 RAG 因为: 1) 大模型知识有截止日期 2) 私有数据未在训练集中 3) 减少幻觉 4) 可溯源

**Q: RAG 怎么优化？**
A: 1) 优化 chunk 策略 2) 混合检索 3) Rerank 4) 查询改写 5) 换 Embedding 6) 优化 Prompt

**Q: Agent 和 Chain 的区别？**
A: Chain 是固定步骤流水线；Agent 由 LLM 自主决策下一步行动，可使用工具，适合复杂多变任务。

**Q: 什么时候用微调 vs RAG？**
A: 需要外部知识用 RAG；需要改变模型行为/风格/格式用微调；两者可结合。
""")


def apply():
    for day, text in SUPPLEMENT.items():
        md_path = DAYS_DIR / f"day{day:02d}.md"
        if not md_path.exists():
            continue
        content = md_path.read_text(encoding="utf-8")
        marker = "## 深度讲义"
        if marker in content and text.strip() not in content:
            content = content.replace(marker, marker + "\n" + text, 1)
            md_path.write_text(content, encoding="utf-8")
            print(f"✅ Supplemented day{day:02d}")
        elif marker not in content:
            # 插入深度讲义
            insert_marker = "## 常见错误与避坑"
            if insert_marker in content:
                block = f"## 深度讲义\n{text}\n\n{insert_marker}"
                content = content.replace(insert_marker, block, 1)
                md_path.write_text(content, encoding="utf-8")
                print(f"✅ Inserted day{day:02d}")


if __name__ == "__main__":
    apply()
    total = sum(len((DAYS_DIR / f"day{d:02d}.md").read_text().splitlines()) for d in range(1, 71))
    print(f"Total lines: {total:,}")
