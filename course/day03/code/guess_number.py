# =============================================
# 猜数字游戏
# 需求编号:REQ-D03-001
# 知识点:while True 主循环、输入校验、if/elif/else、计数器
# =============================================
import random                          # 引入随机数工具箱(标准库,无需安装)

# randint(a, b):返回 a 到 b 之间的随机整数——注意这是"含头又含尾"的少数派!
answer = random.randint(1, 100)
count = 0                              # 计数器:有效猜测次数

print("=" * 40)
print("猜数字:我已想好 1-100 之间的一个整数")
print("=" * 40)

while True:
    # ---- 输入校验(不合法不计次) ----
    guess_text = input("你猜:").strip()

    if not guess_text.isdigit():       # 非数字(含负号、小数点、空串)一律拦下
        print("请输入 1-100 的整数!")
        continue                       # 这把不算,重新输入

    guess = int(guess_text)            # 过了 isdigit,转换绝对安全
    if guess < 1 or guess > 100:
        print("超出范围,请输入 1-100!")
        continue

    # ---- 有效猜测:计数 + 判断 ----
    count += 1

    if guess > answer:
        print("大了 ↓")
    elif guess < answer:
        print("小了 ↑")
    else:
        # 猜中:根据次数给评价,然后退出
        print(f"猜中了!答案是 {answer},共用 {count} 次")
        if count <= 4:
            print("评价:运气爆棚!")
        elif count <= 7:
            print("评价:二分搜索高手!")     # 每次猜中间,7 次必中——二分查找思想
        else:
            print("评价:再接再厉~")
        break                          # 游戏结束,砸破 while True

print("感谢游玩!")
