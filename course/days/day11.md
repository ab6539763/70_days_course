# Day 11: 文件操作与常用标准库

> **零基础大模型应用开发 70 天培训课程** | 第 11/70 天 | Python 编程基础


——————





## 深度讲义

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
phones = re.findall(r"1[3-9]\d{9}", text)
emails = re.findall(r"[\w.-]+@[\w.-]+\.\w+", text)
```

> **RAG 前置技能**: Day 28 加载 PDF 文档前，需要先用今天学的技能做文本清洗


## 常见错误与避坑

- ⚠️ 只看不练 — 必须动手敲代码
- ⚠️ 跳过基础直接调 API — 每天知识环环相扣
- ⚠️ 不写注释 — 企业级代码必须可读

## 课堂练习

- 📝 复习 Day 10 的核心知识点
- 📝 完成今日实操项目并提交 Git
- 📝 用 3 句话总结今天学到了什么


## 课程衔接说明



### ⬅️ 昨日回顾

**Day 10** 学习了「模块、包与异常处理」，今天的知识直接建立在昨天之上。

### 🔗 今日定位

承接 Day 5 JSON，为 Day 28 文档加载与 Day 30 RAG 铺路。

### ➡️ 明日预告

**Day 12** 将学习「网络请求与 API 调用（关键日！）」，今天务必打牢基础。


### 今日时间安排

| 时段 | 内容 |
|------|------|
| 09:00-12:00 上午 | 文件读写(txt/csv/json)、with 上下文管理器、编码问题(UTF-8) |
| 09:00-12:00 上午 | os、pathlib、datetime、random、re 正则表达式入门 |
| 14:00-17:30 下午 | 🛠️ 批量文档读取与关键词统计工具（RAG 文档处理的前置技能） |
| 19:00-21:00 晚自习 | 用正则清洗一份脏文本数据 |



## 一、今日学习目标



完成今天的学习后，你将能够:

- 文件读写(txt/csv/json)、with 上下文管理器、编码问题(UTF-8)
- os、pathlib、datetime、random、re 正则表达式入门

### 核心技能点

- **文件 IO**
- **pathlib**
- **re 正则**

### 与课程主线的关系

今天是 **第 1 阶段（Python 编程基础）** 的第 11 天。

> 今日主题「文件操作与常用标准库」是整条 70 天学习路径中的关键一环。请对照总路线图理解今天学什么、为什么学、后面哪里会用到。



## 二、理论精讲（纳米级拆解）


### 2.1 文件读写(txt/csv/json)、with 上下文管理器、编码问题(UTF-8)

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

### 2.2 os、pathlib、datetime、random、re 正则表达式入门

#### 核心概念

**os、pathlib、datetime、random、re 正则表达式入门** 是今日学习的重要内容。

#### 为什么学？

在大模型应用开发中，这个知识点将在后续项目中直接用到:
- 与 Day 9 的知识形成递进
- 为 Day 14 的实操项目提供基础

#### 学习要点

1. 理解概念定义（用自己的话复述）
2. 跟着课件代码敲一遍（不要复制粘贴）
3. 完成课后练习巩固

#### 常见错误

- 只看不练 → 必须动手写代码
- 跳过基础 → 每天知识环环相扣，不要跳天

## 三、下午实操预告

今日下午核心项目: **文档关键词统计工具**
- 批量文档读取与关键词统计工具（RAG 文档处理的前置技能）



## 下午实操：项目实战



### 项目名称

**文档关键词统计工具**

### 推荐项目目录结构（企业级标准）

```text
day11_project/
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
# 文件名: day11_main.py
# 主题: Day 11 — 文档关键词统计工具
# ================================

"""
Day 11 实操项目入口。

学习要点:
1. 复习昨天所学
2. 完成今日「文档关键词统计工具」核心功能
3. 添加必要注释，提交 Git
"""


def main():
    """主函数 — 按今日课纲逐步实现"""
    print("Day 11: 文档关键词统计工具")
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
5. **提交**: `git add . && git commit -m "Day 11: 文档关键词统计工具"`



## 知识小测




**Q1.** 请用自己的话解释「文件 IO」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 8-11 所学填写）
- 后续应用: 将在 Day 18 左右用到

</details>

**Q2.** 请用自己的话解释「pathlib」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 8-11 所学填写）
- 后续应用: 将在 Day 18 左右用到

</details>

**Q3.** 请用自己的话解释「re 正则」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 8-11 所学填写）
- 后续应用: 将在 Day 18 左右用到

</details>


### 上机题

请不看课件，独立完成今日「实操项目」的核心功能。限时 60 分钟。



## 课后作业



### 必做

1. 完成今日实操项目「文档关键词统计工具」
2. 提交代码到 GitHub（commit message: `Day 11: 文档关键词统计工具`）
3. 在学习笔记中记录 3 个今天学到的新知识点

### 晚自习

- 用正则清洗一份脏文本数据

### 选做

1. 阅读官方文档中与今日主题相关的章节
2. 尝试优化今日代码（更优雅的错误处理、更清晰的注释）


——————

**第 11/70 天 · 零基础大模型应用开发 70 天培训课程**

> 坚持每一天，70 天后你将成为一名合格的大模型应用开发者。
