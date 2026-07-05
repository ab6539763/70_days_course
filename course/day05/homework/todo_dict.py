# =============================================
# Day 05 作业 · 编程题 2:待办数据层重构
# 考点:字典列表建模、改字段代替移动列表、推导式过滤、权重排序
# 对比 Day 04:两个列表(todos/done_list)合并成一个字典列表,
#            "完成"从"pop+append 移动"简化为"改一个布尔字段"——
#            数据结构选对了,代码自然变简单
# =============================================

# ① 添加三条(真实程序里是 append,这里直接字面量初始化)
todos = [
    {"task": "复习JSON", "priority": "高", "done": False},
    {"task": "写作业", "priority": "中", "done": False},
    {"task": "刷LeetCode", "priority": "低", "done": False},
]


def show(items):                      # 偷跑一个函数(明天正式学),避免打印逻辑抄三遍
    for i, t in enumerate(items, start=1):
        mark = "✓" if t["done"] else "□"
        print(f"  {i}. {mark} [{t['priority']}] {t['task']}")


# ② 打印全部
print("全部待办:")
show(todos)

# ③ 完成第 1 条:改字段,不用移动
todos[0]["done"] = True
print("完成第 1 条后:")
show(todos)

# ④ 未完成子清单:推导式过滤
pending = [t for t in todos if not t["done"]]
print("未完成:")
show(pending)

# ⑤ 按优先级排序:字典定义权重 + sorted key
order = {"高": 0, "中": 1, "低": 2}
by_priority = sorted(todos, key=lambda t: order[t["priority"]])
print("按优先级:")
show(by_priority)
