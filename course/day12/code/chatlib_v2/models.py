"""模型层 v2:DeepSeekModel 换上真引擎(Day 12 的核心升级)。

对比 Day 09/10:只动了 _do_request 的内部(模拟 → requests 真调用),
chat 的签名、BaseChatModel、FakeModel、所有调用方——一个字没动。
这就是"接口纹丝不动"的兑现:架构设计的复利第一次变现。
"""
import os

import requests

from chatlib_v2.exceptions import APIError, AuthError, RateLimitError


class BaseChatModel:
    """模型基类(与 Day 10 相同)。"""

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

    def chat(self, messages: list) -> str:
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
    """DeepSeek 模型:今天起是真引擎。"""

    API_URL = "https://api.deepseek.com/chat/completions"

    def __init__(self, model_name: str = "deepseek-chat", temperature: float = 0.7,
                 api_key: str = None):
        super().__init__(model_name, temperature)
        # Key 来源顺序:参数显式传入 > 环境变量(Day 13 会插入 .env 一层)
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY", "")
        if not self.api_key:
            raise AuthError("未提供 API Key(参数或 DEEPSEEK_API_KEY 环境变量)")

    def chat(self, messages: list) -> str:
        """对外接口:与 Day 09 一字不差。"""
        if not messages:
            raise ValueError("messages 不能为空")       # 编程错误:该崩就崩
        return self._do_request(messages)

    def _do_request(self, messages: list) -> str:
        """真实网络请求:Day 09 的模拟代码退役,方法名和职责不变。"""
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
                timeout=60,                              # 大模型接口给足 60 秒
            )
        except requests.Timeout as e:
            raise APIError("请求超时") from e            # 转译 + from e(Day 10)
        except requests.ConnectionError as e:
            raise APIError("网络连接失败") from e

        # 状态码分诊:对应 Day 10 的异常家谱(当时凭空设计,今天对上原型)
        if resp.status_code == 401:
            raise AuthError("API Key 无效,请检查")
        if resp.status_code == 429:
            raise RateLimitError("触发限流,请稍后重试")
        if resp.status_code != 200:
            raise APIError(f"API 返回 {resp.status_code}: {resp.text[:200]}")

        data = resp.json()
        usage = data.get("usage", {})                    # 可选字段:get 防御
        self._record(tokens=usage.get("total_tokens", 0))    # 真实用量记账!
        return data["choices"][0]["message"]["content"]  # 第一名句(Day 05)


class FakeModel(BaseChatModel):
    """测试替身:开发调试用,不花钱(与 Day 10 相同)。"""

    def __init__(self, model_name: str = "fake", temperature: float = 0.7,
                 fail_times: int = 0):
        super().__init__(model_name, temperature)
        self.fail_times = fail_times
        self._failed = 0

    def chat(self, messages: list) -> str:
        if not messages:
            raise ValueError("messages 不能为空")
        if self._failed < self.fail_times:
            self._failed += 1
            raise RateLimitError(f"模拟限流(第 {self._failed} 次失败)")
        self._record(tokens=0)
        last = messages[-1]["content"]
        return f"[假回答] 已收到你的问题:{last[:20]}"
