# Day 28: 文档加载与分割

> **培训阶段**: 第三阶段 RAG 应用开发 | **第 5 周 | **学习时长**: 约 6-8 小时  
> **今日关键词**: Document Loaders、Text Splitters、chunk_size、chunk_overlap、元数据

---

## 📍 课程导航

### 上节回顾

**Day 27** 你掌握了 LangChain Memory 记忆机制：
- `ConversationBufferMemory` / `WindowMemory` / `SummaryMemory`
- `RunnableWithMessageHistory` 为链注入记忆
- Memory + RAG 组合预览

今天进入 RAG 的 **数据工程** 环节。俗话说「Garbage In, Garbage Out」——文档加载与分割的质量直接决定 RAG 系统的上限。

### 本节学习目标

完成本日学习后，你将能够：

1. 使用多种 Document Loader 加载不同格式文档
2. 理解 `Document` 对象的结构（`page_content` + `metadata`）
3. 掌握 `RecursiveCharacterTextSplitter` 递归分割策略
4. 合理设置 `chunk_size` 和 `chunk_overlap` 参数
5. 使用 `TokenTextSplitter` 按 token 数分割
6. 为分割后的 chunks 添加和增强元数据
7. 完成企业 PDF 文档的加载、分割与质量检查

### 与后续课程的衔接

- **Day 29** 将分割后的 chunks **嵌入向量**并存入 Chroma / Milvus
- **Day 30** 用今天处理的文档构建完整 RAG 流水线
- **Day 33** 父文档检索（Parent Document Retriever）依赖今天的分割策略

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：Document 对象与加载器

#### 1.1 Document 数据结构

LangChain 中所有文档都统一为 `Document` 对象：

```python
from langchain_core.documents import Document

doc = Document(
    page_content="LangChain 是一个 LLM 应用开发框架。",
    metadata={
        "source": "intro.txt",
        "page": 1,
        "author": "LangChain Team",
    },
)

print(f"内容: {doc.page_content}")
print(f"元数据: {doc.metadata}")
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `page_content` | str | 文档正文 |
| `metadata` | dict | 来源、页码、作者等元信息 |

#### 1.2 常用 Document Loaders

```python
# day28/01_document_loaders.py
"""常用文档加载器"""
import os

# ===== TextLoader：纯文本 =====
from langchain_community.document_loaders import TextLoader

with open("sample.txt", "w", encoding="utf-8") as f:
    f.write("LangChain 支持多种文档格式。\nRAG 需要先将文档加载再分割。")

loader = TextLoader("sample.txt", encoding="utf-8")
docs = loader.load()
print(f"TextLoader: {len(docs)} 个文档, 内容长度 {len(docs[0].page_content)}")

# ===== PyPDFLoader：PDF 文件 =====
from langchain_community.document_loaders import PyPDFLoader

# 创建测试 PDF（如果没有真实 PDF）
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    c = canvas.Canvas("sample.pdf", pagesize=A4)
    c.drawString(100, 750, "RAG 技术白皮书")
    c.drawString(100, 730, "第一章：检索增强生成概述")
    c.drawString(100, 710, "RAG 通过检索外部知识库来增强大模型的回答能力。")
    c.showPage()
    c.drawString(100, 750, "第二章：文档处理")
    c.drawString(100, 730, "文档加载和分割是 RAG 数据工程的基础环节。")
    c.save()
except ImportError:
    print("未安装 reportlab，跳过 PDF 创建")

if os.path.exists("sample.pdf"):
    pdf_loader = PyPDFLoader("sample.pdf")
    pdf_docs = pdf_loader.load()
    print(f"\nPyPDFLoader: {len(pdf_docs)} 页")
    for doc in pdf_docs:
        print(f"  第 {doc.metadata.get('page', '?')} 页: {doc.page_content[:50]}...")

# ===== CSVLoader：CSV 文件 =====
from langchain_community.document_loaders import CSVLoader

with open("faq.csv", "w", encoding="utf-8") as f:
    f.write("question,answer\n")
    f.write("什么是RAG,检索增强生成技术\n")
    f.write("什么是向量数据库,存储和检索向量的数据库\n")

csv_loader = CSVLoader("faq.csv", encoding="utf-8")
csv_docs = csv_loader.load()
print(f"\nCSVLoader: {len(csv_docs)} 行")
for doc in csv_docs:
    print(f"  {doc.page_content[:60]}")

# ===== DirectoryLoader：批量加载目录 =====
from langchain_community.document_loaders import DirectoryLoader

os.makedirs("docs_dir", exist_ok=True)
with open("docs_dir/doc1.txt", "w") as f:
    f.write("文档一的内容")
with open("docs_dir/doc2.txt", "w") as f:
    f.write("文档二的内容")

dir_loader = DirectoryLoader("docs_dir", glob="**/*.txt", loader_cls=TextLoader,
                              loader_kwargs={"encoding": "utf-8"})
dir_docs = dir_loader.load()
print(f"\nDirectoryLoader: {len(dir_docs)} 个文件")
```

**Loader 选择指南**

| 格式 | Loader | 安装依赖 |
|------|--------|----------|
| `.txt` `.md` | `TextLoader` | 无 |
| `.pdf` | `PyPDFLoader` | `pypdf` |
| `.docx` | `Docx2txtLoader` | `docx2txt` |
| `.csv` | `CSVLoader` | 无 |
| 网页 | `WebBaseLoader` | `beautifulsoup4` |
| Markdown | `UnstructuredMarkdownLoader` | `unstructured` |
| 目录批量 | `DirectoryLoader` | 取决于文件类型 |

#### 1.3 异步加载与懒加载

```python
# day28/02_lazy_loading.py
"""懒加载：处理大文件"""
from langchain_community.document_loaders import TextLoader

# 普通加载：一次性读入内存
docs = TextLoader("sample.txt", encoding="utf-8").load()

# 懒加载：逐文档迭代，节省内存
loader = TextLoader("sample.txt", encoding="utf-8")
for doc in loader.lazy_load():
    print(f"懒加载: {doc.page_content[:30]}...")
```

---

### 9:45 - 10:30 | 模块二：Text Splitters 文本分割

#### 2.1 为什么需要分割？

```
原始文档（10000 字）
    ↓ 分割
Chunk 1（500字） + Chunk 2（500字） + ... + Chunk N
    ↓ 嵌入
Vector 1 + Vector 2 + ... + Vector N
    ↓ 检索
用户问题 → 最相关的 Chunk → 送入 LLM 生成回答
```

**不分割的问题**：
- 超过 Embedding 模型的最大输入长度
- 检索粒度太粗，返回大段不相关内容
- 浪费 token（只需一小段相关信息）

#### 2.2 RecursiveCharacterTextSplitter

最常用的分割器，按优先级尝试不同分隔符：

```python
# day28/03_recursive_splitter.py
"""RecursiveCharacterTextSplitter 详解"""
from langchain_text_splitters import RecursiveCharacterTextSplitter

text = """
# RAG 技术指南

## 第一章：概述
检索增强生成（RAG）是一种结合信息检索与文本生成的技术。
它通过从外部知识库检索相关文档，为大模型提供上下文。

## 第二章：架构
RAG 系统通常包含以下组件：
1. 文档加载器（Document Loader）
2. 文本分割器（Text Splitter）
3. 嵌入模型（Embedding Model）
4. 向量数据库（Vector Store）
5. 检索器（Retriever）
6. 大语言模型（LLM）

## 第三章：最佳实践
- 选择合适的 chunk_size（通常 300-1000 字符）
- 设置 chunk_overlap 避免语义断裂（通常 10%-20%）
- 为 chunks 添加元数据便于过滤和溯源
"""

splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,        # 每个 chunk 最大字符数
    chunk_overlap=50,      # 相邻 chunk 重叠字符数
    length_function=len,   # 计算长度的函数
    separators=["\n\n", "\n", "。", "，", " ", ""],  # 分隔符优先级
)

chunks = splitter.split_text(text)
print(f"分割为 {len(chunks)} 个 chunks\n")
for i, chunk in enumerate(chunks):
    print(f"--- Chunk {i+1} ({len(chunk)} 字) ---")
    print(chunk.strip())
    print()
```

**分割过程示意**：

```
原文: "第一章内容...\n\n第二章内容...\n\n第三章内容..."
         ↓ 尝试 \n\n 分割
["第一章内容...", "第二章内容...", "第三章内容..."]
         ↓ 某段仍 > chunk_size，尝试 \n 分割
         ↓ 继续细分直到每段 <= chunk_size
最终 chunks（相邻之间有 overlap 重叠）
```

#### 2.3 chunk_size 与 chunk_overlap 参数选择

| 参数 | 推荐范围 | 影响 |
|------|----------|------|
| `chunk_size` | 300-1000 字符 | 太小=上下文不足；太大=检索不精确 |
| `chunk_overlap` | 10%-20% of chunk_size | 太小=语义断裂；太大=冗余存储 |

```python
# day28/04_chunk_params.py
"""不同参数对比实验"""
from langchain_text_splitters import RecursiveCharacterTextSplitter

sample_text = "RAG 技术" * 200  # 约 1200 字符

configs = [
    {"chunk_size": 100, "chunk_overlap": 0},
    {"chunk_size": 200, "chunk_overlap": 40},
    {"chunk_size": 500, "chunk_overlap": 100},
]

for cfg in configs:
    splitter = RecursiveCharacterTextSplitter(**cfg)
    chunks = splitter.split_text(sample_text)
    print(f"size={cfg['chunk_size']}, overlap={cfg['chunk_overlap']} "
          f"→ {len(chunks)} chunks, 平均长度 {sum(len(c) for c in chunks)//len(chunks)}")
```

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：高级分割策略

#### 3.1 分割 Document 对象（保留元数据）

```python
# day28/05_split_documents.py
"""分割 Document 对象并保留元数据"""
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = TextLoader("sample.txt", encoding="utf-8")
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
)

# split_documents 会为每个 chunk 继承原文档的 metadata
chunks = splitter.split_documents(documents)

print(f"原始文档: {len(documents)} 个")
print(f"分割后: {len(chunks)} 个 chunks")
for i, chunk in enumerate(chunks):
    print(f"  Chunk {i+1}: source={chunk.metadata.get('source')}, "
          f"长度={len(chunk.page_content)}")
```

#### 3.2 TokenTextSplitter

按 token 数分割，与 Embedding 模型的 token 限制对齐：

```python
# day28/06_token_splitter.py
"""TokenTextSplitter 按 token 分割"""
from langchain_text_splitters import TokenTextSplitter

text = "LangChain 是一个强大的 LLM 应用开发框架。" * 50

token_splitter = TokenTextSplitter(
    chunk_size=50,       # 每个 chunk 最大 50 tokens
    chunk_overlap=10,    # 重叠 10 tokens
)

chunks = token_splitter.split_text(text)
print(f"Token 分割: {len(chunks)} 个 chunks")
for i, chunk in enumerate(chunks[:3]):
    print(f"  Chunk {i+1}: {chunk[:60]}...")
```

#### 3.3 Markdown 与代码专用分割器

```python
# day28/07_specialized_splitters.py
"""专用分割器"""
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    Language,
    RecursiveCharacterTextSplitter,
)

# Markdown 按标题分割
md_text = """# 主标题
## 第一节
第一节的内容。
## 第二节
第二节的内容。
### 子节
子节的内容。
"""

md_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[
        ("#", "h1"),
        ("##", "h2"),
        ("###", "h3"),
    ]
)
md_chunks = md_splitter.split_text(md_text)
print("=== Markdown 分割 ===")
for chunk in md_chunks:
    print(f"  标题: {chunk.metadata}, 内容: {chunk.page_content[:40]}...")

# 代码按语法分割
python_code = '''
def hello():
  print("Hello")

class MyClass:
  def method(self):
    pass
'''

code_splitter = RecursiveCharacterTextSplitter.from_language(
    Language.PYTHON, chunk_size=100, chunk_overlap=10
)
code_chunks = code_splitter.split_text(python_code)
print(f"\n=== 代码分割: {len(code_chunks)} chunks ===")
```

#### 3.4 元数据增强

```python
# day28/08_metadata_enrichment.py
"""为 chunks 增强元数据"""
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

documents = [
    Document(page_content="产品A的功能介绍..." * 10, metadata={"source": "product_a.pdf", "page": 1}),
    Document(page_content="产品B的功能介绍..." * 10, metadata={"source": "product_b.pdf", "page": 1}),
]

splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
chunks = splitter.split_documents(documents)

# 增强元数据
for i, chunk in enumerate(chunks):
    chunk.metadata["chunk_id"] = i
    chunk.metadata["chunk_size"] = len(chunk.page_content)
    chunk.metadata["total_chunks"] = len(chunks)

print(f"增强后元数据示例: {chunks[0].metadata}")
```

---

## 🌆 下午课程（14:00 - 17:00）

### 14:00 - 15:30 | 模块四：文档处理最佳实践

#### 4.1 分割质量检查

```python
# day28/09_quality_check.py
"""分割质量检查工具"""
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def check_split_quality(chunks: list[Document], chunk_size: int) -> dict:
    """检查分割质量"""
    sizes = [len(c.page_content) for c in chunks]
    report = {
        "total_chunks": len(chunks),
        "avg_size": sum(sizes) / len(sizes) if sizes else 0,
        "min_size": min(sizes) if sizes else 0,
        "max_size": max(sizes) if sizes else 0,
        "oversized": sum(1 for s in sizes if s > chunk_size),
        "undersized": sum(1 for s in sizes if s < chunk_size * 0.3),
        "empty_metadata": sum(1 for c in chunks if not c.metadata),
    }
    return report


def print_quality_report(report: dict):
    print("=== 分割质量报告 ===")
    print(f"  总 chunks 数: {report['total_chunks']}")
    print(f"  平均长度: {report['avg_size']:.0f} 字符")
    print(f"  最小/最大: {report['min_size']} / {report['max_size']}")
    print(f"  超大 chunks: {report['oversized']}")
    print(f"  过小 chunks: {report['undersized']}")
    if report['oversized'] > 0:
        print("  ⚠️ 存在超大 chunk，考虑减小 chunk_size")
    if report['undersized'] > report['total_chunks'] * 0.2:
        print("  ⚠️ 过多过小 chunk，考虑增大 chunk_size 或检查分隔符")


# 测试
text = "这是测试文档。" * 100
splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=40)
chunks = splitter.create_documents([text], metadatas=[{"source": "test.txt"}])
report = check_split_quality(chunks, 200)
print_quality_report(report)
```

#### 4.2 完整文档处理流水线

```python
# day28/10_document_pipeline.py
"""完整文档处理流水线：加载 → 清洗 → 分割 → 质检"""
import os
import re
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def clean_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)
    return text


def process_documents(
    directory: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100,
) -> list[Document]:
    # 1. 加载
    loader = DirectoryLoader(
        directory, glob="**/*.{txt,md}",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True,
    )
    raw_docs = loader.load()
    print(f"📂 加载了 {len(raw_docs)} 个文档")

    # 2. 清洗
    for doc in raw_docs:
        doc.page_content = clean_text(doc.page_content)

    # 3. 过滤空文档
    raw_docs = [d for d in raw_docs if len(d.page_content) > 10]
    print(f"🧹 清洗后剩余 {len(raw_docs)} 个有效文档")

    # 4. 分割
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", "。", "！", "？", "；", " ", ""],
    )
    chunks = splitter.split_documents(raw_docs)
    print(f"✂️ 分割为 {len(chunks)} 个 chunks")

    # 5. 增强元数据
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_index"] = i
        chunk.metadata["char_count"] = len(chunk.page_content)

    return chunks


# 使用
os.makedirs("knowledge_base", exist_ok=True)
with open("knowledge_base/policy.txt", "w", encoding="utf-8") as f:
    f.write("公司考勤制度：上班时间 9:00-18:00，迟到 15 分钟内扣 50 元。\n" * 5)
    f.write("年假制度：入职满一年 10 天，满三年 15 天。\n" * 5)

chunks = process_documents("knowledge_base", chunk_size=200, chunk_overlap=50)
for c in chunks[:3]:
    print(f"\n[{c.metadata['source']}] chunk {c.metadata['chunk_index']}")
    print(f"  {c.page_content[:80]}...")
```

---

### 15:30 - 15:45 | 课间休息

---

### 15:45 - 17:00 | 模块五：下午实操——企业文档处理

```python
# day28/11_enterprise_doc_processing.py
"""下午实操：企业文档批量处理系统"""
import os
import json
from dataclasses import dataclass
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


@dataclass
class ProcessingConfig:
    chunk_size: int = 500
    chunk_overlap: int = 100
    min_chunk_size: int = 50
    output_dir: str = "processed_chunks"


class EnterpriseDocProcessor:
  def __init__(self, config: ProcessingConfig):
      self.config = config
      self.splitter = RecursiveCharacterTextSplitter(
          chunk_size=config.chunk_size,
          chunk_overlap=config.chunk_overlap,
          separators=["\n\n", "\n", "。", "！", "？", " ", ""],
      )
      os.makedirs(config.output_dir, exist_ok=True)

  def load_file(self, file_path: str) -> list[Document]:
      ext = os.path.splitext(file_path)[1].lower()
      loaders = {
          ".txt": lambda: TextLoader(file_path, encoding="utf-8"),
          ".md": lambda: TextLoader(file_path, encoding="utf-8"),
          ".pdf": lambda: PyPDFLoader(file_path),
          ".csv": lambda: CSVLoader(file_path, encoding="utf-8"),
      }
      if ext not in loaders:
          raise ValueError(f"不支持的格式: {ext}")
      return loaders[ext]().load()

  def process_file(self, file_path: str) -> list[Document]:
      docs = self.load_file(file_path)
      chunks = self.splitter.split_documents(docs)
      chunks = [c for c in chunks if len(c.page_content) >= self.config.min_chunk_size]

      for i, chunk in enumerate(chunks):
          chunk.metadata.update({
              "chunk_id": f"{os.path.basename(file_path)}_{i}",
              "file_name": os.path.basename(file_path),
              "chunk_index": i,
          })
      return chunks

  def process_directory(self, directory: str) -> list[Document]:
      all_chunks = []
      for root, _, files in os.walk(directory):
          for file in files:
              if file.startswith("."):
                  continue
              file_path = os.path.join(root, file)
              try:
                  chunks = self.process_file(file_path)
                  all_chunks.extend(chunks)
                  print(f"✅ {file}: {len(chunks)} chunks")
              except Exception as e:
                  print(f"❌ {file}: {e}")
      return all_chunks

  def export_chunks(self, chunks: list[Document], filename: str = "chunks.json"):
      output = [
          {"content": c.page_content, "metadata": c.metadata}
          for c in chunks
      ]
      path = os.path.join(self.config.output_dir, filename)
      with open(path, "w", encoding="utf-8") as f:
          json.dump(output, f, ensure_ascii=False, indent=2)
      print(f"📦 导出 {len(chunks)} 个 chunks 到 {path}")


def main():
    os.makedirs("enterprise_docs", exist_ok=True)
    with open("enterprise_docs/员工手册.txt", "w", encoding="utf-8") as f:
        f.write("员工手册\n\n第一章 入职流程\n新员工需在入职第一天完成以下事项...\n" * 3)
        f.write("\n\n第二章 考勤制度\n标准工时 9:00-18:00...\n" * 3)

    processor = EnterpriseDocProcessor(ProcessingConfig(chunk_size=300, chunk_overlap=60))
    chunks = processor.process_directory("enterprise_docs")
    processor.export_chunks(chunks)
    print(f"\n总计处理: {len(chunks)} 个 chunks")


if __name__ == "__main__":
    main()
```

---

## 🌙 晚自习（19:00 - 21:00）

### 19:00 - 20:00 | 自习与练习

1. 准备 2-3 个真实 PDF 文档，用下午项目处理
2. 实验不同 `chunk_size`（200/500/1000）对分割结果的影响
3. 阅读 LangChain 文档分割章节

### 20:00 - 21:00 | 答疑与讨论

- 中文文档的分隔符应该如何设置？
- 表格、图片丰富的 PDF 如何处理？（提示：后续学 Unstructured）

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | Document 对象结构 | |
| 2 | TextLoader / PyPDFLoader / CSVLoader | |
| 3 | DirectoryLoader 批量加载 | |
| 4 | RecursiveCharacterTextSplitter | |
| 5 | chunk_size 与 chunk_overlap 选择 | |
| 6 | TokenTextSplitter | |
| 7 | Markdown / 代码专用分割器 | |
| 8 | 元数据增强 | |
| 9 | 分割质量检查 | |
| 10 | 企业文档批量处理系统 | |

---

## 📝 课后作业

### 必做题

1. **处理真实文档**：用 3 个以上真实文件（含 PDF）完成加载、分割、导出
2. **参数实验报告**：对比 chunk_size=200/500/800 的分割效果，写简短报告
3. **Git 提交**：`git commit -m "Day 28: 文档加载与分割"`

### 选做题

4. 实现 `WebBaseLoader` 加载网页内容并分割
5. 为分割系统添加「重复 chunk 检测与去重」功能

---

## 💡 常见问题 FAQ

**Q1: PyPDFLoader 提取的中文 PDF 乱码怎么办？**

A: 尝试 `PyMuPDFLoader`（`pip install pymupdf`），对中文 PDF 支持更好。或使用 `UnstructuredPDFLoader`。

**Q2: chunk_size 设多少最合适？**

A: 没有万能答案，取决于：
- Embedding 模型最大输入（通常 512 tokens ≈ 300-400 中文字）
- 文档类型（技术文档偏大 500-800，FAQ 偏小 200-400）
- 建议从 500 开始，通过 Ragas 评估调优（Day 34）

**Q3: 分割后 chunk 太多怎么办？**

A: 增大 `chunk_size`、减少源文档冗余、合并过短的 chunks。

**Q4: 如何处理 PDF 中的表格？**

A: 基础 `PyPDFLoader` 会丢失表格结构。进阶方案：
- `UnstructuredPDFLoader` 保留布局
- 表格转 Markdown 再分割
- 使用专门的表格解析工具（如 `tabula-py`）

**Q5: metadata 有什么用？**

A: 检索后展示来源（「引用自员工手册第 3 页」）、按部门/日期过滤、父文档检索（Day 33）。

---

## 🔮 明日预习

**Day 29: 向量数据库**

明天学习 RAG 的「记忆中枢」：

- Embedding 模型原理与使用
- Chroma 本地向量库
- Milvus 生产级向量库
- 相似度搜索与元数据过滤
- 实战：将今天的 chunks 嵌入并存入向量库

**预习建议**：了解什么是「向量嵌入（Embedding）」——将文本转为高维数字向量，语义相近的文本向量距离更近。

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 28*
