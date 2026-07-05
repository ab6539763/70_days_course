# =============================================
# Day 09 作业 · 编程题 1:消息家族(类型即角色)
# 这就是 LangChain SystemMessage/HumanMessage/AIMessage 的同构版,
# Day 25 见面时你已经亲手造过它
# =============================================


class BaseMessage:
    """消息基类:role 由子类的类属性决定——类型即角色。"""

    role: str = None                       # 类属性占位:子类必须覆盖

    def __init__(self, content: str):
        if self.role is None:              # 直接实例化基类:拒绝
            raise NotImplementedError("请使用具体的消息子类")
        self.content = content

    def __str__(self) -> str:
        return f"[{self.role}] {self.content}"

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.content!r})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, BaseMessage):
            return NotImplemented
        return self.role == other.role and self.content == other.content

    def to_dict(self) -> dict:
        """API 海关:role 从类属性来。"""
        return {"role": self.role, "content": self.content}


class SystemMessage(BaseMessage):
    """系统设定消息。"""
    role = "system"


class UserMessage(BaseMessage):
    """用户消息。"""
    role = "user"


class AIMessage(BaseMessage):
    """AI 回复消息。"""
    role = "assistant"


# ---- assert 测试 ----
m = UserMessage("你好")                    # 只传 content:类型即角色
assert m.role == "user"
assert m.to_dict() == {"role": "user", "content": "你好"}
assert str(SystemMessage("设定")) == "[system] 设定"
assert UserMessage("a") == UserMessage("a")
assert UserMessage("a") != AIMessage("a")          # 内容同、角色异:不等
assert repr(AIMessage("hi")) == "AIMessage('hi')"

try:
    BaseMessage("裸基类")                  # 基类禁止直接实例化
    assert False
except NotImplementedError:
    pass
print("✓ 消息家族全部测试通过")

# 收获:role 从"运行时参数"(可能拼错)变成"类型本身"
# (拼错类名直接 NameError,错误提前到写代码时)——
# 用类型系统消灭一类运行时错误,这是继承的高级用法
