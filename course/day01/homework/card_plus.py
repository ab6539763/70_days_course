# =============================================
# Day 01 作业 · 编程题 3:名片美化
# 考点:在已有代码上做增量修改(工程师的日常),变量复用
# =============================================

CURRENT_YEAR = 2026
COURSE_DAYS = 70
BANNER_WIDTH = 40

# 分隔线只生成一次,三处复用——"同样的东西只写一遍"(DRY 原则),
# 以后想把 = 换成 -,只改这一行
line = "=" * BANNER_WIDTH

print(line)
print("     欢迎加入 70 天大模型开发训练营")
print(line)

name = input("请输入你的姓名:")
age = int(input("请输入你的年龄(数字):"))
city = input("请输入你所在的城市:")
job = input("请输入你的期望岗位:")
hours = int(input("请输入你每天可投入的学习小时数(数字):"))
motto = input("请输入你的一句话签名:")        # 本题新增项

birth_year = CURRENT_YEAR - age
total_hours = hours * COURSE_DAYS

card = f"""
┌────────────────────────────────────┐
│          新学员信息卡片              │
├────────────────────────────────────┤
│  姓名:{name}
│  年龄:{age} 岁({birth_year} 年出生)
│  城市:{city}
│  期望岗位:{job}
│  学习投入:每天 {hours} 小时,{COURSE_DAYS} 天共 {total_hours} 小时
│  签名:{motto}
└────────────────────────────────────┘
"""
print(card)

print(f"{name},欢迎你!{COURSE_DAYS} 天后,愿你成为一名合格的{job}。")
print(line)          # 结尾也复用分隔线,首尾呼应
