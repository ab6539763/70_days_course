# Day 11: 文件操作与标准库

> **培训阶段**: 第一阶段 Python 编程基础 | **第 2 周** | **学习时长**: 约 6-8 小时  
> **今日关键词**: 文件读写、with 语句、os、pathlib、datetime、random、re、文档关键词统计

---

## 📍 课程导航

### 上节回顾
在 **Day 10** 中，你学习了模块与包、异常处理、venv 虚拟环境和 pip 包管理，创建了 `llm_toolkit` 包。今天学习 **文件操作** 和常用 **标准库**——让程序能读写数据、处理路径和时间。

### 本节学习目标
完成本日学习后，你将能够：

1. 使用 `open()` 和 `with` 语句读写文本文件
2. 使用 `pathlib` 进行现代化路径操作
3. 使用 `os` 模块进行系统操作
4. 使用 `datetime`、`random`、`re` 标准库
5. 独立完成「文档关键词统计」项目

### 与后续课程的衔接
- **Day 12** API Key 将存储在 `.env` 文件中（文件操作基础）
- **Day 25+** RAG 开发需要读取大量文档文件
- **Day 11** 的 `re` 模块在文本清洗和 Prompt 处理中频繁使用

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：文件读写

#### 1.1 基本文件操作

```python
# day11/file_basic.py

# 写入文件
f = open("day11/hello.txt", "w", encoding="utf-8")
f.write("Hello, AI World!\n")
f.write("第二行内容\n")
f.close()  # 必须关闭！

# 读取文件
f = open("day11/hello.txt", "r", encoding="utf-8")
content = f.read()       # 读取全部内容
f.close()
print(content)

# 逐行读取
f = open("day11/hello.txt", "r", encoding="utf-8")
for line in f:
    print(line.strip())  # strip() 去除换行符
f.close()
```

#### 1.2 with 语句（推荐）

```python
# day11/with_statement.py

# with 自动管理文件的打开和关闭
with open("day11/hello.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)
# 离开 with 块后，文件自动关闭

# 写入
with open("day11/output.txt", "w", encoding="utf-8") as f:
    f.write("使用 with 语句写入\n")
    f.write("自动关闭，即使发生异常\n")

# 读取所有行到列表
with open("day11/hello.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()  # ['Hello, AI World!\n', '第二行内容\n']
    print(lines)
```

#### 1.3 文件打开模式

| 模式 | 说明 |
|------|------|
| `"r"` | 只读（默认） |
| `"w"` | 写入（覆盖已有内容） |
| `"a"` | 追加（在末尾添加） |
| `"r+"` | 读写 |
| `"rb"` | 二进制只读 |
| `"wb"` | 二进制写入 |

```python
# 追加模式
with open("day11/log.txt", "a", encoding="utf-8") as f:
    f.write(f"[{datetime.now()}] 新日志条目\n")
```

#### 1.4 异常处理与文件

```python
# day11/safe_file.py

def read_file_safe(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"文件不存在: {filepath}")
        return None
    except PermissionError:
        print(f"没有读取权限: {filepath}")
        return None
    except UnicodeDecodeError:
        print(f"文件编码错误: {filepath}")
        return None
```

---

### 9:45 - 10:30 | 模块二：pathlib 与 os

#### 2.1 pathlib（推荐）

```python
# day11/pathlib_demo.py
from pathlib import Path

# 创建路径对象
p = Path("day11/data/sample.txt")
print(p.name)        # sample.txt
print(p.stem)        # sample
print(p.suffix)      # .txt
print(p.parent)      # day11/data
print(p.exists())    # False

# 创建目录
data_dir = Path("day11/data")
data_dir.mkdir(parents=True, exist_ok=True)

# 写入文件
sample = data_dir / "sample.txt"
sample.write_text("pathlib 写入的内容", encoding="utf-8")

# 读取文件
content = sample.read_text(encoding="utf-8")
print(content)

# 遍历目录
for file in data_dir.glob("*.txt"):
    print(f"找到文件: {file}")

# 递归遍历
for file in Path("day11").rglob("*.py"):
    print(file)
```

#### 2.2 os 模块

```python
# day11/os_demo.py
import os

print(os.getcwd())                    # 当前工作目录
print(os.listdir("day11"))            # 目录内容列表
print(os.path.exists("day11"))      # 路径是否存在
print(os.path.isfile("day11/main.py"))  # 是否是文件
print(os.path.isdir("day11"))       # 是否是目录
print(os.path.getsize("day11/hello.txt"))  # 文件大小（字节）

# 环境变量（Day 12/13 读取 API Key）
api_key = os.environ.get("DEEPSEEK_API_KEY", "")
print(f"API Key: {'已设置' if api_key else '未设置'}")
```

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：datetime、random、re

#### 3.1 datetime 日期时间

```python
# day11/datetime_demo.py
from datetime import datetime, date, timedelta

# 当前时间
now = datetime.now()
print(now)                          # 2026-07-13 10:30:00.123456
print(now.strftime("%Y-%m-%d"))     # 2026-07-13
print(now.strftime("%H:%M:%S"))     # 10:30:00

# 创建特定日期
d = date(2026, 7, 13)
print(d)

# 时间运算
tomorrow = now + timedelta(days=1)
week_ago = now - timedelta(weeks=1)
print(f"明天: {tomorrow.date()}")
print(f"一周前: {week_ago.date()}")

# 解析字符串
parsed = datetime.strptime("2026-07-13 10:30", "%Y-%m-%d %H:%M")
print(parsed)
```

#### 3.2 random 随机

```python
# day11/random_demo.py
import random

print(random.randint(1, 100))       # 随机整数 [1, 100]
print(random.random())              # 随机浮点 [0.0, 1.0)
print(random.choice(["A", "B", "C"]))  # 随机选择

items = [1, 2, 3, 4, 5]
random.shuffle(items)               # 原地打乱
print(items)

# 随机采样
sample = random.sample(range(100), 5)  # 从 0-99 中随机取 5 个
print(sample)

# 设置种子（可复现）
random.seed(42)
print(random.randint(1, 100))  # 每次运行结果相同
```

#### 3.3 re 正则表达式

```python
# day11/regex_demo.py
import re

text = "联系方式: 138-1234-5678, 邮箱: zhangsan@example.com"

# 查找
phone = re.search(r"\d{3}-\d{4}-\d{4}", text)
if phone:
    print(f"电话: {phone.group()}")  # 138-1234-5678

# 查找所有
emails = re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", text)
print(f"邮箱: {emails}")

# 替换
cleaned = re.sub(r"\d{3}-\d{4}-\d{4}", "[电话已隐藏]", text)
print(cleaned)

# 分割
parts = re.split(r"[,，]\s*", "苹果, 香蕉，橙子, 葡萄")
print(parts)

# 匹配开头/结尾
print(re.match(r"^\d+", "123abc"))   # 从开头匹配
print(re.findall(r"\b\w{3,}\b", "AI is great for NLP"))  # 单词
```

| 正则符号 | 含义 |
|----------|------|
| `\d` | 数字 |
| `\w` | 字母数字下划线 |
| `\s` | 空白字符 |
| `.` | 任意字符 |
| `*` | 0 次或多次 |
| `+` | 1 次或多次 |
| `{n,m}` | n 到 m 次 |
| `^` | 开头 |
| `$` | 结尾 |

---

## 🌇 下午实操（14:00 - 17:30）

### 14:00 - 17:00 | 实操项目：文档关键词统计

#### 项目需求

1. 读取文本文件（支持 .txt / .md）
2. 统计总字符数、单词数、行数
3. 统计词频（Top N 高频词）
4. 支持中英文混合文本
5. 生成统计报告并保存为 JSON 和 TXT
6. 支持批量处理目录下所有文件

#### 参考代码

创建文件 `day11/doc_analyzer.py`：

```python
"""
Day 11 实操项目：文档关键词统计
"""

import re
import json
from pathlib import Path
from datetime import datetime
from collections import Counter


class DocumentAnalyzer:
    """文档分析器"""

    def __init__(self):
        self.content = ""
        self.filename = ""

    def load(self, filepath):
        """加载文件"""
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"文件不存在: {filepath}")
        self.filename = path.name
        self.content = path.read_text(encoding="utf-8")
        return self

    def basic_stats(self):
        """基础统计"""
        lines = self.content.split("\n")
        words = re.findall(r"\b\w+\b", self.content.lower())
        chinese_chars = re.findall(r"[\u4e00-\u9fff]", self.content)

        return {
            "filename": self.filename,
            "chars": len(self.content),
            "chars_no_space": len(self.content.replace(" ", "").replace("\n", "")),
            "lines": len(lines),
            "words": len(words),
            "chinese_chars": len(chinese_chars),
            "empty_lines": sum(1 for l in lines if not l.strip()),
        }

    def word_frequency(self, top_n=20):
        """词频统计"""
        words = re.findall(r"\b[a-zA-Z]{2,}\b", self.content.lower())
        counter = Counter(words)
        return counter.most_common(top_n)

    def chinese_frequency(self, top_n=20):
        """中文词频（单字统计）"""
        chars = re.findall(r"[\u4e00-\u9fff]", self.content)
        # 过滤常见虚词
        stop_chars = set("的了是在有不人也这中大为一个上国我到说们时要就出会可也你对生能而子那得于着下自之年过发后作里如")
        filtered = [c for c in chars if c not in stop_chars]
        counter = Counter(filtered)
        return counter.most_common(top_n)

    def generate_report(self):
        """生成完整报告"""
        stats = self.basic_stats()
        word_freq = self.word_frequency(10)
        cn_freq = self.chinese_frequency(10)

        report = {
            "generated_at": datetime.now().isoformat(),
            "basic_stats": stats,
            "top_english_words": dict(word_freq),
            "top_chinese_chars": dict(cn_freq),
        }
        return report

    def save_report(self, report, output_dir="day11/reports"):
        """保存报告"""
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)

        stem = Path(self.filename).stem
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # JSON 报告
        json_path = out / f"{stem}_{timestamp}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        # 文本报告
        txt_path = out / f"{stem}_{timestamp}.txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(f"文档分析报告\n")
            f.write(f"{'=' * 40}\n")
            f.write(f"文件: {report['basic_stats']['filename']}\n")
            f.write(f"生成时间: {report['generated_at']}\n\n")

            stats = report["basic_stats"]
            f.write(f"基础统计:\n")
            f.write(f"  总字符数: {stats['chars']}\n")
            f.write(f"  有效字符: {stats['chars_no_space']}\n")
            f.write(f"  总行数: {stats['lines']}\n")
            f.write(f"  英文单词: {stats['words']}\n")
            f.write(f"  中文字符: {stats['chinese_chars']}\n\n")

            f.write(f"高频英文词:\n")
            for word, count in report["top_english_words"].items():
                f.write(f"  {word}: {count}\n")

            f.write(f"\n高频中文字:\n")
            for char, count in report["top_chinese_chars"].items():
                f.write(f"  {char}: {count}\n")

        print(f"✅ 报告已保存:")
        print(f"   JSON: {json_path}")
        print(f"   TXT:  {txt_path}")
        return json_path, txt_path


def batch_analyze(directory):
    """批量分析目录下所有文本文件"""
    path = Path(directory)
    files = list(path.glob("*.txt")) + list(path.glob("*.md"))

    if not files:
        print(f"⚠️ 目录 {directory} 中没有 .txt 或 .md 文件")
        return

    print(f"📂 找到 {len(files)} 个文件")
    for file in files:
        print(f"\n分析: {file.name}")
        try:
            analyzer = DocumentAnalyzer().load(file)
            report = analyzer.generate_report()
            analyzer.save_report(report)
        except Exception as e:
            print(f"❌ 分析失败: {e}")


def main():
    print("=" * 40)
    print("     📄 文档关键词统计工具")
    print("=" * 40)

    while True:
        print("\n1. 分析单个文件  2. 批量分析目录  0. 退出")
        choice = input("请选择: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            filepath = input("文件路径: ").strip()
            try:
                analyzer = DocumentAnalyzer().load(filepath)
                report = analyzer.generate_report()
                stats = report["basic_stats"]
                print(f"\n📊 {stats['filename']}")
                print(f"  字符: {stats['chars']}, 行数: {stats['lines']}")
                print(f"  英文词: {stats['words']}, 中文: {stats['chinese_chars']}")
                print(f"\n  Top 英文词: {list(report['top_english_words'].items())[:5]}")
                save = input("保存报告? (y/n): ").strip().lower()
                if save == "y":
                    analyzer.save_report(report)
            except FileNotFoundError as e:
                print(f"❌ {e}")
        elif choice == "2":
            directory = input("目录路径: ").strip()
            batch_analyze(directory)
        else:
            print("⚠️ 无效选择")


if __name__ == "__main__":
    main()
```

#### 测试文件

创建 `day11/sample.txt`：

```
Python is a powerful programming language for AI development.
Python 是人工智能开发的首选编程语言。
Large Language Models (LLMs) are transforming the technology industry.
大语言模型正在改变科技行业。
Python Python Python AI AI development machine learning deep learning
```

---

### 17:00 - 17:30 | 扩展练习

```python
# 用 pathlib 实现文件备份
from pathlib import Path
import shutil
from datetime import datetime

def backup_file(filepath):
    src = Path(filepath)
    if not src.exists():
        return
    backup_dir = src.parent / "backups"
    backup_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dst = backup_dir / f"{src.stem}_{timestamp}{src.suffix}"
    shutil.copy2(src, dst)
    print(f"备份到: {dst}")
```

---

## 🌙 晚自习（19:00 - 21:00）

- 完成文档关键词统计项目
- 用工具分析 Day 1-10 的讲义文件
- Git 提交：`git commit -m "Day 11: 文件操作与文档分析"`

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | open() 与 with 语句 | |
| 2 | 文件读写模式 r/w/a | |
| 3 | pathlib 路径操作 | |
| 4 | os 模块基础 | |
| 5 | datetime 日期时间 | |
| 6 | random 随机数 | |
| 7 | re 正则表达式基础 | |
| 8 | 文档关键词统计项目 | |

---

## 📝 课后作业

### 必做题

1. 完成文档关键词统计项目
2. 创建 3 个测试文本文件并批量分析
3. 编写函数：统计指定目录下所有 .py 文件的总行数

### 选做题

4. 添加停用词过滤功能
5. 生成词频柱状图（用 ASCII 字符画）

---

## 💡 常见问题 FAQ

**Q1: 为什么要指定 encoding="utf-8"？**

A: Python 默认编码因系统而异。显式指定 UTF-8 避免中文乱码，跨平台一致。

**Q2: pathlib 和 os.path 用哪个？**

A: 新项目推荐 `pathlib`，API 更现代面向对象。`os.path` 在旧代码中常见。

**Q3: read() 和 readlines() 有什么区别？**

A: `read()` 返回整个文件字符串；`readlines()` 返回行列表。大文件建议逐行读取避免内存溢出。

---

## 🔮 明日预习

**Day 12: 网络请求与 API 调用** — HTTP 基础、requests 库、**首次调用大模型 API**

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 11*
