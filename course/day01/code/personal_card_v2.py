# =============================================
# 个人信息卡片生成器 v2
# 需求编号:REQ-D01-001
# 新增:出生年份、总学习时长的计算
# 关键知识点:input 返回 str,算术运算前必须 int() 转换
# =============================================

name = input("请输入你的姓名:")

# 与 v1 的区别:input 外面套上 int(),拿到的直接就是整数。
# 如果不转换,下面的 2026 - age 会抛出 TypeError:
#   unsupported operand type(s) for -: 'int' and 'str'
#   (人话:整数不能和字符串做减法)
age = int(input("请输入你的年龄:"))
city = input("请输入你所在的城市:")
job = input("请输入你的期望岗位:")
hours = int(input("请输入你每天可投入的学习小时数:"))

# ---- 处理环节:两个计算 ----
birth_year = 2026 - age       # 出生年份:今年是 2026 年
total_hours = hours * 70      # 70 天课程的总学习时长

# ---- 输出环节:用 f-string 组装人话 ----
print(f"姓名:{name}")
print(f"年龄:{age} 岁(约 {birth_year} 年出生)")
print(f"城市:{city}")
print(f"期望岗位:{job}")
print(f"学习计划:每天 {hours} 小时 × 70 天 = 共 {total_hours} 小时")

# 破坏性实验(课堂演示):年龄输入"二十八"会得到
#   ValueError: invalid literal for int() with base 10: '二十八'
# 优雅地处理这个错误需要 Day 03 的条件判断和 Day 10 的异常捕获,
# 把这个"不爽"记下来——它就是后续课程的学习动力。
