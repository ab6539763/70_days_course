# =============================================
# Day 04 · 下午演示代码:元组与集合
# 文件:tuple_set_demo.py
# =============================================

# ============ 元组 tuple:焊死的列表(有序、不可变) ============

point = (3, 5)                       # 圆括号创建
rgb = (255, 128, 0)
single = (42,)                       # ⚠️ 单元素必须带逗号!(42) 只是括号包着的数字
also = 1, 2, 3                       # 圆括号可省略:逗号才是元组的本体

# 读操作与列表完全一致(序列协议)
print(point[0], rgb[-1], len(rgb), 255 in rgb)    # 3 0 3 True

# 写操作全部禁止:
# point[0] = 4            # TypeError
# point.append(7)         # AttributeError:根本没有这个方法

# 拆包:元组最常用的姿势
x, y = point
print(x, y)                          # 3 5

# 变量交换的 Python 名场面
a, b = 1, 2
a, b = b, a                          # 右边先打包成元组,再拆给左边
print(a, b)                          # 2 1

# 元组存在的意义:①声明"这组数据是整体别动" ②能当字典的键(Day 05)
# ③函数多返回值的载体(Day 06):return name, age 返回的就是元组

# ============ 集合 set:自动去重的袋子(无序、不重复) ============

tags = {"python", "ai", "python", "llm", "ai"}
print(tags)                          # 重复的自动只留一份;顺序不保证

empty_set = set()                    # 空集合唯一正确写法({} 被字典占用)
nums = set([1, 2, 2, 3, 3, 3])       # 列表转集合,顺手去重
print(nums)                          # {1, 2, 3}

tags.add("rag")                      # 加(无序,没有 append)
tags.discard("java")                 # 删:不存在也不报错(remove 会 KeyError)

# ---- 绝活一:去重一行流(Day 52 微调数据清洗的核心工序) ----
emails = ["a@x.com", "b@y.com", "a@x.com", "c@z.com", "b@y.com"]
unique = list(set(emails))
print(unique)                        # 三个不重复邮箱(顺序可能变)
# 保序去重:今天的手工版 ——
kept = []
for e in emails:
    if e not in kept:
        kept.append(e)
print(kept)                          # 保持首次出现的顺序
# 明天解锁一行流:list(dict.fromkeys(emails))

# ---- 绝活二:集合运算 ----
skills_have = {"python", "sql", "excel"}             # 你会的
skills_need = {"python", "langchain", "docker"}      # 岗位要的
print(skills_have & skills_need)     # 交集:{'python'}         匹配的技能
print(skills_need - skills_have)     # 差集:待学清单!
print(skills_have | skills_need)     # 并集:全部技能
print(skills_have ^ skills_need)     # 对称差:只有一方有的
# Day 34 RAG 评估的"检索命中率" = 引用文档集合 & 标准文档集合

# ---- 绝活三:光速查"在不在" ----
# 列表挨个比对,集合"算出"位置(哈希,明天讲透)。
# 数据量大 + 高频查在不在 = 用集合。10 万违禁词的场景,速度差千倍。
big_set = set(range(100000))
print(99999 in big_set)              # True,瞬间完成
