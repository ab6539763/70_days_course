# =============================================
# 用户评论清洗工具 v4(最终版)
# 需求编号:REQ-D02-001
# 作者:你的名字
# 日期:2026-07-06
# 新增:手机号提取与脱敏
# 思路:find("138") 定位 → 切片取 11 位 → 前3后4脱敏 → 替换回原文
# 已知局限:只能识别 138 开头的号码;完美方案是 Day 11 的正则表达式。
#          在代码里诚实标注已知局限,和实现功能同样专业。
# =============================================

raw_comment = """   这个AI客服真是垃圾,回答驴唇不对马嘴!
客服电话13812345678也打不通,   NO ONE CARES!
真是气死我了,做这个产品的都是傻子   
"""

# ---- 流水线 F1~F4(同 v3,压缩书写) ----
text = raw_comment.strip().lower()               # F1+F2 链式调用一行完成

count_total = text.count("垃圾") + text.count("傻子") + text.count("废物")
text = text.replace("垃圾", "**").replace("傻子", "**").replace("废物", "**")   # F3 链式替换

clean_comment = " ".join(text.split())           # F4

# ---- 附加:手机号提取与脱敏 ----
# 第一步:定位。find 返回 "138" 首次出现的索引;-1 表示没找到
pos = clean_comment.find("138")
# 第二步:切片取出从该位置起的 11 个字符(含头不含尾:pos 到 pos+11)
phone = clean_comment[pos:pos + 11]
# 第三步:脱敏——Day 01 预告过的经典切片拼接
masked_phone = phone[:3] + "****" + phone[-4:]
# 第四步:把评论里的明文手机号也替换成脱敏版(隐私不落地)
clean_comment = clean_comment.replace(phone, masked_phone)

# ---- 清洗报告 ----
print("=" * 46)
print(f"{'清洗报告':^42}")
print("=" * 46)
print(f"{'原文长度':<10}{len(raw_comment)} 字符")
print(f"{'净文长度':<10}{len(clean_comment)} 字符")
print(f"{'敏感词处理':<10}{count_total} 个")
print(f"{'手机号脱敏':<10}{masked_phone}")
print("-" * 46)
print("净文预览:")
print(clean_comment)
print("=" * 46)
