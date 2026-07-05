"""模型层:Day 09 成果迁入包内 + 穿上异常铠甲。"""
from chatlib.exceptions import APIError, AuthError, RateLimitError


class BaseChatModel:
    """模型基类:统一接口 + 共同实现。"""

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
        """记录一次调用(内部方法)。"""
        self._call_count += 1
        self._total_tokens += tokens

    def count_usage(self) -> dict:
        """用量统计。"""
        return {"calls": self._call_count, "tokens": self._total_tokens}

    def __repr__(self) -> str:
        return f"{type(self).__name__}(model_name={self.model_name!r}, temperature={self.temperature})"


class DeepSeekModel(BaseChatModel):
    """DeepSeek 模型:带异常铠甲的模拟版(Day 12 换真网络调用,铠甲直接沿用)。"""

    def __init__(self, model_name: str = "deepseek-chat", temperature: float = 0.7,
                 api_base: str = "https://api.deepseek.com"):
        super().__init__(model_name, temperature)
        self.api_base = api_base

    def chat(self, messages: list) -> str:
        """带铠甲的 chat:错误二分法的实战。

        - 空 messages:编程错误 → 直接 raise ValueError,该崩就崩(军规一);
        - 网络异常:环境错误 → 捕获并转译成 APIError 上抛(带 from e)。
        """
        if not messages:
            raise ValueError("messages 不能为空")
        try:
            reply = self._do_request(messages)      # 可能出事的只有这行(军规三)
        except ConnectionError as e:
            raise APIError(f"网络异常,请稍后重试: {e}") from e
        return reply

    def _do_request(self, messages: list) -> str:
        """模拟网络请求(Day 12 换成 requests 真调用,方法名和职责不变)。"""
        last = messages[-1]["content"]
        self._record(tokens=len(last) * 2)
        return f"(DeepSeek@{self.api_base})关于「{last[:10]}」的回答是……"


class FakeModel(BaseChatModel):
    """测试替身:可注入失败模式,为 Day 13 测试重试逻辑服务。

    fail_times=2 表示前两次调用抛 RateLimitError,之后恢复正常——
    可控地模拟"不稳定的外部世界"。
    """

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
        return "这是测试回答。"


if __name__ == "__main__":
    # 模块自测
    m = DeepSeekModel()
    reply = m.chat([{"role": "user", "content": "自测"}])
    assert "DeepSeek" in reply

    try:
        m.chat([])                          # 空消息:编程错误,应崩
        assert False
    except ValueError:
        pass

    flaky = FakeModel(fail_times=2)
    fails = 0
    for _ in range(3):
        try:
            flaky.chat([{"role": "user", "content": "hi"}])
        except RateLimitError:
            fails += 1
    assert fails == 2                       # 前两次失败,第三次成功
    print("models.py 自测通过")
