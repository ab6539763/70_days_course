# Day 36: 阶段项目二（上）——企业级知识库问答系统 Day 1

> **培训阶段**: 第三阶段 RAG 应用开发 | **第 7 周 | **学习时长**: 约 6-8 小时  
> **今日关键词**: 企业知识库、系统架构、FastAPI、文档管理、索引服务

---

## 📍 课程导航

### 上节回顾

**Day 25-35** 你系统学习了 RAG 全技术栈：
- LangChain / LCEL / Memory 框架能力
- 文档处理 / 向量库 / 完整 RAG 流水线
- 高级 RAG 技术 + Ragas 评估
- LlamaIndex 框架

今天是 **阶段项目二的第一天**——将所学技术整合为 **企业级知识库问答系统**。

### 本节学习目标

完成本日学习后，你将能够：

1. 分析企业知识库问答系统的需求与技术选型
2. 设计系统架构（前后端分离 + RAG 后端）
3. 搭建项目工程结构与开发环境
4. 实现文档上传与管理 API
5. 实现文档自动索引服务（加载→分割→嵌入→存储）
6. 实现基础问答 API
7. 完成项目 Day 1 的核心后端功能

### 与后续课程的衔接

- **Day 37** 完成前端界面、用户认证、会话管理、部署
- **Day 38** 项目答辩与代码评审
- 本项目可作为毕业设计的基础或参考

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：项目需求分析

#### 1.1 项目背景

```
某中型科技公司（500 人）内部知识分散在：
- 员工手册 PDF
- 技术文档 Markdown
- FAQ 表格 CSV
- 政策文件 Word

痛点：
- 新员工找不到信息，反复问 HR
- 技术文档搜索困难
- 政策更新后旧版本仍在流传
```

#### 1.2 功能需求

| 模块 | 功能 | 优先级 |
|------|------|--------|
| 文档管理 | 上传/删除/列表/预览 | P0 |
| 智能问答 | 自然语言提问 + 引用来源 | P0 |
| 索引服务 | 自动分割嵌入入库 | P0 |
| 会话管理 | 多轮对话 + 历史记录 | P1 |
| 用户认证 | 登录/权限控制 | P1 |
| 管理后台 | 索引状态/使用统计 | P2 |

#### 1.3 技术选型

| 层次 | 技术 | 理由 |
|------|------|------|
| 后端框架 | FastAPI | Day 24 已学，异步高性能 |
| RAG 框架 | LangChain | 课程主力，生态完善 |
| 向量库 | Chroma（开发）/ Milvus（生产） | 渐进式 |
| Embedding | text-embedding-3-small | 性价比 |
| LLM | DeepSeek-V3 | 课程主力 |
| 前端 | Gradio（Day 37） | 快速原型 |
| 数据库 | SQLite（元数据） | 轻量够用 |

#### 1.4 系统架构

```
┌─────────────────────────────────────────────────┐
│                   前端 (Gradio)                    │
│  文档上传 │ 智能问答 │ 会话历史 │ 管理面板       │
└──────────────────────┬──────────────────────────┘
                       │ HTTP API
┌──────────────────────┴──────────────────────────┐
│                FastAPI 后端                       │
│  ┌──────────┐ ┌──────────┐ ┌──────────────┐    │
│  │ 文档管理  │ │ 问答服务  │ │ 索引服务      │    │
│  │ /docs    │ │ /chat    │ │ /index       │    │
│  └────┬─────┘ └────┬─────┘ └──────┬───────┘    │
│       │            │              │             │
│  ┌────┴────────────┴──────────────┴───────┐    │
│  │           RAG 引擎 (LangChain)          │    │
│  │  Load → Split → Embed → Store → Query  │    │
│  └────────────────────────────────────────┘    │
│       │            │              │             │
│  ┌────┴────┐  ┌────┴────┐  ┌─────┴─────┐      │
│  │ SQLite  │  │ Chroma  │  │ DeepSeek  │      │
│  │ 元数据   │  │ 向量库   │  │ LLM API   │      │
│  └─────────┘  └─────────┘  └───────────┘      │
└─────────────────────────────────────────────────┘
```

---

### 9:45 - 10:30 | 模块二：项目工程搭建

#### 2.1 项目结构

```bash
mkdir -p enterprise-kb/{app/{api,core,models,services},data/{uploads,chromadb},tests}
cd enterprise-kb
```

```
enterprise-kb/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 入口
│   ├── config.py             # 配置管理
│   ├── api/
│   │   ├── __init__.py
│   │   ├── documents.py      # 文档管理 API
│   │   ├── chat.py           # 问答 API
│   │   └── index.py          # 索引 API
│   ├── core/
│   │   ├── __init__.py
│   │   ├── database.py       # SQLite 数据库
│   │   └── rag_engine.py     # RAG 引擎
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py        # Pydantic 模型
│   └── services/
│       ├── __init__.py
│       ├── document_service.py
│       └── index_service.py
├── data/
│   ├── uploads/              # 上传文件存储
│   └── chromadb/             # 向量库持久化
├── tests/
├── requirements.txt
├── .env
└── README.md
```

#### 2.2 配置与依赖

```python
# app/config.py
"""配置管理"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "企业知识库问答系统"
    debug: bool = True

    openai_api_key: str = ""
    openai_api_base: str = "https://api.deepseek.com/v1"
    llm_model: str = "deepseek-chat"
    embedding_model: str = "text-embedding-3-small"

    chroma_persist_dir: str = "./data/chromadb"
    chroma_collection: str = "enterprise_kb"
    upload_dir: str = "./data/uploads"
    database_url: str = "sqlite:///./data/kb_metadata.db"

    chunk_size: int = 500
    chunk_overlap: int = 100
    retrieval_k: int = 3

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
```

```
# requirements.txt
fastapi>=0.110.0
uvicorn>=0.27.0
python-multipart>=0.0.9
pydantic-settings>=2.0.0
langchain>=0.3.0
langchain-openai>=0.2.0
langchain-community>=0.3.0
langchain-chroma>=0.2.0
langchain-text-splitters>=0.3.0
chromadb>=0.5.0
python-dotenv>=1.0.0
pypdf>=4.0.0
```

#### 2.3 数据模型

```python
# app/models/schemas.py
"""Pydantic 数据模型"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DocumentInfo(BaseModel):
    id: int
    filename: str
    file_type: str
    file_size: int
    chunk_count: int = 0
    status: str = "pending"  # pending / indexed / failed
    created_at: datetime
    indexed_at: Optional[datetime] = None


class DocumentUploadResponse(BaseModel):
    id: int
    filename: str
    message: str


class ChatRequest(BaseModel):
    question: str
    session_id: str = "default"


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
    session_id: str


class IndexStatus(BaseModel):
    total_documents: int
    indexed_documents: int
    total_chunks: int
    collection_name: str
```

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：RAG 引擎核心

```python
# app/core/rag_engine.py
"""RAG 引擎核心"""
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from app.config import get_settings
import os


class RAGEngine:
    def __init__(self):
        self.settings = get_settings()
        self.embeddings = OpenAIEmbeddings(model=self.settings.embedding_model)
        self.llm = ChatOpenAI(
            model=self.settings.llm_model, temperature=0,
        )
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.settings.chunk_size,
            chunk_overlap=self.settings.chunk_overlap,
        )
        self.vectorstore = None
        self.chain = None
        self._init_vectorstore()

    def _init_vectorstore(self):
        os.makedirs(self.settings.chroma_persist_dir, exist_ok=True)
        self.vectorstore = Chroma(
            collection_name=self.settings.chroma_collection,
            embedding_function=self.embeddings,
            persist_directory=self.settings.chroma_persist_dir,
        )
        self._build_chain()

    def _build_chain(self):
        retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": self.settings.retrieval_k}
        )
        prompt = ChatPromptTemplate.from_template(
            """你是企业知识库助手。基于参考资料回答问题。
如果资料中没有相关信息，请明确说明"根据现有资料无法回答"。
引用来源，格式：[来源: 文件名]

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
            f"[来源: {d.metadata.get('source', '?')}]\n{d.page_content}" for d in docs
        )

    def load_and_index_file(self, file_path: str, filename: str) -> int:
        ext = os.path.splitext(filename)[1].lower()
        loaders = {
            ".txt": lambda: TextLoader(file_path, encoding="utf-8"),
            ".md": lambda: TextLoader(file_path, encoding="utf-8"),
            ".pdf": lambda: PyPDFLoader(file_path),
            ".csv": lambda: CSVLoader(file_path, encoding="utf-8"),
        }
        if ext not in loaders:
            raise ValueError(f"不支持的文件格式: {ext}")

        documents = loaders[ext]().load()
        for doc in documents:
            doc.metadata["source"] = filename

        chunks = self.splitter.split_documents(documents)
        self.vectorstore.add_documents(chunks)
        return len(chunks)

    def ask(self, question: str) -> dict:
        retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": self.settings.retrieval_k}
        )
        docs = retriever.invoke(question)
        answer = self.chain.invoke(question)
        sources = list(set(d.metadata.get("source", "?") for d in docs))
        return {"answer": answer, "sources": sources}

    def get_stats(self) -> dict:
        return {
            "total_chunks": self.vectorstore._collection.count(),
            "collection_name": self.settings.chroma_collection,
        }
```

---

## 🌆 下午课程（14:00 - 17:00）

### 14:00 - 15:30 | 模块四：API 开发

#### 4.1 文档管理 API

```python
# app/api/documents.py
"""文档管理 API"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.schemas import DocumentUploadResponse, DocumentInfo
from app.services.document_service import DocumentService
from typing import List

router = APIRouter(prefix="/api/documents", tags=["文档管理"])
doc_service = DocumentService()


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(400, "文件名不能为空")

    allowed = {".txt", ".md", ".pdf", ".csv"}
    ext = "." + file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in allowed:
        raise HTTPException(400, f"不支持的格式: {ext}")

    doc_id = await doc_service.save_and_index(file)
    return DocumentUploadResponse(
        id=doc_id, filename=file.filename, message="上传并索引成功"
    )


@router.get("/", response_model=List[DocumentInfo])
async def list_documents():
    return doc_service.list_all()


@router.delete("/{doc_id}")
async def delete_document(doc_id: int):
    doc_service.delete(doc_id)
    return {"message": f"文档 {doc_id} 已删除"}
```

#### 4.2 问答 API

```python
# app/api/chat.py
"""问答 API"""
from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse
from app.core.rag_engine import RAGEngine

router = APIRouter(prefix="/api/chat", tags=["智能问答"])
rag_engine = RAGEngine()


@router.post("/ask", response_model=ChatResponse)
async def ask_question(req: ChatRequest):
    result = rag_engine.ask(req.question)
    return ChatResponse(
        answer=result["answer"],
        sources=result["sources"],
        session_id=req.session_id,
    )


@router.get("/stats")
async def get_stats():
    return rag_engine.get_stats()
```

#### 4.3 主入口

```python
# app/main.py
"""FastAPI 主入口"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import documents, chat
from app.config import get_settings
import os

settings = get_settings()
os.makedirs(settings.upload_dir, exist_ok=True)
os.makedirs(settings.chroma_persist_dir, exist_ok=True)

app = FastAPI(title=settings.app_name, version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])

app.include_router(documents.router)
app.include_router(chat.router)


@app.get("/")
async def root():
    return {"app": settings.app_name, "status": "running", "docs": "/docs"}


@app.get("/health")
async def health():
    return {"status": "healthy"}

# 启动: uvicorn app.main:app --reload --port 8000
```

#### 4.4 文档服务

```python
# app/services/document_service.py
"""文档服务"""
import os
import shutil
from datetime import datetime
from app.config import get_settings
from app.core.rag_engine import RAGEngine

settings = get_settings()
rag = RAGEngine()

_documents = []
_next_id = 1


class DocumentService:
    async def save_and_index(self, file) -> int:
        global _next_id
        doc_id = _next_id
        _next_id += 1

        file_path = os.path.join(settings.upload_dir, f"{doc_id}_{file.filename}")
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        chunk_count = rag.load_and_index_file(file_path, file.filename)

        _documents.append({
            "id": doc_id, "filename": file.filename,
            "file_type": os.path.splitext(file.filename)[1],
            "file_size": os.path.getsize(file_path),
            "chunk_count": chunk_count, "status": "indexed",
            "created_at": datetime.now(), "indexed_at": datetime.now(),
        })
        return doc_id

    def list_all(self):
        return _documents

    def delete(self, doc_id: int):
        _documents[:] = [d for d in _documents if d["id"] != doc_id]
```

---

### 15:30 - 15:45 | 课间休息

---

### 15:45 - 17:00 | 模块五：Day 1 联调测试

#### 5.1 启动与测试

```bash
cd enterprise-kb
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

访问 http://localhost:8000/docs 查看 Swagger API 文档。

#### 5.2 API 测试脚本

```python
# tests/test_api.py
"""API 测试"""
import requests

BASE = "http://localhost:8000"

# 1. 健康检查
print(requests.get(f"{BASE}/health").json())

# 2. 上传文档
with open("test_doc.txt", "w") as f:
    f.write("公司年假制度：入职满一年10天，满三年15天。" * 5)

with open("test_doc.txt", "rb") as f:
    resp = requests.post(f"{BASE}/api/documents/upload", files={"file": f})
    print(f"上传: {resp.json()}")

# 3. 文档列表
print(f"文档列表: {requests.get(f'{BASE}/api/documents/').json()}")

# 4. 问答
resp = requests.post(f"{BASE}/api/chat/ask", json={
    "question": "年假有多少天？", "session_id": "test"
})
print(f"问答: {resp.json()}")

# 5. 统计
print(f"统计: {requests.get(f'{BASE}/api/chat/stats').json()}")
```

#### 5.3 Day 1 完成清单

| 任务 | 状态 |
|------|------|
| 项目结构搭建 | ✅ |
| 配置管理 | ✅ |
| RAG 引擎核心 | ✅ |
| 文档上传 API | ✅ |
| 文档列表/删除 API | ✅ |
| 问答 API | ✅ |
| API 联调测试 | ✅ |

---

## 🌙 晚自习（19:00 - 21:00）

### 19:00 - 20:00

1. 完成 Day 1 所有 API 的联调测试
2. 上传 3 个以上真实文档并测试问答
3. 检查 Swagger 文档是否完整

### 20:00 - 21:00

- 代码 Review：互相检查项目结构
- 讨论 Day 37 前端方案选择

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | 企业知识库需求分析 | |
| 2 | 系统架构设计 | |
| 3 | 项目工程结构规范 | |
| 4 | RAG 引擎核心封装 | |
| 5 | 文档上传与管理 API | |
| 6 | 问答 API | |
| 7 | FastAPI 项目组织 | |
| 8 | API 联调测试 | |

---

## 📝 课后作业

### 必做题

1. **完成后端 API**：所有 Day 1 API 可正常运行
2. **上传测试**：至少 3 个文档上传并索引成功
3. **Git 提交**：`git commit -m "Day 36: 企业知识库项目 Day1"`

### 选做题

4. 添加文档索引状态查询 API
5. 实现 SQLite 持久化文档元数据（替代内存存储）

---

## 💡 常见问题 FAQ

**Q1: 上传大 PDF 索引很慢怎么办？**

A: 返回异步响应，后台任务处理索引。Day 37 可添加 Celery 异步任务。

**Q2: 删除文档后向量库中的 chunks 怎么清理？**

A: 需要按 metadata 中的 source 字段删除对应 chunks。当前版本简化处理，Day 37 完善。

**Q3: 多个用户同时上传会冲突吗？**

A: Chroma 支持并发写入，但建议使用文件锁或队列。

**Q4: API 没有认证安全吗？**

A: Day 37 将添加 JWT 认证。开发阶段可暂不实现。

---

## 🔮 明日预习

**Day 37: 阶段项目二（下）——企业级知识库问答系统 Day 2**

- Gradio 前端界面
- 多轮对话与会话管理
- Query Rewriting 集成
- Docker 部署
- Ragas 评估报告

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 36*
