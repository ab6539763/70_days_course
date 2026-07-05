# =============================================
# Day 09 作业 · 编程题 2:KimiModel(扩展性验收)
# 验证"新增厂商零侵入":run_demo 一个字不改就能跑新模型
# =============================================
import sys
import os

# 让 Python 能找到课堂代码(临时手法;规范做法 Day 10 讲包结构)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from model_layer import BaseChatModel, run_demo


class KimiModel(BaseChatModel):
    """月之暗面 Kimi:验证'新增厂商零侵入'。"""

    def __init__(self, model_name: str = "moonshot-v1-8k", temperature: float = 0.7,
                 context_window: int = 8000):
        super().__init__(model_name, temperature)     # 老三样让爸爸装
        self.context_window = context_window          # 自己的新属性

    @property
    def context_k(self) -> str:
        """人类友好的上下文长度:8000 → '8K'(计算属性)。"""
        return f"{self.context_window // 1000}K"

    def chat(self, messages: list) -> str:
        """Kimi 风格的模拟回答。"""
        last = messages[-1]["content"] if messages else ""
        self._record(tokens=len(last) * 2)
        return f"[Kimi|{self.context_k}] 关于「{last[:10]}」:……"


if __name__ == "__main__":
    kimi = KimiModel()
    assert kimi.context_k == "8K"
    assert isinstance(kimi, BaseChatModel)
    run_demo(kimi)                     # 业务代码零改动:扩展性验收通过
    print("✓ KimiModel 扩展验收通过")
