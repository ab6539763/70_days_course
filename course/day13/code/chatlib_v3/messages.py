"""消息与会话:Day 08-09 成果迁入包内 + 异常体系接轨。"""
import json

from chatlib_v3.exceptions import InvalidMessageError


class ChatMessage:
    """一条对话消息。构造校验改抛 InvalidMessageError(接轨异常家谱)。"""

    VALID_ROLES = ("system", "user", "assistant")
    ROLE_NAMES = {"system": "[系统]", "user": "[我]", "assistant": "[AI]"}

    def __init__(self, role: str, content: str):
        if role not in self.VALID_ROLES:
            raise InvalidMessageError(f"非法角色: {role},合法值: {self.VALID_ROLES}")
        if not str(content).strip():
            raise InvalidMessageError("消息内容不能为空")
        self.role = role
        self.content = content

    def __str__(self) -> str:
        return f"{self.ROLE_NAMES[self.role]} {self.content}"

    def __repr__(self) -> str:
        return f"ChatMessage({self.role!r}, {self.content!r})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, ChatMessage):
            return NotImplemented
        return self.role == other.role and self.content == other.content

    def to_dict(self) -> dict:
        """对象 → API 字典。"""
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
    """会话:消息容器与管家(容器协议 + 存档)。"""

    def __init__(self, session_name: str = "默认会话", system_prompt: str = ""):
        self.session_name = session_name
        self.messages: list = []
        if system_prompt:
            self.messages.append(ChatMessage.system(system_prompt))

    def __len__(self) -> int:
        return len(self.messages)

    def __getitem__(self, index):
        return self.messages[index]

    def __contains__(self, keyword: str) -> bool:
        return any(keyword in m.content for m in self.messages)

    def __repr__(self) -> str:
        return f"ChatSession({self.session_name!r}, {len(self)} msgs)"

    def add_user(self, content: str) -> None:
        """追加用户消息。"""
        self.messages.append(ChatMessage.user(content))

    def add_assistant(self, content: str) -> None:
        """追加 AI 消息。"""
        self.messages.append(ChatMessage.assistant(content))

    def show(self) -> None:
        """打印整个会话。"""
        print(f"===== {self.session_name}({len(self)} 条)=====")
        for msg in self.messages:
            print(f"  {msg}")

    def to_api_format(self) -> list:
        """对象列表 → API 字典列表。"""
        return [m.to_dict() for m in self.messages]

    def trim(self, max_rounds: int = 3) -> None:
        """窗口截断:保 system + 最近 N 轮。"""
        if self.messages and self.messages[0].role == "system":
            head, body = self.messages[:1], self.messages[1:]
        else:
            head, body = [], self.messages
        self.messages = head + body[-max_rounds * 2:]

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
        """从存档复活会话:文件不存在/JSON 损坏分路处理(Day 10 的多路 except)。"""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"(存档 {filename} 不存在,新建空会话)")
            return cls("新会话")
        except json.JSONDecodeError as e:
            print(f"(存档已损坏:第 {e.lineno} 行 {e.msg},新建空会话)")
            return cls("新会话")
        session = cls(data.get("session_name", "已恢复会话"))
        session.messages = [ChatMessage.from_dict(d) for d in data.get("messages", [])]
        return session


if __name__ == "__main__":
    # 模块自测:只有直接运行本文件才执行(__name__ 谜底的实战)
    m = ChatMessage.user("你好")
    assert m.to_dict() == {"role": "user", "content": "你好"}
    try:
        ChatMessage("admin", "越权")
        assert False
    except InvalidMessageError:
        pass
    try:
        ChatMessage("user", "   ")
        assert False
    except InvalidMessageError:
        pass
    s = ChatSession("自测", system_prompt="你是助教")
    s.add_user("问")
    s.add_assistant("答")
    assert len(s) == 3 and "问" in s
    print("messages.py 自测通过")
