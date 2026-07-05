"""chatlib 异常体系:用类型传递"该怎么办"。

家谱:
    Exception
    └── ChatLibError                 使用方一网打尽:except ChatLibError
        ├── InvalidMessageError      消息构造不合法
        └── APIError                 API 调用错误
            ├── RateLimitError       限流:可等待后重试
            └── AuthError            认证失败:重试无用,查 Key

单独成模块的站位理由:messages.py 和 models.py 都要 import 它,
把公共依赖抽到第三个模块,消灭循环导入的可能。
"""


class ChatLibError(Exception):
    """chatlib 所有异常的基类。"""


class InvalidMessageError(ChatLibError):
    """消息构造不合法(role 非法/内容为空)。"""


class APIError(ChatLibError):
    """API 调用错误的基类。"""


class RateLimitError(APIError):
    """限流:可等待后重试。"""


class AuthError(APIError):
    """认证失败:重试无用,请检查 API Key。"""
