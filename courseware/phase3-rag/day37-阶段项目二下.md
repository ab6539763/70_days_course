# Day 37: 阶段项目二（下）——企业级知识库问答系统 Day 2

> **培训阶段**: 第三阶段 RAG 应用开发 | **第 7 周 | **学习时长**: 约 6-8 小时  
> **今日关键词**: Gradio 前端、会话管理、Query Rewriting、Docker 部署、Ragas 评估报告

---

## 📍 课程导航

### 上节回顾

**Day 36** 你完成了企业知识库项目的后端核心：
- 项目架构设计与工程搭建
- RAG 引擎封装（加载→分割→嵌入→存储→查询）
- 文档管理 API（上传/列表/删除）
- 问答 API 与联调测试

今天是项目 **第二天**——完成前端界面、高级功能集成、部署上线，交付可演示的完整系统。

### 本节学习目标

完成本日学习后，你将能够：

1. 用 Gradio 构建知识库问答前端界面
2. 实现多轮对话与会话管理
3. 集成 Query Rewriting 提升检索质量
4. 生成 Ragas 评估报告
5. 使用 Docker 容器化部署
6. 完成项目文档（README + API 文档）
7. 交付可演示的企业级知识库问答系统

### 与后续课程的衔接

- **Day 38** 项目答辩与代码评审
- **Day 39+** Agent 开发将在本项目基础上扩展
- 本项目可直接作为简历项目或毕业设计基础

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：Gradio 前端界面

#### 1.1 界面设计

```
┌─────────────────────────────────────────────────┐
│  🏢 企业知识库问答系统                              │
├──────────────────┬──────────────────────────────┤
│  📁 文档管理      │  💬 智能问答                   │
│  ┌────────────┐  │  ┌────────────────────────┐  │
│  │ 上传文档    │  │  │ 对话历史               │  │
│  │ [选择文件]  │  │  │                        │  │
│  │ [上传]     │  │  │ Q: 年假多少天？         │  │
│  └────────────┘  │  │ A: 满一年10天...       │  │
│  文档列表:        │  │                        │  │
│  - 员工手册.pdf   │  └────────────────────────┘  │
│  - FAQ.csv       │  ┌────────────────────────┐  │
│  - 技术文档.md    │  │ [输入问题...]    [发送] │  │
│                  │  └────────────────────────┘  │
├──────────────────┴──────────────────────────────┤
│  📊 系统状态: 5 文档 | 128 chunks | 运行正常       │
└─────────────────────────────────────────────────┘
```

#### 1.2 Gradio 前端实现

```python
# app/frontend/gradio_app.py
"""Gradio 前端界面"""
import gradio as gr
import requests
import uuid

API_BASE = "http://localhost:8000"


def upload_file(file):
    if file is None:
        return "请选择文件", get_doc_list()
    with open(file.name, "rb") as f:
        resp = requests.post(
            f"{API_BASE}/api/documents/upload",
            files={"file": (file.name.split("/")[-1], f)},
        )
    if resp.status_code == 200:
        data = resp.json()
        return f"✅ {data['message']}: {data['filename']}", get_doc_list()
    return f"❌ 上传失败: {resp.text}", get_doc_list()


def get_doc_list():
    try:
        docs = requests.get(f"{API_BASE}/api/documents/").json()
        if not docs:
            return "暂无文档"
        lines = []
        for d in docs:
            status = "✅" if d["status"] == "indexed" else "⏳"
            lines.append(f"{status} {d['filename']} ({d['chunk_count']} chunks)")
        return "\n".join(lines)
    except Exception:
        return "⚠️ 无法连接后端服务"


def chat(message, history, session_id):
    if not message.strip():
        return history, ""
    try:
        resp = requests.post(f"{API_BASE}/api/chat/ask", json={
            "question": message, "session_id": session_id,
        })
        data = resp.json()
        answer = data["answer"]
        if data.get("sources"):
            answer += f"\n\n📎 参考来源: {', '.join(data['sources'])}"
        history.append((message, answer))
    except Exception as e:
        history.append((message, f"❌ 请求失败: {e}"))
    return history, ""


def get_stats():
    try:
        stats = requests.get(f"{API_BASE}/api/chat/stats").json()
        return f"📊 {stats['total_chunks']} chunks | 集合: {stats['collection_name']}"
    except Exception:
        return "⚠️ 后端未连接"


def create_app():
    session_id = str(uuid.uuid4())

    with gr.Blocks(title="企业知识库问答系统") as demo:
        gr.Markdown("# 🏢 企业知识库问答系统")
        gr.Markdown(get_stats())

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 📁 文档管理")
                file_input = gr.File(label="上传文档", file_types=[".txt", ".md", ".pdf", ".csv"])
                upload_btn = gr.Button("上传并索引", variant="primary")
                upload_status = gr.Textbox(label="上传状态", interactive=False)
                doc_list = gr.Textbox(label="文档列表", lines=8, interactive=False)
                refresh_btn = gr.Button("刷新列表")

            with gr.Column(scale=2):
                gr.Markdown("### 💬 智能问答")
                chatbot = gr.Chatbot(label="对话", height=400)
                msg_input = gr.Textbox(label="输入问题", placeholder="例如：年假有多少天？")
                with gr.Row():
                    send_btn = gr.Button("发送", variant="primary")
                    clear_btn = gr.Button("清空对话")

        upload_btn.click(upload_file, [file_input], [upload_status, doc_list])
        refresh_btn.click(get_doc_list, outputs=doc_list)
        send_btn.click(chat, [msg_input, chatbot, gr.State(session_id)], [chatbot, msg_input])
        msg_input.submit(chat, [msg_input, chatbot, gr.State(session_id)], [chatbot, msg_input])
        clear_btn.click(lambda: ([], ""), outputs=[chatbot, msg_input])

        gr.Examples(
            examples=["年假有多少天？", "报销流程是什么？", "远程办公政策？"],
            inputs=msg_input,
        )

    return demo


if __name__ == "__main__":
    demo = create_app()
    demo.launch(server_name="0.0.0.0", server_port=7860)
```

---

### 9:45 - 10:30 | 模块二：高级功能集成

#### 2.1 Query Rewriting 集成

```python
# app/core/query_enhancer.py
"""查询增强模块"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.config import get_settings


class QueryEnhancer:
    def __init__(self):
        settings = get_settings()
        self.llm = ChatOpenAI(model=settings.llm_model, temperature=0)
        self.rewrite_chain = (
            ChatPromptTemplate.from_template(
                "将以下口语化/模糊问题改写为清晰的知识库检索查询。"
                "只输出改写后的查询，不要解释。\n\n原始问题：{question}"
            )
            | self.llm | StrOutputParser()
        )

    def enhance(self, question: str) -> str:
        if len(question) < 5:
            return question
        oral_markers = ["咋", "啥", "吗", "呢", "啊", "咋整", "咋搞"]
        if any(m in question for m in oral_markers):
            return self.rewrite_chain.invoke({"question": question})
        return question
```

在 RAG 引擎中集成：

```python
# 在 rag_engine.py 的 ask 方法中
from app.core.query_enhancer import QueryEnhancer

class RAGEngine:
    def __init__(self):
        # ... 现有代码 ...
        self.query_enhancer = QueryEnhancer()

    def ask(self, question: str) -> dict:
        enhanced_q = self.query_enhancer.enhance(question)
        retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": self.settings.retrieval_k}
        )
        docs = retriever.invoke(enhanced_q)
        answer = self.chain.invoke(enhanced_q)
        sources = list(set(d.metadata.get("source", "?") for d in docs))
        return {
            "answer": answer, "sources": sources,
            "original_question": question,
            "enhanced_question": enhanced_q,
        }
```

#### 2.2 会话管理

```python
# app/core/session_manager.py
"""会话管理"""
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


class SessionManager:
    def __init__(self, rag_engine):
        self.rag_engine = rag_engine
        self.sessions = {}

    def get_history(self, session_id: str) -> ChatMessageHistory:
        if session_id not in self.sessions:
            self.sessions[session_id] = ChatMessageHistory()
        return self.sessions[session_id]

    def clear_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]

    def get_session_count(self) -> int:
        return len(self.sessions)
```

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：Ragas 评估报告

```python
# app/services/eval_service.py
"""RAG 评估服务"""
import json
from datetime import datetime
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision
from datasets import Dataset
from app.core.rag_engine import RAGEngine


class EvalService:
    def __init__(self, rag_engine: RAGEngine):
        self.rag = rag_engine

    def run_evaluation(self, test_file: str = "eval_dataset.json") -> dict:
        with open(test_file, encoding="utf-8") as f:
            test_data = json.load(f)

        questions, answers, contexts_list, ground_truths = [], [], [], []
        for item in test_data:
            result = self.rag.ask(item["question"])
            questions.append(item["question"])
            answers.append(result["answer"])
            retriever = self.rag.vectorstore.as_retriever(search_kwargs={"k": 3})
            docs = retriever.invoke(item["question"])
            contexts_list.append([d.page_content for d in docs])
            ground_truths.append(item["ground_truth"])

        dataset = Dataset.from_dict({
            "question": questions, "answer": answers,
            "contexts": contexts_list, "ground_truth": ground_truths,
        })

        result = evaluate(
            dataset,
            metrics=[faithfulness, answer_relevancy, context_precision],
            llm=self.rag.llm, embeddings=self.rag.embeddings,
        )

        report = {
            "timestamp": datetime.now().isoformat(),
            "total_questions": len(test_data),
            "metrics": {k: float(v) for k, v in result.items() if isinstance(v, (int, float))},
        }

        with open("data/eval_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        return report
```

---

## 🌆 下午课程（14:00 - 17:00）

### 14:00 - 15:30 | 模块四：Docker 部署

#### 4.1 Dockerfile

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

RUN mkdir -p data/uploads data/chromadb

EXPOSE 8000 7860

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 4.2 Docker Compose

```yaml
# docker-compose.yml
version: "3.8"

services:
  kb-api:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  kb-frontend:
    build: .
    command: python -m app.frontend.gradio_app
    ports:
      - "7860:7860"
    env_file:
      - .env
    depends_on:
      - kb-api
    restart: unless-stopped
```

#### 4.3 部署命令

```bash
# 构建并启动
docker compose up -d --build

# 查看日志
docker compose logs -f kb-api

# 停止
docker compose down
```

---

### 15:30 - 15:45 | 课间休息

---

### 15:45 - 17:00 | 模块五：项目文档与交付

#### 5.1 README.md

```markdown
# 企业级知识库问答系统

基于 RAG 技术的企业内部知识库智能问答系统。

## 功能特性

- 📁 多格式文档上传（PDF/TXT/MD/CSV）
- 🔍 智能语义检索 + Query Rewriting
- 💬 多轮对话支持
- 📎 回答引用来源
- 📊 Ragas 评估报告
- 🐳 Docker 一键部署

## 技术栈

- 后端: FastAPI + LangChain + Chroma
- 前端: Gradio
- LLM: DeepSeek-V3
- Embedding: text-embedding-3-small

## 快速开始

\`\`\`bash
# 1. 配置环境
cp .env.example .env  # 填入 API Key

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动后端
uvicorn app.main:app --reload --port 8000

# 4. 启动前端
python -m app.frontend.gradio_app

# 5. 访问
# API 文档: http://localhost:8000/docs
# 前端界面: http://localhost:7860
\`\`\`

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/documents/upload | 上传文档 |
| GET | /api/documents/ | 文档列表 |
| DELETE | /api/documents/{id} | 删除文档 |
| POST | /api/chat/ask | 智能问答 |
| GET | /api/chat/stats | 系统统计 |

## 项目结构

见 Day 36 课程讲义

## 评估报告

运行评估: `python -m app.services.eval_service`
```

#### 5.2 项目交付清单

| 交付物 | 路径 | 状态 |
|--------|------|------|
| 后端 API | `app/` | ✅ |
| Gradio 前端 | `app/frontend/` | ✅ |
| Docker 部署 | `Dockerfile`, `docker-compose.yml` | ✅ |
| 评估报告 | `data/eval_report.json` | ✅ |
| 项目文档 | `README.md` | ✅ |
| 测试脚本 | `tests/` | ✅ |

#### 5.3 最终演示流程

```
1. 启动系统（Docker 或本地）
2. 上传 3 个企业文档（员工手册、FAQ、技术文档）
3. 等待索引完成
4. 演示 5 个问答场景：
   a. 直接问题："年假有多少天？"
   b. 口语化："咋请假啊"
   c. 多轮对话："报销流程？" → "需要多久？"
   d. 无答案问题："公司上市计划？"
   e. 跨文档："公司的福利政策有哪些？"
5. 展示评估报告数据
6. 展示 API 文档（Swagger）
```

---

## 🌙 晚自习（19:00 - 21:00）

### 19:00 - 20:00

1. 完成所有功能联调
2. 运行 Ragas 评估，生成报告
3. 完善 README 文档
4. 准备 Day 38 答辩 PPT（5-8 页）

### 20:00 - 21:00

- 模拟答辩演练（每人 5 分钟）
- 互相 Code Review

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | Gradio 前端界面开发 | |
| 2 | Query Rewriting 集成 | |
| 3 | 会话管理 | |
| 4 | Ragas 评估报告生成 | |
| 5 | Docker 容器化部署 | |
| 6 | 项目文档编写 | |
| 7 | 完整系统交付 | |

---

## 📝 课后作业

### 必做题

1. **完整系统**：前后端联调通过，可演示
2. **评估报告**：Ragas 评估平均分 > 0.7
3. **答辩 PPT**：5-8 页，包含架构图、Demo 截图、评估数据
4. **Git 提交**：`git commit -m "Day 37: 企业知识库项目 Day2"`

### 选做题

5. 添加用户认证（JWT）
6. 实现文档删除时同步清理向量库 chunks

---

## 💡 常见问题 FAQ

**Q1: Gradio 连不上后端？**

A: 确认后端已启动（`uvicorn app.main:app --port 8000`），检查 `API_BASE` 地址。

**Q2: Docker 构建很慢？**

A: 使用国内 pip 镜像源。Dockerfile 中已配置清华源。

**Q3: 评估分数很低怎么办？**

A: 检查知识库文档是否覆盖测试问题、调整 chunk_size、启用 Query Rewriting。

**Q4: 答辩需要演示什么？**

A: 上传文档 → 问答演示（含口语化问题）→ 展示来源引用 → 评估数据。控制在 5 分钟内。

---

## 🔮 明日预习

**Day 38: 项目答辩与代码评审**

- 答辩流程与评分标准
- 代码评审要点
- 第三阶段（RAG）学习总结
- 第四阶段（Agent）学习预告

**准备建议**：完善答辩 PPT，准备 3 个可能被问到的技术问题和回答。

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 37*
