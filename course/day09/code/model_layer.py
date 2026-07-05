# =============================================
# 可插拔模型层 v1.0(Day 09 实操成果)
# 需求编号:REQ-D09-001
# 架构:BaseChatModel(接口+共同实现)
#       → DeepSeekModel / OpenAIModel / QwenModel / FakeModel
# 这是 LangChain BaseChatModel → ChatOpenAI/ChatTongyi 的同构简化版。
# 未来时间线:Day 12 子类接真 API(接口不变)| Day 13 加重试与 .env
#            | Day 14 项目一投产 | Day 25 与 LangChain 相认
# =============================================


class BaseChatModel:
    """模型基类:统一接口 + 共同实现。"""

    def __init__(self, model_name: str, temperature: float = 0.7):
        self.model_name = model_name
        self.temperature = temperature        # 这行赋值走 setter:安检从出生起生效
        self._call_count = 0                  # 内部计数:单下划线,外人别碰
        self._total_tokens = 0

    # ── temperature:property + setter,范围安检 ──
    @property
    def temperature(self) -> float:
        """采样温度(0~2)。"""
        return self._temperature

    @temperature.setter
    def temperature(self, value: float) -> None:
        if not (0 <= value <= 2):
            raise ValueError(f"temperature 必须在 0~2 之间,收到 {value}")
        self._temperature = value             # 存储属性带下划线:防无限递归

    # ── 接口:子类必须实现 ──
    def chat(self, messages: list) -> str:
        """发送消息列表,返回回答。子类必须重写。"""
        raise NotImplementedError(f"{type(self).__name__} 必须实现 chat()")

    # ── 通用实现:所有子类白拿 ──
    def _record(self, tokens: int) -> None:
        """记录一次调用(内部方法:子类的 chat 里调用)。"""
        self._call_count += 1
        self._total_tokens += tokens

    def count_usage(self) -> dict:
        """用量统计。"""
        return {"calls": self._call_count, "tokens": self._total_tokens}

    def __repr__(self) -> str:
        return f"{type(self).__name__}(model_name={self.model_name!r}, temperature={self.temperature})"

    @classmethod
    def from_config(cls, config: dict) -> "BaseChatModel":
        """配置字典 → 模型实例。cls 保证造出'下单的那个子类'。"""
        return cls(config["model_name"], config.get("temperature", 0.7))


class DeepSeekModel(BaseChatModel):
    """DeepSeek:课程主力模型(Day 12 起接真 API)。"""

    def __init__(self, model_name: str = "deepseek-chat", temperature: float = 0.7,
                 api_base: str = "https://api.deepseek.com"):
        super().__init__(model_name, temperature)     # 老三样让爸爸装
        self.api_base = api_base                      # 自己的新属性自己装

    def chat(self, messages: list) -> str:
        """模拟 DeepSeek 风格回答(Day 12 换成 requests 真调用,接口不变!)。"""
        last = messages[-1]["content"] if messages else ""
        self._record(tokens=len(last) * 2)            # 模拟用量:复用父类记账
        return f"(DeepSeek@{self.api_base})关于「{last[:10]}」的回答是……"


class OpenAIModel(BaseChatModel):
    """OpenAI 系模型。"""

    def chat(self, messages: list) -> str:
        """模拟 OpenAI 风格回答。"""
        last = messages[-1]["content"] if messages else ""
        self._record(tokens=len(last) * 2)
        return f"[GPT:{self.model_name}] Here is my answer to '{last[:10]}'..."


class QwenModel(BaseChatModel):
    """通义千问系模型。"""

    def chat(self, messages: list) -> str:
        """模拟通义风格回答。"""
        last = messages[-1]["content"] if messages else ""
        self._record(tokens=len(last) * 2)
        return f"【通义{self.model_name}】关于「{last[:10]}」,我的回复:……"


class FakeModel(BaseChatModel):
    """测试替身:不花钱、零延迟、输出可预测——多态的可测试性红利。

    Day 14 项目一的工作流:开发调试全程用它,交付前换 DeepSeekModel。
    """

    def chat(self, messages: list) -> str:
        self._record(tokens=0)
        return "这是测试回答。"


def run_demo(model: BaseChatModel) -> None:
    """业务代码:面对接口(BaseChatModel),不面对实现。

    换模型 = 换传进来的实例,本函数一个字不改——多态的现场证明。
    """
    print(f"\n>>> 当前模型:{model!r}")
    msgs = [{"role": "user", "content": "什么是多态?"}]
    print(model.chat(msgs))
    print(f"用量:{model.count_usage()}")


def run_tests() -> None:
    """需求验收测试。"""
    # temperature 安检:构造时生效
    try:
        DeepSeekModel(temperature=3.0)
        assert False, "应该被安检拦下"
    except ValueError:
        pass

    # temperature 安检:运行时修改也生效(setter 的价值)
    m = DeepSeekModel()
    try:
        m.temperature = -1
        assert False
    except ValueError:
        pass

    # from_config 造出对的型号(cls 的价值)
    m2 = QwenModel.from_config({"model_name": "qwen-max"})
    assert type(m2) is QwenModel and m2.model_name == "qwen-max"

    # 基类不能直接干活(接口的纪律)
    try:
        BaseChatModel("base").chat([])
        assert False
    except NotImplementedError:
        pass

    # isinstance 认继承
    assert isinstance(DeepSeekModel(), BaseChatModel)
    assert isinstance(FakeModel("fake"), BaseChatModel)

    # 用量记账(父类通用实现被子类复用)
    fm = FakeModel("fake")
    fm.chat([{"role": "user", "content": "hi"}])
    fm.chat([{"role": "user", "content": "hi"}])
    assert fm.count_usage()["calls"] == 2

    print("✓ 全部验收测试通过")


if __name__ == "__main__":
    run_tests()
    # 四个模型轮流跑,业务函数一字不改
    for m in [DeepSeekModel(), OpenAIModel("gpt-4o"),
              QwenModel("qwen-plus"), FakeModel("fake")]:
        run_demo(m)
