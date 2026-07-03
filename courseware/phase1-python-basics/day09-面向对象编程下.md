# Day 9: 面向对象编程（下）

> **培训阶段**: 第一阶段 Python 编程基础 | **第 2 周** | **学习时长**: 约 6-8 小时  
> **今日关键词**: 继承、多态、魔术方法、BaseModel、OpenAIModel、QwenModel

---

## 📍 课程导航

### 上节回顾
在 **Day 8** 中，你学习了类与对象、`__init__` 构造方法，创建了 `ChatMessage` 和 `Conversation` 类。今天将学习 OOP 的进阶特性——**继承与多态**，并构建大模型 API 调用的类体系。

### 本节学习目标
完成本日学习后，你将能够：

1. 使用继承复用和扩展父类功能
2. 理解多态的概念和实际应用
3. 掌握常用魔术方法（`__len__`、`__getitem__`、`__eq__` 等）
4. 构建 `BaseModel → OpenAIModel / QwenModel` 类层次
5. 理解这种设计模式在大模型开发中的价值

### 与后续课程的衔接
- **Day 12** 将用 requests 真正调用 API——今天的 Model 类是抽象层
- **Day 39+** Agent 开发中的 Tool 类也使用继承体系
- 整个课程的多模型支持都基于今天的多态设计

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：继承

#### 1.1 基本概念

```python
# day09/inheritance.py

class Animal:
    """动物基类"""
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "某种声音"

    def info(self):
        return f"动物: {self.name}"


class Dog(Animal):
    """狗：继承自动物"""
    def speak(self):
        return f"{self.name} 说：汪汪！"

    def fetch(self):
        return f"{self.name} 在捡球"


class Cat(Animal):
    """猫：继承自动物"""
    def speak(self):
        return f"{self.name} 说：喵喵！"

dog = Dog("旺财")
cat = Cat("咪咪")

print(dog.info())    # 动物: 旺财（继承自父类）
print(dog.speak())   # 旺财 说：汪汪！（子类重写）
print(dog.fetch())   # 旺财 在捡球（子类特有）
print(cat.speak())   # 咪咪 说：喵喵！
```

#### 1.2 super() 调用父类

```python
# day09/super_demo.py

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        return f"我是 {self.name}，{self.age} 岁"


class Student(Person):
    def __init__(self, name, age, student_id):
        super().__init__(name, age)  # 调用父类构造
        self.student_id = student_id

    def introduce(self):
        base = super().introduce()  # 调用父类方法
        return f"{base}，学号 {self.student_id}"

s = Student("张三", 20, "2024001")
print(s.introduce())
# 我是 张三，20 岁，学号 2024001
```

#### 1.3 方法重写 (Override)

```python
class Shape:
    def area(self):
        raise NotImplementedError("子类必须实现 area()")

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2

shapes = [Rectangle(3, 4), Circle(5)]
for s in shapes:
    print(f"面积: {s.area()}")  # 多态：同一接口，不同实现
```

---

### 9:45 - 10:30 | 模块二：多态

#### 2.1 多态的概念

**多态**：同一接口，不同实现。调用者不需要知道具体类型。

```python
# day09/polymorphism.py

class LLMProvider:
    """大模型提供商基类"""
    def chat(self, messages):
        raise NotImplementedError

    def get_model_name(self):
        raise NotImplementedError


class DeepSeekProvider(LLMProvider):
    def __init__(self, api_key):
        self.api_key = api_key

    def chat(self, messages):
        return f"[DeepSeek 回复] 收到 {len(messages)} 条消息"

    def get_model_name(self):
        return "deepseek-chat"


class QwenProvider(LLMProvider):
    def __init__(self, api_key):
        self.api_key = api_key

    def chat(self, messages):
        return f"[通义千问 回复] 收到 {len(messages)} 条消息"

    def get_model_name(self):
        return "qwen-plus"


# 多态：统一接口调用不同实现
def ask_ai(provider: LLMProvider, question):
    messages = [{"role": "user", "content": question}]
    print(f"使用模型: {provider.get_model_name()}")
    return provider.chat(messages)

# 切换模型只需换 provider 对象
providers = [
    DeepSeekProvider("sk-xxx"),
    QwenProvider("sk-yyy"),
]

for p in providers:
    print(ask_ai(p, "什么是 Python？"))
```

#### 2.2 isinstance 与类型检查

```python
def process(obj):
    if isinstance(obj, LLMProvider):
        return obj.chat([{"role": "user", "content": "hi"}])
    elif isinstance(obj, str):
        return f"收到字符串: {obj}"
    return "未知类型"
```

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：魔术方法与 Model 类体系

#### 3.1 常用魔术方法

```python
# day09/magic_methods.py

class MessageList:
    """消息列表：演示魔术方法"""

    def __init__(self):
        self._messages = []

    def add(self, msg):
        self._messages.append(msg)

    def __len__(self):
        """len(obj) 时调用"""
        return len(self._messages)

    def __getitem__(self, index):
        """obj[index] 时调用"""
        return self._messages[index]

    def __contains__(self, item):
        """item in obj 时调用"""
        return item in self._messages

    def __iter__(self):
        """for item in obj 时调用"""
        return iter(self._messages)

    def __str__(self):
        return f"MessageList({len(self)} 条消息)"

    def __repr__(self):
        return f"MessageList({self._messages!r})"

    def __eq__(self, other):
        """obj == other 时调用"""
        if isinstance(other, MessageList):
            return self._messages == other._messages
        return False

msgs = MessageList()
msgs.add("hello")
msgs.add("world")
print(len(msgs))       # 2
print(msgs[0])       # hello
print("hello" in msgs)  # True
for m in msgs:
    print(m)
```

| 魔术方法 | 触发方式 | 用途 |
|----------|----------|------|
| `__init__` | `obj = Class()` | 初始化 |
| `__str__` | `print(obj)` / `str(obj)` | 用户友好显示 |
| `__repr__` | `repr(obj)` / 交互式显示 | 调试显示 |
| `__len__` | `len(obj)` | 返回长度 |
| `__getitem__` | `obj[key]` | 索引访问 |
| `__eq__` | `obj == other` | 相等比较 |
| `__iter__` | `for x in obj` | 迭代 |

#### 3.2 BaseModel 类体系

```python
# day09/model_classes.py
import json
from abc import ABC, abstractmethod

class BaseModel(ABC):
    """大模型基类"""

    def __init__(self, api_key, model_name, base_url):
        self.api_key = api_key
        self.model_name = model_name
        self.base_url = base_url
        self.total_tokens = 0

    @abstractmethod
    def chat(self, messages, temperature=0.7, max_tokens=2048):
        """发送对话请求（子类必须实现）"""
        pass

    def build_request_body(self, messages, temperature, max_tokens):
        """构建请求体（通用逻辑）"""
        return {
            "model": self.model_name,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

    def parse_response(self, response_data):
        """解析响应（通用逻辑）"""
        content = response_data["choices"][0]["message"]["content"]
        usage = response_data.get("usage", {})
        self.total_tokens += usage.get("total_tokens", 0)
        return content

    def get_stats(self):
        return {
            "model": self.model_name,
            "total_tokens": self.total_tokens,
        }

    def __str__(self):
        return f"{self.__class__.__name__}({self.model_name})"


class OpenAIModel(BaseModel):
    """OpenAI 兼容 API 模型"""

    def __init__(self, api_key, model_name="gpt-4o", base_url="https://api.openai.com/v1"):
        super().__init__(api_key, model_name, base_url)

    def chat(self, messages, temperature=0.7, max_tokens=2048):
        body = self.build_request_body(messages, temperature, max_tokens)
        # Day 12 会用 requests 真正发送
        print(f"[模拟] POST {self.base_url}/chat/completions")
        print(f"[模拟] 请求体: {json.dumps(body, ensure_ascii=False)[:100]}...")
        # 模拟响应
        mock_response = {
            "choices": [{"message": {"content": f"[{self.model_name}] 模拟回复"}}],
            "usage": {"total_tokens": 50},
        }
        return self.parse_response(mock_response)


class QwenModel(BaseModel):
    """通义千问模型"""

    def __init__(self, api_key, model_name="qwen-plus",
                 base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"):
        super().__init__(api_key, model_name, base_url)

    def chat(self, messages, temperature=0.7, max_tokens=2048):
        body = self.build_request_body(messages, temperature, max_tokens)
        print(f"[模拟] POST {self.base_url}/chat/completions")
        mock_response = {
            "choices": [{"message": {"content": f"[{self.model_name}] 通义千问回复"}}],
            "usage": {"total_tokens": 40},
        }
        return self.parse_response(mock_response)


class DeepSeekModel(BaseModel):
    """DeepSeek 模型"""

    def __init__(self, api_key, model_name="deepseek-chat",
                 base_url="https://api.deepseek.com"):
        super().__init__(api_key, model_name, base_url)

    def chat(self, messages, temperature=0.7, max_tokens=2048):
        body = self.build_request_body(messages, temperature, max_tokens)
        print(f"[模拟] POST {self.base_url}/chat/completions")
        mock_response = {
            "choices": [{"message": {"content": f"[{self.model_name}] DeepSeek 回复"}}],
            "usage": {"total_tokens": 35},
        }
        return self.parse_response(mock_response)


# 使用示例
def demo():
    models = [
        DeepSeekModel("sk-test"),
        QwenModel("sk-test"),
        OpenAIModel("sk-test"),
    ]

    messages = [{"role": "user", "content": "你好"}]

    for model in models:
        print(f"\n--- {model} ---")
        reply = model.chat(messages)
        print(f"回复: {reply}")
        print(f"统计: {model.get_stats()}")

# demo()
```

---

## 🌇 下午实操（14:00 - 17:30）

### 14:00 - 17:00 | 实操项目：多模型对话演示

#### 项目需求

1. 实现 `BaseModel`、`DeepSeekModel`、`QwenModel` 三个类
2. 支持运行时切换模型
3. 记录每个模型的调用统计
4. 用 `ChatMessage`（Day 8）管理消息

#### 参考代码

创建文件 `day09/multi_model_chat.py`：

```python
"""
Day 9 实操项目：多模型对话演示
"""

import json
from abc import ABC, abstractmethod


class ChatMessage:
    def __init__(self, role, content):
        self.role = role
        self.content = content

    def to_dict(self):
        return {"role": self.role, "content": self.content}


class BaseModel(ABC):
    def __init__(self, name, model_id):
        self.name = name
        self.model_id = model_id
        self.call_count = 0
        self.total_tokens = 0

    @abstractmethod
    def chat(self, messages):
        pass

    def get_stats(self):
        return {"name": self.name, "calls": self.call_count, "tokens": self.total_tokens}


class DeepSeekModel(BaseModel):
    def __init__(self):
        super().__init__("DeepSeek", "deepseek-chat")

    def chat(self, messages):
        self.call_count += 1
        tokens = sum(len(m["content"]) for m in messages) // 2 + 30
        self.total_tokens += tokens
        return f"[DeepSeek] 收到您的问题，这是一个模拟回复。（约 {tokens} tokens）"


class QwenModel(BaseModel):
    def __init__(self):
        super().__init__("通义千问", "qwen-plus")

    def chat(self, messages):
        self.call_count += 1
        tokens = sum(len(m["content"]) for m in messages) // 2 + 25
        self.total_tokens += tokens
        return f"[通义千问] 您好！这是来自通义千问的模拟回复。（约 {tokens} tokens）"


class ChatApp:
    """多模型对话应用"""

    def __init__(self):
        self.models = {
            "1": DeepSeekModel(),
            "2": QwenModel(),
        }
        self.current_model = self.models["1"]
        self.messages = []

    def switch_model(self, key):
        if key in self.models:
            self.current_model = self.models[key]
            print(f"✅ 已切换到 {self.current_model.name}")
        else:
            print("⚠️ 无效选择")

    def send_message(self, content):
        self.messages.append(ChatMessage("user", content).to_dict())
        reply = self.current_model.chat(self.messages)
        self.messages.append(ChatMessage("assistant", reply).to_dict())
        return reply

    def show_stats(self):
        print("\n📊 模型调用统计")
        for m in self.models.values():
            stats = m.get_stats()
            current = " ← 当前" if m == self.current_model else ""
            print(f"  {stats['name']}: 调用 {stats['calls']} 次, tokens {stats['tokens']}{current}")

    def run(self):
        print("=" * 40)
        print("   🤖 多模型对话演示")
        print("=" * 40)

        while True:
            print(f"\n当前模型: {self.current_model.name}")
            print("1.发送消息  2.切换模型  3.查看统计  4.查看历史  0.退出")
            choice = input("请选择: ").strip()

            if choice == "0":
                break
            elif choice == "1":
                msg = input("你: ").strip()
                if msg:
                    reply = self.send_message(msg)
                    print(f"AI: {reply}")
            elif choice == "2":
                print("  1. DeepSeek  2. 通义千问")
                self.switch_model(input("选择: ").strip())
            elif choice == "3":
                self.show_stats()
            elif choice == "4":
                for m in self.messages:
                    print(f"  [{m['role']}]: {m['content'][:60]}")
            else:
                print("⚠️ 无效选择")


if __name__ == "__main__":
    ChatApp().run()
```

---

### 17:00 - 17:30 | 扩展：抽象基类

```python
from abc import ABC, abstractmethod

class BaseTool(ABC):
    @abstractmethod
    def run(self, input_text):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

# 不能实例化抽象类
# tool = BaseTool()  # TypeError!
```

---

## 🌙 晚自习（19:00 - 21:00）

- 完成多模型对话演示项目
- 为 `BaseModel` 添加 `stream_chat()` 抽象方法（预习流式输出）
- Git 提交：`git commit -m "Day 9: 继承多态与Model类体系"`

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | 继承与 super() | |
| 2 | 方法重写 (Override) | |
| 3 | 多态概念与应用 | |
| 4 | 魔术方法 __len__/__getitem__/__eq__ | |
| 5 | 抽象基类 ABC | |
| 6 | BaseModel 类设计 | |
| 7 | OpenAIModel / QwenModel 实现 | |
| 8 | 多模型对话演示项目 | |

---

## 📝 课后作业

### 必做题

1. 完成多模型对话演示项目
2. 添加第三个模型类 `GLMModel`
3. 实现 `MessageList` 类的完整魔术方法

### 选做题

4. 实现模型工厂 `ModelFactory.create("deepseek")` 返回对应实例
5. 为 `BaseModel` 添加请求日志功能

---

## 💡 常见问题 FAQ

**Q1: 继承 vs 组合怎么选？**

A: "是一个"用继承（Dog 是 Animal）；"有一个"用组合（Car 有 Engine）。模型类适合继承。

**Q2: 为什么用 ABC 抽象基类？**

A: 强制子类实现 `chat()` 方法，避免忘记实现关键接口。

**Q3: Python 支持多继承吗？**

A: 支持，但初学者建议单继承。多重继承涉及 MRO（方法解析顺序），较复杂。

---

## 🔮 明日预习

**Day 10: 模块包与异常处理** — import、try/except、venv、pip、requirements.txt

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 9*
