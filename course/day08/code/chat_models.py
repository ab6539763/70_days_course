# =============================================
# 对话核心类库 v1.0(Day 08 实操成果)
# 需求编号:REQ-D08-001
# ChatMessage:消息类(构造即校验 + 双向海关 + 快捷工厂)
# ChatSession:会话类(Day 14 项目一的核心类,今天出生)
# 明天(Day 09)将在此基础上加继承、魔术方法、@property——别删!
# =============================================


class ChatMessage:
    """一条对话消息:大模型应用的最小数据单元。"""

    VALID_ROLES = ("system", "user", "assistant")
    ROLE_NAMES = {"system": "[系统]", "user": "[我]", "assistant": "[AI]"}

    def __init__(self, role: str, content: str):
        # 构造即校验:非法角色直接拒绝出厂。
        # raise 主动抛错(Day 10 正式学):让错误暴露在"造对象"的第一现场,
        # 而不是三天后 API 报 400 才从网络层开始排查
        if role not in self.VALID_ROLES:
            raise ValueError(f"非法角色: {role},合法值: {self.VALID_ROLES}")
        self.role = role
        self.content = content

    def format(self) -> str:
        """带角色标签的显示行。"""
        return f"{self.ROLE_NAMES[self.role]} {self.content}"

    def to_dict(self) -> dict:
        """转 API 字典:对象世界 → JSON 世界的出口(海关)。"""
        return {"role": self.role, "content": self.content}

    def char_count(self) -> int:
        """内容字符数(token 估算的前置,Day 15 换 tiktoken)。"""
        return len(self.content)

    @classmethod
    def from_dict(cls, data: dict) -> "ChatMessage":
        """从字典复活对象:JSON 世界 → 对象世界的入口(海关)。"""
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


class ChatSession:
    """一个对话会话:消息的容器与管家。"""

    def __init__(self, session_name: str = "默认会话", system_prompt: str = ""):
        self.session_name = session_name
        self.messages: list = []                      # 可变容器 → 实例属性(铁律)
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
        for msg in self.messages:                     # 遍历对象,直接调方法
            print(f"  {msg.format()}")

    def to_api_format(self) -> list:
        """转成 API 需要的字典列表——Day 12 发送前的最后一步。"""
        return [msg.to_dict() for msg in self.messages]

    def stats(self) -> dict:
        """会话统计:总消息/用户消息/总字符。"""
        user_msgs = [m for m in self.messages if m.role == "user"]
        return {
            "total": len(self.messages),
            "user": len(user_msgs),
            "chars": sum(m.char_count() for m in self.messages),
        }

    def trim(self, max_rounds: int = 3) -> None:
        """窗口截断:保 system + 最近 N 轮(Day 07 上机题 3 的类版本)。"""
        if self.messages and self.messages[0].role == "system":
            head, body = self.messages[:1], self.messages[1:]
        else:
            head, body = [], self.messages
        self.messages = head + body[-max_rounds * 2:]


# ──────────────── 验收测试 ────────────────

def run_tests() -> None:
    """需求验收:assert 全过 + 多会话隔离演示。"""
    # ChatMessage 测试
    m = ChatMessage.user("你好")
    assert m.role == "user" and m.to_dict() == {"role": "user", "content": "你好"}
    assert ChatMessage.from_dict({"role": "assistant", "content": "hi"}).role == "assistant"
    assert ChatMessage.is_valid_role("system") and not ChatMessage.is_valid_role("admin")
    assert m.char_count() == 2

    # 验证"非法角色拒绝出厂"
    try:
        ChatMessage("admin", "越权")
        assert False, "应该抛出 ValueError!"
    except ValueError:
        pass                                   # 正确地被拒绝了

    # ChatSession 测试
    s = ChatSession("测试", system_prompt="你是助教")
    s.add_user("问1")
    s.add_assistant("答1")
    assert s.stats()["total"] == 3 and s.stats()["user"] == 1
    assert s.to_api_format()[0] == {"role": "system", "content": "你是助教"}

    # trim 测试:5 轮截成 2 轮
    for i in range(4):
        s.add_user(f"问{i+2}")
        s.add_assistant(f"答{i+2}")
    s.trim(max_rounds=2)
    assert len(s.messages) == 5                # 1 system + 2 轮 × 2
    assert s.messages[0].role == "system"

    print("✓ 全部验收测试通过")


def demo() -> None:
    """多会话隔离演示。"""
    work = ChatSession("工作助手", system_prompt="你是Python技术顾问")
    life = ChatSession("生活助手", system_prompt="你是生活小帮手")

    work.add_user("字典和JSON的区别?")
    work.add_assistant("字典是内存里的活物,JSON是纸上的描述……")
    life.add_user("晚饭吃什么?")

    work.show()        # 3 条
    life.show()        # 2 条 —— 互不干扰:多实例隔离
    print(work.stats())
    print(work.to_api_format())               # Day 12 就把这个发给 DeepSeek


if __name__ == "__main__":
    run_tests()
    demo()
