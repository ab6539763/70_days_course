# =============================================
# Day 03 作业 · 编程题 4:批量邮箱体检
# 考点:for 遍历列表 + 多条件校验 + 计数器 + 合格率计算
# 伏笔:对"一批数据"逐条校验再统计,是 Day 52 微调数据清洗的骨架
# =============================================

emails = ["zhang@deepseek.com", "invalid-email", "li.si@qwen.ai", "@nouser.com", "wang@deepseek.com"]

valid_count = 0                        # 合格计数器

for email in emails:
    # 两条校验规则,用 and 合并成一个判断:
    # ① 含且只含一个 @;② @ 不在开头
    is_valid = email.count("@") == 1 and not email.startswith("@")

    if is_valid:
        print(f"[合格] {email}")
        valid_count += 1
    else:
        print(f"[不合格] {email}")

total = len(emails)                    # len 对列表同样适用:元素个数
print("-" * 30)
print(f"合格 {valid_count}/{total},合格率 {valid_count / total:.0%}")
