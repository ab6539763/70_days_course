# =============================================
# Day 05 作业 · 编程题 3:messages 工具箱
# 考点:messages 结构的组装、遍历、映射、统计
# 这些零件将在 Day 14 项目一里原样上岗
# =============================================

# ① 初始化:system 打底
messages = [
    {"role": "system", "content": "你是一个专业的Python学习助教"}
]

# ② 三轮模拟对话:一问一答成对 append
questions = ["什么是字典?", "JSON和字典的区别?", "get和方括号怎么选?"]
for q in questions:
    messages.append({"role": "user", "content": q})
    messages.append({"role": "assistant", "content": f"已收到问题:{q}"})

# ③ 打印:role → 显示名,用字典映射(比 if/elif 三连优雅)
ROLE_NAMES = {"system": "[系统设定]", "user": "[我]", "assistant": "[AI]"}
for msg in messages:
    label = ROLE_NAMES.get(msg["role"], "[未知]")     # get 兜底:遇到新角色不崩
    print(f"{label} {msg['content']}")

# ④ 统计
total_count = len(messages)
user_count = len([m for m in messages if m["role"] == "user"])
char_count = sum(len(m["content"]) for m in messages)   # 生成器写法,与推导式同族
print("-" * 30)
print(f"总消息 {total_count} 条 | 用户消息 {user_count} 条 | 总字符 {char_count}")
