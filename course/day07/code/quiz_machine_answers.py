# =============================================
# Day 07 · 周测上机部分:三题参考答案(可直接运行验证)
# 文件:quiz_machine_answers.py
# =============================================


# ──────────────── 上机题 1:订单流水分析(20 分) ────────────────

orders = [
    {"id": "A001", "user": "张三", "amount": 259.0, "status": "paid"},
    {"id": "A002", "user": "李四", "amount": 88.5, "status": "cancelled"},
    {"id": "A003", "user": "张三", "amount": 132.0, "status": "paid"},
    {"id": "A004", "user": "王五", "amount": 46.0, "status": "paid"},
    {"id": "A005", "user": "李四", "amount": 310.0, "status": "refunded"},
]


def paid_total(orders: list) -> float:
    """已支付订单总金额。生成器版 sum + 条件过滤。"""
    return sum(o["amount"] for o in orders if o["status"] == "paid")


def user_spending(orders: list) -> dict:
    """每用户已支付消费额:字典累加器(计数器的金额版)。"""
    spending: dict = {}
    for o in orders:
        if o["status"] != "paid":          # 提前跳过:只统计已支付
            continue
        spending[o["user"]] = spending.get(o["user"], 0) + o["amount"]
    return spending


def top_spender(orders: list) -> str:
    """消费最高的用户名。max 按字典的值比较,返回对应的键。"""
    spending = user_spending(orders)
    return max(spending, key=spending.get)     # "找值最大的键"的标准一行


assert paid_total(orders) == 437.0             # 259 + 132 + 46
assert user_spending(orders) == {"张三": 391.0, "王五": 46.0}
assert top_spender(orders) == "张三"
print("✓ 上机题 1 通过")


# ──────────────── 上机题 2:指令解析器(15 分) ────────────────

def parse_command(text: str) -> tuple:
    """解析用户输入:返回 (指令, 参数) 或 ("", 正文)。

    split(maxsplit=1):最多切一刀——参数里允许有空格,
    这是 maxsplit 的经典用途。本函数将在 Day 14 项目一原样上岗。
    """
    text = text.strip()
    if not text.startswith("/"):
        return ("", text)                      # 非指令:原文本作为正文返回
    parts = text.split(maxsplit=1)             # "/save a.json" → ["/save", "a.json"]
    command = parts[0]
    arg = parts[1].strip() if len(parts) > 1 else ""    # 没参数就给空串
    return (command, arg)


assert parse_command("/save abc.json") == ("/save", "abc.json")
assert parse_command("  /clear  ") == ("/clear", "")
assert parse_command("今天天气如何") == ("", "今天天气如何")
assert parse_command("/save my chat.json") == ("/save", "my chat.json")
print("✓ 上机题 2 通过")


# ──────────────── 上机题 3:对话历史窗口截断(15 分) ────────────────

def trim_history(messages: list, max_rounds: int = 3) -> list:
    """保留 system + 最近 N 轮对话,返回新列表(不动原件)。

    思路:①摘出 system;②剩余消息取最后 2*N 条;③拼回。
    切片天然"尽力而为":不足 N 轮时全保留。
    这是 Day 27 窗口记忆(window memory)的手工版。
    """
    if messages and messages[0]["role"] == "system":
        system_part = messages[:1]             # 切片保持列表形态,好拼接
        chat_part = messages[1:]
    else:
        system_part = []
        chat_part = messages

    recent = chat_part[-max_rounds * 2:]       # 最后 2N 条(切片越界安全)
    return system_part + recent                # 列表相加 = 拼接新列表


msgs = [{"role": "system", "content": "你是助教"}]
for i in range(5):                             # 造 5 轮对话
    msgs.append({"role": "user", "content": f"问{i}"})
    msgs.append({"role": "assistant", "content": f"答{i}"})

trimmed = trim_history(msgs, max_rounds=3)
assert len(trimmed) == 7                       # 1 system + 3 轮 × 2
assert trimmed[0]["role"] == "system"
assert trimmed[1]["content"] == "问2"          # 最早保留的是第 2 轮(0 起)
assert len(msgs) == 11                         # 原列表未被修改!
print("✓ 上机题 3 通过")
