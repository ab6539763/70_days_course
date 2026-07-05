# =============================================
# Day 01 作业 · 编程题 2:API 成本估算器
# 考点:多变量运算、常量提取、f-string
# 伏笔:Day 15 会用 tiktoken 真实计算 token 数,今天先建立成本意识
# =============================================

# ---- 常量区:价格写成常量,涨价时只改这里 ----
PRICE_INPUT_PER_M = 1.0     # 输入价:1 元 / 百万 token(课堂虚拟价,以官网为准)
PRICE_OUTPUT_PER_M = 4.0    # 输出价:4 元 / 百万 token
DAYS_PER_MONTH = 30         # 每月按 30 天估算

# ---- 输入环节 ----
calls_per_day = int(input("每天调用次数:"))
tokens_in = int(input("平均每次输入 token 数:"))
tokens_out = int(input("平均每次输出 token 数:"))

# ---- 处理环节 ----
# 每天总 token = 每次 token × 每天次数;除以 1_000_000 换算成"百万"单位
# (数字里的下划线是 Python 的千分位写法,纯粹为了人类可读,1_000_000 == 1000000)
daily_cost_in = calls_per_day * tokens_in / 1_000_000 * PRICE_INPUT_PER_M
daily_cost_out = calls_per_day * tokens_out / 1_000_000 * PRICE_OUTPUT_PER_M
daily_cost = daily_cost_in + daily_cost_out
monthly_cost = daily_cost * DAYS_PER_MONTH

# ---- 输出环节 ----
print(f"每天成本:{daily_cost:.4f} 元(输入 {daily_cost_in:.4f} + 输出 {daily_cost_out:.4f})")
print(f"每月成本(30 天):{monthly_cost:.4f} 元")
