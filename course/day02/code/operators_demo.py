# =============================================
# Day 02 · 上午演示代码:运算符全家桶
# 文件:operators_demo.py
# 说明:课堂跟敲用。每一段都可以单独取消注释实验
# =============================================

# ---- 1. 七个算术运算符 ----
print(10 + 3)     # 13
print(10 - 3)     # 7
print(10 * 3)     # 30
print(10 / 3)     # 3.3333333333333335  除法结果永远是 float
print(10 / 5)     # 2.0                 就算除得尽也是 float
print(10 // 3)    # 3                   整除:只要商的整数部分
print(10 % 3)     # 1                   取余
print(10 ** 3)    # 1000                幂运算
print(9 ** 0.5)   # 3.0                 0.5 次方 = 开平方

# ---- 2. 整除 + 取余的经典搭配:时间换算 ----
total_minutes = 135
hours = total_minutes // 60      # 2 小时
minutes = total_minutes % 60     # 余 15 分钟
print(f"{total_minutes} 分钟 = {hours} 小时 {minutes} 分钟")

# ---- 3. 优先级:昨天 BMI 坑的现场复盘 ----
weight, height = 70, 1.75              # 一行给多个变量赋值(新语法)
wrong = weight / height * height       # 同级从左到右 → 恒等于 weight,不报错但全错!
right = weight / (height * height)     # 拿不准就加括号
print(wrong, right)                    # 70.0 22.857142857142858

# ---- 4. 复合赋值 ----
count = 0
count += 1            # 等价于 count = count + 1
count += 1
print(count)          # 2
# 【伏笔】Day 24 流式输出的心脏:answer += chunk

# ---- 5. 运算符重载:同一个 + 号的两副面孔 ----
print(3 + 5)              # 8       数字:加法
print("3" + "5")          # 35      字符串:拼接
print("-" * 20)           # 20 个横线:字符串 × 整数 = 重复
# print("3" + 5)          # TypeError!Python 拒绝猜测,必须显式转换:
print(int("3") + 5)       # 8

# ---- 6. 比较运算符:程序学会"提问" ----
age = 28
print(age > 18)       # True
print(age == 28)      # True   双等号是比较;单等号是赋值,千万别混
print(age != 30)      # True
print("abc" == "ABC") # False  字符串比较大小写敏感 → 所以比较前先 lower()

# ---- 7. 逻辑运算符:组合提问 ----
print(age >= 0 and age <= 120)    # True  并且
print(0 <= age <= 120)            # True  Python 特色:区间可以连写
vip, points = False, 12000
print(vip or points > 10000)      # True  或者
print(not vip)                    # True  取反

# ---- 8. 真值规则:空即是 False ----
print(bool(0), bool(""), bool(0.0))    # False False False
print(bool("hi"), bool(-1))            # True True(非零即真)
print(bool(" "))                       # True ⚠️ 空格是字符,不是空!
