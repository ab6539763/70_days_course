# =============================================
# Day 05 作业 · 编程题 1:购物车终极版
# 考点:字典计数器模式(重中之重)、get 防御、items 遍历
# =============================================

prices = {"苹果": 5, "牛奶": 12, "面包": 8}
cart = ["苹果", "牛奶", "苹果", "面包", "牛奶", "苹果", "榴莲"]   # 混入一个没价格的

# ---- ① 字典计数器模式:遍历 + get 累加 ----
# 每见到一个商品,把它在 counter 里的计数 +1;
# 第一次见到时 counter 里还没有它,get 的默认值 0 兜底
counter = {}
for item in cart:
    counter[item] = counter.get(item, 0) + 1
print(counter)          # {'苹果': 3, '牛奶': 2, '面包': 1, '榴莲': 1}
# 这个三行模式请背下来:词频统计(Day 11)、投票计数,全是它

# ---- ② 结算:遍历计数器,查价格表 ----
total = 0
for item, qty in counter.items():
    if item not in prices:                 # ③ 防御:价格表里没有的商品
        print(f"{item} x{qty}:暂无价格,跳过")
        continue
    subtotal = prices[item] * qty          # 有价格:方括号放心取
    total += subtotal
    print(f"{item} x{qty} = {subtotal} 元")

print("-" * 20)
print(f"总计:{total} 元")
