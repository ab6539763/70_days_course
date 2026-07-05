"""chatlib:课程自研对话类库(Day 10 出生,Day 14 服役,Day 25 交棒 LangChain)。

__init__.py 的门面作用:转口常用成员,使用方一行拿到所有主角:
    from chatlib import ChatMessage, ChatSession, DeepSeekModel
"""
from chatlib.exceptions import (
    ChatLibError,
    APIError,
    RateLimitError,
    AuthError,
    InvalidMessageError,
)
from chatlib.messages import ChatMessage, ChatSession
from chatlib.models import BaseChatModel, DeepSeekModel, FakeModel

__all__ = [
    "ChatLibError", "APIError", "RateLimitError", "AuthError", "InvalidMessageError",
    "ChatMessage", "ChatSession",
    "BaseChatModel", "DeepSeekModel", "FakeModel",
]
