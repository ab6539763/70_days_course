# Day 5: 核心数据结构下——字典与 JSON

> **培训阶段**: 第一阶段 Python 编程基础 | **第 1 周** | **学习时长**: 约 6-8 小时  
> **今日关键词**: dict 操作、JSON 格式、json 模块、API 响应解析

---

## 📍 课程导航

### 上节回顾
在 **Day 4** 中，你学习了列表的增删改查、切片、排序和列表推导式，完成了「待办事项管理器」。项目中每个待办用 **字典** 存储属性、所有待办放在 **列表** 中——今天将系统学习字典，并深入 **JSON**——这是与大模型 API 交互的基石数据格式。

### 本节学习目标
完成本日学习后，你将能够：

1. 熟练创建和操作字典（dict）
2. 理解 JSON 格式的语法规则
3. 使用 `json` 模块进行序列化与反序列化
4. 解析模拟的大模型 API 返回 JSON
5. 理解「列表套字典」在 API 数据中的典型结构
6. 为 Day 12 首次调用大模型 API 做好数据格式准备

### 与后续课程的衔接
- **Day 6** 将学习函数——把今天的 JSON 解析逻辑封装为可复用函数
- **Day 11** 将把 JSON 数据持久化到文件
- **Day 12** 将首次调用大模型 API——请求和响应都是 JSON 格式
- **Day 14** 多轮对话助手的消息历史：`[{"role": "user", "content": "..."}]`

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：字典基础

#### 1.1 创建字典

```python
# day05/dict_create.py

# 空字典
empty = {}
also_empty = dict()

# 键值对字典
person = {
    "name": "张三",
    "age": 25,
    "city": "北京",
    "is_student": False
}

# dict() 构造函数
config = dict(host="api.deepseek.com", port=443, timeout=30)

# 键必须是不可变类型（字符串、数字、元组）
# 值可以是任意类型

print(type(person))  # <class 'dict'>
print(len(person))   # 4
```

#### 1.2 访问与修改

```python
# day05/dict_access.py
user = {"name": "李四", "age": 28, "role": "developer"}

# 访问
print(user["name"])        # 李四
print(user.get("age"))     # 28
print(user.get("email"))   # None（键不存在返回 None）
print(user.get("email", "未设置"))  # 未设置（自定义默认值）

# 修改
user["age"] = 29
user["email"] = "lisi@example.com"  # 新增键值对

# 删除
del user["role"]
removed = user.pop("email")  # 删除并返回值
print(user)
```

#### 1.3 遍历字典

```python
# day05/dict_iterate.py
model_config = {
    "model": "deepseek-chat",
    "temperature": 0.7,
    "max_tokens": 2048,
}

# 遍历键
for key in model_config:
    print(f"键: {key}")

# 遍历值
for value in model_config.values():
    print(f"值: {value}")

# 同时遍历键和值（推荐）
for key, value in model_config.items():
    print(f"{key}: {value}")
```

#### 1.4 常用方法

```python
# day05/dict_methods.py
data = {"a": 1, "b": 2, "c": 3}

# 所有键、值、键值对
print(list(data.keys()))    # ['a', 'b', 'c']
print(list(data.values()))  # [1, 2, 3]
print(list(data.items()))   # [('a', 1), ('b', 2), ('c', 3)]

# 更新
data.update({"d": 4, "a": 10})  # 合并，相同键会覆盖
print(data)  # {'a': 10, 'b': 2, 'c': 3, 'd': 4}

# 检查键是否存在
print("a" in data)      # True
print("z" not in data)  # True
```

---

### 9:45 - 10:30 | 模块二：嵌套结构与实用模式

#### 2.1 列表与字典的组合

```python
# day05/nested.py

# 列表套字典——大模型 API 最典型结构
messages = [
    {"role": "system", "content": "你是一个有帮助的助手。"},
    {"role": "user", "content": "什么是 Python？"},
    {"role": "assistant", "content": "Python 是一种高级编程语言..."},
]

# 访问
print(messages[0]["role"])     # system
print(messages[1]["content"])  # 什么是 Python？

# 添加新消息
messages.append({
    "role": "user",
    "content": "能写个 Hello World 吗？"
})

# 字典套列表
student = {
    "name": "王五",
    "scores": [85, 92, 78],
    "courses": ["Python", "数学", "英语"],
}
print(student["scores"][0])    # 85
print(student["courses"][-1])  # 英语
```

#### 2.2 字典推导式

```python
# day05/dict_comprehension.py

# 基本形式：{键表达式: 值表达式 for 变量 in 序列}
squares = {x: x**2 for x in range(1, 6)}
print(squares)  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# 带条件
even_squares = {x: x**2 for x in range(10) if x % 2 == 0}
print(even_squares)  # {0: 0, 2: 4, 4: 16, 6: 36, 8: 64}

# 反转键值
original = {"a": 1, "b": 2, "c": 3}
reversed_dict = {v: k for k, v in original.items()}
print(reversed_dict)  # {1: 'a', 2: 'b', 3: 'c'}
```

#### 2.3  defaultdict 与 Counter 预览

```python
# day05/useful_patterns.py

# 统计词频（不使用额外库）
text = "python is great and python is popular"
word_count = {}
for word in text.split():
    word_count[word] = word_count.get(word, 0) + 1
print(word_count)
# {'python': 2, 'is': 2, 'great': 1, 'and': 1, 'popular': 1}

# 按值排序
sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
print(sorted_words)
```

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：JSON 格式详解

#### 3.1 什么是 JSON？

**JSON**（JavaScript Object Notation）是一种轻量级数据交换格式，是大模型 API 通信的**标准格式**。

```json
{
    "model": "deepseek-chat",
    "messages": [
        {"role": "user", "content": "你好"}
    ],
    "temperature": 0.7,
    "max_tokens": 1024
}
```

#### 3.2 JSON 语法规则

| 规则 | 正确 ✅ | 错误 ❌ |
|------|---------|---------|
| 键必须用双引号 | `"name": "张三"` | `name: "张三"` |
| 字符串用双引号 | `"hello"` | `'hello'` |
| 布尔值小写 | `true`, `false` | `True`, `False` |
| 空值 | `null` | `None` |
| 不支持注释 | — | `// 注释` |
| 不支持尾随逗号 | `{"a": 1}` | `{"a": 1,}` |

#### 3.3 Python 与 JSON 类型对照

| JSON 类型 | Python 类型 |
|-----------|-------------|
| object `{}` | dict |
| array `[]` | list |
| string | str |
| number | int / float |
| true / false | True / False |
| null | None |

#### 3.4 json 模块

```python
# day05/json_module.py
import json

# ===== Python → JSON（序列化）=====
data = {
    "name": "张三",
    "age": 25,
    "skills": ["Python", "AI"],
    "active": True,
    "score": None,
}

# 转为 JSON 字符串
json_str = json.dumps(data, ensure_ascii=False, indent=2)
print(json_str)
print(type(json_str))  # <class 'str'>

# 写入文件
with open("day05/data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# ===== JSON → Python（反序列化）=====
json_text = '{"name": "李四", "age": 30}'

# 从字符串解析
parsed = json.loads(json_text)
print(parsed["name"])  # 李四
print(type(parsed))    # <class 'dict'>

# 从文件读取
with open("day05/data.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
print(loaded)
```

#### 3.5 模拟大模型 API 响应

```python
# day05/api_response.py
import json

# 模拟 DeepSeek API 响应
api_response_json = """
{
    "id": "chatcmpl-abc123",
    "object": "chat.completion",
    "created": 1700000000,
    "model": "deepseek-chat",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "Python 是一种高级、解释型的编程语言，以其简洁的语法和强大的生态系统而闻名。"
            },
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 15,
        "completion_tokens": 42,
        "total_tokens": 57
    }
}
"""

# 解析 JSON
response = json.loads(api_response_json)

# 提取关键信息
content = response["choices"][0]["message"]["content"]
model = response["model"]
total_tokens = response["usage"]["total_tokens"]

print(f"模型: {model}")
print(f"回复: {content}")
print(f"消耗 tokens: {total_tokens}")
```

#### 3.6 安全解析 JSON

```python
# day05/safe_json.py
import json

def safe_parse_json(text):
    """安全解析 JSON，失败时返回 None"""
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        print(f"JSON 解析失败: {e}")
        return None

# 正常解析
result = safe_parse_json('{"key": "value"}')
print(result)

# 错误 JSON
result = safe_parse_json('{key: value}')  # 键没有引号
print(result)  # None
```

---

## 🌇 下午实操（14:00 - 17:30）

### 14:00 - 17:00 | 实操项目：API 响应解析器

#### 项目背景

在 Day 12 你将真正调用大模型 API。今天先用模拟数据练习 JSON 解析——这是每个大模型开发者的必备技能。

#### 项目需求

1. 加载模拟的 API 响应 JSON 文件
2. 解析并美观展示对话内容
3. 统计 token 使用量
4. 支持从 JSON 文件读取/保存对话历史
5. 模拟发送新消息并更新 JSON

#### 参考代码

创建文件 `day05/api_parser.py`：

```python
"""
Day 5 实操项目：API 响应解析器
练习：字典操作、JSON 解析、嵌套数据访问
"""

import json
from datetime import datetime

# ===== 模拟 API 数据 =====

SAMPLE_RESPONSE = {
    "id": "chatcmpl-demo001",
    "object": "chat.completion",
    "created": 1700000000,
    "model": "deepseek-chat",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "你好！我是 AI 助手，有什么可以帮你的吗？"
            },
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 20,
        "completion_tokens": 18,
        "total_tokens": 38
    }
}

SAMPLE_CONVERSATION = {
    "conversation_id": "conv-001",
    "created_at": "2026-07-07T10:00:00",
    "model": "deepseek-chat",
    "messages": [
        {"role": "system", "content": "你是一个专业的 Python 编程助手。"},
        {"role": "user", "content": "什么是列表推导式？"},
        {"role": "assistant", "content": "列表推导式是 Python 中一种简洁的创建列表的方式。\n\n语法：[表达式 for 变量 in 序列 if 条件]\n\n示例：\n```python\nsquares = [x**2 for x in range(10)]\n```"},
        {"role": "user", "content": "能给个过滤的例子吗？"},
        {"role": "assistant", "content": "当然！过滤偶数：\n```python\nevens = [x for x in range(20) if x % 2 == 0]\n```"},
    ],
    "total_tokens": 256
}


# ===== 解析功能 =====

def parse_api_response(response_data):
    """解析 API 响应，提取关键信息"""
    result = {
        "id": response_data.get("id", "unknown"),
        "model": response_data.get("model", "unknown"),
        "content": "",
        "finish_reason": "",
        "tokens": {},
    }

    choices = response_data.get("choices", [])
    if choices:
        result["content"] = choices[0]["message"]["content"]
        result["finish_reason"] = choices[0].get("finish_reason", "")

    usage = response_data.get("usage", {})
    result["tokens"] = {
        "prompt": usage.get("prompt_tokens", 0),
        "completion": usage.get("completion_tokens", 0),
        "total": usage.get("total_tokens", 0),
    }

    return result


def display_response(parsed):
    """美观展示解析结果"""
    print("\n" + "=" * 50)
    print(f"🤖 模型: {parsed['model']}")
    print(f"📋 ID: {parsed['id']}")
    print(f"🏁 结束原因: {parsed['finish_reason']}")
    print("-" * 50)
    print(f"💬 回复内容:\n{parsed['content']}")
    print("-" * 50)
    t = parsed["tokens"]
    print(f"📊 Token 用量: 输入={t['prompt']}, 输出={t['completion']}, 合计={t['total']}")
    print("=" * 50)


def display_conversation(conv_data):
    """展示对话历史"""
    print(f"\n💬 对话 [{conv_data['conversation_id']}]")
    print(f"模型: {conv_data['model']} | 总 tokens: {conv_data['total_tokens']}")
    print("-" * 50)

    role_icons = {
        "system": "⚙️",
        "user": "👤",
        "assistant": "🤖",
    }

    for msg in conv_data["messages"]:
        icon = role_icons.get(msg["role"], "❓")
        content = msg["content"]
        # 长内容截断显示
        if len(content) > 100:
            content = content[:100] + "..."
        print(f"{icon} [{msg['role']}]: {content}")

    print("-" * 50)


def save_json(data, filename):
    """保存数据到 JSON 文件"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ 已保存到 {filename}")


def load_json(filename):
    """从 JSON 文件加载数据"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️ 文件 {filename} 不存在")
        return None
    except json.JSONDecodeError as e:
        print(f"⚠️ JSON 格式错误: {e}")
        return None


def add_message(conv_data, role, content):
    """向对话中添加消息"""
    conv_data["messages"].append({
        "role": role,
        "content": content,
    })
    # 简单估算 token（实际 API 有精确计算）
    estimated_tokens = len(content) // 2
    conv_data["total_tokens"] = conv_data.get("total_tokens", 0) + estimated_tokens
    print(f"✅ 已添加 {role} 消息（约 {estimated_tokens} tokens）")


def analyze_messages(messages):
    """分析消息列表统计"""
    stats = {}
    for msg in messages:
        role = msg["role"]
        stats[role] = stats.get(role, 0) + 1

    total_chars = sum(len(m["content"]) for m in messages)

    print("\n📊 消息分析")
    for role, count in stats.items():
        print(f"  {role}: {count} 条")
    print(f"  总字符数: {total_chars}")
    print(f"  平均消息长度: {total_chars // len(messages)} 字符")


# ===== 主程序 =====

def main():
    print("=" * 50)
    print("     📡 API 响应解析器 v1.0")
    print("=" * 50)
    print("💡 此工具为 Day 12 调用真实 API 做准备")

    # 初始化对话数据
    conversation = SAMPLE_CONVERSATION.copy()
    conversation["messages"] = list(conversation["messages"])

    while True:
        print("\n1. 解析 API 响应示例")
        print("2. 查看对话历史")
        print("3. 添加消息")
        print("4. 分析消息统计")
        print("5. 保存对话到文件")
        print("6. 从文件加载对话")
        print("0. 退出")
        choice = input("请选择: ").strip()

        if choice == "0":
            print("再见！")
            break
        elif choice == "1":
            parsed = parse_api_response(SAMPLE_RESPONSE)
            display_response(parsed)
        elif choice == "2":
            display_conversation(conversation)
        elif choice == "3":
            print("角色: 1-user  2-assistant  3-system")
            role_map = {"1": "user", "2": "assistant", "3": "system"}
            r = input("选择角色: ").strip()
            role = role_map.get(r, "user")
            content = input("消息内容: ").strip()
            if content:
                add_message(conversation, role, content)
        elif choice == "4":
            analyze_messages(conversation["messages"])
        elif choice == "5":
            filename = input("文件名 (默认 conversation.json): ").strip()
            filename = filename or "day05/conversation.json"
            save_json(conversation, filename)
        elif choice == "6":
            filename = input("文件名: ").strip()
            loaded = load_json(filename)
            if loaded:
                conversation = loaded
                print("✅ 对话已加载")
        else:
            print("⚠️ 无效选择")


if __name__ == "__main__":
    main()
```

---

### 17:00 - 17:30 | 扩展练习

#### 练习：配置文件管理

```python
# day05/config_manager.py
import json

DEFAULT_CONFIG = {
    "api_key": "",
    "model": "deepseek-chat",
    "temperature": 0.7,
    "max_tokens": 2048,
    "base_url": "https://api.deepseek.com",
}

def load_config(path="config.json"):
    try:
        with open(path, "r") as f:
            config = json.load(f)
            # 合并默认配置
            return {**DEFAULT_CONFIG, **config}
    except FileNotFoundError:
        return DEFAULT_CONFIG.copy()

def save_config(config, path="config.json"):
    with open(path, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"配置已保存到 {path}")
```

---

## 🌙 晚自习（19:00 - 21:00）

### 19:00 - 20:00 | JSON 调试技巧

#### 在线工具推荐

- **JSON Formatter**: https://jsonformatter.org/
- Python 交互式验证：

```python
import json
# 验证 JSON 是否合法
json.loads(your_json_string)  # 不报错即合法
```

#### 常见 JSON 错误排查

| 错误 | 原因 | 修复 |
|------|------|------|
| `JSONDecodeError: Expecting property name` | 键没用双引号 | 给键加双引号 |
| `JSONDecodeError: Extra data` | 多个 JSON 对象连在一起 | 分开解析 |
| `TypeError: Object of type X is not JSON serializable` | Python 对象不能直接序列化 | 转为 dict/list |

### 20:00 - 21:00 | 自习

- 完成 API 响应解析器项目
- 手动编写一个 JSON 文件，用程序读取并解析
- Git 提交：`git commit -m "Day 5: 字典与JSON解析器"`

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | 字典创建与访问 | |
| 2 | get() 安全访问与默认值 | |
| 3 | 字典增删改查 | |
| 4 | keys()/values()/items() 遍历 | |
| 5 | 字典推导式 | |
| 6 | 列表与字典嵌套结构 | |
| 7 | JSON 语法规则 | |
| 8 | json.dumps() / json.loads() | |
| 9 | json.dump() / json.load() 文件操作 | |
| 10 | 解析 API 响应 JSON | |
| 11 | API 响应解析器项目 | |

---

## 📝 课后作业

### 必做题

1. **API 响应解析器**：完成下午项目
2. **手写 JSON**：创建一个包含 3 轮对话的 JSON 文件，编写程序读取并打印每条消息
3. **类型转换练习**：将以下 Python 数据转为 JSON 字符串并还原

```python
data = {
    "users": [
        {"name": "张三", "scores": [90, 85, 92]},
        {"name": "李四", "scores": [78, 88, 95]},
    ],
    "total": 2,
    "active": True,
}
```

### 选做题

4. **词频 JSON 报告**：读取文本文件，统计词频，输出 JSON 格式报告
5. **模拟 API 请求体构建器**：用户输入消息，程序构建符合 OpenAI 格式的 JSON 请求体

---

## 💡 常见问题 FAQ

**Q1: 字典的键可以用列表吗？**

A: 不可以。键必须是不可变类型（str、int、float、tuple）。列表是可变的，不能作为键。

**Q2: `json.dumps()` 和 `json.dump()` 有什么区别？**

A: `dumps` 把 Python 对象转为 JSON **字符串**；`dump` 直接写入**文件**。对应的 `loads` 和 `load` 是反序列化。

**Q3: 为什么 JSON 用 `null` 而 Python 用 `None`？**

A: JSON 是独立的数据格式规范，Python 的 `json` 模块会自动转换：`None` ↔ `null`。

**Q4: `ensure_ascii=False` 是什么意思？**

A: 默认 `dumps` 会把中文转为 `\uxxxx` 编码。设为 `False` 可以保留中文原文。

**Q5: 如何判断一个字符串是不是合法 JSON？**

A: 用 try-except 包裹 `json.loads()`，捕获 `json.JSONDecodeError` 异常。

---

## 🔮 明日预习

**Day 6: 函数**

明天你将学习：

- 函数定义、参数、返回值
- 作用域与 lambda 表达式
- 递归入门
- **重构前几天项目**——把重复代码封装为函数

**预习建议**：回顾今天项目中每个 `def` 函数，思考哪些逻辑可以进一步拆分。

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 5*
