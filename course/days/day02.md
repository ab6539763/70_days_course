# Day 2: 运算符与字符串

> **零基础大模型应用开发 70 天培训课程** | 第 2/70 天 | Python 编程基础


——————




## 深度讲义


### 2.1 运算符详解

#### 算术运算符

| 运算符 | 示例 | 结果 | 说明 |
|--------|------|------|------|
| `+` | `3 + 2` | `5` | 加法 |
| `-` | `5 - 2` | `3` | 减法 |
| `*` | `4 * 3` | `12` | 乘法 |
| `/` | `7 / 2` | `3.5` | 除法（结果是 float） |
| `//` | `7 // 2` | `3` | 整除 |
| `%` | `7 % 2` | `1` | 取余 |
| `**` | `2 ** 3` | `8` | 幂运算 |

#### 比较运算符

```python
print(3 > 2)    # True
print(3 == 3)   # True（判断相等用 ==，不是 =）
print(3 != 2)   # True
```

#### 逻辑运算符

```python
age = 20
has_id = True
can_enter = age >= 18 and has_id  # True
```

### 2.2 字符串纳米级拆解

#### 索引与切片

```python
text = "Hello, LLM!"
print(text[0])     # H（正向索引从 0 开始）
print(text[-1])    # !（负向索引从 -1 开始）
print(text[0:5])   # Hello（切片：[起始:结束)，结束不包含）
print(text[7:])    # LLM!
```

#### 常用方法

```python
"  hello  ".strip()          # "hello" — 去首尾空格
"a,b,c".split(",")           # ["a", "b", "c"]
"-".join(["a", "b"])         # "a-b"
"hello".replace("l", "L")    # "heLLo"
```

### 2.3 f-string — Prompt 模板的核心

```python
name = "张三"
role = "用户"
prompt = f"你好，我是{{role}}，我的名字是{{name}}。请回答我的问题。"
# 后续 Day 17 你将用 f-string 构建 Prompt 模板
```

> **前后衔接**: Day 1 学了变量 → 今天学字符串操作 → Day 17 用 f-string 写 Prompt 模板


## 完整项目代码（可直接运行）

### 文件: `day02_text_cleaner.py`

```python
"""Day 2: 文本清洗小工具 — 去空格、统一大小写、敏感词替换"""
import re

SENSITIVE_WORDS = ["广告", "spam", "垃圾"]


def clean_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def normalize_case(text: str, mode: str = "lower") -> str:
    if mode == "lower":
        return text.lower()
    if mode == "upper":
        return text.upper()
    return text.title()


def replace_sensitive(text: str, replacement: str = "***") -> str:
    result = text
    for word in SENSITIVE_WORDS:
        result = result.replace(word, replacement)
    return result


def format_report(original: str, cleaned: str) -> str:
    return f"""原文 ({len(original)} 字符):
{original}

清洗后 ({len(cleaned)} 字符):
{cleaned}"""


def main():
    raw = input("请输入待清洗文本: ")
    step1 = clean_whitespace(raw)
    step2 = normalize_case(step1)
    step3 = replace_sensitive(step2)
    print(format_report(raw, step3))


if __name__ == "__main__":
    main()
```

### 运行步骤

```bash
cd course/code/day02
pip install -r requirements.txt  # 如有依赖
python day02_text_cleaner.py
```


## 常见错误与避坑

- ⚠️ 只看不练 — 必须动手敲代码
- ⚠️ 跳过基础直接调 API — 每天知识环环相扣
- ⚠️ 不写注释 — 企业级代码必须可读

## 课堂练习

- 📝 复习 Day 1 的核心知识点
- 📝 完成今日实操项目并提交 Git
- 📝 用 3 句话总结今天学到了什么


## 课程衔接说明



### ⬅️ 昨日回顾

**Day 1** 学习了「开发环境与第一行代码」，今天的知识直接建立在昨天之上。

### 🔗 今日定位

承接 Day 1 变量基础，为 Day 17 Prompt 模板中的 f-string 埋伏笔。

### ➡️ 明日预告

**Day 3** 将学习「流程控制」，今天务必打牢基础。


### 今日时间安排

| 时段 | 内容 |
|------|------|
| 09:00-12:00 上午 | 算术/比较/逻辑运算符、运算优先级 |
| 09:00-12:00 上午 | 字符串索引、切片、常用方法(split/join/strip/replace/format) |
| 09:00-12:00 上午 | f-string 格式化（后续写 Prompt 模板的核心技能） |
| 14:00-17:30 下午 | 🛠️ 文本清洗小工具（去空格、统一大小写、敏感词替换） |
| 19:00-21:00 晚自习 | 复习 Day 1 代码，完成字符串练习题 |



## 一、今日学习目标



完成今天的学习后，你将能够:

- 算术/比较/逻辑运算符、运算优先级
- 字符串索引、切片、常用方法(split/join/strip/replace/format)
- f-string 格式化（后续写 Prompt 模板的核心技能）

### 核心技能点

- **运算符**
- **字符串操作**
- **f-string**

### 与课程主线的关系

今天是 **第 1 阶段（Python 编程基础）** 的第 2 天。

> 今日主题「运算符与字符串」是整条 70 天学习路径中的关键一环。请对照总路线图理解今天学什么、为什么学、后面哪里会用到。



## 二、理论精讲（纳米级拆解）


### 2.1 算术/比较/逻辑运算符、运算优先级

#### 核心概念

**算术/比较/逻辑运算符、运算优先级** 是今日学习的重要内容。

#### 为什么学？

在大模型应用开发中，这个知识点将在后续项目中直接用到:
- 与 Day 1 的知识形成递进
- 为 Day 5 的实操项目提供基础

#### 学习要点

1. 理解概念定义（用自己的话复述）
2. 跟着课件代码敲一遍（不要复制粘贴）
3. 完成课后练习巩固

#### 常见错误

- 只看不练 → 必须动手写代码
- 跳过基础 → 每天知识环环相扣，不要跳天

### 2.2 字符串索引、切片、常用方法(split/join/strip/replace/format)

#### 核心概念

**字符串索引、切片、常用方法(split/join/strip/replace/format)** 是今日学习的重要内容。

#### 为什么学？

在大模型应用开发中，这个知识点将在后续项目中直接用到:
- 与 Day 1 的知识形成递进
- 为 Day 5 的实操项目提供基础

#### 学习要点

1. 理解概念定义（用自己的话复述）
2. 跟着课件代码敲一遍（不要复制粘贴）
3. 完成课后练习巩固

#### 常见错误

- 只看不练 → 必须动手写代码
- 跳过基础 → 每天知识环环相扣，不要跳天

### 2.3 f-string 格式化（后续写 Prompt 模板的核心技能）

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

## 三、下午实操预告

今日下午核心项目: **文本清洗小工具**
- 文本清洗小工具（去空格、统一大小写、敏感词替换）



## 下午实操：项目实战



### 项目名称

**文本清洗小工具**

### 推荐项目目录结构（企业级标准）

```text
day02_project/
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
# 文件名: day02_main.py
# 主题: Day 2 — 文本清洗小工具
# ================================

"""
Day 2 实操项目入口。

学习要点:
1. 复习昨天所学
2. 完成今日「文本清洗小工具」核心功能
3. 添加必要注释，提交 Git
"""


def main():
    """主函数 — 按今日课纲逐步实现"""
    print("Day 2: 文本清洗小工具")
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
5. **提交**: `git add . && git commit -m "Day 2: 文本清洗小工具"`



## 知识小测




**Q1.** 请用自己的话解释「运算符」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 1-2 所学填写）
- 后续应用: 将在 Day 9 左右用到

</details>

**Q2.** 请用自己的话解释「字符串操作」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 1-2 所学填写）
- 后续应用: 将在 Day 9 左右用到

</details>

**Q3.** 请用自己的话解释「f-string」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 1-2 所学填写）
- 后续应用: 将在 Day 9 左右用到

</details>


### 上机题

请不看课件，独立完成今日「实操项目」的核心功能。限时 60 分钟。



## 课后作业



### 必做

1. 完成今日实操项目「文本清洗小工具」
2. 提交代码到 GitHub（commit message: `Day 2: 文本清洗小工具`）
3. 在学习笔记中记录 3 个今天学到的新知识点

### 晚自习

- 复习 Day 1 代码，完成字符串练习题

### 选做

1. 阅读官方文档中与今日主题相关的章节
2. 尝试优化今日代码（更优雅的错误处理、更清晰的注释）


——————

**第 2/70 天 · 零基础大模型应用开发 70 天培训课程**

> 坚持每一天，70 天后你将成为一名合格的大模型应用开发者。
