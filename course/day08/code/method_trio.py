# =============================================
# Day 08 · 下午演示代码:方法三兄弟(实例/类/静态)
# 文件:method_trio.py
# 选择心法:要 self(对象数据)→ 实例方法;
#           要 cls(造对象/类属性)→ 类方法;
#           都不要 → 静态方法(主题归类的工具)
# =============================================


class ChatMessage:
    """演示三种方法的完整版消息类。"""

    ROLE_NAMES = {"system": "[系统]", "user": "[我]", "assistant": "[AI]"}
    VALID_ROLES = ("system", "user", "assistant")     # 常量集合用元组:定型数据

    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

    # ── ① 实例方法:第一个参数 self(90% 的场合) ──
    def format(self) -> str:
        """格式化显示(要用 self.role/self.content → 实例方法)。"""
        return f"{self.ROLE_NAMES.get(self.role, '[?]')} {self.content}"

    # ── ② 类方法:@classmethod,第一个参数 cls(类自己) ──
    @classmethod
    def from_dict(cls, data: dict) -> "ChatMessage":
        """工厂:从字典造消息对象(JSON 加载回来时用)。

        用 cls(...) 而不是硬编码 ChatMessage(...):
        明天学继承后,子类调 from_dict 时 cls 自动变成子类——
        工厂"认得下单的是谁"。
        """
        return cls(data["role"], data["content"])

    @classmethod
    def user(cls, content: str) -> "ChatMessage":
        """快捷工厂:造用户消息(最高频,开专线)。"""
        return cls("user", content)

    # ── ③ 静态方法:@staticmethod,没有 self 也没有 cls ──
    @staticmethod
    def is_valid_role(role: str) -> bool:
        """检查角色名是否合法(只看参数,不碰对象 → 静态)。"""
        return role in ChatMessage.VALID_ROLES


# ── 三兄弟的调用姿势 ──
msg = ChatMessage.user("你好")                       # 类方法:通过类调用,造对象
print(msg.format())                                  # 实例方法:通过对象调用

loaded = ChatMessage.from_dict({"role": "assistant", "content": "你好!"})
print(loaded.format())                               # 从字典复活的对象,一样能用

print(ChatMessage.is_valid_role("user"))             # True
print(ChatMessage.is_valid_role("admin"))            # False

# 【伏笔】Day 25 的 ChatPromptTemplate.from_messages(...)、
# 各类 from_env(...) 全是类方法工厂——今天看懂 from_dict,三周后不用猜文档
