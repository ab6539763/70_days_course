# Day 26: LCEL 表达式与链

> **培训阶段**: 第三阶段 RAG 应用开发 | **第 5 周 | **学习时长**: 约 6-8 小时  
> **今日关键词**: LCEL、Runnable、RunnableParallel、RunnablePassthrough、链组合

---

## 📍 课程导航

### 上节回顾

**Day 25** 你完成了 LangChain 入门，掌握了 Model I/O 三大件：
- `ChatOpenAI` 模型调用与流式输出
- `PromptTemplate` / `ChatPromptTemplate` 模板化
- `StrOutputParser` / `JsonOutputParser` 输出解析
- 使用 `prompt | llm | parser` 搭建第一个链

今天将 **系统深入学习 LCEL**——LangChain Expression Language，这是 LangChain 0.3 的核心语法，也是后续构建 RAG 流水线的必备技能。

### 本节学习目标

完成本日学习后，你将能够：

1. 深入理解 `Runnable` 接口及其完整方法族
2. 熟练使用 LCEL 管道符 `|` 组合任意 Runnable 组件
3. 使用 `RunnableParallel` 实现并行执行
4. 使用 `RunnablePassthrough` 和 `RunnableLambda` 注入自定义逻辑
5. 使用 `RunnableAssign` 向字典状态中添加字段
6. 使用 `RunnableBranch` 实现条件分支
7. 构建多步骤文档处理流水线

### 与后续课程的衔接

- **Day 27** 将用 `RunnableWithMessageHistory` 为链注入 **Memory 记忆**
- **Day 30** 完整 RAG 链就是 LCEL 的组合：`检索 | 格式化 | Prompt | LLM | Parser`
- **Day 32-33** 高级 RAG 技术（Query Rewriting、Rerank）都通过 LCEL 链实现

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：Runnable 接口深入

#### 1.1 什么是 Runnable？

在 LangChain 中，**一切皆 Runnable**。Runnable 是一个统一接口，所有可组合组件都实现了它：

```
PromptTemplate  ─┐
ChatOpenAI      ─┤
StrOutputParser ─┤── 都实现了 Runnable 接口
Retriever       ─┤
自定义函数       ─┘
```

**Runnable 方法族**

| 方法 | 同步/异步 | 说明 |
|------|----------|------|
| `invoke(input)` | 同步 | 处理单个输入 |
| `batch(inputs)` | 同步 | 批量处理（内部可并行） |
| `stream(input)` | 同步 | 流式返回 |
| `ainvoke(input)` | 异步 | 异步单条 |
| `abatch(inputs)` | 异步 | 异步批量 |
| `astream(input)` | 异步 | 异步流式 |

```python
# day26/01_runnable_methods.py
"""Runnable 完整方法族演示"""
import asyncio
import time
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", temperature=0)
prompt = ChatPromptTemplate.from_template("用 20 字解释：{word}")
chain = prompt | llm | StrOutputParser()

# 1. invoke - 同步单条
result = chain.invoke({"word": "LCEL"})
print(f"invoke: {result}")

# 2. batch - 同步批量
results = chain.batch([{"word": "Chain"}, {"word": "Parser"}, {"word": "Runnable"}])
print(f"batch: {results}")

# 3. stream - 流式
print("stream: ", end="")
for chunk in chain.stream({"word": "Streaming"}):
    print(chunk, end="", flush=True)
print()

# 4. 异步方法
async def async_demo():
    result = await chain.ainvoke({"word": "Async"})
    print(f"ainvoke: {result}")

    results = await chain.abatch([{"word": "A"}, {"word": "B"}])
    print(f"abatch: {results}")

    print("astream: ", end="")
    async for chunk in chain.astream({"word": "AStream"}):
        print(chunk, end="", flush=True)
    print()

asyncio.run(async_demo())
```

#### 1.2 LCEL 管道符 `|` 的工作原理

```python
# day26/02_pipe_operator.py
"""管道符工作原理"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

prompt = ChatPromptTemplate.from_template("翻译为英文：{text}")
llm = ChatOpenAI(model="deepseek-chat", temperature=0)
parser = StrOutputParser()

# 以下两种写法等价
chain_v1 = prompt | llm | parser

from langchain_core.runnables import RunnableSequence
chain_v2 = RunnableSequence(prompt, llm, parser)

# 数据流：
# {"text": "你好"} → prompt → [HumanMessage] → llm → AIMessage → parser → "Hello"

result = chain_v1.invoke({"text": "LangChain 表达式语言"})
print(result)
```

**类型推断**：LCEL 会自动推断链的输入输出类型，IDE 可以获得较好的类型提示。

---

### 9:45 - 10:30 | 模块二：RunnableParallel 并行执行

#### 2.1 并行 vs 串行

```
串行：A → B → C  （总耗时 = A + B + C）
并行：A → {B, C} → D  （总耗时 = A + max(B, C) + D）
```

```python
# day26/03_runnable_parallel.py
"""RunnableParallel 并行执行"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", temperature=0.7)

# 定义多个分析链
summary_chain = (
    ChatPromptTemplate.from_template("用一句话总结：{text}")
    | llm | StrOutputParser()
)
sentiment_chain = (
    ChatPromptTemplate.from_template("判断以下文本的情感（正面/负面/中性）：{text}")
    | llm | StrOutputParser()
)
keywords_chain = (
    ChatPromptTemplate.from_template("提取 3 个关键词，逗号分隔：{text}")
    | llm | StrOutputParser()
)

# 并行执行三个分析
analysis_chain = RunnableParallel(
    original=RunnablePassthrough(),  # 保留原始输入
    summary=summary_chain,
    sentiment=sentiment_chain,
    keywords=keywords_chain,
)

text = "LangChain 是一个强大的 LLM 应用开发框架，极大简化了 RAG 系统的构建过程。"
result = analysis_chain.invoke({"text": text})

print("=== 并行分析结果 ===")
for key, value in result.items():
    print(f"{key}: {value}")
```

**输出示例**：
```
original: {'text': 'LangChain 是一个强大的...'}
summary: LangChain 是简化 RAG 系统构建的 LLM 应用开发框架。
sentiment: 正面
keywords: LangChain, RAG, LLM应用开发
```

#### 2.2 字典语法简写

```python
# day26/04_parallel_shorthand.py
"""字典语法简写 RunnableParallel"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", temperature=0)

# 字典语法自动创建 RunnableParallel
chain = {
    "summary": ChatPromptTemplate.from_template("总结：{text}") | llm | StrOutputParser(),
    "translation": ChatPromptTemplate.from_template("翻译为英文：{text}") | llm | StrOutputParser(),
}

result = chain.invoke({"text": "向量数据库用于存储和检索文本嵌入向量。"})
print(result)
# {'summary': '...', 'translation': '...'}
```

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：RunnablePassthrough 与 RunnableLambda

#### 3.1 RunnablePassthrough：透传与赋值

```python
# day26/05_passthrough.py
"""RunnablePassthrough 用法"""
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

# 基础透传：原样传递输入
passthrough = RunnablePassthrough()
result = passthrough.invoke({"key": "value"})
print(f"透传: {result}")

# assign：在输入字典中添加新字段
chain = RunnablePassthrough.assign(
    doubled=lambda x: x["number"] * 2,
    greeting=lambda x: f"Hello, {x['name']}!",
)

result = chain.invoke({"name": "张三", "number": 21})
print(f"assign: {result}")
# {'name': '张三', 'number': 21, 'doubled': 42, 'greeting': 'Hello, 张三!'}
```

#### 3.2 RunnableLambda：自定义函数

```python
# day26/06_runnable_lambda.py
"""RunnableLambda 自定义逻辑"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", temperature=0)

def preprocess(text: str) -> str:
    """文本预处理：去除多余空白"""
    return " ".join(text.split())

def postprocess(answer: str) -> dict:
    """后处理：包装为结构化结果"""
    return {
        "answer": answer,
        "length": len(answer),
        "has_code": "```" in answer,
    }

# 构建带预处理和后处理的链
chain = (
    RunnableLambda(preprocess)
    | ChatPromptTemplate.from_template("回答问题：{input}")
    | llm
    | StrOutputParser()
    | RunnableLambda(postprocess)
)

# 注意：RunnableLambda 接收的是上一个组件的输出
# 第一个 Lambda 接收原始输入，需要适配
full_chain = (
    RunnablePassthrough.assign(
        cleaned=lambda x: preprocess(x["question"])
    )
    | ChatPromptTemplate.from_template("回答问题：{cleaned}")
    | llm
    | StrOutputParser()
    | RunnableLambda(postprocess)
)

result = full_chain.invoke({"question": "  什么是   LCEL？  "})
print(result)
```

#### 3.3 RunnableAssign：状态累积

在复杂链中，经常需要逐步向状态字典添加字段：

```python
# day26/07_runnable_assign.py
"""RunnableAssign 状态累积"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", temperature=0)

# 多步骤链：查询改写 → 回答
chain = (
    RunnablePassthrough.assign(
        # 步骤1：改写查询
        rewritten_query=(
            ChatPromptTemplate.from_template(
                "将以下用户问题改写为更清晰的技术查询：{question}"
            )
            | llm | StrOutputParser()
        )
    )
    | RunnablePassthrough.assign(
        # 步骤2：基于改写后的查询回答
        answer=(
            ChatPromptTemplate.from_template(
                "基于以下查询给出专业回答：{rewritten_query}"
            )
            | llm | StrOutputParser()
        )
    )
)

result = chain.invoke({"question": "rag咋搞"})
print(f"原始问题: {result['question']}")
print(f"改写查询: {result['rewritten_query']}")
print(f"最终回答: {result['answer']}")
```

---

## 🌆 下午课程（14:00 - 17:00）

### 14:00 - 15:30 | 模块四：条件分支与错误处理

#### 4.1 RunnableBranch 条件分支

```python
# day26/08_runnable_branch.py
"""RunnableBranch 条件分支"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnableLambda
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", temperature=0)

# 分类链：判断问题类型
classifier = (
    ChatPromptTemplate.from_template(
        "判断以下问题属于哪个类别，只回答类别名称（技术/产品/其他）：{question}"
    )
    | llm | StrOutputParser()
)

# 不同类别的处理链
tech_chain = ChatPromptTemplate.from_template(
    "作为技术专家回答：{question}"
) | llm | StrOutputParser()

product_chain = ChatPromptTemplate.from_template(
    "作为产品经理回答：{question}"
) | llm | StrOutputParser()

general_chain = ChatPromptTemplate.from_template(
    "作为通用助手回答：{question}"
) | llm | StrOutputParser()

# 条件分支
router = RunnableBranch(
    (lambda x: "技术" in x["category"], tech_chain),
    (lambda x: "产品" in x["category"], product_chain),
    general_chain,  # 默认分支
)

full_chain = (
    RunnableLambda(lambda x: {"question": x["question"], "category": ""})
    | RunnableLambda(lambda x: {**x, "category": classifier.invoke(x)})
    | router
)

questions = [
    "如何优化 RAG 的检索精度？",
    "我们的 SaaS 产品应该增加 AI 功能吗？",
    "今天天气怎么样？",
]

for q in questions:
    answer = full_chain.invoke({"question": q})
    print(f"\nQ: {q}")
    print(f"A: {answer[:100]}...")
```

#### 4.2 链的配置与回调

```python
# day26/09_chain_config.py
"""链的配置：tags、metadata、callbacks"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.callbacks import StdOutCallbackHandler
from dotenv import load_dotenv

load_dotenv()

chain = (
    ChatPromptTemplate.from_template("解释：{concept}")
    | ChatOpenAI(model="deepseek-chat", temperature=0)
    | StrOutputParser()
)

# 带配置调用
result = chain.invoke(
    {"concept": "LCEL"},
    config={
        "tags": ["day26", "demo"],
        "metadata": {"user": "student"},
        "callbacks": [StdOutCallbackHandler()],
    },
)
```

#### 4.3 链的持久化与复用

```python
# day26/10_chain_serialization.py
"""链的序列化与加载"""
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.load import dumps, loads
from dotenv import load_dotenv

load_dotenv()

chain = (
    ChatPromptTemplate.from_template("解释：{topic}")
    | ChatOpenAI(model="deepseek-chat")
    | StrOutputParser()
)

# 序列化（注意：API Key 不会包含在序列化结果中）
serialized = dumps(chain)
print(f"序列化长度: {len(serialized)} 字符")

# 反序列化
restored_chain = loads(serialized)
result = restored_chain.invoke({"topic": "Runnable"})
print(f"恢复链结果: {result[:50]}...")
```

---

### 15:30 - 15:45 | 课间休息

---

### 15:45 - 17:00 | 模块五：下午实操——多步骤文档处理流水线

#### 5.1 项目需求

构建一个文档处理流水线，输入原始文本，依次完成：
1. 文本清洗
2. 语言检测
3. 摘要生成
4. 关键词提取
5. 结构化输出

```python
# day26/11_document_pipeline.py
"""下午实操：多步骤文档处理流水线"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from dotenv import load_dotenv
import json
import re

load_dotenv()

llm = ChatOpenAI(model="deepseek-chat", temperature=0.3)


def clean_text(text: str) -> str:
    """文本清洗：去除多余空白、特殊字符"""
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'[^\w\s\u4e00-\u9fff.,!?;:，。！？；：\-]', '', text)
    return text


def detect_language(text: str) -> str:
    """简单语言检测"""
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    total_chars = len(text.replace(" ", ""))
    if total_chars == 0:
        return "unknown"
    ratio = chinese_chars / total_chars
    return "zh" if ratio > 0.3 else "en"


# 构建流水线
pipeline = (
    # 步骤0：接收输入并清洗
    RunnablePassthrough.assign(
        cleaned=lambda x: clean_text(x["raw_text"]),
    )
    # 步骤1：语言检测
    | RunnablePassthrough.assign(
        language=lambda x: detect_language(x["cleaned"]),
    )
    # 步骤2：并行生成摘要和关键词
    | RunnablePassthrough.assign(
        summary=(
            RunnableLambda(lambda x: {"text": x["cleaned"]})
            | ChatPromptTemplate.from_template("用 50 字总结：{text}")
            | llm | StrOutputParser()
        ),
        keywords=(
            RunnableLambda(lambda x: {"text": x["cleaned"]})
            | ChatPromptTemplate.from_template("提取 5 个关键词，JSON 数组格式：{text}")
            | llm | StrOutputParser()
        ),
    )
    # 步骤3：格式化最终输出
    | RunnableLambda(lambda x: {
        "metadata": {
            "language": x["language"],
            "char_count": len(x["cleaned"]),
            "word_count": len(x["cleaned"].split()),
        },
        "summary": x["summary"],
        "keywords": x["keywords"],
        "original_preview": x["cleaned"][:100] + "..." if len(x["cleaned"]) > 100 else x["cleaned"],
    })
)


def main():
    test_docs = [
        "LangChain   是一个  强大的  LLM  应用开发框架！！！它提供了 LCEL 表达式语言，"
        "让开发者可以用管道符组合各种组件。RAG 系统的构建因此变得简单高效。",
        "Retrieval-Augmented Generation (RAG) combines information retrieval with "
        "text generation to produce more accurate and contextual responses.",
    ]

    for i, doc in enumerate(test_docs):
        print(f"\n{'='*60}")
        print(f"📄 文档 {i+1}")
        print(f"{'='*60}")
        result = pipeline.invoke({"raw_text": doc})
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
```

#### 5.2 LCEL 设计模式总结

| 模式 | 语法 | 使用场景 |
|------|------|----------|
| 串行管道 | `a \| b \| c` | 顺序处理 |
| 并行执行 | `{key1: chain1, key2: chain2}` | 独立任务同时执行 |
| 状态累积 | `RunnablePassthrough.assign(...)` | 多步骤共享状态 |
| 条件路由 | `RunnableBranch(...)` | 根据输入选择不同处理路径 |
| 自定义逻辑 | `RunnableLambda(func)` | 数据转换、业务规则 |
| 透传保留 | `RunnablePassthrough()` | 保留原始输入 |

---

## 🌙 晚自习（19:00 - 21:00）

### 19:00 - 20:00 | 自习与练习

1. 跑通所有 Day 26 示例代码
2. 阅读官方文档 LCEL 章节：https://python.langchain.com/docs/concepts/lcel/
3. 尝试将 Day 25 的 Prompt 工厂改写为 LCEL 链
4. 为文档处理流水线添加「情感分析」步骤

### 20:00 - 21:00 | 答疑与讨论

- LCEL 与 LangGraph 的区别？（提示：LCEL 无状态，LangGraph 有状态图）
- 什么时候用 `RunnableParallel`，什么时候用 `RunnableBranch`？

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | Runnable 完整方法族 | |
| 2 | LCEL 管道符 `\|` 原理 | |
| 3 | RunnableParallel 并行执行 | |
| 4 | 字典语法简写并行 | |
| 5 | RunnablePassthrough 透传与 assign | |
| 6 | RunnableLambda 自定义函数 | |
| 7 | RunnableAssign 状态累积 | |
| 8 | RunnableBranch 条件分支 | |
| 9 | 链的配置 tags/metadata/callbacks | |
| 10 | 多步骤文档处理流水线 | |

---

## 📝 课后作业

### 必做题

1. **文档流水线扩展**：为下午项目添加「标题生成」和「阅读难度评估」两个步骤
2. **条件路由实战**：实现一个智能客服路由链，根据用户意图（咨询/投诉/建议）分流到不同处理链
3. **Git 提交**：`git commit -m "Day 26: LCEL 表达式与链"`

### 选做题

4. 用 `RunnableParallel` 实现「多模型对比」：同一问题同时发给 temperature=0 和 temperature=1 的模型，对比输出
5. 研究 `with_config()` 方法，为链的不同步骤设置不同的 `run_name`

---

## 💡 常见问题 FAQ

**Q1: `RunnableLambda` 和 Python 普通函数有什么区别？**

A: `RunnableLambda` 包装后的函数实现了 Runnable 接口，可以用 `|` 与其他组件组合，并自动支持 invoke/batch/stream 等方法。普通函数不行。

**Q2: 并行链中某个分支失败了怎么办？**

A: 默认会抛出异常中断整个链。可以用 `RunnableLambda` 包裹并 try/except 处理，或使用 LangGraph 的错误恢复机制（Day 39+）。

**Q3: `RunnablePassthrough.assign` 中的 lambda 能访问之前 assign 的字段吗？**

A: 可以。每个 assign 的 lambda 接收的是当前累积的字典状态，包含之前所有 assign 添加的字段。

**Q4: LCEL 链的性能如何？**

A: LCEL 本身开销极小。性能瓶颈在 LLM API 调用。使用 `batch` 和 `RunnableParallel` 可以并行化多个 LLM 调用，显著减少总耗时。

**Q5: 链太长不好调试怎么办？**

A: 
- 使用 `StdOutCallbackHandler` 查看每步输入输出
- 将长链拆分为多个子链，逐步测试
- 使用 LangSmith 可视化追踪（后续课程介绍）

---

## 🔮 明日预习

**Day 27: Memory 记忆机制**

明天你将学习如何让链「记住」对话历史：

- `ConversationBufferMemory` 完整历史
- `ConversationBufferWindowMemory` 滑动窗口
- `ConversationSummaryMemory` 摘要记忆
- `RunnableWithMessageHistory` 为任意链注入记忆
- 实战：带记忆的多轮技术问答助手

**预习建议**：思考 Day 26 的文档流水线如果加入「记住用户上一次查询的主题」，需要怎么改？

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 26*
