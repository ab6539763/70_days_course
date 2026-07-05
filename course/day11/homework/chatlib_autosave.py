# =============================================
# Day 11 作业 · 编程题 4:chatlib 会话自动存档 + 带时间戳的消息
# 暗桩:timestamp 默认值若写 datetime.now().isoformat() 就踩 Day 06 地雷
#      (定义时求值一次,所有消息同一时间)——用 None + or 现生成绕开
# 兼容:旧存档没有 timestamp 字段也能 load(get 默认 None → 现生成)
# =============================================
import json
from datetime import datetime
from pathlib import Path


class ChatMessage:
    """带时间戳的消息(向后兼容旧存档)。"""

    VALID_ROLES = ("system", "user", "assistant")

    def __init__(self, role: str, content: str, timestamp: str = None):
        if role not in self.VALID_ROLES:
            raise ValueError(f"非法角色: {role}")
        self.role = role
        self.content = content
        # ⚠️ 不能写 timestamp: str = datetime.now().isoformat()——
        # 默认值在定义时求值一次,所有消息会共享同一个时间(Day 06 地雷的时间版)
        self.timestamp = timestamp or datetime.now().isoformat(timespec="seconds")

    def to_dict(self) -> dict:
        return {"role": self.role, "content": self.content, "timestamp": self.timestamp}

    @classmethod
    def from_dict(cls, data: dict) -> "ChatMessage":
        # get 默认 None → __init__ 里现生成:旧存档(无 timestamp)兼容!
        return cls(data["role"], data["content"], data.get("timestamp"))


class ChatSession:
    """会话:新增 autosave 自动存档。"""

    def __init__(self, session_name: str = "默认会话"):
        self.session_name = session_name
        self.messages: list = []

    def add_user(self, content: str) -> None:
        self.messages.append(ChatMessage("user", content))

    def add_assistant(self, content: str) -> None:
        self.messages.append(ChatMessage("assistant", content))

    def autosave(self, dirname: str = "sessions") -> str:
        """自动存档:会话名_时间戳.json,返回路径。"""
        d = Path(dirname)
        d.mkdir(exist_ok=True)
        name = f"{self.session_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path = d / name
        data = {
            "session_name": self.session_name,
            "messages": [m.to_dict() for m in self.messages],
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return str(path)

    @classmethod
    def load(cls, filename: str) -> "ChatSession":
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        s = cls(data.get("session_name", "已恢复"))
        s.messages = [ChatMessage.from_dict(d) for d in data.get("messages", [])]
        return s


if __name__ == "__main__":
    import time

    # ---- 测试 1:每条消息时间戳独立(地雷未踩的证明) ----
    s = ChatSession("测试会话")
    s.add_user("第一条")
    time.sleep(1.1)
    s.add_user("第二条")
    assert s.messages[0].timestamp != s.messages[1].timestamp    # 时间不同!
    print("✓ 时间戳独立(Day 06 地雷已绕开)")

    # ---- 测试 2:自动存档与恢复 ----
    path = s.autosave()
    restored = ChatSession.load(path)
    assert len(restored.messages) == 2
    assert restored.messages[0].timestamp == s.messages[0].timestamp
    print(f"✓ 自动存档往返无损:{path}")

    # ---- 测试 3:向后兼容——旧格式(无 timestamp)也能 load ----
    old_format = {
        "session_name": "旧存档",
        "messages": [{"role": "user", "content": "老消息"}],     # 没有 timestamp!
    }
    with open("old_session.json", "w", encoding="utf-8") as f:
        json.dump(old_format, f, ensure_ascii=False)
    old = ChatSession.load("old_session.json")
    assert old.messages[0].timestamp                   # 自动补上了当前时间
    print("✓ 旧存档向后兼容(Day 08 思考题 2 的实践)")

    # 打扫现场
    import os
    import shutil
    os.remove("old_session.json")
    shutil.rmtree("sessions")
