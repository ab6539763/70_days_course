# =============================================
# Day 08 作业 · 编程题 3:BankAccount 类
# 考点:防御设计(raise + 返回 False 两种失败方式)、
#       history 必须是实例属性(别踩类属性雷!)
# =============================================


class BankAccount:
    """银行账户:余额与流水的管家。"""

    def __init__(self, owner: str, balance: float = 0):
        self.owner = owner
        self.balance = balance
        self.history: list = []            # 流水:实例属性!写成类属性就会全行共享

    def deposit(self, amount: float) -> None:
        """存款。金额非正:raise(调用方传错参数,是编程错误,该崩)。"""
        if amount <= 0:
            raise ValueError(f"存款金额必须为正,收到 {amount}")
        self.balance += amount
        self.history.append(f"存入 {amount:.2f},余额 {self.balance:.2f}")

    def withdraw(self, amount: float) -> bool:
        """取款。金额非正 raise;余额不足返回 False(业务上正常发生,不该崩)。

        两种失败方式的选择:
        - 编程错误(负数金额)→ raise:让开发者立刻发现
        - 业务失败(余额不足)→ 返回 False:让调用方走正常分支处理
        """
        if amount <= 0:
            raise ValueError(f"取款金额必须为正,收到 {amount}")
        if amount > self.balance:
            self.history.append(f"取款 {amount:.2f} 失败:余额不足")
            return False
        self.balance -= amount
        self.history.append(f"取出 {amount:.2f},余额 {self.balance:.2f}")
        return True

    def show_history(self) -> None:
        """打印流水。"""
        print(f"—— {self.owner} 的账户流水 ——")
        for i, record in enumerate(self.history, start=1):
            print(f"  {i}. {record}")


# ---- 测试 ----
if __name__ == "__main__":
    a = BankAccount("张三")
    b = BankAccount("李四")

    a.deposit(100)
    assert a.balance == 100 and b.balance == 0          # 账户独立

    assert not a.withdraw(500)                          # 余额不足:False 且不扣款
    assert a.balance == 100

    assert a.withdraw(30)
    assert a.balance == 70

    try:
        a.deposit(-1)                                   # 非法金额:raise
        assert False
    except ValueError:
        pass

    assert len(a.history) == 3 and len(b.history) == 0  # 流水互不串台(实例属性!)
    a.show_history()
    print("✓ BankAccount 全部测试通过")
