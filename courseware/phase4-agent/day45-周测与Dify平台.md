# Day 45: 周测与Dify平台

> **培训阶段**: 第四阶段 Agent 开发 | **第 7 周** | **学习时长**: 约 6-8 小时  
> **今日关键词**: 周测、Dify、低代码、工作流、可视化Agent

---

## 📍 课程导航

### 上节回顾

**Day 44** 学习了MCP与Agent生态相关内容。

**Day 44 核心收获回顾：**
- MCP Server开发
- Agent生态全景
- Cursor MCP集成

### 本节学习目标

完成本日学习后，你将能够：

1. 完成第四阶段第一周周测
2. 理解Dify平台架构
3. 用Dify创建Agent应用
4. 设计可视化工作流
5. 对接DeepSeek API

### 与后续课程的衔接

- **Day 46** 继续深入学习
- 回顾 **Day 44** 的相关内容

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 10:30 | 第四阶段第一周周测

**周测范围**：Day 39-44（ReAct、LangChain Agent、LangGraph、多Agent、MCP）

| 题型 | 数量 | 分值 |
|------|------|------|
| 选择题 | 10 | 20分 |
| 填空题 | 5 | 15分 |
| 简答题 | 3 | 30分 |
| 编程题 | 2 | 35分 |

**编程题预览**：
1. 用 LangGraph 实现带工具调用的 ReAct Agent
2. 编写一个 MCP Server 并提供 search 工具

---

### 10:45 - 12:00 | 模块：Dify 平台入门

#### Dify 架构

```
┌─────────────────────────────────────┐
│            Dify 平台                 │
│  ┌─────────┐  ┌─────────────────┐  │
│  │ 前端UI  │  │  工作流引擎      │  │
│  └─────────┘  └─────────────────┘  │
│  ┌─────────┐  ┌─────────────────┐  │
│  │ 知识库  │  │  Agent 编排     │  │
│  └─────────┘  └─────────────────┘  │
│  ┌─────────┐  ┌─────────────────┐  │
│  │ 模型管理│  │  API 发布       │  │
│  └─────────┘  └─────────────────┘  │
└─────────────────────────────────────┘
```

#### 安装 Dify

```bash
git clone https://github.com/langgenius/dify.git
cd dify/docker
cp .env.example .env
docker compose up -d
# 访问 http://localhost/install
```

#### 创建第一个 Agent 应用

1. 登录 Dify → 创建应用 → 选择「Agent」
2. 配置模型：添加 DeepSeek API
3. 添加工具：内置搜索、计算器
4. 编写系统提示词
5. 发布并测试


### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块二：Dify 平台深度

#### 2.1 Dify 核心功能矩阵

| 功能 | 说明 | 对应课程日 |
|------|------|-----------|
| 聊天助手 | 基础对话应用 | Day 15-19 |
| Agent | 工具调用 Agent | Day 39-43 |
| 工作流 | 可视化编排 | Day 41 LangGraph |
| 知识库 | RAG 检索 | Day 25-38 |
| 模型管理 | 多模型接入 | Day 12 |

#### 2.2 Dify 工作流节点类型

```
开始 → 问题分类 → 知识库检索 → LLM → 回答
                  ↓
              工具调用 → API → 代码执行 → 结束
```

常用节点：
- **LLM 节点**：调用大模型
- **知识检索节点**：RAG 检索
- **条件分支**：if/else 路由
- **HTTP 请求**：调用外部 API
- **代码节点**：Python 代码执行
- **变量聚合**：合并多路结果

#### 2.3 Dify API 集成

```python
# day45/dify_client.py
import requests

class DifyClient:
    def __init__(self, api_key: str, base_url: str = "http://localhost/v1"):
        self.api_key = api_key
        self.base_url = base_url
    
    def chat(self, query: str, user: str = "default", conversation_id: str = None):
        payload = {
            "inputs": {},
            "query": query,
            "response_mode": "blocking",
            "user": user,
        }
        if conversation_id:
            payload["conversation_id"] = conversation_id
        
        resp = requests.post(
            f"{self.base_url}/chat-messages",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json=payload,
        )
        return resp.json()
    
    def upload_knowledge(self, file_path: str, dataset_id: str):
        with open(file_path, "rb") as f:
            resp = requests.post(
                f"{self.base_url}/datasets/{dataset_id}/document/create_by_file",
                headers={"Authorization": f"Bearer {self.api_key}"},
                files={"file": f},
            )
        return resp.json()

# 使用
client = DifyClient(api_key="app-xxx")
result = client.chat("什么是 Agent？")
print(result["answer"])
```

---

## 周测详细说明

### 选择题示例

1. ReAct 框架中，Observation 的作用是？
   A. 触发 LLM 推理  B. 提供工具执行结果  C. 结束循环  D. 格式化输出
   **答案：B**

2. LangGraph 中 `add_conditional_edges` 的作用是？
   A. 添加无条件边  B. 根据状态动态路由  C. 删除节点  D. 并行执行
   **答案：B**

### 编程题评分标准

| 评分项 | 分值 | 标准 |
|--------|------|------|
| 代码可运行 | 10 | 无语法错误，依赖正确 |
| 功能正确 | 15 | 通过测试用例 |
| 代码规范 | 5 | 有注释和类型提示 |
| 错误处理 | 5 | 覆盖主要异常 |

### 10:30 - 10:45 | 课间休息

---

## 🌇 下午实操（14:00 - 17:30）

### 14:00 - 17:30 | 实操：Dify Agent 应用

1. 部署 Dify（Docker）
2. 创建「课程助手」Agent 应用
3. 上传 Day 25-38 的 RAG 知识库
4. 配置 Agent 工具和工作流
5. 发布 API 并用 Python 调用

```python
import requests
response = requests.post(
    "http://localhost/v1/chat-messages",
    headers={"Authorization": "Bearer app-xxx"},
    json={"inputs": {}, "query": "什么是RAG?", "response_mode": "blocking", "user": "test"}
)
print(response.json())
```

### 15:30 - 15:45 | 课间休息

---

### 15:45 - 17:30 | 扩展练习与知识巩固

完成上午核心内容后，继续优化项目代码，添加错误处理、日志记录和测试用例。对照知识清单逐项自查。

---

## 🌙 晚自习（19:00 - 21:00）

### 19:00 - 20:00 | 深度学习

复习 Day 45 内容，阅读官方文档，完成课后作业。

### 20:00 - 21:00 | 自习答疑

- 完成今天的实操项目和课后作业
- 确保代码可运行并提交 GitHub
- Git 提交：`git commit -m "Day 45: 周测与Dify平台"`
- 预习 Day 46 内容

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | 完成第四阶段第一周周测 | |
| 2 | 理解Dify平台架构 | |
| 3 | 用Dify创建Agent应用 | |
| 4 | 设计可视化工作流 | |
| 5 | 对接DeepSeek API | |

---

## 📝 课后作业

### 必做题

1. 完成 Day 45 实操项目
2. 通过所有测试用例
3. 编写学习笔记
4. Git 提交 day45/

### 选做题

- 扩展项目功能，添加额外工具或节点
- 阅读官方文档或相关论文
- 与同学讨论实现方案

---

## 💡 常见问题 FAQ

**Q1: Day 45 最重要的概念是什么？**

A: 参见上午课程核心模块，重点是周测。

**Q2: 代码运行报错怎么办？**

A: 检查依赖安装、API Key 配置、Python 版本。查看 FAQ 常见错误。

**Q3: 学不完怎么办？**

A: 必做题必须完成，选做题可根据时间选做。重点是理解核心概念。

---

## 🔮 明日预习

**Day 46**

继续学习后续内容，巩固今天学的周测。

**预习建议**：回顾今日笔记，提前安装明天所需依赖，浏览官方文档。

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 45 · 第四阶段 Agent 开发*


---

## 📚 深度学习资源

### 推荐阅读

1. 官方文档和教程（见上午课程参考链接）
2. 相关论文和博客文章
3. 开源项目源码阅读

### 关键概念复习

回顾 Day 44 到 Day 45 的知识串联，绘制思维导图。将今天学的知识与前三阶段（Python、RAG、Agent）的知识点关联起来。

---

## 🔧 环境检查清单

```bash
# 检查 Python 环境
python3 --version  # 需要 3.10+

# 检查核心依赖
pip list | grep -E "langchain|langgraph|openai"

# 检查 API Key
echo $DEEPSEEK_API_KEY | head -c 10  # 应显示 sk- 开头

# 检查 Git 状态
git status
git log --oneline -5
```

---

## 📊 学习进度追踪

| 阶段 | 天数 | 状态 |
|------|------|------|
| Python 基础 | Day 1-14 | ✅ 完成 |
| 大模型理论+Web | Day 15-24 | ✅ 完成 |
| RAG 开发 | Day 25-38 | ✅ 完成 |
| Agent 开发 | Day 39-50 | 🔄 进行中 |
| 微调与部署 | Day 51-57 | ⬜ 待开始 |
| 毕业与求职 | Day 58-70 | ⬜ 待开始 |

**当前进度**: Day 45 / 70 (64%)

---

## 🎯 今日学习成果检验

完成以下检验，确认今日学习目标达成：

1. **概念理解**：能用自己的话解释今天 3 个核心概念
2. **代码能力**：能独立编写今天讲义中的核心代码
3. **问题解决**：遇到错误能查阅文档自行解决
4. **知识关联**：能说明今天内容与前后课程的关联
5. **项目应用**：能将今天知识应用到实际项目中

---

## 💼 职业发展连接

今天学的技能在大模型应用开发岗位中的价值：

- **简历关键词**: 周测、Dify、低代码、工作流、可视化Agent
- **面试高频题**: 参见 FAQ 部分
- **项目展示**: 将今天代码整理到 GitHub 作品集
- **实战场景**: 参见下午实操项目

---

## 📝 学习笔记模板

```markdown
# Day 45 学习笔记

## 今日核心概念
1. 
2. 
3. 

## 代码实践记录
- 文件：
- 运行结果：
- 遇到的问题：

## 疑问与解答
- Q: 
- A: 

## 明日计划
- 
```



---

## 🔗 前后课程知识关联图

```
Day44 MCP → Day45 周测+Dify → Day46 工程化
```

---

## 🧪 实验记录表

| 实验编号 | 实验名称 | 预期结果 | 实际结果 | 是否通过 |
|----------|----------|----------|----------|----------|
| EXP-01 | 核心功能验证 | 正常运行 | | |
| EXP-02 | 边界条件测试 | 优雅降级 | | |
| EXP-03 | 性能基准测试 | 响应<5s | | |

---

## 📋 代码审查清单

在提交代码前，逐项检查：

- [ ] 代码有完整的 docstring 和类型提示
- [ ] 所有依赖在 requirements.txt 中声明
- [ ] API Key 通过环境变量读取，不硬编码
- [ ] 错误处理覆盖主要异常路径
- [ ] 代码可以通过 `python -m pytest` 或手动测试
- [ ] Git 提交信息清晰描述变更

---

## 🗣️ 课堂讨论话题

1. 今天学的内容在实际工作中如何应用？
2. 你遇到的最大困难是什么？如何解决的？
3. 如果让你向非技术人员解释今天的核心概念，你会怎么说？

---

## 📖 扩展阅读

### 必读
1. Dify 官方文档 https://docs.dify.ai
2. Dify GitHub README

### 选读
1. Coze 平台对比
2. FastGPT 开源方案

---

## ⚡ 速查卡片

| 概念 | 一句话解释 |
|------|-----------|
| Dify | 开源LLM应用开发平台 |
| 工作流 | 可视化编排节点 |
| 知识库 | 内置RAG能力 |

---

## 🎓 讲师备注

> 本日课程重点在于理论与实践结合。上午理论课务必理解核心概念，下午实操课动手编写代码。晚自习用于查漏补缺和完成作业。如遇问题，优先查阅 FAQ，其次搜索官方文档，最后在课程群提问。


---

## 🏗️ Agent 阶段知识总结（Day 45）

### 已学技术栈

| 技术 | 引入日 | 今日应用 |
|------|--------|----------|
| ReAct | Day 39 | Agent 推理循环基础 |
| LangChain Agent | Day 40 | 工具定义与执行器 |
| LangGraph | Day 41-42 | 图编排与持久化 |
| 多 Agent | Day 43 | Supervisor 协作 |
| MCP | Day 44 | 工具标准化 |

### 今日在 Agent 体系中的位置

Day 45 是 Agent 开发阶段的重要一环。确保你能将今天的内容与 Day 39-43 的技术串联起来。

### 面试常考点

1. 解释 ReAct 框架的 Thought-Action-Observation 循环
2. LangGraph 相比 AgentExecutor 的优势
3. 多 Agent 系统的设计原则和 Supervisor 模式
4. MCP 协议解决什么问题
5. Agent 稳定性保障措施（重试、熔断、监控）
