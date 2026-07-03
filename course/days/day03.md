# Day 3: 流程控制

> **零基础大模型应用开发 70 天培训课程** | 第 3/70 天 | Python 编程基础


——————




## 深度讲义


### 3.1 if/elif/else 条件判断

```python
score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 60:
    grade = "C"
else:
    grade = "D"
print(f"等级: {grade}")
```

### 3.2 循环

#### for 循环

```python
for i in range(5):       # 0, 1, 2, 3, 4
    print(i)

fruits = ["苹果", "香蕉", "橙子"]
for fruit in fruits:
    print(fruit)
```

#### while 循环

```python
count = 0
while count < 3:
    print(f"第 {count + 1} 次")
    count += 1
```

#### break 与 continue

- `break`: 立即退出循环
- `continue`: 跳过本次，进入下一次

### 3.3 简易菜单系统

```python
while True:
    print("\n=== 菜单 ===")
    print("1. 查看")
    print("2. 添加")
    print("0. 退出")
    choice = input("请选择: ")
    if choice == "0":
        break
    elif choice == "1":
        print("查看功能")
    elif choice == "2":
        print("添加功能")
    else:
        print("无效选择")
```

> **前后衔接**: Day 14 多轮对话助手的 `/clear`、`/exit` 指令就是用 today 学的 while + if 实现的


## 完整项目代码（可直接运行）

### 文件: `day03_guess_number.py`

```python
"""Day 3: 猜数字游戏"""
import random

def guess_number_game():
    target = random.randint(1, 100)
    attempts = 0
    print("🎮 猜数字游戏！范围 1-100")

    while True:
        guess_str = input("请输入你的猜测: ")
        try:
            guess = int(guess_str)
        except ValueError:
            print("请输入有效整数！")
            continue

        attempts += 1
        if guess < target:
            print("太小了！")
        elif guess > target:
            print("太大了！")
        else:
            print(f"🎉 恭喜！用了 {attempts} 次猜对了！")
            break


def multiplication_table():
    for i in range(1, 10):
        row = "  ".join(f"{i}×{j}={i*j:2d}" for j in range(1, i + 1))
        print(row)


if __name__ == "__main__":
    guess_number_game()
```

### 运行步骤

```bash
cd course/code/day03
pip install -r requirements.txt  # 如有依赖
python day03_guess_number.py
```


## 常见错误与避坑

- ⚠️ 只看不练 — 必须动手敲代码
- ⚠️ 跳过基础直接调 API — 每天知识环环相扣
- ⚠️ 不写注释 — 企业级代码必须可读

## 课堂练习

- 📝 复习 Day 2 的核心知识点
- 📝 完成今日实操项目并提交 Git
- 📝 用 3 句话总结今天学到了什么


## 课程衔接说明



### ⬅️ 昨日回顾

**Day 2** 学习了「运算符与字符串」，今天的知识直接建立在昨天之上。

### 🔗 今日定位

承接 Day 2 字符串，为 Day 14 多轮对话助手的指令解析(/clear 等)做准备。

### ➡️ 明日预告

**Day 4** 将学习「核心数据结构（上）」，今天务必打牢基础。


### 今日时间安排

| 时段 | 内容 |
|------|------|
| 09:00-12:00 上午 | if/elif/else 条件判断、嵌套条件 |
| 09:00-12:00 上午 | while 循环、for 循环、range、break/continue |
| 14:00-17:30 下午 | 🛠️ 猜数字游戏 |
| 14:00-17:30 下午 | 🛠️ 九九乘法表 |
| 14:00-17:30 下午 | 🛠️ 简易菜单系统 |
| 19:00-21:00 晚自习 | LeetCode 简单题 2 道 |



## 一、今日学习目标



完成今天的学习后，你将能够:

- if/elif/else 条件判断、嵌套条件
- while 循环、for 循环、range、break/continue

### 核心技能点

- **条件分支**
- **循环**
- **用户交互菜单**

### 与课程主线的关系

今天是 **第 1 阶段（Python 编程基础）** 的第 3 天。

> 今日主题「流程控制」是整条 70 天学习路径中的关键一环。请对照总路线图理解今天学什么、为什么学、后面哪里会用到。



## 二、理论精讲（纳米级拆解）


### 2.1 if/elif/else 条件判断、嵌套条件

#### 核心概念

**if/elif/else 条件判断、嵌套条件** 是今日学习的重要内容。

#### 为什么学？

在大模型应用开发中，这个知识点将在后续项目中直接用到:
- 与 Day 1 的知识形成递进
- 为 Day 6 的实操项目提供基础

#### 学习要点

1. 理解概念定义（用自己的话复述）
2. 跟着课件代码敲一遍（不要复制粘贴）
3. 完成课后练习巩固

#### 常见错误

- 只看不练 → 必须动手写代码
- 跳过基础 → 每天知识环环相扣，不要跳天

### 2.2 while 循环、for 循环、range、break/continue

#### 核心概念

**while 循环、for 循环、range、break/continue** 是今日学习的重要内容。

#### 为什么学？

在大模型应用开发中，这个知识点将在后续项目中直接用到:
- 与 Day 1 的知识形成递进
- 为 Day 6 的实操项目提供基础

#### 学习要点

1. 理解概念定义（用自己的话复述）
2. 跟着课件代码敲一遍（不要复制粘贴）
3. 完成课后练习巩固

#### 常见错误

- 只看不练 → 必须动手写代码
- 跳过基础 → 每天知识环环相扣，不要跳天

## 三、下午实操预告

今日下午核心项目: **猜数字游戏 + 简易菜单系统**
- 猜数字游戏
- 九九乘法表
- 简易菜单系统



## 下午实操：项目实战



### 项目名称

**猜数字游戏 + 简易菜单系统**

### 推荐项目目录结构（企业级标准）

```text
day03_project/
├─ src/
│  ├─ __init__.py
│  └─ main.py
├─ data/
├─ outputs/
├─ tests/
├─ requirements.txt
└─ README.md
```

### 代码骨架

```python
# ================================
# 文件名: day03_main.py
# 主题: Day 3 — 猜数字游戏 + 简易菜单系统
# ================================

"""
Day 3 实操项目入口。

学习要点:
1. 复习昨天所学
2. 完成今日「猜数字游戏 + 简易菜单系统」核心功能
3. 添加必要注释，提交 Git
"""


def main():
    """主函数 — 按今日课纲逐步实现"""
    print("Day 3: 猜数字游戏 + 简易菜单系统")
    # TODO: 按课件逐步实现
    pass


if __name__ == "__main__":
    main()
```

### 实现步骤（纳米级拆解）

1. **需求确认**: 阅读今日课纲，明确输入/输出
2. **环境准备**: 激活 venv，`pip install` 今日所需依赖
3. **核心实现**: 按上午所学知识点逐步编码
4. **自测**: 手动运行 3 个以上测试用例
5. **提交**: `git add . && git commit -m "Day 3: 猜数字游戏 + 简易菜单系统"`



## 知识小测




**Q1.** 请用自己的话解释「条件分支」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 1-3 所学填写）
- 后续应用: 将在 Day 10 左右用到

</details>

**Q2.** 请用自己的话解释「循环」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 1-3 所学填写）
- 后续应用: 将在 Day 10 左右用到

</details>

**Q3.** 请用自己的话解释「用户交互菜单」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 1-3 所学填写）
- 后续应用: 将在 Day 10 左右用到

</details>


### 上机题

请不看课件，独立完成今日「实操项目」的核心功能。限时 60 分钟。



## 课后作业



### 必做

1. 完成今日实操项目「猜数字游戏 + 简易菜单系统」
2. 提交代码到 GitHub（commit message: `Day 3: 猜数字游戏 + 简易菜单系统`）
3. 在学习笔记中记录 3 个今天学到的新知识点

### 晚自习

- LeetCode 简单题 2 道

### 选做

1. 阅读官方文档中与今日主题相关的章节
2. 尝试优化今日代码（更优雅的错误处理、更清晰的注释）


——————

**第 3/70 天 · 零基础大模型应用开发 70 天培训课程**

> 坚持每一天，70 天后你将成为一名合格的大模型应用开发者。
