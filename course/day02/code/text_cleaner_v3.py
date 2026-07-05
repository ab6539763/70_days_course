# =============================================
# 用户评论清洗工具 v3
# 需求编号:REQ-D02-001
# 新增:F4 空格规范化 + 对齐的清洗报告
# 关键技巧:" ".join(x.split()) 组合拳、f-string 对齐
# =============================================

raw_comment = """   这个AI客服真是垃圾,回答驴唇不对马嘴!
客服电话13812345678也打不通,   NO ONE CARES!
真是气死我了,做这个产品的都是傻子   
"""

# ---- 流水线 F1~F3(同 v2) ----
step1 = raw_comment.strip()
step2 = step1.lower()

count_1 = step2.count("垃圾")
step3 = step2.replace("垃圾", "**")
count_2 = step3.count("傻子")
step3 = step3.replace("傻子", "**")
count_3 = step3.count("废物")
step3 = step3.replace("废物", "**")
total_replaced = count_1 + count_2 + count_3

# ---- F4:空格规范化 ----
# split() 不带参数 = 按任意空白拆(连续空格/换行一并吞掉)
# " ".join(...) = 用单个空格拼回
# 一进一出,所有"多余空白"都被规范成单个空格
# 副作用说明:换行也会被拍平成空格——对"单条评论"这是可接受的;
# Day 28 处理"整篇文档"时会改用逐行清洗保住段落结构,策略因数据而异
clean_comment = " ".join(step3.split())

# ---- 清洗报告 ----
# 用 f-string 对齐语法排版;:<10 表示左对齐占 10 格
print("=" * 46)
print(f"{'清洗报告':^42}")
print("=" * 46)
print(f"{'原文长度':<10}{len(raw_comment)} 字符")
print(f"{'净文长度':<10}{len(clean_comment)} 字符")
print(f"{'敏感词处理':<10}{total_replaced} 个")
print("-" * 46)
print("净文预览:")
print(clean_comment)
print("=" * 46)
