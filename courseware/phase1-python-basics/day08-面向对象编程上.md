# Day 8: 面向对象编程（上）

> **培训阶段**: 第一阶段 Python 编程基础 | **第 2 周** | **学习时长**: 约 6-8 小时  
> **今日关键词**: 类与对象、__init__、属性、方法、ChatMessage 类

---

## 📍 课程导航

### 上节回顾
**Day 7** 是第一周总结日，你完成了知识串讲、周测和「通讯录管理系统」综合项目。联系人用字典存储——今天将学习 **面向对象编程（OOP）**，用**类**来更优雅地组织数据和行为。

### 本节学习目标
完成本日学习后，你将能够：

1. 理解类与对象的概念及其与字典的区别
2. 使用 `class` 定义类，`__init__` 初始化对象
3. 定义和调用实例方法与属性
4. 创建 `ChatMessage` 类为大模型消息建模
5. 理解 OOP 在大模型开发中的应用场景

### 与后续课程的衔接
- **Day 9** 将学习继承、多态、魔术方法，构建 `BaseModel → OpenAIModel/QwenModel` 体系
- **Day 12** API 调用中的消息对象将用类管理
- **Day 25+** RAG 开发中的 Document、Chunk 类都基于今天的 OOP 基础

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：类与对象

#### 1.1 为什么需要类？

```python
# 用字典存储联系人（Day 7 的方式）
contact = {
    "name": "张三",
    "phone": "13800138000",
    "email": "zhangsan@example.com",
}

# 问题：数据和行为分离，容易出错
contact["name"] = 123  # 没有类型约束
# contact.greet()  # 字典没有方法
```

```python
# 用类存储联系人（OOP 方式）
class Contact:
    def __init__(self, name, phone, email=""):
        self.name = name
        self.phone = phone
        self.email = email

    def greet(self):
        return f"你好，我是 {self.name}，电话 {self.phone}"

    def is_valid(self):
        return bool(self.name and self.phone)

# 创建对象（实例化）
c = Contact("张三", "13800138000", "zhangsan@example.com")
print(c.greet())
print(c.is_valid())  # True
```

#### 1.2 核心概念

| 概念 | 说明 | 示例 |
|------|------|------|
| 类 (class) | 对象的模板/蓝图 | `class Contact:` |
| 对象/实例 (object/instance) | 类的具体实例 | `c = Contact(...)` |
| 属性 (attribute) | 对象的数据 | `self.name` |
| 方法 (method) | 对象的行为 | `def greet(self):` |
| `self` | 指向当前实例 | 方法的第一个参数 |

#### 1.3 定义第一个类

```python
# day08/first_class.py

class Dog:
    """狗的类"""

    def __init__(self, name, breed):
        """构造方法：创建对象时自动调用"""
        self.name = name
        self.breed = breed
        self.energy = 100

    def bark(self):
        """实例方法"""
        return f"{self.name} 说：汪汪！"

    def play(self):
        self.energy -= 20
        return f"{self.name} 在玩耍，剩余体力 {self.energy}"

# 创建对象
dog1 = Dog("旺财", "柴犬")
dog2 = Dog("来福", "金毛")

print(dog1.bark())   # 旺财 说：汪汪！
print(dog2.bark())   # 来福 说：汪汪！
print(dog1.play())   # 旺财 在玩耍，剩余体力 80
```

#### 1.4 类属性 vs 实例属性

```python
# day08/class_vs_instance.py

class Student:
    school = "AI 大学"  # 类属性：所有实例共享

    def __init__(self, name, score):
        self.name = name      # 实例属性：每个实例独有
        self.score = score

s1 = Student("张三", 90)
s2 = Student("李四", 85)

print(s1.school)  # AI 大学
print(s2.school)  # AI 大学
Student.school = "LLM 学院"
print(s1.school)  # LLM 学院（类属性被修改，所有实例同步）
```

---

### 9:45 - 10:30 | 模块二：方法与属性深入

#### 2.1 实例方法、类方法、静态方法

```python
# day08/methods.py

class Calculator:
    pi = 3.14159

    def __init__(self, name):
        self.name = name
        self.history = []

    def add(self, a, b):
        """实例方法：需要 self，可访问实例属性"""
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result

    @classmethod
    def circle_area(cls, radius):
        """类方法：接收 cls，可访问类属性"""
        return cls.pi * radius ** 2

    @staticmethod
    def is_positive(n):
        """静态方法：不需要 self 或 cls"""
        return n > 0

calc = Calculator("我的计算器")
print(calc.add(3, 5))                    # 8
print(Calculator.circle_area(5))         # 78.53975
print(Calculator.is_positive(-3))        # False
```

#### 2.2 属性访问控制

```python
# day08/encapsulation.py

class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance  # 单下划线：约定"内部使用"

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self._balance:
            self._balance -= amount
            return True
        return False

    def get_balance(self):
        return self._balance

account = BankAccount("张三", 1000)
account.deposit(500)
account.withdraw(200)
print(f"余额: {account.get_balance()}")  # 1300
```

#### 2.3 __str__ 与 __repr__

```python
# day08/string_methods.py

class Book:
    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price

    def __str__(self):
        """用户友好的字符串表示（print 时调用）"""
        return f"《{self.title}》 - {self.author}"

    def __repr__(self):
        """开发者友好的表示（调试时调用）"""
        return f"Book('{self.title}', '{self.author}', {self.price})"

book = Book("Python 编程", "张三", 59.9)
print(book)        # 《Python 编程》 - 张三
print(repr(book))  # Book('Python 编程', '张三', 59.9)
```

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：ChatMessage 类

#### 3.1 大模型消息的数据模型

在大模型 API 中，每条消息包含 `role` 和 `content`：

```json
{"role": "user", "content": "你好"}
{"role": "assistant", "content": "你好！有什么可以帮你的？"}
{"role": "system", "content": "你是一个有帮助的助手。"}
```

今天用类来建模这种结构。

#### 3.2 ChatMessage 类实现

```python
# day08/chat_message.py
from datetime import datetime

class ChatMessage:
    """大模型对话消息类"""

    VALID_ROLES = ("system", "user", "assistant")

    def __init__(self, role, content, timestamp=None):
        if role not in self.VALID_ROLES:
            raise ValueError(f"无效角色: {role}，必须是 {self.VALID_ROLES}")
        self.role = role
        self.content = content
        self.timestamp = timestamp or datetime.now()
        self.token_count = len(content) // 2  # 简单估算

    def to_dict(self):
        """转为 API 请求格式的字典"""
        return {"role": self.role, "content": self.content}

    def display(self):
        """美观显示消息"""
        icons = {"system": "⚙️", "user": "👤", "assistant": "🤖"}
        icon = icons.get(self.role, "❓")
        time_str = self.timestamp.strftime("%H:%M:%S")
        return f"[{time_str}] {icon} {self.role}: {self.content}"

    def __str__(self):
        return self.display()

    def __repr__(self):
        return f"ChatMessage('{self.role}', '{self.content[:20]}...')"

    @classmethod
    def from_dict(cls, data):
        """从字典创建消息对象"""
        return cls(role=data["role"], content=data["content"])

    @classmethod
    def system(cls, content):
        """快捷创建系统消息"""
        return cls("system", content)

    @classmethod
    def user(cls, content):
        """快捷创建用户消息"""
        return cls("user", content)

    @classmethod
    def assistant(cls, content):
        """快捷创建助手消息"""
        return cls("assistant", content)


# 使用示例
msg1 = ChatMessage.user("什么是 Python？")
msg2 = ChatMessage.assistant("Python 是一种高级编程语言。")
msg3 = ChatMessage.system("你是一个 Python 导师。")

print(msg1)
print(msg2)

# 转为 API 格式
api_messages = [msg.to_dict() for msg in [msg3, msg1, msg2]]
print(api_messages)
```

#### 3.3 Conversation 类（对话管理）

```python
# day08/conversation.py

class Conversation:
    """对话管理类"""

    def __init__(self, system_prompt=None):
        self.messages = []
        if system_prompt:
            self.messages.append(ChatMessage.system(system_prompt))

    def add_user_message(self, content):
        self.messages.append(ChatMessage.user(content))

    def add_assistant_message(self, content):
        self.messages.append(ChatMessage.assistant(content))

    def get_api_messages(self):
        """获取 API 请求格式的消息列表"""
        return [msg.to_dict() for msg in self.messages]

    def total_tokens(self):
        return sum(msg.token_count for msg in self.messages)

    def display_history(self):
        print(f"\n💬 对话历史 ({len(self.messages)} 条消息)")
        print("-" * 50)
        for msg in self.messages:
            print(msg)
        print(f"📊 估算 tokens: {self.total_tokens()}")
        print("-" * 50)

    def clear(self):
        system_msgs = [m for m in self.messages if m.role == "system"]
        self.messages = system_msgs


# 使用
conv = Conversation("你是一个有帮助的 AI 助手。")
conv.add_user_message("你好！")
conv.add_assistant_message("你好！有什么可以帮你的吗？")
conv.add_user_message("介绍一下 Python")
conv.display_history()
```

---

## 🌇 下午实操（14:00 - 17:30）

### 14:00 - 17:00 | 实操项目：OOP 版通讯录

#### 项目需求

用面向对象方式重构 Day 7 的通讯录：
1. `Contact` 类：封装联系人数据和方法
2. `AddressBook` 类：管理所有联系人
3. 保留原有的增删改查、搜索、JSON 导入导出功能

#### 参考代码

创建文件 `day08/address_book_oop.py`：

```python
"""
Day 8 实操项目：OOP 版通讯录
"""

import json
from datetime import datetime


class Contact:
    """联系人类"""

    def __init__(self, name, phone, email="", group="未分组"):
        self.name = name
        self.phone = phone
        self.email = email
        self.group = group
        self.created = datetime.now().strftime("%Y-%m-%d %H:%M")

    def update(self, **kwargs):
        """更新联系人信息"""
        for key, value in kwargs.items():
            if value and hasattr(self, key):
                setattr(self, key, value)

    def to_dict(self):
        return {
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "group": self.group,
            "created": self.created,
        }

    @classmethod
    def from_dict(cls, data):
        c = cls(data["name"], data["phone"], data.get("email", ""), data.get("group", "未分组"))
        c.created = data.get("created", c.created)
        return c

    def __str__(self):
        return f"{self.name} | {self.phone} | {self.email} | {self.group}"


class AddressBook:
    """通讯录管理类"""

    def __init__(self):
        self.contacts = []

    def add(self, contact):
        self.contacts.append(contact)
        print(f"✅ 已添加: {contact.name}")

    def remove(self, name):
        for i, c in enumerate(self.contacts):
            if c.name == name:
                removed = self.contacts.pop(i)
                print(f"🗑️ 已删除: {removed.name}")
                return True
        print(f"⚠️ 未找到: {name}")
        return False

    def find(self, keyword):
        keyword = keyword.lower()
        return [c for c in self.contacts
                if keyword in c.name.lower() or keyword in c.phone]

    def list_all(self):
        if not self.contacts:
            print("📭 通讯录为空")
            return
        print(f"\n📒 通讯录 ({len(self.contacts)} 人)")
        for i, c in enumerate(self.contacts, 1):
            print(f"  {i}. {c}")

    def export_json(self, filename):
        data = [c.to_dict() for c in self.contacts]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ 已导出到 {filename}")

    def import_json(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.contacts = [Contact.from_dict(d) for d in data]
        print(f"✅ 已导入 {len(self.contacts)} 个联系人")

    def __len__(self):
        return len(self.contacts)


def main():
    book = AddressBook()

    while True:
        print("\n1.添加  2.查看  3.搜索  4.删除  5.导出  6.导入  0.退出")
        choice = input("请选择: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            name = input("姓名: ").strip()
            phone = input("电话: ").strip()
            email = input("邮箱: ").strip()
            group = input("分组: ").strip()
            book.add(Contact(name, phone, email, group or "未分组"))
        elif choice == "2":
            book.list_all()
        elif choice == "3":
            kw = input("搜索: ").strip()
            results = book.find(kw)
            for c in results:
                print(f"  → {c}")
        elif choice == "4":
            name = input("删除姓名: ").strip()
            book.remove(name)
        elif choice == "5":
            book.export_json("day08/contacts.json")
        elif choice == "6":
            book.import_json(input("文件名: ").strip())
        else:
            print("⚠️ 无效选择")


if __name__ == "__main__":
    main()
```

---

### 17:00 - 17:30 | 扩展练习

```python
# 比较 OOP vs 字典方式
# 字典：灵活但无约束
d = {"name": 123}  # 名字可以是数字，没有报错

# 类：可以在 __init__ 中验证
class Contact:
    def __init__(self, name, phone):
        if not isinstance(name, str) or not name:
            raise ValueError("姓名必须是非空字符串")
        self.name = name
        self.phone = phone
```

---

## 🌙 晚自习（19:00 - 21:00）

- 完成 OOP 版通讯录
- 实现 `ChatMessage` 和 `Conversation` 类并测试
- Git 提交：`git commit -m "Day 8: 面向对象编程与ChatMessage"`

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | 类与对象的概念 | |
| 2 | __init__ 构造方法 | |
| 3 | self 参数 | |
| 4 | 实例方法与属性 | |
| 5 | 类方法 @classmethod | |
| 6 | __str__ 与 __repr__ | |
| 7 | ChatMessage 类 | |
| 8 | Conversation 类 | |
| 9 | OOP 版通讯录项目 | |

---

## 📝 课后作业

### 必做题

1. 完成 `ChatMessage` 和 `Conversation` 类
2. 完成 OOP 版通讯录
3. 为 `Contact` 类添加 `__eq__` 方法，支持按姓名比较

### 选做题

4. 实现 `TodoItem` 类，重构 Day 4 待办管理器
5. 为 `ChatMessage` 添加 `edit()` 方法修改内容

---

## 💡 常见问题 FAQ

**Q1: self 是什么？能不能改名？**

A: `self` 代表当前实例，可以改名但不推荐。约定俗成用 `self`。

**Q2: 类和字典什么时候用哪个？**

A: 简单数据用字典；需要方法和数据验证时用类。大模型开发中消息、文档等用类。

**Q3: __init__ 是构造函数吗？**

A: 严格说 Python 的 `__new__` 才是构造，`__init__` 是初始化。日常可以认为 `__init__` 是构造。

---

## 🔮 明日预习

**Day 9: 面向对象编程（下）** — 继承、多态、魔术方法、`BaseModel → OpenAIModel/QwenModel`

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 8*
