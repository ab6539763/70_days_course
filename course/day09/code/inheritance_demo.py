# =============================================
# Day 09 · 上午演示代码 1:继承、重写、super、isinstance
# 文件:inheritance_demo.py
# =============================================


# ---- 1. 继承:站在父类的肩膀上 ----
class BaseModel:
    """所有模型的父类:存放共同的属性与行为。"""

    def __init__(self, model_name: str, temperature: float = 0.7):
        self.model_name = model_name
        self.temperature = temperature

    def format_info(self) -> str:
        """模型信息(所有子类通用,写一遍)。"""
        return f"{self.model_name} (temp={self.temperature})"

    def chat(self, messages: list) -> str:
        """父类的 chat:'必须被子类重写'的占位。

        NotImplementedError 行业惯例:父类只定接口不给实现,
        谁忘了重写,一调用就炸出明确提示(比默默返回 None 好一万倍)。
        """
        raise NotImplementedError("子类必须实现 chat 方法")

    @classmethod
    def from_config(cls, config: dict) -> "BaseModel":
        """从配置字典造模型。cls 是'发起调用的那个类'——子类下单造子类。"""
        return cls(config["model_name"], config.get("temperature", 0.7))


class OpenAIModel(BaseModel):          # class 子类(父类)
    """OpenAI 系模型。"""

    def __init__(self, model_name: str, temperature: float = 0.7,
                 api_base: str = "https://api.openai.com"):
        super().__init__(model_name, temperature)   # 老三样让爸爸装,别抄一遍
        self.api_base = api_base                    # 自己的新属性自己装

    def chat(self, messages: list) -> str:          # 重写:就近覆盖父类版本
        """OpenAI 风格的调用(今天模拟,Day 12 换真 API)。"""
        return f"[OpenAI:{self.model_name}] 收到 {len(messages)} 条消息,回答:……"


class QwenModel(BaseModel):
    """通义千问系模型。"""

    def chat(self, messages: list) -> str:
        """通义风格的调用。"""
        return f"[通义:{self.model_name}] 已处理 {len(messages)} 条消息,答复:……"


# ---- 2. 白拿父类的能力 ----
gpt = OpenAIModel("gpt-4o", api_base="https://my-proxy.com")
qwen = QwenModel("qwen-plus", temperature=0.3)
print(gpt.format_info())       # 没在子类里写 format_info:从父类白拿
print(qwen.format_info())
print(gpt.model_name, gpt.api_base)    # 父类装的 + 自己装的都在(super 的功劳)

# ---- 3. 重写生效:同一个调用,各自表述 ----
msgs = [{"role": "user", "content": "你好"}]
print(gpt.chat(msgs))          # 走 OpenAI 版
print(qwen.chat(msgs))         # 走通义版

# ---- 4. isinstance 认继承,type 只认亲生 ----
print(isinstance(gpt, OpenAIModel))    # True
print(isinstance(gpt, BaseModel))      # True:儿子也是这家人
print(isinstance(gpt, QwenModel))      # False
print(type(gpt) is OpenAIModel)        # True

# ---- 5. cls 工厂的回报:子类下单造子类 ----
m = QwenModel.from_config({"model_name": "qwen-max"})
print(type(m).__name__)        # QwenModel —— 工厂认得下单的是谁
