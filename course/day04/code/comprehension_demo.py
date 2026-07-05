# =============================================
# Day 04 · 上午演示代码 2:列表推导式
# 文件:comprehension_demo.py
# 语法:[表达式 for x in 序列 if 条件]
#        ①装什么   ②从哪来    ③什么条件才要
# =============================================

nums = [1, 2, 3, 4, 5, 6]

# ---- 三行版(Day 03 累加器模式)与一行版对照 ----
kept = []
for n in nums:
    if n % 2 == 0:
        kept.append(n)
print(kept)                                       # [2, 4, 6]

kept = [n for n in nums if n % 2 == 0]            # 同一件事的折叠写法
print(kept)                                       # [2, 4, 6]

# ---- 用法一:过滤 ----
scores = [92, 45, 85, 58, 77]
passed = [s for s in scores if s >= 60]
print(passed)               # [92, 85, 77]

# ---- 用法二:加工 ----
words = ["  RAG ", " Agent", "Prompt  "]
cleaned = [w.strip().lower() for w in words]      # Day 02 清洗组合拳进推导式
print(cleaned)              # ['rag', 'agent', 'prompt']

# ---- 过滤 + 加工同时上:真实项目清洗用户数据的标准写法 ----
raw = ["  张三 ", "", "  ", "李四", "王五  "]
names = [x.strip() for x in raw if x.strip()]     # 剥后非空才要,装进去的是剥过的
print(names)                # ['张三', '李四', '王五']

# ---- 配合 range:批量生成 ----
squares = [i ** 2 for i in range(1, 6)]
print(squares)              # [1, 4, 9, 16, 25]

# ---- 带 if-else 的加工(注意:if-else 放前面,过滤 if 放后面) ----
labels = ["及格" if s >= 60 else "不及格" for s in scores]
print(labels)               # ['及格', '不及格', '及格', '不及格', '及格']

# ---- 尺度守则 ----
# 超过一屏宽 / 嵌套两层 for / 逻辑要想三秒 → 改回多行 for。
# 推导式的使命是"简单批量操作一眼看懂",不是炫技压行。

# 【预告】Day 28 文档分块后的批量清洗,就是这个形状:
# chunks = [c.strip() for c in raw_chunks if len(c.strip()) > 20]
