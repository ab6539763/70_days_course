# =============================================
# Day 03 · 上午演示代码 1:条件判断全家桶
# 文件:if_demo.py
# =============================================

# ---- 1. 最小 if:兑现 Day 01 思考题 2 ----
age = int(input("请输入你的年龄:"))
if age < 0 or age > 120:
    print("年龄不合法,请检查输入!")

# ---- 2. if / else:二选一 ----
api_key = input("请输入 API Key:").strip()      # 进门先清洗(Day 02 习惯)
if api_key.startswith("sk-"):                    # Day 02 的方法今天上岗
    print("Key 格式正确,准备调用大模型……")
else:
    print("Key 格式错误:应以 sk- 开头")

# ---- 3. elif 多路分支:从上到下,命中即退出 ----
score = int(input("请输入分数(0-100):"))
if score >= 90:
    grade = "优秀"
elif score >= 80:          # 走到这里,隐含 score < 90 已成立,不用重复写
    grade = "良好"
elif score >= 60:
    grade = "及格"
else:                      # 兜底:以上全不成立
    grade = "不及格"
print(f"分数 {score},等级:{grade}")

# ⚠️ 反面教材(注释保留,体会"顺序错了逻辑就错"):
# if score >= 60: grade = "及格"      ← 95 分会在第一关被拦截!
# elif score >= 90: grade = "优秀"    ← 永远走不到

# ---- 4. 嵌套 vs 平铺:超过三层嵌套要重构 ----
is_vip = input("是否 VIP 用户?(y/n):").strip().lower() == "y"
wait_count = int(input("当前排队人数:"))

# 平铺版(推荐):合并条件,四条分支一目了然
if is_vip and wait_count > 10:
    print("VIP 通道也繁忙,已为您升级专属客服")
elif is_vip:
    print("已接入 VIP 专属通道")
elif wait_count > 50:
    print("当前繁忙,建议先试试 AI 客服")      # ← 未来接入大模型应用的位置
else:
    print(f"排队中,前方 {wait_count} 人")

# ---- 5. 真值判断上岗:非空才处理(Day 14 主循环预演) ----
user_input = input("请输入问题(直接回车退出):").strip()
if user_input:                    # 等价于 != "",但更 Pythonic
    print(f"收到问题:{user_input}")
else:
    print("未输入内容,再见")
