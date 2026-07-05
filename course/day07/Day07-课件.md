# Day 07:第一周复习与周测 —— 把六天的珠子串成一条链

---

# 【旁白解读】今天为什么是"复习日"而不是"新课日"?

先说一个学习科学的事实:**新知识如果 72 小时内不被"提取"(主动回忆、动手使用),遗忘率超过 70%**。前六天我们以每天一个大主题的速度推进,今天必须停下来做三件事:

1. **串讲**:把六天的知识点从"六颗散珠"串成"一条链"——你会看到它们不是六个孤立话题,而是一条精心设计的因果链;
2. **周测**:笔试 + 上机,不是为了排名,是为了让你**精确知道**自己哪块虚。模糊的"我大概都会"是复习的最大敌人;
3. **综合项目**:通讯录管理系统——第一周全部知识的合体考核,也是你简历上第一个"完整"的作品(麻雀虽小,五脏俱全:数据建模、分层架构、输入校验、持久化)。

**今天与前后的连接**:通讯录项目里首次实现"数据存活过程序重启"(JSON 持久化),这是 Day 14 项目一"对话历史保存"的直接彩排;明天(Day 08)开始第二周,进入面向对象——你会发现 OOP 的第一课就是把今天通讯录里"数据(字典)+ 操作数据的函数"绑定成一个"类",第一周和第二周之间没有缝。

---

# 上午 · 串讲(9:00 - 12:00):六天知识的因果链

## 1.1 一张图看懂第一周

```
Day 01  变量/类型/输入输出          "程序 = 输入 → 处理 → 输出"
   │      f-string ────────────────────────────┐
   ▼                                           │
Day 02  运算符/字符串方法            数据的"清洗"与"提问"能力
   │      strip/split/join/replace ────────────┤
   ▼                                           │
Day 03  if/while/for               程序会"选路"和"重复"        │
   │      主循环+分发器骨架 ────────────────────┤
   ▼                                           │
Day 04  列表/元组/集合              数据有了"家"(容器)         │
   │      append/推导式/可变性 ─────────────────┤
   ▼                                           │
Day 05  字典/JSON                  数据有了"名字"和"通用语"     │
   │      messages结构/第一名句 ────────────────┤
   ▼                                           ▼
Day 06  函数                       代码有了"组织"          全部汇入
   │      三层架构/注册表模式                 今天的通讯录项目
   ▼                                     和 Day 14 的 AI 助手
Day 07  ★ 你在这里:合体验收
```

**串讲的主线问题:如果要做一个 AI 对话助手,每一天分别贡献了什么?**

- Day 01:助手的骨架是"输入(用户提问)→ 处理 → 输出(打印回答)";Prompt 用 f-string 组装;
- Day 02:用户输入要 `strip().lower()` 清洗;判断指令用 `startswith("/")`;
- Day 03:主体是 `while True` 主循环,`/exit` 就 break,空输入就 continue;
- Day 04:对话历史是一个不断 `append` 的**列表**;超长了切片截断;
- Day 05:每条消息是 `{"role": ..., "content": ...}` **字典**;和 API 的通信语言是 **JSON**;回答藏在 `data["choices"][0]["message"]["content"]`;
- Day 06:每个动作(组消息、存历史、格式化输出)是一个**函数**,主循环只做调度。

看懂这条线,你就明白:**第一周不是"Python 基础",是"AI 助手零件生产周"。** Day 14 的项目一,只是把这些零件加上一根网线(Day 12 的 requests)组装起来。

## 1.2 高频考点快问快答(周测前的最后检查)

> 串讲课上讲师快速提问,学员抢答。这里整理成自测清单,每题先自己答,再看括号里的答案要点。

**Day 01 组**
1. `input()` 的返回值类型?(永远 str)
2. `int("28.5")` 的结果?(ValueError;要先 float 再 int)
3. `f"{0.856:.1%}"` 输出?(85.6%)
4. Git 三连的顺序?(add → commit -m → push)

**Day 02 组**
5. `"Python"[1:4]` 是?(yth——含头不含尾)
6. `s.strip()` 不赋值会怎样?(白调用,字符串不可变)
7. `"a,b".split(",")` 和 `"-".join(["a","b"])` 各得什么?(['a','b'] 和 "a-b";join 的分隔符在前)
8. `"3" + 5` 会?(TypeError,Python 拒绝猜测)

**Day 03 组**
9. elif 链命中一个后,后面的还看吗?(不看,命中即退出)
10. break 和 continue 的区别?(不玩了 / 这把不算再来)
11. `range(1, 10, 2)` 产出?(1 3 5 7 9)
12. 死循环的急刹车?(Ctrl + C)

**Day 04 组**
13. `b = a` 之后改 b,a 变吗?(a 是列表则变——同一对象两张标签;要副本用 copy)
14. `lst.sort()` 的返回值?(None!要新列表用 sorted)
15. `[x*2 for x in range(3)]` 是?([0, 2, 4])
16. 空集合怎么写?(set(),{} 是空字典)

**Day 05 组**
17. `d["k"]` 与 `d.get("k")` 缺键时各怎样?(KeyError / None——必要字段用前者,可选字段用后者)
18. JSON 里 True 怎么写?(true 全小写)
19. "第一名句"默写?(data["choices"][0]["message"]["content"])
20. loads 和 dumps 的方向?(loads:字符串→对象"解析进来";dumps:对象→字符串"序列化出去")

**Day 06 组**
21. 没写 return 的函数返回什么?(None)
22. `def f(items=[])` 的问题?(默认可变对象所有调用共享;改 None 再造)
23. 注册表字典里函数带不带括号?(不带!带了是立刻执行)
24. 工具函数为什么只 return 不 print?(展示与逻辑分离,保住复用性)

**答对 20+ 的同学,下午的周测稳了;低于 15 的,用上午剩余时间重点回看对应天的"课堂笔记"节。**

## 1.3 三段"必须焊死"的代码(闭眼能写)

```python
# ① 字典计数器(Day 05)——词频、投票、统计的万能模板
counter = {}
for item in items:
    counter[item] = counter.get(item, 0) + 1

# ② 范围整数读取(Day 03+06)——一切"要编号"场合的守门员
def read_int_in_range(prompt: str, low: int, high: int) -> int:
    """读取 [low, high] 内的整数,不合法重问。"""
    while True:
        text = input(prompt).strip()
        if not text.isdigit():
            print("请输入数字!")
            continue
        value = int(text)
        if not (low <= value <= high):
            print(f"请输入 {low}-{high} 之间的数!")
            continue
        return value

# ③ messages 一轮对话(Day 04+05)——Day 14 的心脏
messages.append({"role": "user", "content": user_input})
# ……(Day 12 起这里是真实 API 调用)……
messages.append({"role": "assistant", "content": ai_reply})
```

---

# 下午 · 第一节(14:00 - 14:40):周测(笔试部分)

> 闭卷,30 分钟,满分 50。真题与答案附在本课件末尾【周测试卷与答案】一节——**请先做完再翻答案**,自测的意义在于暴露盲区。

---

# 下午 · 第二节(14:50 - 17:30):综合项目——通讯录管理系统

## 2.1 需求文档

> ### 需求文档:命令行通讯录管理系统 v1.0
>
> **需求编号**:REQ-D07-001(第一周综合考核项目)
> **需求方**:「智言科技」行政部
> **背景**:行政部需要一个命令行通讯录工具管理员工联系方式。本项目为第一周综合考核:覆盖字典建模、函数分层、输入校验、JSON 持久化四大能力。
>
> **数据模型**:每个联系人为一个字典:
> ```json
> {"name": "张三", "phone": "13812345678", "email": "zhang@x.com", "group": "研发"}
> ```
> 通讯录整体为字典列表。
>
> **功能需求**:
> 1. 列表:带编号显示全部联系人(姓名、脱敏手机号、分组);
> 2. 添加:姓名非空且不重复;手机号必须 11 位纯数字;邮箱必须含且只含一个 @ 且不在开头(Day 02/03 作业规则的复用);分组可空,默认"未分组";
> 3. 搜索:按关键词模糊匹配姓名或手机号(包含即命中),显示命中列表;
> 4. 修改:按编号选择联系人,逐字段修改(回车跳过表示不改);
> 5. 删除:按编号 + 二次确认;
> 6. 分组统计:各分组人数(字典计数器!);
> 7. **持久化:退出时自动保存到 contacts.json;启动时自动加载**——数据必须活过程序重启;
> 8. 所有输入清洗,所有编号校验,任何乱输入不崩溃。
>
> **技术约束(考核点)**:
> - 三层架构:工具层纯函数 / 功能层 / main() 入口;
> - 字典驱动菜单(注册表模式);
> - 每个函数必须有 docstring 与类型注解;
> - 持久化使用 json 模块(文件读写用本文档提供的"简化模板",Day 11 转正)。
>
> **验收标准**:功能逐项演示通过;重启程序数据还在;乱输入轰炸不崩;代码规范逐条落实。

## 2.2 关于文件读写:今天的"简化模板"

文件操作是 Day 11 的正课,今天先发两个"封装好的模板函数",**照抄使用,Day 11 揭晓每行原理**:

```python
import json


def save_json(data, filename: str) -> None:
    """把 Python 对象保存为 JSON 文件。(模板函数,Day 11 讲原理)"""
    with open(filename, "w", encoding="utf-8") as f:      # 打开文件准备写(w)
        json.dump(data, f, ensure_ascii=False, indent=2)  # dump 不带 s:直写文件


def load_json(filename: str, default=None):
    """从 JSON 文件加载 Python 对象;文件不存在返回 default。(模板函数)"""
    try:                                                   # 尝试打开(Day 10 讲 try)
        with open(filename, "r", encoding="utf-8") as f:   # 打开文件准备读(r)
            return json.load(f)                            # load 不带 s:直读文件
    except FileNotFoundError:                              # 第一次运行没有文件:正常
        return default if default is not None else []
```

注意看:**dump/load(不带 s)对文件,dumps/loads(带 s)对字符串**——Day 05 记忆图的另一半今天启用了。`encoding="utf-8"` 保证中文不乱码,`ensure_ascii=False` 保证存进文件的中文人类可读。

## 2.3 架构设计图

```
┌────────────────────────────────────────────────────────┐
│ 入口层  main()                                          │
│   启动:contacts = load_json("contacts.json")   ◄─┐     │
│   主循环:字典驱动菜单 → 调功能函数                │     │
│   退出:save_json(contacts, "contacts.json")  ────┘     │
│         (数据的生命周期:启动加载 → 内存操作 → 退出落盘) │
├────────────────────────────────────────────────────────┤
│ 功能层  list_contacts / add_contact / search_contacts   │
│         edit_contact / delete_contact / group_stats     │
├────────────────────────────────────────────────────────┤
│ 工具层  is_valid_phone / is_valid_email / mask_phone    │
│         find_by_index / format_contact                  │
│         (全部纯函数,全部可 assert 测试)                  │
├────────────────────────────────────────────────────────┤
│ 数据层  contacts: list[dict]  ⇄  contacts.json 文件      │
└────────────────────────────────────────────────────────┘
```

**架构点评**:与 Day 06 工具箱相比,新增了最底下的"数据层双形态"——内存里是字典列表(操作快),磁盘上是 JSON 文件(能存活)。“启动加载、退出落盘”是最简单的持久化策略;它的缺陷(中途崩溃丢数据)在作业思考题里讨论,数据库方案 Day 24 见。

## 2.4 参考实现(核心节选,完整代码见 code/contacts_app.py)

```python
# ──────────────── 工具层:纯函数 ────────────────

def is_valid_phone(phone: str) -> bool:
    """校验手机号:11 位纯数字。"""
    return phone.isdigit() and len(phone) == 11


def is_valid_email(email: str) -> bool:
    """校验邮箱:含且只含一个 @,且不在开头。(Day 03 作业规则的函数化)"""
    return email.count("@") == 1 and not email.startswith("@")


def mask_phone(phone: str) -> str:
    """手机号脱敏。第一周写的最后一遍——从此永远 import 复用。"""
    return phone[:3] + "****" + phone[-4:]


def format_contact(c: dict) -> str:
    """单个联系人的展示行。"""
    return f"{c['name']:<8}{mask_phone(c['phone']):<15}[{c.get('group', '未分组')}]"


# ──────────────── 功能层(节选两个代表) ────────────────

def add_contact(contacts: list) -> None:
    """添加联系人:全字段校验。"""
    name = input("姓名:").strip()
    if not name:
        print("姓名不能为空!")
        return
    if any(c["name"] == name for c in contacts):       # any + 生成器:查重
        print(f"「{name}」已存在!")
        return

    while True:                                        # 校验循环:手机号
        phone = input("手机号(11位):").strip()
        if is_valid_phone(phone):
            break
        print("手机号必须是 11 位数字!")

    while True:                                        # 校验循环:邮箱
        email = input("邮箱:").strip()
        if is_valid_email(email):
            break
        print("邮箱格式不对!")

    group = input("分组(回车=未分组):").strip() or "未分组"    # or 兜底

    contacts.append({"name": name, "phone": phone, "email": email, "group": group})
    print(f"已添加:{name}")


def group_stats(contacts: list) -> None:
    """分组统计:字典计数器的实战。"""
    if not contacts:
        print("通讯录为空")
        return
    counter: dict = {}
    for c in contacts:
        g = c.get("group", "未分组")
        counter[g] = counter.get(g, 0) + 1             # 焊死的三行,今天变现
    for group, num in sorted(counter.items(), key=lambda kv: -kv[1]):   # 按人数降序
        print(f"  {group}:{num} 人")


# ──────────────── 入口层 ────────────────

DATA_FILE = "contacts.json"


def main() -> None:
    """入口:加载 → 主循环 → 落盘。"""
    contacts = load_json(DATA_FILE, default=[])        # 启动:从磁盘唤醒数据
    print(f"已加载 {len(contacts)} 位联系人")

    menu = {
        "1": ("查看全部", lambda: list_contacts(contacts)),
        "2": ("添加", lambda: add_contact(contacts)),
        "3": ("搜索", lambda: search_contacts(contacts)),
        "4": ("修改", lambda: edit_contact(contacts)),
        "5": ("删除", lambda: delete_contact(contacts)),
        "6": ("分组统计", lambda: group_stats(contacts)),
    }

    while True:
        print("\n" + "=" * 32)
        for key, (name, _) in menu.items():
            print(f"  {key}. {name}")
        print("  0. 保存并退出")
        choice = input("请选择:").strip()

        if choice == "0":
            save_json(contacts, DATA_FILE)             # 退出:落盘
            print(f"已保存 {len(contacts)} 位联系人,再见!")
            break
        if choice not in menu:
            print(f"没有选项 [{choice}]")
            continue
        menu[choice][1]()                              # 取函数并执行(紧凑写法)


if __name__ == "__main__":
    main()
```

**验收仪式(每人必做)**:添加两个联系人 → 选 0 退出 → **重新运行程序** → 看到"已加载 2 位联系人"——这一刻,你的程序第一次拥有了"记忆"。打开生成的 contacts.json 亲眼看看你的数据长什么样(它就是 Day 05 学的 JSON,indent=2 排版,中文可读)。

## 2.5 上机考核评分表(讲师用,也是你的自查表)

| 检查项 | 分值 | 自查 |
|--------|------|------|
| 七大功能全部可用 | 30 | □ |
| 重启后数据还在(持久化) | 15 | □ |
| 乱输入轰炸不崩(空值/非数字/越界/重复) | 15 | □ |
| 三层架构清晰,工具层可独立测试 | 15 | □ |
| 字典驱动菜单 | 10 | □ |
| docstring + 类型注解齐全 | 10 | □ |
| Git 提交记录完整(至少 3 个有意义的 commit) | 5 | □ |

---

# 【周测试卷与答案】笔试部分(50 分,30 分钟)

## 试卷

**一、选择题(每题 3 分,共 24 分)**

1. `print(type(input()))` 无论用户输入什么,输出都是?
   A. 取决于输入 B. `<class 'str'>` C. `<class 'int'>` D. 报错

2. `"LangChain"[-5:]` 的值是?
   A. Chain B. hain C. LangC D. 报错

3. 下列不会引发错误的是?
   A. `int("3.5")` B. `[1,2][5]` C. `{"a":1}["b"]` D. `"abc"[1:99]`

4. `nums = [3,1,2]; a = nums.sort(); b = sorted(nums)`,此时 a、b 分别是?
   A. [1,2,3] 和 [1,2,3] B. None 和 [1,2,3] C. [1,2,3] 和 None D. None 和 [3,1,2]

5. JSON 中合法的写法是?
   A. `{'a': 1}` B. `{"a": True}` C. `{"a": null}` D. `{"a": 1,}`

6. `d = {}; d["x"] = d.get("x", 0) + 1; d["x"] = d.get("x", 0) + 1; print(d["x"])` 输出?
   A. 0 B. 1 C. 2 D. KeyError

7. `def f(a, b=5): return a * b`,下列调用报错的是?
   A. `f(2)` B. `f(2, 3)` C. `f(b=3, a=2)` D. `f(b=3)`

8. 想让函数修改调用方的列表,正确的理解是?
   A. 必须 return 新列表,原列表永远改不了
   B. 传入列表后函数内 append 即可影响原列表(传的是标签)
   C. 必须用 global
   D. 列表不能作为参数

**二、读程序写结果(每题 4 分,共 16 分)**

9.
```python
s = "  AI, Python, RAG  "
parts = [p.strip() for p in s.strip().split(",")]
print(parts)
print("-".join(parts))
```

10.
```python
data = '{"items": [{"name": "a", "n": 2}, {"name": "b", "n": 5}]}'
import json
obj = json.loads(data)
total = sum(item["n"] for item in obj["items"])
print(total, obj["items"][1]["name"])
```

11.
```python
def f(lst):
    lst.append(len(lst))
    return lst

x = [7]
y = f(x)
print(x, y, x is y)
```

12.
```python
count = 0
for i in range(10):
    if i % 4 == 0:
        continue
    if i == 7:
        break
    count += 1
print(count)
```

**三、编程题(10 分)**

13. 写一个函数 `word_freq(text: str) -> dict`:统计一段英文文本里每个单词的出现次数(按空白拆分,统一小写,忽略两端的标点 `.,!?`)。要求 docstring + 类型注解,并写两条 assert 验证。

## 参考答案与评分说明

**1. B。** input 永远返回 str——第一周说了七遍,周测必考。
**2. A。** 负索引切片取最后 5 个字符:Chain。
**3. D。** 切片越界不报错(尽力而为);A ValueError、B IndexError、C KeyError——三大错误类型对号入座。
**4. B。** sort 原地干活返回 None(但 nums 已变成 [1,2,3]),所以 b = sorted([1,2,3]) = [1,2,3]。
**5. C。** null 合法;A 单引号、B 大写 True、D 尾逗号均非法。
**6. C。** 字典计数器执行两遍:0+1=1,1+1=2。
**7. D。** a 没有默认值,必须以位置或关键字方式提供;`f(b=3)` 缺 a → TypeError。
**8. B。** 参数传标签:函数内通过标签修改可变对象,外面可见。A 说法对不可变类型(字符串)成立,对列表不成立;C 是对 global 的滥用误解。

**9.**
```
['AI', 'Python', 'RAG']
AI-Python-RAG
```
清洗组合拳:外层 strip → split(",") → 每段再 strip(推导式加工)。

**10.**
```
7 b
```
JSON 解析 → 字典列表遍历求和(生成器版 sum)→ 嵌套取值。这是"第一名句"的姊妹考法。

**11.**
```
[7, 1] [7, 1] True
```
传标签:x 和 y 是同一个列表(is 为 True);append(len(lst)) 时 len 是 1。

**12.** `5`。i=0 continue;1,2,3 计数(3);4 continue;5,6 计数(5);7 break。逐步走查,凭感觉必错。

**13. 参考实现:**

```python
def word_freq(text: str) -> dict:
    """统计英文文本词频:按空白拆分、统一小写、剥两端标点。"""
    counter: dict = {}
    for raw_word in text.split():                 # 按任意空白拆
        word = raw_word.strip(".,!?").lower()     # 剥标点 + 小写(链式)
        if not word:                              # 纯标点剥完剩空串:跳过
            continue
        counter[word] = counter.get(word, 0) + 1  # 字典计数器
    return counter


assert word_freq("Go go GO!") == {"go": 3}
assert word_freq("Hi, hi. Bye!") == {"hi": 2, "bye": 1}
```

评分:拆分 2 分、清洗 3 分(strip 标点 + lower)、计数器 3 分、assert 2 分。用了 `strip(".,!?")` 指定字符剥离(Day 02 的进阶用法)满分;只处理了 lower 没剥标点扣 2。

**分数解读**:≥40 优秀,继续保持;30-39 合格,把错题对应的"课堂笔记"节重看;<30 需要今晚加练——重做错题对应天的编程作业(不看答案),明早找讲师面批。

---

# 【周测试卷与答案】上机部分(50 分,90 分钟)

> 上机部分与综合项目二选一计分:基础扎实的同学直接做综合项目(通讯录,50 分制按评分表);感觉吃力的同学先做下面三道独立上机题(20+15+15),再尽力完成项目。三道题都提供逐行讲解的参考答案——先自己写满 30 分钟再看。

## 上机题 1(20 分):订单流水分析

内置数据(照抄):

```python
orders = [
    {"id": "A001", "user": "张三", "amount": 259.0, "status": "paid"},
    {"id": "A002", "user": "李四", "amount": 88.5, "status": "cancelled"},
    {"id": "A003", "user": "张三", "amount": 132.0, "status": "paid"},
    {"id": "A004", "user": "王五", "amount": 46.0, "status": "paid"},
    {"id": "A005", "user": "李四", "amount": 310.0, "status": "refunded"},
]
```

要求:① 函数 `paid_total(orders) -> float`:已支付订单总金额;② 函数 `user_spending(orders) -> dict`:每个用户的已支付消费额(字典累加器——计数器的金额版);③ 函数 `top_spender(orders) -> str`:消费最高的用户名(max + key);④ 全部配 assert。

**参考答案:**

```python
def paid_total(orders: list) -> float:
    """已支付订单总金额。生成器版 sum + 条件过滤。"""
    return sum(o["amount"] for o in orders if o["status"] == "paid")


def user_spending(orders: list) -> dict:
    """每用户已支付消费额:字典累加器(计数器的金额版)。"""
    spending: dict = {}
    for o in orders:
        if o["status"] != "paid":          # 提前跳过:只统计已支付
            continue
        spending[o["user"]] = spending.get(o["user"], 0) + o["amount"]
    return spending


def top_spender(orders: list) -> str:
    """消费最高的用户名。max 按字典的值比较,返回对应的键。"""
    spending = user_spending(orders)
    return max(spending, key=spending.get)     # 遍历键,按 spending[键] 比大小
    # spending.get 不带括号:把方法本身当 key 函数用——函数是一等公民


assert paid_total(orders) == 437.0             # 259 + 132 + 46
assert user_spending(orders) == {"张三": 391.0, "王五": 46.0}
assert top_spender(orders) == "张三"
```

评分:①5 分(过滤+求和)②8 分(累加器 + 跳过非 paid)③4 分(max key 用法)④3 分。`max(d, key=d.get)` 是"找字典里值最大的键"的标准一行,值得单独记住。

## 上机题 2(15 分):指令解析器

Day 14 的 AI 助手要支持 `/save my_chat.json` 这种"指令 + 参数"格式。写函数 `parse_command(text: str) -> tuple`:输入用户原始输入,返回 `(指令, 参数)` 元组——`"/save abc.json"` → `("/save", "abc.json")`;`"/clear"` → `("/clear", "")`;不以 / 开头 → `("", 原文本清洗后)`。全部清洗两端空白。配 assert。

**参考答案:**

```python
def parse_command(text: str) -> tuple:
    """解析用户输入:返回 (指令, 参数) 或 ("", 正文)。

    split(maxsplit=1):最多切一刀——参数里允许有空格
    (比如 /save my chat.json),这是 maxsplit 的经典用途。
    """
    text = text.strip()
    if not text.startswith("/"):
        return ("", text)                      # 非指令:原文本作为正文返回
    parts = text.split(maxsplit=1)             # "/save a.json" → ["/save", "a.json"]
    command = parts[0]
    arg = parts[1].strip() if len(parts) > 1 else ""    # 没参数就给空串
    return (command, arg)


assert parse_command("/save abc.json") == ("/save", "abc.json")
assert parse_command("  /clear  ") == ("/clear", "")
assert parse_command("今天天气如何") == ("", "今天天气如何")
assert parse_command("/save my chat.json") == ("/save", "my chat.json")
```

评分:startswith 判断 4 分、maxsplit 切分 5 分(用普通 split 后 join 回参数也给分)、无参数容错 4 分、assert 2 分。这个函数会在 Day 14 项目一里**原样上岗**——周测题就是项目零件,本课程一贯如此。

## 上机题 3(15 分):对话历史的窗口截断

写函数 `trim_history(messages: list, max_rounds: int = 3) -> list`:保留 system 消息(如果第一条是 system)+ 最近 max_rounds 轮对话(一轮 = 一条 user + 一条 assistant),返回**新列表**(不修改原列表)。这是 Day 27 窗口记忆的手工版。

**参考答案:**

```python
def trim_history(messages: list, max_rounds: int = 3) -> list:
    """保留 system + 最近 N 轮对话,返回新列表。

    思路:①摘出 system;②剩余消息取最后 2*N 条(一轮两条);③拼回。
    切片天然"尽力而为":不足 N 轮时全保留,不用额外判断。
    """
    if messages and messages[0]["role"] == "system":
        system_part = messages[:1]             # 切片而不是 [0]:保持列表形态好拼接
        chat_part = messages[1:]
    else:
        system_part = []
        chat_part = messages

    recent = chat_part[-max_rounds * 2:]       # 最后 2N 条(切片越界安全)
    return system_part + recent                # 列表相加 = 拼接,产生新列表


msgs = [{"role": "system", "content": "你是助教"}]
for i in range(5):                             # 造 5 轮对话
    msgs.append({"role": "user", "content": f"问{i}"})
    msgs.append({"role": "assistant", "content": f"答{i}"})

trimmed = trim_history(msgs, max_rounds=3)
assert len(trimmed) == 7                       # 1 system + 3 轮 × 2
assert trimmed[0]["role"] == "system"
assert trimmed[1]["content"] == "问2"          # 最早保留的是第 2 轮(0 起)
assert len(msgs) == 11                         # 原列表未被修改!
```

评分:system 摘取 5 分、负切片取最近 2N 条 5 分、返回新列表不动原件 3 分、assert 2 分。**"返回新列表还是原地修改"是有意识的设计决策**:本题要求新列表,因为截断是"发送 API 前的临时视图",正史(完整历史)要留着存盘——Day 27 你会看到 LangChain 也是这么设计的。

---

# 【课堂笔记】Day 07 速查表(第一周浓缩版)

**因果链**:输入输出(D1)→ 清洗提问(D2)→ 选路重复(D3)→ 容器(D4)→ 命名容器+JSON(D5)→ 组织(D6)→ 合体(D7)

**三段焊死的代码**:字典计数器 | read_int_in_range | messages 一轮对话

**持久化最小方案**(今天新增):
- 启动 `contacts = load_json(file, default=[])`,退出 `save_json(contacts, file)`
- dump/load 对**文件**,dumps/loads 对**字符串**
- 文件必带 `encoding="utf-8"`;JSON 必带 `ensure_ascii=False`

**三大错误类型对号**:ValueError(值不合法:int("abc"))| IndexError(位置越界)| KeyError(键不存在)

**架构四层**:入口(调度+数据生命周期)/ 功能(交互)/ 工具(纯函数)/ 数据(内存 ⇄ 磁盘)

---

# 【附录】课堂答疑实录(晚自习整理)

**问 1:周测考砸了,是不是说明我不适合编程?**

答:第一周周测的区分度反映的是"熟练度"不是"天赋"。写代码是肌肉记忆,你和高分同学的差距通常就是"敲过的遍数"。诊断方法:把错题归类——是"概念没懂"(比如说不清 sort 和 sorted 的区别)还是"手生"(懂但写不出来)?前者重看课件对应节,后者只有一个药方:把那天的实操项目**不看答案**重写一遍。另外记住课程设计:Day 14、21、31…每周都有验收,一次周测只是七分之一。

**问 2:通讯录退出时才保存,中途崩溃(或者我直接点了终端的叉)数据就丢了,怎么办?**

答:你发现了"启动加载、退出落盘"策略的致命弱点,这正是作业思考题。渐进的改良方案:① **每次修改后立即保存**(add/edit/delete 完就 save_json)——代价是频繁写盘,小数据无所谓,今天就可以实现;② **定时保存 + 退出保存**(编辑器的自动保存);③ **写前日志**(先记"我要做什么"再做,崩溃后重放日志恢复)——数据库就是这么干的,Day 24 的 SQLite 每次 commit 都是持久的。今天的作业里就有"改成即时保存"的题。

**问 3:为什么 contacts.json 用记事本打开,中文是正常的,而我同事的项目里 JSON 全是 \u4e2d\u6587?**

答:因为我们的模板函数带了 `ensure_ascii=False`。默认(True)时,json 模块把所有非 ASCII 字符转义成 \uXXXX——数据没坏(loads 回来还是中文),但人没法读。你同事的项目八成是忘了这个参数。顺带一提 `encoding="utf-8"` 是另一层保险:它管的是"文件以什么编码写入磁盘",Windows 默认是 GBK,不指定的话跨系统就乱码。两个参数管两层,Day 11 讲编码时会画图讲透。

**问 4:菜单里的 lambda: add_contact(contacts) 能不能不用 lambda?**

答:能,两个替代:① 让功能函数不接参数、直接用全局 contacts——但这违反"参数进 return 出"的原则,不推荐;② 明天学的**类**:把 contacts 变成对象的属性 `self.contacts`,功能函数变成方法,菜单直接存方法 `self.add_contact`——这是最优雅的解,也是明天 OOP 课的开场案例。所以今天的 lambda 是"类还没学之前的最佳方案",忍一天。

**问 5:any(c["name"] == name for c in contacts) 这个写法没见过?**

答:它是"生成器表达式 + any"的组合:`any(...)` 问"有没有任何一个为 True",生成器逐个产出判断结果,any 遇到第一个 True 就立刻停(不用遍历完,高效)。等价的啰嗦版:写个 for 循环带标志变量(Day 03 的手法)。同族的还有 `all(...)`(是否全部为 True)。这两个函数配合推导式语法,是"批量判断"的标准姿势,本周作业里已经出现过两次,下周转正为常规武器。

**问 6:第一周结束了,我该怎么复习才不会像上周学的都忘了?**

答:三个动作,按性价比排序:① **本周项目重写**(最有效):挑通讯录或待办管理器,下周三前不看代码重写一遍——能默写出来的知识才是你的;② **错题驱动**:周测错题对应的知识点,把那天作业里同类的题重做;③ **教是最好的学**:向同学(或者对着墙)讲一遍"从字典到 JSON 到 API 报文"这条线,讲不顺的地方就是没懂的地方。不推荐的复习方式:重看课件划重点——"看懂"和"会写"隔着一条太平洋,时间要花在敲代码上。

---

# 【明日预告】Day 08:面向对象编程(上)

第二周开张。今天答疑里的钩子就是明天的开场:通讯录的 `contacts` 数据和操作它的六个函数,像"一家人却分居各处"——**类(class)**把它们装进同一个屋檐:数据成为**属性**,函数成为**方法**,`self` 就是"这个对象自己"。明天上午:类与对象、`__init__` 构造方法、属性与方法;下午:实例方法/类方法/静态方法的区别;实操:定义 `ChatMessage` 类(role、content 属性)——把 Day 05 的消息字典升级成消息对象,为 Day 09 的 `BaseModel → OpenAIModel / QwenModel` 继承体系打地基。OOP 是很多同学的第一道"抽象坎",但我们有秘密武器:你已经用了一周的对象了(字符串的 .strip()、列表的 .append(),全是"对象.方法"),明天只是揭晓"你怎么自己造这种东西"。

**睡前自检清单**:
- [ ] 周测订正完成,错题知识点定位到具体某天的课件章节
- [ ] 通讯录项目按评分表自查,七大功能 + 持久化全过
- [ ] contacts.json 打开亲眼看过
- [ ] 作业完成并 push,绿格子连续第 7 天(满一周!)
