# =============================================
# Day 06 · 上午演示代码 2:作用域、lambda、递归
# 文件:scope_lambda_recursion.py
# =============================================

# ---- 1. 作用域:函数内外是两个世界 ----
count = 0                        # 全局变量


def demo():
    msg = "函数内部的临时变量"      # 局部变量:函数结束即销毁
    print(count)                 # ✅ 函数内可以"读"全局
    print(msg)


demo()
# print(msg)                     # ❌ NameError:外面不认识局部变量

# 读可以,改不行(函数内赋值即局部,UnboundLocalError):
# def try_modify():
#     count = count + 1          # 报错!

# 正道:参数进,return 出(纯函数,不碰外面的东西)
def good_style(n: int) -> int:
    """计数加一:进出都走明路。"""
    return n + 1


count = good_style(count)
print(count)                     # 1

# 例外须知:传"可变对象"= 给函数原件的钥匙
def add_message(messages: list, content: str) -> None:
    """往对话历史里添加一条用户消息(明示的原地修改)。"""
    messages.append({"role": "user", "content": content})


history = []
add_message(history, "你好")
print(history)                   # 外面真的变了——知情+故意,这是特性不是 bug

# ---- 2. lambda:一次性小函数,主场是 key= ----
todos = [
    {"task": "复习", "priority": 2},
    {"task": "写作业", "priority": 1},
    {"task": "刷题", "priority": 3},
]
todos.sort(key=lambda t: t["priority"])          # 按 priority 字段排
print([t["task"] for t in todos])                # ['写作业', '复习', '刷题']

scores = [("张三", 92), ("李四", 85), ("王五", 88)]
top = max(scores, key=lambda s: s[1])            # 按元组第 2 项找最大
print(top)                                       # ('张三', 92)
# 尺度:lambda 只容一个表达式;想给它起名字 = 该用 def 了

# ---- 3. 递归:出口 + 规模缩小 ----
def countdown(n: int) -> None:
    """倒数(递归版,教学演示)。"""
    if n == 0:                    # ① 出口:必须有,否则 RecursionError
        print("发射!")
        return
    print(n)
    countdown(n - 1)              # ② 自我调用:规模缩小


countdown(3)                      # 3 2 1 发射!


def factorial(n: int) -> int:
    """阶乘:n! = n × (n-1)!"""
    if n <= 1:                    # 出口:1! = 1
        return 1
    return n * factorial(n - 1)   # 委托给"算 (n-1)! 的自己"


print(factorial(5))               # 120

# 循环版对照(更快更省内存;平铺问题用循环,套娃问题用递归):
def factorial_loop(n: int) -> int:
    """阶乘:循环版。"""
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


print(factorial_loop(5))          # 120
