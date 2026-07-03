# Day 38: 项目答辩与代码评审

> **培训阶段**: 第三阶段 RAG 应用开发 | **第 7 周 | **学习时长**: 约 6-8 小时  
> **今日关键词**: 项目答辩、代码评审、RAG 阶段总结、Agent 预告

---

## 📍 课程导航

### 上节回顾

**Day 36-37** 你完成了企业级知识库问答系统的开发与部署：
- Day 36: 后端 API + RAG 引擎 + 文档管理
- Day 37: Gradio 前端 + Query Rewriting + Docker 部署 + Ragas 评估

今天是第三阶段的 **收官日**——项目答辩、代码评审、学习总结，并为第四阶段 Agent 开发做准备。

### 本节学习目标

完成本日学习后，你将能够：

1. 完成项目答辩展示（5 分钟演讲 + 3 分钟 Q&A）
2. 参与代码评审，提出和接受改进建议
3. 系统回顾第三阶段 RAG 知识体系
4. 理解常见代码问题及最佳实践
5. 制定第四阶段 Agent 开发学习计划
6. 获得第三阶段学习成果认证

### 与后续课程的衔接

- **Day 39** 开始第四阶段：Agent 开发（LangGraph、工具调用）
- 本项目代码将作为 Agent 项目的知识库基础
- RAG + Agent 结合 = 企业级 AI 应用完整形态

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:30 | 模块一：答辩流程与评分标准

#### 1.1 答辩流程

```
09:30 - 09:35  抽签决定答辩顺序
09:35 - 12:00  答辩环节（每人约 8 分钟）
  ├── 5 分钟: 项目展示（PPT + Live Demo）
  └── 3 分钟: 评委提问
12:00 - 12:30  休息
```

#### 1.2 评分标准（总分 100）

| 维度 | 权重 | 评分要点 |
|------|------|----------|
| 功能完整性 | 30% | 文档上传、问答、来源引用、多轮对话 |
| 技术深度 | 25% | RAG  pipeline 完整性、高级技术应用 |
| 代码质量 | 20% | 项目结构、命名规范、错误处理 |
| 演示效果 | 15% | Demo 流畅度、问题应对能力 |
| 文档与评估 | 10% | README、API 文档、Ragas 报告 |

| 等级 | 分数 | 说明 |
|------|------|------|
| 优秀 | 90-100 | 功能完整 + 高级特性 + 高质量代码 |
| 良好 | 75-89 | 核心功能完整，代码规范 |
| 合格 | 60-74 | 基本功能可用，有明显改进空间 |
| 不合格 | <60 | 核心功能缺失，需重做 |

#### 1.3 答辩 PPT 模板

```
第 1 页: 封面
  - 项目名称、姓名、日期

第 2 页: 问题背景
  - 企业知识分散的痛点
  - 项目要解决什么问题

第 3 页: 系统架构
  - 架构图（前端 + API + RAG 引擎 + 存储）
  - 技术选型及理由

第 4 页: 核心功能演示
  - 文档上传截图
  - 问答效果截图（含来源引用）
  - 口语化问题处理效果

第 5 页: 技术亮点
  - Query Rewriting
  - Ragas 评估数据
  - Docker 部署

第 6 页: 评估与优化
  - Ragas 评估分数
  - 优化前后对比
  - 已知问题与改进计划

第 7 页: 总结与展望
  - 项目收获
  - 下一步计划（Agent 集成）
```

---

### 9:30 - 12:00 | 模块二：项目答辩

#### 2.1 答辩演示脚本

```
[开场 30秒]
"各位老师好，我是 XXX。今天答辩的项目是「企业级知识库问答系统」。
该系统基于 RAG 技术，解决企业内部知识分散、检索困难的痛点。"

[架构介绍 1分钟]
"系统采用前后端分离架构。后端基于 FastAPI + LangChain，
向量库使用 Chroma，LLM 使用 DeepSeek。
前端使用 Gradio 快速构建交互界面。"

[Live Demo 3分钟]
1. 打开 Gradio 界面，展示已有文档
2. 上传一个新文档，等待索引
3. 提问："年假有多少天？" → 展示回答和来源
4. 口语化提问："咋请假啊" → 展示 Query Rewriting 效果
5. 多轮对话："报销流程？" → "需要多久？"
6. 无答案问题："公司上市计划？" → 展示"无法回答"

[技术亮点 1分钟]
"项目集成了 Query Rewriting 处理口语化查询，
使用 Ragas 框架评估，Faithfulness 达到 0.85。
支持 Docker 一键部署。"

[总结 30秒]
"通过本项目，我掌握了 RAG 全技术栈，
从文档处理到向量检索到 LLM 生成的完整流水线。
下一步计划集成 Agent 能力，实现更复杂的任务处理。谢谢！"
```

#### 2.2 常见答辩问题与参考回答

**Q1: 你的 RAG 系统和直接用 ChatGPT 有什么区别？**

A: 三个核心区别：
1. **私有知识**：系统基于企业内部文档回答，ChatGPT 没有这些知识
2. **来源可追溯**：每个回答都标注引用来源，便于核实
3. **数据安全**：文档不离开企业服务器，ChatGPT 会上传数据

**Q2: 如果检索到的文档不相关怎么办？**

A: 多层保障：
1. Query Rewriting 优化查询表述
2. 调整 k 值和 chunk_size 参数
3. Prompt 约束"只根据资料回答，无关则说明"
4. 后续可集成 Rerank 重排序（Day 33 技术）

**Q3: 向量库能支撑多大规模？**

A: Chroma 支持百万级 chunks，对于 500 人企业完全够用。如果扩展到集团级，可迁移到 Milvus。

**Q4: 文档更新后如何同步？**

A: 当前方案：重新上传 → 自动索引新 chunks。改进方案：按 source 删除旧 chunks 后重新索引。

**Q5: 评估分数怎么解读？**

A:
- Faithfulness > 0.8：回答忠实于检索内容，幻觉少
- Answer Relevancy > 0.8：回答与问题相关
- Context Precision > 0.7：检索结果精准
- 低于 0.7 的指标需要针对性优化

**Q6: LangChain 和 LlamaIndex 你为什么选 LangChain？**

A: 本项目需要 FastAPI 深度集成和后续 Agent 扩展，LangChain 的 LCEL 和 LangGraph 生态更适合。LlamaIndex 在纯 RAG 场景更简洁，但 Agent 能力不如 LangChain。

**Q7: 生产环境还需要做什么？**

A:
1. 用户认证与权限控制
2. Milvus 替换 Chroma
3. 异步索引任务队列（Celery）
4. 监控告警（Prometheus + Grafana）
5. 日志审计
6. HTTPS 和安全加固

---

## 🌆 下午课程（14:00 - 17:00）

### 14:00 - 15:30 | 模块三：代码评审

#### 3.1 代码评审清单

**项目结构**

| 检查项 | 标准 | 常见问题 |
|--------|------|----------|
| 目录结构 | 分层清晰（api/core/services/models） | 所有代码放一个文件 |
| 配置管理 | 使用 .env + Settings 类 | API Key 硬编码 |
| 依赖管理 | requirements.txt 版本锁定 | 缺少依赖文件 |

**代码质量**

| 检查项 | 标准 | 常见问题 |
|--------|------|----------|
| 命名规范 | 类名大驼峰，函数蛇形 | 拼音命名 |
| 错误处理 | API 层有 try/except 和 HTTP 错误码 | 无错误处理 |
| 类型注解 | 函数参数和返回值有类型 | 无类型注解 |
| 文档字符串 | 核心类和函数有 docstring | 无注释 |

**RAG 专项**

| 检查项 | 标准 | 常见问题 |
|--------|------|----------|
| Prompt 设计 | 有约束、要求引用来源 | 无约束导致幻觉 |
| 检索参数 | k 值、chunk_size 可配置 | 硬编码参数 |
| 来源追溯 | 回答附带 metadata 来源 | 无来源信息 |
| 异常处理 | 无检索结果时有兜底 | 返回空回答 |

#### 3.2 典型代码问题与修复

**问题 1：API Key 硬编码**

```python
# ❌ 错误
llm = ChatOpenAI(api_key="sk-xxx", model="deepseek-chat")

# ✅ 正确
from app.config import get_settings
settings = get_settings()
llm = ChatOpenAI(model=settings.llm_model)
```

**问题 2：无错误处理**

```python
# ❌ 错误
@router.post("/ask")
async def ask(req: ChatRequest):
    result = rag_engine.ask(req.question)
    return result

# ✅ 正确
@router.post("/ask")
async def ask(req: ChatRequest):
    try:
        result = rag_engine.ask(req.question)
        return ChatResponse(**result, session_id=req.session_id)
    except Exception as e:
        raise HTTPException(500, f"问答服务异常: {str(e)}")
```

**问题 3：RAG 链无来源**

```python
# ❌ 错误
def ask(self, question):
    return self.chain.invoke(question)

# ✅ 正确
def ask(self, question) -> dict:
    docs = self.retriever.invoke(question)
    answer = self.chain.invoke(question)
    return {
        "answer": answer,
        "sources": [d.metadata.get("source") for d in docs],
    }
```

#### 3.3 互评流程

```
1. 两人一组，交换 GitHub 仓库链接
2. 按评审清单逐项检查（30 分钟）
3. 记录问题清单（至少 3 条建议）
4. 面对面反馈（15 分钟）
5. 提交评审报告
```

**评审报告模板**

```markdown
# 代码评审报告

## 评审信息
- 评审人: XXX
- 被评审人: XXX
- 项目: 企业知识库问答系统
- 日期: 2026-XX-XX

## 总体评价
（优秀/良好/合格/需改进）

## 优点（至少 2 条）
1. ...
2. ...

## 改进建议（至少 3 条）
1. [严重] ...
2. [建议] ...
3. [可选] ...

## 评分
- 项目结构: /10
- 代码质量: /10
- RAG 实现: /10
- 文档完整: /10
- 总分: /40
```

---

### 15:30 - 15:45 | 课间休息

---

### 15:45 - 17:00 | 模块四：第三阶段学习总结

#### 4.1 RAG 知识体系回顾

```
第三阶段：RAG 应用开发（Day 25-38，共 14 天）

Week 5: LangChain 基础
├── Day 25: LangChain 入门（Model I/O、Chain）
├── Day 26: LCEL 表达式与链
├── Day 27: Memory 记忆机制
├── Day 28: 文档加载与分割
├── Day 29: 向量数据库（Chroma / Milvus）
└── Day 30: 完整 RAG 系统搭建

Week 6: 高级 RAG + 评估
├── Day 31: 周测与 RAG 调优
├── Day 32: 高级 RAG 上（Query Rewriting / Multi-Query / HyDE）
├── Day 33: 高级 RAG 下（混合检索 / Rerank / 父文档检索）
├── Day 34: RAG 评估（Ragas）
└── Day 35: LlamaIndex 框架

Week 7: 项目实战
├── Day 36: 企业知识库项目 Day 1（后端 API）
├── Day 37: 企业知识库项目 Day 2（前端 + 部署）
└── Day 38: 项目答辩与代码评审 ← 今天
```

#### 4.2 核心技能矩阵

| 技能 | 掌握要求 | 对应天数 |
|------|----------|----------|
| LangChain 开发 | 独立搭建 LCEL 链 | Day 25-26 |
| 对话记忆 | RunnableWithMessageHistory | Day 27 |
| 文档工程 | 加载/分割/质检 | Day 28 |
| 向量检索 | Chroma/Milvus + Retriever | Day 29 |
| RAG 系统 | 端到端流水线 | Day 30 |
| 系统调优 | chunk/Prompt/k 值调优 | Day 31 |
| 查询增强 | Rewriting/Multi-Query/HyDE | Day 32 |
| 检索优化 | 混合检索/Rerank/父文档 | Day 33 |
| 量化评估 | Ragas 框架 | Day 34 |
| 框架对比 | LlamaIndex | Day 35 |
| 项目交付 | 企业级完整项目 | Day 36-38 |

#### 4.3 第三阶段结业标准

| 要求 | 标准 |
|------|------|
| 出勤 | 14 天中至少到课 12 天 |
| 周测 | Day 31 周测 ≥ 60 分 |
| 项目 | 答辩 ≥ 60 分 |
| 代码 | GitHub 有完整提交记录 |
| 评估 | Ragas Faithfulness ≥ 0.7 |

---

### 17:00 - 17:30 | 模块五：第四阶段预告

#### 5.1 Agent 开发学习路线

```
Week 7-8: Agent 开发（Day 39-50）

Day 39-40: Agent 基础概念 + LangGraph 入门
Day 41-42: 工具调用 (Function Calling)
Day 43-44: ReAct Agent 实现
Day 45-46: 多 Agent 协作
Day 47-48: Agent + RAG 集成
Day 49-50: 阶段项目三（智能客服 Agent）
```

#### 5.2 RAG + Agent = 完整 AI 应用

```
当前能力（RAG）:
  用户提问 → 检索知识库 → 生成回答

即将学习（Agent）:
  用户提问 → Agent 分析意图 → 选择工具
    ├── 知识库检索（RAG）
    ├── 数据库查询
    ├── API 调用
    ├── 计算工具
    └── 多步推理 → 综合回答
```

#### 5.3 预习建议

1. 阅读 LangGraph 官方文档 Getting Started
2. 了解 Function Calling 概念
3. 保持企业知识库项目可运行（Agent 项目将复用）
4. 复习 LCEL 和 Runnable 接口（Agent 编排的基础）

---

## 🌙 晚自习（19:00 - 21:00）

### 19:00 - 20:00 | 结业与反思

1. 填写第三阶段学习反思表
2. 根据代码评审建议改进项目
3. 整理 GitHub 仓库（README、目录清理）

**学习反思表**

| 问题 | 你的回答 |
|------|----------|
| 第三阶段最大的收获？ | |
| 最困难的部分？ | |
| 项目中最满意的设计？ | |
| 如果重做会改变什么？ | |
| 对 Agent 阶段有什么期待？ | |

### 20:00 - 21:00 | 自由交流

- 分享项目开发中的趣事和踩坑
- 讨论 RAG 在实际工作中的应用前景
- 组队准备 Agent 阶段项目

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | 项目答辩展示 | |
| 2 | 代码评审方法与清单 | |
| 3 | 典型代码问题识别与修复 | |
| 4 | 第三阶段知识体系回顾 | |
| 5 | RAG 核心技能矩阵 | |
| 6 | Agent 开发预告 | |

---

## 📝 课后作业

### 必做题

1. **提交评审报告**：完成互评并提交评审报告
2. **项目优化**：根据评审建议至少修复 2 个问题
3. **学习反思**：填写反思表
4. **Git 提交**：`git commit -m "Day 38: 项目答辩与代码评审"`

### 选做题

5. 将答辩 PPT 和 Demo 录制为 5 分钟视频，上传 B 站/YouTube
6. 撰写技术博客：《从零搭建企业 RAG 系统实战》

---

## 💡 常见问题 FAQ

**Q1: 答辩紧张怎么办？**

A: 提前演练 2-3 遍，准备好 Demo 环境。评委关注的是你的思考过程，不是完美演示。说"这个问题我需要进一步研究"比编造答案更好。

**Q2: 代码评审被指出很多问题怎么办？**

A: 这是学习过程。优先修复「严重」问题，「建议」和「可选」可以后续迭代。每个优秀工程师都经历过大量 Code Review。

**Q3: 第三阶段没完全掌握怎么办？**

A: 重点确保 RAG 基础（Day 25-30）和项目（Day 36-37）掌握。高级技术（Day 32-33）可以在项目中逐步集成。Agent 阶段会继续巩固。

**Q4: 项目可以写进简历吗？**

A: 当然可以！建议格式：
```
企业级知识库问答系统 | 个人项目 | 2026.XX
- 基于 LangChain + FastAPI + Chroma 构建 RAG 问答系统
- 集成 Query Rewriting 和 Ragas 评估，Faithfulness 0.85
- 支持 PDF/TXT/CSV 多格式文档，Docker 容器化部署
技术栈: Python, LangChain, FastAPI, Chroma, Gradio, Docker
```

**Q5: 第四阶段 Agent 难吗？**

A: Agent 比 RAG 更抽象，但你在第三阶段积累的 LangChain 基础（LCEL、Runnable、Memory）是 Agent 的基石。难度递增但可行。

---

## 🔮 第四阶段预习

**Day 39: Agent 基础概念**

- 什么是 AI Agent
- Agent vs Chain vs RAG
- LangGraph 入门
- 第一个简单 Agent

**预习建议**：
1. 阅读 https://langchain-ai.github.io/langgraph/
2. 思考：企业知识库项目如何升级为 Agent？（如：自动判断是否需要检索、多工具协作）
3. 保持本阶段项目代码可运行

---

## 🎓 第三阶段结业寄语

恭喜你完成了 **第三阶段：RAG 应用开发** 的全部 14 天学习！

从 Day 25 的 LangChain 第一行代码，到 Day 38 的项目答辩，你已经：
- 掌握了 RAG 全技术栈（14 天 × 6-8 小时 = 约 90 小时学习）
- 独立交付了企业级知识库问答系统
- 具备了 **大模型应用开发工程师** 的核心技能

RAG 是大模型应用落地的「第一公里」，Agent 是「第二公里」。明天开始，你将进入更激动人心的 Agent 开发阶段。

**继续加油！Day 39 见！** 🚀

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 38*
