# =============================================
# Day 06 作业 · 编程题 5:注册表加"参数化功能"
# 考点:lambda 延迟绑定——给注册表塞"预装了参数的调用"
# =============================================


def run_power(n: int = 2) -> None:
    """N 次方计算器。"""
    x = float(input("输入一个数:").strip())
    print(f"{x} 的 {n} 次方 = {x ** n}")


def main() -> None:
    # 注册表要求存"不带括号的可调用对象",但 run_power 需要参数——
    # lambda: run_power(3) 制造了一个"无参数的壳",壳里装着带参数的调用。
    # 调用壳的时候(func()),里面的 run_power(3) 才真正执行。
    # 这个技巧叫"延迟绑定/偏函数思想",Day 13 的 functools.partial 是正规军
    menu = {
        "4": ("平方计算器", lambda: run_power(2)),
        "5": ("立方计算器", lambda: run_power(3)),
    }

    while True:
        print()
        for key, (name, _) in menu.items():
            print(f"  {key}. {name}")
        print("  0. 退出")
        choice = input("请选择:").strip()

        if choice == "0":
            break
        if choice not in menu:
            print(f"没有选项 [{choice}]")
            continue
        _, func = menu[choice]
        func()


if __name__ == "__main__":
    main()
