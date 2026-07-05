# =============================================
# Day 02 作业 · 编程题 1:秒数换算器
# 考点:整除与取余的连环使用
# =============================================

total_seconds = int(input("请输入总秒数:"))

# 第一刀:总秒数里有几个 3600 秒 → 小时数
hours = total_seconds // 3600
# 余下的秒数(不足 1 小时的部分)
remainder = total_seconds % 3600

# 第二刀:余数里有几个 60 秒 → 分钟数
minutes = remainder // 60
# 再余下的就是秒
seconds = remainder % 60

print(f"{hours} 小时 {minutes} 分钟 {seconds} 秒")
