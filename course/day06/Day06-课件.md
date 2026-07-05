# Day 06:函数 —— 从"会写代码"到"会组织代码"

---

# 【旁白解读】昨天、今天、明天

先盘点这五天你欠下的"复制粘贴债",每一笔都有案底:

1. Day 03 作业 BMI 2.0:两段一模一样的输入校验循环,只差提示语;
2. Day 03/04 菜单系统:编号校验代码在"完成"和"删除"里写了两遍;猜数字逻辑在两个文件里各写一遍;
3. Day 05 作业待办重构:打印待办的循环要用四次,答案里偷跑了一个 `def show(items)` 才没抄四遍;
4. Day 05 答疑:字典驱动菜单的"完全体"要求函数能当字典的值——欠着。

**今天(Day 06)是"还债日":函数(function)一次清账。** 函数是把一段逻辑**打包、命名、参数化**的机制——一处定义,处处调用;改一处,处处生效。它是编程世界的"乐高积木标准化",也是你从"能写出跑通的代码"跨向"能组织一个项目"的分水岭。

今天的路线:

- **上午前半**:函数的定义与调用、返回值 return、"参数四件套"(位置/关键字/默认值/`*args` 与 `**kwargs`)——学完你会突然看懂这几天所有"照抄"的写法:`json.dumps(obj, ensure_ascii=False, indent=2)` 是关键字参数,`enumerate(lst, start=1)` 是默认参数,`print("a", "b", "c", sep="-")` 的 print 本身就是 `*args` 函数;
- **上午后半**:作用域(函数内外的变量世界)、lambda 匿名函数(昨天排序里照抄的那个,今天给名分)、递归入门;
- **下午**:**大重构日**——把前五天的项目重构成函数式结构,亲手体验"同样的功能,代码量减三分之一,可读性翻倍"。重构后的骨架,就是 Day 07 周测项目和 Day 14 项目一的直接底座。

**未来的钩子**:Day 08 的"方法"就是"长在类身上的函数";Day 13 的装饰器是"包装函数的函数";Day 19 的 Function Calling,顾名思义,是**让大模型来决定调用你的哪个函数**——你今天定义函数的能力,三周后会成为 Agent 的"手和脚"。函数学不牢,后面全是空中楼阁;学牢了,后面全是顺水推舟。

---

# 上午 · 第一节(9:00 - 10:40):函数的定义、调用与参数四件套

## 1.1 第一个函数:从复制粘贴的废墟上站起来

Day 02 的手机号脱敏,这几天写了至少三遍:

```python
# 这行代码你已经写了三遍:
masked = phone[:3] + "****" + phone[-4:]
```

打包成函数:

```python
# ---- 定义(def = define):打包逻辑,起名,声明需要什么材料 ----
def mask_phone(phone):
    """把 11 位手机号脱敏为 138****5678 的形式。"""      # 文档字符串,一会儿讲
    return phone[:3] + "****" + phone[-4:]

# ---- 调用:名字 + 括号 + 递材料 ----
print(mask_phone("13812345678"))     # 138****5678
print(mask_phone("13900001111"))     # 139****1111
result = mask_phone("13700002222")   # 返回值可以接住继续用
```

解剖定义的语法:

```
def mask_phone(phone):
└┬┘ └───┬────┘ └─┬─┘│
 │      │        │  └── 冒号 + 缩进块:老规矩(if/for 的同款)
 │      │        └── 参数(parameter):函数需要的"原材料"占位符
 │      └── 函数名:蛇形命名,动词开头(mask/get/save/check……)
 └── def 关键字:定义函数

    return phone[:3] + "****" + phone[-4:]
    └─┬──┘
      └── return:把结果"递出去"并立刻结束函数
```

**三个立刻要建立的认知:**

**认知 1:定义 ≠ 执行。** `def` 块只是"登记了一份菜谱",Python 读到它时**不执行**里面的代码;只有调用 `mask_phone(...)` 时才照着菜谱做菜。初学者常犯:定义完就以为运行了,程序啥也没输出——因为没调用。

**认知 2:return 与 print 是两码事(今天头号考点)。**

```python
def add_print(a, b):
    print(a + b)             # 只是"喊出"结果:显示在屏幕上,然后就没了

def add_return(a, b):
    return a + b             # 把结果"递出去":调用方可以接住继续用

x = add_print(3, 5)          # 屏幕上出现 8,但……
print(x)                     # None!—— print 版没有 return,函数默认递出 None

y = add_return(3, 5)         # 屏幕安静,但结果被 y 接住了
print(y * 10)                # 80 —— 能继续参与计算
```

心法:**print 是给人看的,return 是给程序用的**。函数的正职是"加工原料递出成品"(return);要不要顺便喊一嗓子(print)是副业。经验法则:**工具函数只 return 不 print**,打印留给调用方决定——这样同一个函数既能用在命令行程序里(调用方 print),也能用在 Web 接口里(调用方塞进 JSON 响应),复用性天差地别。

**认知 3:return 立刻终结函数。** return 之后的代码永远不执行。这带来一个昨天预告的重构神技——**提前返回(early return)**,Day 03 的"嵌套地狱化解技巧 2"今天兑现:

```python
# 嵌套版(箭头形代码,难读)
def check_password_nested(pwd):
    if len(pwd) >= 8:
        if not pwd.isdigit():
            if pwd.lower() != pwd:
                return "强"
            else:
                return "中"
        else:
            return "弱:纯数字"
    else:
        return "弱:太短"

# 提前返回版(平铺直叙,把"不合格"先踢出去)
def check_password(pwd):
    if len(pwd) < 8:
        return "弱:太短"            # 不合格?立刻走人
    if pwd.isdigit():
        return "弱:纯数字"          # 又一批走人
    if pwd.lower() == pwd:
        return "中"                 # 没有大写字母
    return "强"                     # 活到最后的都是强密码
# 每个 if 处理完一种情况就 return 离场,永远不需要 else,缩进永远一层
```

## 1.2 参数四件套

### ① 位置参数:按顺序对号入座

```python
def make_message(role, content):
    """组装一条 messages 消息(Day 05 的结构,今天开始函数化)。"""
    return {"role": role, "content": content}

msg = make_message("user", "你好")            # "user"→role,"你好"→content,按位置
print(msg)                                    # {'role': 'user', 'content': '你好'}
# 顺序错了不报错但语义全错:make_message("你好", "user") → role 变成了"你好"!
# 位置参数的软肋:参数一多,顺序靠背——所以有了第二件套
```

### ② 关键字参数:指名道姓,顺序随意

```python
msg = make_message(content="你好", role="user")     # 点名递材料,顺序无所谓
# 这就是你抄了四天的写法的真身:
# json.dumps(obj, ensure_ascii=False, indent=2)
#            └─位置参数─┘ └────── 关键字参数 ──────┘
# 规则:位置参数必须在关键字参数前面;混用时先位置后关键字
```

**工程建议:超过两个参数的调用,后面的都用关键字**——`create_user("张三", 28, True, False)` 里的 True/False 是什么鬼?`create_user("张三", 28, is_vip=True, is_banned=False)` 一目了然。

### ③ 默认参数:不传就用出厂设置

```python
def make_message(content, role="user"):        # role 不传时默认 "user"
    return {"role": role, "content": content}

print(make_message("你好"))                        # 默认 user(最常用的情况最省事)
print(make_message("你是助教", role="system"))      # 需要时显式覆盖

# enumerate(lst, start=1) 的 start、print 的 sep/end、
# range 的步长……你用了一周的"可选项",全是默认参数。
# 设计心法:把 80% 场景的取值设为默认,让常见调用最短。
```

**默认参数的一个著名地雷,今天必须拆了它:默认值不要用可变对象(列表/字典)!**

```python
# ❌ 地雷版:默认列表在"定义那一刻"创建,且只创建一次,所有调用共享!
def add_task_bad(task, todos=[]):
    todos.append(task)
    return todos

print(add_task_bad("A"))     # ['A']
print(add_task_bad("B"))     # ['A', 'B'] ?!—— 上次的 A 还在!两次调用共用同一个列表
# (Day 04 可变性大坑的函数版变身)

# ✅ 正确版:默认给 None,函数体内再造新列表
def add_task(task, todos=None):
    if todos is None:            # is None 是判断 None 的规范写法(而不是 == None)
        todos = []               # 每次调用都造全新的列表
    todos.append(task)
    return todos

print(add_task("A"))         # ['A']
print(add_task("B"))         # ['B'] —— 各自独立,符合直觉
```

这是 Python 面试的高频陷阱题,也是真实项目里的隐蔽 bug 源。口诀:**默认值只用不可变的(数字/字符串/None/元组);要可变容器,默认 None 进去再造。**

### ④ `*args` 与 `**kwargs`:数量不定的参数

```python
# *args:把多余的"位置参数"打包成元组
def average(*scores):                 # 调用时想传几个传几个
    if not scores:                    # 防空:没传任何参数时 scores 是空元组
        return 0
    return sum(scores) / len(scores)

print(average(90, 85))                # 87.5
print(average(90, 85, 77, 60))        # 78.0
# print("a", "b", "c") 能随便传几个值,因为 print 的定义就是 print(*objects, ...)

# **kwargs:把多余的"关键字参数"打包成字典
def call_llm(model, **options):       # 除 model 外的具名参数全进 options 字典
    print(f"模型:{model}")
    print(f"可选参数:{options}")

call_llm("deepseek-chat", temperature=0.7, max_tokens=200, stream=False)
# 模型:deepseek-chat
# 可选参数:{'temperature': 0.7, 'max_tokens': 200, 'stream': False}
# 【伏笔】Day 25 的 LangChain 源码里 **kwargs 铺天盖地——各家模型参数不同,
# 框架用 **kwargs "照单全收再转交",这是它能统一调度百家模型的语法基础

# 反向操作:调用时解包。字典前加 ** 把键值对摊开成关键字参数
params = {"temperature": 0.7, "max_tokens": 200}
call_llm("deepseek-chat", **params)          # 等价于逐个写 temperature=0.7, ...
# 【实用】配置存在字典/JSON 文件里(Day 05 的能力),运行时 ** 一撒就传参——
# "配置与代码分离"再进一步
```

四件套的完整排队顺序(能读懂即可,自己写函数用不了这么全):`def f(位置, 默认值=x, *args, **kwargs)`。

## 1.3 文档字符串与类型注解:让函数自带说明书

```python
def estimate_cost(tokens_in: int, tokens_out: int, price_in: float = 1.0, price_out: float = 4.0) -> float:
    """估算一次大模型 API 调用的成本。

    参数:
        tokens_in: 输入 token 数
        tokens_out: 输出 token 数
        price_in: 输入价格(元/百万 token),默认 DeepSeek 价
        price_out: 输出价格(元/百万 token)
    返回:
        成本(元)
    """
    return tokens_in / 1_000_000 * price_in + tokens_out / 1_000_000 * price_out
```

两样新东西:

1. **文档字符串(docstring)**:def 下第一行的三引号字符串,是函数的官方说明书。VS Code 里鼠标悬停在函数名上就能看到它;`help(estimate_cost)` 也能打印它。**公司代码规范普遍强制要求**,我们从今天开始也强制:每个正式函数必须有 docstring(一行版也行);
2. **类型注解**:`tokens_in: int` 说明参数期望类型,`-> float` 说明返回类型。**注意它只是"注释级"的声明,Python 不强制检查**(传字符串进去也能跑到出错为止),但它让编辑器能提示、让读者秒懂。Day 13 正式讲 typing,Day 23 的 FastAPI 会把类型注解玩出真正的魔法(自动校验 + 自动生成文档),今天先养成写的习惯。

---

# 上午 · 第二节(10:50 - 12:00):作用域、lambda 与递归

## 2.1 作用域:函数内外是两个世界

```python
count = 0                        # 全局变量:定义在函数外,整个文件可见

def demo():
    msg = "函数内部的临时变量"      # 局部变量:函数内定义,函数结束即销毁
    print(count)                 # ✅ 函数内可以"读"全局变量
    print(msg)

demo()
# print(msg)                     # ❌ NameError:msg 只活在函数里,外面不认识

# ⚠️ 读可以,"改"不行:
def try_modify():
    # count = count + 1          # UnboundLocalError!
    # Python 规则:函数内一旦对某名字赋值,该名字全程按"局部变量"处理,
    # 而这行右边的 count 还没被局部赋值过 → 报错
    pass

# 强行改全局:global 声明(能用,但强烈不推荐)
def bad_style():
    global count
    count += 1                   # 声明后就能改了……但是:

# 为什么不推荐 global?
# 函数偷偷改外面的变量 = "看不见的手"。调用 10 个函数后全局变量变成什么样,
# 没人说得清,调试是噩梦。工程正道:
#   数据用"参数"递进去,结果用"return"递出来,函数不碰外面的东西。
# 这样的函数叫"纯函数":同样输入必得同样输出,可测试、可复用、可并行。

def good_style(count):
    return count + 1             # 进出都走明路
count = good_style(count)
```

**一个必须现在澄清的例外(Day 04 大坑的函数版)**:参数传的是"标签"——把**可变对象**(列表/字典)传进函数,函数内通过它修改,**外面的原件也变**:

```python
def add_message(messages, content):
    """往对话历史里添加一条用户消息(故意的原地修改)。"""
    messages.append({"role": "user", "content": content})    # 改的就是外面那个列表

history = []
add_message(history, "你好")
print(history)                   # [{'role': 'user', 'content': '你好'}] —— 外面真的变了
```

这算 bug 吗?**不算,这是常用手法**——对话历史本来就该被累积,函数名 add_message 也明示了"我要往里加"。要点是**知情 + 故意**:知道传列表进函数 = 给函数原件的钥匙;函数要么明示会修改(add/append/update 系动词命名),要么内部先 copy 再操作。失控的是"不知情的修改",不是修改本身。

## 2.2 lambda:一次性小函数

昨天排序时照抄的 `key=lambda t: order[t["priority"]]`,今天正名:

```python
# lambda 参数: 表达式  ——  一行版匿名函数,自动 return 表达式的值
square = lambda x: x ** 2         # 等价于 def square(x): return x ** 2
print(square(5))                  # 25(这样赋值给名字属于教学演示,实战别这么用)

# lambda 的真正主场:作为参数递给别的函数,"告诉它按什么规则办事"
todos = [
    {"task": "复习", "priority": 2},
    {"task": "写作业", "priority": 1},
    {"task": "刷题", "priority": 3},
]
todos.sort(key=lambda t: t["priority"])          # 按 priority 字段排
print([t["task"] for t in todos])                # ['写作业', '复习', '刷题']

scores = [("张三", 92), ("李四", 85), ("王五", 88)]
top = max(scores, key=lambda s: s[1])            # 按元组的第 2 项找最大
print(top)                                       # ('张三', 92)

# 尺度:lambda 只装得下"一个表达式"。要写 if/for/多步逻辑?老老实实 def。
# 心法:lambda 是便利贴,def 是正式文件。规则简单用便利贴,复杂就立正式文件。
```

## 2.3 递归入门:函数调用自己

```python
def countdown(n):
    """倒数:递归版(教学演示)。"""
    if n == 0:                    # ① 出口(base case):必须有,否则无限递归
        print("发射!")
        return
    print(n)
    countdown(n - 1)              # ② 自我调用:问题规模必须缩小(n → n-1)

countdown(3)                      # 3 2 1 发射!

# 经典例子:阶乘  n! = n × (n-1)!
def factorial(n):
    if n <= 1:                    # 出口:1! = 1
        return 1
    return n * factorial(n - 1)   # 把"算 n!"委托给"算 (n-1)! 的自己"

print(factorial(5))               # 120
```

递归两要素:**出口 + 规模缩小**,缺出口就是函数版死循环(Python 会在约 1000 层时抛 RecursionError 强制刹车)。坦白说:**日常应用开发中递归出场率不高**(循环通常更直观),今天入门它有两个理由:① 面试和 LeetCode 常客;② 天然适配"嵌套结构"的处理——比如遍历一个深度未知的 JSON(字典套列表套字典……),递归是最优雅的解法,Day 28 处理带层级的文档目录树时会重逢。今天到"能看懂、能写倒数和阶乘"即可,不必深钻。

---

# 下午 · 实操(14:00 - 17:30):大重构日 —— 给前五天的代码"函数化装修"

## 3.1 需求文档

> ### 需求文档:学习工具箱 v2.0(函数化重构)
>
> **需求编号**:REQ-D06-001
> **需求方**:「智言科技」培训部
> **背景**:前五天积累的小工具(文本清洗、手机号脱敏、猜数字、待办管理)代码全部平铺,重复严重,维护困难。要求按公司代码规范重构为函数式结构,作为 Day 07 周测项目和 Day 14 项目一的基座。
>
> **重构要求(公司代码规范节选)**:
> 1. 每个功能一个函数,函数只做一件事(单一职责);
> 2. 工具函数只 return 不 print(展示与逻辑分离);
> 3. 重复代码必须提取为公共函数(DRY 原则:Don't Repeat Yourself);
> 4. 每个函数必须有 docstring 和类型注解;
> 5. 主流程必须在 `main()` 函数中,文件末尾用 `if __name__ == "__main__": main()` 启动(该写法今天先照抄记住,Day 10 讲模块时揭晓原理);
> 6. 菜单必须字典驱动:选项号 → (功能名, 函数) 的映射,新增功能只改一处。
>
> **验收标准**:功能与重构前完全一致;全部规范逐条落实;代码行数可见地下降。

## 3.2 架构设计:三层结构

```
┌─────────────────────────────────────────────┐
│ 入口层   main()                              │
│   主循环:显示菜单 → 读选择 → 从 MENU 字典     │
│   里取出函数 → 调用                           │
├─────────────────────────────────────────────┤
│ 功能层   run_cleaner() run_mask()            │
│          run_guess()  run_todo()             │
│   每个功能一个函数;负责该功能的交互与展示      │
├─────────────────────────────────────────────┤
│ 工具层   clean_text()  mask_phone()          │
│          read_int_in_range()  …              │
│   纯逻辑,只 return 不 print;被功能层复用     │
└─────────────────────────────────────────────┘
```

**分层的判断标准**:工具层函数换个项目也能直接用(mask_phone 放进任何项目都成立);功能层绑定本程序的交互流程;入口层只负责"调度"。这个三层结构,就是 Day 23 FastAPI 项目"路由层 / 服务层 / 工具层"的雏形——**你今天学的不是怎么写这一个程序,是怎么组织所有程序**。

## 3.3 重构实录(节选核心,完整代码见 code/toolbox.py)

### 第一步:提取工具层(那些被抄了 N 遍的代码)

```python
# =============================================
# 学习工具箱 v2.0 —— 函数化重构
# 需求编号:REQ-D06-001
# 架构:入口层 main / 功能层 run_* / 工具层(纯函数)
# =============================================
import random


# ──────────────── 工具层:纯函数,只 return 不 print ────────────────

def clean_text(text: str, banned_words: list = None) -> str:
    """清洗文本:去两端空白、小写化、规范空格、敏感词打码。

    Day 02 的四道工序流水线,函数化后成为可复用组件。
    banned_words 默认 None 再造列表——上午刚拆的地雷,实弹演习。
    """
    if banned_words is None:
        banned_words = ["垃圾", "傻子", "废物"]
    result = " ".join(text.strip().lower().split())     # F1+F2+F4
    for word in banned_words:                            # F3:Day 03 承诺的循环版
        result = result.replace(word, "*" * len(word))   # 等长打码
    return result


def mask_phone(phone: str) -> str:
    """手机号脱敏:138****5678。写了五遍的代码,从此只此一份。"""
    return phone[:3] + "****" + phone[-4:]


def read_int_in_range(prompt: str, low: int, high: int) -> int:
    """读取一个 [low, high] 范围内的整数,不合法就重问,保证返回合法值。

    Day 03 校验循环的最终归宿:菜单编号、猜数字、年龄……所有
    "要一个范围内整数"的场合,一行调用解决。这就是 DRY 的威力。
    """
    while True:
        text = input(prompt).strip()
        if not text.isdigit():
            print("请输入数字!")
            continue
        value = int(text)
        if not (low <= value <= high):
            print(f"请输入 {low}-{high} 之间的数!")
            continue
        return value            # return 直接终结循环+函数,连 break 都省了
```

注意 `read_int_in_range` 的最后一行:**return 兼职了 break**——函数版校验循环比 Day 03 的裸版还少一行。这类"打包后反而更顺"的体验,今天下午会反复出现。

### 第二步:功能层(每个功能一个函数)

```python
# ──────────────── 功能层:负责交互,调用工具层 ────────────────

def run_cleaner() -> None:            # -> None:不返回有意义的值(纯交互)
    """功能:文本清洗。"""
    raw = input("请输入待清洗文本:")
    print(f"清洗结果:{clean_text(raw)}")        # 逻辑一行搞定:工具层的红利


def run_mask() -> None:
    """功能:手机号脱敏。"""
    while True:
        phone = input("请输入 11 位手机号:").strip()
        if phone.isdigit() and len(phone) == 11:
            break
        print("格式不对!")
    print(f"脱敏结果:{mask_phone(phone)}")


def run_guess() -> None:
    """功能:猜数字。Day 03 写了两遍的逻辑,从此一份。"""
    answer = random.randint(1, 100)
    count = 0
    print("我想好了一个 1-100 的数")
    while True:
        guess = read_int_in_range("你猜:", 1, 100)      # 工具层复用:三行变一行
        count += 1
        if guess > answer:
            print("大了 ↓")
        elif guess < answer:
            print("小了 ↑")
        else:
            print(f"猜中!共 {count} 次")
            return              # 函数里退出多层逻辑,return 比 break 干脆
```

### 第三步:字典驱动的入口层(Day 05 欠账的"完全体")

```python
# ──────────────── 入口层:字典驱动的主循环 ────────────────

def main() -> None:
    """程序入口:菜单调度。"""
    # 字典的值是 (功能名, 函数) 元组——函数不带括号!
    # 带括号是"立刻执行拿结果",不带括号是"函数本身"(可以存、可以传,
    # 需要时再加括号执行)。函数在 Python 里是"一等公民",能像数据一样搬运——
    # 这也是 Day 13 装饰器、Day 19 工具注册表的语法根基
    menu = {
        "1": ("文本清洗", run_cleaner),
        "2": ("手机号脱敏", run_mask),
        "3": ("猜数字游戏", run_guess),
    }

    while True:
        print()
        print("=" * 36)
        print("      学习工具箱 v2.0(函数版)")
        print("=" * 36)
        for key, (name, _) in menu.items():        # 拆包:值是元组,函数用 _ 占位
            print(f"  {key}. {name}")
        print("  0. 退出")

        choice = input("请选择:").strip()
        if choice == "0":
            print("再见!")
            break
        if choice not in menu:
            print(f"没有选项 [{choice}]")
            continue

        _, func = menu[choice]        # 从字典取出函数
        func()                        # 加括号:执行!


if __name__ == "__main__":            # 今天照抄,Day 10 揭晓原理:
    main()                            # "直接运行本文件才执行 main,被 import 时不执行"
```

**看新增功能的成本变化**:重构前——菜单打印处加一行 + 分发器加一段 elif(两处,容易漏);重构后——写一个 `run_xxx` 函数 + menu 字典加一行(功能和注册天然在一起)。Day 19 的 Function Calling 工具注册表、Day 40 LangChain 的 Tool 列表,就是这个"注册表模式"的行业标准版。**你今天写的 menu 字典,和三周后 Agent 的工具表,是同一个设计思想。**

## 3.4 重构前后对账(当堂对比)

| 指标 | 重构前(Day 03/04 版) | 重构后 |
|------|----------------------|--------|
| 猜数字逻辑份数 | 2 份(两个文件各一份) | 1 份 |
| 输入校验代码 | 4 处各写一遍 | 1 个函数调 4 次 |
| 新增功能改动点 | 2 处(菜单+分发) | 1 处(注册表) |
| 主循环行数 | ~60 行 | ~20 行 |
| 单个函数可独立测试 | 不可能(全糊在一起) | 每个都可以 |

最后一行最值钱:**函数是可测试性的最小单元**。`assert mask_phone("13812345678") == "138****5678"` 一行就是一个测试(Day 05 的 assert 复利)——糊成一团的代码连测试的"抓手"都没有。

---

# 【常见错误与排错手册】Day 06 专属篇

**错误 1:定义了函数没调用,程序"什么都不干"。** def 只登记菜谱不做菜。检查文件末尾有没有 `main()` 或函数调用。

**错误 2:忘写 return,接到 None。** `result = f(...)` 后 `print(result)` 是 None → 九成是函数里只 print 没 return。补 return,或想清楚这个函数到底该不该有产出。

**错误 3:`TypeError: f() missing 1 required positional argument`。** 调用时少递了材料。看报错里点名缺谁,补上;或给该参数设默认值。

**错误 4:`TypeError: f() got multiple values for argument 'x'`。** 位置参数和关键字参数给同一个参数重复喂料:`f(1, x=2)` 而 x 正好是第一个参数。删掉重复的一个。

**错误 5:默认参数用了可变对象,数据"串台"。** 上午拆过的地雷:`def f(items=[])` 所有调用共享一个列表。改 `items=None` + 函数内再造。

**错误 6:函数内改全局变量报 UnboundLocalError。** 函数内赋值即局部。正道:参数进、return 出;确实要全局,global 声明(慎用)。

**错误 7:menu 字典里函数带了括号。** `{"1": ("清洗", run_cleaner())}` ——写定义时就执行了一遍,存进去的是执行结果(None)!注册表里放函数**本身**(不带括号),调用时再加括号。

**错误 8:lambda 里写复杂逻辑挤不下。** lambda 只容一个表达式。挤不下=在提醒你该用 def 了。

---

# 【课堂笔记】Day 06 知识点速查表

**定义与调用**
- `def 名(参数):` + docstring + 缩进体;调用 `名(材料)`
- 定义 ≠ 执行;函数名动词开头蛇形命名
- **print 给人看,return 给程序用**;工具函数只 return 不 print
- return 立刻终结函数(还兼职 break);没 return 默认递出 None
- 提前返回:不合格先踢走,消灭嵌套

**参数四件套**
1. 位置:按顺序对号入座
2. 关键字:`f(x=1)` 指名道姓;多参数调用后面的都用关键字
3. 默认值:`def f(a, b=10)`;**地雷:默认值禁用可变对象,用 None 再造**
4. `*args` 元组收位置参数 / `**kwargs` 字典收关键字参数;`f(**配置字典)` 反向解包

**规范三件**:docstring 说明书 | 类型注解 `x: int -> str`(编辑器友好,不强制)| `if __name__ == "__main__": main()`(Day 10 揭晓)

**作用域**
- 函数内=局部(用完销毁);外=全局;内可读外,赋值即局部
- global 能改全局但慎用;正道:参数进 return 出(纯函数)
- 传可变对象=给钥匙:函数内 append 外面也变(知情+故意则是特性)

**lambda**:`lambda x: 表达式`;主场是 sort/max/min 的 key;复杂逻辑请 def
**递归**:出口 + 规模缩小;缺出口 = RecursionError;适配嵌套结构

**函数是一等公民**:可存进字典(注册表模式)、可作参数(key=)、可被返回(Day 13 装饰器)
**三层架构**:入口(main 调度)/ 功能(run_* 交互)/ 工具(纯函数)——FastAPI 分层的雏形

---

# 【附录】课堂答疑实录(晚自习整理)

**问 1:函数应该多大?我怕拆得太碎。**

答:两个实用标尺:① **一屏原则**——不滚动屏幕能看完(约 30-40 行),超了就该拆;② **一句话原则**——你能用一句不带"和"字的话说清它干什么("清洗文本"✅;"清洗文本和保存文件和发通知"❌,拆三个)。拆得碎的代价远小于糊成坨的代价:碎函数最多让你多点几次跳转,坨代码会让三个月后的你重写整个文件。初学阶段宁碎勿坨。

**问 2:参数和全局变量,什么时候用哪个传数据?**

答:默认永远用参数。全局只留给两类东西:① 真正的常量(全大写:`PRICE_TABLE`、`MAX_RETRY`)——只读不改,没有"看不见的手"问题;② 程序唯一的核心状态且传参会让每个函数都多拖一个参数(比如今天工具箱如果有全局配置)。但即便是②,更专业的解法是 Day 08 的类(把状态和操作它的函数封装在一起)——所以答案其实是:**现在用参数,周一学了类之后用类**。

**问 3:`-> None` 和不写返回类型注解有区别吗?**

答:对 Python 运行没区别,对人和工具有区别。`-> None` 是明确宣告"此函数没有产出,别接它的返回值";不写是"没说"。规范里推荐写:让"这是纯交互函数"和"作者忘了标"可区分。类型注解的哲学就是把隐含的约定显式化——写代码是给三类读者:机器、同事、三个月后的你,后两类最需要注解。

**问 4:`if __name__ == "__main__"` 到底什么意思?每个文件都要写吗?**

答:完整原理 Day 10(模块)揭晓,今天给最短版:这行的意思是"**只有直接运行本文件时才执行下面的代码;本文件被别的文件 import 借用时不执行**"。为什么需要?Day 10 你会把工具函数拆到独立文件,别的文件 `import toolbox` 借用 mask_phone——如果 toolbox.py 里的 main() 裸奔在文件末尾,import 的瞬间菜单就弹出来了,谁受得了。要不要每个文件都写:凡是"既可能直接跑、也可能被借用"的文件都写;纯脚本(肯定只直接跑)可以不写,但写了不亏,我们规范统一写。

**问 5:lambda 看起来能少写好几行,为什么课件反复劝我少用?**

答:因为它省的是"写的人"的三行,费的是"读的人"的三秒——而代码被读的次数是被写的十倍。lambda 的合法生态位很窄:**作为参数,表达一条简单规则**(按什么排序、按什么找最大)。超出这个范围的 lambda 都是负资产。一个判别法:如果你想给 lambda 起个名字,说明它值得成为 def。

**问 6:递归和循环怎么选?阶乘用循环也能写吧?**

答:能,而且循环版更快更省内存(没有层层调用的开销)。选择标准:**问题本身是"平铺"的用循环(数数、遍历列表);问题本身是"套娃"的用递归(深度未知的嵌套 JSON、文件夹套文件夹、树形目录)**。套娃问题用循环写反而要自己管理一个栈,更绕。日常应用开发 95% 是平铺问题,所以循环为主;但那 5% 的套娃场景(Day 28 的文档树、面试的二叉树题),递归是唯一优雅解。

**问 7:今天说"函数是一等公民,能存能传",这到底有什么大用?感觉只是个菜单小技巧。**

答:这个特性是后面三个大杀器的地基,预告一下:① **Day 13 装饰器**:`@retry` 一行给任何函数加上重试能力——本质是"接收函数、返回加强版函数的函数";② **Day 19 Function Calling**:把你的函数注册给大模型,模型说"调 get_weather"你就从注册表(今天的 menu 字典同款!)里取出函数执行;③ **Day 40 LangChain Tool**:`@tool` 装饰器把函数变成 Agent 的工具。三者的共同前提就是"函数可以被当成数据搬运"。今天的菜单是这个思想的第一次落地,不是最后一次。

**问 8:重构会不会把原来能跑的代码改坏?有点不敢动手。**

答:会,所以工程界有配套纪律:① **小步走**——一次只提取一个函数,立刻运行验证,再动下一个(今天下午我们就是这么做的);② **行为不变**——重构的定义就是"不改变外部行为的内部结构调整",每步都拿同样的输入试,输出必须一样;③ **Git 兜底**——重构前先 commit,改坏了 `git checkout .` 一秒回滚(Day 01 的 Git 在这里变现!)。职业建议:重构的胆量来自"随时能回去"的保障,而不是"肯定不会错"的自信。

---

# 【明日预告】Day 07:第一周复习与周测

明天是第一周的验收日。上午:六天知识点串讲 + 答疑(变量类型 → 字符串 → 流程控制 → 容器 → JSON → 函数,一条线捋通);下午:**周测**(笔试 30 分钟 + 上机 90 分钟)+ 综合项目:**命令行"通讯录管理系统"**——增删改查 + JSON 持久化,它是本周全部知识的合体:联系人是字典、通讯录是字典列表(Day 05)、操作是函数(Day 06)、调度是主循环+分发器(Day 03)、校验用循环(Day 03)、显示用 enumerate 和 f-string 对齐(Day 04/02)、退出前 dumps 保存(Day 05,文件写入给简化模板,Day 11 转正)。今晚请优先复习:第一名句、messages 结构、字典计数器、read_int_in_range 的写法——明天全考。

**睡前自检清单**:
- [ ] 能说清 return 和 print 的区别、默认参数地雷、注册表模式
- [ ] toolbox.py 重构完成且功能与原版一致
- [ ] LeetCode:LC 344(反转字符串,函数版)、LC 509(斐波那契数,先循环后递归各写一遍)
- [ ] 作业完成并 push,绿格子连续第 6 天
