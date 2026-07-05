# =============================================
# Day 01 作业 · 编程题 1:BMI 计算器
# 考点:input + float 转换、算术运算、f-string 格式控制
# =============================================

# 体重和身高都可能带小数,所以用 float() 而不是 int()
weight = float(input("请输入你的体重(公斤):"))
height = float(input("请输入你的身高(米,如 1.75):"))

# BMI 公式 = 体重(kg) / 身高(m) 的平方
# 注意括号:不加括号的话 weight / height * height 会从左到右算,结果恒等于 weight
bmi = weight / (height * height)

# :.1f 保留一位小数
print(f"你的 BMI 是:{bmi:.1f}")
