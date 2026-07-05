# =============================================
# Day 08 作业 · 编程题 4:ChatSession 加会话存档
# 直通 Day 14:"对话历史保存为 JSON"的完整预制件
# 结构:{"session_name": ..., "messages": [{...}, ...]}
# =============================================
import json


class ChatMessage:
    """消息类(与课堂 chat_models.py 相同,为独立运行复制于此)。"""

    VALID_ROLES = ("system", "user", "assistant")
    ROLE_NAMES = {"system": "[系统]", "user": "[我]", "assistant": "[AI]"}

    def __init__(self, role: str, content: str):
        if role not in self.VALID_ROLES:
            raise ValueError(f"非法角色: {role}")
        self.role = role
        self.content = content

    def format(self) -> str:
        """带角色标签的显示行。"""
        return f"{self.ROLE_NAMES[self.role]} {self.content}"

    def to_dict(self) -> dict:
        """对象 → 字典。"""
        return {"role": self.role, "content": self.content}

    @classmethod
    def from_dict(cls, data: dict) -> "ChatMessage":
        """字典 → 对象。"""
        return cls(data["role"], data["content"])

    @classmethod
    def user(cls, content: str) -> "ChatMessage":
        return cls("user", content)

    @classmethod
    def assistant(cls, content: str) -> "ChatMessage":
        return cls("assistant", content)

    @classmethod
    def system(cls, content: str) -> "ChatMessage":
        return cls("system", content)


class ChatSession:
    """会话类:本次作业新增 save/load 存档能力。"""

    def __init__(self, session_name: str = "默认会话", system_prompt: str = ""):
        self.session_name = session_name
        self.messages: list = []
        if system_prompt:
            self.messages.append(ChatMessage.system(system_prompt))

    def add_user(self, content: str) -> None:
        self.messages.append(ChatMessage.user(content))

    def add_assistant(self, content: str) -> None:
        self.messages.append(ChatMessage.assistant(content))

    def save(self, filename: str) -> None:
        """会话存档:嵌套结构——外层会话信息,内层消息列表。"""
        data = {
            "session_name": self.session_name,
            "messages": [m.to_dict() for m in self.messages],   # 逐个过海关
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, filename: str) -> "ChatSession":
        """从存档复活会话。get 给默认值:兼容旧格式(思考题 2 的实践)。"""
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        session = cls(data.get("session_name", "已恢复会话"))
        session.messages = [ChatMessage.from_dict(d) for d in data.get("messages", [])]
        return session


# ---- 测试:存档 → 复活 → 验证无损 ----
if __name__ == "__main__":
    s = ChatSession("周末学习", system_prompt="你是Python助教")
    s.add_user("什么是类方法?")
    s.add_assistant("类方法是第一个参数为 cls 的方法,常用作工厂……")

    s.save("session_test.json")
    restored = ChatSession.load("session_test.json")

    assert restored.session_name == "周末学习"
    assert len(restored.messages) == 3
    assert restored.messages[0].role == "system"
    assert restored.messages[1].content == "什么是类方法?"
    print("✓ 会话存档往返无损,Day 14 的 /save 指令预制件就绪")
