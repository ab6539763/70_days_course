# Day 5: 核心数据结构（下）—— 字典重点日

> **零基础大模型应用开发 70 天培训课程** | 第 5/70 天 | Python 编程基础


——————




## 深度讲义


### 5.1 字典 dict — API 交互的核心

```python
user = {
    "name": "张三",
    "age": 25,
    "skills": ["Python", "AI"],
    "address": {
        "city": "北京",
        "district": "海淀"
    }
}

# 访问
print(user["name"])           # 张三
print(user.get("email", "无")) # 安全访问，不存在返回默认值

# 修改
user["age"] = 26
user["email"] = "zhang@example.com"

# 遍历
for key, value in user.items():
    print(f"{key}: {value}")
```

### 5.2 JSON — 大模型世界的通用语言

**为什么 JSON 是重点？**

因为所有大模型 API 的请求和响应都是 JSON 格式。今天学不好 JSON，Day 12 调 API 就会卡住。

#### JSON 与 Python 的对应关系

| JSON | Python |
|------|--------|
| object `{}` | dict |
| array `[]` | list |
| string | str |
| number | int / float |
| true/false | True/False |
| null | None |

#### json 模块四个核心函数

```python
import json

# 1. dumps: Python 对象 → JSON 字符串
data = {"role": "user", "content": "你好"}
json_str = json.dumps(data, ensure_ascii=False)
# '{"role": "user", "content": "你好"}'

# 2. loads: JSON 字符串 → Python 对象
parsed = json.loads(json_str)

# 3. dump: Python 对象 → 写入 JSON 文件
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 4. load: 从 JSON 文件读取
with open("data.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
```

### 5.3 模拟 API 响应结构

```json
{
  "id": "chatcmpl-xxx",
  "model": "deepseek-chat",
  "choices": [{
    "message": {
      "role": "assistant",
      "content": "你好！"
    }
  }],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 5,
    "total_tokens": 15
  }
}
```

> **前后衔接**: 今天解析 JSON → Day 12 构造并解析真实 API 的 JSON


## 完整项目代码（可直接运行）

### 文件: `day05_json_parser.py`

```python
"""Day 5: 解析模拟 API 返回的 JSON"""
import json

MOCK_API_RESPONSE = """
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "model": "deepseek-chat",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "你好！我是 AI 助手，有什么可以帮你的？"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 20,
    "total_tokens": 30
  }
}
"""


def parse_api_response(json_str: str) -> dict:
    data = json.loads(json_str)
    return {
        "model": data["model"],
        "reply": data["choices"][0]["message"]["content"],
        "role": data["choices"][0]["message"]["role"],
        "total_tokens": data["usage"]["total_tokens"],
    }


def main():
    result = parse_api_response(MOCK_API_RESPONSE)
    print("=" * 40)
    print(f"模型: {result['model']}")
    print(f"角色: {result['role']}")
    print(f"回复: {result['reply']}")
    print(f"Token 消耗: {result['total_tokens']}")
    print("=" * 40)


if __name__ == "__main__":
    main()
```

### 运行步骤

```bash
cd course/code/day05
pip install -r requirements.txt  # 如有依赖
python day05_json_parser.py
```


## 常见错误与避坑

- ⚠️ 只看不练 — 必须动手敲代码
- ⚠️ 跳过基础直接调 API — 每天知识环环相扣
- ⚠️ 不写注释 — 企业级代码必须可读

## 课堂练习

- 📝 复习 Day 4 的核心知识点
- 📝 完成今日实操项目并提交 Git
- 📝 用 3 句话总结今天学到了什么


## 课程衔接说明



### ⬅️ 昨日回顾

**Day 4** 学习了「核心数据结构（上）」，今天的知识直接建立在昨天之上。

### 🔗 今日定位

承接 Day 4 列表，JSON 是 Day 12 调用大模型 API 的必备技能。

### ➡️ 明日预告

**Day 6** 将学习「函数」，今天务必打牢基础。


### 今日时间安排

| 时段 | 内容 |
|------|------|
| 09:00-12:00 上午 | 字典 dict 的增删改查、嵌套字典、遍历 |
| 09:00-12:00 上午 | JSON 格式详解（与 API 交互的基石，重点！） |
| 09:00-12:00 上午 | json 模块的 loads/dumps/load/dump |
| 14:00-17:30 下午 | 🛠️ 解析一份模拟的 API 返回 JSON，提取指定字段 |
| 19:00-21:00 晚自习 | 手写 3 个嵌套 JSON 并用代码遍历 |



## 一、今日学习目标



完成今天的学习后，你将能够:

- 字典 dict 的增删改查、嵌套字典、遍历
- JSON 格式详解（与 API 交互的基石，重点！）
- json 模块的 loads/dumps/load/dump

### 核心技能点

- **dict**
- **JSON**
- **json 模块**

### 与课程主线的关系

今天是 **第 1 阶段（Python 编程基础）** 的第 5 天。

> 今日主题「核心数据结构（下）—— 字典重点日」是整条 70 天学习路径中的关键一环。请对照总路线图理解今天学什么、为什么学、后面哪里会用到。



## 二、理论精讲（纳米级拆解）


### 2.1 字典 dict 的增删改查、嵌套字典、遍历

#### 核心概念

**字典 dict 的增删改查、嵌套字典、遍历** 是今日学习的重要内容。

#### 为什么学？

在大模型应用开发中，这个知识点将在后续项目中直接用到:
- 与 Day 3 的知识形成递进
- 为 Day 8 的实操项目提供基础

#### 学习要点

1. 理解概念定义（用自己的话复述）
2. 跟着课件代码敲一遍（不要复制粘贴）
3. 完成课后练习巩固

#### 常见错误

- 只看不练 → 必须动手写代码
- 跳过基础 → 每天知识环环相扣，不要跳天

### 2.2 JSON 格式详解（与 API 交互的基石，重点！）

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

### 2.3 json 模块的 loads/dumps/load/dump

#### JSON 是大模型开发的通用语言

所有大模型 API 的请求和响应都是 JSON 格式:

```python
import json

# Python 对象 → JSON 字符串
data = {"role": "user", "content": "你好"}
json_str = json.dumps(data, ensure_ascii=False)
# '{"role": "user", "content": "你好"}'

# JSON 字符串 → Python 对象
parsed = json.loads(json_str)
print(parsed["content"])  # 你好

# 读写 JSON 文件
with open("chat_history.json", "w", encoding="utf-8") as f:
    json.dump([data], f, ensure_ascii=False, indent=2)
```

#### 与大模型 API 的关系

Day 12 调用 API 时，你将构造和解析的正是这种 JSON 结构。

## 三、下午实操预告

今日下午核心项目: **API JSON 解析练习**
- 解析一份模拟的 API 返回 JSON，提取指定字段



## 下午实操：项目实战



### 项目名称

**API JSON 解析练习**

### 推荐项目目录结构（企业级标准）

```text
day05_project/
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
# 文件名: day05_main.py
# 主题: Day 5 — API JSON 解析练习
# ================================

"""
Day 5 实操项目入口。

学习要点:
1. 复习昨天所学
2. 完成今日「API JSON 解析练习」核心功能
3. 添加必要注释，提交 Git
"""


def main():
    """主函数 — 按今日课纲逐步实现"""
    print("Day 5: API JSON 解析练习")
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
5. **提交**: `git add . && git commit -m "Day 5: API JSON 解析练习"`



## 知识小测




**Q1.** 请用自己的话解释「dict」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 2-5 所学填写）
- 后续应用: 将在 Day 12 左右用到

</details>

**Q2.** 请用自己的话解释「JSON」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 2-5 所学填写）
- 后续应用: 将在 Day 12 左右用到

</details>

**Q3.** 请用自己的话解释「json 模块」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 2-5 所学填写）
- 后续应用: 将在 Day 12 左右用到

</details>


### 上机题

请不看课件，独立完成今日「实操项目」的核心功能。限时 60 分钟。



## 课后作业



### 必做

1. 完成今日实操项目「API JSON 解析练习」
2. 提交代码到 GitHub（commit message: `Day 5: API JSON 解析练习`）
3. 在学习笔记中记录 3 个今天学到的新知识点

### 晚自习

- 手写 3 个嵌套 JSON 并用代码遍历

### 选做

1. 阅读官方文档中与今日主题相关的章节
2. 尝试优化今日代码（更优雅的错误处理、更清晰的注释）


——————

**第 5/70 天 · 零基础大模型应用开发 70 天培训课程**

> 坚持每一天，70 天后你将成为一名合格的大模型应用开发者。
