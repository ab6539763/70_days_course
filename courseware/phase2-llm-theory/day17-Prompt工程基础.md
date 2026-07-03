# Day 17: Prompt 工程基础

> **培训阶段**: 第二阶段 大模型理论与 API | **第 3 周 | **学习时长**: 约 6-8 小时  
> **今日关键词**: Prompt 四要素、Zero/One/Few-shot、角色扮演、输出格式约束

---

## 📍 课程导航

### 上节回顾
**Day 16** 我们掌握了：

- `temperature`、`top_p`、`max_tokens` 等 API 核心参数
- `system` / `user` / `assistant` 三种角色的设计策略
- 流式输出（stream）的实现与 SSE 数据流解析
- 场景化参数预设与对比实验方法

今天进入 **Prompt 工程**——这是大模型应用开发中投入产出比最高的技能。

### 本节学习目标
完成本日学习后，你将能够：

1. 运用 Prompt 四要素（角色、任务、上下文、格式）设计高质量提示词
2. 区分并应用 Zero-shot、One-shot、Few-shot 三种提示策略
3. 设计角色扮演 Prompt，让 AI 扮演特定专家
4. 使用格式约束确保输出结构化、可解析
5. 独立完成 10 个典型场景的 Prompt 模板

### 与后续课程的衔接
- **Day 1** f-string → Prompt 模板就是「带变量的 f-string」
- **Day 5** JSON → 格式约束常要求模型输出 JSON
- **Day 13** 正则表达式 → 验证和清洗模型输出
- **Day 16** system prompt → 今天是系统化的 Prompt 设计方法论
- **Day 18** CoT、ToT 等进阶技巧 → 今天的四要素是基础
- **Day 25+** RAG → Prompt 中注入检索到的上下文

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：Prompt 工程概述

#### 1.1 什么是 Prompt 工程

**Prompt 工程（Prompt Engineering）** 是通过设计和优化输入文本（Prompt），引导大模型产生期望输出的技术与艺术。

```
普通用户                    Prompt 工程师
┌─────────────┐            ┌─────────────┐
│ "帮我写代码"  │            │ 结构化 Prompt │
│  → 泛泛的回答 │            │  → 精确输出   │
└─────────────┘            └─────────────┘
```

**为什么 Prompt 工程重要？**

| 原因 | 说明 |
|------|------|
| 零成本高收益 | 不需要重新训练模型，改几个字就能提升效果 |
| 应用开发核心 | 80% 的大模型应用质量取决于 Prompt |
| 面试必考 | 「如何设计 Prompt」是高频面试题 |
| 与 RAG/Agent 协同 | 好的 Prompt 让检索和工具调用事半功倍 |

#### 1.2 Prompt 四要素框架

每个高质量 Prompt 都应包含以下四个要素（按重要性排序）：

```
┌─────────────────────────────────────────────────────────┐
│  ① 角色 (Role)      — AI 是谁？什么专业背景？              │
│  ② 任务 (Task)      — 要做什么？具体目标是什么？            │
│  ③ 上下文 (Context)  — 背景信息、输入数据、约束条件         │
│  ④ 格式 (Format)    — 输出长什么样？JSON？表格？列表？      │
└─────────────────────────────────────────────────────────┘
```

**四要素示例**

```python
# 差的 Prompt（只有任务）
bad_prompt = "分析这段代码"

# 好的 Prompt（四要素齐全）
good_prompt = """
## 角色
你是一位有 10 年经验的 Python 高级开发工程师，擅长代码审查和性能优化。

## 任务
审查以下 Python 代码，找出潜在的 bug、性能问题和安全隐患。

## 上下文
这是一个处理用户上传文件的 Web 应用后端代码：
```python
{code}
```

## 格式
请按以下 JSON 格式输出：
{
  "issues": [
    {"severity": "high/medium/low", "line": 行号, "description": "问题描述", "fix": "修复建议"}
  ],
  "summary": "总体评价（一句话）"
}
"""
```

#### 1.3 Prompt 模板化

结合 Day 1 的 f-string，Prompt 应该模板化：

```python
# day17/prompt_templates.py
"""Prompt 模板库"""

CODE_REVIEW_TEMPLATE = """
## 角色
你是一位资深 {language} 开发工程师。

## 任务
审查以下代码，找出 bug 和性能问题。

## 上下文
```{language}
{code}
```

## 格式
以编号列表输出，每项包含：问题描述、严重程度、修复建议。
"""


def build_prompt(template: str, **kwargs) -> str:
    """填充 Prompt 模板"""
    return template.format(**kwargs)


# 使用
prompt = build_prompt(CODE_REVIEW_TEMPLATE,
                      language="python",
                      code="def add(a, b): return a + b")
```

---

### 9:45 - 10:30 | 模块二：Zero-shot / One-shot / Few-shot

#### 2.1 三种提示策略

```
Zero-shot（零样本）          One-shot（单样本）         Few-shot（少样本）
┌──────────────┐           ┌──────────────┐          ┌──────────────┐
│ 只给任务描述   │           │ 给 1 个示例   │          │ 给 2-5 个示例  │
│ 不提供示例    │           │ 展示期望格式   │          │ 展示多种情况   │
└──────────────┘           └──────────────┘          └──────────────┘
  简单任务适用                格式要求严格时              复杂/模糊任务
```

#### 2.2 Zero-shot

**适用**：模型已经理解的常见任务。

```python
zero_shot_prompt = """
将以下中文句子翻译成英文，保持原意和语气。

句子：{sentence}
"""
```

**示例**

```python
# 情感分析 - Zero-shot
prompt = "判断以下评论的情感倾向（正面/负面/中性）：\n这家餐厅的服务太差了，等了一个小时才上菜。"
# 模型输出：负面
```

#### 2.3 One-shot

**适用**：需要特定输出格式，给一个示例最经济。

```python
one_shot_prompt = """
从文本中提取人名、地点和时间，以 JSON 格式输出。

示例：
输入：张三昨天在北京参加了人工智能大会。
输出：{"persons": ["张三"], "locations": ["北京"], "times": ["昨天"]}

输入：{input_text}
输出：
"""
```

#### 2.4 Few-shot

**适用**：任务复杂、边界情况多、需要展示多种模式。

```python
few_shot_prompt = """
将用户意图分类为以下类别之一：查询天气、设置提醒、播放音乐、其他。

示例 1：
用户：明天北京会下雨吗？
分类：查询天气

示例 2：
用户：帮我定一个明天早上 8 点的闹钟
分类：设置提醒

示例 3：
用户：播放周杰伦的晴天
分类：播放音乐

示例 4：
用户：你好
分类：其他

用户：{user_input}
分类：
"""
```

#### 2.5 选择策略的决策树

```
任务是否简单且模型熟悉？
  ├─ 是 → Zero-shot
  └─ 否 → 输出格式是否严格？
            ├─ 是 → One-shot（给 1 个格式示例）
            └─ 否 → 是否有多种情况需要覆盖？
                      ├─ 是 → Few-shot（2-5 个示例）
                      └─ 否 → Zero-shot + 详细格式描述
```

> 💡 **Token 成本**：Few-shot 示例占用输入 Token。示例越精炼越好，Day 15 学的 Token 计数在这里直接派上用场。

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：角色扮演与输出格式约束

#### 3.1 角色扮演（Role Playing）

让 AI 扮演特定角色，可以显著提升输出质量。

**角色设计要素**

| 要素 | 示例 |
|------|------|
| 身份 | 资深律师、儿科医生、UX 设计师 |
| 经验 | 10 年从业经验、处理过 1000+ 案例 |
| 风格 | 严谨专业 / 通俗易懂 / 幽默风趣 |
| 限制 | 只讨论 XX 领域、不做 XX |

```python
ROLE_PROMPTS = {
    "python_tutor": """你是一位耐心的 Python 编程导师，专门教零基础学员。
- 用生活中的类比解释编程概念
- 每个概念配一个不超过 10 行的代码示例
- 鼓励学员，不说「这很简单」
- 学员出错时，引导他自己发现错误""",

    "legal_advisor": """你是一位中国法律顾问，专注于劳动合同领域。
- 引用具体法律条文（劳动合同法、工伤保险条例等）
- 免责声明：你的回答仅供参考，不构成法律意见
- 用通俗语言解释法律术语
- 遇到复杂案件建议咨询执业律师""",

    "data_analyst": """你是一位数据分析专家，擅长用数据讲故事。
- 分析时先给出核心结论，再展示数据支撑
- 使用 Markdown 表格呈现数据
- 指出数据的局限性和可能的偏差
- 给出可执行的建议""",
}
```

#### 3.2 输出格式约束

**为什么需要格式约束？**

模型默认输出自然语言，但应用开发通常需要结构化数据（JSON、CSV、表格）以便程序解析。

**常用格式约束技巧**

| 技巧 | 示例 |
|------|------|
| 明确指定格式 | 「以 JSON 格式输出」 |
| 给出 Schema | 「字段：name(str), age(int), email(str)」 |
| 给完整示例 | 展示期望输出的完整样例 |
| 禁止多余内容 | 「只输出 JSON，不要其他文字」 |
| 使用 Markdown | 「用 Markdown 表格输出」 |

```python
# JSON 格式约束
json_prompt = """
分析以下产品评论，提取信息。

评论：{review}

严格按以下 JSON 格式输出，不要包含任何其他文字：
{
  "sentiment": "positive/negative/neutral",
  "rating": 1-5,
  "keywords": ["关键词1", "关键词2"],
  "summary": "一句话总结"
}
"""

# Markdown 表格约束
table_prompt = """
将以下数据整理为 Markdown 表格，包含表头和对齐：

{raw_data}

要求：
- 表头加粗
- 数字右对齐
- 按销售额降序排列
"""

# 编号列表约束
list_prompt = """
列出学习大模型应用开发的 5 个步骤。

格式要求：
1. 每步一行，格式为「步骤N：[动词]+[具体内容]」
2. 每步不超过 30 字
3. 按学习顺序排列
"""
```

#### 3.3 输出解析与验证

```python
# day17/output_parser.py
"""解析和验证模型输出"""

import json
import re


def extract_json(text: str) -> dict:
    """从模型输出中提取 JSON（容错）"""
    # 尝试直接解析
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 尝试从 ```json 代码块中提取
    match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
    if match:
        return json.loads(match.group(1))

    # 尝试找到第一个 { 到最后一个 }
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group())

    raise ValueError(f"无法从文本中提取 JSON: {text[:200]}")


def validate_sentiment(data: dict) -> bool:
    """验证情感分析输出格式"""
    required = ["sentiment", "rating", "keywords", "summary"]
    if not all(k in data for k in required):
        return False
    if data["sentiment"] not in ("positive", "negative", "neutral"):
        return False
    if not isinstance(data["rating"], int) or not 1 <= data["rating"] <= 5:
        return False
    return True
```

---

## 🌆 下午课程（14:00 - 17:00）

### 14:00 - 17:00 | 模块四：10 个场景 Prompt 实战

#### 场景 1：智能客服

```python
CUSTOMER_SERVICE_PROMPT = """
## 角色
你是「智慧科技」的在线客服小智，负责解答产品咨询和售后问题。

## 任务
回答用户关于产品的咨询，无法回答时引导用户联系人工客服。

## 上下文
产品信息：
- 产品名：SmartHome Pro 智能音箱
- 价格：¥599
- 功能：语音控制、音乐播放、智能家居联动
- 保修：1 年免费保修
- 客服电话：400-123-4567

用户问题：{question}

## 格式
- 语气友好专业
- 回答不超过 100 字
- 涉及退货/投诉时，提供客服电话
"""
```

#### 场景 2：代码生成

```python
CODE_GEN_PROMPT = """
## 角色
你是 Python 开发专家，代码风格遵循 PEP 8。

## 任务
根据需求编写 Python 函数，包含类型注解和 docstring。

## 上下文
需求：{requirement}

## 格式
```python
# 只输出代码，包含：
# 1. 类型注解
# 2. Google 风格 docstring
# 3. 2-3 个使用示例（用 if __name__ == "__main__"）
```
"""
```

#### 场景 3：文章摘要

```python
SUMMARY_PROMPT = """
## 角色
你是资深编辑，擅长提炼文章核心观点。

## 任务
为以下文章生成摘要。

## 上下文
文章：
{article}

## 格式
- 摘要长度：{max_words} 字以内
- 结构：一句话核心观点 + 3 个要点（编号列表）
- 保留关键数据和专有名词
"""
```

#### 场景 4：SQL 生成

```python
SQL_GEN_PROMPT = """
## 角色
你是数据库专家，精通 MySQL 和 PostgreSQL。

## 任务
根据自然语言描述生成 SQL 查询语句。

## 上下文
数据库表结构：
{schema}

用户需求：{query}

## 格式
```sql
-- 只输出 SQL，加简要注释
```
注意：只生成 SELECT 查询，不生成 INSERT/UPDATE/DELETE。
"""
```

#### 场景 5：邮件撰写

```python
EMAIL_PROMPT = """
## 角色
你是商务沟通专家，擅长撰写得体的商务邮件。

## 任务
根据要点撰写一封商务邮件。

## 上下文
- 收件人：{recipient}
- 目的：{purpose}
- 要点：{key_points}
- 语气：{tone}（正式/友好/紧急）

## 格式
主题：[邮件主题]

正文：
[邮件正文，分段落]

此致敬礼
[发件人姓名]
"""
```

#### 场景 6：数据清洗指令

```python
DATA_CLEAN_PROMPT = """
## 角色
你是数据清洗专家。

## 任务
分析以下原始数据的问题，并给出清洗后的结果。

## 上下文
原始数据（CSV 格式）：
{raw_csv}

已知问题：{known_issues}

## 格式
1. 问题诊断（编号列表）
2. 清洗后的数据（CSV 格式，用 ```csv 包裹）
3. 清洗说明（每个修改的原因）
"""
```

#### 场景 7：学习计划制定

```python
STUDY_PLAN_PROMPT = """
## 角色
你是资深学习规划师，熟悉大模型应用开发学习路径。

## 任务
为用户制定个性化学习计划。

## 上下文
- 当前水平：{level}（零基础/有编程基础/有 AI 基础）
- 可用时间：每天 {hours} 小时
- 学习目标：{goal}
- 期限：{deadline}

## 格式
| 周次 | 主题 | 每日任务 | 检验标准 |
|------|------|----------|----------|
（按周规划，每周 5 个学习日）
"""
```

#### 场景 8：产品评论分析

```python
REVIEW_ANALYSIS_PROMPT = """
## 角色
你是电商数据分析专家。

## 任务
批量分析产品评论，输出结构化分析报告。

## 上下文
产品：{product_name}
评论列表：
{reviews}

## 格式
{
  "overall_sentiment": "positive/negative/mixed",
  "average_rating": 浮点数,
  "top_complaints": ["投诉1", "投诉2", "投诉3"],
  "top_praises": ["好评1", "好评2", "好评3"],
  "improvement_suggestions": ["建议1", "建议2"]
}
只输出 JSON。
"""
```

#### 场景 9：技术文档问答

```python
TECH_QA_PROMPT = """
## 角色
你是 {technology} 的技术文档专家。

## 任务
基于提供的文档内容回答用户问题。只使用文档中的信息，不要编造。

## 上下文
文档内容：
{document}

用户问题：{question}

## 格式
- 直接回答问题
- 引用文档中的相关段落（用 > 引用格式）
- 如果文档中没有相关信息，回答「文档中未找到相关信息」
"""
```

#### 场景 10：多语言翻译

```python
TRANSLATE_PROMPT = """
## 角色
你是专业翻译，精通 {source_lang} 和 {target_lang}。

## 任务
翻译以下文本，保持原意、语气和专业术语的准确性。

## 上下文
原文（{source_lang}）：
{text}

翻译要求：
- 风格：{style}（直译/意译/本地化）
- 专业术语：保留英文原文并在括号中标注中文

## 格式
译文（{target_lang}）：
[翻译结果]

术语对照：
| 原文 | 译文 |
|------|------|
"""
```

#### 4.1 综合项目：Prompt 模板管理器

```python
# day17/prompt_manager.py
"""Prompt 模板管理器"""

import os
import json
import requests
from pathlib import Path

API_KEY = os.getenv("DEEPSEEK_API_KEY")
URL = "https://api.deepseek.com/v1/chat/completions"


class PromptManager:
    def __init__(self, templates_dir: str = "day17/templates"):
        self.templates_dir = Path(templates_dir)
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.templates = {}
        self._load_templates()

    def _load_templates(self):
        for f in self.templates_dir.glob("*.json"):
            with open(f, encoding="utf-8") as fp:
                self.templates[f.stem] = json.load(fp)

    def save_template(self, name: str, template: str, description: str = ""):
        data = {"template": template, "description": description}
        path = self.templates_dir / f"{name}.json"
        with open(path, "w", encoding="utf-8") as fp:
            json.dump(data, fp, ensure_ascii=False, indent=2)
        self.templates[name] = data

    def render(self, name: str, **kwargs) -> str:
        if name not in self.templates:
            raise KeyError(f"模板 '{name}' 不存在，可用: {list(self.templates.keys())}")
        return self.templates[name]["template"].format(**kwargs)

    def run(self, name: str, **kwargs) -> str:
        prompt = self.render(name, **kwargs)
        resp = requests.post(URL, json={
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
        }, headers={"Authorization": f"Bearer {API_KEY}"}, timeout=60)
        return resp.json()["choices"][0]["message"]["content"]

    def list_templates(self) -> list:
        return [(name, data.get("description", ""))
                for name, data in self.templates.items()]


# 使用示例
if __name__ == "__main__":
    pm = PromptManager()
    pm.save_template("code_review", CODE_GEN_PROMPT, "代码生成")
    pm.save_template("summary", SUMMARY_PROMPT, "文章摘要")
    print("可用模板:", pm.list_templates())
```

---

## 🌙 晚自习（19:00 - 21:00）

### 19:00 - 20:00 | Prompt 优化技巧

#### 迭代优化流程

```
初版 Prompt → 测试 3-5 个用例 → 分析失败案例 → 修改 Prompt → 再测试
     ↑                                                              │
     └──────────────────────────────────────────────────────────────┘
```

#### 常见问题与修复

| 问题 | 原因 | 修复 |
|------|------|------|
| 输出太长 | 未限制长度 | 加「不超过 N 字」 |
| 格式不对 | 格式描述模糊 | 给完整示例 |
| 答非所问 | 任务不清晰 | 重写任务描述 |
| 编造信息 | 未要求基于上下文 | 加「只使用提供的信息」 |
| 输出中英混杂 | 未指定语言 | 加「用中文回答」 |

### 20:00 - 21:00 | 自习答疑

- 完成 10 个场景 Prompt 的测试
- 将最佳 Prompt 保存到 `prompt_manager.py`
- 预习 Day 18 进阶技巧

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | Prompt 工程的价值与定位 | |
| 2 | 四要素框架（角色/任务/上下文/格式） | |
| 3 | Prompt 模板化与 f-string 结合 | |
| 4 | Zero-shot 适用场景 | |
| 5 | One-shot 示例设计 | |
| 6 | Few-shot 多样例策略 | |
| 7 | 角色扮演 Prompt 设计 | |
| 8 | 输出格式约束技巧 | |
| 9 | JSON 输出解析与验证 | |
| 10 | 10 个典型场景 Prompt 实战 | |

---

## 📝 课后作业

### 必做题

1. **四要素练习**：为以下任务编写完整 Prompt（含四要素）
   - 将会议纪要转为待办事项列表
   - 检查一封英文邮件的语法错误

2. **Few-shot 实验**：设计一个「文本分类」Few-shot Prompt（至少 3 个示例），测试 5 个不同输入

3. **Prompt 管理器**：完成 `prompt_manager.py`，至少保存 5 个模板，Git 提交

### 选做题

4. 对比 Zero-shot 和 Few-shot 在同一任务上的输出质量和 Token 消耗
5. 设计一个「Prompt 评审」Prompt——让 AI 评价另一个 Prompt 的质量
6. 为 Day 13 的文件处理项目编写 Prompt，实现「读取文件内容并生成摘要」

---

## 💡 常见问题 FAQ

**Q1: Prompt 越长越好吗？**

A: 不是。冗长的 Prompt 浪费 Token（Day 15），且可能分散模型注意力。追求「简洁、精确、结构化」。

**Q2: Few-shot 示例越多越好吗？**

A: 通常 2-5 个示例足够。过多示例占用 Token 且可能引入噪声。示例应覆盖典型情况和边界情况。

**Q3: 角色扮演真的有用吗？**

A: 有用。实验表明，明确的角色设定能显著提升输出质量，尤其在专业领域（法律、医疗、代码）。

**Q4: 模型不遵守格式约束怎么办？**

A: 策略一：降低 temperature（Day 16）。策略二：在 system prompt 中强调格式。策略三：用代码做后处理（正则提取 JSON）。策略四：使用 JSON Mode（Day 18）。

**Q5: 中文 Prompt 和英文 Prompt 哪个效果好？**

A: 取决于模型。Qwen 等中文优化模型用中文更好；GPT-4 对高质量英文 Prompt 响应略好。建议用目标用户使用的语言编写。

---

## 🔮 明日预习

**Day 18: Prompt 工程进阶**

明天你将学习：

- **Chain-of-Thought (CoT)** 思维链提示
- **Self-Consistency** 自洽性策略
- **Tree of Thoughts (ToT)** 思维树
- 提示词注入攻击与防御
- JSON Mode 与 Function Calling 初探

**预习建议**：思考一个问题：「如何让 AI 一步步推理而不是直接给答案？」

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 17*
