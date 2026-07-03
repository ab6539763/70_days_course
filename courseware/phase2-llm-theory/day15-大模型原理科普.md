# Day 15: 大模型原理科普

> **培训阶段**: 第二阶段 大模型理论与 API | **第 3 周** | **学习时长**: 约 6-8 小时  
> **今日关键词**: NLP 发展史、Transformer、预训练/SFT/RLHF、Token、tiktoken

---

## 📍 课程导航

### 上节回顾
恭喜你完成了 **第一阶段 Python 编程基础（Day 1-14）**！你已经掌握了：

- **Day 1-4**：变量、数据类型、运算符、字符串与 f-string（后续编写 Prompt 模板的基石）
- **Day 5-7**：列表、字典、JSON（大模型 API 请求/响应的核心数据格式）
- **Day 8-10**：函数、模块、`requests` 库（调用 API 的必备技能）
- **Day 11-12**：异常处理、环境变量、首次大模型 API 调用
- **Day 13-14**：文件读写、正则表达式、综合项目

今天开始 **第二阶段**，从「会用 Python」升级为「理解大模型原理 + 精通 API 调用」。

### 本节学习目标
完成本日学习后，你将能够：

1. 梳理 NLP 从规则系统到 Transformer 的发展脉络
2. 用通俗语言解释 Transformer 的核心机制（注意力、编码器/解码器）
3. 区分预训练、SFT、RLHF 三阶段训练流程及其作用
4. 理解 Token 的概念、计费逻辑与上下文窗口限制
5. 盘点 2025-2026 主流大模型及其适用场景
6. 使用 `tiktoken` 库进行 Token 计数与成本估算实操

### 与后续课程的衔接
- **Day 1** 的 f-string → 今天理解 Token 后，你会知道为什么 Prompt 长度直接影响 API 费用
- **Day 5** 的 JSON → 明天 API 参数（temperature、top_p 等）都以 JSON 形式传递
- **Day 12** 的 API 调用 → 今天补全「模型为什么能回答」的理论背景
- **Day 16-19** 将深入 API 参数与 Prompt 工程——今天打下的原理基础会让参数调优更有章法
- **Day 25+** RAG 阶段需要理解 Embedding 与向量相似度——今天的 Token 与模型架构知识是前置铺垫

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：NLP 发展史——从规则到神经网络

#### 1.1 什么是自然语言处理（NLP）

**自然语言处理（Natural Language Processing, NLP）** 是让计算机理解、生成和处理人类语言的技术领域。大语言模型是 NLP 发展至今最重要的里程碑。

**NLP 要解决的核心问题**

| 任务类型 | 示例 | 大模型能否胜任 |
|----------|------|----------------|
| 文本分类 | 判断邮件是否为垃圾邮件 | ✅ 优秀 |
| 命名实体识别 | 从新闻中提取人名、地名 | ✅ 优秀 |
| 机器翻译 | 中文 → 英文 | ✅ 优秀 |
| 问答系统 | 根据文档回答问题 | ✅（需 RAG 增强） |
| 文本生成 | 写文章、写代码 | ✅ 核心能力 |
| 情感分析 | 判断评论正面/负面 | ✅ 优秀 |

#### 1.2 NLP 发展四阶段

```
1950s-1980s          1990s-2000s           2010s                 2017-至今
┌──────────┐        ┌──────────┐         ┌──────────┐          ┌──────────┐
│ 规则系统  │   →    │ 统计方法  │    →    │ 深度学习  │     →    │Transformer│
│ 专家手写  │        │ N-gram   │         │ RNN/LSTM │          │ 大语言模型 │
│ 语法规则  │        │ HMM/CRF  │         │ Word2Vec │          │ GPT/BERT  │
└──────────┘        └──────────┘         └──────────┘          └──────────┘
```

**阶段一：规则系统（1950s-1980s）**

- 语言学家手工编写语法规则和词典
- 代表：ELIZA 聊天机器人（1966）
- 局限：规则无法覆盖语言的复杂性，维护成本极高

**阶段二：统计方法（1990s-2000s）**

- 从大量语料中统计词频、共现概率
- 代表：N-gram 语言模型、隐马尔可夫模型（HMM）
- 突破：不再依赖人工规则，数据驱动
- 局限：无法捕捉长距离依赖，「银行」在不同上下文含义不同

**阶段三：深度学习（2010s）**

- 用神经网络自动学习语言表示
- 代表：
  - **Word2Vec（2013）**：将词映射为向量，「国王 - 男人 + 女人 ≈ 女王」
  - **RNN/LSTM（2014-2016）**：能处理序列，但长文本容易「遗忘」
  - **Seq2Seq + Attention（2014-2015）**：机器翻译的突破

**阶段四：Transformer 时代（2017-至今）**

- 2017 年 Google 发表论文《Attention Is All You Need》
- 完全基于注意力机制，抛弃 RNN
- 2018 BERT → 2019 GPT-2 → 2020 GPT-3 → 2022 ChatGPT → 2024+ 多模态大模型

> 💡 **与 Python 基础的联系**：你在 Day 13 学的正则表达式属于「规则系统」思路；大模型用统计+神经网络替代了大部分手工规则，但正则仍在数据清洗（Day 25 RAG 文档预处理）中大量使用。

#### 1.3 为什么需要「大」模型

| 维度 | 小模型（百万参数） | 大模型（千亿参数） |
|------|-------------------|-------------------|
| 训练数据 | MB 级语料 | TB 级互联网文本 |
| 能力 | 单一任务 | 通用能力（涌现） |
| 使用方式 | 针对任务训练 | 预训练 + Prompt 即可 |
| 代表 | 传统 BERT-base | GPT-4、DeepSeek-V3 |

**涌现能力（Emergent Abilities）**：当模型规模超过某个阈值，会突然具备小模型没有的能力（如复杂推理、代码生成）。这是「大」的价值所在。

---

### 9:45 - 10:30 | 模块二：Transformer 通俗讲解

#### 2.1 核心思想：注意力机制（Attention）

**问题**：一句话中，每个词的含义取决于上下文。

例句：「我把 **苹果** 放进了 **冰箱**」vs「我买了一个 **苹果** 手机」

「苹果」的含义由周围的词决定。注意力机制就是让模型自动学习「当前词应该关注哪些其他词」。

**通俗类比：开卷考试**

```
传统 RNN：按顺序逐字阅读，读到后面可能忘了前面（闭卷考试）
Transformer：同时看到全文，每写一个字都可以「回头看」任何位置（开卷考试 + 划重点）
```

#### 2.2 Transformer 架构概览

```
                    Transformer 架构
    ┌─────────────────────────────────────────────┐
    │              输入: "我爱学习AI"               │
    │                    ↓                        │
    │         ┌─────────────────────┐             │
    │         │   Token Embedding   │  词嵌入     │
    │         │   + Position Encoding│  位置编码   │
    │         └──────────┬──────────┘             │
    │                    ↓                        │
    │    ┌───────────────────────────────┐        │
    │    │     Multi-Head Attention      │  多头注意力│
    │    │  （每个词关注全文其他词）        │        │
    │    └───────────────┬───────────────┘        │
    │                    ↓                        │
    │    ┌───────────────────────────────┐        │
    │    │      Feed Forward Network     │  前馈网络  │
    │    └───────────────┬───────────────┘        │
    │                    ↓                        │
    │         （重复 N 层，GPT-3 有 96 层）         │
    │                    ↓                        │
    │              输出概率分布                     │
    │         预测下一个 Token 是什么               │
    └─────────────────────────────────────────────┘
```

#### 2.3 编码器 vs 解码器

| 架构 | 代表模型 | 特点 | 适用场景 |
|------|----------|------|----------|
| 仅编码器（Encoder-only） | BERT | 双向理解全文 | 文本分类、NER |
| 仅解码器（Decoder-only） | GPT 系列 | 从左到右生成 | 文本生成、对话 |
| 编码器+解码器（Enc-Dec） | T5、BART | 理解+生成 | 翻译、摘要 |

**本课程重点**：GPT 类 Decoder-only 架构，因为 ChatGPT、DeepSeek、Qwen 等对话模型都采用此架构。

#### 2.4 大模型如何生成文字

大模型的本质：**下一个 Token 预测器**

```
输入: "今天天气"
模型计算概率:
  "很好" → 35%
  "不错" → 25%
  "真棒" → 15%
  "糟糕" → 10%
  ... 其他词

根据采样策略（temperature 等，Day 16 详讲）选择一个 Token
输出: "今天天气很好"

然后把这个结果作为新输入，继续预测下一个 Token...
循环直到生成结束标记 <EOS> 或达到 max_tokens
```

> 💡 **关键洞察**：大模型并不是「搜索数据库找答案」，而是基于概率「接龙」生成文本。这就是为什么它可能「一本正经地胡说八道」——幻觉（Hallucination）的根源。

#### 2.5 知识截止与幻觉

| 概念 | 说明 | 应对策略 |
|------|------|----------|
| 知识截止 | 训练数据有时间边界，不知道之后的事 | RAG 检索最新文档（Day 25+） |
| 幻觉 | 生成看似合理但实际错误的内容 | 降低 temperature、要求引用来源 |
| 上下文窗口 | 一次能处理的 Token 上限 | 控制输入长度、摘要压缩 |

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：预训练、SFT 与 RLHF

#### 3.1 大模型训练三阶段

```
阶段一                阶段二                 阶段三
预训练 (Pre-training)  微调 (SFT)            对齐 (RLHF/DPO)
┌─────────────┐      ┌─────────────┐       ┌─────────────┐
│ 海量无标注文本 │  →  │ 人工标注对话  │   →   │ 人类偏好排序  │
│ 学习语言规律  │      │ 学习指令遵循  │       │ 学习人类价值观 │
│ 成本: 极高   │      │ 成本: 中等   │       │ 成本: 较高   │
└─────────────┘      └─────────────┘       └─────────────┘
     ↓                    ↓                     ↓
  Base Model          Instruct Model         Chat Model
  (只会续写)           (能执行指令)            (对话友好)
```

#### 3.2 阶段一：预训练（Pre-training）

**目标**：让模型学会语言的统计规律

**数据**：互联网文本、书籍、代码、论文等（TB 级）

**任务**：给定前面的 Token，预测下一个 Token（自回归语言建模）

```python
# 预训练任务示意（非真实训练代码）
# 输入: "今天天气很"
# 标签: "好"（下一个 Token）
# 模型学习: P("好" | "今天天气很") 应该很高
```

**结果**：Base Model——能续写文本，但不会对话。你问它「你好」，它可能续写成「你好，我是来自...」而不是回答你。

#### 3.3 阶段二：监督微调（SFT, Supervised Fine-Tuning）

**目标**：教会模型遵循人类指令

**数据**：人工编写的高质量「指令-回答」对

```json
{
  "instruction": "将以下句子翻译成英文",
  "input": "今天天气很好",
  "output": "The weather is nice today."
}
```

**类比**：预训练是「读完整个图书馆」，SFT 是「上培训班学怎么回答问题」。

**结果**：Instruct Model——能执行指令，但可能回答有害内容或质量不稳定。

#### 3.4 阶段三：人类反馈强化学习（RLHF）

**目标**：让模型输出更符合人类偏好（有用、无害、诚实）

**流程**：

```
1. 模型对同一问题生成多个回答
2. 人类标注员对回答排序（A > B > C > D）
3. 训练「奖励模型」学习人类偏好
4. 用强化学习优化生成策略
```

**替代方案**：DPO（Direct Preference Optimization）、RLAIF（AI 反馈）等，效果类似但更高效。

**结果**：Chat Model——就是我们日常使用的对话模型。

#### 3.5 对应用开发者的启示

| 训练阶段 | 你需要关心吗 | 原因 |
|----------|-------------|------|
| 预训练 | ❌ 一般不需要 | 由模型厂商完成，成本极高 |
| SFT | ⚠️ 了解即可 | Day 51-55 会学 LoRA 微调（轻量 SFT） |
| RLHF | ❌ 一般不需要 | 厂商已对齐，你通过 Prompt 进一步引导 |
| **Prompt 工程** | ✅ **核心技能** | 在不重训模型的情况下控制输出（Day 17-18） |
| **RAG** | ✅ **核心技能** | 注入外部知识弥补知识截止（Day 25+） |

---

## 🌆 下午课程（14:00 - 17:00）

### 14:00 - 15:15 | 模块四：Token 深度理解

#### 4.1 什么是 Token

**Token** 是大模型处理文本的最小单位。它不是「一个字」也不是「一个词」，而是介于两者之间的子词片段。

**示例：「我爱学习人工智能」的 Token 切分**

| 模型 | Token 切分结果 | Token 数 |
|------|---------------|----------|
| GPT-4 (cl100k_base) | `["我", "爱", "学习", "人工", "智能"]` | 5 |
| 英文 "Hello world" | `["Hello", " world"]` | 2 |
| 英文 "unhappiness" | `["un", "happiness"]` | 2 |

**为什么用子词而非整词？**

- 平衡词表大小与表达能力
- 未登录词（OOV）可以拆成已知子词
- 中文通常 1-2 字一个 Token，英文约 4 字符一个 Token

#### 4.2 Token 与计费

API 按 Token 计费，理解 Token 是控制成本的关键。

| 模型 | 输入价格（约） | 输出价格（约） | 上下文窗口 |
|------|---------------|---------------|-----------|
| DeepSeek-V3 | ¥1/百万 Token | ¥2/百万 Token | 64K |
| GPT-4o | $2.5/百万 Token | $10/百万 Token | 128K |
| Qwen2.5-72B | ¥0.5/百万 Token | ¥2/百万 Token | 128K |

**成本估算公式**

```
总费用 = (输入 Token 数 × 输入单价) + (输出 Token 数 × 输出单价)
```

#### 4.3 上下文窗口（Context Window）

上下文窗口 = 输入 Token + 输出 Token 的上限。

```
┌─────────────────────────────────────────────┐
│            上下文窗口 (如 64K Token)          │
│  ┌──────────────────┬───────────────────┐  │
│  │   输入 (Prompt)   │   输出 (Completion) │  │
│  │   System + User   │   模型生成的回答     │  │
│  │   + History       │                   │  │
│  └──────────────────┴───────────────────┘  │
└─────────────────────────────────────────────┘
```

**超出窗口会怎样？** API 报错或自动截断最早的消息。Day 16 会学 `max_tokens` 参数控制输出长度。

#### 4.4 Token 与 Python 字符串的关系

```python
# Day 1 学的 len() 计算字符数
text = "我爱AI"
print(len(text))  # 4（4 个字符）

# Token 数通常不等于字符数
# "我爱AI" 可能被切分为 3-4 个 Token
# 需要用 tiktoken 等工具精确计算
```

---

### 15:15 - 15:30 | 课间休息

---

### 15:30 - 17:00 | 模块五：主流模型盘点 + tiktoken 实操

#### 5.1 2025-2026 主流大模型全景

| 模型 | 厂商 | 架构 | 上下文 | 特点 | 本课程 |
|------|------|------|--------|------|--------|
| GPT-4o | OpenAI | MoE | 128K | 综合最强，多模态 | 选修 |
| Claude 3.5 Sonnet | Anthropic | — | 200K | 代码/长文本优秀 | 选修 |
| DeepSeek-V3 | 深度求索 | MoE | 64K | 国产高性价比 | ✅ 主力 |
| Qwen2.5 | 阿里通义 | Dense/MoE | 128K | 中文优秀，开源 | ✅ 主力 |
| GLM-4 | 智谱 AI | — | 128K | 国产综合能力强 | 选修 |
| Llama 3.1 | Meta | Dense | 128K | 开源标杆 | ✅ 微调 |
| Gemini 2.0 | Google | — | 1M | 超长上下文 | 选修 |

**选型建议**

| 场景 | 推荐模型 | 理由 |
|------|----------|------|
| 学习练习 | DeepSeek-V3 | 便宜、国内访问快 |
| 中文应用 | Qwen2.5 | 中文理解最好 |
| 长文档分析 | Claude 3.5 / Gemini | 超长上下文 |
| 本地部署 | Llama 3.1 / Qwen2.5 | 开源可自托管 |
| 代码生成 | DeepSeek-Coder / Claude | 代码能力强 |

#### 5.2 安装 tiktoken

```bash
pip install tiktoken -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 5.3 tiktoken 实操：Token 计数

创建项目文件 `day15/token_counter.py`：

```python
# day15/token_counter.py
"""Token 计数与成本估算工具"""

import tiktoken


def count_tokens(text: str, model: str = "gpt-4o") -> int:
    """计算文本的 Token 数量"""
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    return len(tokens)


def show_tokens(text: str, model: str = "gpt-4o") -> None:
    """显示 Token 切分详情"""
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    print(f"文本: {text}")
    print(f"字符数: {len(text)}")
    print(f"Token 数: {len(tokens)}")
    print(f"Token 列表: {tokens}")
    print(f"切分结果: {[encoding.decode([t]) for t in tokens]}")
    print("-" * 50)


def estimate_cost(
    input_text: str,
    output_tokens: int = 500,
    input_price_per_million: float = 1.0,
    output_price_per_million: float = 2.0,
    model: str = "gpt-4o",
) -> dict:
    """估算 API 调用成本（单位：人民币元）"""
    input_tokens = count_tokens(input_text, model)
    input_cost = input_tokens / 1_000_000 * input_price_per_million
    output_cost = output_tokens / 1_000_000 * output_price_per_million
    total_cost = input_cost + output_cost
    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "input_cost_yuan": round(input_cost, 6),
        "output_cost_yuan": round(output_cost, 6),
        "total_cost_yuan": round(total_cost, 6),
    }


if __name__ == "__main__":
    # 测试不同文本的 Token 切分
    show_tokens("Hello, world!")
    show_tokens("我爱学习大模型应用开发")
    show_tokens("The quick brown fox jumps over the lazy dog")

  # 对比中英文 Token 效率
    chinese = "人工智能正在改变世界的运作方式，大语言模型是这一变革的核心驱动力。"
    english = "Artificial intelligence is transforming how the world works, and large language models are at the core of this revolution."
    print(f"中文 ({len(chinese)} 字符): {count_tokens(chinese)} Token")
    print(f"英文 ({len(english)} 字符): {count_tokens(english)} Token")

    # 成本估算
    prompt = "请详细解释什么是 Transformer 架构，包括注意力机制的原理。"
    cost = estimate_cost(prompt, output_tokens=1000)
    print(f"\n成本估算: {cost}")
```

**运行**

```bash
cd ~/llm-course
python3 day15/token_counter.py
```

**期望输出（部分）**

```
文本: 我爱学习大模型应用开发
字符数: 11
Token 数: 8
切分结果: ['我', '爱', '学习', '大', '模型', '应用', '开发']
--------------------------------------------------
中文 (33 字符): 22 Token
英文 (118 字符): 22 Token
```

#### 5.4 实操练习：Prompt 长度优化

```python
# day15/prompt_optimizer.py
"""对比冗长 Prompt 与精简 Prompt 的 Token 差异"""

import tiktoken

encoding = tiktoken.encoding_for_model("gpt-4o")

verbose_prompt = """
请你扮演一位非常专业的人工智能领域专家，拥有丰富的学术研究经验和深厚的技术背景。
我需要你详细地、全面地向一位初学者解释什么是 Transformer 架构。
请确保你的解释通俗易懂，同时又不失专业性和准确性。
请从注意力机制开始讲起，然后介绍编码器和解码器的结构...
"""  # 冗长版

concise_prompt = "用通俗语言向初学者解释 Transformer 架构，包括注意力机制、编码器/解码器。"

v_tokens = len(encoding.encode(verbose_prompt))
c_tokens = len(encoding.encode(concise_prompt))

print(f"冗长 Prompt: {v_tokens} Token")
print(f"精简 Prompt: {c_tokens} Token")
print(f"节省: {v_tokens - c_tokens} Token ({(1 - c_tokens/v_tokens)*100:.1f}%)")
```

> 💡 **实践建议**：在 Day 17 Prompt 工程中，精简 Prompt 既省钱又往往效果更好——废话会干扰模型注意力。

#### 5.5 下午小结项目：Token 预算管理器

```python
# day15/token_budget.py
"""Token 预算管理器——确保不超出上下文窗口"""

import tiktoken

MAX_CONTEXT = 64000  # DeepSeek-V3 上下文窗口
RESERVED_FOR_OUTPUT = 4096  # 预留给模型输出


class TokenBudget:
    def __init__(self, max_context: int = MAX_CONTEXT, reserved_output: int = RESERVED_FOR_OUTPUT):
        self.max_context = max_context
        self.reserved_output = reserved_output
        self.max_input = max_context - reserved_output
        self.encoding = tiktoken.encoding_for_model("gpt-4o")
        self.used = 0

    def add(self, text: str) -> bool:
        """添加文本，返回是否成功（未超预算）"""
        tokens = len(self.encoding.encode(text))
        if self.used + tokens > self.max_input:
            print(f"⚠️ 超出预算！需要 {tokens} Token，剩余 {self.max_input - self.used}")
            return False
        self.used += tokens
        return True

    def remaining(self) -> int:
        return self.max_input - self.used

    def report(self) -> None:
        pct = self.used / self.max_input * 100
        print(f"已用: {self.used}/{self.max_input} Token ({pct:.1f}%)")
        print(f"剩余: {self.remaining()} Token")


# 使用示例
budget = TokenBudget()
budget.add("你是一个有帮助的AI助手。")  # system prompt
budget.add("请解释什么是 RAG？")  # user message
budget.report()
```

---

## 🌙 晚自习（19:00 - 21:00）

### 19:00 - 20:00 | 原理巩固与拓展阅读

#### 推荐资源

| 资源 | 类型 | 链接/说明 |
|------|------|----------|
| The Illustrated Transformer | 图解博客 | Jay Alammar 经典文章 |
| Attention Is All You Need | 原始论文 | arXiv:1706.03762（可选读） |
| DeepSeek-V3 技术报告 | 模型报告 | 了解国产模型进展 |
| OpenAI Tokenizer | 在线工具 | platform.openai.com/tokenizer |

#### 自测题（口头回答）

1. RNN 和 Transformer 处理长文本的核心区别是什么？
2. 预训练、SFT、RLHF 分别解决什么问题？
3. 为什么大模型可能产生幻觉？如何缓解？
4. 中文同样意思的 Prompt，Token 数一定比英文少吗？

### 20:00 - 21:00 | 自习答疑

- 确保 `tiktoken` 安装成功，所有示例代码可运行
- 用自己的话写一段「Transformer 原理总结」（200 字以内）
- 预习 Day 16：API 核心参数

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | NLP 发展四阶段（规则→统计→深度学习→Transformer） | |
| 2 | 注意力机制的核心思想 | |
| 3 | Transformer 架构（Embedding、Attention、FFN） | |
| 4 | 编码器/解码器/Enc-Dec 三种架构及代表模型 | |
| 5 | 下一个 Token 预测与文本生成原理 | |
| 6 | 预训练（Pre-training）的目标与数据 | |
| 7 | SFT 监督微调的作用 | |
| 8 | RLHF 人类反馈强化学习流程 | |
| 9 | Token 概念、切分规则与计费逻辑 | |
| 10 | 上下文窗口与 Token 预算管理 | |
| 11 | 主流大模型特点与选型建议 | |
| 12 | tiktoken 安装与 Token 计数实操 | |

---

## 📝 课后作业

### 必做题

1. **Token 计数实验**：分别计算以下文本的 Token 数，填写表格

   | 文本 | 字符数 | Token 数 | 字符/Token 比 |
   |------|--------|----------|---------------|
   | "Hello" | | | |
   | "你好" | | | |
   | 一篇 500 字中文短文 | | | |
   | 同等意思的英文翻译 | | | |

2. **成本估算器升级**：在 `token_counter.py` 基础上，添加：
   - 支持自定义模型价格
   - 支持从文件读取 Prompt 并计算 Token
   - 输出格式化报告

3. **Git 提交**：`git commit -m "Day 15: 大模型原理科普与 tiktoken 实操"`

### 选做题

4. 阅读 Jay Alammar 的 The Illustrated Transformer，用思维导图总结
5. 对比 GPT-4、DeepSeek-V3、Qwen2.5 三家 API 文档中的定价和上下文限制
6. 实现一个函数：给定消息列表（模拟多轮对话），计算总 Token 并在接近窗口上限时发出警告

---

## 💡 常见问题 FAQ

**Q1: 我需要理解 Transformer 的数学公式才能做应用开发吗？**

A: 不需要。应用开发者只需理解「注意力机制让模型关注上下文」「模型是概率接龙生成器」这两个核心直觉即可。数学细节是算法工程师的领域。

**Q2: Token 和字符数为什么差这么多？**

A: 中文通常 1-2 字一个 Token，但复杂词汇可能更多。英文按子词切分，平均约 4 字符一个 Token。API 计费用 Token 而非字符，所以必须用 `tiktoken` 精确计算。

**Q3: Base Model 和 Chat Model 有什么区别？我能直接用 Base Model 吗？**

A: Base Model 只会续写文本，不会对话。Chat Model 经过 SFT + RLHF，能遵循指令。API 默认提供 Chat Model，应用开发应使用 Chat/Instruct 版本。

**Q4: 为什么说「Prompt 工程」可以替代微调？**

A: 对于大多数应用场景，好的 Prompt + RAG 足以达到业务需求，无需重新训练模型。微调（Day 51-55）适合需要特定风格或私有知识的场景。先用 Prompt 工程，不够再考虑微调。

**Q5: tiktoken 的编码和国产模型（DeepSeek/Qwen）一致吗？**

A: 不完全一致。各模型有自己的词表和分词器。`tiktoken` 主要用于 OpenAI 系列模型的估算。国产模型可参考其官方文档提供的 Token 计算 API，或用近似估算（中文约 1.5-2 字/Token）。

**Q6: 上下文窗口越大越好吗？**

A: 不一定。更大的窗口意味着更高的输入成本和更慢的响应。应根据实际需求选择：简单问答 4K-8K 足够，长文档分析才需要 64K+。

---

## 🔮 明日预习

**Day 16: 大模型 API 核心参数**

明天你将学习：

- `temperature`、`top_p`、`max_tokens`、`presence_penalty` 等核心参数的含义与调优
- `system` / `user` / `assistant` 三种角色的设计策略
- **流式输出（stream）** 的原理与实现——让 AI 回答像 ChatGPT 一样逐字显示
- 参数对比实验：同一 Prompt 不同参数的输出差异

**预习建议**：回顾 Day 12 的 API 调用代码，思考「当时用了哪些参数？默认值是什么？能否优化？」

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 15*
