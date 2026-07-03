# Day 20: 多模态与嵌入模型

> **培训阶段**: 第二阶段 大模型理论与 API | **第 3 周 | **学习时长**: 约 6-8 小时  
> **今日关键词**: 多模态 API、Embedding、余弦相似度、相似问题匹配

---

## 📍 课程导航

### 上节回顾
**Day 19** 我们完成了 Function Calling 多工具助手：

- Function Calling 完整请求-响应循环
- 工具 Schema 设计规范与注册模式
- 天气 + 计算器 + 时间查询助手项目
- 多工具并行调用与错误处理

今天学习 **多模态** 和 **Embedding**——后者是 Day 25+ RAG 开发的核心基础。

### 本节学习目标
完成本日学习后，你将能够：

1. 调用多模态 API 实现图片理解（Vision）
2. 理解 Embedding 向量的含义与生成方式
3. 使用余弦相似度衡量文本语义相似性
4. 实现相似问题匹配工具（RAG 检索的雏形）
5. 为下周 RAG 开发做好理论和技术铺垫

### 与后续课程的衔接
- **Day 5** 列表/字典 → Embedding 结果是浮点数列表
- **Day 9** 模块与 pip → 今天安装 `numpy` 做向量计算
- **Day 15** Token → Embedding 输入也受 Token 限制
- **Day 25-28** RAG 核心 → 今天的相似度匹配就是 RAG 检索的原型
- **Day 30+** 向量数据库 → 今天用内存列表，后续升级为 Chroma/Milvus

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：多模态 API

#### 1.1 什么是多模态

**多模态（Multimodal）** 指模型能理解和生成多种类型的数据：文本、图片、音频、视频。

```
单模态（Day 12-19）              多模态（今天）
┌─────────────┐                ┌─────────────────────┐
│  文本 → 文本  │                │  文本 + 图片 → 文本   │
│  Prompt → 回答│                │  图片 → 文本描述      │
└─────────────┘                │  文本 → 图片生成      │
                               └─────────────────────┘
```

#### 1.2 图片理解（Vision）

```python
# day20/vision_demo.py
"""多模态：图片理解"""

import os
import base64
import requests

API_KEY = os.getenv("DEEPSEEK_API_KEY")  # 或 OpenAI API Key
URL = "https://api.deepseek.com/v1/chat/completions"  # 根据实际 API 调整


def encode_image(image_path: str) -> str:
    """将图片编码为 base64"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def analyze_image(image_path: str, question: str = "描述这张图片的内容") -> str:
    """分析图片内容"""
    base64_image = encode_image(image_path)

    response = requests.post(URL, json={
        "model": "deepseek-chat",  # 需支持 vision 的模型
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        "max_tokens": 1024,
    }, headers={"Authorization": f"Bearer {API_KEY}"}, timeout=60)

    return response.json()["choices"][0]["message"]["content"]


# 使用示例
# result = analyze_image("photo.jpg", "这张图片里有什么？")
# result = analyze_image("chart.png", "分析这个图表的数据趋势")
# result = analyze_image("code.png", "读取并解释这段代码")
```

#### 1.3 多模态应用场景

| 场景 | 输入 | 输出 | 应用 |
|------|------|------|------|
| 图片描述 | 图片 | 文字描述 | 无障碍、内容审核 |
| OCR | 图片 | 文字 | 文档数字化 |
| 图表分析 | 图表截图 | 数据解读 | 商业分析 |
| 代码截图 | 代码图片 | 代码文本 | 开发辅助 |
| 医疗影像 | X 光片 | 初步诊断 | 医疗 AI（需专业模型） |

#### 1.4 图片生成（了解）

```python
# 图片生成 API 示例（OpenAI DALL-E 风格）
# 注意：DeepSeek 暂不支持图片生成，此处以 OpenAI 为例

def generate_image(prompt: str, size: str = "1024x1024") -> str:
    """根据文字描述生成图片"""
    response = requests.post(
        "https://api.openai.com/v1/images/generations",
        json={
            "model": "dall-e-3",
            "prompt": prompt,
            "size": size,
            "n": 1,
        },
        headers={"Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"},
        timeout=60,
    )
    return response.json()["data"][0]["url"]
```

---

### 9:45 - 10:30 | 模块二：Embedding 详解

#### 2.1 什么是 Embedding

**Embedding（嵌入向量）** 是将文本映射为高维浮点数向量的技术。语义相近的文本，其向量在空间中距离更近。

```
"猫是一种可爱的宠物"  →  [0.12, -0.34, 0.56, ..., 0.78]   (1536 维)
"狗是人类的好朋友"    →  [0.15, -0.31, 0.52, ..., 0.75]   (相近方向)
"今天股市大涨"       →  [-0.45, 0.67, -0.12, ..., 0.23]  (远距离)
```

#### 2.2 为什么需要 Embedding

| 传统方法 | Embedding 方法 |
|----------|---------------|
| 关键词匹配 | 语义匹配 |
| 「汽车」≠「轿车」 | 「汽车」≈「轿车」 |
| 无法处理同义词 | 自动理解语义 |
| 精确匹配才命中 | 模糊匹配也能找到 |

**核心应用：RAG 检索**（Day 25+）

```
用户问题 → Embedding → 向量
                          ↓ 余弦相似度
知识库文档 → Embedding → 向量  →  找到最相关的文档 → 注入 Prompt
```

#### 2.3 调用 Embedding API

```python
# day20/embedding_demo.py
"""Embedding API 调用"""

import os
import requests

API_KEY = os.getenv("DEEPSEEK_API_KEY")
# DeepSeek Embedding 端点（以实际文档为准）
EMBED_URL = "https://api.deepseek.com/v1/embeddings"


def get_embedding(text: str, model: str = "deepseek-embedding") -> list[float]:
    """获取文本的 Embedding 向量"""
    response = requests.post(EMBED_URL, json={
        "model": model,
        "input": text,
    }, headers={"Authorization": f"Bearer {API_KEY}"}, timeout=30)

    data = response.json()
    return data["data"][0]["embedding"]


def get_embeddings_batch(texts: list[str], model: str = "deepseek-embedding") -> list[list[float]]:
    """批量获取 Embedding"""
    response = requests.post(EMBED_URL, json={
        "model": model,
        "input": texts,
    }, headers={"Authorization": f"Bearer {API_KEY}"}, timeout=30)

    data = response.json()
    # 按 index 排序确保顺序
    sorted_data = sorted(data["data"], key=lambda x: x["index"])
    return [item["embedding"] for item in sorted_data]


# 使用
if __name__ == "__main__":
    vec = get_embedding("大模型应用开发")
    print(f"向量维度: {len(vec)}")
    print(f"前 5 个值: {vec[:5]}")
```

#### 2.4 Embedding 模型选择

| 模型 | 维度 | 特点 | 适用 |
|------|------|------|------|
| text-embedding-3-small | 1536 | OpenAI，性价比高 | 英文为主 |
| text-embedding-3-large | 3072 | OpenAI，精度高 | 高精度需求 |
| deepseek-embedding | — | 国产，便宜 | 中文场景 |
| bge-large-zh | 1024 | 开源，中文优秀 | 本地部署 |

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：余弦相似度

#### 3.1 相似度度量

两个向量有多「像」，用相似度度量：

| 度量 | 公式 | 特点 |
|------|------|------|
| 余弦相似度 | cos(θ) = A·B / (\|A\|×\|B\|) | 只看方向，不看长度（最常用） |
| 欧氏距离 | \|A - B\| | 看绝对距离 |
| 点积 | A · B | 受向量长度影响 |

**余弦相似度**：值域 [-1, 1]，越接近 1 越相似。

```
cos(θ) = 1.0   → 完全相同方向（语义相同）
cos(θ) = 0.0   → 正交（无关）
cos(θ) = -1.0  → 完全相反
```

#### 3.2 NumPy 实现

```bash
pip install numpy -i https://pypi.tuna.tsinghua.edu.cn/simple
```

```python
# day20/similarity.py
"""余弦相似度计算"""

import numpy as np


def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """计算两个向量的余弦相似度"""
    a = np.array(vec_a)
    b = np.array(vec_b)
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(dot_product / (norm_a * norm_b))


def cosine_similarity_batch(query_vec: list[float], doc_vecs: list[list[float]]) -> list[float]:
    """计算一个查询向量与多个文档向量的相似度"""
    q = np.array(query_vec)
    docs = np.array(doc_vecs)
    dot_products = docs @ q
    norms = np.linalg.norm(docs, axis=1) * np.linalg.norm(q)
    return (dot_products / norms).tolist()


# 验证
if __name__ == "__main__":
    # 简单测试
    a = [1, 0, 0]
    b = [1, 0, 0]
    c = [0, 1, 0]
    print(f"相同向量: {cosine_similarity(a, b):.4f}")  # 1.0
    print(f"正交向量: {cosine_similarity(a, c):.4f}")  # 0.0
```

#### 3.3 语义相似度实验

```python
# day20/semantic_test.py
"""语义相似度实验"""

from embedding_demo import get_embedding
from similarity import cosine_similarity


def compare_texts(text_a: str, text_b: str) -> float:
    vec_a = get_embedding(text_a)
    vec_b = get_embedding(text_b)
    return cosine_similarity(vec_a, vec_b)


# 实验
pairs = [
    ("猫是一种可爱的宠物", "狗是人类最好的朋友"),
    ("猫是一种可爱的宠物", "猫咪很可爱"),
    ("猫是一种可爱的宠物", "今天股市大涨"),
    ("如何学习 Python", "Python 入门教程"),
    ("如何学习 Python", "怎么做红烧肉"),
]

for a, b in pairs:
    score = compare_texts(a, b)
    print(f"相似度 {score:.4f} | 「{a}」 vs 「{b}」")
```

**期望结果**

```
相似度 0.75+ | 「猫是一种可爱的宠物」 vs 「狗是人类最好的朋友」
相似度 0.85+ | 「猫是一种可爱的宠物」 vs 「猫咪很可爱」
相似度 0.20- | 「猫是一种可爱的宠物」 vs 「今天股市大涨」
相似度 0.80+ | 「如何学习 Python」 vs 「Python 入门教程」
相似度 0.20- | 「如何学习 Python」 vs 「怎么做红烧肉」
```

---

## 🌆 下午课程（14:00 - 17:00）

### 14:00 - 17:00 | 模块四：相似问题匹配工具

#### 4.1 项目目标

构建一个 **FAQ 相似问题匹配工具**：

```
用户输入：「怎么装 Python？」
  ↓ Embedding
  ↓ 与 FAQ 库中所有问题计算相似度
  ↓ 返回最相似的问题及答案

匹配到：「如何安装 Python 环境？」（相似度 0.92）
答案：请访问 python.org 下载...
```

这就是 **RAG 检索** 的简化版：没有大模型生成，只有向量检索。

#### 4.2 FAQ 知识库

```python
# day20/faq_data.py
"""FAQ 知识库"""

FAQ_DATA = [
    {
        "question": "如何安装 Python 环境？",
        "answer": "访问 https://www.python.org/downloads/ 下载 Python 3.10+，安装时勾选 Add to PATH。",
    },
    {
        "question": "怎么调用大模型 API？",
        "answer": "使用 requests 库发送 POST 请求到 API 端点，在 Header 中携带 API Key，Body 中包含 model 和 messages 参数。",
    },
    {
        "question": "什么是 Prompt 工程？",
        "answer": "Prompt 工程是通过设计和优化输入文本，引导大模型产生期望输出的技术。包括角色设定、任务描述、格式约束等。",
    },
    {
        "question": "如何学习大模型应用开发？",
        "answer": "建议路径：Python 基础 → API 调用 → Prompt 工程 → RAG 开发 → Agent 开发 → 微调部署。",
    },
    {
        "question": "temperature 参数有什么作用？",
        "answer": "temperature 控制输出的随机性。值越低输出越确定（适合代码生成），值越高越有创造性（适合写作）。",
    },
    {
        "question": "什么是 RAG？",
        "answer": "RAG（Retrieval-Augmented Generation）检索增强生成，通过检索外部知识库来增强大模型的回答能力，解决知识截止和幻觉问题。",
    },
    {
        "question": "如何部署大模型应用？",
        "answer": "常见方案：FastAPI 后端 + 前端 UI，Docker 容器化，部署到云服务器。Day 55-56 会详细学习。",
    },
    {
        "question": "Embedding 和 Fine-tuning 有什么区别？",
        "answer": "Embedding 是将文本转为向量用于检索，不改变模型。Fine-tuning 是调整模型参数以适应特定任务。",
    },
]
```

#### 4.3 相似问题匹配器

```python
# day20/faq_matcher.py
"""FAQ 相似问题匹配工具"""

import json
import numpy as np
from pathlib import Path
from embedding_demo import get_embedding, get_embeddings_batch
from similarity import cosine_similarity


class FAQMatcher:
    def __init__(self, faq_data: list[dict], cache_path: str = "day20/faq_vectors.json"):
        self.faq_data = faq_data
        self.cache_path = Path(cache_path)
        self.questions = [item["question"] for item in faq_data]
        self.vectors = None
        self._load_or_build_vectors()

    def _load_or_build_vectors(self):
        """加载缓存或重新计算向量"""
        if self.cache_path.exists():
            with open(self.cache_path, encoding="utf-8") as f:
                cache = json.load(f)
            if cache.get("questions") == self.questions:
                self.vectors = cache["vectors"]
                print(f"从缓存加载 {len(self.vectors)} 个向量")
                return

        print("正在计算 FAQ 向量（首次运行较慢）...")
        self.vectors = get_embeddings_batch(self.questions)
        self._save_cache()

    def _save_cache(self):
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.cache_path, "w", encoding="utf-8") as f:
            json.dump({"questions": self.questions, "vectors": self.vectors}, f)

    def search(self, query: str, top_k: int = 3, threshold: float = 0.5) -> list[dict]:
        """搜索最相似的 FAQ"""
        query_vec = get_embedding(query)
        scores = []
        for i, vec in enumerate(self.vectors):
            score = cosine_similarity(query_vec, vec)
            scores.append((score, i))

        scores.sort(reverse=True)
        results = []
        for score, idx in scores[:top_k]:
            if score < threshold:
                break
            results.append({
                "question": self.faq_data[idx]["question"],
                "answer": self.faq_data[idx]["answer"],
                "score": round(score, 4),
            })
        return results

    def answer(self, query: str) -> str:
        """返回最佳匹配的答案"""
        results = self.search(query, top_k=1)
        if not results:
            return "抱歉，没有找到相关问题的答案。请尝试换一种方式提问。"
        best = results[0]
        return f"匹配问题：{best['question']}（相似度 {best['score']}）\n\n{best['answer']}"
```

#### 4.4 交互式 FAQ 机器人

```python
# day20/faq_bot.py
"""FAQ 智能机器人"""

from faq_data import FAQ_DATA
from faq_matcher import FAQMatcher


def main():
    matcher = FAQMatcher(FAQ_DATA)
    print("=" * 50)
    print("  FAQ 智能问答（基于 Embedding 相似度匹配）")
    print("  输入 quit 退出")
    print("=" * 50)

    while True:
        query = input("\n你的问题: ").strip()
        if query.lower() in ("quit", "exit", "q"):
            break
        if not query:
            continue

        results = matcher.search(query, top_k=3)
        if not results:
            print("未找到相关问题。")
            continue

        print(f"\n找到 {len(results)} 个相关问题：")
        for i, r in enumerate(results, 1):
            print(f"\n--- 匹配 {i}（相似度 {r['score']}）---")
            print(f"Q: {r['question']}")
            print(f"A: {r['answer']}")


if __name__ == "__main__":
    main()
```

#### 4.5 升级为 RAG 预览

```python
# day20/mini_rag.py
"""迷你 RAG：检索 + 大模型生成"""

import os
import requests
from faq_data import FAQ_DATA
from faq_matcher import FAQMatcher

API_KEY = os.getenv("DEEPSEEK_API_KEY")
URL = "https://api.deepseek.com/v1/chat/completions"


class MiniRAG:
    def __init__(self):
        self.matcher = FAQMatcher(FAQ_DATA)

    def ask(self, question: str) -> str:
        # 第一步：检索相关 FAQ
        results = self.matcher.search(question, top_k=2, threshold=0.3)
        if not results:
            context = "知识库中没有相关信息。"
        else:
            context = "\n\n".join(
                f"Q: {r['question']}\nA: {r['answer']}" for r in results
            )

        # 第二步：将检索结果注入 Prompt，让大模型生成回答
        prompt = f"""基于以下参考资料回答用户问题。如果资料中没有相关信息，请诚实说明。

## 参考资料
{context}

## 用户问题
{question}

请给出准确、有帮助的回答。"""

        resp = requests.post(URL, json={
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
        }, headers={"Authorization": f"Bearer {API_KEY}"}, timeout=60)

        return resp.json()["choices"][0]["message"]["content"]


if __name__ == "__main__":
    rag = MiniRAG()
    print(rag.ask("怎么装 Python？"))
    print("---")
    print(rag.ask("RAG 是什么？有什么好处？"))
```

> 💡 **这就是 RAG 的核心流程**：检索（Retrieval）+ 增强（Augmented）+ 生成（Generation）。Day 25 将用向量数据库和专业文档处理升级这个原型。

---

## 🌙 晚自习（19:00 - 21:00）

### 19:00 - 20:00 | 知识串联

#### 从 Embedding 到 RAG 的演进

```
Day 20（今天）          Day 25-28（RAG）           Day 30+（生产级）
┌──────────────┐       ┌──────────────────┐       ┌──────────────────┐
│ 内存 FAQ 列表  │  →    │ 向量数据库 Chroma  │  →    │ Milvus/Pinecone   │
│ 手动算相似度   │       │ 文档分块+批量索引   │       │ 分布式+持久化      │
│ 单文件缓存    │       │ LangChain 集成     │       │ 混合检索+重排序    │
└──────────────┘       └──────────────────┘       └──────────────────┘
```

### 20:00 - 21:00 | 自习答疑

- 完成 FAQ 匹配工具并测试 10 个问题
- 运行 mini_rag.py，体验检索+生成
- 预习 Day 21 周测

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | 多模态概念与应用场景 | |
| 2 | 图片理解 Vision API 调用 | |
| 3 | Embedding 向量表示原理 | |
| 4 | Embedding API 调用（单个/批量） | |
| 5 | 余弦相似度计算（NumPy） | |
| 6 | 语义相似度 vs 关键词匹配 | |
| 7 | FAQ 相似问题匹配器实现 | |
| 8 | 向量缓存策略 | |
| 9 | 迷你 RAG 检索+生成流程 | |
| 10 | 从 Embedding 到 RAG 的技术演进 | |

---

## 📝 课后作业

### 必做题

1. **FAQ 匹配器**：完成 `faq_matcher.py`，测试至少 10 个不同问法
2. **相似度实验**：找 5 组文本对，记录相似度分数，分析是否符合直觉
3. **迷你 RAG**：运行 `mini_rag.py`，对比纯检索和 RAG 的回答差异

### 选做题

4. 扩展 FAQ 库到 20 条，覆盖 Day 15-19 的知识点
5. 实现混合检索：Embedding 相似度 + 关键词匹配加权
6. 尝试用开源模型 `bge-large-zh` 本地生成 Embedding

---

## 💡 常见问题 FAQ

**Q1: Embedding 向量维度越高越好吗？**

A: 不一定。更高维度能捕获更细语义，但计算和存储成本更高。1536 维对大多数应用足够。

**Q2: 余弦相似度多少算「相似」？**

A: 经验值：> 0.8 非常相似，0.6-0.8 相关，< 0.5 不相关。具体阈值需根据业务数据调优。

**Q3: 每次查询都要调用 Embedding API 吗？**

A: 知识库向量化只需一次（可缓存）。每次用户查询需要一次 Embedding API 调用。Day 25+ 会学批量优化。

**Q4: FAQ 匹配和 RAG 有什么区别？**

A: FAQ 匹配是「找最相似的问题，返回预设答案」。RAG 是「检索相关文档片段，让大模型基于片段生成新答案」。RAG 更灵活但成本更高。

**Q5: 图片理解 API 一定需要 GPT-4V 吗？**

A: 不是。Qwen-VL、GLM-4V 等国产模型也支持。选择取决于预算和精度要求。

---

## 🔮 明日预习

**Day 21: 周测与综合练习**

明天是第 3 周总结：

- 本周知识周测（理论 + 实操）
- **综合项目**：多轮对话 + 工具调用 + 流式输出整合
- 第二阶段中期复盘

**预习建议**：回顾 Day 15-20 的知识清单，准备好 API Key 和环境。

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 20*
