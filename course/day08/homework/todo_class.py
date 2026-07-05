# =============================================
# Day 08 作业 · 编程题 1:Todo 类
# 考点:构造即校验、默认参数、to_dict/from_dict 海关对
# =============================================


class Todo:
    """一条待办事项。"""

    VALID_PRIORITIES = ("高", "中", "低")           # 常量集合用元组

    def __init__(self, task: str, priority: str = "中", done: bool = False):
        if not task.strip():                        # 校验 1:内容非空
            raise ValueError("待办内容不能为空")
        if priority not in self.VALID_PRIORITIES:   # 校验 2:优先级合法
            raise ValueError(f"优先级必须是 {self.VALID_PRIORITIES} 之一")
        self.task = task.strip()                    # 进门先清洗:类里同样适用
        self.priority = priority
        self.done = done

    def finish(self) -> None:
        """标记完成。"""
        self.done = True

    def format(self) -> str:
        """展示行。"""
        mark = "✓" if self.done else "□"
        return f"{mark} [{self.priority}] {self.task}"

    def to_dict(self) -> dict:
        """出境海关:对象 → 字典(准备存 JSON)。"""
        return {"task": self.task, "priority": self.priority, "done": self.done}

    @classmethod
    def from_dict(cls, data: dict) -> "Todo":
        """入境海关:字典 → 对象。get 给默认值:容忍旧数据缺字段。"""
        return cls(data["task"], data.get("priority", "中"), data.get("done", False))


# ---- assert 测试 ----
t = Todo("写作业", "高")
assert t.format() == "□ [高] 写作业"
t.finish()
assert t.done and t.format().startswith("✓")
assert Todo.from_dict(t.to_dict()).task == "写作业"      # 海关往返无损

try:
    Todo("   ")                                # 空内容应被拒绝
    assert False
except ValueError:
    pass
try:
    Todo("x", "紧急")                          # 非法优先级应被拒绝
    assert False
except ValueError:
    pass
print("✓ Todo 类全部测试通过")
