# =============================================
# Day 04 作业 · 编程题 1:成绩单分析器
# 考点:max/min/sum、推导式过滤、sorted、比率计算
# =============================================

scores = [92, 45, 85, 58, 77, 63, 88, 51]

# ① 三个统计:max/min/sum 是内置函数,接收列表直接出结果
highest = max(scores)
lowest = min(scores)
average = sum(scores) / len(scores)          # 平均 = 总和 / 个数

print(f"最高 {highest} | 最低 {lowest} | 平均 {average:.1f}")

# ② 及格名单:推导式过滤
passed = [s for s in scores if s >= 60]
print(f"及格名单:{passed}")

# ③ 排名:sorted 复制一份降序排(不动原始数据,保留"提交顺序")
ranking = sorted(scores, reverse=True)
print(f"排名:{ranking}")

# ④ 及格率:及格人数 / 总人数
rate = len(passed) / len(scores)
print(f"及格率:{rate:.1%}")
