# =============================================
# 学习工具箱 v2.0 —— 函数化重构(大重构日成果)
# 需求编号:REQ-D06-001
# 架构:入口层 main() / 功能层 run_*() / 工具层(纯函数)
# 公司规范落实清单:
#   ✅ 每个功能一个函数(单一职责)
#   ✅ 工具函数只 return 不 print(展示与逻辑分离)
#   ✅ 重复代码提取为公共函数(DRY)
#   ✅ docstring + 类型注解
#   ✅ main() + if __name__ == "__main__"(原理 Day 10 揭晓)
#   ✅ 字典驱动菜单(注册表模式:Day 19 工具注册表的雏形)
# =============================================
import random


# ──────────────── 工具层:纯函数,只 return 不 print ────────────────

def clean_text(text: str, banned_words: list = None) -> str:
    """清洗文本:去两端空白、小写化、规范空格、敏感词打码。

    Day 02 的四道工序流水线,函数化后成为可复用组件。
    banned_words 默认 None 再造列表——默认参数地雷的正确拆法。
    """
    if banned_words is None:
        banned_words = ["垃圾", "傻子", "废物"]
    result = " ".join(text.strip().lower().split())     # F1+F2+F4
    for word in banned_words:                            # F3:Day 03 承诺的循环版
        result = result.replace(word, "*" * len(word))   # 等长打码
    return result


def mask_phone(phone: str) -> str:
    """手机号脱敏:138****5678。写了五遍的代码,从此只此一份。"""
    return phone[:3] + "****" + phone[-4:]


def read_int_in_range(prompt: str, low: int, high: int) -> int:
    """读取一个 [low, high] 范围内的整数,不合法就重问,保证返回合法值。

    Day 03 校验循环的最终归宿:所有"要一个范围内整数"的场合一行调用解决。
    注意最后的 return 兼职了 break:直接终结循环+函数。
    """
    while True:
        text = input(prompt).strip()
        if not text.isdigit():
            print("请输入数字!")
            continue
        value = int(text)
        if not (low <= value <= high):
            print(f"请输入 {low}-{high} 之间的数!")
            continue
        return value


# ──────────────── 功能层:负责交互,调用工具层 ────────────────

def run_cleaner() -> None:
    """功能:文本清洗。"""
    raw = input("请输入待清洗文本:")
    print(f"清洗结果:{clean_text(raw)}")        # 逻辑一行搞定:工具层的红利


def run_mask() -> None:
    """功能:手机号脱敏。"""
    while True:
        phone = input("请输入 11 位手机号:").strip()
        if phone.isdigit() and len(phone) == 11:
            break
        print("格式不对!")
    print(f"脱敏结果:{mask_phone(phone)}")


def run_guess() -> None:
    """功能:猜数字。Day 03 写了两遍的逻辑,从此一份。"""
    answer = random.randint(1, 100)
    count = 0
    print("我想好了一个 1-100 的数")
    while True:
        guess = read_int_in_range("你猜:", 1, 100)      # 工具层复用:三行变一行
        count += 1
        if guess > answer:
            print("大了 ↓")
        elif guess < answer:
            print("小了 ↑")
        else:
            print(f"猜中!共 {count} 次")
            return              # 函数里退出,return 比 break 干脆


# ──────────────── 入口层:字典驱动的主循环 ────────────────

def main() -> None:
    """程序入口:菜单调度。

    menu 的值是 (功能名, 函数) 元组——函数不带括号!
    带括号是"立刻执行拿结果",不带括号是"函数本身"。
    函数是一等公民,能像数据一样存进字典——
    这是 Day 13 装饰器、Day 19 工具注册表的语法根基。
    """
    menu = {
        "1": ("文本清洗", run_cleaner),
        "2": ("手机号脱敏", run_mask),
        "3": ("猜数字游戏", run_guess),
    }

    while True:
        print()
        print("=" * 36)
        print("      学习工具箱 v2.0(函数版)")
        print("=" * 36)
        for key, (name, _) in menu.items():        # 拆包:函数用 _ 占位
            print(f"  {key}. {name}")
        print("  0. 退出")

        choice = input("请选择:").strip()
        if choice == "0":
            print("再见!")
            break
        if choice not in menu:
            print(f"没有选项 [{choice}]")
            continue

        _, func = menu[choice]        # 从注册表取出函数
        func()                        # 加括号:执行!


if __name__ == "__main__":            # 直接运行才执行 main;被 import 时不执行
    main()
