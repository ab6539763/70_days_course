# =============================================
# Day 04 作业 · 编程题 3:模拟对话历史管理
# 考点:append 积累状态、切片截断、指令分发
# 这就是 Day 14 AI 助手的"记忆管理"裸奔版:
#   真实版只是把"模拟回复"换成 API 调用、把字符串换成字典(Day 05 学)
# 第④点"超长截断"正是 Day 27 记忆窗口(window memory)的原始思想
# =============================================

history = []                       # 对话历史:程序的核心状态
MAX_LEN = 6                        # 记忆上限:常量

while True:
    text = input("你说:").strip()

    if not text:                   # 空输入:跳过(真值规则)
        continue

    if text == "/exit":
        print("再见!")
        break

    if text == "/history":
        if not history:
            print("(暂无记录)")
        for i, msg in enumerate(history, start=1):
            print(f"  {i}. {msg}")
        continue                   # 指令处理完,不落入"正常对话"分支

    if text == "/count":
        print(f"当前 {len(history)} 条记录")
        continue

    # ---- 正常对话:一问一答各存一条 ----
    history.append(f"[用户] {text}")
    history.append(f"[AI回复] 收到:{text}")
    print(f"[AI回复] 收到:{text}")

    # ---- 记忆压缩:超上限就砍掉最早的 2 条 ----
    if len(history) > MAX_LEN:
        history = history[2:]      # 切片:丢弃最早 2 条,留下其余
        print("(记忆已压缩:最早的一问一答被遗忘)")
