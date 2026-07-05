# =============================================
# Day 04 · 上午演示代码 1:列表的增删改查与排序
# 文件:list_demo.py
# =============================================

# ---- 1. 创建与基本操作(全是 Day 02 的老功夫平移过来:序列协议) ----
banned_words = ["赌博", "诈骗", "刷单"]
scores = [92, 85, 77, 60, 88]
empty = []                                       # 空列表:累积数据的起点

print(len(scores))          # 5      元素个数
print(scores[0])            # 92     索引从 0 开始
print(scores[-1])           # 88     负索引
print(scores[1:3])          # [85, 77]  切片:含头不含尾,返回新列表
print(92 in scores)         # True   包含判断

# ---- 2. 增:append / insert / extend ----
todo = ["学列表", "写作业"]
todo.append("刷 LeetCode")                       # 尾追:使用率 90%
todo.insert(0, "复习昨天的循环")                  # 插队到最前
todo.extend(["提交 Git", "预习字典"])             # 并入另一个列表
print(todo)

# append vs extend 的经典混淆:
box = [1, 2]
box.append([3, 4])          # 整个列表当"一个元素"塞进去 → 嵌套
print(box)                  # [1, 2, [3, 4]]
box2 = [1, 2]
box2.extend([3, 4])         # 拆开逐个并入
print(box2)                 # [1, 2, 3, 4]

# ---- 3. 删:remove / pop / clear / del ----
todo = ["复习", "学列表", "写作业", "摸鱼", "提交 Git"]
todo.remove("摸鱼")                              # 按值删;不存在会 ValueError,先 in 检查
done = todo.pop(0)                               # 按位置删,并把删掉的"递给你"
print(f"已完成:{done}")
last = todo.pop()                                # 无参:删最后一个
print(f"弹出:{last}")
nums = [10, 20, 30, 40, 50]
del nums[0]                                      # del 语句:按位置删,不递给你
del nums[1:3]                                    # 还能删切片
print(nums)                 # [20, 50]

# ---- 4. 改与查 ----
scores = [92, 85, 77, 60, 88]
scores[3] = 65              # 索引直接赋值——列表可变,字符串做不到
print(scores.index(77))     # 2     按值找位置(找不到 ValueError)
print([1, 2, 2, 3, 2].count(2))    # 3

# ---- 5. 排序:sort(原地) vs sorted(新列表) ----
scores.sort()                                    # 原地升序,返回 None!
print(scores)
scores.sort(reverse=True)                        # 原地降序
print(scores)

raw = [3, 1, 2]
ordered = sorted(raw)                            # 复制一份再排,原列表不动
print(raw, ordered)         # [3, 1, 2] [1, 2, 3]

result = raw.sort()                              # 经典事故现场
print(result)               # None ← sort 不返回排好的列表!

# key 参数:按"加工后的值"排
words = ["Agent", "rag", "Prompt", "llm"]
print(sorted(words, key=str.lower))              # 忽略大小写排
print(sorted(words, key=len))                    # 按长度排
# Day 33 检索结果按分数排序:sorted(..., key=..., reverse=True)

# ---- 6. 可变性大坑:Day 01"标签模型"伏笔兑现 ----
a = [1, 2, 3]
b = a                       # 贴标签,不是复制!
b.append(4)
print(a)                    # [1, 2, 3, 4] ← a "也变了":本来就是同一个列表
print(id(a) == id(b))       # True  照妖镜:同一个对象

c = a.copy()                # 真副本
c.append(5)
print(a)                    # [1, 2, 3, 4]  安然无恙
print(id(a) == id(c))       # False

# ---- 7. 遍历三姿势 ----
tasks = ["学列表", "写作业", "刷题"]
for task in tasks:                               # 姿势一:直接遍历
    print(task)
for i, task in enumerate(tasks, start=1):        # 姿势二:要编号用 enumerate
    print(f"{i}. {task}")
names = ["张三", "李四", "王五"]
points = [92, 85, 77]
for name, score in zip(names, points):           # 姿势三:两列并排走
    print(f"{name}:{score} 分")

# 铁律:不边遍历边增删。正确姿势:遍历旧的,构建新的
nums = [1, 2, 3, 4, 5, 6]
kept = []
for n in nums:
    if n % 2 == 0:
        kept.append(n)
print(kept)                 # [2, 4, 6]
