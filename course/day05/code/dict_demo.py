# =============================================
# Day 05 · 上午演示代码 1:字典的增删改查与遍历
# 文件:dict_demo.py
# =============================================

# ---- 1. 从昨天购物车的痛点进入 ----
# 昨天:元组列表,查一个价格要遍历
prices_old = [("苹果", 5), ("牛奶", 12), ("面包", 8)]
# 今天:字典,按名字直接取,商品再多也是一步
prices = {"苹果": 5, "牛奶": 12, "面包": 8}
print(prices["苹果"])               # 5

# 三条基本法则:键唯一(重复则覆盖)、键必须不可变、值随便

# ---- 2. 增、改:同一个动作 ----
user = {"name": "张三", "age": 28}
user["city"] = "上海"               # 键不存在 → 增
user["age"] = 29                    # 键已存在 → 改(覆盖)
print(user)

# 从空字典逐步构建(下午组装 API 请求体的套路)
request = {}
request["model"] = "deepseek-chat"
request["temperature"] = 0.7
print(request)

# ---- 3. 查:方括号 vs get(今天第一个重点抉择) ----
print(user["name"])                     # 键理应存在 → 方括号,缺了就该崩(报警)
# print(user["email"])                  # KeyError!
print(user.get("email"))                # None:键可能没有 → get,不崩
print(user.get("email", "未填写"))       # 带默认值
print(user.get("name", "未填写"))        # 键存在时默认值不生效
# 心法:对必要字段严格(方括号),对可选字段宽容(get)

# ---- 4. 删 ----
user["temp"] = "草稿"
removed = user.pop("temp")              # 删并递给你
print(removed)
user.pop("nothing", None)               # 带默认值:不存在也不崩
# del user["city"] 也能删,不递给你

# ---- 5. in 查的是"键" ----
print("name" in user)                   # True
print("张三" in user)                    # False:"张三"是值不是键
print("张三" in user.values())           # True:查值要显式说明
print(len(user))                        # 键值对个数

# ---- 6. 遍历三姿势 ----
model_prices = {"deepseek-chat": 1.0, "gpt-4o": 18.0, "qwen-plus": 4.0}

for name in model_prices:               # 姿势一:直接 for → 只出键
    print(name)

for name, price in model_prices.items():    # 姿势二:.items() 键值一起(最常用)
    print(f"{name}:{price} 元/百万token")

total = sum(model_prices.values())      # 姿势三:只要值
print(f"均价:{total / len(model_prices):.1f}")

# ---- 7. 保序去重一行流(昨天答疑的兑现) ----
emails = ["a@x.com", "b@y.com", "a@x.com"]
unique = list(dict.fromkeys(emails))    # 键不重复 + 保插入顺序
print(unique)

# ---- 8. 哈希速览 ----
# 列表查找:挨个比对(线性);字典/集合:键→哈希函数→抽屉号,一步到位。
# 所以:键必须不可变(变了哈希就变,东西找不回);集合无序(按哈希安家)。
# 用列表当键的下场:
# bad = {["a", "b"]: 1}      # TypeError: unhashable type: 'list'
good = {("a", "b"): 1}       # 元组可以当键(不可变)
print(good[("a", "b")])
