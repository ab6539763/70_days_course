"""chatlib 异常体系(与 Day 10 相同,为本日独立运行复制)。"""


class ChatLibError(Exception):
    """chatlib 所有异常的基类。"""


class InvalidMessageError(ChatLibError):
    """消息构造不合法。"""


class APIError(ChatLibError):
    """API 调用错误的基类。"""


class RateLimitError(APIError):
    """限流:可等待后重试。"""


class AuthError(APIError):
    """认证失败:重试无用,请检查 API Key。"""
