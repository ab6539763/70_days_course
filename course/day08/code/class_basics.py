# =============================================
# Day 08 · 上午演示代码:类与对象、__init__、属性、self
# 文件:class_basics.py
# =============================================


# ---- 1. 最小可用的类 ----
class ChatMessageV1:                       # class + 大驼峰命名
    """一条对话消息(最小版)。"""

    def __init__(self, role, content):    # 构造方法:造对象时自动执行
        self.role = role                  # 把材料挂到"这个对象自己"身上 → 属性
        self.content = content


msg1 = ChatMessageV1("user", "你好")                       # 实例化:类名+括号
msg2 = ChatMessageV1("assistant", "你好!有什么可以帮你?")
print(msg1.role)                  # user
print(msg2.content)               # 两个对象属性独立
print(msg1.role == msg2.role)     # False


# ---- 2. self 的真身:msg.f(x) ≡ Class.f(msg, x) ----
class ChatMessageV2:
    """加上方法的版本。"""

    def __init__(self, role, content):
        self.role = role
        self.content = content

    def preview(self, width=10):
        """内容预览:方法自己知道自己的数据(self)。"""
        return self.content[:width] + ("..." if len(self.content) > width else "")


msg = ChatMessageV2("user", "请详细介绍一下Python的字典和JSON的区别")
print(msg.preview())                            # 简写调用
print(ChatMessageV2.preview(msg, 4))            # 完整形态:两者等价!看懂这行,self 就懂了


# ---- 3. 数据与行为的合体 + 类属性 vs 实例属性 ----
class ChatMessage:
    """一条对话消息:数据(role/content)与行为(format/to_dict)的合体。"""

    ROLE_NAMES = {"system": "[系统]", "user": "[我]", "assistant": "[AI]"}   # 类属性:全类共享

    def __init__(self, role: str, content: str):
        self.role = role                  # 实例属性:每个对象一份
        self.content = content

    def format(self) -> str:
        """格式化显示行:不用传数据,self 就是数据。"""
        label = self.ROLE_NAMES.get(self.role, "[?]")
        return f"{label} {self.content}"

    def to_dict(self) -> dict:
        """转回 API 需要的字典格式。"""
        return {"role": self.role, "content": self.content}


m = ChatMessage("user", "你好")
print(m.format())                 # [我] 你好
print(m.to_dict())                # {'role': 'user', 'content': '你好'}

# 区分口诀:"人手一份"用实例属性,"全班共用"用类属性
# ⚠️ 可变容器(列表/字典)必须做实例属性,类属性只放常量——
#    否则所有对象共享一个容器(Day 06 默认参数地雷的类版本)


# ---- 4. 动态属性的自由与代价 ----
m.timestamp = 1751702400          # 运行时随意加属性:不报错
m.contnet = "手滑拼错"             # 拼错也不报错!挂了个新属性,content 纹丝不动
print(m.content)                  # 还是"你好"——阴险的静默 bug
# 纪律:属性只在 __init__ 里定义,方法里只用不新增
# 防护预告:Day 09 @property、Day 23 Pydantic(拒绝未知字段)


# ---- 5. 把通讯录装进类:昨天痛点的解法 ----
class ContactBook:
    """通讯录:数据与操作的合体;多实例天然隔离。"""

    def __init__(self, data_file: str = "contacts.json"):
        self.data_file = data_file
        self.contacts: list = []          # 可变容器 → 实例属性(标准示范)

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


book = ContactBook()
book.add("张三", "13812345678")           # 不用传 contacts:数据就在 book 身上
book.add("李四", "13900001111")
print(book.count())                       # 2
print(book.search("138"))

work_book = ContactBook("work.json")      # 再造一本,互不干扰
print(work_book.count())                  # 0 —— 多实例隔离:Day 27 多会话管理的基石
