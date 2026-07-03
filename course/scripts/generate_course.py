#!/usr/bin/env python3
"""
70天大模型应用开发培训课程 — Markdown 课件批量生成器

参考 SVM/K-Means/PCA 课件风格：
- 纳米级粒度拆解
- 业务/场景驱动
- 完整可运行代码
- 与前后课程环环相扣
"""

from __future__ import annotations

import os
import textwrap
from pathlib import Path

from curriculum import COURSE_META, DAYS, PHASES, get_phase

ROOT = Path(__file__).resolve().parent.parent
DAYS_DIR = ROOT / "days"
CODE_DIR = ROOT / "code"


def hr(char: str = "—", n: int = 6) -> str:
    return char * n


def section(title: str, level: int = 1) -> str:
    return f"\n{'#' * level} {title}\n\n"


def blockquote(text: str) -> str:
    lines = text.strip().split("\n")
    return "\n".join(f"> {line}" for line in lines) + "\n"


# ─────────────────────────────────────────────
# Day 1 完整代码示例（黄金标准）
# ─────────────────────────────────────────────
DAY1_CODE = '''\
# ================================
# 文件名: day01_personal_card.py
# 主题: Day 1 — 个人信息卡片
# 说明:
# 1. 使用变量存储个人信息
# 2. 练习 print / input / f-string
# 3. 为后续 Prompt 模板中的字符串格式化打基础
# ================================

def collect_user_info() -> dict:
    """交互式收集用户信息，返回字典（Day 5 将深入学习 dict）"""
    print("=" * 40)
    print("  欢迎使用「个人信息卡片」生成器")
    print("=" * 40)

    name = input("请输入你的姓名: ").strip()
    age_str = input("请输入你的年龄: ").strip()
    city = input("请输入你所在的城市: ").strip()
    goal = input("请输入你的学习目标: ").strip()

    # 类型转换：input 永远返回 str，年龄需要转为 int
    try:
        age = int(age_str)
    except ValueError:
        print("[警告] 年龄输入无效，已设为 0")
        age = 0

    return {
        "name": name,
        "age": age,
        "city": city,
        "goal": goal,
    }


def render_card(info: dict) -> str:
    """用 f-string 渲染个人信息卡片（Day 2 将深入 f-string）"""
    border = "─" * 36
    card = f"""
{border}
  📇 个人信息卡片
{border}
  姓名: {info['name']}
  年龄: {info['age']} 岁
  城市: {info['city']}
  学习目标: {info['goal']}
{border}
  生成时间: 由 Python 自动生成
{border}
"""
    return card


def main():
    info = collect_user_info()
    card_text = render_card(info)
    print(card_text)

    # 保存到文件（Day 11 将系统学习文件操作）
    output_file = "my_card.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(card_text)
    print(f"✅ 卡片已保存到 {output_file}")


if __name__ == "__main__":
    main()
'''

DAY1_ENV_GUIDE = """\
### Step 1: 安装 Python 3.10+

访问 https://www.python.org/downloads/ 下载安装包。

**Windows 注意**: 安装时勾选 ✅ `Add Python to PATH`

验证安装:

```bash
python --version
# 期望输出: Python 3.10.x 或更高
pip --version
```

### Step 2: 安装 VS Code

访问 https://code.visualstudio.com/ 下载安装。

推荐插件:
- Python (Microsoft)
- Pylance
- GitLens

### Step 3: 配置国内 pip 镜像源

```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### Step 4: 创建项目目录

```bash
mkdir llm-course-day01
cd llm-course-day01
python -m venv venv

# Windows
venv\\Scripts\\activate
# macOS / Linux
source venv/bin/activate
```

### Step 5: 运行第一个程序

创建 `hello.py`:

```python
print("Hello, LLM World!")
```

```bash
python hello.py
```
"""

DAY1_GIT_GUIDE = """\
### 为什么程序员必须学 Git？

大模型应用开发全程需要版本管理:
- 每天的代码增量提交
- 毕业时 GitHub 主页是作品集核心
- 企业协作必备技能

### 安装 Git

- Windows: https://git-scm.com/download/win
- macOS: `xcode-select --install` 或 `brew install git`

### 基础命令（今晚自习掌握）

```bash
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"

# 初始化仓库
git init
git add .
git commit -m "Day 1: 个人信息卡片程序"

# 关联 GitHub 远程仓库
git remote add origin https://github.com/你的用户名/llm-course.git
git push -u origin main
```
"""

# ─────────────────────────────────────────────
# 按天定制的深度内容块
# ─────────────────────────────────────────────
DAY_EXTRA_CONTENT: dict[int, str] = {}


def _build_day1_extra() -> str:
    return f"""
{section("一、课程全景：为什么学这门课？", 2)}

### 1. 大模型行业正在发生什么？

2023-2026 年，大模型从「实验室玩具」变成「生产力基础设施」:

| 趋势 | 具体表现 | 对开发者意味着什么 |
|------|----------|---------------------|
| API 普惠 | DeepSeek/Qwen 等低价 API | 零基础也能做出可用产品 |
| RAG 爆发 | 企业知识库问答成为标配 | 岗位需求最大的方向之一 |
| Agent 崛起 | 从聊天到自主执行任务 | 2025-2026 最热技能栈 |
| 低代码 + 代码并存 | Dify/Coze + LangChain | 懂代码的更有竞争力 |

### 2. 70 天你将获得什么？

{blockquote("""毕业时你能独立开发:
1. 企业知识库问答系统（RAG）
2. 多 Agent 智能办公助手
3. 微调并部署自己的小模型
4. 一个内容充实的 GitHub 作品集""")}

### 3. 职业路径参考

```
零基础 → Python 基础(14天) → Prompt 工程(10天) → RAG 开发(14天)
       → Agent 开发(12天) → 微调部署(10天) → 毕业设计+就业(13天)
```

岗位方向:
- **大模型应用开发工程师**（最匹配）
- AI 产品经理（技术理解力加分）
- 智能客服 / 知识库系统开发
- 独立开发者 / AI 创业

{section("二、纳米级拆解：什么是「变量」？", 2)}

### 1. 先用生活类比

变量就像一个**贴了标签的盒子**:
- 标签 = 变量名（如 `name`）
- 盒子里的东西 = 变量的值（如 `"张三"`）
- 你可以随时打开盒子，看看或换掉里面的东西

```python
name = "张三"      # 把字符串 "张三" 放进名为 name 的盒子
age = 25           # 把整数 25 放进名为 age 的盒子
is_student = True  # 把布尔值 True 放进名为 is_student 的盒子
```

### 2. 四大基本数据类型

| 类型 | Python 关键字 | 示例 | 用途 |
|------|--------------|------|------|
| 整数 | `int` | `42`, `-7`, `0` | 计数、年龄 |
| 浮点数 | `float` | `3.14`, `-0.5` | 价格、温度 |
| 字符串 | `str` | `"Hello"`, `'你好'` | 文本、Prompt |
| 布尔值 | `bool` | `True`, `False` | 条件判断 |

### 3. 类型查看与转换

```python
x = 42
print(type(x))        # <class 'int'>

# 类型转换（非常常用！）
age_str = "25"
age_int = int(age_str)    # str → int
price = 9.99
price_str = str(price)    # float → str
```

> **与大模型开发的联系**: API 返回的 JSON 中，所有值在解析前都是字符串。
> Day 5 你将深入学习 JSON，Day 12 你将解析 API 返回结果。
> 今天的类型转换是那一天的基础。

{section("三、print 与 input：程序与用户的桥梁", 2)}

### print — 输出

```python
print("Hello, World!")                    # 基础输出
print("姓名:", name, "年龄:", age)         # 多值输出
print(f"我叫{{name}}，今年{{age}}岁")       # f-string（Day 2 深入）
```

### input — 输入

```python
name = input("请输入你的名字: ")
# input 返回的永远是字符串！
# 如果期望数字，必须手动转换: int(input("请输入年龄: "))
```

{section("四、下午实操：个人信息卡片", 2)}

### 项目需求

编写一个命令行程序:
1. 提示用户输入姓名、年龄、城市、学习目标
2. 用 f-string 格式化输出一张精美的信息卡片
3. 将卡片保存到 `my_card.txt` 文件

### 完整参考代码

```python
{DAY1_CODE.strip()}
```

### 运行方式

```bash
cd course/code/day01
python day01_personal_card.py
```

{section("五、环境搭建完整指南", 2)}

{DAY1_ENV_GUIDE}

{section("六、晚自习：Git 与 GitHub 入门", 2)}

{DAY1_GIT_GUIDE}

{section("七、知识自检清单", 2)}

完成以下检查项，打 ✅ 表示掌握:

- [ ] 能独立安装 Python 3.10+ 并验证版本
- [ ] 能创建虚拟环境并激活
- [ ] 理解变量、int/float/str/bool 四种类型
- [ ] 能使用 print 和 input
- [ ] 能运行个人信息卡片程序
- [ ] 完成首次 git commit

{section("八、课后作业", 2)}

### 必做
1. 在个人信息卡片基础上，增加「爱好」和「编程经验」两个字段
2. 用 `type()` 打印每个变量的类型
3. 完成 Git 安装并提交 Day 1 代码到 GitHub

### 选做
1. 让程序支持多次输入（提示: 用 while 循环，Day 3 正式学习）
2. 了解 `black` 代码格式化工具: `pip install black && black day01_personal_card.py`
"""


DAY_EXTRA_CONTENT[1] = _build_day1_extra()


def _generic_theory_block(day: int, title: str, morning: list[str], skills: list[str]) -> str:
    phase = get_phase(day)
    topics_md = "\n".join(f"- {t}" for t in morning)
    skills_md = "\n".join(f"- **{s}**" for s in skills)

    return f"""
{section(f"一、今日学习目标", 2)}

完成今天的学习后，你将能够:

{topics_md}

### 核心技能点

{skills_md}

### 与课程主线的关系

今天是 **第 {phase['id']} 阶段（{phase['name']}）** 的第 {day - phase['days'][0] + 1} 天。

{blockquote(f"今日主题「{title}」是整条 70 天学习路径中的关键一环。"
           f"请对照总路线图理解今天学什么、为什么学、后面哪里会用到。")}
"""


def _generic_code_block(day: int, project: str) -> str:
    code_filename = f"day{day:02d}_main.py"
    return f"""
{section("下午实操：项目实战", 2)}

### 项目名称

**{project}**

### 推荐项目目录结构（企业级标准）

```text
day{day:02d}_project/
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
# 文件名: {code_filename}
# 主题: Day {day} — {project}
# ================================

\"\"\"
Day {day} 实操项目入口。

学习要点:
1. 复习昨天所学
2. 完成今日「{project}」核心功能
3. 添加必要注释，提交 Git
\"\"\"


def main():
    \"\"\"主函数 — 按今日课纲逐步实现\"\"\"
    print("Day {day}: {project}")
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
5. **提交**: `git add . && git commit -m "Day {day}: {project}"`
"""


def _quiz_block(day: int, skills: list[str]) -> str:
    questions = []
    for i, skill in enumerate(skills[:5], 1):
        questions.append(f"""
**Q{i}.** 请用自己的话解释「{skill}」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day {max(1, day-3)}-{day} 所学填写）
- 后续应用: 将在 Day {min(70, day+7)} 左右用到

</details>
""")
    return f"""
{section("知识小测", 2)}

{"".join(questions)}

### 上机题

请不看课件，独立完成今日「实操项目」的核心功能。限时 60 分钟。
"""


def _connection_block(day: int, connection: str) -> str:
    prev_day = day - 1 if day > 1 else None
    next_day = day + 1 if day < 70 else None

    prev_info = ""
    if prev_day and prev_day in DAYS:
        prev_info = f"**Day {prev_day}** 学习了「{DAYS[prev_day][0]}」，今天的知识直接建立在昨天之上。"

    next_info = ""
    if next_day and next_day in DAYS:
        next_info = f"**Day {next_day}** 将学习「{DAYS[next_day][0]}」，今天务必打牢基础。"

    return f"""
{section("课程衔接说明", 2)}

### ⬅️ 昨日回顾

{prev_info if prev_info else "这是课程第一天，欢迎开启大模型开发之旅！"}

### 🔗 今日定位

{connection}

### ➡️ 明日预告

{next_info if next_info else "恭喜完成全部 70 天课程！"}
"""


def _schedule_table(morning: list[str], afternoon: list[str], evening: list[str]) -> str:
    rows = []
    for item in morning:
        rows.append(f"| 09:00-12:00 上午 | {item} |")
    for item in afternoon:
        rows.append(f"| 14:00-17:30 下午 | 🛠️ {item} |")
    for item in evening:
        rows.append(f"| 19:00-21:00 晚自习 | {item} |")

    return f"""
### 今日时间安排

| 时段 | 内容 |
|------|------|
{chr(10).join(rows)}
"""


def generate_day_markdown(day: int) -> str:
    if day not in DAYS:
        raise ValueError(f"Day {day} not in curriculum")

    title, morning, afternoon, evening, project, skills, connection = DAYS[day]
    phase = get_phase(day)

    parts = [
        f"# Day {day}: {title}\n",
        f"> **{COURSE_META['title']}** | 第 {day}/70 天 | {phase['name']}\n",
        f"\n{hr()}\n",
        _connection_block(day, connection),
        _schedule_table(morning, afternoon, evening),
    ]

    # 深度内容：Day 1 有完整定制内容，其余天有通用+按主题扩展
    if day in DAY_EXTRA_CONTENT:
        parts.append(DAY_EXTRA_CONTENT[day])
    else:
        parts.append(_generic_theory_block(day, title, morning, skills))
        parts.append(_expand_day_topics(day, title, morning, afternoon, project, skills))
        parts.append(_generic_code_block(day, project))

    parts.append(_quiz_block(day, skills))
    parts.append(_homework_block(day, project, evening))
    parts.append(_generate_footer(day))

    return "\n".join(parts)


def _expand_day_topics(
    day: int, title: str, morning: list[str], afternoon: list[str],
    project: str, skills: list[str],
) -> str:
    """为每天生成按主题拆分的纳米级内容"""
    blocks = [section("二、理论精讲（纳米级拆解）", 2)]

    for idx, topic in enumerate(morning, 1):
        blocks.append(f"\n### 2.{idx} {topic}\n")
        blocks.append(_topic_detail(day, topic))

    blocks.append(section("三、下午实操预告", 2))
    blocks.append(f"今日下午核心项目: **{project}**\n")
    for item in afternoon:
        blocks.append(f"- {item}\n")

    return "".join(blocks)


def _topic_detail(day: int, topic: str) -> str:
    """根据主题关键词生成细节内容"""
    lower = topic.lower()

    if "api" in lower or "http" in lower or "requests" in lower:
        return _api_topic_detail(day)
    if "prompt" in lower or "cot" in lower or "few-shot" in lower:
        return _prompt_topic_detail(day)
    if "rag" in lower or "向量" in topic or "embedding" in lower:
        return _rag_topic_detail(day)
    if "agent" in lower or "react" in lower or "langgraph" in lower:
        return _agent_topic_detail(day)
    if "langchain" in lower or "lcel" in lower:
        return _langchain_topic_detail(day)
    if "微调" in topic or "lora" in lower or "llama-factory" in lower:
        return _finetune_topic_detail(day)
    if "docker" in lower:
        return _docker_topic_detail(day)
    if "fastapi" in lower:
        return _fastapi_topic_detail(day)
    if "json" in lower:
        return _json_topic_detail(day)
    if "函数" in topic or "function calling" in lower:
        return _function_topic_detail(day)
    if "面试" in topic or "简历" in topic or "答辩" in topic:
        return _career_topic_detail(day, topic)

    # 通用模板
    return f"""
#### 核心概念

**{topic}** 是今日学习的重要内容。

#### 为什么学？

在大模型应用开发中，这个知识点将在后续项目中直接用到:
- 与 Day {max(1, day-2)} 的知识形成递进
- 为 Day {min(70, day+3)} 的实操项目提供基础

#### 学习要点

1. 理解概念定义（用自己的话复述）
2. 跟着课件代码敲一遍（不要复制粘贴）
3. 完成课后练习巩固

#### 常见错误

- 只看不练 → 必须动手写代码
- 跳过基础 → 每天知识环环相扣，不要跳天
"""


def _api_topic_detail(day: int) -> str:
    return """
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
"""


def _prompt_topic_detail(day: int) -> str:
    return """
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
"""


def _rag_topic_detail(day: int) -> str:
    return """
#### RAG 完整链路

```
文档 → 加载 → 分割 → 向量化 → 存储 → 检索 → 增强生成 → 回答
```

#### 核心公式（通俗版）

> 用户问题 → 转成向量 → 在知识库中找最相似的文本块 → 塞进 Prompt → 大模型生成回答

#### 关键参数

| 参数 | 作用 | 调优建议 |
|------|------|----------|
| chunk_size | 每个文本块大小 | 300-1000 字符 |
| chunk_overlap | 块之间重叠 | chunk_size 的 10-20% |
| top_k | 检索返回数量 | 3-10 |
| similarity_threshold | 相似度阈值 | 0.5-0.8 |
"""


def _agent_topic_detail(day: int) -> str:
    return """
#### Agent vs Chain

| | Chain | Agent |
|---|-------|-------|
| 执行方式 | 固定步骤 | 自主决策 |
| 灵活性 | 低 | 高 |
| 适用场景 | 翻译、摘要 | 复杂任务、多步推理 |

#### ReAct 循环

```
Thought（思考）→ Action（行动）→ Observation（观察）→ Thought → ...
```

#### 核心组件

1. **LLM**: 大脑，负责推理
2. **Tools**: 手脚，负责执行（搜索、计算、查数据库）
3. **Memory**: 记忆，维护上下文
4. **Planner**: 规划器（LangGraph 中实现）
"""


def _langchain_topic_detail(day: int) -> str:
    return """
#### 为什么需要 LangChain？

纯 API 调用的痛点:
- 多模型切换需要改大量代码
- Prompt 管理混乱
- 链式调用难以维护
- 缺少 Memory、Retriever 等开箱即用组件

#### LCEL 管道语法

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

chain = prompt | model | StrOutputParser()
result = chain.invoke({"input": "你好"})
```

#### 生态全景

- **LangChain**: 组件库 + 链式编排
- **LangGraph**: 图结构 Agent 编排
- **LangSmith**: 调试追踪平台
"""


def _finetune_topic_detail(day: int) -> str:
    return """
#### 微调 vs RAG vs Prompt 决策树

```
数据是公开知识？ → RAG
需要改变模型行为/风格？ → 微调
只是临时任务？ → Prompt 工程
```

#### LoRA 原理（通俗版）

> 不改动大模型全部参数，只训练一小撮「适配器」参数。
> 就像给一本厚书贴便利贴，而不是重写整本书。

#### 显存估算（经验公式）

> 7B 模型 LoRA 微调约需 16-24GB 显存
> 用 QLoRA 可降到 8-12GB
"""


def _docker_topic_detail(day: int) -> str:
    return """
#### 核心概念

| 概念 | 类比 | 说明 |
|------|------|------|
| 镜像 Image | 安装光盘 | 只读模板 |
| 容器 Container | 运行中的程序 | 镜像的实例 |
| Dockerfile | 安装说明书 | 构建镜像的脚本 |
| Docker Compose | 批量启动器 | 多容器编排 |

#### 示例 Dockerfile

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```
"""


def _fastapi_topic_detail(day: int) -> str:
    return """
#### 最小 FastAPI 应用

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AI Chat API")

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

@app.post("/chat")
async def chat(req: ChatRequest):
    # 调用大模型 API
    reply = f"收到: {req.message}"
    return {"reply": reply}
```

#### 自动文档

启动后访问:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
"""


def _json_topic_detail(day: int) -> str:
    return """
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
"""


def _function_topic_detail(day: int) -> str:
    return """
#### Python 函数核心语法

```python
def greet(name: str, greeting: str = "你好") -> str:
    \"\"\"问候函数 — 文档字符串说明用途\"\"\"
    return f"{greeting}, {name}!"

# 调用
print(greet("张三"))           # 你好, 张三!
print(greet("李四", "Hello"))  # Hello, 李四!
```

#### 与大模型开发的联系

- Day 12: 封装 API 调用为函数
- Day 14: 项目一代码全部函数化
- Day 19: Function Calling 是「让大模型调用你的函数」
"""


def _career_topic_detail(day: int, topic: str) -> str:
    return f"""
#### {topic}

今日以实战演练和职业准备为主。

##### 简历 STAR 法则

- **S**ituation: 项目背景
- **T**ask: 你的任务
- **A**ction: 你做了什么（技术栈、架构）
- **R**esult: 量化成果（准确率、用户数、响应时间）

##### 项目描述模板

```
项目名称: 企业级知识库问答系统
技术栈: Python, LangChain, Chroma, FastAPI, React
描述:
- 基于 RAG 技术构建企业知识库问答，支持 PDF/Word/Markdown 多格式文档上传
- 实现混合检索(BM25+向量) + Rerank 重排，答案忠实度达 92%
- 使用 FastAPI + SSE 实现流式输出，Docker Compose 一键部署
```
"""


def _homework_block(day: int, project: str, evening: list[str]) -> str:
    evening_items = "\n".join(f"- {e}" for e in evening)
    return f"""
{section("课后作业", 2)}

### 必做

1. 完成今日实操项目「{project}」
2. 提交代码到 GitHub（commit message: `Day {day}: {project}`）
3. 在学习笔记中记录 3 个今天学到的新知识点

### 晚自习

{evening_items}

### 选做

1. 阅读官方文档中与今日主题相关的章节
2. 尝试优化今日代码（更优雅的错误处理、更清晰的注释）
"""


def _generate_footer(day: int) -> str:
    return f"""
{hr()}

**第 {day}/70 天 · {COURSE_META['title']}**

> 坚持每一天，70 天后你将成为一名合格的大模型应用开发者。
"""


def write_code_files():
    """生成关键天的代码文件"""
    CODE_DIR.mkdir(parents=True, exist_ok=True)

    # Day 1
    day01_dir = CODE_DIR / "day01"
    day01_dir.mkdir(exist_ok=True)
    (day01_dir / "day01_personal_card.py").write_text(DAY1_CODE, encoding="utf-8")
    (day01_dir / "hello.py").write_text('print("Hello, LLM World!")\n', encoding="utf-8")
    (day01_dir / "requirements.txt").write_text("# Day 1 无第三方依赖\n", encoding="utf-8")

    # 其余每天生成代码骨架
    for day in range(2, 71):
        if day not in DAYS:
            continue
        title, _, _, _, project, _, _ = DAYS[day]
        day_dir = CODE_DIR / f"day{day:02d}"
        day_dir.mkdir(exist_ok=True)
        code = f'''\
# ================================
# 文件名: day{day:02d}_main.py
# 主题: Day {day} — {project}
# ================================

"""Day {day} 实操项目: {project}"""


def main():
    print("Day {day}: {project}")
    # TODO: 按课件 day{day:02d}.md 逐步实现
    pass


if __name__ == "__main__":
    main()
'''
        (day_dir / f"day{day:02d}_main.py").write_text(code, encoding="utf-8")


def generate_all():
    DAYS_DIR.mkdir(parents=True, exist_ok=True)

    for day in range(1, 71):
        md = generate_day_markdown(day)
        out = DAYS_DIR / f"day{day:02d}.md"
        out.write_text(md, encoding="utf-8")
        print(f"✅ Generated {out.name} ({len(md):,} chars)")

    write_code_files()
    print(f"\n📁 Output: {DAYS_DIR}")
    print(f"📁 Code:   {CODE_DIR}")


if __name__ == "__main__":
    generate_all()
