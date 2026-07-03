# Day 10: 模块包与异常处理

> **培训阶段**: 第一阶段 Python 编程基础 | **第 2 周** | **学习时长**: 约 6-8 小时  
> **今日关键词**: import、模块包、try/except、venv、pip、requirements.txt

---

## 📍 课程导航

### 上节回顾
在 **Day 8-9** 中，你学习了面向对象编程，构建了 `ChatMessage`、`BaseModel` 等类体系。随着项目代码增多，需要把代码分散到不同文件中管理——今天学习 **模块与包**，以及让程序更健壮的 **异常处理**。

### 本节学习目标
完成本日学习后，你将能够：

1. 使用 `import` 导入模块和包
2. 创建自己的 Python 模块和包
3. 使用 `try/except` 处理异常
4. 创建和管理 Python 虚拟环境（venv）
5. 使用 pip 安装包并管理 requirements.txt

### 与后续课程的衔接
- **Day 12** 将 `pip install requests` 并调用 API——今天学的包管理是基础
- **Day 13** 将安装 `python-dotenv`——通过 pip 管理
- 整个培训课程的项目都使用 venv + requirements.txt 管理依赖

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：模块与 import

#### 1.1 什么是模块？

一个 `.py` 文件就是一个模块。Day 6 的 `utils.py` 已经是模块。

```python
# day10/my_math.py
"""自定义数学工具模块"""

PI = 3.14159

def add(a, b):
    return a + b

def circle_area(radius):
    return PI * radius ** 2

# 模块级变量
__version__ = "1.0.0"
```

```python
# day10/use_math.py
# 导入整个模块
import my_math
print(my_math.add(3, 5))
print(my_math.PI)

# 导入特定函数
from my_math import add, circle_area
print(add(10, 20))

# 别名
import my_math as mm
print(mm.circle_area(5))

# 导入所有（不推荐）
from my_math import *
```

#### 1.2 标准库模块

```python
import os           # 操作系统接口
import sys          # 系统相关
import json         # JSON 处理
import random       # 随机数
import datetime       # 日期时间
from pathlib import Path  # 路径操作

print(os.getcwd())           # 当前工作目录
print(sys.version)           # Python 版本
print(random.randint(1, 100))  # 随机整数
print(datetime.date.today())   # 今天日期
```

#### 1.3 __name__ 与模块入口

```python
# day10/demo_module.py
def hello():
    print("Hello from module!")

# 直接运行此文件时 __name__ == "__main__"
# 被 import 时 __name__ == "demo_module"
if __name__ == "__main__":
    hello()
    print(f"模块名: {__name__}")
```

#### 1.4 包（Package）

包是包含 `__init__.py` 的目录，用于组织多个模块。

```
day10/
├── llm_toolkit/          # 包
│   ├── __init__.py       # 包初始化
│   ├── message.py        # 消息模块
│   ├── model.py          # 模型模块
│   └── utils.py          # 工具模块
└── main.py
```

```python
# day10/llm_toolkit/__init__.py
"""LLM 开发工具包"""
from .message import ChatMessage
from .model import BaseModel

__version__ = "0.1.0"
```

```python
# day10/llm_toolkit/message.py
class ChatMessage:
    def __init__(self, role, content):
        self.role = role
        self.content = content

    def to_dict(self):
        return {"role": self.role, "content": self.content}
```

```python
# day10/main.py
from llm_toolkit import ChatMessage
from llm_toolkit.message import ChatMessage as Msg

msg = ChatMessage("user", "你好")
print(msg.to_dict())
```

---

### 9:45 - 10:30 | 模块二：异常处理

#### 2.1 为什么需要异常处理？

```python
# 没有异常处理：程序崩溃
age = int(input("年龄: "))  # 用户输入 "abc" → ValueError，程序终止

# 有异常处理：优雅降级
try:
    age = int(input("年龄: "))
    print(f"你 {age} 岁")
except ValueError:
    print("⚠️ 请输入有效数字")
```

#### 2.2 try/except 基本语法

```python
# day10/exceptions.py

# 捕获特定异常
try:
    result = 10 / 0
except ZeroDivisionError:
    print("除数不能为零")

# 捕获多种异常
try:
    data = json.loads('{"key": value}')  # 故意写错
except json.JSONDecodeError as e:
    print(f"JSON 解析错误: {e}")
except Exception as e:
    print(f"其他错误: {e}")

# try/except/else/finally
try:
    f = open("data.txt", "r")
    content = f.read()
except FileNotFoundError:
    print("文件不存在")
    content = ""
else:
    print("文件读取成功")  # 没有异常时执行
finally:
    print("清理工作")      # 无论如何都执行
```

#### 2.3 常见异常类型

| 异常 | 触发场景 |
|------|----------|
| `ValueError` | 值类型正确但内容无效 |
| `TypeError` | 类型不匹配 |
| `KeyError` | 字典键不存在 |
| `IndexError` | 列表索引越界 |
| `FileNotFoundError` | 文件不存在 |
| `json.JSONDecodeError` | JSON 格式错误 |
| `ZeroDivisionError` | 除零 |
| `ConnectionError` | 网络连接失败（Day 12） |

#### 2.4 主动抛出异常

```python
def set_api_key(key):
    if not key:
        raise ValueError("API Key 不能为空")
    if not key.startswith("sk-"):
        raise ValueError("API Key 格式不正确，应以 sk- 开头")
    return key

def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("除数不能为零")
    return a / b
```

#### 2.5 与大模型开发的联系

```python
# API 调用异常处理（Day 12 会实际使用）
import json

def safe_api_call(response_text):
    try:
        data = json.loads(response_text)
        content = data["choices"][0]["message"]["content"]
        return content
    except json.JSONDecodeError:
        print("API 返回了非 JSON 数据")
        return None
    except KeyError as e:
        print(f"响应格式异常，缺少字段: {e}")
        return None
    except Exception as e:
        print(f"未知错误: {e}")
        return None
```

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：虚拟环境与包管理

#### 3.1 为什么需要虚拟环境？

不同项目可能需要不同版本的库。虚拟环境隔离项目依赖，避免冲突。

```bash
# 创建虚拟环境
cd ~/llm-course
python3 -m venv venv

# 激活虚拟环境
# Linux/macOS:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 激活后，pip install 只影响当前环境
# 命令行前缀会显示 (venv)
```

#### 3.2 pip 包管理

```bash
# 安装包
pip install requests

# 安装指定版本
pip install requests==2.31.0

# 卸载
pip uninstall requests

# 查看已安装
pip list

# 查看包信息
pip show requests

# 使用国内镜像（Day 1 已配置）
pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 3.3 requirements.txt

```bash
# 导出当前环境依赖
pip freeze > requirements.txt

# 安装项目依赖
pip install -r requirements.txt
```

```
# requirements.txt 示例
requests==2.31.0
python-dotenv==1.0.0
openai==1.12.0
```

#### 3.4 项目标准结构

```
llm-course/
├── venv/                  # 虚拟环境（不提交到 Git）
├── .gitignore             # 忽略 venv/
├── requirements.txt       # 依赖清单
├── day10/
│   ├── llm_toolkit/       # 自定义包
│   └── main.py
└── README.md
```

```gitignore
# .gitignore
venv/
__pycache__/
*.pyc
.env
.DS_Store
```

---

## 🌇 下午实操（14:00 - 17:30）

### 14:00 - 17:00 | 实操项目：LLM 工具包

#### 项目需求

1. 创建 `llm_toolkit` 包，包含 message、model、utils 三个模块
2. 添加异常处理和安全 JSON 解析
3. 创建 venv 并编写 requirements.txt
4. 编写主程序测试包的导入和使用

#### 参考代码

**目录结构：**

```
day10/
├── llm_toolkit/
│   ├── __init__.py
│   ├── message.py
│   ├── model.py
│   └── utils.py
├── main.py
└── requirements.txt
```

**llm_toolkit/message.py:**

```python
"""消息模块"""

class ChatMessage:
    VALID_ROLES = ("system", "user", "assistant")

    def __init__(self, role, content):
        if role not in self.VALID_ROLES:
            raise ValueError(f"无效角色: {role}")
        if not content or not content.strip():
            raise ValueError("消息内容不能为空")
        self.role = role
        self.content = content.strip()

    def to_dict(self):
        return {"role": self.role, "content": self.content}

    @classmethod
    def from_dict(cls, data):
        return cls(data["role"], data["content"])

    def __str__(self):
        icons = {"system": "⚙️", "user": "👤", "assistant": "🤖"}
        return f"{icons.get(self.role, '?')} [{self.role}]: {self.content[:50]}"
```

**llm_toolkit/utils.py:**

```python
"""工具模块"""
import json

def safe_json_loads(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON 解析失败: {e}") from e

def safe_json_load_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"文件不存在: {filepath}")
    except json.JSONDecodeError as e:
        raise ValueError(f"文件 JSON 格式错误: {e}") from e

def format_token_count(count):
    if count >= 1000:
        return f"{count / 1000:.1f}K"
    return str(count)
```

**llm_toolkit/model.py:**

```python
"""模型模块"""
from .message import ChatMessage

class ModelError(Exception):
    """模型相关异常"""
    pass

class BaseModel:
    def __init__(self, name, model_id):
        self.name = name
        self.model_id = model_id

    def validate_messages(self, messages):
        if not messages:
            raise ModelError("消息列表不能为空")
        for msg in messages:
            if "role" not in msg or "content" not in msg:
                raise ModelError(f"消息格式错误: {msg}")

    def chat(self, messages):
        self.validate_messages(messages)
        return f"[{self.name}] 模拟回复: 收到 {len(messages)} 条消息"
```

**llm_toolkit/__init__.py:**

```python
"""LLM 开发工具包 v0.1"""
from .message import ChatMessage
from .model import BaseModel, ModelError
from .utils import safe_json_loads, safe_json_load_file

__version__ = "0.1.0"
__all__ = ["ChatMessage", "BaseModel", "ModelError", "safe_json_loads"]
```

**main.py:**

```python
"""Day 10 主程序：测试 llm_toolkit 包"""

from llm_toolkit import ChatMessage, BaseModel, ModelError, safe_json_loads

def test_messages():
    print("=== 测试消息模块 ===")
    try:
        msg = ChatMessage("user", "你好")
        print(msg)
        print(msg.to_dict())

        # 测试异常
        ChatMessage("invalid", "test")
    except ValueError as e:
        print(f"✅ 捕获预期异常: {e}")

def test_model():
    print("\n=== 测试模型模块 ===")
    model = BaseModel("DeepSeek", "deepseek-chat")
    messages = [
        ChatMessage("user", "什么是 Python?").to_dict(),
    ]
    try:
        reply = model.chat(messages)
        print(reply)
        model.chat([])  # 触发异常
    except ModelError as e:
        print(f"✅ 捕获预期异常: {e}")

def test_utils():
    print("\n=== 测试工具模块 ===")
    valid = '{"key": "value"}'
    print(safe_json_loads(valid))

    try:
        safe_json_loads("{invalid}")
    except ValueError as e:
        print(f"✅ 捕获预期异常: {e}")

if __name__ == "__main__":
    test_messages()
    test_model()
    test_utils()
    print("\n✅ 所有测试完成")
```

**requirements.txt:**

```
# Day 10 项目依赖
# Day 12 会添加 requests
python-dotenv==1.0.0
```

---

### 17:00 - 17:30 | 环境搭建实操

```bash
# 在项目中创建虚拟环境
cd ~/llm-course
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r day10/requirements.txt

# 运行测试
python day10/main.py

# 确认环境
which python  # 应指向 venv 目录
pip list
```

---

## 🌙 晚自习（19:00 - 21:00）

- 完成 llm_toolkit 包
- 创建 .gitignore 文件
- Git 提交：`git commit -m "Day 10: 模块包与异常处理"`

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | import 导入模块 | |
| 2 | from...import 用法 | |
| 3 | 创建自定义模块 | |
| 4 | 包结构与 __init__.py | |
| 5 | try/except/else/finally | |
| 6 | 常见异常类型 | |
| 7 | raise 抛出异常 | |
| 8 | venv 虚拟环境 | |
| 9 | pip 与 requirements.txt | |
| 10 | llm_toolkit 包项目 | |

---

## 📝 课后作业

### 必做题

1. 完成 llm_toolkit 包并通过 main.py 测试
2. 创建 venv 并安装 requirements.txt
3. 为 Day 7 通讯录添加异常处理（文件不存在、JSON 错误等）

### 选做题

4. 在 llm_toolkit 中添加 logging 模块
5. 编写自定义异常类 `APIError`、`ConfigError`

---

## 💡 常见问题 FAQ

**Q1: import 报错 ModuleNotFoundError？**

A: 检查：1) 文件/包是否存在；2) 是否在正确目录运行；3) `__init__.py` 是否存在；4) PYTHONPATH 是否包含模块目录。

**Q2: 应该捕获 Exception 吗？**

A: 尽量捕获具体异常。`except Exception` 作为最后兜底，但不要吞掉所有异常。

**Q3: venv 需要提交到 Git 吗？**

A: 不需要。将 `venv/` 加入 `.gitignore`，只提交 `requirements.txt`。

**Q4: pip 和 pip3 有什么区别？**

A: 在 venv 激活后，`pip` 就是当前环境的 pip3。系统级可能 `pip` 对应 Python 2（已淘汰）。

---

## 🔮 明日预习

**Day 11: 文件操作与标准库** — 文件读写、with、os/pathlib/datetime/random/re

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 10*
