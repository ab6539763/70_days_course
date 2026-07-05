# =============================================
# 简易菜单系统:三日小工具合集
# 需求编号:REQ-D03-002
# 架构:主循环(while True) + 分发器(if/elif)
# 这是 Day 14《命令行 AI 助手》的骨架直系祖先——
# 届时菜单换成自由输入、功能换成调大模型 API、"0"换成"/exit",架构不变
#
# 已知毛病(讲师评审,也是后续课程的教学目标):
#   1. 功能实现平铺在分发器里,主循环太胖 → Day 06 用函数重构
#   2. 猜数字与 guess_number.py 代码重复 → Day 06 函数复用
#   3. 菜单文本写死,加功能要改两处 → Day 05 字典驱动
# =============================================
import random

usage_count = 0                                # 会话计数器:累加器模式

while True:
    # ---- 显示菜单 ----
    # 每轮循环都重新打印,保证功能用完回来还能看到选项
    print()
    print("=" * 36)
    print("      三日小工具合集 v1.0")
    print("=" * 36)
    print("  1. 文本清洗(Day02 成果)")
    print("  2. 手机号脱敏(Day02 成果)")
    print("  3. 猜数字游戏(Day03 成果)")
    print("  0. 退出")
    print("-" * 36)

    choice = input("请选择功能:").strip()      # 清洗输入,老习惯

    # ---- 分发器:根据选择走不同分支 ----
    if choice == "1":
        # 功能 1:文本清洗(Day 02 流水线的浓缩版)
        raw = input("请输入待清洗文本:")
        clean = " ".join(raw.strip().lower().split())     # F1+F2+F4 一行流
        clean = clean.replace("垃圾", "**").replace("傻子", "**")   # F3
        print(f"清洗结果:{clean}")
        usage_count += 1

    elif choice == "2":
        # 功能 2:手机号脱敏(带校验循环)
        while True:
            phone = input("请输入 11 位手机号:").strip()
            if phone.isdigit() and len(phone) == 11:      # 全数字 且 长度 11
                break
            print("格式不对,请输入 11 位数字!")
        print(f"脱敏结果:{phone[:3]}****{phone[-4:]}")
        usage_count += 1

    elif choice == "3":
        # 功能 3:猜数字(简化版,聚焦主流程)
        answer = random.randint(1, 100)
        count = 0
        print("我想好了一个 1-100 的数")
        while True:
            guess_text = input("你猜:").strip()
            if not guess_text.isdigit():
                print("请输入数字!")
                continue
            guess = int(guess_text)
            count += 1
            if guess > answer:
                print("大了 ↓")
            elif guess < answer:
                print("小了 ↑")
            else:
                print(f"猜中!共 {count} 次")
                break
        usage_count += 1

    elif choice == "0":
        # 退出:先统计,再砸破主循环
        print(f"本次会话共使用功能 {usage_count} 次,再见!")
        break

    else:
        # 兜底分支:一切非法输入到这里,程序永不裸奔
        print(f"没有选项 [{choice}],请输入 0-3")
