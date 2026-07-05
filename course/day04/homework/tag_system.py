# =============================================
# Day 04 作业 · 编程题 2:标签系统
# 考点:set 去重 + 集合运算 + sorted 把集合变回有序列表
# =============================================

tags_a = ["python", "ai", "llm", "python", "rag"]
tags_b = ["ai", "agent", "llm", "docker"]

# ① 列表 → 集合:自动去重
set_a = set(tags_a)
set_b = set(tags_b)
print(f"A 去重:{set_a}")
print(f"B 去重:{set_b}")

# ② 交集:两篇共同话题
print(f"共同标签:{set_a & set_b}")

# ③ 差集:A 独有
print(f"A 独有:{set_a - set_b}")

# ④ 并集后排序:集合无序,展示给人看时用 sorted 变回有序列表
all_tags = sorted(set_a | set_b)
print(f"全部标签:{all_tags}")
