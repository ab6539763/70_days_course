# Day 24: FastAPI 后端开发（下）

> **培训阶段**: 第二阶段 大模型理论与 API | **第 4 周** | **学习时长**: 约 6-8 小时  
> **今日关键词**: SSE 流式接口、CORS、SQLite、SQLAlchemy、ChatGPT 克隆联调

---

## 📍 课程导航

### 上节回顾
**Day 23** 我们完成了 FastAPI 后端基础：

- FastAPI 项目结构与路由定义
- Pydantic 数据验证模型
- 大模型服务层封装
- AI 对话 REST API 端点
- Swagger UI 测试

今天是第二阶段的 **收官之日**——SSE 流式输出、CORS 跨域、数据库持久化，完成网页版 ChatGPT 克隆！

### 本节学习目标
完成本日学习后，你将能够：

1. 实现 SSE（Server-Sent Events）流式 API 端点
2. 配置 CORS 解决前后端跨域问题
3. 使用 SQLite + SQLAlchemy 持久化对话历史
4. 完成前后端完整联调，打造可用的 Web 聊天应用
5. 为 Day 25 开始的 RAG 阶段做好准备

### 与后续课程的衔接
- **Day 14** 文件读写/SQLite 初识 → 今天用 SQLAlchemy ORM 操作数据库
- **Day 16** 流式输出 → 今天升级为 SSE Web 接口
- **Day 19** 工具调用 → Day 39+ Agent 将集成到 Web 后端
- **Day 22-23** 前端+后端 → 今天完整联调
- **Day 25+** RAG 开发 → 在今日后端基础上添加文档检索能力
- **Day 55-56** 部署 → 今天的项目可部署上线

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：SSE 流式接口

#### 1.1 什么是 SSE

**SSE（Server-Sent Events）** 是一种服务器向客户端推送数据的技术，适合流式输出场景。

```
普通 REST API：                SSE 流式 API：
Client → Request → Server     Client → Request → Server
Client ← Response（一次）      Client ← data: chunk1
                              Client ← data: chunk2
                              Client ← data: chunk3
                              Client ← data: [DONE]
```

| 对比 | WebSocket | SSE |
|------|-----------|-----|
| 方向 | 双向 | 单向（服务器→客户端） |
| 复杂度 | 较高 | 简单 |
| 适用 | 实时聊天、游戏 | 流式文本、通知 |
| 本课程 | Day 39+ 可选 | ✅ 今天使用 |

#### 1.2 FastAPI SSE 实现

```python
# day24/routers/chat_stream.py
"""SSE 流式聊天接口"""

import json
import requests
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from models.schemas import ChatRequest
from config import settings

router = APIRouter(prefix="/api", tags=["流式聊天"])


def generate_stream(messages: list, temperature: float, max_tokens: int):
    """生成 SSE 数据流"""
    response = requests.post(
        f"{settings.API_BASE_URL}/chat/completions",
        json={
            "model": settings.MODEL,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,
        },
        headers={
            "Authorization": f"Bearer {settings.API_KEY}",
            "Content-Type": "application/json",
        },
        stream=True,
        timeout=120,
    )
    response.raise_for_status()

    for line in response.iter_lines():
        if not line:
            continue
        line = line.decode("utf-8")
        if line.startswith("data: "):
            data = line[6:]
            if data == "[DONE]":
                yield "data: [DONE]\n\n"
                break
            try:
                chunk = json.loads(data)
                delta = chunk["choices"][0].get("delta", {})
                content = delta.get("content", "")
                if content:
                    # SSE 格式：data: {json}\n\n
                    yield f"data: {json.dumps({'content': content}, ensure_ascii=False)}\n\n"
            except json.JSONDecodeError:
                continue


@router.post("/chat/stream")
def chat_stream(request: ChatRequest):
    """SSE 流式聊天接口

    返回 text/event-stream 格式的流式响应。
    每个事件格式：data: {"content": "文字片段"}
    结束标记：data: [DONE]
    """
    api_messages = []
    has_system = any(m.role == "system" for m in request.messages)
    if not has_system:
        api_messages.append({
            "role": "system",
            "content": settings.SYSTEM_PROMPT,
        })
    for m in request.messages:
        api_messages.append({"role": m.role.value, "content": m.content})

    return StreamingResponse(
        generate_stream(
            api_messages,
            request.temperature or settings.DEFAULT_TEMPERATURE,
            request.max_tokens or settings.DEFAULT_MAX_TOKENS,
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # 禁用 Nginx 缓冲
        },
    )
```

#### 1.3 前端对接 SSE

```javascript
// day24/frontend/app.js 中的流式接收

async function sendToAPIStream(text) {
    messages.push({ role: "user", content: text });

    const response = await fetch("http://localhost:8000/api/chat/stream", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: messages, temperature: 0.7 }),
    });

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let fullContent = "";

    // 创建 AI 消息气泡（空内容，逐步填充）
    const messageDiv = createMessageElement("assistant", "");
    const bubble = messageDiv.querySelector(".bubble");
    chatArea.appendChild(messageDiv);

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split("\n");

        for (const line of lines) {
            if (line.startsWith("data: ")) {
                const data = line.slice(6);
                if (data === "[DONE]") break;

                try {
                    const parsed = JSON.parse(data);
                    if (parsed.content) {
                        fullContent += parsed.content;
                        bubble.innerHTML = formatContent(fullContent);
                        chatArea.scrollTop = chatArea.scrollHeight;
                    }
                } catch (e) {
                    // 跳过无法解析的行
                }
            }
        }
    }

    messages.push({ role: "assistant", content: fullContent });
    return fullContent;
}
```

---

### 9:45 - 10:30 | 模块二：CORS 跨域配置

#### 2.1 什么是 CORS

**CORS（Cross-Origin Resource Sharing）** 是浏览器的安全机制，阻止网页向不同域名发请求。

```
前端：http://localhost:3000
后端：http://localhost:8000
      ↑ 不同端口 = 不同源 = 浏览器阻止 fetch
```

#### 2.2 FastAPI CORS 配置

```python
# day24/main.py
"""FastAPI 应用入口 - 完整版"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routers import chat, chat_stream, conversations
import time

app = FastAPI(
    title="AI 聊天助手 API",
    description="大模型应用开发课程 - 网页版 ChatGPT 克隆",
    version="2.0.0",
)

# CORS 配置（必须在路由之前）
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",    # 前端开发服务器
        "http://127.0.0.1:3000",
        "http://localhost:5500",    # Live Server
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 请求日志中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    print(f"{request.method} {request.url.path} - {response.status_code} - {duration:.2f}s")
    return response

# 注册路由
app.include_router(chat.router)
app.include_router(chat_stream.router)
app.include_router(conversations.router)


@app.get("/")
def root():
    return {
        "message": "AI 聊天助手 API v2.0",
        "docs": "/docs",
        "endpoints": {
            "chat": "POST /api/chat",
            "stream": "POST /api/chat/stream",
            "conversations": "GET /api/conversations",
        },
    }


@app.get("/health")
def health():
    return {"status": "ok", "version": "2.0.0"}
```

#### 2.3 验证 CORS

```bash
# 启动后端
cd ~/llm-course/day24
uvicorn main:app --reload --port 8000

# 启动前端（另一个终端）
cd ~/llm-course/day24/frontend
python3 -m http.server 3000

# 浏览器访问 http://localhost:3000
# 打开 F12 → Network，发送消息，确认无 CORS 错误
```

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：SQLite + SQLAlchemy

#### 3.1 为什么需要数据库

| 无数据库 | 有数据库 |
|----------|----------|
| 刷新页面丢失对话 | 对话持久保存 |
| 无法查看历史会话 | 历史会话列表 |
| 无法多用户 | 支持多用户（Day 39+） |

#### 3.2 安装 SQLAlchemy

```bash
pip install sqlalchemy -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 3.3 数据库模型

```python
# day24/database/models.py
"""数据库模型"""

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

DATABASE_URL = "sqlite:///./chat.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Conversation(Base):
    """对话会话"""
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), default="新对话")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    """消息记录"""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role = Column(String(20), nullable=False)  # system/user/assistant
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")


def init_db():
    """初始化数据库（创建表）"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """获取数据库会话（依赖注入用）"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### 3.4 对话服务

```python
# day24/services/conversation.py
"""对话历史服务"""

from sqlalchemy.orm import Session
from database.models import Conversation, Message


class ConversationService:
    def create(self, db: Session, title: str = "新对话") -> Conversation:
        conv = Conversation(title=title)
        db.add(conv)
        db.commit()
        db.refresh(conv)
        return conv

    def get(self, db: Session, conv_id: int) -> Conversation | None:
        return db.query(Conversation).filter(Conversation.id == conv_id).first()

    def list_all(self, db: Session, limit: int = 50) -> list[Conversation]:
        return (
            db.query(Conversation)
            .order_by(Conversation.updated_at.desc())
            .limit(limit)
            .all()
        )

    def add_message(self, db: Session, conv_id: int, role: str, content: str) -> Message:
        msg = Message(conversation_id=conv_id, role=role, content=content)
        db.add(msg)
        # 更新会话时间
        conv = self.get(db, conv_id)
        if conv:
            from datetime import datetime
            conv.updated_at = datetime.utcnow()
            # 用第一条用户消息作为标题
            if conv.title == "新对话" and role == "user":
                conv.title = content[:50]
        db.commit()
        db.refresh(msg)
        return msg

    def get_messages(self, db: Session, conv_id: int) -> list[Message]:
        return (
            db.query(Message)
            .filter(Message.conversation_id == conv_id)
            .order_by(Message.created_at)
            .all()
        )

    def delete(self, db: Session, conv_id: int) -> bool:
        conv = self.get(db, conv_id)
        if conv:
            db.delete(conv)
            db.commit()
            return True
        return False


conversation_service = ConversationService()
```

#### 3.5 对话历史 API

```python
# day24/routers/conversations.py
"""对话历史路由"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database.models import get_db, init_db
from services.conversation import conversation_service

router = APIRouter(prefix="/api/conversations", tags=["对话历史"])


class ConversationCreate(BaseModel):
    title: str = "新对话"


class ConversationResponse(BaseModel):
    id: int
    title: str
    created_at: str
    message_count: int = 0

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: str

    class Config:
        from_attributes = True


@router.on_event("startup")
def startup():
    init_db()


@router.post("/", response_model=ConversationResponse)
def create_conversation(data: ConversationCreate, db: Session = Depends(get_db)):
    conv = conversation_service.create(db, data.title)
    return ConversationResponse(
        id=conv.id, title=conv.title,
        created_at=conv.created_at.isoformat(), message_count=0,
    )


@router.get("/", response_model=list[ConversationResponse])
def list_conversations(db: Session = Depends(get_db)):
    convs = conversation_service.list_all(db)
    return [
        ConversationResponse(
            id=c.id, title=c.title,
            created_at=c.created_at.isoformat(),
            message_count=len(c.messages),
        )
        for c in convs
    ]


@router.get("/{conv_id}/messages", response_model=list[MessageResponse])
def get_messages(conv_id: int, db: Session = Depends(get_db)):
    messages = conversation_service.get_messages(db, conv_id)
    return [
        MessageResponse(
            id=m.id, role=m.role, content=m.content,
            created_at=m.created_at.isoformat(),
        )
        for m in messages
    ]


@router.delete("/{conv_id}")
def delete_conversation(conv_id: int, db: Session = Depends(get_db)):
    if not conversation_service.delete(db, conv_id):
        raise HTTPException(status_code=404, detail="对话不存在")
    return {"message": "已删除"}
```

---

## 🌆 下午课程（14:00 - 17:00）

### 14:00 - 17:00 | 模块四：网页版 ChatGPT 克隆联调

#### 4.1 完整项目结构

```
day24/
├── main.py                    # FastAPI 入口
├── config.py                  # 配置
├── requirements.txt
├── .env
├── database/
│   ├── __init__.py
│   └── models.py              # SQLAlchemy 模型
├── models/
│   └── schemas.py             # Pydantic 模型
├── routers/
│   ├── chat.py                # 普通聊天
│   ├── chat_stream.py         # 流式聊天
│   └── conversations.py       # 对话历史
├── services/
│   ├── llm.py                 # 大模型服务
│   └── conversation.py        # 对话服务
└── frontend/
    ├── index.html
    ├── style.css
    └── app.js                 # 完整前端逻辑
```

#### 4.2 完整前端（流式 + 历史）

```javascript
// day24/frontend/app.js
// 网页版 ChatGPT 克隆 - 完整前端

const API_BASE = "http://localhost:8000/api";
let currentConversationId = null;
let messages = [];

// 初始化
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("sendBtn").addEventListener("click", handleSend);
    document.getElementById("clearBtn").addEventListener("click", handleNewChat);
    document.getElementById("userInput").addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    });
    loadConversations();
});

// 发送消息（流式）
async function handleSend() {
    const input = document.getElementById("userInput");
    const text = input.value.trim();
    if (!text) return;

    appendMessage("user", text);
    input.value = "";
    setLoading(true);

    try {
        // 确保有对话 ID
        if (!currentConversationId) {
            const resp = await fetch(`${API_BASE}/conversations/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ title: text.slice(0, 50) }),
            });
            const conv = await resp.json();
            currentConversationId = conv.id;
        }

        messages.push({ role: "user", content: text });
        await streamChat(text);
        loadConversations();
    } catch (error) {
        appendMessage("assistant", "抱歉，出现了错误：" + error.message);
    } finally {
        setLoading(false);
    }
}

// 流式聊天
async function streamChat(text) {
    const response = await fetch(`${API_BASE}/chat/stream`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: messages, temperature: 0.7 }),
    });

    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let fullContent = "";

    // 移除加载指示器，创建空消息
    document.getElementById("loadingIndicator")?.remove();
    const msgDiv = appendMessage("assistant", "");
    const bubble = msgDiv.querySelector(".bubble");

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        for (const line of chunk.split("\n")) {
            if (!line.startsWith("data: ")) continue;
            const data = line.slice(6);
            if (data === "[DONE]") break;
            try {
                const parsed = JSON.parse(data);
                if (parsed.content) {
                    fullContent += parsed.content;
                    bubble.innerHTML = formatContent(fullContent);
                    scrollToBottom();
                }
            } catch (e) { /* skip */ }
        }
    }

    messages.push({ role: "assistant", content: fullContent });
}

// 加载对话列表
async function loadConversations() {
    try {
        const resp = await fetch(`${API_BASE}/conversations/`);
        const convs = await resp.json();
        const list = document.getElementById("conversationList");
        if (!list) return;
        list.innerHTML = convs.map(c => `
            <div class="conv-item ${c.id === currentConversationId ? 'active' : ''}"
                 onclick="loadConversation(${c.id})">
                <span>${c.title}</span>
                <small>${c.message_count} 条消息</small>
            </div>
        `).join("");
    } catch (e) { console.error("加载对话列表失败", e); }
}

// 加载指定对话
async function loadConversation(convId) {
    currentConversationId = convId;
    messages = [];
    document.getElementById("chatArea").innerHTML = "";

    const resp = await fetch(`${API_BASE}/conversations/${convId}/messages`);
    const msgs = await resp.json();
    for (const m of msgs) {
        if (m.role !== "system") {
            appendMessage(m.role, m.content);
            messages.push({ role: m.role, content: m.content });
        }
    }
    loadConversations();
}

// 新建对话
function handleNewChat() {
    currentConversationId = null;
    messages = [];
    document.getElementById("chatArea").innerHTML = `
        <div class="message assistant">
            <div class="avatar">🤖</div>
            <div class="bubble">新对话已开始，有什么可以帮你的？</div>
        </div>`;
    loadConversations();
}

// UI 辅助函数
function appendMessage(role, content) {
    const chatArea = document.getElementById("chatArea");
    const div = document.createElement("div");
    div.className = `message ${role}`;
    const avatar = role === "user" ? "👤" : "🤖";
    div.innerHTML = `
        <div class="avatar">${avatar}</div>
        <div class="bubble">${formatContent(content)}</div>`;
    chatArea.appendChild(div);
    scrollToBottom();
    return div;
}

function formatContent(text) {
    if (!text) return '<div class="typing-indicator"><span></span><span></span><span></span></div>';
    return text.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;")
        .replace(/\*\*(.*?)\*\*/g,"<strong>$1</strong>")
        .replace(/`([^`]+)`/g,"<code>$1</code>")
        .replace(/\n/g,"<br>");
}

function setLoading(loading) {
    document.getElementById("sendBtn").disabled = loading;
    document.getElementById("userInput").disabled = loading;
    if (loading) {
        const div = document.createElement("div");
        div.className = "message assistant";
        div.id = "loadingIndicator";
        div.innerHTML = `<div class="avatar">🤖</div><div class="bubble">${formatContent("")}</div>`;
        document.getElementById("chatArea").appendChild(div);
        scrollToBottom();
    }
}

function scrollToBottom() {
    const chatArea = document.getElementById("chatArea");
    chatArea.scrollTop = chatArea.scrollHeight;
}
```

#### 4.3 启动与联调

```bash
# 终端 1：启动后端
cd ~/llm-course/day24
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# 终端 2：启动前端
cd ~/llm-course/day24/frontend
python3 -m http.server 3000

# 浏览器访问 http://localhost:3000
```

#### 4.4 联调检查清单

| 步骤 | 操作 | 期望结果 |
|------|------|----------|
| 1 | 访问前端页面 | 聊天界面正常显示 |
| 2 | 发送「你好」 | 流式逐字显示 AI 回复 |
| 3 | 继续对话 | 多轮上下文连贯 |
| 4 | 刷新页面 | 对话历史保留（如实现了侧边栏） |
| 5 | 新建对话 | 开始新会话 |
| 6 | F12 Network | 无 CORS 错误 |
| 7 | 后端 /docs | 所有端点可用 |
| 8 | chat.db | SQLite 文件已创建 |

#### 4.5 第二阶段总结

```
第二阶段（Day 15-24）学习路径
═══════════════════════════════════════════════════

Week 3: 大模型理论与 API
  Day 15  原理科普 ─── Transformer、Token、tiktoken
  Day 16  API 参数 ─── temperature、stream、角色
  Day 17  Prompt 基础 ─ 四要素、Few-shot
  Day 18  Prompt 进阶 ─ CoT、JSON Mode、FC 初探
  Day 19  Function Calling ─ 多工具助手
  Day 20  Embedding ─── 相似度、迷你 RAG
  Day 21  周测综合 ─── 全能 AI 助手

Week 4: Web 开发
  Day 22  前端速成 ─── HTML/CSS/JS、聊天界面
  Day 23  FastAPI 上 ── REST API、Pydantic
  Day 24  FastAPI 下 ── SSE、CORS、数据库、联调 ✅

═══════════════════════════════════════════════════
下一阶段：Day 25+ RAG 检索增强生成
```

---

## 🌙 晚自习（19:00 - 21:00）

### 19:00 - 20:00 | 项目完善与部署预览

#### 可选增强

1. **侧边栏对话列表**：在 index.html 添加 conversationList 区域
2. **Markdown 渲染**：引入 marked.js 渲染 AI 回复
3. **暗色模式**：CSS 变量切换主题
4. **Docker 部署预览**（Day 55 详学）：

```dockerfile
# Dockerfile 预览
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 20:00 - 21:00 | 第二阶段复盘

- 回顾 Day 15-24 所有项目代码
- 确保 ChatGPT 克隆可完整运行
- 预习 Day 25 RAG 概念

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | SSE 流式接口原理与实现 | |
| 2 | FastAPI StreamingResponse | |
| 3 | 前端 EventSource/fetch 流式读取 | |
| 4 | CORS 跨域原理与 CORSMiddleware | |
| 5 | SQLAlchemy ORM 模型定义 | |
| 6 | SQLite 数据库操作 | |
| 7 | 对话历史 CRUD API | |
| 8 | 前后端完整联调 | |
| 9 | 网页版 ChatGPT 克隆运行 | |
| 10 | 第二阶段知识体系总结 | |

---

## 📝 课后作业

### 必做题

1. **ChatGPT 克隆**：完成前后端联调，流式对话可用
2. **对话持久化**：验证刷新页面后对话历史保留
3. **Git 提交**：`git commit -m "Day 24: ChatGPT克隆 - SSE+CORS+SQLite"`

### 选做题

4. 添加侧边栏对话列表 UI
5. 实现消息的 Markdown 渲染（代码高亮）
6. 添加「导出对话」功能（下载 JSON 文件）

---

## 💡 常见问题 FAQ

**Q1: SSE 和 Day 16 的 stream 有什么区别？**

A: 本质相同，都是流式传输。Day 16 是 Python 客户端消费流；今天是 FastAPI 服务端转发流，浏览器前端消费 SSE。

**Q2: 生产环境可以用 SQLite 吗？**

A: 小型应用可以。大规模应用建议 PostgreSQL。RAG 阶段的向量数据会用 Chroma/Milvus 等专业数据库。

**Q3: CORS 配置 allow_origins=["*"] 可以吗？**

A: 开发环境可以，生产环境应指定具体域名，避免安全风险。

**Q4: 前端和后端必须分开部署吗？**

A: 不一定。可以用 FastAPI 的 `StaticFiles` 挂载前端，一个服务同时提供 API 和页面。分开部署更灵活。

**Q5: 第二阶段学完能达到什么水平？**

A: 你能独立开发一个完整的 Web AI 聊天应用——这是大模型应用开发工程师的核心交付能力。Day 25+ 在此基础上添加 RAG、Agent 等高级能力。

---

## 🔮 明日预习

**Day 25: RAG 概念与文档加载（第三阶段开启）**

下周开始进入 **RAG 检索增强生成** 阶段：

- RAG 架构原理与工作流程
- 文档加载与文本分块
- 向量数据库入门
- 在今日 ChatGPT 克隆基础上添加「文档问答」能力

**预习建议**：回顾 Day 20 的 Embedding 和迷你 RAG 代码，确保理解检索+生成的流程。

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 24*
