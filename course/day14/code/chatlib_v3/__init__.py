"""chatlib v3:项目一战备版(Day 13 三件套武装完成)。

三件套:@retry 指数退避重试 | dotenv 配置管理 | timeout 参数化。
"""
from chatlib_v3.exceptions import (
    ChatLibError, APIError, RateLimitError, AuthError, InvalidMessageError,
)
from chatlib_v3.messages import ChatMessage, ChatSession
from chatlib_v3.models import BaseChatModel, DeepSeekModel, FakeModel
from chatlib_v3.utils import retry, Message, Messages

__all__ = [
    "ChatLibError", "APIError", "RateLimitError", "AuthError", "InvalidMessageError",
    "ChatMessage", "ChatSession",
    "BaseChatModel", "DeepSeekModel", "FakeModel",
    "retry", "Message", "Messages",
]
