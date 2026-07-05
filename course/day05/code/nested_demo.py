# =============================================
# Day 05 · 上午演示代码 2:嵌套结构与字典列表
# 文件:nested_demo.py
# 口诀:从外往里剥洋葱,每层先问"这层是字典还是列表?"
#       字典用 ["名字"],列表用 [数字]
# =============================================

# ---- 1. 字典嵌套字典、嵌套列表 ----
student = {
    "name": "张三",
    "age": 28,
    "contact": {                        # 值是另一个字典
        "email": "zhang@x.com",
        "phone": "13812345678"
    },
    "skills": ["python", "sql"],        # 值是列表
    "scores": {"day01": 92, "day02": 85}
}

# 逐层取值
print(student["contact"]["email"])       # zhang@x.com
print(student["skills"][0])              # python:字典套列表,先按名字后按位置
print(student["scores"]["day02"])        # 85

# 逐层修改
student["contact"]["phone"] = "13900000000"
student["skills"].append("langchain")    # 取出列表直接 append(列表可变)
print(student["skills"])

# ---- 2. 字典列表:数据世界的通用形态 ----
todos = [
    {"task": "复习字典", "priority": "高", "done": False},
    {"task": "写作业", "priority": "中", "done": False},
    {"task": "刷 LeetCode", "priority": "低", "done": True},
]

# 遍历:每轮一个字典,按名字取字段——不用记"2 号位是什么"
for todo in todos:
    status = "✓" if todo["done"] else "□"
    print(f"{status} [{todo['priority']}] {todo['task']}")
    # 引号嵌套:f-string 外层双引号,里层键名用单引号

# 过滤:未完成的高优先级(Day 04 推导式 + 今天字典)
urgent = [t for t in todos if t["priority"] == "高" and not t["done"]]
print(urgent)

# 排序:按优先级权重排(字典定义权重 + sorted 的 key)
order = {"高": 0, "中": 1, "低": 2}
by_priority = sorted(todos, key=lambda t: order[t["priority"]])
# lambda 是"临时小函数",Day 06 正式学;今天知道它告诉 sorted"按什么排"
for t in by_priority:
    print(t["task"])

# ---- 3. Day 14 预告代码的全部谜底:messages 就是字典列表 ----
# 这就是 7 天后要发给 DeepSeek 的真实数据结构(一字不差):
messages = [
    {"role": "system", "content": "你是一个乐于助人的AI助手"},
    {"role": "user", "content": "你好,请介绍一下自己"},
    {"role": "assistant", "content": "你好!我是AI助手……"},
    {"role": "user", "content": "北京今天天气怎么样?"}
]
# 多轮对话 = 不断 append 新字典(昨天练的动作):
messages.append({"role": "assistant", "content": "(这里将是模型的回答)"})
print(f"当前对话 {len(messages)} 条")

# ---- 4. 字典驱动菜单:偿还 Day 03 的欠账 ----
MENU = {
    "1": "文本清洗",
    "2": "手机号脱敏",
    "3": "猜数字游戏",
    "0": "退出",
}
for key, name in MENU.items():          # 菜单打印自动生成,加功能只改 MENU
    print(f"  {key}. {name}")
choice = input("请选择:").strip()
if choice not in MENU:                   # 合法性检查也自动化:in 查键
    print(f"没有选项 [{choice}]")
else:
    print(f"你选择了:{MENU[choice]}")
# 完全体(选项映射到函数)Day 06 解锁:函数也能当字典的值
