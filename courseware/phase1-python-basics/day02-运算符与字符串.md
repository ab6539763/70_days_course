# Day 2: 运算符与字符串

> **培训阶段**: 第一阶段 Python 编程基础 | **第 1 周** | **学习时长**: 约 6-8 小时  
> **今日关键词**: 算术运算符、比较运算符、逻辑运算符、字符串索引切片、f-string、文本清洗

---

## 📍 课程导航

### 上节回顾
在 **Day 1** 中，你完成了开发环境搭建，学习了变量、四种基本数据类型（int/float/str/bool）、`print()` 与 `input()`，并完成了「个人信息卡片」项目。你还初步接触了 f-string 格式化输出。

### 本节学习目标
完成本日学习后，你将能够：

1. 熟练使用算术、比较、逻辑运算符进行计算与条件判断
2. 理解运算符优先级，能正确阅读复杂表达式
3. 掌握字符串的索引、切片、常用方法
4. 深入使用 f-string 进行格式化输出——**这是后续编写 Prompt 模板的核心技能**
5. 独立完成「文本清洗小工具」命令行程序
6. 理解字符串处理在大模型开发中的重要性

### 与后续课程的衔接
- **Day 3** 将学习流程控制（if/for/while）——今天学的比较与逻辑运算符是条件判断的基础
- **Day 5** 将学习 JSON 字符串解析——字符串操作是处理 API 返回数据的前提
- **Day 17** 将编写 Prompt 模板——f-string 拼接变量是 Prompt 工程的核心写法
- **Day 12** 调用大模型 API 时，你需要清洗用户输入的文本——今天的文本清洗技能直接派上用场

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：算术运算符

#### 1.1 基本算术运算

```python
# day02/arithmetic.py
a = 10
b = 3

print(f"加法: {a} + {b} = {a + b}")    # 13
print(f"减法: {a} - {b} = {a - b}")    # 7
print(f"乘法: {a} * {b} = {a * b}")    # 30
print(f"除法: {a} / {b} = {a / b}")    # 3.3333...（结果是 float）
print(f"整除: {a} // {b} = {a // b}")  # 3（向下取整）
print(f"取余: {a} % {b} = {a % b}")    # 1
print(f"幂运算: {a} ** {b} = {a ** b}")  # 1000
```

#### 1.2 运算符详解

| 运算符 | 名称 | 示例 | 结果 | 说明 |
|--------|------|------|------|------|
| `+` | 加法 | `5 + 3` | `8` | 数字相加；字符串拼接 |
| `-` | 减法 | `5 - 3` | `2` | |
| `*` | 乘法 | `5 * 3` | `15` | 数字相乘；字符串重复 |
| `/` | 真除法 | `10 / 3` | `3.333...` | 结果永远是 float |
| `//` | 整除 | `10 // 3` | `3` | 向下取整 |
| `%` | 取余 | `10 % 3` | `1` | 判断奇偶、循环索引 |
| `**` | 幂运算 | `2 ** 10` | `1024` | |

#### 1.3 字符串与数字的混合运算

```python
# 字符串拼接（+ 两侧必须都是 str）
greeting = "Hello" + " " + "World"
print(greeting)  # Hello World

# 字符串重复（* 一侧是 str，一侧是 int）
line = "=" * 40
print(line)  # ========================================

# ⚠️ 常见错误：字符串和数字不能直接相加
# print("年龄: " + 25)  # TypeError!
# 正确做法：
age = 25
print("年龄: " + str(age))       # 方法1：类型转换
print(f"年龄: {age}")            # 方法2：f-string（推荐）
```

#### 1.4 复合赋值运算符

```python
count = 0
count += 1   # 等价于 count = count + 1
count *= 2   # 等价于 count = count * 2
print(count)  # 2

# 在大模型开发中，token 计数常用 +=
total_tokens = 0
total_tokens += 150  # 本次请求消耗 150 tokens
total_tokens += 200  # 下次请求消耗 200 tokens
print(f"累计 token: {total_tokens}")  # 350
```

#### 1.5 运算符优先级

从高到低：

```
**          幂运算
* / // %    乘除取余
+ -         加减
```

```python
result = 2 + 3 * 4       # 14，不是 20
result2 = (2 + 3) * 4    # 20，括号改变优先级
print(result, result2)
```

---

### 9:45 - 10:30 | 模块二：比较运算符与逻辑运算符

#### 2.1 比较运算符

比较运算符的结果是 **布尔值**（True 或 False）：

```python
# day02/comparison.py
x = 10
y = 5

print(x > y)    # True
print(x < y)    # False
print(x == y)   # False（等于，注意是两个等号！）
print(x != y)   # True（不等于）
print(x >= 10)  # True
print(x <= 5)   # False

# 字符串也可以比较（按字典序）
print("apple" < "banana")  # True
print("张三" == "张三")     # True
```

| 运算符 | 含义 | 示例 |
|--------|------|------|
| `==` | 等于 | `5 == 5` → True |
| `!=` | 不等于 | `5 != 3` → True |
| `>` | 大于 | `5 > 3` → True |
| `<` | 小于 | `3 < 5` → True |
| `>=` | 大于等于 | `5 >= 5` → True |
| `<=` | 小于等于 | `3 <= 5` → True |

> ⚠️ **新手陷阱**：赋值用 `=`，比较用 `==`。`if x = 5` 是语法错误！

#### 2.2 逻辑运算符

```python
# day02/logic.py
age = 25
has_degree = True

# and：两个条件都为 True 才为 True
can_apply = age >= 22 and has_degree
print(can_apply)  # True

# or：任一条件为 True 就为 True
is_weekend = False
is_holiday = True
can_rest = is_weekend or is_holiday
print(can_rest)  # True

# not：取反
is_raining = False
go_out = not is_raining
print(go_out)  # True
```

| 运算符 | 含义 | 示例 |
|--------|------|------|
| `and` | 与 | `True and False` → False |
| `or` | 或 | `True or False` → True |
| `not` | 非 | `not True` → False |

#### 2.3 真值判断

在 Python 中，以下值被视为 **False**：

```python
# 以下都等价于 False
bool(0)       # 数字零
bool(0.0)
bool("")      # 空字符串
bool([])      # 空列表（Day 4 会学）
bool(None)    # 空值

# 其他值都视为 True
bool("hello")  # True
bool(-1)       # True（非零数字都是 True）
```

> 💡 **与大模型开发的联系**：在 Day 12 调用 API 前，你会用 `if api_key:` 检查密钥是否已配置——这就是真值判断。

#### 2.4 链式比较

Python 支持优雅的链式比较：

```python
score = 85
# 判断成绩是否在 60 到 100 之间
is_pass = 60 <= score <= 100
print(is_pass)  # True

# 等价于
is_pass = score >= 60 and score <= 100
```

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：字符串深入

#### 3.1 字符串索引

字符串中每个字符都有一个位置编号（索引），从 **0** 开始：

```python
# day02/string_index.py
text = "Hello, AI!"

# 正向索引（从 0 开始）
print(text[0])   # H
print(text[1])   # e
print(text[7])   # A

# 负向索引（从 -1 开始，-1 是最后一个字符）
print(text[-1])  # !
print(text[-2])  # I
print(text[-3])  #  

# 索引示意图
#  H   e   l   l   o   ,       A   I   !
#  0   1   2   3   4   5   6   7   8   9
# -10  -9  -8  -7  -6  -5  -4  -3  -2  -1
```

#### 3.2 字符串切片

切片语法：`字符串[起始:结束:步长]`

```python
text = "Hello, AI World!"

# 基本切片：[起始:结束)，结束位置不包含
print(text[0:5])    # Hello
print(text[7:9])    # AI

# 省略起始：从头开始
print(text[:5])     # Hello

# 省略结束：到末尾
print(text[7:])     # AI World!

# 省略起始和结束：复制整个字符串
print(text[:])      # Hello, AI World!

# 步长
print(text[::2])    # Hlo AIWrd!（每隔一个字符）
print(text[::-1])   # !dlroW IA ,olleH（反转字符串）
```

#### 3.3 常用字符串方法

```python
# day02/string_methods.py
text = "  Hello, AI World!  "

# 大小写转换
print(text.upper())        #   HELLO, AI WORLD!  
print(text.lower())        #   hello, ai world!  
print(text.title())        #   Hello, Ai World!  

# 去除空白
print(text.strip())        # Hello, AI World!（去除两端空白）
print(text.lstrip())       # 去除左侧空白
print(text.rstrip())       # 去除右侧空白

# 查找与替换
print(text.find("AI"))     # 9（找到返回索引，找不到返回 -1）
print(text.replace("AI", "人工智能"))  #   Hello, 人工智能 World!  

# 分割与拼接
sentence = "Python,Java,Go,Rust"
langs = sentence.split(",")    # ['Python', 'Java', 'Go', 'Rust']
print(langs)
joined = " | ".join(langs)     # Python | Java | Go | Rust
print(joined)

# 判断
print("123".isdigit())     # True
print("abc".isalpha())     # True
print(text.startswith("  H"))  # True
print(text.endswith("!  "))     # True
```

| 方法 | 功能 | 示例 |
|------|------|------|
| `.strip()` | 去除两端空白 | `"  hi  ".strip()` → `"hi"` |
| `.lower()` / `.upper()` | 大小写转换 | `"Hello".lower()` → `"hello"` |
| `.replace(old, new)` | 替换子串 | `"a-b".replace("-", "_")` → `"a_b"` |
| `.split(sep)` | 按分隔符分割 | `"a,b".split(",")` → `['a','b']` |
| `.join(list)` | 拼接列表 | `",".join(['a','b'])` → `"a,b"` |
| `.find(sub)` | 查找子串位置 | `"hello".find("ll")` → `2` |
| `.startswith()` / `.endswith()` | 判断开头/结尾 | |

#### 3.4 f-string 格式化深入

f-string 是 Python 3.6+ 引入的字符串格式化方式，**简洁、高效、可读性强**：

```python
# day02/fstring.py
name = "王小明"
score = 95.567
count = 42

# 基本用法
print(f"学生 {name} 的成绩是 {score} 分")

# 表达式
print(f"10 年后 {name} {25 + 10} 岁")

# 格式说明符
print(f"成绩: {score:.1f}")      # 95.6（保留1位小数）
print(f"成绩: {score:.2f}")      # 95.57（保留2位小数）
print(f"编号: {count:05d}")      # 00042（5位数字，前补零）
print(f"编号: {count:>5}")       #    42（右对齐，占5位）
print(f"姓名: {name:<10}")       # 王小明      （左对齐，占10位）
print(f"姓名: {name:^10}")       #   王小明    （居中，占10位）

# 百分比
ratio = 0.856
print(f"准确率: {ratio:.1%}")    # 准确率: 85.6%
```

**与大模型开发的联系——Prompt 模板预览：**

```python
# 这是 Day 17 Prompt 工程的雏形！
system_prompt = "你是一个专业的 Python 编程助手。"
user_question = "什么是列表推导式？"
language = "中文"

prompt = f"""你是一个专业的编程助手。

请用{language}回答以下问题：
{user_question}

要求：
1. 回答简洁明了
2. 附带代码示例
3. 不超过 200 字
"""
print(prompt)
```

#### 3.5 原始字符串与转义字符

```python
# 转义字符
print("第一行\n第二行")       # \n 换行
print("制表符\t分隔")         # \t 制表符
print("引号: \"你好\"")       # \" 转义引号
print("反斜杠: \\")           # \\ 反斜杠

# 原始字符串 r""：不处理转义，常用于正则表达式
path = r"C:\Users\name\Documents"
print(path)  # C:\Users\name\Documents

# 多行字符串
multiline = """
这是第一行
这是第二行
这是第三行
"""
```

---

## 🌇 下午实操（14:00 - 17:30）

### 14:00 - 15:30 | 实操项目：文本清洗小工具

#### 项目背景

在大模型应用开发中，用户输入的文本往往包含多余空白、特殊字符、不一致的大小写等问题。在将文本发送给大模型之前，需要进行清洗和标准化。今天你将编写一个命令行文本清洗工具。

#### 项目需求

1. 提示用户输入一段文本（支持多行，输入 `END` 结束）
2. 提供以下清洗功能（通过菜单选择）：
   - 去除首尾空白
   - 转换为小写/大写
   - 去除所有空白字符
   - 替换指定字符
   - 统计字符数和单词数
   - 显示清洗后的文本
3. 支持循环操作，直到用户选择退出

#### 参考代码

创建文件 `day02/text_cleaner.py`：

```python
"""
Day 2 实操项目：文本清洗小工具
功能：对用户输入的文本进行各种清洗操作
"""

def show_menu():
    """显示功能菜单"""
    print("\n" + "=" * 40)
    print("       文本清洗小工具 v1.0")
    print("=" * 40)
    print("1. 输入/重新输入文本")
    print("2. 去除首尾空白")
    print("3. 转换为小写")
    print("4. 转换为大写")
    print("5. 去除所有空白字符")
    print("6. 替换指定字符")
    print("7. 统计字符信息")
    print("8. 显示当前文本")
    print("0. 退出")
    print("-" * 40)


def get_multiline_input():
    """获取多行文本输入"""
    print("请输入文本（输入 END 单独一行结束）：")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)
    return "\n".join(lines)


def count_info(text):
    """统计文本信息"""
    char_count = len(text)
    # 简单按空白分割统计"词"数（中文按字符计）
    words = text.split()
    word_count = len(words)
    line_count = text.count("\n") + 1
    print(f"\n📊 文本统计：")
    print(f"  字符数（含空格）: {char_count}")
    print(f"  单词/片段数: {word_count}")
    print(f"  行数: {line_count}")


def main():
    text = ""
    print("欢迎使用文本清洗小工具！")
    print("💡 提示：此工具的技能在 Day 12 调用大模型 API 时会用到")

    while True:
        show_menu()
        choice = input("请选择功能 (0-8): ").strip()

        if choice == "0":
            print("感谢使用，再见！")
            break

        elif choice == "1":
            text = get_multiline_input()
            if text:
                print(f"✅ 已输入 {len(text)} 个字符")
            else:
                print("⚠️ 未输入任何文本")

        elif choice == "2":
            if not text:
                print("⚠️ 请先输入文本（选择 1）")
                continue
            text = text.strip()
            print("✅ 已去除首尾空白")

        elif choice == "3":
            if not text:
                print("⚠️ 请先输入文本（选择 1）")
                continue
            text = text.lower()
            print("✅ 已转换为小写")

        elif choice == "4":
            if not text:
                print("⚠️ 请先输入文本（选择 1）")
                continue
            text = text.upper()
            print("✅ 已转换为大写")

        elif choice == "5":
            if not text:
                print("⚠️ 请先输入文本（选择 1）")
                continue
            text = text.replace(" ", "").replace("\t", "").replace("\n", "")
            print("✅ 已去除所有空白字符")

        elif choice == "6":
            if not text:
                print("⚠️ 请先输入文本（选择 1）")
                continue
            old = input("请输入要替换的字符/字符串: ")
            new = input("请输入替换为: ")
            count = text.count(old)
            text = text.replace(old, new)
            print(f"✅ 已替换 {count} 处")

        elif choice == "7":
            if not text:
                print("⚠️ 请先输入文本（选择 1）")
                continue
            count_info(text)

        elif choice == "8":
            if not text:
                print("⚠️ 当前没有文本")
                continue
            print("\n📄 当前文本：")
            print("-" * 40)
            print(text)
            print("-" * 40)

        else:
            print("⚠️ 无效选择，请输入 0-8")


if __name__ == "__main__":
    main()
```

#### 运行效果示例

```
欢迎使用文本清洗小工具！
💡 提示：此工具的技能在 Day 12 调用大模型 API 时会用到

========================================
       文本清洗小工具 v1.0
========================================
1. 输入/重新输入文本
...
请选择功能 (0-8): 1
请输入文本（输入 END 单独一行结束）：
  Hello, AI World!  
  Welcome to LLM Development  
END
✅ 已输入 42 个字符

请选择功能 (0-8): 2
✅ 已去除首尾空白

请选择功能 (0-8): 7

📊 文本统计：
  字符数（含空格）: 38
  单词/片段数: 6
  行数: 2
```

#### 代码解析

| 代码 | 说明 |
|------|------|
| `def show_menu():` | 定义函数（Day 6 会系统学习） |
| `while True:` | 无限循环（Day 3 会系统学习） |
| `text.strip().upper() == "END"` | 链式调用字符串方法 |
| `text.count(old)` | 统计子串出现次数 |
| `if __name__ == "__main__":` | 程序入口，直接运行此文件时执行 |

---

### 15:30 - 15:45 | 课间休息

---

### 15:45 - 17:30 | 扩展练习

#### 练习 1：温度转换器（运用运算符）

```python
# day02/temperature.py
celsius = float(input("请输入摄氏温度: "))
fahrenheit = celsius * 9 / 5 + 32
print(f"{celsius}°C = {fahrenheit:.1f}°F")
```

#### 练习 2：BMI 计算器

```python
# day02/bmi.py
height = float(input("请输入身高（米）: "))
weight = float(input("请输入体重（公斤）: "))
bmi = weight / (height ** 2)
print(f"你的 BMI 指数为: {bmi:.1f}")

if bmi < 18.5:
    advice = "偏瘦，建议适当增加营养"
elif bmi < 24:
    advice = "正常，请保持健康生活方式"
elif bmi < 28:
    advice = "偏胖，建议适当运动"
else:
    advice = "肥胖，建议咨询医生"
print(f"健康建议: {advice}")
```

#### 练习 3：字符串切片挑战

```python
url = "https://api.deepseek.com/v1/chat/completions"

# 不使用 split，用切片提取域名
# 期望输出: api.deepseek.com
domain = url[8:url.find("/", 8)]
print(domain)

# 提取 API 版本
version = url[url.find("/v")+2:url.find("/v")+3]
print(f"API 版本: v{version}")
```

#### 练习 4：简易 Prompt 模板生成器

```python
# day02/prompt_template.py
role = input("AI 角色（如：Python 导师）: ")
task = input("任务描述: ")
language = input("回答语言（如：中文）: ")

prompt = f"""你是一位{role}。

任务：{task}

要求：
- 使用{language}回答
- 回答简洁专业
- 如需要，提供代码示例
"""
print("\n生成的 Prompt 模板：")
print("=" * 40)
print(prompt)
print("=" * 40)
```

---

## 🌙 晚自习（19:00 - 21:00）

### 19:00 - 20:00 | 字符串方法速查与实操

#### 字符串方法分类速查表

**变换类**
- `.lower()` `.upper()` `.title()` `.capitalize()` `.swapcase()`

**查找类**
- `.find(sub)` `.index(sub)` `.count(sub)` `.startswith(prefix)` `.endswith(suffix)`

**修改类**
- `.strip()` `.replace(old, new)` `.split(sep)` `.join(iterable)`

**判断类**
- `.isdigit()` `.isalpha()` `.isalnum()` `.isspace()`

#### 自习任务

1. 运行今天所有代码示例，确保理解每个运算符和方法
2. 完成「文本清洗小工具」项目
3. 尝试用 f-string 重写 Day 1 的「个人信息卡片」

### 20:00 - 21:00 | 预习 Day 3

阅读 Day 3 讲义开头，思考：
- 今天写的 BMI 计算器用了 `if/elif/else`，但还没系统学习——明天会深入
- 文本清洗工具的 `while True` 循环——明天会学更多循环用法

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | 算术运算符 + - * / // % ** | |
| 2 | 复合赋值运算符 += -= 等 | |
| 3 | 运算符优先级与括号 | |
| 4 | 比较运算符 == != > < >= <= | |
| 5 | 逻辑运算符 and or not | |
| 6 | 真值判断与链式比较 | |
| 7 | 字符串索引（正向/负向） | |
| 8 | 字符串切片 [start:end:step] | |
| 9 | 常用字符串方法 strip/replace/split/join | |
| 10 | f-string 格式化（对齐、精度、百分比） | |
| 11 | 转义字符与原始字符串 r"" | |
| 12 | 文本清洗小工具项目 | |

---

## 📝 课后作业

### 必做题

1. **文本清洗小工具**：完成下午实操项目，要求：
   - 所有 8 个菜单功能正常工作
   - 代码有适当注释
   - 提交到 GitHub：`git commit -m "Day 2: 文本清洗小工具"`

2. **f-string 练习**：编写程序，输入商品名称、单价、数量，用 f-string 输出格式化账单

3. **字符串操作练习**：给定字符串 `"  Hello, DeepSeek AI!  "`，完成：
   - 去除首尾空白
   - 将 "DeepSeek" 替换为 "通义千问"
   - 统计字符数
   - 反转字符串

### 选做题

4. **密码强度检测器**：输入密码，检查是否包含大写、小写、数字，输出强度评级
5. **Markdown 标题生成器**：输入标题文本和级别（1-6），输出对应数量的 `#` 加标题

---

## 💡 常见问题 FAQ

**Q1: `/` 和 `//` 有什么区别？**

A: `/` 是真除法，结果永远是浮点数（`10 / 2 = 5.0`）；`//` 是整除，向下取整（`10 // 3 = 3`）。在大模型开发中，计算 token 费用时常用 `//` 估算批次数量。

**Q2: `find()` 和 `index()` 有什么区别？**

A: 找不到时，`find()` 返回 `-1`，`index()` 抛出异常。日常推荐用 `find()` 更安全。

**Q3: 为什么 `text[10]` 会报 IndexError？**

A: 索引超出字符串长度。有效索引范围是 `0` 到 `len(text)-1`（或 `-len(text)` 到 `-1`）。

**Q4: f-string 中 `{score:.2f}` 的 `.2f` 是什么意思？**

A: `.2` 表示保留 2 位小数，`f` 表示浮点数格式。类似地，`:d` 是整数，`:s` 是字符串。

**Q5: 字符串是不可变的，那 `text = text.strip()` 是怎么回事？**

A: `strip()` 返回一个**新字符串**，变量 `text` 被重新赋值为新字符串。原字符串并未改变。

---

## 🔮 明日预习

**Day 3: 流程控制**

明天你将学习：

- 条件语句 `if` / `elif` / `else`
- `while` 循环与 `for` 循环
- `break`、`continue` 循环控制
- 实操项目：猜数字游戏、九九乘法表、简易菜单系统

**预习建议**：回顾今天 BMI 计算器中的 `if/elif/else`，思考如何让程序根据不同输入执行不同分支。

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 2*
