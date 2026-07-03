# Day 23: FastAPI 后端开发（上）

> **零基础大模型应用开发 70 天培训课程** | 第 23/70 天 | 大模型基础理论与 Prompt 工程


——————





## 深度讲义

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


## 常见错误与避坑

- ⚠️ 只看不练 — 必须动手敲代码
- ⚠️ 跳过基础直接调 API — 每天知识环环相扣
- ⚠️ 不写注释 — 企业级代码必须可读

## 课堂练习

- 📝 复习 Day 22 的核心知识点
- 📝 完成今日实操项目并提交 Git
- 📝 用 3 句话总结今天学到了什么


## 课程衔接说明



### ⬅️ 昨日回顾

**Day 22** 学习了「前端速成」，今天的知识直接建立在昨天之上。

### 🔗 今日定位

承接 Day 13 异步与 Day 14 对话逻辑，为 Day 24 SSE 流式接口铺垫。

### ➡️ 明日预告

**Day 24** 将学习「FastAPI 后端开发（下）+ 数据库」，今天务必打牢基础。


### 今日时间安排

| 时段 | 内容 |
|------|------|
| 09:00-12:00 上午 | FastAPI 入门：路由、路径参数、查询参数、自动文档 |
| 09:00-12:00 上午 | Pydantic 数据模型、请求体校验、响应模型 |
| 14:00-17:30 下午 | 🛠️ 把 AI 对话功能封装成 REST API |
| 19:00-21:00 晚自习 | 阅读 FastAPI 自动生成的 Swagger 文档 |



## 一、今日学习目标



完成今天的学习后，你将能够:

- FastAPI 入门：路由、路径参数、查询参数、自动文档
- Pydantic 数据模型、请求体校验、响应模型

### 核心技能点

- **FastAPI**
- **Pydantic**
- **REST**

### 与课程主线的关系

今天是 **第 2 阶段（大模型基础理论与 Prompt 工程）** 的第 9 天。

> 今日主题「FastAPI 后端开发（上）」是整条 70 天学习路径中的关键一环。请对照总路线图理解今天学什么、为什么学、后面哪里会用到。



## 二、理论精讲（纳米级拆解）


### 2.1 FastAPI 入门：路由、路径参数、查询参数、自动文档

#### HTTP 协议基础

| 方法 | 用途 | 大模型场景 |
|------|------|-----------|
| GET | 获取资源 | 查询模型列表 |
| POST | 提交数据 | **调用 Chat API（最常用）** |

#### 关键概念

- **URL**: 接口地址，如 `https://api.deepseek.com/v1/chat/completions`
- **Header**: 请求头，携带 `Authorization: Bearer <API_KEY>`
- **Body**: 请求体，JSON 格式，包含 `model`、`messages` 等
- **Status Code**: 200=成功, 401=密钥错误, 429=频率限制

#### 大模型 API 请求结构

```python
import requests

API_KEY = "your-api-key"
URL = "https://api.deepseek.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

payload = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "system", "content": "你是一个有帮助的助手。"},
        {"role": "user", "content": "你好！"},
    ],
    "temperature": 0.7,
}

response = requests.post(URL, headers=headers, json=payload)
result = response.json()
print(result["choices"][0]["message"]["content"])
```

> 这段代码将在今天下午的实操中完整实现。

### 2.2 Pydantic 数据模型、请求体校验、响应模型

#### 核心概念

**Pydantic 数据模型、请求体校验、响应模型** 是今日学习的重要内容。

#### 为什么学？

在大模型应用开发中，这个知识点将在后续项目中直接用到:
- 与 Day 21 的知识形成递进
- 为 Day 26 的实操项目提供基础

#### 学习要点

1. 理解概念定义（用自己的话复述）
2. 跟着课件代码敲一遍（不要复制粘贴）
3. 完成课后练习巩固

#### 常见错误

- 只看不练 → 必须动手写代码
- 跳过基础 → 每天知识环环相扣，不要跳天

## 三、下午实操预告

今日下午核心项目: **AI 对话 REST API**
- 把 AI 对话功能封装成 REST API



## 下午实操：项目实战



### 项目名称

**AI 对话 REST API**

### 推荐项目目录结构（企业级标准）

```text
day23_project/
├─ src/
│  ├─ __init__.py
│  └─ main.py
├─ data/
├─ outputs/
├─ tests/
├─ requirements.txt
└─ README.md
```

### 代码骨架

```python
# ================================
# 文件名: day23_main.py
# 主题: Day 23 — AI 对话 REST API
# ================================

"""
Day 23 实操项目入口。

学习要点:
1. 复习昨天所学
2. 完成今日「AI 对话 REST API」核心功能
3. 添加必要注释，提交 Git
"""


def main():
    """主函数 — 按今日课纲逐步实现"""
    print("Day 23: AI 对话 REST API")
    # TODO: 按课件逐步实现
    pass


if __name__ == "__main__":
    main()
```

### 实现步骤（纳米级拆解）

1. **需求确认**: 阅读今日课纲，明确输入/输出
2. **环境准备**: 激活 venv，`pip install` 今日所需依赖
3. **核心实现**: 按上午所学知识点逐步编码
4. **自测**: 手动运行 3 个以上测试用例
5. **提交**: `git add . && git commit -m "Day 23: AI 对话 REST API"`



## 知识小测




**Q1.** 请用自己的话解释「FastAPI」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 20-23 所学填写）
- 后续应用: 将在 Day 30 左右用到

</details>

**Q2.** 请用自己的话解释「Pydantic」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 20-23 所学填写）
- 后续应用: 将在 Day 30 左右用到

</details>

**Q3.** 请用自己的话解释「REST」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 20-23 所学填写）
- 后续应用: 将在 Day 30 左右用到

</details>


### 上机题

请不看课件，独立完成今日「实操项目」的核心功能。限时 60 分钟。



## 课后作业



### 必做

1. 完成今日实操项目「AI 对话 REST API」
2. 提交代码到 GitHub（commit message: `Day 23: AI 对话 REST API`）
3. 在学习笔记中记录 3 个今天学到的新知识点

### 晚自习

- 阅读 FastAPI 自动生成的 Swagger 文档

### 选做

1. 阅读官方文档中与今日主题相关的章节
2. 尝试优化今日代码（更优雅的错误处理、更清晰的注释）


——————

**第 23/70 天 · 零基础大模型应用开发 70 天培训课程**

> 坚持每一天，70 天后你将成为一名合格的大模型应用开发者。
