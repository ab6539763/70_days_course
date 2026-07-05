# =============================================
# Day 03 作业 · 编程题 5:菜单系统 v2(新增违禁词检测)
# 考点:在已有代码上增量开发;标志变量 vs for-else 的选择
# 审题决定工具:要"全部列出"命中的词 → 不能 break → 用标志变量
# =============================================
import random

usage_count = 0

while True:
    print()
    print("=" * 36)
    print("      三日小工具合集 v2.0")
    print("=" * 36)
    print("  1. 文本清洗(Day02 成果)")
    print("  2. 手机号脱敏(Day02 成果)")
    print("  3. 猜数字游戏(Day03 成果)")
    print("  4. 违禁词检测(Day03 作业成果)")     # 新增菜单项
    print("  0. 退出")
    print("-" * 36)

    choice = input("请选择功能:").strip()

    if choice == "1":
        raw = input("请输入待清洗文本:")
        clean = " ".join(raw.strip().lower().split())
        clean = clean.replace("垃圾", "**").replace("傻子", "**")
        print(f"清洗结果:{clean}")
        usage_count += 1

    elif choice == "2":
        while True:
            phone = input("请输入 11 位手机号:").strip()
            if phone.isdigit() and len(phone) == 11:
                break
            print("格式不对,请输入 11 位数字!")
        print(f"脱敏结果:{phone[:3]}****{phone[-4:]}")
        usage_count += 1

    elif choice == "3":
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

    elif choice == "4":
        # 功能 4:违禁词检测(本次作业新增)
        text = input("请输入待检测文本:").strip()
        banned_words = ["赌博", "诈骗", "刷单", "代考"]
        found = False                          # 标志变量:是否发现过违禁词
        for word in banned_words:
            if word in text:
                print(f"命中违禁词:{word}")
                found = True                   # 不 break:要报出所有命中词
        if not found:
            print("审核通过")
        usage_count += 1

    elif choice == "0":
        print(f"本次会话共使用功能 {usage_count} 次,再见!")
        break

    else:
        print(f"没有选项 [{choice}],请输入 0-4")
