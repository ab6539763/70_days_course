# Day 08:面向对象编程(上)—— 你已经用了一周的对象,今天学会自己造

---

# 【旁白解读】昨天、今天、明天

第二周开张。先恭喜:第一周的验收(周测 + 通讯录项目)你挺过来了,Python 的"生存技能"已经在手。第二周的主题是**进阶与工程化**:面向对象(Day 08-09)、模块与异常(Day 10)、文件与标准库(Day 11)、网络与 API(Day 12,首次调用大模型!)、进阶语法(Day 13),最后 Day 14 项目一验收。

**今天进入很多人闻风丧胆的"面向对象编程(OOP)"。** 先消除恐惧:你其实已经用了一整周的对象——

```python
"  hi  ".strip()        # 字符串对象,自带 strip 技能
[1, 2].append(3)        # 列表对象,自带 append 技能
{"a": 1}.get("a")       # 字典对象,自带 get 技能
```

`对象.方法()` 这个姿势你一天敲几十遍。**所谓面向对象,只是从"用别人造好的对象"进化到"自己造对象"。** Day 02 留下的悬案"为什么有的功能是函数 len(),有的是方法 .strip()?"今天正式结案。

**为什么现在学 OOP?三个正在发生的痛点:**

1. 昨天通讯录的 `contacts` 数据和操作它的六个函数"一家人分居各处",菜单里全是 `lambda: add_contact(contacts)` 这种别扭的传参——**数据和它的操作理应住在一起**;
2. Day 05 的消息是裸字典 `{"role": ..., "content": ...}`,谁都能塞进一个 `{"rloe": "usr"}`(拼错的键),没有任何防护——**数据需要"出厂规格"**;
3. 未来两周你要用的所有框架,全部是 OOP 写的:`ChatOpenAI(model="gpt-4o")` 是在造对象,`chain.invoke(...)` 是在调方法——**看不懂类,就看不懂框架文档**。

今天的路线:上午——类与对象、`__init__` 构造方法、属性与方法、self 的真身;下午——实例方法/类方法/静态方法三兄弟;实操——**定义 `ChatMessage` 类**,把 Day 05 的消息字典升级成消息对象,并重构一个 `ChatSession` 会话类(Day 14 项目一的核心类,今天出生)。明天(Day 09)继承与多态,搭出 `BaseModel → OpenAIModel / QwenModel` 的模型家族——LangChain 统一调度百家模型的秘密,明天亲手造一遍。

---

# 上午 · 第一节(9:00 - 10:30):类与对象、__init__、属性

## 1.1 类是图纸,对象是实物

```
类(class)       =  图纸/模具        "ChatMessage 类:每条消息该有什么、能干什么"
对象(object)     =  照图纸造的实物    "这一条具体的消息"(也叫"实例 instance")
造对象的动作      =  实例化           ChatMessage("user", "你好")
```

生活类比:"学员"是类(规定了每个学员都有姓名、年龄,都能签到、交作业);"张三"是对象(一个具体学员)。类只有一份,对象可以造无数个,各自独立。

最小可用的类,五行:

```python
class ChatMessage:                        # class 关键字 + 类名(大驼峰:每个单词首字母大写!)
    """一条对话消息。"""                    # 类也有 docstring

    def __init__(self, role, content):    # 构造方法:造对象时自动执行
        self.role = role                  # 把材料存到"这个对象自己"身上 → 属性
        self.content = content


# 实例化:类名 + 括号(材料递给 __init__,但不用传 self)
msg1 = ChatMessage("user", "你好")
msg2 = ChatMessage("assistant", "你好!有什么可以帮你?")

# 用点号访问属性
print(msg1.role)          # user
print(msg2.content)       # 你好!有什么可以帮你?
print(msg1.role == msg2.role)     # False —— 两个对象,各自的属性独立
```

**命名规范立刻记住**:类名用**大驼峰**(ChatMessage、OpenAIModel),函数和变量用蛇形(chat_message)——这是 Python 社区的铁律,看名字就知道是类还是函数。

## 1.2 `__init__` 与 self:两个最大的困惑点一次讲透

**`__init__`(读"因尼特",双下划线包裹)是构造方法**:实例化的瞬间自动执行,负责"给新对象做出厂设置"。你写 `ChatMessage("user", "你好")` 时,Python 幕后做了三件事:①造一个空对象;②调用 `__init__(空对象, "user", "你好")`;③把装修好的对象交给你。

**self 就是"这个对象自己"。** 它是幕后第一步造出的那个对象,Python 自动把它塞进每个方法的第一个参数:

```python
class ChatMessage:
    def __init__(self, role, content):
        # self = 正在被装修的那个新对象
        # self.role = role 的意思:"把材料 role 挂到这个对象身上,起名 role"
        # 左边的 self.role 是属性(挂在对象上,长期存在)
        # 右边的 role 是参数(方法的局部变量,方法结束就没了)
        self.role = role
        self.content = content

    def preview(self, width=10):
        # 每个方法的第一个参数都是 self:调用时 Python 自动传
        # msg.preview(5) 实际上是 ChatMessage.preview(msg, 5)
        return self.content[:width] + ("..." if len(self.content) > width else "")


msg = ChatMessage("user", "请详细介绍一下Python的字典和JSON的区别")
print(msg.preview())       # 请详细介绍一下Pyt...
print(msg.preview(4))      # 请详细介绍...
```

**self 三问(今天的头号 FAQ):**

- **为什么定义时写 self,调用时不传?** 因为 `msg.preview(5)` 只是 `ChatMessage.preview(msg, 5)` 的简写——点号左边的对象被自动填进 self。两种写法都合法,试一次就懂;
- **self 这个名字是强制的吗?** 不强制(叫 this、me 都能跑),但**全宇宙 Python 程序员都用 self**,别标新立异;
- **忘写 self 会怎样?** 今天最高频报错:`TypeError: preview() takes 1 positional argument but 2 were given`——你定义了 `def preview(width)`,调用 `msg.preview(5)` 时 Python 自动塞了 msg 进第一个位置,width 收到了 msg,5 没地方去。看到 "takes N but N+1 were given" 就检查 self。

## 1.3 对象方法操作自己的属性:数据与行为的合体

OOP 的核心红利在这里显形。对比昨天的写法:

```python
# ── 第一周的写法:数据(字典)和行为(函数)分居 ──
def format_message(msg: dict) -> str:               # 函数在这里
    return f"[{msg['role']}] {msg['content']}"

msg = {"role": "user", "content": "你好"}            # 数据在那里
print(format_message(msg))                           # 用的时候手工撮合


# ── OOP 写法:数据和行为住在一起 ──
class ChatMessage:
    """一条对话消息:数据(role/content)与行为(format/to_dict)的合体。"""

    ROLE_NAMES = {"system": "[系统]", "user": "[我]", "assistant": "[AI]"}   # 类属性:全类共享

    def __init__(self, role: str, content: str):
        self.role = role                  # 实例属性:每个对象一份
        self.content = content

    def format(self) -> str:
        """格式化显示行。方法随身携带,不用传数据——self 就是数据。"""
        label = self.ROLE_NAMES.get(self.role, "[?]")
        return f"{label} {self.content}"

    def to_dict(self) -> dict:
        """转回 API 需要的字典格式(发送给大模型前的最后一步)。"""
        return {"role": self.role, "content": self.content}


msg = ChatMessage("user", "你好")
print(msg.format())        # [我] 你好 —— 不用传参:方法自己知道自己的数据
print(msg.to_dict())       # {'role': 'user', 'content': '你好'} —— 随时能变回字典喂 API
```

注意 `ROLE_NAMES` 的位置:它定义在 `__init__` 外、直接挂在类身上,叫**类属性**——所有对象共享一份(角色对照表没必要每条消息都复制一份)。与之相对,`self.role` 是**实例属性**——每个对象自己一份。区分口诀:**"人手一份"用实例属性,"全班共用"用类属性**。

## 1.4 属性的动态性与防拼错

```python
msg = ChatMessage("user", "你好")

# Python 允许运行时随意加属性(动态语言的自由)
msg.timestamp = 1751702400        # 挂一个新属性,不报错

# 自由的代价:拼错也不报错!
msg.contnet = "改个内容"           # 手滑:contnet ≠ content
print(msg.content)                # 还是"你好"——你以为改了,其实挂了个新属性
# 这种 bug 极其阴险(不崩溃,只是悄悄不对)。
# 防护手段预告:Day 09 的 @property、Day 23 的 Pydantic(自动拒绝未知字段)。
# 今天的纪律:属性只在 __init__ 里定义,方法里只用不新增——让 IDE 能帮你补全和查错
```

---

# 上午 · 第二节(10:40 - 12:00):把通讯录装进类 —— ChatSession 的前传

用一个完整改造案例把上午的知识焊牢:昨天通讯录的"数据 + 函数分居"问题,类的解法:

```python
class ContactBook:
    """通讯录:数据(contacts)与操作(add/search/…)的合体。

    对比昨天:不再需要 lambda: add_contact(contacts) 传数据——
    数据就在 self 身上,方法伸手就拿。
    """

    def __init__(self, data_file: str = "contacts.json"):
        self.data_file = data_file
        self.contacts: list = []          # 数据住进对象:属性

    def add(self, name: str, phone: str) -> bool:
        """添加联系人;成功 True,重名 False。"""
        if any(c["name"] == name for c in self.contacts):
            return False
        self.contacts.append({"name": name, "phone": phone})
        return True

    def search(self, keyword: str) -> list:
        """关键词搜索。"""
        return [c for c in self.contacts
                if keyword in c["name"] or keyword in c["phone"]]

    def count(self) -> int:
        """联系人总数。"""
        return len(self.contacts)


book = ContactBook()                      # 造一本通讯录
book.add("张三", "13812345678")           # 不用传 contacts:它就在 book 身上
book.add("李四", "13900001111")
print(book.count())                       # 2
print(book.search("138"))                 # [{'name': '张三', ...}]

work_book = ContactBook("work.json")      # 再造一本,互不干扰——
print(work_book.count())                  # 0    对象化的另一个红利:多实例天然隔离
```

最后两行值得多看一眼:**函数版的通讯录全程只有一份全局 contacts,想同时管理"私人通讯录"和"工作通讯录"就要大改;类版造两个对象就完了。** "多实例隔离"在大模型应用里是刚需:Day 27 的多会话记忆管理(每个用户一个 session 对象)靠的就是它。

---

# 下午 · 第一节(14:00 - 15:20):方法三兄弟——实例方法、类方法、静态方法

```python
class ChatMessage:
    """演示三种方法的完整版消息类。"""

    ROLE_NAMES = {"system": "[系统]", "user": "[我]", "assistant": "[AI]"}
    VALID_ROLES = ("system", "user", "assistant")          # 类属性:合法角色表(元组:定型数据)

    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

    # ── ① 实例方法:第一个参数 self,操作"这一个对象" ──────────
    # 三兄弟里 90% 的场合用它
    def format(self) -> str:
        """格式化显示(要用到 self.role/self.content → 实例方法)。"""
        return f"{self.ROLE_NAMES.get(self.role, '[?]')} {self.content}"

    # ── ② 类方法:@classmethod 装饰,第一个参数 cls(类自己) ──
    # 主战场:"另一种造对象的方式"(工厂方法)
    @classmethod
    def from_dict(cls, data: dict) -> "ChatMessage":
        """从字典造消息对象——JSON 加载回来时用(Day 05 的逆操作)。

        cls 就是 ChatMessage 类本身;cls(...) 等于 ChatMessage(...)。
        为什么不直接写 ChatMessage(...)?明天学了继承你会看到:
        子类调用 from_dict 时,cls 自动变成子类——工厂造出来的是"对的型号"。
        """
        return cls(data["role"], data["content"])

    @classmethod
    def user(cls, content: str) -> "ChatMessage":
        """快捷工厂:造用户消息(最高频的一种,给它开专线)。"""
        return cls("user", content)

    # ── ③ 静态方法:@staticmethod 装饰,没有 self 也没有 cls ──
    # "和这个类主题相关,但不需要碰任何对象/类数据"的工具函数
    @staticmethod
    def is_valid_role(role: str) -> bool:
        """检查角色名是否合法(只看参数,不碰对象 → 静态方法)。"""
        return role in ChatMessage.VALID_ROLES


# ── 三兄弟的调用姿势 ──
msg = ChatMessage.user("你好")                       # 类方法:通过类调用,造对象
print(msg.format())                                  # 实例方法:通过对象调用

loaded = ChatMessage.from_dict({"role": "assistant", "content": "你好!"})
print(loaded.format())                               # 从字典复活的对象,一样能用

print(ChatMessage.is_valid_role("user"))             # True   静态方法:通过类调用
print(ChatMessage.is_valid_role("admin"))            # False
```

**选择心法(拿到一个方法需求先问两个问题):**

```
要用到 self.xxx(对象的数据)吗?
  ├─ 要 → 实例方法(默认选它)
  └─ 不要 → 要用到 cls(造对象/读类属性)吗?
              ├─ 要 → 类方法(典型:from_xxx 工厂)
              └─ 不要 → 静态方法(其实放类外做普通函数也行,
                         放进来只是"主题归类")
```

**@classmethod 的 from_xxx 工厂模式请重点圈起来**:Day 25 你会遇到 `ChatPromptTemplate.from_messages(...)`、`ChatOpenAI.from_env(...)` 这类调用铺天盖地——那全是类方法工厂。今天看懂了 from_dict,三周后看框架文档不用猜。

顺带补一刀 Day 02 的悬案:**为什么 len() 是函数而 strip() 是方法?** 设计取舍:len 对一切容器通用(字符串/列表/字典/集合),做成统一函数,任何新容器只要实现 `__len__`(明天讲魔术方法)就能被 len 量;strip 只对字符串有意义,做成字符串的专属方法。**通用能力做函数,专属能力做方法**——你自己设计类的时候也遵循这个直觉。

---

# 下午 · 第二节(15:30 - 17:30):实操——ChatMessage 与 ChatSession

## 4.1 需求文档

> ### 需求文档:对话核心类库 v1.0
>
> **需求编号**:REQ-D08-001
> **需求方**:「智言科技」AI 平台组
> **背景**:Day 14 将交付《命令行多轮对话 AI 助手》。平台组要求先把核心数据层做成类库(今天),再接 API(Day 12)、组装成品(Day 14)。今天交付两个类:
>
> **类 1:ChatMessage(消息)**
> - 属性:role、content;类属性:合法角色表、显示名映射;
> - 构造时校验:role 不合法直接报错(宁可造不出来,不要造出残次品);
> - 方法:`format()` 显示行;`to_dict()` 转 API 字典;`char_count()` 字符数;
> - 类方法:`from_dict(data)`;快捷工厂 `user(content)` / `assistant(content)` / `system(content)`;
> - 静态方法:`is_valid_role(role)`。
>
> **类 2:ChatSession(会话)**
> - 属性:messages(ChatMessage 对象列表)、session_name;
> - 构造时可选传入 system 设定,自动作为第一条消息;
> - 方法:`add_user(content)` / `add_assistant(content)` 追加消息;`show()` 打印全部;`to_api_format()` 返回 API 需要的字典列表;`stats()` 返回统计字典(总消息数/用户消息数/总字符);`trim(max_rounds)` 窗口截断(昨天周测上机题 3 的类版本);
> - 会话之间互相隔离(多实例)。
>
> **验收标准**:附带的 assert 测试全过;演示两个并行会话互不干扰。

## 4.2 参考实现(完整代码见 code/chat_models.py,此处讲解核心)

```python
class ChatMessage:
    """一条对话消息:大模型应用的最小数据单元。"""

    VALID_ROLES = ("system", "user", "assistant")
    ROLE_NAMES = {"system": "[系统]", "user": "[我]", "assistant": "[AI]"}

    def __init__(self, role: str, content: str):
        # 构造即校验:非法角色直接拒绝出厂。
        # raise 是"主动抛出错误"(Day 10 正式学),今天先会用这一句:
        # 它让错误暴露在"造对象"的第一现场,而不是三天后 API 报 400
        if role not in self.VALID_ROLES:
            raise ValueError(f"非法角色: {role},合法值: {self.VALID_ROLES}")
        self.role = role
        self.content = content

    def format(self) -> str:
        """带角色标签的显示行。"""
        return f"{self.ROLE_NAMES[self.role]} {self.content}"

    def to_dict(self) -> dict:
        """转 API 字典:对象世界 → JSON 世界的出口。"""
        return {"role": self.role, "content": self.content}

    def char_count(self) -> int:
        """内容字符数(token 估算的前置,Day 15 换 tiktoken)。"""
        return len(self.content)

    @classmethod
    def from_dict(cls, data: dict) -> "ChatMessage":
        """从字典复活对象:JSON 世界 → 对象世界的入口。"""
        return cls(data["role"], data["content"])

    @classmethod
    def user(cls, content: str) -> "ChatMessage":
        """快捷工厂:用户消息。"""
        return cls("user", content)

    @classmethod
    def assistant(cls, content: str) -> "ChatMessage":
        """快捷工厂:AI 消息。"""
        return cls("assistant", content)

    @classmethod
    def system(cls, content: str) -> "ChatMessage":
        """快捷工厂:系统设定。"""
        return cls("system", content)

    @staticmethod
    def is_valid_role(role: str) -> bool:
        """角色合法性检查。"""
        return role in ChatMessage.VALID_ROLES
```

```python
class ChatSession:
    """一个对话会话:消息的容器与管家。Day 14 项目一的核心类,今天出生。"""

    def __init__(self, session_name: str = "默认会话", system_prompt: str = ""):
        self.session_name = session_name
        self.messages: list = []                      # ChatMessage 对象列表
        if system_prompt:                             # 有设定就自动垫底
            self.messages.append(ChatMessage.system(system_prompt))

    def add_user(self, content: str) -> None:
        """追加用户消息。"""
        self.messages.append(ChatMessage.user(content))

    def add_assistant(self, content: str) -> None:
        """追加 AI 消息。"""
        self.messages.append(ChatMessage.assistant(content))

    def show(self) -> None:
        """打印整个会话。"""
        print(f"===== {self.session_name}({len(self.messages)} 条)=====")
        for msg in self.messages:                     # 遍历的是对象,直接调方法
            print(f"  {msg.format()}")

    def to_api_format(self) -> list:
        """转成 API 需要的字典列表——Day 12 发送前的最后一步。"""
        return [msg.to_dict() for msg in self.messages]     # 推导式 + 方法调用

    def stats(self) -> dict:
        """会话统计。"""
        user_msgs = [m for m in self.messages if m.role == "user"]
        return {
            "total": len(self.messages),
            "user": len(user_msgs),
            "chars": sum(m.char_count() for m in self.messages),
        }

    def trim(self, max_rounds: int = 3) -> None:
        """窗口截断:保 system + 最近 N 轮(昨天上机题 3 的类版本,原地修改)。"""
        if self.messages and self.messages[0].role == "system":
            head, body = self.messages[:1], self.messages[1:]
        else:
            head, body = [], self.messages
        self.messages = head + body[-max_rounds * 2:]
```

## 4.3 验收测试与多会话演示

```python
# ---- 验收:assert 测试 ----
m = ChatMessage.user("你好")
assert m.role == "user" and m.to_dict() == {"role": "user", "content": "你好"}
assert ChatMessage.from_dict({"role": "assistant", "content": "hi"}).role == "assistant"
assert ChatMessage.is_valid_role("system") and not ChatMessage.is_valid_role("admin")

try:                                       # 验证"非法角色拒绝出厂"
    ChatMessage("admin", "越权")
    assert False, "应该抛出 ValueError!"
except ValueError:
    pass                                   # 正确地被拒绝了

# ---- 多会话隔离演示 ----
work = ChatSession("工作助手", system_prompt="你是Python技术顾问")
life = ChatSession("生活助手", system_prompt="你是生活小帮手")

work.add_user("字典和JSON的区别?")
work.add_assistant("字典是内存里的活物,JSON是纸上的描述……")
life.add_user("晚饭吃什么?")

work.show()        # 3 条(system + 一问一答)
life.show()        # 2 条 —— 两个会话互不干扰:多实例隔离
print(work.stats())                        # {'total': 3, 'user': 1, 'chars': ...}
print(work.to_api_format())                # Day 12 就把这个发给 DeepSeek
```

## 4.4 收尾:看一眼三天后的未来

Day 14 项目一的主循环,用今天的类写出来长这样(**预告代码,Day 12 后全部打通**):

```python
# session = ChatSession("我的助手", system_prompt="你是乐于助人的AI")
# while True:
#     text = input("你:").strip()
#     if text == "/exit": break
#     session.add_user(text)
#     reply = call_deepseek(session.to_api_format())    # ← Day 12 的唯一缺口
#     session.add_assistant(reply)
#     print(f"AI:{reply}")
```

主循环瘦成了 7 行——所有复杂度都被 ChatSession 类消化了。**这就是 OOP 的终极卖点:复杂度不会消失,但可以被封装到看不见的地方。**

---

# 【常见错误与排错手册】Day 08 专属篇

**错误 1:`TypeError: xxx() takes 1 positional argument but 2 were given`。** 方法定义忘了 self。点号调用会自动多塞一个对象进第一个参数。

**错误 2:方法里直接写 `role` 而不是 `self.role` → NameError。** 属性必须通过 self 访问,裸名字是局部变量。反过来,`self.` 前缀写多了(给局部临时变量也加 self)会污染对象,同样要避免。

**错误 3:`__init__` 拼写错误(`__int__`、`_init_`)。** 不报错但构造方法不执行,属性全没有,用的时候 `AttributeError: 'X' object has no attribute 'role'`。双下划线、init 四个字母,逐字检查。

**错误 4:实例化忘了括号。** `msg = ChatMessage` 拿到的是**类本身**(还记得注册表模式吗——不带括号是对象本身),不是实例。后续 `msg.role` 报 AttributeError。判别:`print(msg)` 显示 `<class ...>` 就是忘了括号。

**错误 5:类属性当实例属性改,发生"分裂"。** `msg.ROLE_NAMES = {...}` 不会改类属性,而是给这个对象挂了个同名实例属性遮住类属性。改类属性要 `ChatMessage.ROLE_NAMES = ...`。原则:类属性当只读常量用,要改就明确通过类名。

**错误 6:可变类属性被全类共享出事。** 若把 `messages = []` 写成类属性,所有会话共用一个列表(Day 06 默认参数地雷的类版本)!**可变容器一律放 `__init__` 里做实例属性。** 今天 ChatSession 的写法就是标准示范。

**错误 7:`from_dict` 里忘了 return cls(...)。** 工厂不 return,调用方拿到 None。

**错误 8:类里方法之间互相调用忘了 self。** 应写 `self.add_user(...)` 而不是 `add_user(...)`——对象内部的互相调用也要经过 self 这个"自己"。

---

# 【课堂笔记】Day 08 知识点速查表

**核心概念**
- 类=图纸(class 大驼峰命名),对象/实例=实物;实例化=类名()
- `__init__`:构造方法,实例化自动执行,负责出厂设置
- self=这个对象自己;`msg.f(x)` ≡ `Class.f(msg, x)`;定义写、调用不传
- 实例属性(`self.x`,人手一份)vs 类属性(类体直接定义,全类共享)
- **可变容器必须做实例属性**(放 __init__),类属性只放常量

**方法三兄弟**
| | 装饰器 | 第一参数 | 用途 | 占比 |
|---|---|---|---|---|
| 实例方法 | 无 | self | 操作对象数据 | 90% |
| 类方法 | @classmethod | cls | from_xxx 工厂 | 9% |
| 静态方法 | @staticmethod | 无 | 主题相关的工具 | 1% |

**今日两个核心类**(Day 14 的地基)
- ChatMessage:构造即校验(raise ValueError)、to_dict/from_dict 双向门、快捷工厂 user/assistant/system
- ChatSession:messages 容器、add_user/add_assistant、to_api_format、trim 截断、多实例隔离

**设计箴言**
- 数据和操作它的行为住在一起(类的存在理由)
- 构造即校验:宁可造不出来,不造残次品
- 复杂度不消失,但可以被封装到看不见的地方
- 通用能力做函数(len),专属能力做方法(strip)

---

# 【附录】课堂答疑实录(晚自习整理)

**问 1:什么时候该写类,什么时候函数就够了?我怕以后什么都想套个类。**

答:好警惕,过度设计和不会设计一样糟。判断标准:**有没有"一份数据 + 围绕它的一组操作"要长期共存?** 有 → 类(会话+增删查、通讯录+增删改查);只是"进料加工出料"的一次性动作 → 函数(mask_phone、word_freq)。一个反向信号:如果你发现好几个函数都在传同一个参数(第一周所有函数都在传 contacts / messages / todos),那份数据就在喊"给我建个类"。另外脚本级小工具(几十行)不用类,平铺函数更清爽——类是为"活得久、会生长"的代码准备的。

**问 2:类属性 ROLE_NAMES 为什么用 self.ROLE_NAMES 也能访问?**

答:Python 找属性的顺序是"先对象自己,再找类"(再找父类,明天讲继承时补全)。self.ROLE_NAMES 在对象身上找不到,就向上去类里找到了。所以读类属性用 self 没问题,**写**才有陷阱(排错手册错误 5:会在对象上创建同名属性遮住类属性)。规范建议:读类常量时写 `self.ROLE_NAMES`(支持子类覆盖,明天见效)或 `ChatMessage.ROLE_NAMES`(强调它是类级的)都行,团队统一即可。

**问 3:to_dict/from_dict 这一对为什么这么重要?感觉只是格式转换。**

答:它们是**对象世界和数据世界的海关**。对象只活在 Python 内存里;要出境(存文件、发 API、进数据库)必须换成通用格式(字典→JSON),入境时再复活成对象。这对方法今后无处不在:Day 11 会话存档(对象→JSON 文件)、Day 12 发请求(对象→API 字典)、Day 23 的 Pydantic 模型自带 model_dump()/model_validate()(就是工业级的 to_dict/from_dict)。凡是设计"要持久化或要传输"的类,第一件事就是配这对海关。

**问 4:构造时校验 raise ValueError,程序不就崩了吗?为什么说这是好事?**

答:对比两种死法:①构造时崩——报错指向"造消息"那一行,role 拼错当场现形,五秒修好;②不校验——带病的消息静静躺在列表里,三天后发到 DeepSeek,API 返回 400 Bad Request,你从网络层开始排查两小时。**错误离出生点越近越便宜。** 当然,"崩"不等于"死给用户看"——Day 10 学 try/except 后,调用方可以优雅接住这个 ValueError 转成友好提示。raise(制造警报)和 try(处理警报)是一对,今天先学会拉响,后天学会接警。

**问 5:方法和函数,文档里说法好像混着用,到底怎么区分?**

答:方法就是"长在类里的函数",本质无区别(def 定义、参数、return 全一样),差别只在归属和调用方式(方法通过对象/类用点号调)。日常口语确实混用,不用纠结。真正要分清的是三兄弟(实例/类/静态)——看第一个参数是 self、cls 还是没有。

**问 6:今天的 ChatSession 和 Day 05 的裸字典列表比,代码变多了,值得吗?**

答:代码行数确实多了(类定义本身占地),但看三个别的指标:①**调用方代码**变少了(4.4 节的主循环 7 行);②**出错面**变小了(role 拼错出厂即拦、trim 逻辑只有一份);③**变化成本**变低了(想加时间戳字段,只改 ChatMessage 一处,所有用它的地方自动受益)。工程上叫"把复杂度搬到定义处,让使用处简单"——定义写一次,使用写百次,这笔账怎么算都赚。小脚本另说(问 1 的答案)。

**问 7:VALID_ROLES 用元组不用列表,是讲究还是习惯?**

答:讲究。三层理由:①语义——合法角色表是定型数据,元组宣告"别改我"(Day 04 的心法);②安全——真有人手滑 append 也改不动;③性能——微小但白赚。**常量集合用元组(或 frozenset)**是 Python 的通用惯例,类属性尤其如此(可变类属性是排错手册错误 6 的雷)。

**问 8:明天的继承预告里说"子类调用 from_dict 时 cls 自动变成子类",没看懂。**

答:正常,这正是明天的开场包袱。今天只需记住现象:类方法用 `cls(...)` 而不是硬编码 `ChatMessage(...)` 造对象,是给明天的继承留的活口。明天定义 `SystemMessage(ChatMessage)` 子类后,`SystemMessage.from_dict(...)` 造出来的会自动是 SystemMessage 而不是 ChatMessage——工厂"认得下单的是谁"。挖坑就是为了让你带着问题睡觉。

---

# 【明日预告】Day 09:面向对象编程(下)—— 继承、多态与魔术方法

明天解决今天留下的三个钩子:① **继承**——`BaseModel → OpenAIModel / QwenModel` 的模型家族,不同厂商的模型共享一套接口,这正是 LangChain 能"统一调用百家模型"的原理,明天亲手造;② **多态与方法重写**——同一个 `chat()` 调用,不同子类各有各的实现;super() 让子类"先照抄爸爸再加自己的";③ **魔术方法**——`__str__` 让 print(msg) 直接输出人话、`__len__` 让 len(session) 直接可用、`__call__` 让对象像函数一样被调用(LangChain 的 Runnable 就靠它);外加 @property 把方法伪装成属性(顺手解决今天"属性拼错不报错"的隐患)。今天的 ChatMessage/ChatSession 明天继续进化,别删。

**睡前自检清单**:
- [ ] 能向别人解释:类/对象/实例化/self/__init__ 五个词
- [ ] 三兄弟的选择心法能画出来(要 self 吗→要 cls 吗)
- [ ] chat_models.py 手敲运行,assert 全过,多会话演示成功
- [ ] LeetCode:LC 705(设计哈希集合——第一次用 class 刷题)、LC 1603(设计停车系统)
- [ ] 作业完成并 push,绿格子连续第 8 天
