# Day 1: 开发环境与第一行代码

> **培训阶段**: 第一阶段 Python 编程基础 | **第 1 周** | **学习时长**: 约 6-8 小时  
> **今日关键词**: 环境搭建、变量、数据类型、print/input、Git 入门

---

## 📍 课程导航

### 上节回顾
欢迎加入 **零基础大模型应用开发 70 天培训课程**！今天是 Day 1，没有上节内容。你将从零开始，踏上成为大模型应用开发工程师的旅程。

### 本节学习目标
完成本日学习后，你将能够：

1. 理解大模型行业的基本格局与职业发展方向
2. 在 Windows / macOS / Linux 上独立安装并配置 Python 3.10+ 开发环境
3. 安装 VS Code 及 Python 扩展，配置国内 pip 镜像源
4. 理解并使用 Python 的四种基本数据类型：int、float、str、bool
5. 使用 `print()` 输出信息、`input()` 接收用户输入
6. 独立完成「个人信息卡片」命令行程序
7. 注册 GitHub 账号，完成第一次 Git 提交

### 与后续课程的衔接
- **Day 2** 将学习运算符与字符串操作——字符串格式化（f-string）是后续编写 **Prompt 模板** 的核心技能
- **Day 5** 将深入学习 JSON——这是与所有大模型 API 交互的数据格式基石
- **Day 12** 将首次调用大模型 API——今天写的 `print`/`input` 程序将升级为 AI 问答助手
- 今天配置的 **Git + GitHub** 将贯穿整个 70 天培训，毕业时你将拥有一个内容充实的代码仓库

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：课程介绍与大模型行业全景

#### 1.1 欢迎来到大模型时代

2022 年底 ChatGPT 的发布，标志着人工智能进入了一个全新的阶段。大语言模型（Large Language Model, LLM）不再只是实验室里的研究成果，而是成为了每个人都可以使用的生产力工具。

**什么是大语言模型？**

用最通俗的话说：大语言模型是一个「读过互联网上几乎所有文字」的超级大脑。你给它一段文字（Prompt），它会根据学到的知识生成下一段文字。它可以：

- 回答问题、翻译语言、撰写文章
- 分析数据、生成代码、调试程序
- 理解图片、创作图像（多模态能力）

**本课程的定位**

| 维度 | 说明 |
|------|------|
| 起点 | 零编程基础或仅有少量基础 |
| 终点 | 能独立开发 RAG 应用、Agent 应用、微调小模型并部署上线 |
| 周期 | 70 天（10 周），每天 6-8 小时 |
| 核心技能 | Python → Prompt 工程 → RAG → Agent → 微调部署 |

#### 1.2 大模型行业全景

**产业链图谱**

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  基础层      │    │  模型层      │    │  应用层      │
│  算力/芯片   │ →  │  大模型训练  │ →  │  行业应用    │
│  云计算      │    │  开源/闭源   │    │  产品开发    │
└─────────────┘    └─────────────┘    └─────────────┘
                          ↓
                   ┌─────────────┐
                   │  工具层      │  ← 本课程重点！
                   │  LangChain  │
                   │  LlamaIndex │
                   │  Dify/Coze  │
                   └─────────────┘
```

**主流大模型一览（2025-2026）**

| 模型 | 厂商 | 特点 | 本课程是否使用 |
|------|------|------|----------------|
| GPT-4o / GPT-4 | OpenAI | 综合能力最强，API 生态完善 | 选修参考 |
| Claude 3.5 | Anthropic | 长文本、代码能力强 | 选修参考 |
| DeepSeek-V3 | 深度求索 | 国产高性价比，推理能力强 | ✅ 主力 API |
| Qwen2.5 | 阿里通义 | 中文优秀，开源可微调 | ✅ 主力 API |
| GLM-4 | 智谱 AI | 国产综合能力强 | 选修 |
| Llama 3 | Meta | 开源标杆，可本地部署 | ✅ 微调阶段 |

#### 1.3 职业路径分析

**大模型相关岗位（按入门难度排序）**

1. **Prompt 工程师** — 设计提示词，优化模型输出（本课程 Day 15-19 覆盖）
2. **大模型应用开发工程师** — 用 API + 框架开发 RAG/Agent 应用（本课程核心目标）
3. **AI 产品经理** — 理解技术边界，设计 AI 产品（本课程也适合 PM 学习）
4. **模型微调工程师** — 针对垂直领域微调模型（本课程 Day 51-55 覆盖）
5. **AI 基础设施工程师** — 部署推理服务、优化性能（本课程 Day 55-56 入门）

**薪资参考（2025 年国内市场，仅供参考）**

| 岗位 | 初级（0-1年） | 中级（1-3年） | 高级（3年+） |
|------|---------------|---------------|--------------|
| 大模型应用开发 | 15-25K | 25-40K | 40-60K |
| Prompt 工程师 | 12-20K | 20-30K | 30-45K |
| 模型微调工程师 | 18-28K | 28-45K | 45-70K |

> 💡 **关键洞察**：当前市场对「能独立交付大模型应用」的工程师需求远大于「能训练大模型」的研究员。本课程聚焦**应用开发**，这是最务实、最高效的入行路径。

#### 1.4 70 天学习路线图预览

```
Week 1-2  ████████░░░░░░░░░░░░  Python 基础（Day 1-14）
Week 3-4  ░░░░░░░░████████░░░░  大模型理论 + Web（Day 15-24）
Week 5-6  ░░░░░░░░░░░░░░██████  RAG 开发（Day 25-38）
Week 7-8  ░░░░░░░░░░░░░░░░░░██  Agent 开发（Day 39-50）
Week 9    ░░░░░░░░░░░░░░░░░░░░  微调与部署（Day 51-57）
Week 10   ░░░░░░░░░░░░░░░░░░░░  毕业设计（Day 58-70）
```

---

### 9:45 - 10:30 | 模块二：Python 环境安装

#### 2.1 为什么选择 Python？

Python 是大模型应用开发的首选语言，原因如下：

| 原因 | 说明 |
|------|------|
| AI 生态最完善 | LangChain、LlamaIndex、PyTorch 等核心库都是 Python 优先 |
| 语法简洁 | 接近自然语言，零基础友好 |
| 社区活跃 | 遇到问题几乎都能找到答案 |
| 就业市场需求大 | 大模型岗位 90%+ 要求 Python |

#### 2.2 安装 Python 3.10+

**Step 1：检查是否已安装**

打开终端（Windows 用 PowerShell 或 CMD，macOS 用 Terminal），输入：

```bash
python --version
# 或
python3 --version
```

如果显示 `Python 3.10.x` 或更高版本，可以跳过安装。如果版本低于 3.10 或未安装，继续下一步。

**Step 2：下载安装**

| 操作系统 | 下载地址 | 注意事项 |
|----------|----------|----------|
| Windows | https://www.python.org/downloads/ | ⚠️ 勾选 "Add Python to PATH" |
| macOS | `brew install python@3.12` 或官网下载 | 推荐用 Homebrew |
| Linux | `sudo apt install python3.12` | Ubuntu/Debian 系 |

**Step 3：验证安装**

```bash
python3 --version
# 期望输出: Python 3.12.x

python3 -c "print('Hello, AI World!')"
# 期望输出: Hello, AI World!
```

#### 2.3 安装 VS Code

VS Code 是目前最流行的代码编辑器，对大模型开发支持极好。

1. 访问 https://code.visualstudio.com/ 下载安装
2. 打开 VS Code，点击左侧扩展图标（或 `Ctrl+Shift+X`）
3. 搜索并安装以下扩展：
   - **Python**（Microsoft 官方，必装）
   - **Pylance**（智能代码提示，通常随 Python 扩展自动安装）
   - **Chinese (Simplified)**（中文语言包，可选）

**创建第一个项目文件夹**

```bash
# 在你的用户目录下创建课程项目文件夹
mkdir ~/llm-course
cd ~/llm-course

# 用 VS Code 打开
code .
```

#### 2.4 配置国内 pip 镜像源

由于网络原因，直接使用 `pip install` 可能很慢。配置国内镜像可以大幅加速。

**方法一：永久配置（推荐）**

```bash
# Linux / macOS
pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# Windows
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

**方法二：临时使用**

```bash
pip3 install requests -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**常用国内镜像源**

| 镜像源 | URL |
|--------|-----|
| 清华大学 | https://pypi.tuna.tsinghua.edu.cn/simple |
| 阿里云 | https://mirrors.aliyun.com/pypi/simple |
| 中科大 | https://pypi.mirrors.ustc.edu.cn/simple |

**验证 pip 配置**

```bash
pip3 config list
# 应显示: global.index-url='https://pypi.tuna.tsinghua.edu.cn/simple'
```

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：Python 基础语法（一）

#### 3.1 你的第一行 Python 代码

在 VS Code 中，创建文件 `day01/hello.py`：

```python
# day01/hello.py
# 这是你的第一行 Python 代码！
# 井号(#) 开头的是注释，Python 会忽略它

print("Hello, AI World!")
print("欢迎来到大模型应用开发课程！")
```

**运行方式一：在终端中运行**

```bash
cd ~/llm-course
python3 day01/hello.py
```

**运行方式二：在 VS Code 中运行**

1. 打开 `hello.py` 文件
2. 点击右上角的 ▶️ 按钮
3. 或按 `F5` 键（首次会提示选择 Python 解释器）

**期望输出：**

```
Hello, AI World!
欢迎来到大模型应用开发课程！
```

#### 3.2 变量：程序的记忆

变量就像一个贴了标签的盒子，用来存储数据。

```python
# 创建变量并赋值
name = "张三"          # 字符串类型 str
age = 25               # 整数类型 int
height = 1.75          # 浮点数类型 float
is_student = True      # 布尔类型 bool

# 使用变量
print(name)
print(age)
print(height)
print(is_student)
```

**变量命名规则**

| 规则 | 正确示例 | 错误示例 |
|------|----------|----------|
| 只能包含字母、数字、下划线 | `user_name`, `age2` | `user-name`, `2age` |
| 不能以数字开头 | `name1` | `1name` |
| 区分大小写 | `Name` ≠ `name` | — |
| 不能使用 Python 关键字 | `my_class` | `class`, `for`, `if` |
| 推荐用小写+下划线 | `user_name` | `userName`（也可以，但 Python 社区偏好下划线） |

> 💡 **与大模型开发的联系**：在 Day 12 调用 API 时，你会用变量存储 API Key；在 Day 17 编写 Prompt 时，会用变量拼接提示词模板。

#### 3.3 四种基本数据类型

**整数 (int)**

```python
count = 100
negative = -42
big_number = 1_000_000  # Python 允许用下划线分隔大数字，提高可读性

print(type(count))  # <class 'int'>
```

**浮点数 (float)**

```python
price = 19.99
temperature = -3.5
scientific = 1.5e6  # 科学计数法，等于 1500000.0

print(type(price))  # <class 'float'>
```

**字符串 (str)**

```python
greeting = "你好"
message = '欢迎学习 Python'
multiline = """这是
多行
字符串"""

# 字符串拼接
full_name = "张" + "三"
print(full_name)  # 张三

print(type(greeting))  # <class 'str'>
```

**布尔值 (bool)**

```python
is_active = True
is_deleted = False

# 布尔值常用于条件判断
print(10 > 5)   # True
print(3 == 7)   # False

print(type(is_active))  # <class 'bool'>
```

**类型查看与转换**

```python
x = "42"
print(type(x))        # <class 'str'> — 这是字符串，不是数字！

y = int(x)            # 字符串转整数
print(type(y))        # <class 'int'>
print(y + 8)          # 50

z = str(100)          # 整数转字符串
print(z + "分")       # 100分
```

#### 3.4 print() 函数详解

`print()` 是 Python 中最常用的输出函数。

```python
# 基本用法
print("Hello")

# 打印多个值，默认用空格分隔
print("姓名:", "张三", "年龄:", 25)
# 输出: 姓名: 张三 年龄: 25

# 自定义分隔符
print("2026", "07", "03", sep="-")
# 输出: 2026-07-03

# 自定义结尾（默认是换行 \n）
print("第一行", end=" | ")
print("第二行")
# 输出: 第一行 | 第二行

# 格式化输出（f-string，Day 2 会深入学习）
name = "李四"
score = 95.5
print(f"学生 {name} 的成绩是 {score} 分")
# 输出: 学生 李四 的成绩是 95.5 分
```

#### 3.5 input() 函数详解

`input()` 用于接收用户的键盘输入，**返回值永远是字符串**。

```python
# 基本用法
name = input("请输入你的姓名: ")
print(f"你好, {name}!")

# ⚠️ 注意：input() 返回的是字符串！
age = input("请输入你的年龄: ")
print(type(age))  # <class 'str'>

# 如果需要数字，必须手动转换
age = int(input("请输入你的年龄: "))
print(type(age))  # <class 'int'>
print(f"10年后你 {age + 10} 岁")
```

---

## 🌇 下午实操（14:00 - 17:30）

### 14:00 - 15:30 | 实操项目：个人信息卡片

#### 项目需求

编写一个命令行程序，收集用户的个人信息并以美观的格式打印出来。

**功能要求：**
1. 提示用户输入：姓名、年龄、城市、职业
2. 将信息格式化为一张「个人信息卡片」打印出来
3. 使用 f-string 进行格式化（Day 2 会系统学习，今天先体验）

#### 参考代码

创建文件 `day01/profile_card.py`：

```python
"""
Day 1 实操项目：个人信息卡片
作者：[你的名字]
日期：2026-07-03
"""

# ===== 收集用户信息 =====
print("=" * 40)
print("       个人信息卡片生成器")
print("=" * 40)
print()

name = input("请输入你的姓名: ")
age = int(input("请输入你的年龄: "))
city = input("请输入你所在的城市: ")
job = input("请输入你的职业: ")

# ===== 生成并打印卡片 =====
print()
print("┌" + "─" * 38 + "┐")
print(f"│  姓名: {name:<30}│")
print(f"│  年龄: {age} 岁{' ' * (30 - len(str(age)) - 4)}│")
print(f"│  城市: {city:<30}│")
print(f"│  职业: {job:<30}│")
print("└" + "─" * 38 + "┘")
print()
print(f"你好 {name}！作为一名{city}的{job}，")
print(f"学习大模型开发将为你打开新的职业可能！")
```

#### 运行效果

```
========================================
       个人信息卡片生成器
========================================

请输入你的姓名: 王小明
请输入你的年龄: 28
请输入你所在的城市: 北京
请输入你的职业: 产品经理

┌──────────────────────────────────────┐
│  姓名: 王小明                          │
│  年龄: 28 岁                          │
│  城市: 北京                            │
│  职业: 产品经理                        │
└──────────────────────────────────────┘

你好 王小明！作为一名北京的产品经理，
学习大模型开发将为你打开新的职业可能！
```

#### 代码解析

| 代码 | 说明 |
|------|------|
| `"""..."""` | 文档字符串，描述文件功能 |
| `"=" * 40` | 字符串重复，生成 40 个等号 |
| `int(input(...))` | 先获取字符串输入，再转为整数 |
| `f"..."` | f-string 格式化字符串，`{变量}` 会被替换 |
| `{name:<30}` | 左对齐，占 30 个字符宽度 |
| `"─" * 38` | Unicode 制表符，画表格边框 |

#### 挑战练习（选做）

1. **增加字段**：添加「学习目标」字段，让用户输入想掌握的技能
2. **输入验证**：如果用户输入的年龄不是数字，给出友好提示（提示：Day 10 会学异常处理）
3. **保存功能**：将信息保存到文本文件（提示：Day 11 会学文件操作）

---

### 15:30 - 15:45 | 课间休息

---

### 15:45 - 17:30 | 扩展练习与知识巩固

#### 练习 1：变量交换

```python
# 不使用第三个变量，交换两个变量的值
a = 10
b = 20
print(f"交换前: a={a}, b={b}")

# Python 的优雅写法
a, b = b, a
print(f"交换后: a={a}, b={b}")
```

#### 练习 2：简易计算器

```python
# 创建文件 day01/simple_calc.py
num1 = float(input("请输入第一个数字: "))
num2 = float(input("请输入第二个数字: "))

print(f"{num1} + {num2} = {num1 + num2}")
print(f"{num1} - {num2} = {num1 - num2}")
print(f"{num1} × {num2} = {num1 * num2}")
if num2 != 0:
    print(f"{num1} ÷ {num2} = {num1 / num2:.2f}")
else:
    print("除数不能为零！")
```

#### 练习 3：类型转换练习

```python
# 猜测以下代码的输出，然后运行验证
print(int(3.9))       # ?
print(float(5))       # ?
print(str(True))      # ?
print(bool(0))        # ?
print(bool(""))       # ?
print(bool("hello"))  # ?
```

<details>
<summary>点击查看答案</summary>

```
3        # int() 直接截断小数部分
5.0      # float() 整数转浮点
True     # str() 布尔转字符串
False    # 0 被视为 False
False    # 空字符串被视为 False
True     # 非空字符串被视为 True
```

</details>

---

## 🌙 晚自习（19:00 - 21:00）

### 19:00 - 20:00 | Git 与 GitHub 入门

#### 为什么学 Git？

在整个 70 天培训中，你的所有代码都将通过 Git 管理并推送到 GitHub。毕业时，你将拥有一个展示给面试官的 **GitHub 主页**——这是大模型开发岗位求职的重要加分项。

#### 安装 Git

```bash
# 验证是否已安装
git --version

# macOS
brew install git

# Ubuntu/Debian
sudo apt install git

# Windows: 下载 https://git-scm.com/download/win
```

#### 基础配置

```bash
git config --global user.name "你的名字"
git config --global user.email "你的邮箱@example.com"
```

#### 注册 GitHub 账号

1. 访问 https://github.com 注册账号
2. 建议用户名使用英文（如 `zhangsan-ai`），方便写在简历上

#### 第一次 Git 提交

```bash
cd ~/llm-course

# 初始化 Git 仓库
git init

# 查看文件状态
git status

# 添加所有文件到暂存区
git add .

# 提交
git commit -m "Day 1: 开发环境搭建与第一行代码"

# 查看提交历史
git log --oneline
```

#### 推送到 GitHub

```bash
# 在 GitHub 上创建一个新仓库（如 llm-course），然后：
git remote add origin https://github.com/你的用户名/llm-course.git
git branch -M main
git push -u origin main
```

> 💡 **每日习惯**：从明天开始，每天结束时都执行 `git add . && git commit -m "Day X: 描述"` 并推送。70 天后你的 GitHub 将拥有 70+ 次提交记录！

### 20:00 - 21:00 | 自习答疑

- 复习今天的代码，确保每个示例都能独立运行
- 完成课后作业（见下方）
- 预习 Day 2 内容：运算符与字符串

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | 大模型行业格局与职业路径 | |
| 2 | Python 3.10+ 安装与验证 | |
| 3 | VS Code 安装与 Python 扩展配置 | |
| 4 | pip 国内镜像源配置 | |
| 5 | 变量的创建与命名规则 | |
| 6 | 四种基本数据类型 int/float/str/bool | |
| 7 | type() 查看类型 | |
| 8 | 类型转换 int()/float()/str()/bool() | |
| 9 | print() 输出与格式化参数 | |
| 10 | input() 接收用户输入 | |
| 11 | f-string 基础用法 | |
| 12 | Git 初始化、add、commit、push | |

---

## 📝 课后作业

### 必做题

1. **环境验证清单**：截图证明以下环境已配置成功
   - [ ] `python3 --version` 显示 3.10+
   - [ ] VS Code 能运行 Python 文件
   - [ ] `pip3 config list` 显示清华镜像源
   - [ ] Git 已配置用户名和邮箱

2. **个人信息卡片**：完成下午实操项目，要求：
   - 至少包含 4 个输入字段
   - 使用 f-string 格式化输出
   - 代码能无报错运行
   - 提交到 GitHub

3. **Git 提交**：完成今天的第一次 Git 提交并推送到 GitHub

### 选做题

4. 编写一个「BMI 计算器」：输入身高（米）和体重（公斤），计算并输出 BMI 值及健康建议
5. 编写一个「温度转换器」：输入摄氏温度，输出对应的华氏温度（公式：F = C × 9/5 + 32）

---

## 💡 常见问题 FAQ

**Q1: 安装 Python 时忘记勾选 "Add Python to PATH" 怎么办？**

A: Windows 用户可以重新运行安装程序，选择 "Modify"，勾选该选项。或者手动将 Python 安装目录添加到系统环境变量 PATH 中。

**Q2: `python` 和 `python3` 命令有什么区别？**

A: 在 macOS/Linux 上，系统可能预装了 Python 2.x（`python` 命令），Python 3 需要用 `python3`。Windows 安装时勾选 PATH 后通常 `python` 就是 Python 3。本课程统一使用 `python3`。

**Q3: input() 获取的数字为什么不能直接做数学运算？**

A: 因为 `input()` 永远返回字符串类型。必须先使用 `int()` 或 `float()` 转换。这是初学者最常犯的错误之一！

**Q4: f-string 中的 `{name:<30}` 是什么意思？**

A: `<` 表示左对齐，`30` 表示占 30 个字符宽度。Day 2 会系统学习字符串格式化，今天先会用即可。

**Q5: Git 提交时提示 "Please tell me who you are" 怎么办？**

A: 需要先配置用户名和邮箱：
```bash
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
```

---

## 🔮 明日预习

**Day 2: 运算符与字符串**

明天你将学习：

- 算术运算符（`+`、`-`、`*`、`/`、`//`、`%`、`**`）
- 比较运算符与逻辑运算符
- 字符串索引、切片、常用方法
- **f-string 格式化深入**——这是后续编写 Prompt 模板的核心技能！
- 实操作业：文本清洗小工具

**预习建议**：回顾今天写的 f-string 代码，思考如何用变量拼接出更复杂的文本输出。

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 1*
