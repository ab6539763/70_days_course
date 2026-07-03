# Day 23: FastAPI 后端开发（上）

> **培训阶段**: 第二阶段 大模型理论与 API | **第 4 周 | **学习时长**: 约 6-8 小时  
> **今日关键词**: FastAPI、路由、Pydantic、AI 对话 REST API

---

## 📍 课程导航

### 上节回顾
**Day 22** 我们完成了前端速成：

- HTML 页面结构与 CSS 样式
- JavaScript 基础与 DOM 操作
- fetch API 发送 HTTP 请求
- 静态聊天界面原型（mock 模式）

今天开始构建 **FastAPI 后端**——连接前端 UI 与大模型 API 的桥梁。

### 本节学习目标
完成本日学习后，你将能够：

1. 安装配置 FastAPI 和 Uvicorn 开发服务器
2. 定义路由、请求体和响应体
3. 使用 Pydantic 模型进行数据验证
4. 实现 AI 对话 REST API 端点
5. 用 Day 22 前端对接后端，替换 mock 模式

### 与后续课程的衔接
- **Day 8** 函数 → FastAPI 路由函数处理 HTTP 请求
- **Day 5** 字典/JSON → Pydantic 模型自动序列化 JSON
- **Day 11** 异常处理 → FastAPI HTTPException
- **Day 12-19** API 调用/工具 → 后端封装大模型逻辑
- **Day 22** 前端 fetch → 今天提供后端 API 地址
- **Day 24** SSE 流式 + CORS + 数据库 → 后端进阶

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：FastAPI 入门

#### 1.1 为什么选择 FastAPI

| 框架 | 优势 | 劣势 |
|------|------|------|
| Flask | 简单、生态成熟 | 同步、无自动文档 |
| Django | 全功能、ORM | 重、学习曲线陡 |
| **FastAPI** | 异步、自动文档、类型提示 | 相对较新 |

**FastAPI 核心优势**

- 基于 Python 类型提示，自动生成 API 文档
- 原生异步支持（async/await）
- Pydantic 数据验证
- 性能接近 Node.js 和 Go
- AI 生态友好（LangChain、LlamaIndex 等推荐）

#### 1.2 安装与 Hello World

```bash
pip install fastapi uvicorn python-dotenv -i https://pypi.tuna.tsinghua.edu.cn/simple
```

```python
# day23/main.py
"""FastAPI Hello World"""

from fastapi import FastAPI

app = FastAPI(
    title="AI 聊天助手 API",
    description="大模型应用开发课程 - Day 23",
    version="1.0.0",
)

@app.get("/")
def root():
    return {"message": "AI 聊天助手 API 运行中", "docs": "/docs"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
```

**启动服务**

```bash
cd ~/llm-course/day23
uvicorn main:app --reload --port 8000
```

- 访问 http://localhost:8000 查看 API
- 访问 http://localhost:8000/docs 查看自动生成的 Swagger 文档

#### 1.3 项目结构

```
day23/
├── main.py              # FastAPI 入口
├── config.py            # 配置管理
├── models/
│   ├── __init__.py
│   └── schemas.py       # Pydantic 模型
├── routers/
│   ├── __init__.py
│   └── chat.py          # 聊天路由
├── services/
│   ├── __init__.py
│   └── llm.py           # 大模型服务
├── .env                 # 环境变量
└── requirements.txt
```

---

### 9:45 - 10:30 | 模块二：路由与 Pydantic

#### 2.1 路由基础

```python
from fastapi import FastAPI, Query, Path

app = FastAPI()

# GET 请求
@app.get("/items")
def list_items():
    return {"items": []}

# GET 带路径参数
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}

# GET 带查询参数
@app.get("/search")
def search(q: str = Query(..., min_length=1), limit: int = Query(10, ge=1, le=100)):
    return {"query": q, "limit": limit}

# POST 请求
@app.post("/items")
def create_item(data: dict):
    return {"created": data}
```

#### 2.2 Pydantic 数据模型

Pydantic 用 Python 类定义数据结构，自动验证和序列化。

```python
# day23/models/schemas.py
"""Pydantic 数据模型"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class Role(str, Enum):
    system = "system"
    user = "user"
    assistant = "assistant"


class Message(BaseModel):
    """单条消息"""
    role: Role
    content: str = Field(..., min_length=1, max_length=10000)

    class Config:
        json_schema_extra = {
            "example": {
                "role": "user",
                "content": "你好，请介绍一下自己",
            }
        }


class ChatRequest(BaseModel):
    """聊天请求"""
    messages: list[Message] = Field(..., min_length=1)
    temperature: Optional[float] = Field(0.7, ge=0, le=2)
    max_tokens: Optional[int] = Field(2048, ge=1, le=8192)

    class Config:
        json_schema_extra = {
            "example": {
                "messages": [
                    {"role": "user", "content": "什么是 FastAPI？"}
                ],
                "temperature": 0.7,
            }
        }


class ChatResponse(BaseModel):
    """聊天响应"""
    reply: str
    model: str = "deepseek-chat"
    usage: Optional[dict] = None


class ErrorResponse(BaseModel):
    """错误响应"""
    detail: str
    code: int = 400
```

#### 2.3 在路由中使用 Pydantic

```python
from fastapi import FastAPI, HTTPException
from models.schemas import ChatRequest, ChatResponse

app = FastAPI()

@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """聊天接口 - Pydantic 自动验证请求体"""
    # request.messages 已经是验证过的 Message 对象列表
    # 如果客户端发送了无效数据，FastAPI 自动返回 422 错误
    reply = f"收到 {len(request.messages)} 条消息"
    return ChatResponse(reply=reply)
```

**自动验证示例**

```bash
# 有效请求 → 200
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "你好"}]}'

# 无效请求（缺少 content）→ 422
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user"}]}'
```

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：配置管理与服务层

#### 3.1 配置管理

```python
# day23/config.py
"""应用配置"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    API_BASE_URL: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
    MODEL: str = os.getenv("MODEL", "deepseek-chat")
    DEFAULT_TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    DEFAULT_MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "2048"))
    SYSTEM_PROMPT: str = os.getenv(
        "SYSTEM_PROMPT",
        "你是一个友好的AI助手，回答简洁准确。",
    )


settings = Settings()
```

```bash
# day23/.env
DEEPSEEK_API_KEY=your-api-key-here
MODEL=deepseek-chat
TEMPERATURE=0.7
MAX_TOKENS=2048
```

#### 3.2 大模型服务层

```python
# day23/services/llm.py
"""大模型服务封装"""

import requests
from fastapi import HTTPException
from config import settings
from models.schemas import Message


class LLMService:
    def __init__(self):
        self.api_key = settings.API_KEY
        self.base_url = settings.API_BASE_URL
        self.model = settings.MODEL

    def chat(
        self,
        messages: list[Message],
        temperature: float = None,
        max_tokens: int = None,
    ) -> dict:
        """调用大模型 API"""
        if not self.api_key:
            raise HTTPException(status_code=500, detail="API Key 未配置")

        # 构建 messages（确保有 system prompt）
        api_messages = []
        has_system = any(m.role == "system" for m in messages)
        if not has_system:
            api_messages.append({
                "role": "system",
                "content": settings.SYSTEM_PROMPT,
            })
        for m in messages:
            api_messages.append({"role": m.role.value, "content": m.content})

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json={
                    "model": self.model,
                    "messages": api_messages,
                    "temperature": temperature or settings.DEFAULT_TEMPERATURE,
                    "max_tokens": max_tokens or settings.DEFAULT_MAX_TOKENS,
                },
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                timeout=60,
            )
            response.raise_for_status()
            data = response.json()

            return {
                "reply": data["choices"][0]["message"]["content"],
                "model": data.get("model", self.model),
                "usage": data.get("usage"),
            }

        except requests.exceptions.Timeout:
            raise HTTPException(status_code=504, detail="大模型 API 超时")
        except requests.exceptions.HTTPError as e:
            raise HTTPException(
                status_code=502,
                detail=f"大模型 API 错误: {e.response.status_code}",
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"服务内部错误: {str(e)}")


llm_service = LLMService()
```

#### 3.3 路由模块化

```python
# day23/routers/chat.py
"""聊天路由"""

from fastapi import APIRouter
from models.schemas import ChatRequest, ChatResponse
from services.llm import llm_service

router = APIRouter(prefix="/api", tags=["聊天"])


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """AI 对话接口

  发送消息列表，获取 AI 回复。
    支持多轮对话（传入完整 messages 历史）。
    """
    result = llm_service.chat(
        messages=request.messages,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )
    return ChatResponse(**result)


@router.get("/models")
def list_models():
    """获取可用模型列表"""
    return {
        "models": [
            {"id": "deepseek-chat", "name": "DeepSeek Chat"},
        ],
        "default": "deepseek-chat",
    }
```

```python
# day23/main.py（更新）
"""FastAPI 应用入口"""

from fastapi import FastAPI
from routers import chat

app = FastAPI(
    title="AI 聊天助手 API",
    description="大模型应用开发课程 - Day 23",
    version="1.0.0",
)

app.include_router(chat.router)


@app.get("/")
def root():
    return {
        "message": "AI 聊天助手 API",
        "docs": "/docs",
        "chat": "/api/chat",
    }


@app.get("/health")
def health():
    return {"status": "ok"}
```

---

## 🌆 下午课程（14:00 - 17:00）

### 14:00 - 15:15 | 模块四：前后端联调

#### 4.1 启动后端

```bash
cd ~/llm-course/day23
uvicorn main:app --reload --port 8000
```

#### 4.2 测试 API

```bash
# 测试健康检查
curl http://localhost:8000/health

# 测试聊天接口
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "用一句话介绍 FastAPI"}
    ],
    "temperature": 0.7
  }'
```

**期望响应**

```json
{
  "reply": "FastAPI 是一个现代、高性能的 Python Web 框架...",
  "model": "deepseek-chat",
  "usage": {
    "prompt_tokens": 25,
    "completion_tokens": 50,
    "total_tokens": 75
  }
}
```

#### 4.3 更新前端对接后端

```javascript
// 修改 day22/app.js 中的配置
const CONFIG = {
    apiUrl: "http://localhost:8000/api/chat",
    useMock: false,  // 改为 false，使用真实后端
};

// 更新 sendToAPI 函数
async function sendToAPI(text) {
    messages.push({ role: "user", content: text });

    const response = await fetch(CONFIG.apiUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            messages: messages,
            temperature: 0.7,
        }),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || `HTTP ${response.status}`);
    }

    const data = await response.json();
    messages.push({ role: "assistant", content: data.reply });
    return data.reply;
}
```

> ⚠️ **注意**：此时前端 fetch 可能因 CORS 跨域报错。Day 24 将配置 CORS。临时方案：用 Swagger UI（/docs）测试后端。

#### 4.4 用 Swagger UI 测试

访问 http://localhost:8000/docs

1. 展开 `POST /api/chat`
2. 点击「Try it out」
3. 填入请求体
4. 点击「Execute」
5. 查看响应

---

### 15:15 - 15:30 | 课间休息

---

### 15:30 - 17:00 | 模块五：进阶功能

#### 5.1 多轮对话 API

```python
# day23/routers/chat.py 补充

@router.post("/chat/simple")
def simple_chat(message: str = Query(..., min_length=1)):
    """简化接口：单条消息，自动管理历史"""
    from models.schemas import Message, Role

    # 实际项目中，历史存在数据库（Day 24）
    messages = [Message(role=Role.user, content=message)]
    result = llm_service.chat(messages)
    return ChatResponse(**result)
```

#### 5.2 错误处理中间件

```python
# day23/main.py 补充

from fastapi import Request
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"未处理异常: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "服务器内部错误", "code": 500},
    )
```

#### 5.3 请求日志

```python
# day23/main.py 补充

import time
from fastapi import Request


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    print(f"{request.method} {request.url.path} - {response.status_code} - {duration:.2f}s")
    return response
```

#### 5.4 下午综合项目：完整后端

```python
# day23/requirements.txt
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
pydantic>=2.5.0
python-dotenv>=1.0.0
requests>=2.31.0
```

**验证清单**

| 测试 | 方法 | 期望 |
|------|------|------|
| 健康检查 | GET /health | `{"status": "ok"}` |
| API 文档 | GET /docs | Swagger UI 页面 |
| 单轮对话 | POST /api/chat | 返回 AI 回复 |
| 多轮对话 | POST 带历史 messages | 上下文连贯 |
| 无效请求 | POST 空 messages | 422 验证错误 |
| 无 API Key | 删除 .env 中的 Key | 500 错误提示 |

---

## 🌙 晚自习（19:00 - 21:00）

### 19:00 - 20:00 | FastAPI 知识补充

#### 依赖注入（了解）

```python
from fastapi import Depends

def get_llm_service():
    return llm_service

@router.post("/chat")
def chat(request: ChatRequest, llm: LLMService = Depends(get_llm_service)):
    result = llm.chat(request.messages)
    return ChatResponse(**result)
```

#### 异步路由（了解）

```python
import httpx

@router.post("/chat")
async def chat_async(request: ChatRequest):
    async with httpx.AsyncClient() as client:
        response = await client.post(...)
    return ChatResponse(...)
```

### 20:00 - 21:00 | 自习答疑

- 确保后端 API 通过 Swagger UI 测试通过
- 理解项目结构和各模块职责
- 预习 Day 24 SSE 流式与 CORS

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | FastAPI 安装与项目结构 | |
| 2 | 路由定义（GET/POST） | |
| 3 | Pydantic 模型定义与验证 | |
| 4 | 请求体/响应体类型声明 | |
| 5 | 环境变量与配置管理 | |
| 6 | 服务层封装大模型 API | |
| 7 | 路由模块化（APIRouter） | |
| 8 | 错误处理（HTTPException） | |
| 9 | Swagger 自动文档 | |
| 10 | 前后端联调（API 测试） | |

---

## 📝 课后作业

### 必做题

1. **完成后端 API**：实现 /api/chat 端点，Swagger UI 测试通过
2. **多轮对话测试**：用 curl 或 Swagger 测试 3 轮连续对话
3. **Git 提交**：`git commit -m "Day 23: FastAPI 后端与 AI 对话 API"`

### 选做题

4. 添加 `/api/chat/translate` 端点（翻译专用 system prompt）
5. 实现请求频率限制（简单版：每分钟最多 20 次）
6. 添加 API Key 认证（Header: X-API-Key）

---

## 💡 常见问题 FAQ

**Q1: FastAPI 和 Flask 应该学哪个？**

A: 本课程选 FastAPI，因为它是当前 AI 应用开发的主流选择。学会 FastAPI 后看 Flask 代码也很容易。

**Q2: Pydantic v1 和 v2 有什么区别？**

A: 本课程使用 Pydantic v2（`model_config` 替代 `class Config`）。安装时确保 `pydantic>=2.0`。

**Q3: 为什么前端调用后端报 CORS 错误？**

A: 浏览器的同源策略限制。Day 24 将通过 `CORSMiddleware` 解决。今天先用 Swagger UI 测试。

**Q4: uvicorn --reload 是什么意思？**

A: 开发模式，代码修改后自动重启服务。生产环境不用 --reload。

**Q5: 如何把 API Key 放在后端而不是前端？**

A: 这正是今天做的方式——API Key 在 `.env` 中，后端读取后调用大模型 API。前端只调用自己的后端，不接触 Key。

---

## 🔮 明日预习

**Day 24: FastAPI 后端开发（下）**

明天你将学习：

- **SSE 流式接口**实现（逐字返回 AI 回答）
- **CORS 跨域配置**（前后端联调）
- **SQLite + SQLAlchemy** 对话历史持久化
- **网页版 ChatGPT 克隆**完整联调

**预习建议**：确保今天后端可正常运行，前端文件齐全。

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 23*
