# Day 30: 完整 RAG 系统搭建

> **培训阶段**: 第三阶段 RAG 应用开发 | **第 6 周 | **学习时长**: 约 6-8 小时  
> **今日关键词**: RAG Pipeline、Retrieval Chain、流式问答、Web 封装

---

## 📍 课程导航

### 上节回顾

**Day 25-29** 你逐一掌握了 RAG 的各个组件：
- Day 25: LangChain 入门（Model I/O）
- Day 26: LCEL 表达式与链
- Day 27: Memory 记忆机制
- Day 28: 文档加载与分割
- Day 29: 向量数据库（Chroma / Milvus）

今天是 **RAG 大汇合**——将所有组件串联为完整系统。

### 本节学习目标

完成本日学习后，你将能够：

1. 理解 RAG 完整架构与数据流
2. 用 LCEL 构建标准 RAG 链
3. 实现带引用来源的问答
4. 集成 Memory 实现多轮 RAG 对话
5. 实现流式 RAG 输出
6. 用 Gradio 封装为 Web 界面
7. 用 FastAPI 封装为 API 服务

### 与后续课程的衔接

- **Day 31** 周测与 RAG 调优，优化今天搭建的系统
- **Day 32-33** 高级 RAG 技术将在此基础上叠加
- **Day 36-37** 企业级项目是本日系统的生产级升级版

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：RAG 架构全景

#### 1.1 RAG 完整数据流

```
┌─────────── 离线阶段（Indexing）───────────┐
│  文档 → 加载 → 分割 → 嵌入 → 向量库      │
└─────────────────────────────────────────┘
                    ↓
┌─────────── 在线阶段（Retrieval + Generation）───────────┐
│  用户问题 → 嵌入 → 向量检索 → 相关文档                    │
│       ↓                                                   │
│  Prompt(问题 + 上下文) → LLM → 回答（附引用来源）         │
└─────────────────────────────────────────────────────────┘
```

#### 1.2 标准 RAG Prompt 模板

```python
RAG_PROMPT = """你是一个专业的企业知识库助手。请基于以下参考资料回答用户问题。

要求：
1. 只根据参考资料回答，不要编造信息
2. 如果资料中没有相关信息，请明确说明"根据现有资料无法回答"
3. 回答时引用来源，格式：[来源: 文件名]
4. 回答简洁准确，使用 Markdown 格式

参考资料：
{context}

用户问题：{question}"""
```

---

### 9:45 - 10:30 | 模块二：LCEL 构建 RAG 链

#### 2.1 最简 RAG 链

```python
# day30/01_basic_rag_chain.py
"""最简 RAG 链"""
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()

# 加载已有向量库
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma(
    collection_name="knowledge_base",
    embedding_function=embeddings,
    persist_directory="./chroma_db",
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

llm = ChatOpenAI(model="deepseek-chat", temperature=0)

def format_docs(docs):
    formatted = []
    for doc in docs:
        source = doc.metadata.get("source", "未知")
        formatted.append(f"[来源: {source}]\n{doc.page_content}")
    return "\n\n---\n\n".join(formatted)

prompt = ChatPromptTemplate.from_template("""基于以下参考资料回答问题。如果资料中没有相关信息，请说明。

参考资料：
{context}

问题：{question}""")

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 测试
questions = ["年假有多少天？", "报销流程是什么？", "公司成立于哪一年？"]
for q in questions:
    print(f"\n{'='*50}")
    print(f"Q: {q}")
    print(f"A: {rag_chain.invoke(q)}")
```

#### 2.2 带来源的 RAG 链

```python
# day30/02_rag_with_sources.py
"""带引用来源的 RAG"""
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma(
    collection_name="knowledge_base",
    embedding_function=embeddings,
    persist_directory="./chroma_db",
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
llm = ChatOpenAI(model="deepseek-chat", temperature=0)

prompt = ChatPromptTemplate.from_template("""基于参考资料回答问题。

参考资料：
{context}

问题：{question}""")

def format_docs_with_source(docs):
    return "\n\n".join(
        f"[{i+1}] 来源: {d.metadata.get('source', '?')}\n{d.page_content}"
        for i, d in enumerate(docs)
    )

rag_chain = (
    RunnableParallel(
        context=retriever | format_docs_with_source,
        question=RunnablePassthrough(),
        source_documents=retriever,
    )
    | RunnablePassthrough.assign(
        answer=prompt | llm | StrOutputParser()
    )
)

result = rag_chain.invoke("远程办公政策是什么？")
print(f"回答: {result['answer']}")
print(f"\n引用来源:")
for doc in result["source_documents"]:
    print(f"  - {doc.metadata.get('source', '?')}")
```

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：RAG + Memory + 流式输出

#### 3.1 多轮 RAG 对话

```python
# day30/03_rag_with_memory.py
"""RAG + Memory 多轮对话"""
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma(
    collection_name="knowledge_base",
    embedding_function=embeddings,
    persist_directory="./chroma_db",
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
llm = ChatOpenAI(model="deepseek-chat", temperature=0)

store = {}
def get_history(session_id):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def retrieve_context(inputs):
    docs = retriever.invoke(inputs["input"])
    context = "\n".join(d.page_content for d in docs)
    return {**inputs, "context": context}

prompt = ChatPromptTemplate.from_messages([
    ("system", "基于参考资料回答问题。\n\n参考资料：{context}"),
    MessagesPlaceholder("history"),
    ("human", "{input}"),
])

chain = (
    RunnablePassthrough.assign(context=lambda x: "\n".join(
        d.page_content for d in retriever.invoke(x["input"])
    ))
    | prompt | llm | StrOutputParser()
)

chain_with_memory = RunnableWithMessageHistory(
    chain, get_history, input_messages_key="input", history_messages_key="history",
)

config = {"configurable": {"session_id": "user_001"}}
print(chain_with_memory.invoke({"input": "年假有多少天？"}, config=config))
print(chain_with_memory.invoke({"input": "刚才那个问题，满三年呢？"}, config=config))
```

#### 3.2 流式 RAG 输出

```python
# day30/04_streaming_rag.py
"""流式 RAG 输出"""
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma(
    collection_name="knowledge_base",
    embedding_function=embeddings,
    persist_directory="./chroma_db",
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
llm = ChatOpenAI(model="deepseek-chat", temperature=0, streaming=True)

prompt = ChatPromptTemplate.from_template(
    "基于资料回答：\n{context}\n\n问题：{question}"
)

rag_chain = (
    {"context": retriever | (lambda docs: "\n".join(d.page_content for d in docs)),
     "question": RunnablePassthrough()}
    | prompt | llm | StrOutputParser()
)

print("Q: 报销流程是什么？")
print("A: ", end="")
for chunk in rag_chain.stream("报销流程是什么？"):
    print(chunk, end="", flush=True)
print()
```

---

## 🌆 下午课程（14:00 - 17:00）

### 14:00 - 15:30 | 模块四：Web 界面封装

#### 4.1 Gradio 界面

```bash
pip install gradio -i https://pypi.tuna.tsinghua.edu.cn/simple
```

```python
# day30/05_gradio_rag_app.py
"""Gradio RAG 问答界面"""
import gradio as gr
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma(
    collection_name="knowledge_base",
    embedding_function=embeddings,
    persist_directory="./chroma_db",
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
llm = ChatOpenAI(model="deepseek-chat", temperature=0)

prompt = ChatPromptTemplate.from_template(
    "基于参考资料回答。资料：\n{context}\n\n问题：{question}"
)
rag_chain = (
    {"context": retriever | (lambda d: "\n".join(x.page_content for x in d)),
     "question": RunnablePassthrough()}
    | prompt | llm | StrOutputParser()
)

def ask_question(question):
    if not question.strip():
        return "请输入问题"
    docs = retriever.invoke(question)
    sources = set(d.metadata.get("source", "?") for d in docs)
    answer = rag_chain.invoke(question)
    source_text = "\n".join(f"- {s}" for s in sources)
    return f"{answer}\n\n---\n📎 参考来源:\n{source_text}"

demo = gr.Interface(
    fn=ask_question,
    inputs=gr.Textbox(label="请输入您的问题", placeholder="例如：年假有多少天？"),
    outputs=gr.Markdown(label="回答"),
    title="🏢 企业知识库问答系统",
    description="基于 RAG 技术的企业内部知识库智能问答",
    examples=["年假有多少天？", "报销流程是什么？", "远程办公政策？"],
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
```

#### 4.2 FastAPI 封装

```python
# day30/06_fastapi_rag.py
"""FastAPI RAG API 服务"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="RAG API", version="1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma(
    collection_name="knowledge_base",
    embedding_function=embeddings,
    persist_directory="./chroma_db",
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
llm = ChatOpenAI(model="deepseek-chat", temperature=0)

prompt = ChatPromptTemplate.from_template(
    "基于资料回答：\n{context}\n\n问题：{question}"
)
rag_chain = (
    {"context": retriever | (lambda d: "\n".join(x.page_content for x in d)),
     "question": RunnablePassthrough()}
    | prompt | llm | StrOutputParser()
)

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str
    sources: list[str]

@app.post("/ask", response_model=AnswerResponse)
async def ask(req: QuestionRequest):
    docs = retriever.invoke(req.question)
    sources = list(set(d.metadata.get("source", "?") for d in docs))
    answer = await rag_chain.ainvoke(req.question)
    return AnswerResponse(answer=answer, sources=sources)

@app.get("/health")
async def health():
    return {"status": "ok", "docs_count": vectorstore._collection.count()}

# 启动: uvicorn day30.06_fastapi_rag:app --reload --port 8000
```

---

### 15:30 - 15:45 | 课间休息

---

### 15:45 - 17:00 | 模块五：下午实操——完整 RAG 系统

```python
# day30/07_complete_rag_system.py
"""下午实操：完整 RAG 系统（类封装）"""
import os
from dataclasses import dataclass
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()


@dataclass
class RAGConfig:
    docs_dir: str = "knowledge_base"
    persist_dir: str = "./chroma_db"
    collection_name: str = "knowledge_base"
    chunk_size: int = 500
    chunk_overlap: int = 100
    retrieval_k: int = 3
    model: str = "deepseek-chat"
    temperature: float = 0


class RAGSystem:
    def __init__(self, config: RAGConfig):
        self.config = config
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.llm = ChatOpenAI(model=config.model, temperature=config.temperature)
        self.vectorstore = None
        self.chain = None

    def index_documents(self):
        loader = DirectoryLoader(
            self.config.docs_dir, glob="**/*.{txt,md}",
            loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"},
        )
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.chunk_size,
            chunk_overlap=self.config.chunk_overlap,
        )
        chunks = splitter.split_documents(docs)
        self.vectorstore = Chroma.from_documents(
            chunks, self.embeddings,
            persist_directory=self.config.persist_dir,
            collection_name=self.config.collection_name,
        )
        print(f"✅ 索引完成: {len(chunks)} chunks")
        self._build_chain()

    def load_vectorstore(self):
        self.vectorstore = Chroma(
            collection_name=self.config.collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.config.persist_dir,
        )
        self._build_chain()

    def _build_chain(self):
        retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": self.config.retrieval_k}
        )
        prompt = ChatPromptTemplate.from_template(
            """你是企业知识库助手。基于参考资料回答，无相关信息请说明。

参考资料：
{context}

问题：{question}"""
        )
        self.chain = (
            {"context": retriever | self._format_docs, "question": RunnablePassthrough()}
            | prompt | self.llm | StrOutputParser()
        )

    @staticmethod
    def _format_docs(docs):
        return "\n\n".join(
            f"[{d.metadata.get('source', '?')}]\n{d.page_content}" for d in docs
        )

    def ask(self, question: str) -> dict:
        docs = self.vectorstore.as_retriever(
            search_kwargs={"k": self.config.retrieval_k}
        ).invoke(question)
        answer = self.chain.invoke(question)
        return {
            "question": question,
            "answer": answer,
            "sources": [d.metadata.get("source", "?") for d in docs],
        }

    def stream_ask(self, question: str):
        for chunk in self.chain.stream(question):
            yield chunk


def main():
    rag = RAGSystem(RAGConfig())
    if os.path.exists("./chroma_db"):
        rag.load_vectorstore()
        print("📂 加载已有向量库")
    else:
        rag.index_documents()

  while True:
        q = input("\n请输入问题 (quit 退出): ")
        if q.lower() in ("quit", "exit", "q"):
            break
        result = rag.ask(q)
        print(f"\n📎 来源: {', '.join(set(result['sources']))}")
        print(f"💬 {result['answer']}")


if __name__ == "__main__":
    main()
```

---

## 🌙 晚自习（19:00 - 21:00）

### 19:00 - 20:00

1. 跑通 Gradio 和 FastAPI 版本
2. 用 10 个问题测试 RAG 系统，记录回答质量
3. 尝试修改 Prompt 模板，观察回答风格变化

### 20:00 - 21:00

- 讨论 RAG 系统最常见的 3 个问题及解决方案
- 为 Day 31 周测做准备

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | RAG 完整架构与数据流 | |
| 2 | LCEL 构建标准 RAG 链 | |
| 3 | 带引用来源的 RAG | |
| 4 | RAG + Memory 多轮对话 | |
| 5 | 流式 RAG 输出 | |
| 6 | Gradio Web 界面 | |
| 7 | FastAPI API 服务 | |
| 8 | RAGSystem 类封装 | |

---

## 📝 课后作业

### 必做题

1. **完整系统**：搭建可运行的 RAG 系统（CLI + Gradio 二选一）
2. **测试报告**：10 个问题的问答测试，标注正确/部分正确/错误
3. **Git 提交**：`git commit -m "Day 30: 完整 RAG 系统搭建"`

### 选做题

4. 同时实现 Gradio 和 FastAPI 版本
5. 添加「上传文档并自动索引」功能

---

## 💡 常见问题 FAQ

**Q1: RAG 回答编造信息（幻觉）怎么办？**

A: 
1. Prompt 中强调「只根据参考资料回答」
2. 降低 temperature 到 0
3. 检查检索结果是否包含相关信息（Day 31 调优）
4. Day 32-33 高级技术进一步提升

**Q2: 检索不到相关文档？**

A: 检查 Embedding 模型、chunk_size、查询与文档的语义差距。Day 32 的 Query Rewriting 可解决。

**Q3: Gradio 启动后无法访问？**

A: 确认 `server_name="0.0.0.0"`，检查防火墙和端口占用。

**Q4: 如何更新知识库？**

A: 重新运行 `index_documents()`，或增量 `add_documents()`。注意去重。

**Q5: RAG 链的响应太慢？**

A: 瓶颈通常在 LLM 调用。优化方向：减少 k 值、用更快的模型、流式输出提升体验。

---

## 🔮 明日预习

**Day 31: 周测与 RAG 调优**

明天进行第 5 周总结测验，并系统学习 RAG 调优：

- 第 5 周知识周测
- chunk_size / overlap 调优实验
- Prompt 工程对 RAG 的影响
- 检索参数 k 值调优
- 常见问题诊断清单

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 30*
