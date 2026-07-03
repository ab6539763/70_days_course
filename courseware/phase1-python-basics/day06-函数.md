# Day 6: 函数

> **培训阶段**: 第一阶段 Python 编程基础 | **第 1 周** | **学习时长**: 约 6-8 小时  
> **今日关键词**: 函数定义、参数、返回值、作用域、lambda、递归、代码重构

---

## 📍 课程导航

### 上节回顾
在 **Day 5** 中，你学习了字典操作、JSON 格式与 `json` 模块，完成了「API 响应解析器」。项目中已使用 `def` 定义函数，但尚未系统学习。今天将掌握函数——**代码复用与模块化的核心工具**。

### 本节学习目标
完成本日学习后，你将能够：

1. 定义和调用函数，理解参数与返回值
2. 使用默认参数、关键字参数、可变参数
3. 理解变量作用域（局部 vs 全局）
4. 使用 lambda 表达式处理简单逻辑
5. 理解递归的基本思想
6. 将 Day 2-5 的项目重构为函数式结构

### 与后续课程的衔接
- **Day 8-9** 面向对象编程是函数的进阶——用类组织相关函数和数据
- **Day 10** 模块与包——将函数分散到不同文件中管理
- **Day 13** 装饰器——本质是「包装函数的高阶函数」
- **Day 14** 阶段项目将用函数模块化 AI 助手的各个功能

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：函数基础

#### 1.1 为什么需要函数？

```python
# 没有函数：重复代码
print("=" * 40)
print("  菜单 A")
print("=" * 40)

print("=" * 40)
print("  菜单 B")
print("=" * 40)

# 有函数：复用
def print_header(title):
    print("=" * 40)
    print(f"  {title}")
    print("=" * 40)

print_header("菜单 A")
print_header("菜单 B")
```

#### 1.2 定义与调用

```python
# day06/function_basic.py

def greet(name):
    """向用户打招呼（文档字符串）"""
    message = f"你好, {name}!"
    return message

# 调用函数
result = greet("张三")
print(result)  # 你好, 张三!

# 没有 return 的函数返回 None
def say_hello():
    print("Hello!")

ret = say_hello()  # Hello!
print(ret)         # None
```

#### 1.3 参数类型

```python
# day06/parameters.py

# 位置参数
def add(a, b):
    return a + b

print(add(3, 5))  # 8

# 默认参数
def greet(name, greeting="你好"):
    return f"{greeting}, {name}!"

print(greet("李四"))              # 你好, 李四!
print(greet("李四", "早上好"))     # 早上好, 李四!

# 关键字参数（顺序无关）
print(greet(greeting="欢迎", name="王五"))  # 欢迎, 王五!

# 可变位置参数 *args
def sum_all(*numbers):
    total = 0
    for n in numbers:
        total += n
    return total

print(sum_all(1, 2, 3))       # 6
print(sum_all(1, 2, 3, 4, 5)) # 15

# 可变关键字参数 **kwargs
def create_user(**info):
    return info

user = create_user(name="张三", age=25, city="北京")
print(user)  # {'name': '张三', 'age': 25, 'city': '北京'}
```

#### 1.4 与大模型开发的联系

```python
# API 调用函数雏形（Day 12 会真正使用）
def build_request(model, messages, temperature=0.7, max_tokens=2048):
    """构建 API 请求体"""
    return {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

messages = [{"role": "user", "content": "你好"}]
request = build_request("deepseek-chat", messages)
print(request)
```

---

### 9:45 - 10:30 | 模块二：返回值与作用域

#### 2.1 多种返回值

```python
# day06/return_values.py

# 返回多个值（实际是返回元组）
def get_min_max(numbers):
    return min(numbers), max(numbers)

nums = [3, 1, 4, 1, 5, 9]
minimum, maximum = get_min_max(nums)
print(f"最小: {minimum}, 最大: {maximum}")

# 提前返回
def check_api_key(key):
    if not key:
        return False, "API Key 不能为空"
    if len(key) < 10:
        return False, "API Key 格式不正确"
    return True, "验证通过"

valid, msg = check_api_key("")
print(msg)  # API Key 不能为空
```

#### 2.2 变量作用域

```python
# day06/scope.py

global_var = "我是全局变量"

def demo():
    local_var = "我是局部变量"
    print(global_var)  # 可以读取全局变量
    print(local_var)

demo()
# print(local_var)  # NameError! 外部不能访问局部变量

# 修改全局变量需要 global 声明
count = 0

def increment():
    global count
    count += 1

increment()
print(count)  # 1

# ⚠️ 最佳实践：尽量避免使用 global，通过参数和返回值传递数据
```

#### 2.3 LEGB 规则

Python 查找变量的顺序：

```
L - Local（局部）
E - Enclosing（嵌套函数的外层）
G - Global（全局）
B - Built-in（内置，如 print、len）
```

```python
x = "全局"

def outer():
    x = "外层"
    def inner():
        x = "内层"
        print(x)  # 内层
    inner()

outer()
```

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：lambda 与递归

#### 3.1 lambda 表达式

```python
# day06/lambda.py

# 普通函数
def square(x):
    return x ** 2

# 等价的 lambda
square = lambda x: x ** 2
print(square(5))  # 25

# lambda 常用于简短回调，如排序
students = [
    {"name": "张三", "score": 85},
    {"name": "李四", "score": 92},
    {"name": "王五", "score": 78},
]

# 按分数降序排列
sorted_students = sorted(students, key=lambda s: s["score"], reverse=True)
for s in sorted_students:
    print(f"{s['name']}: {s['score']}")

# map / filter 与 lambda
nums = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, nums))
evens = list(filter(lambda x: x % 2 == 0, nums))
print(doubled)  # [2, 4, 6, 8, 10]
print(evens)    # [2, 4]
```

#### 3.2 递归

```python
# day06/recursion.py

# 经典：阶乘
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))  # 120

# 经典：斐波那契
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

for i in range(10):
    print(fib(i), end=" ")  # 0 1 1 2 3 5 8 13 21 34

# 实用：遍历嵌套 JSON
def find_key(data, target_key):
    """在嵌套字典中查找指定键的值"""
    if isinstance(data, dict):
        if target_key in data:
            return data[target_key]
        for value in data.values():
            result = find_key(value, target_key)
            if result is not None:
                return result
    elif isinstance(data, list):
        for item in data:
            result = find_key(item, target_key)
            if result is not None:
                return result
    return None
```

#### 3.3 函数作为参数（高阶函数）

```python
# day06/higher_order.py

def apply_operation(x, y, operation):
    """将操作作为参数传入"""
    return operation(x, y)

result = apply_operation(10, 3, lambda a, b: a + b)
print(result)  # 13

# 这思想是 Day 13 装饰器的基础！
def repeat(n):
    """装饰器雏形：重复执行函数 n 次"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(n):
                print(f"--- 第 {i+1} 次 ---")
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(3)
def say_hi():
    print("Hi!")

# say_hi()  # 会打印 3 次 Hi!
```

---

## 🌇 下午实操（14:00 - 17:30）

### 14:00 - 17:00 | 实操项目：重构前几天代码

#### 项目目标

将 Day 2-5 的核心逻辑抽取为独立函数，组织成可复用的工具模块。

#### 参考代码

创建文件 `day06/utils.py`（工具函数库）：

```python
"""
Day 6 工具函数库
将 Day 2-5 的常用逻辑封装为可复用函数
"""


# ===== Day 2: 文本处理 =====

def clean_text(text, operations=None):
    """
    文本清洗
    operations: 操作列表，如 ['strip', 'lower', 'remove_spaces']
    """
    if operations is None:
        operations = ["strip"]

    for op in operations:
        if op == "strip":
            text = text.strip()
        elif op == "lower":
            text = text.lower()
        elif op == "upper":
            text = text.upper()
        elif op == "remove_spaces":
            text = text.replace(" ", "").replace("\t", "").replace("\n", "")
    return text


def count_text_info(text):
    """统计文本信息，返回字典"""
    return {
        "chars": len(text),
        "words": len(text.split()),
        "lines": text.count("\n") + 1,
    }


def format_prompt(role, task, language="中文", constraints=None):
    """生成 Prompt 模板（Day 17 会深入）"""
    prompt = f"你是一位{role}。\n\n任务：{task}\n\n要求：\n- 使用{language}回答\n"
    if constraints:
        for i, c in enumerate(constraints, 1):
            prompt += f"- {c}\n"
    return prompt


# ===== Day 3: 游戏与工具 =====

def validate_input(prompt, validator, error_msg="输入无效，请重试"):
    """通用输入验证循环"""
    while True:
        value = input(prompt).strip()
        if validator(value):
            return value
        print(f"⚠️ {error_msg}")


def validate_int(prompt, min_val=None, max_val=None):
    """验证整数输入"""
    def check(v):
        if not v.isdigit():
            return False
        n = int(v)
        if min_val is not None and n < min_val:
            return False
        if max_val is not None and n > max_val:
            return False
        return True
    return int(validate_input(prompt, check))


# ===== Day 4: 列表工具 =====

def filter_list(items, key_func, value):
    """按条件过滤列表"""
    return [item for item in items if key_func(item) == value]


def sort_by_key(items, key_func, reverse=False):
    """按指定键排序"""
    return sorted(items, key=key_func, reverse=reverse)


# ===== Day 5: JSON 工具 =====

import json

def safe_json_loads(text):
    """安全解析 JSON 字符串"""
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        print(f"JSON 解析失败: {e}")
        return None


def extract_api_content(response):
    """从 API 响应中提取回复内容"""
    try:
        return response["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        return None


def extract_api_tokens(response):
    """从 API 响应中提取 token 统计"""
    usage = response.get("usage", {})
    return {
        "prompt": usage.get("prompt_tokens", 0),
        "completion": usage.get("completion_tokens", 0),
        "total": usage.get("total_tokens", 0),
    }
```

创建文件 `day06/refactored_demo.py`（重构后的演示程序）：

```python
"""
Day 6 实操项目：使用工具函数库重构演示
"""

from utils import (
    clean_text, count_text_info, format_prompt,
    validate_int, safe_json_loads, extract_api_content,
)

def demo_text_tools():
    """演示文本工具"""
    print("\n=== 文本工具演示 ===")
    text = "  Hello, DeepSeek AI!  "
    cleaned = clean_text(text, ["strip", "lower"])
    print(f"清洗后: '{cleaned}'")
    info = count_text_info(text)
    print(f"统计: {info}")

    prompt = format_prompt(
        role="Python 导师",
        task="解释什么是函数",
        constraints=["简洁明了", "附带代码示例", "不超过 200 字"],
    )
    print(f"\n生成的 Prompt:\n{prompt}")


def demo_validation():
    """演示输入验证"""
    print("\n=== 输入验证演示 ===")
    age = validate_int("请输入年龄 (1-120): ", min_val=1, max_val=120)
    print(f"你的年龄: {age}")


def demo_json_tools():
    """演示 JSON 工具"""
    print("\n=== JSON 工具演示 ===")
    sample = '{"choices": [{"message": {"content": "你好！"}}], "usage": {"total_tokens": 10}}'
    data = safe_json_loads(sample)
    if data:
        content = extract_api_content(data)
        print(f"提取内容: {content}")


def main():
    print("=" * 40)
    print("   Day 6 函数重构演示")
    print("=" * 40)

    while True:
        print("\n1. 文本工具  2. 输入验证  3. JSON 工具  0. 退出")
        choice = input("请选择: ").strip()

        demos = {"1": demo_text_tools, "2": demo_validation, "3": demo_json_tools}
        if choice == "0":
            break
        elif choice in demos:
            demos[choice]()
        else:
            print("⚠️ 无效选择")


if __name__ == "__main__":
    main()
```

#### 重构要点总结

| 原则 | 说明 | 示例 |
|------|------|------|
| DRY | Don't Repeat Yourself | 输入验证提取为 `validate_input()` |
| 单一职责 | 每个函数只做一件事 | `clean_text()` 只负责清洗 |
| 有意义命名 | 函数名表达意图 | `extract_api_content()` |
| 文档字符串 | 说明参数和返回值 | `"""安全解析 JSON"""` |
| 合理参数 | 提供默认值 | `operations=None` |

---

### 17:00 - 17:30 | 扩展练习

```python
# 实现一个通用菜单框架
def run_menu(title, options):
    """
    通用菜单运行器
    options: {"1": ("显示名", 函数), ...}
    """
    print(f"\n{'=' * 30}\n  {title}\n{'=' * 30}")
    for key, (name, _) in options.items():
        print(f"  {key}. {name}")
    print("  0. 退出")

    while True:
        choice = input("请选择: ").strip()
        if choice == "0":
            return
        if choice in options:
            options[choice][1]()
        else:
            print("⚠️ 无效选择")
```

---

## 🌙 晚自习（19:00 - 21:00）

### 19:00 - 20:00 | 函数设计最佳实践

1. **函数不宜过长**：超过 30 行考虑拆分
2. **参数不宜过多**：超过 5 个考虑用字典
3. **纯函数优先**：相同输入产生相同输出，无副作用
4. **先写文档字符串**：明确函数做什么

### 20:00 - 21:00 | 自习

- 完成 utils.py 工具库
- 尝试将 Day 4 待办管理器中的函数提取到独立文件
- Git 提交：`git commit -m "Day 6: 函数与代码重构"`

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | def 定义与调用函数 | |
| 2 | 参数：位置、默认、关键字 | |
| 3 | *args 和 **kwargs | |
| 4 | return 与多返回值 | |
| 5 | 局部变量与全局变量 | |
| 6 | LEGB 作用域规则 | |
| 7 | lambda 表达式 | |
| 8 | 递归基本思想 | |
| 9 | 高阶函数概念 | |
| 10 | 代码重构实践 | |

---

## 📝 课后作业

### 必做题

1. **工具函数库**：完成 `utils.py`，至少包含 8 个函数
2. **重构待办管理器**：将 Day 4 项目的功能函数提取到 `todo_functions.py`
3. **实现计算器函数**：`calculate(a, b, op)` 支持四则运算

### 选做题

4. **实现 reduce**：不用内置函数，用循环实现 `my_reduce(func, items)`
5. **柯里化**：实现 `curry_add(a)(b)(c)` 返回 `a+b+c`

---

## 💡 常见问题 FAQ

**Q1: 默认参数为什么不能用可变对象（如列表）？**

A: 默认参数在函数定义时只求值一次。`def f(lst=[])` 会导致所有调用共享同一个列表。应使用 `def f(lst=None): lst = lst or []`。

**Q2: return 和 print 有什么区别？**

A: `print` 显示给用户看；`return` 将值返回给调用者继续处理。函数间通信用 `return`。

**Q3: lambda 能替代所有函数吗？**

A: 不能。lambda 只适合单行简单表达式。复杂逻辑仍用 `def`。

**Q4: 递归会不会栈溢出？**

A: Python 默认递归深度约 1000 层。深度递归应改用循环或 `sys.setrecursionlimit()`（谨慎使用）。

**Q5: *args 和 **kwargs 的星号有什么区别？**

A: 定义时 `*args` 收集多余位置参数为元组，`**kwargs` 收集多余关键字参数为字典。调用时 `*list` 展开列表为位置参数，`**dict` 展开字典为关键字参数。

---

## 🔮 明日预习

**Day 7: 第一周复习与周测**

明天是第一周总结日：

- 知识点串讲（Day 1-6 回顾）
- 周测（笔试 + 上机）
- 综合项目：通讯录管理系统

**预习建议**：回顾本周所有项目代码，确保能独立复现。

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 6*
