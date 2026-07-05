# Day 13:进阶语法与异步入门 —— 项目一冲刺前的最后武装

---

# 【旁白解读】昨天、今天、明天

**昨天(Day 12)是通电日**:第一次真实调用大模型成功,chatlib 换上真引擎。但昨天的代码留了四处"毛边",今天逐一打磨:

1. qa_app 里限流重试是手写的 try 套 try(丑,且每个要重试的地方都要抄一遍)——今天的**装饰器**让它变成函数头上的一行 `@retry`;
2. API Key 存临时环境变量,"新开终端就失效"折磨了你一下午——今天 **python-dotenv** 根治;
3. 类型注解一直在"凭感觉写"——今天 **typing** 系统化,为 Day 23 的 FastAPI(类型注解驱动一切)铺路;
4. "能不能同时发多个请求?"——今天 **asyncio 异步入门**给出第一个答案,顺便学 **生成器 yield**(Day 24 流式输出的语法地基)。

今天是第一阶段最后一个"知识日"(明天是项目一考核),知识点偏抽象,但每一个都直连未来:装饰器 → Day 40 的 @tool;生成器 → Day 24 的 SSE 流式;typing → Day 23 的 Pydantic;dotenv → 以后每一个项目的第一步。**抽象的语法配上你已经亲手痛过的场景,就不抽象了**——这是把这些难点安排在第 13 天而不是第 3 天的原因。

---

# 上午 · 第一节(9:00 - 10:40):装饰器 —— 给函数穿铠甲的优雅姿势

## 1.1 复习两块地基

装饰器 = 两个你已经会的东西的组合:

```python
# 地基 1(Day 06):函数是一等公民——能存、能传、能被返回
def shout(text): return text.upper() + "!"
f = shout                    # 存
print(f("hi"))               # HI!

# 地基 2(Day 06 思考题 + Day 09 作业):闭包——内层函数记得出生环境
def make_multiplier(n):
    def inner(x):
        return x * n         # inner 带走了 n
    return inner
double = make_multiplier(2)
print(double(5))             # 10
```

Day 09 作业你还写过 RetryWrapper(类版包装器)。今天的装饰器就是它的函数版 + 一颗语法糖。

## 1.2 从手写包装到 @ 语法糖

需求:给任意函数加"调用前后打日志"。

```python
def with_log(func):
    """装饰器:接收一个函数,返回它的加强版。"""
    def wrapper(*args, **kwargs):            # *args/**kwargs:原样转发,不限制被包函数的签名
        print(f"[日志] 调用 {func.__name__},参数 {args}")
        result = func(*args, **kwargs)       # 干正事:调用原函数
        print(f"[日志] {func.__name__} 返回 {result!r}")
        return result                        # 别忘了把结果递出去!
    return wrapper                           # 返回加强版(闭包记住了 func)


# ── 手动包装(装饰器的"素颜") ──
def greet(name):
    return f"你好,{name}"

greet = with_log(greet)          # 用加强版顶替原函数——名字不变,内涵升级
greet("张三")

# ── @ 语法糖(完全等价,只是写法优雅) ──
@with_log                        # 这一行 = greet = with_log(greet)
def greet(name):
    return f"你好,{name}"

greet("张三")
# [日志] 调用 greet,参数 ('张三',)
# [日志] greet 返回 '你好,张三'
```

**@ 符号没有任何魔法**:`@with_log` 就是 `greet = with_log(greet)` 的缩写。看穿了糖衣,装饰器只剩三个动作:**收函数、造 wrapper、还 wrapper**。

两个规范细节立刻补上:

```python
import functools

def with_log(func):
    @functools.wraps(func)                   # ① 保住原函数的名字和 docstring
    def wrapper(*args, **kwargs):            #    (不加的话 greet.__name__ 会变成 'wrapper',
        ...                                  #     调试和文档都被搞乱——规范:装饰器必加)
        return func(*args, **kwargs)         # ② wrapper 必须 return,否则调用方拿到 None
    return wrapper
```

## 1.3 带参数的装饰器:@retry(max_retries=3)

昨天 qa_app 的手写重试,今天的最终形态:

```python
import functools
import time


def retry(max_retries: int = 3, retry_on: tuple = (Exception,), base_delay: float = 1.0):
    """重试装饰器工厂:失败自动重试,间隔指数退避(1s→2s→4s)。

    三层结构(比普通装饰器多一层,因为要先"吃参数"):
      retry(参数)      → 返回装饰器
      装饰器(func)     → 返回 wrapper
      wrapper(调用)    → 真正干活
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except retry_on as e:                    # 白名单:只重试"重试有用的"
                    last_error = e
                    if attempt < max_retries:
                        delay = base_delay * (2 ** (attempt - 1))    # 指数退避:1, 2, 4...
                        print(f"[retry] 第 {attempt} 次失败({e}),{delay:.0f}s 后重试")
                        time.sleep(delay)
            raise last_error                             # 次数用尽:原样上抛
        return wrapper
    return decorator


# ── 使用:一行给 chat 穿上重试铠甲 ──
from chatlib_v2 import RateLimitError, APIError

@retry(max_retries=3, retry_on=(RateLimitError, APIError))     # 401 的 AuthError 不在白名单:重试无用
def ask(model, messages):
    """一次调用(被装饰后自动带指数退避重试)。"""
    return model.chat(messages)
```

**指数退避(exponential backoff)**是行业标准的重试节奏:每次失败等待翻倍——限流时疯狂重试只会越限越死(昨天排错手册第 7 条),拉开间隔给服务喘息。openai 官方 SDK 内置的重试就是这个策略,今天你造了它的手工版。

装饰器的未来点名:Day 19 注册工具、**Day 40 LangChain 的 @tool**(把函数变成 Agent 的工具,一行)、Day 23 FastAPI 的 @app.get(路由注册)——**框架的"魔法一行",全是今天这套三层结构**。

## 1.4 functools.partial:Day 06 作业彩蛋兑现

Day 06 菜单作业用 `lambda: run_power(3)` 打包参数,当时说"正规军是 functools.partial":

```python
from functools import partial

def power(x, n): return x ** n

square = partial(power, n=2)         # 预填 n=2,得到新函数
cube = partial(power, n=3)
print(square(5), cube(5))            # 25 125
# 与 lambda 版等价,但 partial 保留函数元信息、可序列化,工程上更正规
```

---

# 上午 · 第二节(10:50 - 12:00):生成器与 yield —— 边生产边交付

## 2.1 从一个内存问题进入

需求:产出 1 到 1000 万的平方数,逐个处理。

```python
# 列表版:先把 1000 万个数全部造好装进内存(几百 MB),才开始处理第一个
squares = [i ** 2 for i in range(10_000_000)]

# 生成器版:造一个"会下蛋的鸡",要一个下一个,内存里永远只有一个
def square_gen(n):
    for i in range(n):
        yield i ** 2          # yield:交出一个值,然后"暂停在这里"等下次索取

gen = square_gen(10_000_000)
print(next(gen))              # 0     ← 手动索取一个
print(next(gen))              # 1     ← 函数从上次暂停处继续!
for sq in square_gen(5):      # for 会自动帮你 next 到耗尽
    print(sq)                 # 0 1 4 9 16
```

**yield 与 return 的本质区别**:return 是"交卷走人"(函数结束);**yield 是"交货暂停"**(函数冻结在原地,保留全部局部状态,下次被索取时原地复活继续跑)。含 yield 的函数调用时不执行任何代码,只返回一个**生成器对象**——真正的执行发生在每次 next。

其实你早就用过生成器:Day 05 起写的 `sum(len(m.content) for m in messages)` 里那个"没有方括号的推导式"就是**生成器表达式**——不建列表,边算边喂给 sum。Day 11 的 `for line in f` 逐行读文件,文件对象也是同一个精神:流式,不囤货。

## 2.2 生成器的主战场:流式输出(Day 24 的语法地基)

```python
import time


def fake_llm_stream(answer: str):
    """模拟大模型流式输出:一次吐两个字(真实 API 是逐 token 吐)。"""
    for i in range(0, len(answer), 2):
        time.sleep(0.1)                   # 模拟生成延迟
        yield answer[i:i + 2]             # 吐一块,暂停,等下次索取


# 消费端:打字机效果——Day 01 埋的 end="" 伏笔,今天正式接上!
answer = "大模型的流式输出,本质上就是一个生成器:服务器边生成边吐,客户端边收边显示。"
for chunk in fake_llm_stream(answer):
    print(chunk, end="", flush=True)      # 不换行 + 立即刷新 = 打字机
print()
```

看清这个结构:**生产者(生成器)按自己的节奏 yield,消费者(for)按自己的节奏取,两者通过"暂停/唤醒"衔接**。Day 24 的真实版里,生产者换成"DeepSeek 服务器的 SSE 数据流",消费循环几乎一字不改。ChatGPT 的打字机效果,语法内核就是今天这十行。

生成器要点补遗:**一次性用品**(耗尽后再遍历为空,要重新调用函数造新的);**惰性**(不索取就永不执行——省内存也意味着"错误会延迟到消费时才暴露",调试时注意)。

---

# 下午 · 第一节(14:00 - 15:00):typing 类型注解系统化 + dotenv

## 3.1 typing:把口头约定写成文档

两周来你一直在写 `def f(x: int) -> str`,今天补全常用武器谱:

```python
from typing import Optional, Union, Any, Callable

# ── 容器类型:装什么要说清楚(Python 3.9+ 直接用小写内置名) ──
def to_api_format(messages: list[dict]) -> list[dict[str, str]]:
    """list[dict]:字典组成的列表;dict[str, str]:键值都是字符串的字典。"""
    ...

# ── Optional:可能是 None(= X | None,Day 06 作业见过) ──
def find_session(name: str) -> Optional["ChatSession"]:      # 找不到返回 None
    ...
# Python 3.10+ 更爱写:-> ChatSession | None(竖线语法,课程首选)

# ── Callable:参数是"一个函数"(装饰器/回调的注解) ──
def retry_call(func: Callable[[], str], max_retries: int = 3) -> str:
    """Callable[[参数类型们], 返回类型]。"""
    ...

# ── Any:什么都可能(尽量少用——它等于放弃了注解的保护) ──
def load_json(filename: str) -> Any: ...

# ── 类型别名:给复杂类型起个业务名,可读性质变 ──
Message = dict[str, str]                       # 一条消息
Messages = list[Message]                       # 消息列表

def chat(messages: Messages) -> str: ...       # 一眼读懂,胜过三层嵌套的类型
```

再强调一次定位:**注解是文档 + 编辑器燃料,Python 运行时不强制检查**(传错类型照样跑到出错为止)。那谁来检查?三个层次:①VS Code 的 Pylance 实时画波浪线(装好 Python 插件就有,今天起注意看它);②mypy 等工具在 CI 里查(工程进阶,课程不展开);③**Pydantic 在运行时真查**——Day 23 的 FastAPI 里,类型注解会变成实打实的请求校验,"注解即校验"是那天的主菜。今天把注解写顺手,十天后直接起飞。

## 3.2 python-dotenv:API Key 管理的正规军

昨天的痛:临时环境变量,新终端就失效,每天重设。根治方案——把变量写进项目根目录的 `.env` 文件,程序启动时加载:

```bash
pip install python-dotenv
pip freeze > requirements.txt        # 清单更新,老规矩
```

```
# ── 文件:.env(项目根目录;已被 Day 10 的 .gitignore 挡住,绝不进 Git!) ──
DEEPSEEK_API_KEY=sk-你的真实key
APP_ENV=dev
```

```python
# ── 使用:程序入口最顶部,两行 ──
from dotenv import load_dotenv
load_dotenv()                        # 读 .env,把里面的键值注入 os.environ

import os
api_key = os.environ.get("DEEPSEEK_API_KEY")     # 之后照旧——昨天的代码零改动!
```

**配套纪律(行业标准做法)**:仓库里放一份 `.env.example`(只有键名没有真值:`DEEPSEEK_API_KEY=你的key填这里`),**它进 Git**,作为同事的配置说明书;真 `.env` 各自本地维护。这套"example 进库、真身不进库"的模式,你以后接手任何开源项目都会见到——clone 下来第一件事就是 `cp .env.example .env` 填 Key。

优先级也要说清:我们的 DeepSeekModel 里 Key 来源是"参数 > 环境变量",load_dotenv **不会覆盖**已存在的环境变量(默认行为)——所以顺序是:显式参数 > 系统环境变量 > .env 文件。配置的"就近覆盖"原则,Day 56 的 Docker 环境变量还会再遇到。

---

# 下午 · 第二节(15:10 - 16:20):asyncio 异步入门 —— 理解 async/await

## 4.1 为什么需要异步:等待才是最大的浪费

昨天答疑问 7 的正式回答。看一笔时间账:调用一次大模型 API 约 3 秒,其中你的 CPU 干活(组装 JSON、解析响应)不到 0.001 秒——**99.9% 的时间在干等网络**。要给 10 段文本做摘要:

```
同步(串行):发① 等3s 收① → 发② 等3s 收② → …  共 30 秒,CPU 全程围观
异步(并发):发①②…⑩(等待重叠在一起)→ 陆续收齐        共约 3 秒
```

异步的本质:**等待的时候去干别的**。像一个服务员看十桌客人(菜在厨房做的时候去招呼别桌),而不是站在一桌旁边等菜上齐才动。注意它不是多核并行(那是另一套机制),而是"单人高效调度等待"——**对 I/O 密集型任务(网络请求、读写文件)是降维打击,对计算密集型无效**。大模型应用几乎全是 I/O 密集,所以异步是这个领域的显学。

## 4.2 async/await 最小语法集

```python
import asyncio


async def fetch_summary(doc_id: int) -> str:
    """async def:定义'协程函数'——可暂停可恢复的函数(生成器的亲戚!)。"""
    print(f"发出请求 {doc_id}")
    await asyncio.sleep(3)               # await:"这里要等,调度器你先去忙别的"
    # 真实场景这里是异步的 HTTP 请求;asyncio.sleep 模拟 3 秒网络延迟
    print(f"收到响应 {doc_id}")
    return f"文档{doc_id}的摘要"


async def main():
    # ── 串行写法(错误示范):await 一个再 await 下一个 → 9 秒 ──
    # r1 = await fetch_summary(1); r2 = await fetch_summary(2); ...

    # ── 并发写法:gather 把三个任务一起交给调度器 → 3 秒 ──
    results = await asyncio.gather(
        fetch_summary(1),
        fetch_summary(2),
        fetch_summary(3),
    )
    print(results)                       # ['文档1的摘要', '文档2的摘要', '文档3的摘要']


asyncio.run(main())                      # 异步世界的总开关:启动事件循环
# 运行观察:三个"发出请求"几乎同时打印,3 秒后三个"收到响应"一起到——
# 总耗时 3 秒而不是 9 秒。亲眼看到这个输出,异步就懂了一半
```

四个词的最小心智模型:**async def** 定义可暂停的函数(协程);**await** 标记"此处要等,让出控制权";**gather** 把多个协程并发跑;**asyncio.run** 总开关。再补三条纪律:①协程函数直接调用不执行(`fetch_summary(1)` 只返回协程对象——和生成器"调用不执行"同一个精神),必须 await 或交给 gather/run;②**同步函数里不能用 await**(SyntaxError);③async 世界里禁止调用会卡住的同步操作(如 time.sleep、requests)——会把整个调度器堵死,要用 asyncio.sleep、aiohttp/httpx 等异步版。

## 4.3 课程定位:今天只到"入门"

诚实地说清楚边界:**今天的目标是"看懂 + 体感",不是"熟练"**。原因:①异步代码的调试难度显著高于同步,初学阶段收益不抵成本;②你马上要用的框架替你处理了大部分异步——**Day 23 的 FastAPI 里 `async def` 的路由函数随处可见**(今天之后你能看懂它了),LangChain 的 `ainvoke`/`astream` 是 invoke/stream 的异步版(Day 26 见到不慌);③真正需要手写并发的场景(批量向量化、压测)集中在 Day 28+ 和 Day 46,届时带着真实需求回炉,一次到位。今天种下心智模型:**异步 = 把等待重叠起来;async/await = 标记在哪等**。

---

# 下午 · 第三节(16:30 - 17:30):实操——chatlib 三件套武装

## 5.1 需求文档

> ### 需求文档:chatlib v3——项目一战备版
>
> **需求编号**:REQ-D13-001
> **背景**:明天(Day 14)交付项目一。今天完成 chatlib 的最后武装,三件套:
> 1. **@retry 装饰器**(utils.py 新模块):指数退避、异常白名单、functools.wraps;应用到 DeepSeekModel.chat 上(白名单:RateLimitError、APIError;**AuthError 不重试**);
> 2. **dotenv 集成**:main 入口 load_dotenv;仓库提供 .env.example;确认 .gitignore 挡住 .env;
> 3. **超时参数化**:DeepSeekModel 增加 timeout 构造参数(默认 60),类型注解全面补齐(Messages 类型别名)。
>
> **验收标准**:FakeModel(fail_times=2) + @retry 自动恢复(观察退避日志 1s→2s);.env 配置后新终端直接可用;AuthError 立刻失败不重试。

## 5.2 关键实现(完整见 code/chatlib_v3/)

```python
# chatlib_v3/utils.py —— 新模块:通用工具
import functools
import time

Message = dict[str, str]                 # 类型别名:一条消息
Messages = list[Message]                 # 消息列表——全库统一用它注解


def retry(max_retries: int = 3, retry_on: tuple = (Exception,), base_delay: float = 1.0):
    """重试装饰器工厂(指数退避 + 异常白名单)。"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except retry_on as e:
                    last_error = e
                    if attempt < max_retries:
                        delay = base_delay * (2 ** (attempt - 1))
                        print(f"[retry] 第 {attempt} 次失败({e}),{delay:.0f}s 后重试")
                        time.sleep(delay)
            raise last_error
        return wrapper
    return decorator
```

```python
# chatlib_v3/models.py 里的应用(节选)
from chatlib_v3.utils import retry, Messages
from chatlib_v3.exceptions import APIError, AuthError, RateLimitError


class DeepSeekModel(BaseChatModel):
    def __init__(self, ..., timeout: int = 60):
        ...
        self.timeout = timeout                       # 超时参数化:压测/慢网可调

    @retry(max_retries=3, retry_on=(RateLimitError, APIError), base_delay=1.0)
    def chat(self, messages: Messages) -> str:
        """带自动重试的对话调用。AuthError 不在白名单:重试无用,立刻上抛。"""
        if not messages:
            raise ValueError("messages 不能为空")
        return self._do_request(messages)
    # 注意:装饰器装在 chat 上而不是 _do_request 上——
    # 让"参数校验错误(ValueError)"也走一遍装饰器?不:ValueError 不在白名单,
    # 第一次抛出就直接上抛,行为正确。白名单机制天然保护了这一点
```

对照昨天 qa_app 里那坨手写的 try 套 try:**今天全部删掉,主循环里只剩干净的一层 except**——重试的复杂度被装饰器吸走了。"复杂度不消失,但可以被封装到看不见的地方",Day 08 的话第三次应验。

## 5.3 验收演示(完整见 code/drill.py)

```python
from dotenv import load_dotenv
load_dotenv()                            # 三件套之二:入口两行

from chatlib_v3 import FakeModel, DeepSeekModel, AuthError
from chatlib_v3.utils import retry
from chatlib_v3.exceptions import RateLimitError

# 演示 1:@retry 自动恢复(观察退避日志)
flaky = FakeModel(fail_times=2)

@retry(max_retries=4, retry_on=(RateLimitError,), base_delay=0.2)
def ask(model, messages):
    return model.chat(messages)

print(ask(flaky, [{"role": "user", "content": "hi"}]))
# [retry] 第 1 次失败(...),0s 后重试
# [retry] 第 2 次失败(...),0s 后重试
# [假回答] ...  ← 第三次成功,调用方全程无感

# 演示 2:AuthError 不重试(白名单外直接上抛,秒失败)
```

---

# 【常见错误与排错手册】Day 13 专属篇

**错误 1:wrapper 忘了 return func(...) 的结果。** 被装饰的函数"返回 None 了"。装饰器三步:收函数、造 wrapper(**里面 return**)、还 wrapper。

**错误 2:带参装饰器少写一层。** `@retry` 和 `@retry()` 不一样!我们的 retry 是"装饰器工厂",必须带括号调用(`@retry(max_retries=3)` 或至少 `@retry()`);裸 `@retry` 会把函数直接喂给工厂,报诡异的 TypeError。判别:定义有三层 def 的,使用必带括号。

**错误 3:忘 @functools.wraps,函数名变 wrapper。** 调试时 traceback 全是 wrapper,分不清谁是谁。规范:装饰器必加 wraps。

**错误 4:生成器耗尽后再用,得到空。** 生成器是一次性用品。要重复遍历:重新调用生成器函数,或一开始就 list() 物化(小数据时)。

**错误 5:协程函数调用了没 await。** `RuntimeWarning: coroutine 'xxx' was never awaited`——拿到协程对象却没启动。补 await,或交给 gather/run。

**错误 6:async 函数里用了 time.sleep / requests。** 不报错但整个事件循环被堵死,并发变串行。异步世界用 asyncio.sleep / httpx.AsyncClient。

**错误 7:.env 改了不生效。** 三查:①load_dotenv() 是否在读取 os.environ **之前**执行;②.env 是否在运行目录(或用 load_dotenv(dotenv_path=...) 指定);③系统环境变量里是否残留同名旧值(默认不覆盖——`load_dotenv(override=True)` 可强制,但先搞清楚哪来的旧值)。

**错误 8:.env 提交进 Git 了。** 立刻:①把 Key 在平台后台作废重发(泄露了就是泄露了,删提交救不回已被抓取的);②确认 .gitignore 有 .env;③`git rm --cached .env` 移出追踪。预防胜于补救,每次 push 前 `git status` 扫一眼。

---

# 【课堂笔记】Day 13 知识点速查表

**装饰器**
- 本质:`@d` ≡ `f = d(f)`;三步:收函数 → 造 wrapper(转发 *args/**kwargs,**return 结果**)→ 还 wrapper
- 必加 `@functools.wraps(func)`;带参装饰器 = 三层 def 的工厂,使用必带括号
- @retry:指数退避(delay = base × 2^(n-1))+ 异常白名单(只重试"重试有用的")
- 未来:@tool(Day 40)、@app.get(Day 23)全是这个结构
- partial:预填参数的正规军(lambda 打包的替代)

**生成器**
- yield = 交货暂停(保留状态原地复活);return = 交卷走人
- 调用不执行,next/for 才驱动;一次性用品;惰性(不索取不执行)
- 生成器表达式 `(x for x in ...)`:无方括号的推导式,喂 sum/any 直接用
- 主战场:流式输出(打字机 = yield 块 + `print(chunk, end="", flush=True)`)→ Day 24

**typing**
- `list[dict]`、`dict[str, str]`、`X | None`(Optional)、Callable、类型别名 `Messages = list[Message]`
- 注解是文档不强制;Pylance 实时检查;Pydantic 运行时真查(Day 23)

**dotenv**
- .env 放 Key(**不进 Git**);.env.example 进 Git 当说明书
- 入口两行:`from dotenv import load_dotenv; load_dotenv()`
- 优先级:显式参数 > 系统环境变量 > .env(默认不覆盖)

**asyncio(入门版心智模型)**
- 异步 = 把等待重叠;I/O 密集降维打击,计算密集无效
- async def 协程(调用不执行)/ await 让出控制权 / gather 并发 / asyncio.run 总开关
- 禁在 async 里用 time.sleep/requests;FastAPI 的 async def 路由(Day 23)现在能看懂了

---

# 【附录】课堂答疑实录(晚自习整理)

**问 1:装饰器和 Day 09 的 RetryWrapper 类,以后到底用哪个?**

答:95% 用装饰器——@ 语法糖让"给函数加能力"变成零成本动作,行业惯例也是它。类版包装器的生态位:需要**运行时改配置**(wrapper 的参数在装饰时就定死了,类的属性随时能改)、需要**携带复杂状态**(重试统计、熔断计数)。Day 46 讲 Agent 稳定性时的"熔断器"会用类版。今天起简历技能表可以写"熟悉装饰器原理与自定义装饰器"了——前提是明天开始每次用的时候都能默写出三层结构。

**问 2:一个函数能叠多个装饰器吗?顺序有讲究吗?**

答:能,自下而上装、自上而下拆:

```python
@with_log            # 后装(在外层):日志里能看到重试过程
@retry()             # 先装(在内层):贴着函数
def chat(...): ...
# 等价于 chat = with_log(retry()(chat))
```

顺序当然有讲究:@retry 在内 → 重试的是裸函数,日志看到完整重试过程;反过来 → 每次重试都各打一份日志。规则:**从紧贴函数的那个开始,由内向外生效**。Day 23 的 FastAPI 里"@app.get + 依赖注入"的叠放顺序同理。

**问 3:yield 和 return 能同时出现在一个函数里吗?**

答:能。生成器里的 return 表示"不再下蛋了"(触发 StopIteration 结束迭代),常用来提前收工:`if bad: return`。但 return 带值的用法(值藏在 StopIteration 里)很少直接用。日常心法:**生成器里 return = 只用来刹车**。

**问 4:异步能让单次 API 调用变快吗?**

答:不能,这是最常见的误解。单次调用的 3 秒是模型推理 + 网络传输的物理时间,异步不改变它。异步优化的是**吞吐**(单位时间完成的总量):10 个请求从 30 秒到 3 秒,靠的是等待重叠,不是任何一个变快。要单次变快:换更快的模型、减少 max_tokens、用流式让"首字时间"提前(体感快,总时长不变)——这是 Day 46 延迟优化的话题清单。

**问 5:.env、环境变量、配置文件(JSON),都能放配置,怎么分工?**

答:按"机密程度 + 变化频率"分:**机密**(API Key、数据库密码)→ .env/环境变量(不进 Git 是硬边界);**环境差异配置**(dev/prod 的 URL、开关)→ 环境变量为主(Day 56 Docker 注入);**业务配置**(菜单结构、价格表、Prompt 模板)→ JSON/YAML 文件(进 Git,要版本追溯)。判断口诀:泄露会出事的进 .env,换环境会变的进环境变量,业务要审阅的进配置文件。

**问 6:为什么 @retry 装在 chat 上而不是 _do_request 上?**

答:课件 5.2 注释提了一半,展开说:两处都可行,选 chat 有两个理由:①**语义**——"带重试的对话"是对外承诺的一部分,装在公开接口上让使用者可见(看源码一眼看到 @retry);②**未来**——子类如果重写 _do_request(比如 Day 24 的流式版),装在 chat 上的重试自动覆盖新实现,装在 _do_request 上则要每个子类自己记得装。装饰器的位置 = 能力的作用域,放在"稳定的接口"上比放在"易变的实现"上划算——又是接口与实现之辨(Day 09)。

**问 7:明天项目一,今晚要准备什么?**

答:三件事:①**通读需求**——明天课件开头就是完整需求文档,但你其实已经知道了:多轮对话记忆(维护 messages)、历史保存 JSON、异常处理、指令 /clear /save /exit——每一样的零件都在你手里,今晚可以先想架构;②**盘点零件**——chatlib_v3(今天的成果)、ChatSession(Day 09 完全体)、parse_command(Day 07 上机题 2!)、存档管理(Day 11 作业)——明天是组装日,不是发明日;③**睡好**——明天有代码互评环节,你的代码会被同学阅读,今晚可以把这两周的坏习惯(裸变量名、没 docstring)提前自查一遍。

**问 8:两周学完了 Python 基础,我和"科班一年"的差距还有多少?**

答:分维度看。**语法覆盖面**:你已达到日常开发的 90%(缺的多线程、元类、描述符等属于"用到再学"的长尾);**工程习惯**:你的 Git 日提交、venv、异常军规、类型注解,坦白说超过很多科班生(他们的课程不教这些);**算法与计算机体系**:这是真差距(数据结构、操作系统、网络原理的深度),LeetCode 日课就是在补,但需要时间。战略建议:应用层求职看"工程能力 + 项目作品 + 领域知识(大模型)"三样,恰好是本课程的配重——把你的长板打到极长,短板补到不拖后腿。明天的项目一,就是第一块长板。

---

# 【明日预告】Day 14:阶段考核 —— 项目一《命令行多轮对话 AI 助手》

明天全天项目日:上午需求讲解 + 架构设计 + 开发;下午继续开发 + 测试;晚上代码互评 + 讲师点评。需求关键词:**多轮对话记忆**(维护 messages——昨天撞过的墙,明天拆)、**对话历史保存为 JSON**(/save,Day 11 的手艺)、**异常处理**(Day 10 军规 + 今天的 @retry)、**指令系统**(/clear /save /exit,Day 07 的 parse_command)。这是你简历上的第一个完整项目,两周的一切都为它。早点睡。

**睡前自检清单**:
- [ ] 能默写三层 def 的 @retry 骨架
- [ ] yield 的"交货暂停"、async/await 的"等待重叠"能给同桌讲明白
- [ ] .env 配置完成,新终端直接跑通 drill.py
- [ ] chatlib_v3 三件套验收全过
- [ ] LeetCode:LC 118(杨辉三角——用生成器写一版!)、LC 70(爬楼梯)
- [ ] 作业完成并 push,绿格子连续第 13 天
