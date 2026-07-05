# =============================================
# Day 03 作业 · 编程题 1:BMI 计算器 2.0
# 考点:校验循环 + elif 分级(条件从严到宽单调排列)
# 注:两段校验循环几乎一模一样——这份"复制粘贴的痛苦"是故意的,
#    Day 06 学函数后本题要求重构成一个函数用两次
# =============================================

# ---- 校验循环 1:体重 ----
while True:
    w_text = input("体重(公斤):").strip()
    # replace(".", "", 1) 删掉第一个小数点后再 isdigit:
    # "70.5" → "705" → True;"7..5" → "7.5" → False;"-70" → False
    if w_text.replace(".", "", 1).isdigit() and float(w_text) > 0:
        weight = float(w_text)
        break
    print("请输入正数!")

# ---- 校验循环 2:身高 ----
while True:
    h_text = input("身高(米,如 1.75):").strip()
    if h_text.replace(".", "", 1).isdigit() and float(h_text) > 0:
        height = float(h_text)
        break
    print("请输入正数!")

bmi = weight / (height * height)

# ---- 分级:条件从严到宽,命中即退出 ----
if bmi >= 28:
    level = "肥胖"
elif bmi >= 24:
    level = "偏胖"
elif bmi >= 18.5:
    level = "正常"
else:
    level = "偏瘦"

print(f"BMI = {bmi:.1f},分级:{level}")
