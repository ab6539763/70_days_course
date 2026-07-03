# Day 10: 模块、包与异常处理

> **零基础大模型应用开发 70 天培训课程** | 第 10/70 天 | Python 编程基础


——————





## 深度讲义

### 10.1 模块与包

```
my_project/
├── main.py
├── config.py
├── models/
│   ├── __init__.py
│   ├── base.py
│   └── openai_model.py
└── utils/
    ├── __init__.py
    └── helpers.py
```

```python
# main.py
from models.openai_model import OpenAIModel
from utils.helpers import load_config

if __name__ == "__main__":
  config = load_config()
  model = OpenAIModel(**config)
```

### 10.2 异常处理

```python
try:
    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.Timeout:
    print("请求超时，请重试")
except requests.exceptions.HTTPError as e:
    print(f"HTTP 错误: {e.response.status_code}")
except json.JSONDecodeError:
    print("响应不是有效 JSON")
finally:
    print("请求完成")
```

### 10.3 虚拟环境

```bash
python -m venv venv
source venv/bin/activate
pip install requests python-dotenv
pip freeze > requirements.txt
```


## 常见错误与避坑

- ⚠️ 只看不练 — 必须动手敲代码
- ⚠️ 跳过基础直接调 API — 每天知识环环相扣
- ⚠️ 不写注释 — 企业级代码必须可读

## 课堂练习

- 📝 复习 Day 9 的核心知识点
- 📝 完成今日实操项目并提交 Git
- 📝 用 3 句话总结今天学到了什么


## 课程衔接说明



### ⬅️ 昨日回顾

**Day 9** 学习了「面向对象编程（下）」，今天的知识直接建立在昨天之上。

### 🔗 今日定位

承接 Day 6 函数化，为 Day 14 企业级项目目录规范做准备。

### ➡️ 明日预告

**Day 11** 将学习「文件操作与常用标准库」，今天务必打牢基础。


### 今日时间安排

| 时段 | 内容 |
|------|------|
| 09:00-12:00 上午 | import 机制、创建自己的模块和包、if __name__ == '__main__' |
| 09:00-12:00 上午 | try/except/else/finally、自定义异常、raise |
| 09:00-12:00 上午 | 虚拟环境 venv / conda、pip 与 requirements.txt |
| 14:00-17:30 下午 | 🛠️ 把项目拆分为多文件包结构 |
| 19:00-21:00 晚自习 | 编写 requirements.txt 并在新 venv 中复现环境 |



## 一、今日学习目标



完成今天的学习后，你将能够:

- import 机制、创建自己的模块和包、if __name__ == '__main__'
- try/except/else/finally、自定义异常、raise
- 虚拟环境 venv / conda、pip 与 requirements.txt

### 核心技能点

- **模块**
- **异常处理**
- **venv**

### 与课程主线的关系

今天是 **第 1 阶段（Python 编程基础）** 的第 10 天。

> 今日主题「模块、包与异常处理」是整条 70 天学习路径中的关键一环。请对照总路线图理解今天学什么、为什么学、后面哪里会用到。



## 二、理论精讲（纳米级拆解）


### 2.1 import 机制、创建自己的模块和包、if __name__ == '__main__'

#### 核心概念

**import 机制、创建自己的模块和包、if __name__ == '__main__'** 是今日学习的重要内容。

#### 为什么学？

在大模型应用开发中，这个知识点将在后续项目中直接用到:
- 与 Day 8 的知识形成递进
- 为 Day 13 的实操项目提供基础

#### 学习要点

1. 理解概念定义（用自己的话复述）
2. 跟着课件代码敲一遍（不要复制粘贴）
3. 完成课后练习巩固

#### 常见错误

- 只看不练 → 必须动手写代码
- 跳过基础 → 每天知识环环相扣，不要跳天

### 2.2 try/except/else/finally、自定义异常、raise

#### 核心概念

**try/except/else/finally、自定义异常、raise** 是今日学习的重要内容。

#### 为什么学？

在大模型应用开发中，这个知识点将在后续项目中直接用到:
- 与 Day 8 的知识形成递进
- 为 Day 13 的实操项目提供基础

#### 学习要点

1. 理解概念定义（用自己的话复述）
2. 跟着课件代码敲一遍（不要复制粘贴）
3. 完成课后练习巩固

#### 常见错误

- 只看不练 → 必须动手写代码
- 跳过基础 → 每天知识环环相扣，不要跳天

### 2.3 虚拟环境 venv / conda、pip 与 requirements.txt

#### 核心概念

**虚拟环境 venv / conda、pip 与 requirements.txt** 是今日学习的重要内容。

#### 为什么学？

在大模型应用开发中，这个知识点将在后续项目中直接用到:
- 与 Day 8 的知识形成递进
- 为 Day 13 的实操项目提供基础

#### 学习要点

1. 理解概念定义（用自己的话复述）
2. 跟着课件代码敲一遍（不要复制粘贴）
3. 完成课后练习巩固

#### 常见错误

- 只看不练 → 必须动手写代码
- 跳过基础 → 每天知识环环相扣，不要跳天

## 三、下午实操预告

今日下午核心项目: **多文件包结构项目**
- 把项目拆分为多文件包结构



## 下午实操：项目实战



### 项目名称

**多文件包结构项目**

### 推荐项目目录结构（企业级标准）

```text
day10_project/
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
# 文件名: day10_main.py
# 主题: Day 10 — 多文件包结构项目
# ================================

"""
Day 10 实操项目入口。

学习要点:
1. 复习昨天所学
2. 完成今日「多文件包结构项目」核心功能
3. 添加必要注释，提交 Git
"""


def main():
    """主函数 — 按今日课纲逐步实现"""
    print("Day 10: 多文件包结构项目")
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
5. **提交**: `git add . && git commit -m "Day 10: 多文件包结构项目"`



## 知识小测




**Q1.** 请用自己的话解释「模块」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 7-10 所学填写）
- 后续应用: 将在 Day 17 左右用到

</details>

**Q2.** 请用自己的话解释「异常处理」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 7-10 所学填写）
- 后续应用: 将在 Day 17 左右用到

</details>

**Q3.** 请用自己的话解释「venv」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 7-10 所学填写）
- 后续应用: 将在 Day 17 左右用到

</details>


### 上机题

请不看课件，独立完成今日「实操项目」的核心功能。限时 60 分钟。



## 课后作业



### 必做

1. 完成今日实操项目「多文件包结构项目」
2. 提交代码到 GitHub（commit message: `Day 10: 多文件包结构项目`）
3. 在学习笔记中记录 3 个今天学到的新知识点

### 晚自习

- 编写 requirements.txt 并在新 venv 中复现环境

### 选做

1. 阅读官方文档中与今日主题相关的章节
2. 尝试优化今日代码（更优雅的错误处理、更清晰的注释）


——————

**第 10/70 天 · 零基础大模型应用开发 70 天培训课程**

> 坚持每一天，70 天后你将成为一名合格的大模型应用开发者。
