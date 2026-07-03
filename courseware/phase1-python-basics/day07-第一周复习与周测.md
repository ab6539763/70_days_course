# Day 7: 第一周复习与周测

> **培训阶段**: 第一阶段 Python 编程基础 | **第 1 周** | **学习时长**: 约 6-8 小时  
> **今日关键词**: 知识串讲、周测、通讯录管理系统、第一周总结

---

## 📍 课程导航

### 上节回顾
第一周（Day 1-6）你学习了 Python 开发环境、变量与数据类型、运算符与字符串、流程控制、列表、字典与 JSON、函数。今天是 **第一周总结日**，通过复习、测试和综合项目检验学习成果。

### 本节学习目标
完成本日学习后，你将能够：

1. 系统回顾第一周所有核心知识点
2. 完成笔试和周测上机题
3. 独立完成「通讯录管理系统」综合项目
4. 识别自己的薄弱环节并制定补强计划
5. 为第二周（Day 8-14）面向对象与 API 调用做好准备

### 与后续课程的衔接
- **Day 8** 开始面向对象编程——用类组织今天通讯录中的联系人数据
- **Day 12** 首次调用大模型 API——第一周的基础将全部派上用场
- **Day 14** 阶段考核项目——综合本周所有技能

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 10:30 | 模块一：第一周知识点串讲

#### 1.1 知识地图

```
Day 1  环境 + 变量 + 基本类型 + print/input
  ↓
Day 2  运算符 + 字符串 + f-string
  ↓
Day 3  if/elif/else + while/for 循环
  ↓
Day 4  列表 list + 列表推导式
  ↓
Day 5  字典 dict + JSON
  ↓
Day 6  函数 def + lambda + 重构
  ↓
Day 7  复习 + 周测 + 综合项目 ← 今天
```

#### 1.2 核心语法速查

**数据类型**

| 类型 | 创建 | 可变？ | 典型用途 |
|------|------|--------|----------|
| int/float | `42`, `3.14` | — | 数值计算 |
| str | `"hello"` | 否 | 文本、Prompt |
| bool | `True/False` | — | 条件判断 |
| list | `[1, 2, 3]` | 是 | 有序数据集合 |
| dict | `{"k": "v"}` | 是 | 键值对、JSON |

**流程控制**

```python
# 条件
if condition:
    ...
elif other:
    ...
else:
    ...

# 循环
for item in sequence:
    ...
while condition:
    ...
    break / continue
```

**函数**

```python
def func(param, default="值"):
    """文档字符串"""
    return result
```

#### 1.3 常见模式回顾

**模式 1：菜单系统**

```python
while True:
    show_menu()
    choice = input("请选择: ")
    if choice == "0":
        break
    elif choice == "1":
        do_something()
```

**模式 2：输入验证**

```python
while True:
    value = input("请输入: ")
    if value.isdigit():
        break
    print("无效输入")
```

**模式 3：列表 CRUD**

```python
items = []
items.append(new_item)      # 增
item = items[index]          # 查
items[index] = updated       # 改
items.pop(index)             # 删
```

**模式 4：JSON 处理**

```python
import json
data = json.loads(json_string)   # 字符串 → Python
text = json.dumps(python_obj)    # Python → 字符串
```

#### 1.4 与大模型开发的知识对应

| 第一周技能 | 大模型开发应用 |
|------------|----------------|
| f-string | Prompt 模板拼接 |
| 列表 | 消息历史 messages[] |
| 字典 | API 请求/响应体 |
| JSON | 所有 API 交互格式 |
| 函数 | 模块化 API 调用逻辑 |
| while 循环 | 多轮对话循环 |

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块二：周测（笔试部分）

#### 笔试题（共 20 题，45 分钟）

**一、选择题（每题 2 分，共 10 题）**

1. `input()` 返回的数据类型是？
   - A. int  B. float  C. str  D. 取决于输入

2. `10 // 3` 的结果是？
   - A. 3.33  B. 3  C. 4  D. 1

3. 以下哪个不是 Python 关键字？
   - A. if  B. for  C. function  D. while

4. `{"a": 1, "b": 2}.get("c", 0)` 的结果是？
   - A. None  B. 0  C. 报错  D. "c"

5. `[x**2 for x in range(5) if x % 2 == 0]` 的结果是？
   - A. [0, 4, 16]  B. [1, 9]  C. [0, 2, 4]  D. [0, 1, 4, 9, 16]

6. `json.loads()` 的作用是？
   - A. Python 对象转 JSON 字符串  B. JSON 字符串转 Python 对象
   - C. 写入 JSON 文件  D. 读取 JSON 文件

7. 以下关于 f-string 的说法正确的是？
   - A. `f"{3.14:.1f}"` 输出 `3.1`
   - B. f-string 是 Python 2 的特性
   - C. f-string 中不能包含表达式
   - D. `f"{name:>10}"` 表示左对齐

8. `break` 的作用是？
   - A. 跳过本次循环  B. 退出整个循环  C. 退出程序  D. 暂停循环

9. 函数中 `return` 不带值时返回？
   - A. 0  B. False  C. None  D. 空字符串

10. 列表 `nums = [3, 1, 4, 1, 5]`，`nums.sort()` 后 `nums` 是？
    - A. `[1, 1, 3, 4, 5]`  B. `[5, 4, 3, 1, 1]`  C. `[3, 1, 4, 1, 5]`  D. `[1, 3, 4, 5]`

**二、填空题（每空 2 分，共 5 题）**

11. Python 中用 ______ 符号开头表示注释。

12. 字符串 `"hello"[1:4]` 的结果是 ______。

13. 将字符串 `"42"` 转为整数使用 ______ 函数。

14. 字典遍历键值对使用 `.______()` 方法。

15. 定义函数使用 ______ 关键字。

**三、简答题（每题 5 分，共 5 题）**

16. 解释 `==` 和 `=` 的区别。

17. 列表和字典分别适合存储什么类型的数据？各举一个例子。

18. 什么是 JSON？它在大模型 API 调用中起什么作用？

19. 解释 `while True` + `break` 模式的适用场景。

20. 为什么要把代码封装成函数？列举两个好处。

<details>
<summary>📋 参考答案</summary>

**选择题**: 1-C 2-B 3-C 4-B 5-A 6-B 7-A 8-B 9-C 10-A

**填空题**: 11-# 12-ell 13-int() 14-items 15-def

**简答题**: 参考讲义相关内容，言之有理即可得分。

</details>

---

## 🌇 下午实操（14:00 - 17:30）

### 14:00 - 15:00 | 周测（上机部分）

#### 上机题（共 5 题，60 分钟）

**题目 1：字符串处理（10 分）**

编写函数 `reverse_words(sentence)`，将句子中每个单词反转，但保持单词顺序。
- 输入：`"Hello AI World"`
- 输出：`"olleH IA dlroW"`

**题目 2：条件与循环（10 分）**

编写程序，输出 1-100 之间所有能被 3 整除但不能被 5 整除的数。

**题目 3：列表操作（15 分）**

给定学生成绩列表 `scores = [85, 92, 78, 95, 88, 72, 90]`，编写程序：
- 计算平均分（保留 1 位小数）
- 找出最高分和最低分
- 用列表推导式找出所有高于平均分的成绩

**题目 4：字典与 JSON（15 分）**

编写程序，将以下 Python 字典转为 JSON 字符串，再解析回来，验证数据一致性：

```python
data = {
    "course": "LLM开发",
    "week": 1,
    "topics": ["Python", "JSON", "函数"],
    "completed": True
}
```

**题目 5：函数综合（20 分）**

编写函数 `analyze_text(text)`，返回一个字典，包含：
- `chars`: 字符数
- `words`: 单词数
- `lines`: 行数
- `most_common_char`: 出现最多的字符（忽略空格）

#### 上机题参考解答

```python
# day07/exam_solutions.py

# 题目 1
def reverse_words(sentence):
    words = sentence.split()
    reversed_words = [w[::-1] for w in words]
    return " ".join(reversed_words)

# 题目 2
for i in range(1, 101):
    if i % 3 == 0 and i % 5 != 0:
        print(i, end=" ")

# 题目 3
scores = [85, 92, 78, 95, 88, 72, 90]
avg = sum(scores) / len(scores)
print(f"平均分: {avg:.1f}")
print(f"最高: {max(scores)}, 最低: {min(scores)}")
above_avg = [s for s in scores if s > avg]
print(f"高于平均分: {above_avg}")

# 题目 4
import json
data = {"course": "LLM开发", "week": 1, "topics": ["Python", "JSON", "函数"], "completed": True}
json_str = json.dumps(data, ensure_ascii=False)
parsed = json.loads(json_str)
assert data == parsed
print("验证通过")

# 题目 5
def analyze_text(text):
    from collections import Counter
    chars_no_space = [c for c in text if c != " "]
    counter = Counter(chars_no_space)
    return {
        "chars": len(text),
        "words": len(text.split()),
        "lines": text.count("\n") + 1,
        "most_common_char": counter.most_common(1)[0][0] if chars_no_space else "",
    }
```

---

### 15:00 - 15:15 | 课间休息

---

### 15:15 - 17:30 | 综合项目：通讯录管理系统

#### 项目需求

1. 添加联系人（姓名、电话、邮箱、分组）
2. 查看所有联系人（支持按分组筛选）
3. 搜索联系人（按姓名或电话模糊搜索）
4. 修改联系人信息
5. 删除联系人
6. 导出通讯录为 JSON 文件
7. 从 JSON 文件导入通讯录

#### 参考代码

创建文件 `day07/address_book.py`：

```python
"""
Day 7 综合项目：通讯录管理系统
整合第一周所有知识点
"""

import json
from datetime import datetime

# ===== 数据存储 =====
contacts = []
next_id = 1


# ===== 工具函数 =====

def find_contact(contact_id):
    """按 ID 查找联系人"""
    for c in contacts:
        if c["id"] == contact_id:
            return c
    return None


def search_contacts(keyword):
    """模糊搜索"""
    keyword = keyword.lower()
    return [
        c for c in contacts
        if keyword in c["name"].lower()
        or keyword in c["phone"]
        or keyword in c.get("email", "").lower()
    ]


# ===== 核心功能 =====

def add_contact():
    """添加联系人"""
    global next_id
    name = input("姓名: ").strip()
    if not name:
        print("⚠️ 姓名不能为空")
        return

    phone = input("电话: ").strip()
    email = input("邮箱 (可选): ").strip()
    group = input("分组 (如: 家人/同事/朋友): ").strip() or "未分组"

    contact = {
        "id": next_id,
        "name": name,
        "phone": phone,
        "email": email,
        "group": group,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    contacts.append(contact)
    next_id += 1
    print(f"✅ 已添加联系人: {name}")


def list_contacts(group_filter=None):
    """查看联系人列表"""
    filtered = contacts
    if group_filter:
        filtered = [c for c in contacts if c["group"] == group_filter]

    if not filtered:
        print("📭 暂无联系人")
        return

    print(f"\n📒 通讯录 ({len(filtered)} 人)")
    print("-" * 65)
    print(f"{'ID':>4}  {'姓名':<10} {'电话':<15} {'邮箱':<20} {'分组'}")
    print("-" * 65)
    for c in sorted(filtered, key=lambda x: x["name"]):
        print(f"{c['id']:>4}  {c['name']:<10} {c['phone']:<15} {c['email']:<20} {c['group']}")
    print("-" * 65)


def update_contact():
    """修改联系人"""
    list_contacts()
    if not contacts:
        return

    try:
        cid = int(input("请输入要修改的 ID: "))
    except ValueError:
        print("⚠️ 无效 ID")
        return

    contact = find_contact(cid)
    if not contact:
        print(f"⚠️ 未找到 ID={cid}")
        return

    print(f"修改联系人: {contact['name']} (直接回车保持不变)")
    name = input(f"  姓名 [{contact['name']}]: ").strip()
    phone = input(f"  电话 [{contact['phone']}]: ").strip()
    email = input(f"  邮箱 [{contact['email']}]: ").strip()
    group = input(f"  分组 [{contact['group']}]: ").strip()

    if name: contact["name"] = name
    if phone: contact["phone"] = phone
    if email: contact["email"] = email
    if group: contact["group"] = group
    print(f"✅ 已更新: {contact['name']}")


def delete_contact():
    """删除联系人"""
    list_contacts()
    if not contacts:
        return

    try:
        cid = int(input("请输入要删除的 ID: "))
    except ValueError:
        print("⚠️ 无效 ID")
        return

    for i, c in enumerate(contacts):
        if c["id"] == cid:
            removed = contacts.pop(i)
            print(f"🗑️ 已删除: {removed['name']}")
            return
    print(f"⚠️ 未找到 ID={cid}")


def export_json():
    """导出为 JSON"""
    filename = input("文件名 (默认 contacts.json): ").strip() or "day07/contacts.json"
    data = {
        "exported_at": datetime.now().isoformat(),
        "total": len(contacts),
        "contacts": contacts,
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ 已导出 {len(contacts)} 个联系人到 {filename}")


def import_json():
    """从 JSON 导入"""
    global next_id
    filename = input("文件名: ").strip()
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        imported = data.get("contacts", data)  # 兼容纯列表格式
        contacts.clear()
        contacts.extend(imported)
        if contacts:
            next_id = max(c["id"] for c in contacts) + 1
        print(f"✅ 已导入 {len(contacts)} 个联系人")
    except FileNotFoundError:
        print(f"⚠️ 文件 {filename} 不存在")
    except json.JSONDecodeError:
        print("⚠️ JSON 格式错误")


def show_groups():
    """显示分组统计"""
    groups = {}
    for c in contacts:
        g = c["group"]
        groups[g] = groups.get(g, 0) + 1
    print("\n📊 分组统计")
    for g, count in sorted(groups.items()):
        print(f"  {g}: {count} 人")


# ===== 主程序 =====

def main():
    print("=" * 40)
    print("     📒 通讯录管理系统 v1.0")
    print("=" * 40)
    print("💡 Day 7 综合项目 — 整合第一周所有技能")

    while True:
        print("\n1.添加  2.查看  3.搜索  4.修改  5.删除")
        print("6.导出  7.导入  8.分组统计  0.退出")
        choice = input("请选择: ").strip()

        if choice == "0":
            print(f"再见！通讯录共 {len(contacts)} 人")
            break
        elif choice == "1":
            add_contact()
        elif choice == "2":
            group = input("按分组筛选 (回车显示全部): ").strip()
            list_contacts(group if group else None)
        elif choice == "3":
            kw = input("搜索关键词: ").strip()
            results = search_contacts(kw)
            if results:
                for c in results:
                    print(f"  [{c['id']}] {c['name']} - {c['phone']}")
            else:
                print("🔍 未找到匹配联系人")
        elif choice == "4":
            update_contact()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            export_json()
        elif choice == "7":
            import_json()
        elif choice == "8":
            show_groups()
        else:
            print("⚠️ 无效选择")


if __name__ == "__main__":
    main()
```

---

## 🌙 晚自习（19:00 - 21:00）

### 19:00 - 20:00 | 第一周学习复盘

#### 自我评估表

| Day | 主题 | 自评(1-5) | 薄弱环节 |
|-----|------|-----------|----------|
| 1 | 环境与基础语法 | | |
| 2 | 运算符与字符串 | | |
| 3 | 流程控制 | | |
| 4 | 列表 | | |
| 5 | 字典与 JSON | | |
| 6 | 函数 | | |
| 7 | 复习与项目 | | |

#### 补强建议

- 字符串/列表操作不熟 → 重做 Day 2、Day 4 练习
- 流程控制逻辑混乱 → 重做 Day 3 三个项目
- JSON 解析困难 → 重做 Day 5 API 解析器
- 函数封装困难 → 重做 Day 6 重构练习

### 20:00 - 21:00 | 预习第二周

第二周主题预览：
- Day 8-9: 面向对象编程（类、继承、多态）
- Day 10: 模块包与异常处理
- Day 11: 文件操作与标准库
- Day 12: **首次调用大模型 API**
- Day 13-14: 进阶语法与阶段考核

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | 第一周全部语法回顾 | |
| 2 | 笔试题完成 | |
| 3 | 上机题完成 | |
| 4 | 通讯录管理系统 | |
| 5 | 薄弱环节识别 | |

---

## 📝 课后作业

### 必做题

1. **完成周测**：笔试 + 上机全部题目
2. **通讯录项目**：完成并测试所有 8 个功能
3. **Git 提交**：`git commit -m "Day 7: 第一周复习与通讯录系统"`

### 选做题

4. 为通讯录添加「收藏」功能
5. 实现通讯录数据的 CSV 格式导出

---

## 💡 常见问题 FAQ

**Q1: 周测不及格怎么办？**

A: 不及格（<60分）建议用周末重做 Day 3-6 的练习，第二周开始前补齐基础。

**Q2: 通讯录项目太复杂，能否简化？**

A: 核心功能（增删改查 + JSON 导出）必须完成，搜索和分组统计可以后补。

**Q3: 第一周的知识在后续课程中还会用到吗？**

A: 每天都会用到！特别是列表、字典、JSON、函数，贯穿整个 70 天培训。

---

## 🔮 明日预习

**Day 8: 面向对象编程（上）**

明天你将学习：

- 类与对象的概念
- `__init__` 构造方法
- 创建 `ChatMessage` 类——为大模型消息建模

**预习建议**：思考通讯录中的「联系人」能否抽象为一个「类」？

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 7*
