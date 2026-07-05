"""模型层 v3:三件套武装完成(@retry + timeout 参数化 + 类型注解)。

对比 v2 的变化:
  1. chat 戴上 @retry(白名单:RateLimitError/APIError;AuthError 不重试);
  2. timeout 成为构造参数(默认 60);
  3. 全面使用 Messages 类型别名。
"""
import os

import requests

from chatlib_v3.exceptions import APIError, AuthError, RateLimitError
from chatlib_v3.utils import retry, Messages


class BaseChatModel:
    """模型基类。"""

    def __init__(self, model_name: str, temperature: float = 0.7):
        self.model_name = model_name
        self.temperature = temperature
        self._call_count = 0
        self._total_tokens = 0

    @property
    def temperature(self) -> float:
        """采样温度(0~2)。"""
        return self._temperature

    @temperature.setter
    def temperature(self, value: float) -> None:
        if not (0 <= value <= 2):
            raise ValueError(f"temperature 必须在 0~2 之间,收到 {value}")
        self._temperature = value

    def chat(self, messages: Messages) -> str:
        """发送消息列表,返回回答。子类必须重写。"""
        raise NotImplementedError(f"{type(self).__name__} 必须实现 chat()")

    def _record(self, tokens: int) -> None:
        """记录一次调用。"""
        self._call_count += 1
        self._total_tokens += tokens

    def count_usage(self) -> dict:
        """用量统计。"""
        return {"calls": self._call_count, "tokens": self._total_tokens}

    def __repr__(self) -> str:
        return f"{type(self).__name__}(model_name={self.model_name!r}, temperature={self.temperature})"


class DeepSeekModel(BaseChatModel):
    """DeepSeek 模型:项目一战备版。"""

    API_URL = "https://api.deepseek.com/chat/completions"

    def __init__(self, model_name: str = "deepseek-chat", temperature: float = 0.7,
                 api_key: str | None = None, timeout: int = 60):
        super().__init__(model_name, temperature)
        # Key 优先级:显式参数 > 环境变量(load_dotenv 已把 .env 注入环境变量)
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY", "")
        self.timeout = timeout                       # 超时参数化:压测/慢网可调
        if not self.api_key:
            raise AuthError("未提供 API Key(参数 / DEEPSEEK_API_KEY 环境变量 / .env)")

    @retry(max_retries=3, retry_on=(RateLimitError, APIError), base_delay=1.0)
    def chat(self, messages: Messages) -> str:
        """带自动重试的对话调用。

        AuthError 不在白名单:重试无用,第一次抛出即上抛;
        ValueError(空 messages)同理——白名单机制天然保护了"该崩的崩"。
        装饰器装在 chat(稳定接口)而不是 _do_request(易变实现)上:
        子类重写 _do_request(如 Day 24 流式版)时重试能力自动覆盖。
        """
        if not messages:
            raise ValueError("messages 不能为空")
        return self._do_request(messages)

    def _do_request(self, messages: Messages) -> str:
        """真实网络请求(与 v2 相同,timeout 改用实例属性)。"""
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": self.temperature,
            "stream": False,
        }
        try:
            resp = requests.post(
                self.API_URL,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=payload,
                timeout=self.timeout,
            )
        except requests.Timeout as e:
            raise APIError("请求超时") from e
        except requests.ConnectionError as e:
            raise APIError("网络连接失败") from e

        if resp.status_code == 401:
            raise AuthError("API Key 无效,请检查")
        if resp.status_code == 429:
            raise RateLimitError("触发限流,请稍后重试")
        if resp.status_code != 200:
            raise APIError(f"API 返回 {resp.status_code}: {resp.text[:200]}")

        data = resp.json()
        usage = data.get("usage", {})
        self._record(tokens=usage.get("total_tokens", 0))
        return data["choices"][0]["message"]["content"]


class FakeModel(BaseChatModel):
    """测试替身(与 v2 相同)。"""

    def __init__(self, model_name: str = "fake", temperature: float = 0.7,
                 fail_times: int = 0):
        super().__init__(model_name, temperature)
        self.fail_times = fail_times
        self._failed = 0

    def chat(self, messages: Messages) -> str:
        if not messages:
            raise ValueError("messages 不能为空")
        if self._failed < self.fail_times:
            self._failed += 1
            raise RateLimitError(f"模拟限流(第 {self._failed} 次失败)")
        self._record(tokens=0)
        last = messages[-1]["content"]
        return f"[假回答] 已收到你的问题:{last[:20]}"
