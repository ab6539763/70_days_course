# =============================================
# Day 09 作业 · 编程题 4:ChatSession 完全体
# Day 08 的会话类 + 今天的魔术方法 + @property
# 这是 Day 14 项目一将直接使用的最终形态
# =============================================
import json


class ChatMessage:
    """消息类(自带魔术方法版)。"""

    VALID_ROLES = ("system", "user", "assistant")

    def __init__(self, role: str, content: str):
        if role not in self.VALID_ROLES:
            raise ValueError(f"非法角色: {role}")
        self.role = role
        self.content = content

    def __str__(self) -> str:
        return f"[{self.role}] {self.content}"

    def __repr__(self) -> str:
        return f"ChatMessage({self.role!r}, {self.content!r})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, ChatMessage):
            return NotImplemented
        return self.role == other.role and self.content == other.content

    def to_dict(self) -> dict:
        return {"role": self.role, "content": self.content}

    @classmethod
    def from_dict(cls, data: dict) -> "ChatMessage":
        return cls(data["role"], data["content"])


class ChatSession:
    """会话完全体:容器协议 + property 安检 + 计算属性 + 存档。"""

    def __init__(self, session_name: str = "默认会话", system_prompt: str = ""):
        self.session_name = session_name           # 走 setter:出生即安检
        self.messages: list = []
        if system_prompt:
            self.messages.append(ChatMessage("system", system_prompt))

    # ── property 安检 ──
    @property
    def session_name(self) -> str:
        """会话名。"""
        return self._session_name

    @session_name.setter
    def session_name(self, value: str) -> None:
        if not value.strip():
            raise ValueError("会话名不能为空")
        self._session_name = value.strip()

    # ── 计算属性 ──
    @property
    def last_reply(self) -> str:
        """最后一条 AI 回复(没有则空串)——Day 14 显示'AI 正在说'的取数口。"""
        for m in reversed(self.messages):       # 从后往前找,找到即停
            if m.role == "assistant":
                return m.content
        return ""

    # ── 容器协议 ──
    def __len__(self) -> int:
        return len(self.messages)

    def __getitem__(self, index):
        return self.messages[index]

    def __contains__(self, keyword: str) -> bool:
        return any(keyword in m.content for m in self.messages)

    def __repr__(self) -> str:
        return f"ChatSession({self.session_name!r}, {len(self)} msgs)"

    # ── 业务方法 ──
    def add_user(self, content: str) -> None:
        """追加用户消息。"""
        self.messages.append(ChatMessage("user", content))

    def add_assistant(self, content: str) -> None:
        """追加 AI 消息。"""
        self.messages.append(ChatMessage("assistant", content))

    def to_api_format(self) -> list:
        """API 海关:对象列表 → 字典列表。"""
        return [m.to_dict() for m in self.messages]

    # ── 存档(Day 08 作业的能力) ──
    def save(self, filename: str) -> None:
        """会话存档。"""
        data = {
            "session_name": self.session_name,
            "messages": [m.to_dict() for m in self.messages],
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, filename: str) -> "ChatSession":
        """从存档复活会话。"""
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        session = cls(data.get("session_name", "已恢复会话"))
        session.messages = [ChatMessage.from_dict(d) for d in data.get("messages", [])]
        return session


# ---- assert 测试 ----
if __name__ == "__main__":
    s = ChatSession("完全体测试", system_prompt="你是助教")
    s.add_user("什么是多态?")
    s.add_assistant("多态是同一接口各自表述……")

    assert len(s) == 3                             # __len__
    assert "多态" in s                              # __contains__
    assert s[-1].role == "assistant"                # __getitem__
    assert s.last_reply == "多态是同一接口各自表述……"   # 计算属性
    assert repr(s) == "ChatSession('完全体测试', 3 msgs)"

    try:
        s.session_name = "  "                       # 空名:setter 拦截
        assert False
    except ValueError:
        pass

    empty = ChatSession("空会话")
    assert empty.last_reply == ""                   # 没有 AI 消息:空串

    print("✓ ChatSession 完全体全部测试通过,Day 14 就绪")
