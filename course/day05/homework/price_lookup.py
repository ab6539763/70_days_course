# =============================================
# Day 05 作业 · 编程题 5:模型价格查询器
# 考点:嵌套字典查询、in 防御、keys 列举、主循环骨架(Day 03 复利)
# =============================================

PRICE_TABLE = {
    "deepseek-chat": {"input": 1.0, "output": 4.0},
    "gpt-4o": {"input": 18.0, "output": 72.0},
    "qwen-plus": {"input": 4.0, "output": 12.0},
}

while True:
    name = input("模型名(/exit 退出):").strip().lower()    # 清洗+统一小写

    if name == "/exit":
        print("再见!")
        break

    if name not in PRICE_TABLE:                    # in 查键:防 KeyError
        # ", ".join(...) 把所有键拼成人话(Day 02 join 的复利)
        print(f"没有 [{name}],可选:{', '.join(PRICE_TABLE.keys())}")
        continue

    price = PRICE_TABLE[name]                      # 确认存在后,方括号放心取
    print(f"{name}:输入 {price['input']} 元/百万 | 输出 {price['output']} 元/百万")

    # ---- 加分项:成本预估 ----
    t_in = input("预计输入token数(回车跳过):").strip()
    if t_in.isdigit():
        t_out = input("预计输出token数:").strip()
        if t_out.isdigit():
            cost = (int(t_in) / 1_000_000 * price["input"]
                    + int(t_out) / 1_000_000 * price["output"])
            print(f"预估成本:{cost:.4f} 元")
