# Day 4: 核心数据结构上——列表

> **培训阶段**: 第一阶段 Python 编程基础 | **第 1 周** | **学习时长**: 约 6-8 小时  
> **今日关键词**: list 增删改查、切片、排序、列表推导式、待办事项管理器

---

## 📍 课程导航

### 上节回顾
在 **Day 3** 中，你掌握了 `if/elif/else` 条件分支、`while`/`for` 循环，完成了猜数字游戏、九九乘法表和简易菜单系统。菜单中的多个选项已经暗示了「一组数据」的需求——今天学习的 **列表（list）** 正是存储和管理一组数据的利器。

### 本节学习目标
完成本日学习后，你将能够：

1. 创建列表并进行增删改查（CRUD）操作
2. 使用列表切片提取子列表
3. 对列表进行排序和反转
4. 掌握列表推导式——Python 最优雅的语法特性之一
5. 使用 `for` 循环遍历列表
6. 独立完成「待办事项管理器」命令行项目

### 与后续课程的衔接
- **Day 5** 将学习字典（dict）——列表存「一组值」，字典存「键值对」，两者配合使用
- **Day 6** 将把今天的待办管理器重构为函数式结构
- **Day 12** 调用 API 时，消息历史用列表存储：`messages = [{"role": "user", "content": "..."}]`
- **Day 25+** RAG 开发中，文档块（chunks）通常用列表管理

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：列表基础

#### 1.1 创建列表

```python
# day04/list_create.py

# 空列表
empty = []
also_empty = list()

# 数字列表
numbers = [1, 2, 3, 4, 5]

# 混合类型列表（Python 列表可以包含不同类型）
mixed = ["张三", 25, True, 3.14]

# 嵌套列表
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# 字符串列表（大模型开发中最常见）
messages = [
    "你好，请介绍一下 Python",
    "Python 是一种高级编程语言...",
    "能给我一个 Hello World 示例吗？"
]

print(type(numbers))   # <class 'list'>
print(len(numbers))    # 5
```

#### 1.2 访问元素

```python
# day04/list_access.py
fruits = ["苹果", "香蕉", "橙子", "葡萄", "西瓜"]

# 索引访问（与字符串相同）
print(fruits[0])    # 苹果
print(fruits[-1])   # 西瓜（最后一个）
print(fruits[-2])   # 葡萄

# 修改元素
fruits[1] = "芒果"
print(fruits)  # ['苹果', '芒果', '橙子', '葡萄', '西瓜']
```

#### 1.3 列表切片

```python
# day04/list_slice.py
nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

print(nums[2:5])     # [2, 3, 4]
print(nums[:3])      # [0, 1, 2]
print(nums[5:])      # [5, 6, 7, 8, 9]
print(nums[::2])     # [0, 2, 4, 6, 8]
print(nums[::-1])    # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

# 切片复制（浅拷贝）
copy = nums[:]
print(copy)  # 完整复制
```

#### 1.4 遍历列表

```python
# day04/list_iterate.py
tasks = ["学 Python", "学 Prompt", "做项目", "找工作"]

# 方式一：直接遍历
for task in tasks:
    print(f"📌 {task}")

# 方式二：带索引
for i, task in enumerate(tasks):
    print(f"{i + 1}. {task}")

# 方式三：按索引
for i in range(len(tasks)):
    print(f"任务 {i}: {tasks[i]}")
```

---

### 9:45 - 10:30 | 模块二：列表增删改查

#### 2.1 添加元素

```python
# day04/list_add.py
todos = ["买牛奶", "写代码"]

# append：末尾添加单个元素
todos.append("健身")
print(todos)  # ['买牛奶', '写代码', '健身']

# insert：指定位置插入
todos.insert(0, "起床")  # 插入到最前面
print(todos)  # ['起床', '买牛奶', '写代码', '健身']

# extend：末尾添加多个元素
todos.extend(["做饭", "阅读"])
print(todos)  # ['起床', '买牛奶', '写代码', '健身', '做饭', '阅读']

# + 运算符（创建新列表，不修改原列表）
more = todos + ["睡觉"]
print(len(more))   # 7
print(len(todos))  # 6（原列表未变）
```

#### 2.2 删除元素

```python
# day04/list_remove.py
items = ["A", "B", "C", "B", "D"]

# remove：按值删除（只删第一个匹配）
items.remove("B")
print(items)  # ['A', 'C', 'B', 'D']

# pop：按索引删除并返回该元素
last = items.pop()      # 删除最后一个
print(last)   # D
print(items)  # ['A', 'C', 'B']

first = items.pop(0)    # 删除第一个
print(first)  # A

# del：按索引删除
del items[1]
print(items)  # ['C', 'B']

# clear：清空列表
items.clear()
print(items)  # []
```

#### 2.3 查找与统计

```python
# day04/list_search.py
scores = [85, 92, 78, 92, 88, 92]

# in 运算符
print(92 in scores)      # True
print(100 in scores)     # False

# index：查找索引
print(scores.index(78))  # 2

# count：统计出现次数
print(scores.count(92))  # 3

# min / max / sum
print(f"最低: {min(scores)}, 最高: {max(scores)}, 总分: {sum(scores)}")
print(f"平均: {sum(scores) / len(scores):.1f}")
```

#### 2.4 与大模型开发的联系

```python
# 消息历史管理（Day 12/14 的核心数据结构）
messages = []

# 添加用户消息
messages.append({"role": "user", "content": "什么是 RAG？"})

# 添加助手回复
messages.append({"role": "assistant", "content": "RAG 是检索增强生成..."})

# 查看对话历史
for msg in messages:
    print(f"[{msg['role']}]: {msg['content'][:50]}...")
```

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：排序与列表推导式

#### 3.1 排序

```python
# day04/list_sort.py
nums = [3, 1, 4, 1, 5, 9, 2, 6]

# sort()：原地排序（修改原列表）
nums.sort()
print(nums)  # [1, 1, 2, 3, 4, 5, 6, 9]

nums.sort(reverse=True)
print(nums)  # [9, 6, 5, 4, 3, 2, 1, 1]

# sorted()：返回新列表（不修改原列表）
original = [3, 1, 4, 1, 5]
sorted_list = sorted(original)
print(original)     # [3, 1, 4, 1, 5]（未变）
print(sorted_list)  # [1, 1, 3, 4, 5]

# 字符串排序
names = ["张三", "李四", "王五", "赵六"]
names.sort()
print(names)

# reverse：反转
nums = [1, 2, 3, 4, 5]
nums.reverse()
print(nums)  # [5, 4, 3, 2, 1]
```

#### 3.2 列表推导式（List Comprehension）

列表推导式是 Python 最优雅的语法之一，用一行代码完成「遍历 + 过滤 + 变换」：

```python
# day04/comprehension.py

# 基本形式：[表达式 for 变量 in 序列]
squares = [x ** 2 for x in range(1, 6)]
print(squares)  # [1, 4, 9, 16, 25]

# 带条件过滤：[表达式 for 变量 in 序列 if 条件]
evens = [x for x in range(20) if x % 2 == 0]
print(evens)  # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# 字符串处理
words = ["hello", "world", "python", "ai"]
upper_words = [w.upper() for w in words]
print(upper_words)  # ['HELLO', 'WORLD', 'PYTHON', 'AI']

# 过滤长单词
long_words = [w for w in words if len(w) > 4]
print(long_words)  # ['hello', 'world', 'python']

# 对比：传统写法 vs 推导式
# 传统
result = []
for w in words:
    if len(w) > 4:
        result.append(w.upper())

# 推导式（一行搞定）
result = [w.upper() for w in words if len(w) > 4]
```

#### 3.3 实用推导式示例

```python
# day04/comprehension_practice.py

# 从大模型 API 响应中提取内容
responses = [
    {"role": "user", "content": "你好"},
    {"role": "assistant", "content": "你好！有什么可以帮你的？"},
    {"role": "user", "content": "介绍一下 Python"},
]

# 提取所有 user 消息
user_messages = [r["content"] for r in responses if r["role"] == "user"]
print(user_messages)

# 计算文本长度
lengths = [len(r["content"]) for r in responses]
print(lengths)  # [2, 13, 11]

# 二维列表展平
matrix = [[1, 2], [3, 4], [5, 6]]
flat = [num for row in matrix for num in row]
print(flat)  # [1, 2, 3, 4, 5, 6]
```

#### 3.4 列表常用方法速查

| 方法 | 功能 | 示例 |
|------|------|------|
| `.append(x)` | 末尾添加 | `[1,2].append(3)` → `[1,2,3]` |
| `.insert(i, x)` | 指定位置插入 | `[1,3].insert(1,2)` → `[1,2,3]` |
| `.extend(lst)` | 末尾扩展 | `[1].extend([2,3])` → `[1,2,3]` |
| `.remove(x)` | 按值删除 | `[1,2,3].remove(2)` → `[1,3]` |
| `.pop(i)` | 按索引删除并返回 | `[1,2,3].pop()` → `3` |
| `.sort()` | 原地排序 | |
| `.reverse()` | 原地反转 | |
| `.index(x)` | 查找索引 | |
| `.count(x)` | 统计次数 | |
| `.copy()` | 浅拷贝 | |
| `.clear()` | 清空 | |

---

## 🌇 下午实操（14:00 - 17:30）

### 14:00 - 17:00 | 实操项目：待办事项管理器

#### 项目需求

1. 添加待办事项（支持优先级：高/中/低）
2. 查看所有待办（按优先级排序显示）
3. 标记待办为已完成
4. 删除待办事项
5. 统计待办完成情况
6. 搜索待办（按关键词）

#### 数据结构设计

```python
# 每个待办事项是一个字典（Day 5 会深入学习字典）
todo = {
    "id": 1,
    "title": "学习 Python 列表",
    "priority": "高",      # 高/中/低
    "done": False,
    "created": "2026-07-06"
}
# 所有待办存储在列表中
todos = [todo, ...]
```

#### 参考代码

创建文件 `day04/todo_manager.py`：

```python
"""
Day 4 实操项目：待办事项管理器
练习：列表 CRUD、排序、列表推导式、字典（预习）
"""

from datetime import date

# ===== 数据存储 =====
todos = []          # 待办列表
next_id = 1         # 自增 ID

PRIORITY_ORDER = {"高": 0, "中": 1, "低": 2}
PRIORITY_ICONS = {"高": "🔴", "中": "🟡", "低": "🟢"}


# ===== 功能函数 =====

def add_todo():
    """添加待办事项"""
    global next_id
    title = input("待办标题: ").strip()
    if not title:
        print("⚠️ 标题不能为空")
        return

    print("优先级: 1-高  2-中  3-低")
    p_choice = input("选择 (默认中): ").strip()
    priority_map = {"1": "高", "2": "中", "3": "低", "": "中"}
    priority = priority_map.get(p_choice, "中")

    todo = {
        "id": next_id,
        "title": title,
        "priority": priority,
        "done": False,
        "created": str(date.today()),
    }
    todos.append(todo)
    next_id += 1
    print(f"✅ 已添加: {title}")


def list_todos(show_done=None):
    """查看待办列表"""
    if not todos:
        print("📭 暂无待办事项")
        return

    # 过滤
    if show_done is True:
        filtered = [t for t in todos if t["done"]]
        label = "已完成"
    elif show_done is False:
        filtered = [t for t in todos if not t["done"]]
        label = "未完成"
    else:
        filtered = todos
        label = "全部"

    if not filtered:
        print(f"📭 没有{label}的待办")
        return

    # 按优先级排序
    sorted_todos = sorted(filtered, key=lambda t: PRIORITY_ORDER[t["priority"]])

    print(f"\n📋 {label}待办 ({len(sorted_todos)} 项)")
    print("-" * 55)
    for t in sorted_todos:
        icon = PRIORITY_ICONS[t["priority"]]
        status = "✅" if t["done"] else "⬜"
        print(f"  {status} [{t['id']:>3}] {icon} {t['title']:<25} ({t['created']})")
    print("-" * 55)


def complete_todo():
    """标记完成"""
    list_todos(show_done=False)
    if not any(not t["done"] for t in todos):
        return

    try:
        todo_id = int(input("请输入要完成的 ID: "))
    except ValueError:
        print("⚠️ 请输入有效数字")
        return

    for t in todos:
        if t["id"] == todo_id:
            t["done"] = True
            print(f"✅ 已完成: {t['title']}")
            return
    print(f"⚠️ 未找到 ID={todo_id} 的待办")


def delete_todo():
    """删除待办"""
    list_todos()
    if not todos:
        return

    try:
        todo_id = int(input("请输入要删除的 ID: "))
    except ValueError:
        print("⚠️ 请输入有效数字")
        return

    for i, t in enumerate(todos):
        if t["id"] == todo_id:
            removed = todos.pop(i)
            print(f"🗑️ 已删除: {removed['title']}")
            return
    print(f"⚠️ 未找到 ID={todo_id} 的待办")


def search_todos():
    """搜索待办"""
    keyword = input("搜索关键词: ").strip().lower()
    if not keyword:
        return

    results = [t for t in todos if keyword in t["title"].lower()]
    if not results:
        print(f"🔍 未找到包含 '{keyword}' 的待办")
        return

    print(f"\n🔍 搜索结果 ({len(results)} 项)")
    for t in results:
        status = "✅" if t["done"] else "⬜"
        print(f"  {status} [{t['id']}] {t['title']}")


def show_stats():
    """统计信息"""
    total = len(todos)
    done = len([t for t in todos if t["done"]])
    pending = total - done

    print(f"\n📊 待办统计")
    print(f"  总计: {total}")
    print(f"  已完成: {done}")
    print(f"  未完成: {pending}")
    if total > 0:
        print(f"  完成率: {done / total:.0%}")

    # 按优先级统计
    for p in ["高", "中", "低"]:
        count = len([t for t in todos if t["priority"] == p and not t["done"]])
        if count:
            print(f"  {PRIORITY_ICONS[p]} {p}优先级未完成: {count}")


# ===== 主程序 =====

def main():
    print("=" * 40)
    print("     📝 待办事项管理器 v1.0")
    print("=" * 40)

    while True:
        print("\n1. 添加待办  2. 查看全部  3. 查看未完成")
        print("4. 标记完成  5. 删除待办  6. 搜索")
        print("7. 统计信息  0. 退出")
        choice = input("请选择: ").strip()

        actions = {
            "1": add_todo,
            "2": lambda: list_todos(),
            "3": lambda: list_todos(show_done=False),
            "4": complete_todo,
            "5": delete_todo,
            "6": search_todos,
            "7": show_stats,
        }

        if choice == "0":
            pending = len([t for t in todos if not t["done"]])
            if pending:
                print(f"⚠️ 你还有 {pending} 项未完成待办！")
            print("再见！")
            break
        elif choice in actions:
            actions[choice]()
        else:
            print("⚠️ 无效选择")


if __name__ == "__main__":
    main()
```

#### 运行效果示例

```
========================================
     📝 待办事项管理器 v1.0
========================================

1. 添加待办  2. 查看全部  3. 查看未完成
...
请选择: 1
待办标题: 学习 Python 列表
优先级: 1-高  2-中  3-低
选择 (默认中): 1
✅ 已添加: 学习 Python 列表

请选择: 2

📋 全部待办 (1 项)
-------------------------------------------------------
  ⬜ [  1] 🔴 学习 Python 列表           (2026-07-06)
-------------------------------------------------------
```

---

### 17:00 - 17:30 | 扩展练习

#### 练习：列表推导式挑战

```python
# 1. 生成 1-20 中能被 3 整除的数的平方
result = [x**2 for x in range(1, 21) if x % 3 == 0]
print(result)  # [9, 36, 81, 144, 225, 324, 361]

# 2. 将字符串列表按长度降序排列
words = ["AI", "Python", "LLM", "RAG", "Agent"]
sorted_words = sorted(words, key=len, reverse=True)
print(sorted_words)  # ['Python', 'Agent', 'LLM', 'RAG', 'AI']

# 3. 提取文件名列表
paths = ["/docs/readme.md", "/src/main.py", "/data/train.json"]
filenames = [p.split("/")[-1] for p in paths]
print(filenames)  # ['readme.md', 'main.py', 'train.json']
```

---

## 🌙 晚自习（19:00 - 21:00）

### 19:00 - 20:00 | 列表进阶思考

#### 浅拷贝 vs 深拷贝

```python
# 浅拷贝：只复制第一层
original = [1, 2, [3, 4]]
shallow = original.copy()  # 或 original[:]
shallow[2][0] = 99
print(original)  # [1, 2, [99, 4]] — 嵌套列表被共享！

# 深拷贝：完全独立
import copy
deep = copy.deepcopy(original)
deep[2][0] = 0
print(original)  # [1, 2, [99, 4]] — 不受影响
```

### 20:00 - 21:00 | 自习

- 完成待办事项管理器
- 尝试用列表推导式重写项目中的过滤逻辑
- Git 提交：`git commit -m "Day 4: 待办事项管理器"`

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | 列表创建与基本操作 | |
| 2 | 索引访问与修改 | |
| 3 | 列表切片 | |
| 4 | append/insert/extend 添加 | |
| 5 | remove/pop/del/clear 删除 | |
| 6 | index/count/in 查找 | |
| 7 | sort/sorted/reverse 排序 | |
| 8 | 列表推导式基本语法 | |
| 9 | 带条件的列表推导式 | |
| 10 | for 循环遍历列表 | |
| 11 | 待办事项管理器项目 | |

---

## 📝 课后作业

### 必做题

1. **待办事项管理器**：完成下午项目，所有功能正常运行
2. **列表推导式练习**：完成以下推导式
   - 1-100 中所有奇数
   - 字符串列表 `["hello", "world", "ai"]` 每个元素的长度
   - 从 `[1,2,3,4,5,6,7,8,9,10]` 中筛选大于 5 的偶数
3. **Git 提交**：推送到 GitHub

### 选做题

4. **学生成绩管理**：用列表存储多个学生成绩，支持添加、删除、排名、计算平均分
5. **词频统计**：输入一段文本，统计每个单词出现次数（用列表实现）

---

## 💡 常见问题 FAQ

**Q1: append() 和 extend() 有什么区别？**

A: `append()` 将整个对象作为一个元素添加；`extend()` 将可迭代对象的每个元素分别添加。`[1,2].append([3,4])` → `[1,2,[3,4]]`；`[1,2].extend([3,4])` → `[1,2,3,4]`。

**Q2: sort() 和 sorted() 有什么区别？**

A: `sort()` 原地修改列表，返回 `None`；`sorted()` 返回新列表，原列表不变。需要保留原列表时用 `sorted()`。

**Q3: 列表推导式会不会太难读？**

A: 简单的一行推导式非常 Pythonic；过于复杂的建议拆成 for 循环。经验法则：不超过两个 for 和一个 if。

**Q4: 为什么待办项目用字典存每个待办，而不是列表？**

A: 字典的键值对结构更适合表示「有多个属性的对象」。明天 Day 5 会系统学习字典。

**Q5: 列表和字符串的切片语法一样吗？**

A: 完全一样！但字符串切片返回字符串，列表切片返回列表。字符串不可变，列表可变。

---

## 🔮 明日预习

**Day 5: 核心数据结构下——字典与 JSON**

明天你将学习：

- 字典（dict）的创建与操作
- JSON 格式详解——**大模型 API 交互的核心数据格式**
- `json` 模块的使用
- 解析 API 返回的 JSON 数据

**预习建议**：今天待办项目中每个 todo 是字典、所有 todo 存在列表中——思考这种「列表套字典」的结构在 API 数据中如何出现。

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 4*
