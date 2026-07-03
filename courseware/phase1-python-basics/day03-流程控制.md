# Day 3: 流程控制

> **培训阶段**: 第一阶段 Python 编程基础 | **第 1 周** | **学习时长**: 约 6-8 小时  
> **今日关键词**: if/elif/else、while 循环、for 循环、break/continue、猜数字游戏、九九乘法表

---

## 📍 课程导航

### 上节回顾
在 **Day 2** 中，你学习了算术/比较/逻辑运算符、字符串索引切片与方法、f-string 格式化，并完成了「文本清洗小工具」。BMI 计算器和文本清洗工具中已初步使用了 `if` 和 `while`，今天将系统掌握流程控制。

### 本节学习目标
完成本日学习后，你将能够：

1. 熟练使用 `if` / `elif` / `else` 进行条件分支
2. 掌握 `while` 循环处理重复任务和菜单系统
3. 掌握 `for` 循环遍历序列和执行固定次数操作
4. 使用 `break`、`continue` 控制循环流程
5. 独立完成猜数字游戏、九九乘法表、简易菜单三个项目
6. 理解流程控制在大模型应用中的角色（重试逻辑、批处理等）

### 与后续课程的衔接
- **Day 4** 将学习列表——`for` 循环遍历列表是最常见的组合用法
- **Day 6** 将把今天的菜单逻辑重构为函数，提高代码复用性
- **Day 13** 将学习装饰器实现 API 重试——本质是循环 + 条件判断的封装
- **Day 14** 阶段项目中的多轮对话菜单——今天学的 `while` 循环是核心结构

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：条件语句 if/elif/else

#### 1.1 基本 if 语句

```python
# day03/if_basic.py
score = int(input("请输入成绩: "))

if score >= 60:
    print("恭喜，及格了！")
    print(f"你的成绩是 {score} 分")
```

**语法结构：**

```python
if 条件:
    # 条件为 True 时执行（注意缩进！）
    语句块
```

> ⚠️ Python 用 **缩进**（4个空格）表示代码块，不使用花括号 `{}`。

#### 1.2 if-else 二选一

```python
# day03/if_else.py
age = int(input("请输入年龄: "))

if age >= 18:
    print("你已成年，可以独立签订合同。")
else:
    print("你未成年，需要监护人同意。")
```

#### 1.3 if-elif-else 多分支

```python
# day03/if_elif_else.py
score = int(input("请输入成绩 (0-100): "))

if score >= 90:
    grade = "A"
    comment = "优秀！"
elif score >= 80:
    grade = "B"
    comment = "良好！"
elif score >= 70:
    grade = "C"
    comment = "中等"
elif score >= 60:
    grade = "D"
    comment = "及格"
else:
    grade = "F"
    comment = "不及格，需要加油！"

print(f"等级: {grade}，{comment}")
```

#### 1.4 嵌套条件

```python
# day03/nested_if.py
username = input("用户名: ")
password = input("密码: ")

if username == "admin":
    if password == "123456":
        print("✅ 登录成功！")
    else:
        print("❌ 密码错误")
else:
    print("❌ 用户不存在")
```

#### 1.5 条件表达式（三元运算符）

```python
# 传统写法
age = 20
if age >= 18:
    status = "成年"
else:
    status = "未成年"

# 简洁写法（三元表达式）
status = "成年" if age >= 18 else "未成年"
print(status)

# 实际应用：设置默认值
api_key = input("API Key（留空使用默认）: ")
api_key = api_key if api_key else "default-key-12345"
```

#### 1.6 与大模型开发的联系

```python
# API 响应状态判断（Day 12 会实际用到）
status_code = 200
response_text = "正常响应内容"

if status_code == 200:
    print("请求成功，解析响应...")
elif status_code == 401:
    print("API Key 无效，请检查配置")
elif status_code == 429:
    print("请求过于频繁，稍后重试")
else:
    print(f"未知错误，状态码: {status_code}")
```

---

### 9:45 - 10:30 | 模块二：while 循环

#### 2.1 基本 while 循环

```python
# day03/while_basic.py
# 倒计时
count = 5
while count > 0:
    print(f"倒计时: {count}")
    count -= 1  # 等价于 count = count - 1
print("🚀 发射！")
```

**语法结构：**

```python
while 条件:
    # 条件为 True 时重复执行
    语句块
```

#### 2.2 用户输入验证（经典模式）

```python
# day03/input_validation.py
while True:
    age = input("请输入年龄（1-120）: ")
    if age.isdigit() and 1 <= int(age) <= 120:
        age = int(age)
        break  # 输入合法，跳出循环
    print("⚠️ 输入无效，请重新输入")

print(f"你的年龄是 {age} 岁")
```

#### 2.3 菜单系统模式

```python
# day03/menu_pattern.py
def show_menu():
    print("\n===== 主菜单 =====")
    print("1. 功能一")
    print("2. 功能二")
    print("0. 退出")
    print("==================")

while True:
    show_menu()
    choice = input("请选择: ").strip()

    if choice == "0":
        print("再见！")
        break
    elif choice == "1":
        print("执行功能一...")
    elif choice == "2":
        print("执行功能二...")
    else:
        print("⚠️ 无效选择")
```

> 💡 Day 2 的「文本清洗小工具」用的就是这个模式！今天学完后你应该能完全理解那段代码。

#### 2.4 break 与 continue

```python
# day03/break_continue.py

# break：立即退出循环
print("--- break 示例 ---")
i = 0
while i < 10:
    if i == 5:
        break  # 当 i 等于 5 时退出
    print(i, end=" ")
    i += 1
print()  # 输出: 0 1 2 3 4

# continue：跳过本次，进入下一次
print("--- continue 示例 ---")
i = 0
while i < 10:
    i += 1
    if i % 2 == 0:
        continue  # 跳过偶数
    print(i, end=" ")
print()  # 输出: 1 3 5 7 9
```

| 关键字 | 作用 |
|--------|------|
| `break` | 立即退出整个循环 |
| `continue` | 跳过本次循环剩余代码，进入下一次 |

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：for 循环

#### 3.1 基本 for 循环与 range()

```python
# day03/for_basic.py

# range(stop)：从 0 到 stop-1
for i in range(5):
    print(i, end=" ")  # 0 1 2 3 4
print()

# range(start, stop)
for i in range(2, 6):
    print(i, end=" ")  # 2 3 4 5
print()

# range(start, stop, step)
for i in range(0, 10, 2):
    print(i, end=" ")  # 0 2 4 6 8
print()

# 倒序
for i in range(5, 0, -1):
    print(i, end=" ")  # 5 4 3 2 1
print()
```

#### 3.2 遍历字符串

```python
# day03/for_string.py
message = "AI"

for char in message:
    print(char)

# 带索引遍历
for index, char in enumerate(message):
    print(f"索引 {index}: {char}")
```

#### 3.3 for vs while 选择指南

| 场景 | 推荐 | 原因 |
|------|------|------|
| 已知循环次数 | `for` + `range()` | 代码更简洁 |
| 遍历序列 | `for` | Python 风格 |
| 未知循环次数（如用户输入验证） | `while` | 灵活 |
| 菜单系统 | `while True` + `break` | 标准模式 |

#### 3.4 嵌套循环

```python
# day03/nested_loop.py
# 打印矩形
rows = 3
cols = 5
for i in range(rows):
    for j in range(cols):
        print("*", end="")
    print()  # 每行结束后换行

# 输出:
# *****
# *****
# *****
```

#### 3.5 循环中的 else 子句

```python
# day03/for_else.py
# for-else：循环正常结束（未被 break）时执行 else
for i in range(3):
    print(i)
else:
    print("循环正常结束")

# 实用场景：搜索
target = 7
for i in range(10):
    if i == target:
        print(f"找到了: {i}")
        break
else:
    print(f"未找到 {target}")
```

---

## 🌇 下午实操（14:00 - 17:30）

### 14:00 - 15:00 | 项目一：猜数字游戏

#### 项目需求

1. 程序随机生成 1-100 之间的整数
2. 玩家最多有 7 次猜测机会
3. 每次猜测后提示「太大了」或「太小了」
4. 猜对则祝贺并显示用了几次
5. 次数用完则揭示答案

#### 参考代码

创建文件 `day03/guess_number.py`：

```python
"""
Day 3 项目一：猜数字游戏
练习：while 循环、if 条件、break
"""

import random

def play_game():
    """主游戏逻辑"""
    secret = random.randint(1, 100)
    max_attempts = 7
    attempts = 0

    print("=" * 40)
    print("       🎮 猜数字游戏")
    print("=" * 40)
    print(f"我想了一个 1-100 之间的整数，你有 {max_attempts} 次机会！")
    print()

    while attempts < max_attempts:
        remaining = max_attempts - attempts
        guess_input = input(f"第 {attempts + 1} 次猜测（还剩 {remaining} 次）: ").strip()

        # 输入验证
        if not guess_input.isdigit():
            print("⚠️ 请输入有效的数字！")
            continue

        guess = int(guess_input)
        attempts += 1

        if guess < secret:
            print("📈 太小了！往大一点猜")
        elif guess > secret:
            print("📉 太大了！往小一点猜")
        else:
            print(f"\n🎉 恭喜你！猜对了！答案是 {secret}")
            print(f"你用了 {attempts} 次，{'太厉害了！' if attempts <= 3 else '不错哦！'}")
            return True

    print(f"\n😢 游戏结束！答案是 {secret}")
    return False


def main():
    while True:
        play_game()
        again = input("\n再玩一局？(y/n): ").strip().lower()
        if again != "y":
            print("感谢游玩，再见！")
            break


if __name__ == "__main__":
    main()
```

---

### 15:00 - 16:00 | 项目二：九九乘法表

#### 项目需求

1. 打印标准的九九乘法表
2. 格式整齐对齐
3. 支持选择打印几种模式

#### 参考代码

创建文件 `day03/multiplication_table.py`：

```python
"""
Day 3 项目二：九九乘法表
练习：嵌套 for 循环、字符串格式化
"""

def print_table_standard():
    """标准九九乘法表（下三角）"""
    print("\n📐 标准九九乘法表")
    print("-" * 50)
    for i in range(1, 10):
        for j in range(1, i + 1):
            # 格式化：乘法表达式占 12 个字符宽度
            print(f"{j}×{i}={i*j:<3}", end="")
        print()  # 每行换行


def print_table_full():
    """完整 9×9 表格"""
    print("\n📐 完整乘法表")
    print("-" * 80)
    # 表头
    print("   ", end="")
    for j in range(1, 10):
        print(f"{j:4}", end="")
    print()
    print("   " + "-" * 36)

    for i in range(1, 10):
        print(f"{i} |", end="")
        for j in range(1, 10):
            print(f"{i*j:4}", end="")
        print()


def print_table_row(n):
    """打印单行：N 的乘法口诀"""
    if not 1 <= n <= 9:
        print("⚠️ 请输入 1-9 之间的数字")
        return
    print(f"\n📐 {n} 的乘法口诀")
    for i in range(1, 10):
        print(f"{n} × {i} = {n * i}")


def main():
    while True:
        print("\n" + "=" * 40)
        print("       九九乘法表生成器")
        print("=" * 40)
        print("1. 标准九九乘法表（下三角）")
        print("2. 完整 9×9 表格")
        print("3. 指定数字的口诀")
        print("0. 退出")

        choice = input("请选择: ").strip()

        if choice == "0":
            print("再见！")
            break
        elif choice == "1":
            print_table_standard()
        elif choice == "2":
            print_table_full()
        elif choice == "3":
            n = int(input("请输入数字 (1-9): "))
            print_table_row(n)
        else:
            print("⚠️ 无效选择")


if __name__ == "__main__":
    main()
```

---

### 16:00 - 16:15 | 课间休息

---

### 16:15 - 17:30 | 项目三：简易菜单系统

#### 项目需求

整合前几天知识，编写一个「学习中心」菜单系统：
1. 个人信息展示（Day 1）
2. 简易计算器（Day 2）
3. 文本统计（Day 2）
4. BMI 计算（Day 2）

#### 参考代码

创建文件 `day03/study_center.py`：

```python
"""
Day 3 项目三：学习中心简易菜单
整合 Day 1-3 知识的综合练习
"""

# ===== 功能模块 =====

def show_profile():
    """个人信息展示"""
    print("\n--- 个人信息 ---")
    name = input("姓名: ")
    age = int(input("年龄: "))
    city = input("城市: ")
    print(f"\n你好，{city}的{name}，今年{age}岁！")


def calculator():
    """简易计算器"""
    print("\n--- 简易计算器 ---")
    a = float(input("第一个数: "))
    op = input("运算符 (+ - * /): ").strip()
    b = float(input("第二个数: "))

    if op == "+":
        result = a + b
    elif op == "-":
        result = a - b
    elif op == "*":
        result = a * b
    elif op == "/":
        if b == 0:
            print("❌ 除数不能为零！")
            return
        result = a / b
    else:
        print("❌ 无效运算符")
        return

    print(f"结果: {a} {op} {b} = {result:.4f}")


def text_stats():
    """文本统计"""
    print("\n--- 文本统计 ---")
    text = input("请输入文本: ")
    print(f"字符数: {len(text)}")
    print(f"单词数: {len(text.split())}")
    print(f"行数: {text.count(chr(10)) + 1}")


def bmi_calculator():
    """BMI 计算"""
    print("\n--- BMI 计算器 ---")
    h = float(input("身高(米): "))
    w = float(input("体重(公斤): "))
    bmi = w / (h ** 2)
    print(f"BMI: {bmi:.1f}", end=" — ")

    if bmi < 18.5:
        print("偏瘦")
    elif bmi < 24:
        print("正常")
    elif bmi < 28:
        print("偏胖")
    else:
        print("肥胖")


# ===== 主菜单 =====

def main():
    MENU = {
        "1": ("个人信息", show_profile),
        "2": ("简易计算器", calculator),
        "3": ("文本统计", text_stats),
        "4": ("BMI 计算", bmi_calculator),
    }

    print("欢迎来到学习中心！")

    while True:
        print("\n" + "=" * 35)
        print("        🎓 学习中心")
        print("=" * 35)
        for key, (name, _) in MENU.items():
            print(f"  {key}. {name}")
        print("  0. 退出")
        print("=" * 35)

        choice = input("请选择: ").strip()

        if choice == "0":
            print("再见，继续加油学习！")
            break
        elif choice in MENU:
            _, func = MENU[choice]
            func()
        else:
            print("⚠️ 无效选择，请重试")


if __name__ == "__main__":
    main()
```

---

## 🌙 晚自习（19:00 - 21:00）

### 19:00 - 20:00 | 流程控制综合练习

#### 练习：打印素数（1-50）

```python
# day03/prime_numbers.py
print("1-50 之间的素数:")
for num in range(2, 51):
    is_prime = True
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            is_prime = False
            break
    if is_prime:
        print(num, end=" ")
print()
```

#### 练习：斐波那契数列

```python
# day03/fibonacci.py
n = int(input("输出前 N 项: "))
a, b = 0, 1
for i in range(n):
    print(a, end=" ")
    a, b = b, a + b
print()
```

### 20:00 - 21:00 | 自习与 Git 提交

- 完成三个下午项目
- Git 提交：`git commit -m "Day 3: 流程控制与三个项目"`
- 预习 Day 4 列表内容

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | if / elif / else 条件分支 | |
| 2 | 嵌套条件与三元表达式 | |
| 3 | while 循环基本用法 | |
| 4 | 输入验证 + while True 模式 | |
| 5 | break 退出循环 | |
| 6 | continue 跳过本次 | |
| 7 | for 循环与 range() | |
| 8 | enumerate() 带索引遍历 | |
| 9 | 嵌套循环 | |
| 10 | 猜数字游戏项目 | |
| 11 | 九九乘法表项目 | |
| 12 | 简易菜单系统项目 | |

---

## 📝 课后作业

### 必做题

1. **猜数字游戏**：完成项目，增加难度选择（简单 1-50 / 困难 1-200）
2. **九九乘法表**：完成项目并能解释嵌套循环执行过程
3. **菜单系统**：完成学习中心项目，至少添加一个自定义功能

### 选做题

4. **石头剪刀布**：与电脑对战，三局两胜，统计胜率
5. **打印空心菱形**：输入奇数 N，打印 N 行空心菱形
6. **百钱买百鸡**：公鸡 5 文/只，母鸡 3 文/只，小鸡 1 文 3 只，100 文买 100 只

---

## 💡 常见问题 FAQ

**Q1: if 后面一定要写 else 吗？**

A: 不一定。如果只需要在条件成立时执行某些操作，只写 `if` 即可。

**Q2: while True 不会死循环吗？**

A: 需要在循环体内用 `break` 退出，否则确实是死循环。菜单系统标准模式就是 `while True` + 退出选项。

**Q3: range(5) 和 range(1, 6) 有什么区别？**

A: `range(5)` 生成 0,1,2,3,4；`range(1, 6)` 生成 1,2,3,4,5。注意 `range` 的结束值不包含在内。

**Q4: for 循环和 while 循环可以互换吗？**

A: 理论上可以，但 `for` 遍历已知序列更 Pythonic，`while` 适合条件驱动的循环。选对工具让代码更清晰。

**Q5: 缩进用 Tab 还是空格？**

A: Python 官方推荐 **4 个空格**。VS Code 默认按 Tab 键会插入 4 个空格。

---

## 🔮 明日预习

**Day 4: 核心数据结构上——列表**

明天你将学习：

- 列表的创建、增删改查
- 列表切片与排序
- 列表推导式（Python 最优雅的特性之一）
- 实操项目：待办事项管理器

**预习建议**：思考今天菜单系统中的多个选项，能否用「列表」来存储和管理？

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 3*
