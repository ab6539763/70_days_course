# =============================================
# Day 03 作业 · 编程题 2:密码强度检查器
# 考点:for 遍历字符串 + 标志变量 + 多条件评分
# 标志变量(flag):先假设 False,循环中发现证据就翻成 True——高频模式
# =============================================

password = input("请输入密码:").strip()

# 四个标志变量,初始全为"未发现"
has_lower = False
has_upper = False
has_digit = False
has_special = False

SPECIALS = "!@#$%^&*"          # 特殊字符表:常量

for ch in password:            # 逐字符检查,每个字符最多点亮一个标志
    if ch.islower():
        has_lower = True
    elif ch.isupper():
        has_upper = True
    elif ch.isdigit():
        has_digit = True
    elif ch in SPECIALS:
        has_special = True

# 计分:四条规则各 1 分
score = 0
if len(password) >= 8:
    score += 1
if has_lower and has_upper:
    score += 1
if has_digit:
    score += 1
if has_special:
    score += 1

# 分级
if score >= 4:
    strength = "强"
elif score >= 2:
    strength = "中"
else:
    strength = "弱"

print(f"得分 {score}/4,强度:{strength}")
