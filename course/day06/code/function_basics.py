# =============================================
# Day 06 · 上午演示代码 1:函数定义、return、参数四件套
# 文件:function_basics.py
# =============================================

# ---- 1. 第一个函数:从复制粘贴的废墟上站起来 ----
def mask_phone(phone):
    """把 11 位手机号脱敏为 138****5678 的形式。"""
    return phone[:3] + "****" + phone[-4:]

print(mask_phone("13812345678"))     # 138****5678
print(mask_phone("13900001111"))     # 139****1111

# 认知 1:定义 ≠ 执行。def 只登记菜谱,调用才做菜。

# ---- 2. return vs print(今天头号考点) ----
def add_print(a, b):
    print(a + b)             # 只是"喊出"结果,喊完就没了

def add_return(a, b):
    return a + b             # 把结果"递出去",调用方能接住继续用

x = add_print(3, 5)          # 屏幕出现 8,但……
print(x)                     # None:没 return 的函数默认递出 None
y = add_return(3, 5)
print(y * 10)                # 80:能继续参与计算
# 心法:print 给人看,return 给程序用;工具函数只 return 不 print

# ---- 3. 提前返回:消灭嵌套(Day 03 欠的技巧 2) ----
def check_password(pwd):
    """密码强度:提前返回版——不合格先踢走,缩进永远一层。"""
    if len(pwd) < 8:
        return "弱:太短"
    if pwd.isdigit():
        return "弱:纯数字"
    if pwd.lower() == pwd:
        return "中"
    return "强"

print(check_password("abc"))          # 弱:太短
print(check_password("Abcdefg8"))     # 强

# ---- 4. 参数四件套 ----
# ① 位置参数:按顺序对号入座
def make_message(content, role="user"):        # ③ 默认参数:不传用出厂设置
    """组装一条 messages 消息(Day 05 结构的函数化)。"""
    return {"role": role, "content": content}

print(make_message("你好"))                          # 默认 user
print(make_message("你是助教", role="system"))        # ② 关键字参数:指名道姓

# ④ *args:多余的位置参数打包成元组
def average(*scores):
    """算任意个成绩的平均分。"""
    if not scores:                    # 防空:空元组
        return 0
    return sum(scores) / len(scores)

print(average(90, 85))                # 87.5
print(average(90, 85, 77, 60))        # 78.0

# ④ **kwargs:多余的关键字参数打包成字典
def call_llm(model, **options):
    """模拟大模型调用:除 model 外的具名参数全进 options。
    LangChain 源码里 **kwargs 铺天盖地,原理就是这个。"""
    print(f"模型:{model}")
    print(f"可选参数:{options}")

call_llm("deepseek-chat", temperature=0.7, max_tokens=200, stream=False)

# 反向解包:配置字典 ** 一撒就传参(配置与代码分离再进一步)
params = {"temperature": 0.7, "max_tokens": 200}
call_llm("deepseek-chat", **params)

# ---- 5. 默认参数地雷:禁用可变对象 ----
def add_task_bad(task, todos=[]):          # ❌ 默认列表只创建一次,所有调用共享!
    todos.append(task)
    return todos

print(add_task_bad("A"))     # ['A']
print(add_task_bad("B"))     # ['A', 'B'] ?! 上次的 A 还在

def add_task(task, todos=None):            # ✅ 默认 None,函数体内再造
    """往待办列表添加任务;不传列表则新建。"""
    if todos is None:                      # is None 是判断 None 的规范写法
        todos = []
    todos.append(task)
    return todos

print(add_task("A"))         # ['A']
print(add_task("B"))         # ['B'] 各自独立

# ---- 6. docstring + 类型注解:函数自带说明书 ----
def estimate_cost(tokens_in: int, tokens_out: int,
                  price_in: float = 1.0, price_out: float = 4.0) -> float:
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

print(f"{estimate_cost(1200, 800):.6f} 元")
help(estimate_cost)          # help 打印 docstring;VS Code 悬停也能看
