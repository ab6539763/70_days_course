# =============================================
# Day 03 · 上午演示代码 2:循环全家桶
# 文件:loop_demo.py
# =============================================

# ---- 1. while 三要素:初始化、条件、更新 ----
count = 1                    # ① 初始化
while count <= 5:            # ② 条件
    print(f"第 {count} 次")
    count += 1               # ③ 更新(注释掉这行体验死循环,Ctrl+C 急刹车)
print("循环结束")

# ---- 2. 输入校验循环:Day 01 思考题 2 的完整答案 ----
while True:
    age_text = input("请输入年龄(0-120):").strip()
    if not age_text.isdigit():             # 先检查:全数字才放行(负号/小数点都拦下)
        print("请输入数字!")
        continue                           # 这把不算,再来
    age = int(age_text)                    # 过了检查,转换绝对安全,不会 ValueError
    if age < 0 or age > 120:
        print("年龄超出合理范围!")
        continue
    break                                  # 通过全部校验,带着合法 age 离开
print(f"校验通过,年龄:{age}")

# ---- 3. for:对一批东西挨个处理(结清 Day 02 作业编程题 4 的账) ----
text = input("请输入内容:")
banned_words = ["赌博", "诈骗", "刷单"]        # 列表:明天的主角,今天先用
for word in banned_words:                     # 第一个 in:for 语法的一部分
    if word in text:                          # 第二个 in:包含判断运算符,不是一个东西
        print(f"检测到违禁词:{word}")

# for-else 冷知识:循环没被 break 打断才执行 else
for word in banned_words:
    if word in text:
        print(f"驳回:含违禁词 {word}")
        break
else:                          # 注意:else 对齐 for,不是对齐 if!
    print("审核通过")

# ---- 4. range:数字序列生成器(含头不含尾,和切片同一约定) ----
for i in range(5):
    print(i, end=" ")          # 0 1 2 3 4
print()
for i in range(1, 6):
    print(i, end=" ")          # 1 2 3 4 5
print()
for i in range(5, 0, -1):      # 步长为负 = 倒数
    print(i, end=" ")
print("发射!")

# ---- 5. 累加器三件套:今后所有统计代码的地基 ----
# 数字累加
total = 0
for i in range(1, 101):
    total += i
print(f"1 加到 100 = {total}")            # 5050

# 字符串拼接:Day 24 流式输出的雏形(今天用假数据跑通形状)
answer = ""
for chunk in ["大模型", "正在", "逐字", "返回"]:
    answer += chunk
    print(f"当前已收到:{answer}")
print(f"完整回答:{answer}")

# 条件计数
count = 0
for ch in "large language model":
    if ch in "aeiou":
        count += 1
print(f"元音数量:{count}")               # 7
