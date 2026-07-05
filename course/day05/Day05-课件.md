# Day 05:字典与 JSON —— 大模型 API 的母语(第一周最重要的一天)

---

# 【旁白解读】昨天、今天、明天

先把昨天留下的三个"钩子"摆上桌:

1. 待办管理器的扎心问题:待办要带"内容 + 时间 + 优先级"三个字段,嵌套列表 `["写作业", "2026-07-08", "高"]` 能存但没法看——谁记得 2 号位是什么?
2. 购物车作业的别扭:查"苹果的单价"要**遍历**整个价格列表,一万种商品就要比对一万次;
3. Day 14 的预告代码里那个大括号:`{"role": "user", "content": user_input}`——它到底是什么?

**三个钩子,一个答案:字典(dict)。** 按名字存、按名字取,不用记位置,不用遍历。它是 Python 四大容器的最后一块,也是最重要的一块。

但今天真正的主角还不止字典。**今天下午要学的 JSON,是整个第一周分量最重的知识点**,课表上白纸黑字写着"与 API 交互的基石,重点!"。原因一句话:**你未来和大模型的每一次通信,发出去的和收回来的,全都是 JSON。** Day 12 你首次调用 DeepSeek API 时,请求体是 JSON、响应是 JSON;Day 19 Function Calling 的工具定义是 JSON;Day 23 FastAPI 的接口进出全是 JSON;Day 52 微调数据集是 JSON 格式的文件。**JSON 学不透,后面 65 天寸步难行;JSON 学透了,Day 12 那天你会觉得"调用大模型 API 也不过如此"。**

今天的路线:上午吃透字典(增删改查、遍历、嵌套、和列表的配合);下午先讲 JSON 格式本身,再学 json 模块的四大函数(loads/dumps/load/dump),最后实操:**解析一份和真实 DeepSeek API 返回一模一样的 JSON,从里面提取出模型的回答**——这是 Day 12 的完整彩排。

昨天的账也今天还:待办管理器"程序一关数据就没"的持久化问题,今天你会看到答案的前半段(列表转 JSON 字符串),Day 11 补后半段(写入文件),Day 07 周测项目就要求完整实现。

---

# 上午 · 第一节(9:00 - 10:30):字典的增删改查

## 1.1 从"查单价"的痛点进入

昨天购物车作业的痛点代码:

```python
# 昨天:元组列表存价格,查一个价格要遍历
prices = [("苹果", 5), ("牛奶", 12), ("面包", 8)]
for name, price in prices:          # 一万种商品就要比对一万次
    if name == "苹果":
        print(price)
```

字典版:

```python
# 今天:字典存价格,按名字直接取
prices = {"苹果": 5, "牛奶": 12, "面包": 8}
print(prices["苹果"])               # 5 —— 一步到位,不管商品有多少种
```

字典的构造:**大括号包裹,"键: 值"成对,逗号分隔**。

```
prices = { "苹果": 5,  "牛奶": 12,  "面包": 8 }
           └─┬─┘ └┬┘
            键     值
          (key)  (value)     一对"键: 值"叫一个"键值对"(key-value pair)
```

心智模型:**字典 = 带标签的抽屉柜**。列表的抽屉按 0、1、2 编号(位置);字典的抽屉贴着名字标签("苹果"、"牛奶")。列表按位置取,字典按名字取。

三条基本法则:

1. **键必须唯一**:同名键后写的覆盖先写的(一个抽屉一个标签);
2. **键必须是不可变类型**:字符串(99% 的场景)、数字、元组可以;列表不行(`TypeError: unhashable type: 'list'`)——Day 02 "字符串为什么不可变"和昨天"元组存在的意义",两个伏笔在此汇合;
3. **值随便**:任何类型,包括列表、另一个字典(嵌套,第二节的主角)。

## 1.2 增、改:同一个动作

```python
user = {"name": "张三", "age": 28}

# 键不存在 → 增
user["city"] = "上海"
print(user)                 # {'name': '张三', 'age': 28, 'city': '上海'}

# 键已存在 → 改(覆盖)
user["age"] = 29
print(user)                 # {'name': '张三', 'age': 29, 'city': '上海'}

# 从空字典开始逐步构建——今天下午组装 API 请求体就是这个套路
request = {}
request["model"] = "deepseek-chat"
request["temperature"] = 0.7
```

## 1.3 查:方括号 vs get —— 今天第一个重点抉择

```python
user = {"name": "张三", "age": 29}

# ── 方式一:方括号 —— 键不存在直接报错 ──
print(user["name"])         # 张三
# print(user["email"])      # KeyError: 'email' —— 程序当场崩溃

# ── 方式二:get —— 键不存在返回 None(或你指定的默认值),不崩 ──
print(user.get("email"))               # None
print(user.get("email", "未填写"))      # 未填写 —— 第二个参数是默认值
print(user.get("name", "未填写"))       # 张三 —— 键存在时默认值不生效
```

**选择心法(工程师的防御性思维):**

- 键**理应存在**、不存在就是严重 bug → 用方括号,让它响亮地崩(崩溃是最诚实的报警);
- 键**可能没有**、没有也正常(用户没填邮箱、API 响应里可选字段)→ 用 get + 默认值。

这个抉择在 Day 12 有真实的用武之地:解析 API 响应时,`data["choices"]` 用方括号(没有 choices 说明调用失败了,该崩该报);`data.get("usage", {})` 用 get(个别接口不返回用量统计,没有就算了)。**对必要字段严格,对可选字段宽容。**

## 1.4 删与其他操作

```python
user = {"name": "张三", "age": 29, "city": "上海", "temp": "草稿"}

# pop(键):删并递给你(和列表的 pop 精神一致)
removed = user.pop("temp")
print(removed)              # 草稿

# pop 不存在的键会 KeyError;给默认值就不崩:
user.pop("nothing", None)   # 安静地什么都不发生

# del 语句:删,不递给你
del user["city"]

# in:检查"键"在不在(注意:检查的是键,不是值!)
print("name" in user)       # True
print("张三" in user)        # False —— "张三"是值不是键
print("张三" in user.values())    # True —— 查值要显式说明

# len:键值对个数
print(len(user))            # 2
```

## 1.5 遍历字典的三种姿势

```python
model_prices = {"deepseek-chat": 1.0, "gpt-4o": 18.0, "qwen-plus": 4.0}

# 姿势一:直接 for → 遍历"键"(最简)
for name in model_prices:
    print(name)

# 姿势二:.items() → 键值一起来(最常用!)
for name, price in model_prices.items():      # 每轮拆包出一对键值——昨天拆包的复利
    print(f"{name}:{price} 元/百万token")

# 姿势三:.values() / .keys() → 只要值 / 只要键
total = sum(model_prices.values())             # 所有值求和
print(f"均价:{total / len(model_prices):.1f}")

# 昨天答疑承诺的"保序去重"一行流,现在能看懂了:
emails = ["a@x.com", "b@y.com", "a@x.com"]
unique = list(dict.fromkeys(emails))           # fromkeys 把列表元素变成字典的键:
print(unique)                                  # 键不重复 + 保插入顺序,去重且保序
```

**顺序问题的正式回答**(昨天速查表留白的那格):Python 3.7 起,**字典保持插入顺序**——先放进去的键,遍历时先出来。所以四大容器速查表可以补全了:dict 是"按插入序、可变、键不重复"。但请注意语义:字典的本职是"按名字取",顺序只是附赠品;真正以顺序为本职的还是列表。

## 1.6 哈希:字典和集合为什么查得快(昨天答疑的正式版)

昨天说集合查"在不在"像查字典(新华字典),今天给出正式原理,只讲思想不讲实现:

```
列表查找:  "苹果" → 0号比一下?不是 → 1号?不是 → 2号?…… 挨个比(线性查找)
字典查找:  "苹果" → 哈希函数算一下 → "第 7 号抽屉" → 直接开抽屉(一步到位)
```

**哈希函数**:把任意键"搅拌"成一个数字(哈希值),这个数字决定它存放在哪个"抽屉"。查找时对键再算一次哈希,直接去对应抽屉拿。数据量 10 条还是 10 万条,都是"算一次、拿一次"。

这也解释了两个悬案:① **为什么键必须不可变**——如果键是列表,存进去之后内容一变,哈希值就变了,但它还躺在按旧哈希值分配的抽屉里,从此再也找不到它(所以 Python 干脆禁止可变类型当键,报错 unhashable);② **为什么集合无序**——元素按哈希值安家,不按你放入的顺序。

哈希思想的远景:Day 29 向量数据库的索引、Git 的每个提交号(那串十六进制就是哈希值)、区块链——都是它。今天种下概念即可。

---

# 上午 · 第二节(10:40 - 12:00):嵌套 —— 字典与列表的乐高组合

## 2.1 字典里装字典、装列表

真实世界的数据是有层次的。字典的值可以是任何东西,于是可以搭出任意深的结构:

```python
# 一个学员的完整档案:字典嵌套字典、嵌套列表
student = {
    "name": "张三",
    "age": 28,
    "contact": {                        # 值是另一个字典:联系方式有自己的内部结构
        "email": "zhang@x.com",
        "phone": "13812345678"
    },
    "skills": ["python", "sql"],        # 值是列表:技能有多项
    "scores": {"day01": 92, "day02": 85}
}

# 逐层取值:一层一个方括号,像剥洋葱
print(student["contact"]["email"])       # zhang@x.com
print(student["skills"][0])              # python —— 字典套列表:先按名字后按位置
print(student["scores"]["day02"])        # 85

# 逐层修改
student["contact"]["phone"] = "13900000000"
student["skills"].append("langchain")    # 取出列表,直接 append(列表可变)
```

**读嵌套结构的口诀:从外往里,一层一层问自己"这一层是字典还是列表?"**——字典用 `["名字"]`,列表用 `[数字]`。这个口诀今天下午解析 API 响应时是保命符。

## 2.2 字典列表:最重要的复合结构(没有之一)

**"列表里装着一批字典"**——这是数据世界的通用形态:数据库查询结果、Excel 表格、API 返回的批量数据,长的全是这个样子:

```python
# 昨天待办管理器的终极形态:每个待办是一个字典,全部待办是字典的列表
todos = [
    {"task": "复习字典", "priority": "高", "done": False},
    {"task": "写作业", "priority": "中", "done": False},
    {"task": "刷 LeetCode", "priority": "低", "done": True},
]

# 遍历:每轮拿到一个字典,按名字取字段——再也不用记"2 号位是优先级"
for todo in todos:
    status = "✓" if todo["done"] else "□"
    print(f"{status} [{todo['priority']}] {todo['task']}")
    # 注意引号嵌套:f-string 外层用了双引号,里层键名就用单引号,避免打架

# 过滤:未完成的高优先级事项(昨天的推导式 + 今天的字典)
urgent = [t for t in todos if t["priority"] == "高" and not t["done"]]

# 排序:按优先级排(sorted 的 key 参数昨天预告的完整威力)
order = {"高": 0, "中": 1, "低": 2}                    # 用字典定义"排序权重"
by_priority = sorted(todos, key=lambda t: order[t["priority"]])
# lambda 是"临时小函数",Day 06 正式学;今天先照抄,知道它是"告诉 sorted 按什么排"
```

**现在,兑现 Day 14 预告代码的全部谜底。** 大模型 API 的对话历史 `messages`,就是一个字典列表:

```python
# 这就是你 7 天后要发给 DeepSeek 的真实数据结构(一字不差):
messages = [
    {"role": "system", "content": "你是一个乐于助人的AI助手"},
    {"role": "user", "content": "你好,请介绍一下自己"},
    {"role": "assistant", "content": "你好!我是AI助手……"},
    {"role": "user", "content": "北京今天天气怎么样?"}
]
# 每条消息一个字典:role 说明是谁说的(system 设定/user 用户/assistant 模型),
# content 是说话内容。多轮对话 = 不断 append 新字典(昨天练的动作)。
# Day 15 会专门讲三种 role 的区别,今天先把结构焊进脑子。
```

到这一刻,Day 01 的 f-string、Day 03 的主循环、Day 04 的 append、今天的字典列表——四天的知识拼图合上了:**AI 对话应用的数据层,你已经全部学完了。** 缺的只剩"怎么发出去"(HTTP,Day 12)。

## 2.3 字典驱动:菜单系统欠账的部分偿还

Day 03 菜单系统的毛病之三"菜单文本写死,加功能要改两处",现在可以用字典优雅化解一半:

```python
# 字典驱动的菜单:选项号 → 功能名,数据和展示自动同步
MENU = {
    "1": "文本清洗",
    "2": "手机号脱敏",
    "3": "猜数字游戏",
    "0": "退出",
}

# 菜单打印:遍历字典自动生成,加功能只改 MENU 一处
for key, name in MENU.items():
    print(f"  {key}. {name}")

choice = input("请选择:").strip()
if choice not in MENU:                    # 合法性检查也自动化了:in 查键
    print(f"没有选项 [{choice}]")
print(f"你选择了:{MENU.get(choice, '未知')}")
# 完全体(选项直接映射到"要执行的函数")需要 Day 06 的函数——函数也能当字典的值!
```

---

# 下午 · 第一节(14:00 - 15:30):JSON —— 与 API 交互的基石(重点!)

## 3.1 JSON 是什么,为什么非学不可

先看问题。你的 Python 程序里有个字典,想把它:发送给另一台服务器(调 API)、保存到文件(持久化)、给 JavaScript 写的网页用(前端)。麻烦来了:**Python 的字典是内存里的活物,只有 Python 认识**。网络上传输的只能是文本(字节),别的语言也不认识 Python 的内部格式。

所以需要一种**所有语言都认识的、纯文本的数据格式**作为通用语。这就是 **JSON(JavaScript Object Notation)**——名字里带 JavaScript 是历史原因,如今它是整个互联网的数据世界语:你手机里每个 App 和服务器的通信、大模型 API 的进进出出,几乎全是 JSON。

**一句话定义:JSON 是一种"长得极像 Python 字典/列表"的纯文本格式。** 看一眼:

```json
{
    "name": "张三",
    "age": 28,
    "is_vip": true,
    "balance": 3.5,
    "skills": ["python", "sql"],
    "email": null,
    "contact": {"phone": "13812345678"}
}
```

和 Python 字典几乎一样!但注意,**"几乎"里藏着全部考点**。差异对照表(今天必须背下来):

| 项目 | Python | JSON |
|------|--------|------|
| 键的引号 | 单双都行 | **只能双引号** |
| 字符串 | 单双都行 | **只能双引号** |
| 真/假 | `True` / `False`(大写开头) | `true` / `false`(全小写) |
| 空值 | `None` | `null` |
| 尾逗号 | 允许 `[1, 2, 3,]` | **禁止**,最后一个元素后不能有逗号 |
| 注释 | `#` | **不支持任何注释** |
| 数据类型 | 字典/列表/元组/集合…… | 只有 6 种:对象{}、数组[]、字符串、数字、布尔、null |

术语对照:JSON 管 `{}` 叫**对象(object)**,管 `[]` 叫**数组(array)**——和 Python 的字典、列表一一对应,只是叫法不同。以后看英文文档见到 object/array 不要慌。

**再强调一次身份问题,这是初学者最大的概念坑:JSON 是字符串(文本),不是字典。** 一份 JSON 数据在 Python 眼里就是个 `str`,你不能对它 `["name"]` 取值(那是对字典的操作)。要用,必须先"翻译"成字典——这个翻译动作就是下一节的 json 模块。

## 3.2 json 模块四大函数:两对镜像

```
                loads(load string)                    dumps(dump string)
   JSON 字符串 ──────────────────► Python 字典/列表 ──────────────────► JSON 字符串
   (网络收到的/文件读的)   解析           (程序里操作)        序列化       (要发出去的/要存的)

   带 s 的管字符串:loads / dumps       ← 今天的主角(网络通信用)
   不带 s 的管文件:load / dump         ← Day 11 文件课的主角(今天先见一面)
```

两个术语立刻记住,行业黑话天天说:**解析(parse)**= JSON 字符串 → 程序对象;**序列化(serialize)**= 程序对象 → JSON 字符串。

### loads:解析(收到的报文变成能操作的字典)

```python
import json                      # 标准库,无需安装

# 模拟从网络收到的 JSON(注意:它是个字符串!单引号包裹的整体)
raw = '{"name": "张三", "age": 28, "skills": ["python", "sql"], "is_vip": true}'

print(type(raw))                 # <class 'str'>  —— 现在还是文本,动不了里面的字段

data = json.loads(raw)           # 解析:字符串 → 字典
print(type(data))                # <class 'dict'> —— 活了!
print(data["name"])              # 张三 —— 上午的字典操作全部可用
print(data["skills"][0])         # python
print(data["is_vip"])            # True —— 注意:JSON 的 true 自动翻译成 Python 的 True
```

类型自动翻译表:object→dict、array→list、string→str、number→int/float、true/false→True/False、null→None。**双向都是自动的,你不用手工转。**

### dumps:序列化(字典打包成能发送/保存的文本)

```python
import json

request = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "user", "content": "你好"}
    ],
    "temperature": 0.7,
    "stream": False
}

# 基础序列化
text = json.dumps(request)
print(text)      # {"model": "deepseek-chat", ... "stream": false}
                 # 注意:False 变成了 false,Python 世界 → JSON 世界的自动翻译

# ── 两个必会参数 ──
# ensure_ascii=False:让中文原样输出(默认会变成 \u4f60\u597d 这种转义,不便阅读)
# indent=2:缩进美化(调试和存文件时用;网络传输时不加,省流量)
pretty = json.dumps(request, ensure_ascii=False, indent=2)
print(pretty)
# {
#   "model": "deepseek-chat",
#   "messages": [
#     {
#       "role": "user",
#       "content": "你好"     ← 中文可读,层次分明
#     }
#   ],
#   ...
# }
```

**`ensure_ascii=False` 请形成肌肉记忆**——处理中文数据时不加它,打印和存盘的 JSON 全是 `\uXXXX` 天书。这是中文开发者的日经坑。

### 一个来回:序列化 → 解析,数据无损往返

```python
import json

original = {"task": "学JSON", "tags": ["重点", "API"], "hours": 3.5, "done": None}
text = json.dumps(original, ensure_ascii=False)     # 打包成文本
restored = json.loads(text)                          # 再解开
print(restored == original)                          # True —— 完美还原
# 这个"打包→存起来/传出去→解开"的往返,就是持久化和网络通信的本质。
# 昨天待办管理器"程序一关数据就没"的解药,你已经拿到一半了:
# 退出前 dumps 存文件,启动时读文件 loads——文件读写 Day 11 补上,Day 07 周测先用简化版
```

### 解析失败:JSONDecodeError

```python
import json

bad = "{'name': '张三'}"          # 单引号——Python 字典合法,JSON 非法!
# json.loads(bad)                 # json.decoder.JSONDecodeError: Expecting property name
                                  # enclosed in double quotes ...
```

报错信息直译:"期望用双引号包裹的属性名"。**JSONDecodeError 的三大来源:单引号、尾逗号、大写的 True/False**——全在 3.1 的差异表里。真实工作中这个错误最常出现在:让大模型"输出 JSON"结果它输出得不标准(Day 18 的重要话题,有专门的治法)。

---

# 下午 · 第二节(15:40 - 17:30):实操——解析真实结构的大模型 API 响应

## 4.1 需求文档

> ### 需求文档:API 响应解析器 v1.0
>
> **需求编号**:REQ-D05-001
> **需求方**:「智言科技」AI 平台组
> **背景**:公司即将接入 DeepSeek API(下周上线,即 Day 12)。为了让新人提前熟悉数据格式,平台组提供了一份**与真实 API 返回一字不差**的样例报文,要求写一个解析器,为下周的正式接入做好准备。
>
> **功能需求**:
> 1. 解析样例 JSON 报文(字符串形式内置在代码里);
> 2. 提取并展示:模型回答正文、模型名、结束原因、三项 token 用量;
> 3. 按 DeepSeek 定价(输入 1 元/百万 token,输出 4 元/百万 token,虚拟价)计算本次调用成本;
> 4. 防御性处理:用量字段可能缺失(用 get);回答正文必须存在(用方括号,没有就该崩);
> 5. 反向练习:把一份多轮对话的 messages 结构序列化成规范 JSON 并美化打印。
>
> **验收标准**:输出信息完整准确;字段缺失的样例不崩溃;序列化结果可被 loads 无损还原。

## 4.2 先读懂敌人:真实 DeepSeek 响应的结构解剖

下面就是 DeepSeek(兼容 OpenAI 格式,行业事实标准)返回的真实结构。**先用眼睛解析,再用代码解析**:

```
{
  "id": "chatcmpl-abc123",                    ← 本次调用的唯一编号
  "object": "chat.completion",
  "created": 1751702400,                      ← 时间戳(Day 11 的 datetime 能翻译它)
  "model": "deepseek-chat",                   ← 实际使用的模型
  "choices": [                                ← ⚠️ 数组!模型的回答在这里面
    {
      "index": 0,
      "message": {                            ← 眼熟吗?就是 messages 里的那种字典!
        "role": "assistant",
        "content": "Python是一种简洁优雅的编程语言……"     ← ★ 我们最想要的东西
      },
      "finish_reason": "stop"                 ← 为什么停:stop 正常说完 / length 被截断
    }
  ],
  "usage": {                                  ← 计费依据:token 用量
    "prompt_tokens": 12,                      ← 输入(你发的)
    "completion_tokens": 25,                  ← 输出(它答的)
    "total_tokens": 37
  }
}
```

**取出回答正文的路径,用上午的剥洋葱口诀走一遍**:最外层是字典 → `["choices"]` 是列表 → `[0]` 取第一个元素(字典)→ `["message"]` 是字典 → `["content"]` 到手。连起来:

```python
content = data["choices"][0]["message"]["content"]
```

**这一行,是大模型应用开发的"第一名句"**,从 Day 12 到毕业设计你会写它上百遍。为什么 choices 是个列表?因为 API 支持一次要多个候选回答(参数 n>1,Day 16 讲),默认只有一个,所以永远先 `[0]`。

## 4.3 代码实现

```python
# =============================================
# API 响应解析器
# 需求编号:REQ-D05-001
# 这是 Day 12 首次真实调用 API 的完整彩排:
#   届时唯一的区别是——raw_response 不再是写死的字符串,
#   而是 requests 库从 api.deepseek.com 真实收回来的
# =============================================
import json

# ---- 样例报文:与真实 DeepSeek API 返回结构一字不差 ----
# 三引号包裹多行字符串(Day 01 的语法),内容是标准 JSON
raw_response = """
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "created": 1751702400,
  "model": "deepseek-chat",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Python是一种简洁优雅的编程语言,特别适合数据处理与AI应用开发。"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 12,
    "completion_tokens": 25,
    "total_tokens": 37
  }
}
"""

# ---- 定价常量(虚拟价,以官网为准;Day 01 成本作业的复利) ----
PRICE_INPUT_PER_M = 1.0      # 输入:元/百万 token
PRICE_OUTPUT_PER_M = 4.0     # 输出:元/百万 token

# ---- 第一步:解析(字符串 → 字典) ----
data = json.loads(raw_response)
print(type(data))            # <class 'dict'> 确认解析成功

# ---- 第二步:提取核心字段 ----
# 回答正文:必要字段,用方括号——没有它说明调用失败,崩溃即报警
content = data["choices"][0]["message"]["content"]

# 结束原因:同样重要。length 意味着回答被 max_tokens 截断了(Day 16 详解)
finish_reason = data["choices"][0]["finish_reason"]

# 模型名:可选展示信息,用 get 更稳
model = data.get("model", "未知模型")

# 用量:可选字段,双层防御——
# 外层 get 返回空字典兜底,内层再 get 数字 0 兜底,任何缺失都不崩
usage = data.get("usage", {})
tokens_in = usage.get("prompt_tokens", 0)
tokens_out = usage.get("completion_tokens", 0)
tokens_total = usage.get("total_tokens", 0)

# ---- 第三步:成本计算 ----
cost = (tokens_in / 1_000_000 * PRICE_INPUT_PER_M
        + tokens_out / 1_000_000 * PRICE_OUTPUT_PER_M)

# ---- 第四步:格式化报告(Day 02 的对齐语法) ----
print("=" * 50)
print(f"{'API 调用报告':^46}")
print("=" * 50)
print(f"{'模型':<8}{model}")
print(f"{'结束原因':<8}{finish_reason}")
print(f"{'输入tokens':<10}{tokens_in:>6}")
print(f"{'输出tokens':<10}{tokens_out:>6}")
print(f"{'总tokens':<10}{tokens_total:>6}")
print(f"{'本次成本':<8}{cost:.6f} 元")
print("-" * 50)
print("模型回答:")
print(content)
print("=" * 50)

# ---- 第五步:反向练习——组装并序列化一份请求体 ----
# 这就是 Day 12 要"发出去"的东西,今天先学会打包
request_body = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "system", "content": "你是一个乐于助人的AI助手"},
        {"role": "user", "content": "用一句话介绍Python"}
    ],
    "temperature": 0.7,
    "max_tokens": 200,
    "stream": False
}

request_json = json.dumps(request_body, ensure_ascii=False, indent=2)
print("请求体 JSON(即将在 Day 12 发往 api.deepseek.com):")
print(request_json)

# 无损往返验证(需求验收项)
assert json.loads(request_json) == request_body       # assert:断言,不相等就报错
print("✓ 序列化-解析往返验证通过")
```

## 4.4 加练:字段缺失的容错测试

需求第 4 条要求"字段缺失不崩溃"。当场测试——把 usage 整个删掉的残缺报文:

```python
# 残缺报文:没有 usage(某些代理接口真的会这样)
raw_no_usage = '{"model": "deepseek-chat", "choices": [{"index": 0, "message": {"role": "assistant", "content": "你好!"}, "finish_reason": "stop"}]}'

data2 = json.loads(raw_no_usage)
usage2 = data2.get("usage", {})                    # 没有 usage → 拿到空字典,不崩
print(usage2.get("total_tokens", 0))               # 空字典再 get → 0,依然不崩
content2 = data2["choices"][0]["message"]["content"]   # 必要字段照常方括号
print(content2)                                    # 你好!
```

两层 get 的接力兜底,让"可选信息缺失"永远不会炸掉主流程——这就是 1.3 节抉择心法的完整落地。**把这个防御模式记住,Day 12 的真实代码原样复用。**

## 4.5 收尾:数据层已集齐,只差一根网线

盘点一下你现在的装备:会组装 messages 字典列表(请求的核心)、会 dumps 打包、会 loads 解析、会从 choices 里剥出回答、会算成本、会防御缺失字段。**Day 12 那天要新学的,只剩 requests 库的三行代码(把 JSON 发到网址上、收回来)。** 一周后回看今天,你会明白这场彩排的价值。

---

# 【常见错误与排错手册】Day 05 专属篇

**错误 1:对着 JSON 字符串直接取值。** `raw["name"]` 报 `TypeError: string indices must be integers`——它还是字符串!先 `json.loads()`。判别技巧:`print(type(x))`,是 str 就得先解析。

**错误 2:JSONDecodeError 三大来源。** 单引号、尾逗号、Python 式大写 True/False/None。对照 3.1 差异表逐项检查。补一个隐蔽的:JSON 里字符串内部的换行必须写成 `\n`,真实换行会报错。

**错误 3:KeyError 但你确定键"存在"。** 三种真相:① 键有前后空格(`"name "` 不是 `"name"`,strip 治);② 大小写不一(`"Name"` 不是 `"name"`);③ 你在错的层级取——`data["content"]` 不存在,存在的是 `data["choices"][0]["message"]["content"]`。排查:`print(data.keys())` 看这一层到底有哪些键,一层一层往下看。

**错误 4:`for k, v in d` 忘了 `.items()`。** 报 `ValueError: too many values to unpack`(直接遍历字典只出键,没法拆成两个)。要键值对就 `.items()`。

**错误 5:用列表当键。** `TypeError: unhashable type: 'list'`。换成元组,或反思设计。

**错误 6:dumps 中文变 \uXXXX。** 忘了 `ensure_ascii=False`。数据没坏(loads 回来还是中文),只是没法看。

**错误 7:get 的默认值掩盖了真 bug。** 反面案例:`data.get("choices", [])` 之后 `[0]` 照样 IndexError 崩,而且崩得更晦涩。必要字段就该用方括号让它在第一现场崩——**防御要用在"缺了也正常"的字段上,不是用来把所有错误藏起来**。

**错误 8:嵌套结构里字典/列表取法混用。** `data["choices"]["message"]` 报 `TypeError: list indices must be integers`——choices 是列表,先 `[0]` 再往里走。剥洋葱口诀:每层先问"这层是字典还是列表"。

---

# 【课堂笔记】Day 05 知识点速查表

**字典 dict:按名字存取的抽屉柜**
- 创建:`{"键": 值}`;空字典 `{}`(空集合才是 set())
- 键:唯一、不可变(str/数字/元组);值:任意
- 增/改:`d[k] = v`(不存在则增,存在则改)
- 查:`d[k]` 缺键崩(必要字段用)| `d.get(k, 默认)` 缺键兜底(可选字段用)
- 删:`d.pop(k)` 递给你 | `del d[k]` | `d.pop(k, None)` 不崩版
- `in` 查的是**键**;查值 `v in d.values()`
- 遍历:`for k, v in d.items()`(最常用)| `.keys()` | `.values()`
- Python 3.7+ 字典保插入顺序;保序去重 `list(dict.fromkeys(lst))`

**哈希**:键 →哈希函数→ 抽屉号,一步到位;so 键必须不可变、集合无序

**嵌套**:剥洋葱口诀——每层先问是字典还是列表;字典 `["名"]`,列表 `[数]`
**字典列表**:`[{...}, {...}]` 数据世界通用形态;messages 就是它

**大模型 API 双格式(今天的核心资产)**
- 请求:`{"model": ..., "messages": [{"role": ..., "content": ...}], "temperature": ...}`
- 响应第一名句:`data["choices"][0]["message"]["content"]`
- 用量:`data.get("usage", {}).get("total_tokens", 0)` 双层兜底

**JSON**
- 身份:纯文本格式,是**字符串**不是字典
- 与 Python 差异:双引号 only、true/false/null 小写、无尾逗号、无注释
- 术语:object=字典、array=列表;解析 parse、序列化 serialize
- `json.loads(str)` → 对象;`json.dumps(obj, ensure_ascii=False, indent=2)` → 字符串
- load/dump(不带 s)管文件,Day 11 见
- 失败:JSONDecodeError,查单引号/尾逗号/大写布尔

---

# 【附录】课堂答疑实录(晚自习整理)

**问 1:字典和 JSON 到底什么关系?我感觉它们长得一样,总是分不清。**

答:一句话:**字典是内存里的活物,JSON 是纸上的描述**。类比:字典像一只活的猫(能摸能喂能操作),JSON 像这只猫的档案卡(一张纸,写着品种毛色)。你不能喂档案卡吃东西(不能对 JSON 字符串取值),也不能把活猫塞进传真机(不能把字典直接发到网上)。loads 是"照着档案卡领养一只一样的猫",dumps 是"给猫建档案"。判别永远靠 `type()`:dict 是猫,str 是卡。

**问 2:为什么 API 不直接传字典,非要转成 JSON 绕一圈?**

答:因为"字典"是 Python 的内部构造,内存里是一堆指针和哈希表,离开这个 Python 进程就没有意义——对方服务器可能是 Go 写的、前端是 JavaScript,谁认识你的内存布局?网络只能传字节流,所以必须先"拍平"成一种大家约好的文本格式。JSON 就是这个约定。类比:两国人打电话,各自脑子里的想法(字典)必须先转成双方约定的语言(JSON)才能传过去,对方听到再在自己脑子里重建想法(loads 成他们语言的对象)。

**问 3:除了 JSON 还有别的格式吗?为什么大模型 API 都选 JSON?**

答:有。XML(上一代主流,标签繁琐,银行等老系统还在用)、YAML(缩进式,爱当配置文件,Day 56 的 Docker Compose 就用它)、CSV(表格,Day 11 见)、Protobuf(二进制,更小更快但人读不了,内部微服务用)。API 选 JSON 是因为它正好卡在"人能读 + 机器好解析 + 所有语言原生支持 + 和 Web 前端无缝"的甜点上。行业选择已成事实,你顺势精通它就行。

**问 4:get 套 get 写起来好长,`data.get("usage", {}).get("total_tokens", 0)` 有没有更优雅的办法?**

答:好问题,几个层次的答案:① 两层还能接受,是业界常见写法;② 更深的嵌套(四五层)确实会失控,Python 生态的正规解法是 **Pydantic**——预先声明数据结构,自动校验和取值,它正是 Day 23 FastAPI 的核心组件,届时你会用它优雅地建模请求响应;③ 官方 SDK(openai 库)已经替你包好了,`response.choices[0].message.content` 用点号取,Day 12 两种方式都会教。今天用原始 get,是为了让你**看见包装纸底下的真实结构**——会走路再坐车,车抛锚了你也不慌。

**问 5:messages 里的 role 有三种,为什么第一条通常是 system?它和 user 有什么区别?**

答:完整答案在 Day 15/16,先给三句话版:**system 是"给模型的人设与规则"**(你是客服/只能答中文/不许透露内部信息),用户看不到它,但模型会遵守;**user 是用户说的话**;**assistant 是模型答的话**(多轮对话时要把它之前的回答存回去,模型才"记得"自己说过什么)。为什么 system 放第一条?因为模型对开头的指令最"上心"。Prompt 注入攻击(Day 18)本质就是用户试图用 user 消息推翻 system 规则——这场攻防战下下周开打。

**问 6:`assert` 是什么?今天代码里突然出现。**

答:断言——"我断定此事为真,若假立刻报错"。`assert 条件` 在条件为 False 时抛 AssertionError 停下来。它是工程师的"自检点":在代码里埋下"此处数据必须长这样"的检查,错误在离案发现场最近的地方暴露。今天用它验证"序列化再解析必须无损"。以后写测试(Day 34 的评估、Day 46 的工程化)全是 assert 家族。日常开发也可以随手埋:`assert len(messages) > 0`,比莫名其妙在十行之后崩清楚十倍。

**问 7:时间戳 1751702400 是什么?为什么不直接写"2026年7月5日"?**

答:Unix 时间戳——从 1970 年 1 月 1 日 0 点(UTC)到那一刻的**秒数**。机器世界用它,因为:一个整数,好存好算好比较(算两个时间差就是减法),没有时区、格式、语言的歧义。给人看时才翻译成"2026-07-05",翻译官是 datetime 模块(Day 11)。顺便留个彩蛋:`1751702400 % 60` 等于多少?——用 Day 02 的取余算算这个时刻的秒针位置。

**问 8:今天信息量爆炸,字典 + JSON 一天,我怕消化不了,重点保哪个?**

答:保三样,按优先级:① **第一名句** `data["choices"][0]["message"]["content"]`——闭眼能写;② **messages 的结构**——role/content 字典列表,append 累积;③ **loads/dumps + ensure_ascii=False**。这三样掌握,Day 12 就畅通。字典的花式操作(fromkeys、setdefault 之类)可以慢慢补,遍历和 get 用多了自然熟。另外明天(Day 06)的函数课信息密度略低,有喘息空间;后天(Day 07)周测复习日,上午会把这五天全部串讲一遍——课程节奏替你安排了消化时间,今晚把作业做完就是最好的消化。

---

# 【明日预告】Day 06:函数

五天下来,你已经攒了一堆"复制粘贴的痛":Day 03 BMI 作业的两段一模一样的校验循环、菜单系统里重复的编号校验、今天答疑说的"函数也能当字典的值"。明天的**函数(def)**一次全部解决:把一段逻辑打包命名,一处定义、处处调用;参数让它灵活(位置/关键字/默认值/*args/**kwargs——你会发现 `json.dumps(obj, ensure_ascii=False, indent=2)` 里的写法原来就是关键字参数);返回值让它产出(return 多个值就是昨天的元组)。下午的实操是**大重构日**:把前五天的所有小项目重构成函数式结构——同样的功能,代码量减三分之一,可读性翻倍。这是从"会写代码"到"会组织代码"的关键一跃。

**睡前自检清单**:
- [ ] 能闭眼写出"第一名句"和 messages 结构
- [ ] 能说出 JSON 与 Python 字典的 5 个差异
- [ ] loads/dumps 方向不混(带 s 管字符串;解析进来,序列化出去)
- [ ] API 响应解析器手敲运行通过,容错测试通过
- [ ] LeetCode:LC 1(两数之和)今天用字典重做一遍——哈希表解法,比昨天的双循环快一个量级,体会字典的威力
- [ ] 作业完成并 push,绿格子连续第 5 天
