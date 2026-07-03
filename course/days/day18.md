# Day 18: Prompt 工程进阶

> **零基础大模型应用开发 70 天培训课程** | 第 18/70 天 | 大模型基础理论与 Prompt 工程


——————





## 深度讲义

### 18.1 思维链 CoT

```python
prompt = '''
请一步步思考以下数学问题:

问题: 一个商店打八折后再减10元，最终价格是多少？原价200元。

让我们一步步思考:
1. 首先计算打八折后的价格
2. 然后减去10元
3. 得出最终价格

请按此格式回答。
'''
```

### 18.2 Prompt 注入防御

```python
def sanitize_input(user_input: str) -> str:
    dangerous_patterns = [
        "忽略之前的指令",
        "ignore previous",
        "你现在是",
    ]
    for pattern in dangerous_patterns:
        if pattern.lower() in user_input.lower():
            return "[输入已被过滤]"
    return user_input
```


## 常见错误与避坑

- ⚠️ 只看不练 — 必须动手敲代码
- ⚠️ 跳过基础直接调 API — 每天知识环环相扣
- ⚠️ 不写注释 — 企业级代码必须可读

## 课堂练习

- 📝 复习 Day 17 的核心知识点
- 📝 完成今日实操项目并提交 Git
- 📝 用 3 句话总结今天学到了什么


## 课程衔接说明



### ⬅️ 昨日回顾

**Day 17** 学习了「Prompt 工程基础」，今天的知识直接建立在昨天之上。

### 🔗 今日定位

承接 Day 17 基础 Prompt，为 Day 19 Function Calling 做准备。

### ➡️ 明日预告

**Day 19** 将学习「Function Calling / Tool Use（重点日！）」，今天务必打牢基础。


### 今日时间安排

| 时段 | 内容 |
|------|------|
| 09:00-12:00 上午 | 思维链 CoT(Chain of Thought)、'let's think step by step' |
| 09:00-12:00 上午 | 自洽性(Self-Consistency)、思维树 ToT 概念 |
| 09:00-12:00 上午 | Prompt 攻击与防御（提示词注入、越狱）、防注入实践 |
| 09:00-12:00 上午 | 结构化输出：JSON Mode、Function Calling 初探 |
| 14:00-17:30 下午 | 🛠️ 构建一个「智能客服意图分类器」（输出结构化 JSON） |
| 19:00-21:00 晚自习 | 测试 3 种 Prompt 注入攻击并加固 |



## 一、今日学习目标



完成今天的学习后，你将能够:

- 思维链 CoT(Chain of Thought)、'let's think step by step'
- 自洽性(Self-Consistency)、思维树 ToT 概念
- Prompt 攻击与防御（提示词注入、越狱）、防注入实践
- 结构化输出：JSON Mode、Function Calling 初探

### 核心技能点

- **CoT**
- **Prompt 注入防御**
- **JSON Mode**

### 与课程主线的关系

今天是 **第 2 阶段（大模型基础理论与 Prompt 工程）** 的第 4 天。

> 今日主题「Prompt 工程进阶」是整条 70 天学习路径中的关键一环。请对照总路线图理解今天学什么、为什么学、后面哪里会用到。



## 二、理论精讲（纳米级拆解）


### 2.1 思维链 CoT(Chain of Thought)、'let's think step by step'

#### Prompt 设计四要素

| 要素 | 说明 | 示例 |
|------|------|------|
| 指令 | 告诉模型做什么 | "请将以下文本翻译成英文" |
| 上下文 | 背景信息 | "这是一份医疗科普文章" |
| 输入 | 待处理内容 | 用户提供的原文 |
| 输出格式 | 约束返回形式 | "请以 JSON 格式返回" |

#### Zero-shot vs Few-shot

```python
# Zero-shot: 直接给指令
prompt_zero = "判断以下评论的情感（正面/负面）: 这个产品太好用了！"

# Few-shot: 给几个示例
prompt_few = '''
判断评论情感，示例:
评论: 太差了 → 负面
评论: 非常满意 → 正面
评论: 这个产品太好用了！ →
'''
```

#### 与大模型岗位的关系

Prompt 工程是大模型应用开发**第一天就要用、每一天都在用**的技能。

### 2.2 自洽性(Self-Consistency)、思维树 ToT 概念

#### 核心概念

**自洽性(Self-Consistency)、思维树 ToT 概念** 是今日学习的重要内容。

#### 为什么学？

在大模型应用开发中，这个知识点将在后续项目中直接用到:
- 与 Day 16 的知识形成递进
- 为 Day 21 的实操项目提供基础

#### 学习要点

1. 理解概念定义（用自己的话复述）
2. 跟着课件代码敲一遍（不要复制粘贴）
3. 完成课后练习巩固

#### 常见错误

- 只看不练 → 必须动手写代码
- 跳过基础 → 每天知识环环相扣，不要跳天

### 2.3 Prompt 攻击与防御（提示词注入、越狱）、防注入实践

#### Prompt 设计四要素

| 要素 | 说明 | 示例 |
|------|------|------|
| 指令 | 告诉模型做什么 | "请将以下文本翻译成英文" |
| 上下文 | 背景信息 | "这是一份医疗科普文章" |
| 输入 | 待处理内容 | 用户提供的原文 |
| 输出格式 | 约束返回形式 | "请以 JSON 格式返回" |

#### Zero-shot vs Few-shot

```python
# Zero-shot: 直接给指令
prompt_zero = "判断以下评论的情感（正面/负面）: 这个产品太好用了！"

# Few-shot: 给几个示例
prompt_few = '''
判断评论情感，示例:
评论: 太差了 → 负面
评论: 非常满意 → 正面
评论: 这个产品太好用了！ →
'''
```

#### 与大模型岗位的关系

Prompt 工程是大模型应用开发**第一天就要用、每一天都在用**的技能。

### 2.4 结构化输出：JSON Mode、Function Calling 初探

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

今日下午核心项目: **智能客服意图分类器**
- 构建一个「智能客服意图分类器」（输出结构化 JSON）



## 下午实操：项目实战



### 项目名称

**智能客服意图分类器**

### 推荐项目目录结构（企业级标准）

```text
day18_project/
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
# 文件名: day18_main.py
# 主题: Day 18 — 智能客服意图分类器
# ================================

"""
Day 18 实操项目入口。

学习要点:
1. 复习昨天所学
2. 完成今日「智能客服意图分类器」核心功能
3. 添加必要注释，提交 Git
"""


def main():
    """主函数 — 按今日课纲逐步实现"""
    print("Day 18: 智能客服意图分类器")
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
5. **提交**: `git add . && git commit -m "Day 18: 智能客服意图分类器"`



## 知识小测




**Q1.** 请用自己的话解释「CoT」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 15-18 所学填写）
- 后续应用: 将在 Day 25 左右用到

</details>

**Q2.** 请用自己的话解释「Prompt 注入防御」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 15-18 所学填写）
- 后续应用: 将在 Day 25 左右用到

</details>

**Q3.** 请用自己的话解释「JSON Mode」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 15-18 所学填写）
- 后续应用: 将在 Day 25 左右用到

</details>


### 上机题

请不看课件，独立完成今日「实操项目」的核心功能。限时 60 分钟。



## 课后作业



### 必做

1. 完成今日实操项目「智能客服意图分类器」
2. 提交代码到 GitHub（commit message: `Day 18: 智能客服意图分类器`）
3. 在学习笔记中记录 3 个今天学到的新知识点

### 晚自习

- 测试 3 种 Prompt 注入攻击并加固

### 选做

1. 阅读官方文档中与今日主题相关的章节
2. 尝试优化今日代码（更优雅的错误处理、更清晰的注释）


——————

**第 18/70 天 · 零基础大模型应用开发 70 天培训课程**

> 坚持每一天，70 天后你将成为一名合格的大模型应用开发者。
