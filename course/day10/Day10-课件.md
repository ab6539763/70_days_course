# Day 10:模块、包与异常处理 —— 让代码住进楼房,给程序穿上铠甲

---

# 【旁白解读】昨天、今天、明天

**昨天(Day 09)你搭出了可插拔模型层**,OOP 全部通关。但代码组织还停留在"单文件"时代:chat_models.py、model_layer.py 各自为政,昨天作业 kimi_model.py 里甚至出现了 `sys.path.insert(0, ...)` 这种"临时手法"(注释里写着"规范做法 Day 10 讲")——今天兑现。

**今天上午解决"代码的居住问题"**:程序大了,单文件塞不下,怎么拆成多文件(模块)、多文件夹(包)?import 到底怎么工作?`if __name__ == "__main__"` 拖了四天的谜底揭晓。附带两个工程刚需:**虚拟环境 venv**(每个项目一个独立的库空间,防止版本打架)和 **requirements.txt**(项目依赖清单)——明天开始我们要安装第三方库(Day 12 的 requests),没有这两样,你的电脑三个月后就是库版本的战场。

**今天下午解决"程序的生存问题"**:异常处理。你已经零星见过它四次:Day 05 的 JSONDecodeError 演示、Day 07 持久化模板里的 try/except FileNotFoundError、Day 08 的 raise ValueError、昨天 RetryWrapper 里的 try/except——每次都说"Day 10 正式学"。今天系统讲透 try/except/else/finally 的完整语法、异常的类型体系、自定义异常,以及最重要的:**什么时候该捕获、什么时候该让它崩**(这比语法难十倍,也值钱十倍)。

**为什么这两个主题放在一起、放在今天?** 因为 Day 12(后天)首次调用真实 API,那是一个"外部世界"的入口:网络会断、Key 会错、服务会限流、返回会残缺——**没有异常处理的 API 调用,就是在裸奔**;而 API 调用代码需要被封装成可复用的模块给 Day 14 的项目用——**没有包结构,复用就是复制粘贴**。今天的两课,都是 Day 12 的行前装备。

下午实操:把第二周的类库拆成规范的多文件包 `chatlib/`,并给模型层穿上第一层异常铠甲。这个包会一路用到 Day 14,然后被 LangChain"平替"——那时你会因为造过轮子而真正理解轮子。

---

# 上午 · 第一节(9:00 - 10:20):模块与 import 机制

## 1.1 模块 = 一个 .py 文件

**每个 .py 文件天然就是一个模块(module)**,别的文件可以 import 借用它的函数、类、变量。你已经用了两周的 `import json`、`import random`,借的就是 Python 自带的模块(标准库)。今天学会借自己的:

```python
# ── 文件 1:text_utils.py(工具模块) ──────────────────
"""文本工具模块:第一周积累的清洗函数,正式安家。"""

DEFAULT_BANNED = ["垃圾", "傻子", "废物"]        # 模块级变量


def mask_phone(phone: str) -> str:
    """手机号脱敏。"""
    return phone[:3] + "****" + phone[-4:]


def clean_text(text: str) -> str:
    """基础清洗:去两端空白 + 规范空格。"""
    return " ".join(text.strip().split())
```

```python
# ── 文件 2:main.py(使用方,与 text_utils.py 同目录) ──
import text_utils                          # 方式一:整个模块搬进来,用"模块.成员"访问

print(text_utils.mask_phone("13812345678"))
print(text_utils.DEFAULT_BANNED)

from text_utils import clean_text, mask_phone     # 方式二:点名借具体成员,直接用名字

print(clean_text("  多余   空格  "))

from text_utils import mask_phone as mask         # 方式三:借来改个名(名字冲突时用)
print(mask("13900001111"))
```

**三种 import 的选择规范**(公司常见约定):

- `import 模块`:最稳,来源清晰(`text_utils.clean_text` 一看就知道哪来的),模块名短时首选;
- `from 模块 import 成员`:高频使用的成员点名借,代码更短;**但别一次借太多**;
- `from 模块 import *`:**禁用**。把对方所有名字倒进你的命名空间,谁覆盖了谁完全失控——除了教学演示,永远不要写。

## 1.2 import 的幕后:执行,而不只是"读取"

**关键认知:import 一个模块时,Python 会从头到尾执行它一遍**(定义函数、创建变量……都是"执行")。用实验钉死:

```python
# ── noisy.py ──
print("我是 noisy 模块,我被执行了!")       # 模块顶层的裸代码

def hello():
    return "hi"

# ── main.py ──
import noisy          # 屏幕立刻打印"我是 noisy 模块,我被执行了!"
import noisy          # 第二次 import:什么都不打印(模块只执行一次,之后走缓存)
```

两个推论,每个都直击你写过的代码:

**推论 1:`if __name__ == "__main__"` 的谜底(四天悬案结案)。**

Python 给每个模块一个内置变量 `__name__`:**直接运行**这个文件时,它的值是 `"__main__"`;**被 import** 时,它的值是模块名(如 `"text_utils"`)。于是:

```python
# text_utils.py 末尾
if __name__ == "__main__":
    # 只有"python text_utils.py"直接运行时才执行这里——
    # 通常放模块的自测代码;被 import 时这里完全跳过
    assert mask_phone("13812345678") == "138****5678"
    print("text_utils 自测通过")
```

这就是 Day 06 起每个文件末尾那两行的全部原理:**让文件"可直接运行自测,也可被安静地借用"**。反面案例:如果 main() 裸奔在文件末尾,别人 import 你的工具模块时会莫名弹出你的菜单——Day 06 答疑预言过的事故。

**推论 2:模块顶层不要放"有动作的"裸代码。** 顶层只放:import、常量、函数/类定义。打印、输入、启动逻辑一律进函数,由 `if __name__ == "__main__"` 守门。

## 1.3 包 = 装模块的文件夹

模块多了,用文件夹归类——**包(package)就是含 `__init__.py` 的文件夹**:

```
chatlib/                    ← 包(文件夹)
├── __init__.py             ← 包的"身份证"(可以是空文件;也可做门面,见下)
├── messages.py             ← 模块:消息类
├── models.py               ← 模块:模型层
└── utils/                  ← 子包(包可以套包)
    ├── __init__.py
    └── text.py             ← 模块:文本工具
```

```python
# 使用方(在 chatlib 的上一级目录):
from chatlib.messages import ChatMessage          # 包.模块 路径式导入
from chatlib.models import DeepSeekModel
from chatlib.utils.text import mask_phone         # 子包再深一层
```

`__init__.py` 的两个角色:①**身份证**——告诉 Python"这个文件夹是包"(新版本 Python 没有它也勉强能跑,但**规范要求必须有**,空文件即可);②**门面**——在里面预先转口常用成员,让使用方少写一层:

```python
# chatlib/__init__.py
"""chatlib:课程自研对话类库(Day 08-14 服役,Day 25 由 LangChain 接棒)。"""
from chatlib.messages import ChatMessage, ChatSession       # 转口
from chatlib.models import BaseChatModel, DeepSeekModel, FakeModel

__all__ = ["ChatMessage", "ChatSession", "BaseChatModel", "DeepSeekModel", "FakeModel"]

# 使用方从此可以直接:
# from chatlib import ChatMessage, DeepSeekModel      ← 少写一层,好记
```

你天天在享受这种门面:`from langchain_openai import ChatOpenAI` 之所以这么短,就是人家 `__init__.py` 里做了转口。**Day 25 起你读框架源码,第一步永远是看它的 `__init__.py`**——那是一个包的目录页。

顺带解决昨天的"临时手法":kimi_model.py 里的 `sys.path.insert` 是在手动把某个目录塞进 Python 的搜索路径。规范做法就是今天的包结构:**代码组织成包,从项目根目录运行**,Python 自然找得到,永远不需要 sys.path 杂技。

## 1.4 虚拟环境 venv 与 requirements.txt

**问题场景**:项目 A 需要 langchain 0.2,项目 B 需要 langchain 0.3,全装在系统 Python 里必然打架。**解法:每个项目一个独立的"库房间"——虚拟环境**:

```bash
# ① 在项目根目录创建虚拟环境(会生成 .venv 文件夹,装着一个独立的小 Python)
python -m venv .venv

# ② 激活(进入这个房间;终端提示符前会出现 (.venv) 标记)
#    Windows (PowerShell):
.venv\Scripts\Activate.ps1
#    Windows (cmd):
.venv\Scripts\activate.bat
#    macOS / Linux:
source .venv/bin/activate

# ③ 激活后,pip 装的一切只进这个房间,不污染系统
pip install requests

# ④ 退出房间
deactivate
```

**requirements.txt:房间的购物清单。** 记录项目依赖,让任何人(包括三个月后的你、服务器、同事)一条命令复原环境:

```bash
# 导出当前环境的依赖清单
pip freeze > requirements.txt
# 文件内容形如:
#   requests==2.32.3
#   python-dotenv==1.0.1

# 别人拿到项目后一键装齐:
pip install -r requirements.txt
```

**课程纪律(从明天起强制执行)**:每个项目根目录必有 `.venv`(并写进 .gitignore,虚拟环境本身不进 Git!)和 `requirements.txt`(必须进 Git)。conda 是另一套同类工具(数据科学圈常用,Day 51 的 GPU 服务器上会遇到),概念相通:conda create 建房间、conda activate 进房间。

## 1.5 VS Code 与虚拟环境的配合

创建 .venv 后,VS Code 右下角选择解释器时选 `.venv` 里的那个(通常会自动弹窗建议)。**判断选对了没有**:集成终端新开一个,提示符带 `(.venv)` 前缀;`pip -V` 显示的路径在项目的 .venv 下。Day 01 说过"右下角是排错第一现场",从今天起它多了一层含义:不但要是对的版本,还要是对的房间。

---

# 上午 · 第二节(10:30 - 12:00)+ 下午第一节(14:00 - 15:00):异常处理

## 2.1 异常是什么:程序的"事故报告"

两周里你已经集齐了错误图鉴:SyntaxError(语法,运行前就拦)、NameError、TypeError、ValueError、IndexError、KeyError、FileNotFoundError、JSONDecodeError、RecursionError……**除 SyntaxError 外,这些都是"异常(Exception)":程序运行中发生的意外事件**。不处理,程序当场死亡并打印"讣告"(traceback);处理了,程序可以认错、补救、继续活。

```python
# 不处理的下场:
age = int("abc")          # ValueError: invalid literal for int()...
print("这行永远执行不到")   # 程序已死
```

## 2.2 try/except:接住异常

```python
# 基本形态:把"可能出事的代码"放进 try,出事了跳到 except
try:
    age = int(input("年龄:"))          # 可能 ValueError
    print(f"十年后你 {age + 10} 岁")
except ValueError:
    print("请输入数字!")               # 出事时的补救
print("程序继续活着")                    # 无论出没出事都会到这里
```

执行逻辑:try 块顺序执行 → 某行抛异常 → **该行之后的 try 内代码全部跳过** → 匹配的 except 接住处理 → 继续往下。没出事则 except 整块跳过。

**带着异常对象处理(as e)+ 多路捕获:**

```python
import json

def load_config(filename: str) -> dict:
    """读取 JSON 配置:演示多路 except。"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"配置文件 {filename} 不存在,使用默认配置")
        return {}
    except json.JSONDecodeError as e:              # as e:拿到异常对象
        print(f"配置文件格式坏了(第 {e.lineno} 行):{e.msg}")     # 异常对象带着案发详情
        return {}
    # 多个 except 像 elif:从上到下匹配,命中一个就走一个
```

**except 的匹配也认继承**(昨天的知识立刻复用):异常是一棵类树,`Exception` 是几乎所有异常的父类,所以 `except Exception` 能接住一切——**但这是双刃剑,马上讲**。

## 2.3 完整形态:else 与 finally

```python
try:
    f = open("data.json", "r", encoding="utf-8")
except FileNotFoundError:
    print("文件不存在")
else:
    # else:try 块"没出事"才执行——把"只有成功才该做的事"放这里,
    #       避免它们意外触发上面的 except(精确控制监控范围)
    data = f.read()
    print(f"读到 {len(data)} 字符")
finally:
    # finally:无论成功失败、甚至 try 里有 return,都必然执行——
    #          放"打扫战场"的动作:关文件、关网络连接、释放资源
    print("清理完毕")
```

四件套的分工口诀:**try 干活,except 救火,else 庆功,finally 打扫**。实战中 else 出场率不高(常被"把成功逻辑直接写在 try 末尾"替代),finally 的主战场(关资源)大多被 with 语句接管(明天文件课详讲 with 的原理),但语法必须认识——读别人代码时都会遇到。

## 2.4 raise 与自定义异常

Day 08 你已经会 raise 了,今天补全进阶姿势:

```python
# ── 自定义异常:继承 Exception,通常一行就够 ──
class APIError(Exception):
    """API 调用相关错误的基类。"""

class RateLimitError(APIError):
    """限流错误(可重试)。"""

class AuthError(APIError):
    """认证错误(重试也没用,该查 Key)。"""
# 为什么自定义?让调用方能"分门别类地接":
# except RateLimitError → 等一等重试;except AuthError → 提示查 Key。
# 用异常的类型传递"该怎么办"的信息——昨天"类型即角色"思想的异常版


def call_api_mock(key: str) -> str:
    """模拟 API:演示抛出自定义异常。"""
    if not key.startswith("sk-"):
        raise AuthError(f"API Key 格式错误: {key[:6]}...")
    return "调用成功"


# ── 接住后再抛:except 里裸 raise(原样上抛,常配日志) ──
try:
    call_api_mock("bad-key")
except AuthError:
    print("记录日志:认证失败……")
    raise                       # 裸 raise:把刚接住的异常原样再抛出去——
                                # "我记录一下,但这事我处理不了,上级继续处理"

# ── 异常链:raise ... from e(转译异常但保留原始案发现场) ──
def load_user(raw_json: str) -> dict:
    try:
        return json.loads(raw_json)
    except json.JSONDecodeError as e:
        # 把底层异常"转译"成业务异常,from e 保留因果链,
        # traceback 会显示"由下面这个异常直接导致"——两层案情都在
        raise APIError("用户数据损坏") from e
```

## 2.5 什么时候捕获,什么时候让它崩(全天最重要的一节)

语法五分钟就会,**判断力才是异常处理的真功夫**。三条军规:

**军规一:只捕获你能处理的。** "处理"意味着你有真正的对策:重试、用默认值、换条路、给用户友好提示。没有对策就别捕获,让它往上抛——上层也许有对策,实在没有就崩,崩比"带病运行"好。

**军规二:严禁"吞异常"。** 天下第一坏代码:

```python
try:
    do_everything()
except Exception:
    pass                    # ❌ 出了任何事都装没看见
# 后果:程序"看起来正常",数据早就坏了,三周后发现时已无案发现场。
# Day 02 说过"不报错的逻辑错误最危险",吞异常就是亲手制造它
```

如果真的需要"兜底不崩"(比如主循环),最低要求是**留下案底**:

```python
try:
    handle_request()
except Exception as e:
    print(f"[ERROR] 未预期的异常: {type(e).__name__}: {e}")     # 至少打出来
    # 真实项目用 logging 模块记录完整 traceback,Day 46 讲可观测性时升级
```

**军规三:捕获要具体,范围要小。** `except ValueError` 好于 `except Exception`(后者会把你没想到的 bug 也吞进"补救"分支);try 块只包住"真正可能出事的那几行",不要把两百行全塞进去(出事了都不知道是哪行的事)。

**EAFP:Python 的原生风格(Day 03 答疑的伏笔兑现)。** "先斩后奏"(Easier to Ask Forgiveness than Permission)vs "三思后行"(LBYL, Look Before You Leap):

```python
# LBYL:先检查再动手(Day 03 的 isdigit 就是它)
if text.isdigit():
    age = int(text)

# EAFP:直接干,出事再说——Python 社区更推崇
try:
    age = int(text)
except ValueError:
    age = None
# EAFP 的优势:① 覆盖完整(isdigit 拦不住 "1e5"、"²" 这些怪输入,int 自己最清楚
# 什么转不了);② 没有"检查和使用之间"的空窗(文件检查存在后、打开前被删了呢?)。
# 从今天起,类型转换类校验优先用 EAFP;业务规则类校验(年龄范围)继续用 if
```

## 2.6 给模型层穿铠甲(昨天钩子兑现)

```python
class DeepSeekModel(BaseChatModel):
    def chat(self, messages: list) -> str:
        """带异常处理的 chat(今天是模拟版铠甲,Day 12 保护真网络调用)。"""
        if not messages:
            raise ValueError("messages 不能为空")       # 编程错误:该崩就崩(军规一)
        try:
            reply = self._do_request(messages)          # 可能出事的只有这一行(军规三)
        except ConnectionError as e:
            # 网络错误:可处理(告知用户/触发重试),转译成业务异常上抛
            raise APIError(f"网络异常,请稍后重试: {e}") from e
        return reply
```

注意分层:**ValueError(调用方传错参,编程错误)直接 raise 不捕获;ConnectionError(环境问题)捕获并转译**。"错误分两种:代码写错了(崩,修代码)和世界不完美(接,做补救)"——这个区分标准比任何语法都值钱。

---

# 下午 · 第二节(15:10 - 17:30):实操——chatlib 包的诞生

## 3.1 需求文档

> ### 需求文档:chatlib 对话类库 v1.0(包化重构)
>
> **需求编号**:REQ-D10-001
> **需求方**:「智言科技」AI 平台组
> **背景**:第二周积累的类(ChatMessage/ChatSession/模型层)散落在单文件里,即将被 Day 12-14 的多个程序复用。要求重构为规范的 Python 包,并补齐异常体系。
>
> **包结构要求**:
> ```
> week2_project/                  ← 项目根目录
> ├── .venv/                      ← 虚拟环境(不进 Git)
> ├── .gitignore                  ← 至少含 .venv/ __pycache__/ *.json
> ├── requirements.txt            ← 目前为空清单,明天开始生长
> ├── chatlib/                    ← 包
> │   ├── __init__.py             ← 门面:转口常用类
> │   ├── exceptions.py           ← 异常体系(新增)
> │   ├── messages.py             ← ChatMessage / ChatSession(Day 08-09 成果迁入)
> │   └── models.py               ← 模型层(Day 09 成果迁入 + 穿铠甲)
> └── main.py                     ← 演示入口
> ```
>
> **功能要求**:
> 1. `exceptions.py`:ChatLibError(基类)→ APIError → RateLimitError / AuthError;InvalidMessageError;
> 2. `messages.py`:ChatMessage 构造校验改抛 InvalidMessageError;ChatSession.load 对"文件不存在/JSON 损坏"分路处理;
> 3. `models.py`:chat 空消息抛 ValueError;模拟网络层按 3.1 节分层处理;FakeModel 可注入"必失败模式"(为测试重试逻辑服务);
> 4. 每个模块带 `if __name__ == "__main__"` 自测;main.py 演示 from chatlib import 一步到位。
>
> **验收标准**:`python main.py` 从项目根目录运行全通;各模块单独运行自测全通;.gitignore 生效(git status 看不到 .venv 与 __pycache__)。

## 3.2 关键实现讲解(完整代码见 code/week2_project/)

**exceptions.py——异常也要有家谱:**

```python
"""chatlib 异常体系:用类型传递'该怎么办'。"""


class ChatLibError(Exception):
    """chatlib 所有异常的基类。使用方一网打尽:except ChatLibError。"""


class InvalidMessageError(ChatLibError):
    """消息构造不合法(role 非法/内容为空)。"""


class APIError(ChatLibError):
    """API 调用错误的基类。"""


class RateLimitError(APIError):
    """限流:可等待后重试。"""


class AuthError(APIError):
    """认证失败:重试无用,请检查 API Key。"""
```

家谱的价值在使用方的 except 里显形:

```python
try:
    model.chat(session.to_api_format())
except RateLimitError:
    time.sleep(5)                      # 限流:等等再来
except AuthError as e:
    print(f"请检查 API Key:{e}")       # 认证:提示后放弃
except ChatLibError as e:
    print(f"对话服务异常:{e}")         # 家谱兜底:其他 chatlib 错误统一友好提示
# 三层 except 从具体到宽泛排列——elif 的"从严到宽"守则在异常上重演
```

**`__init__.py`——门面:**

```python
"""chatlib:课程自研对话类库(Day 10 出生,Day 14 服役,Day 25 交棒 LangChain)。"""
from chatlib.exceptions import ChatLibError, APIError, RateLimitError, AuthError, InvalidMessageError
from chatlib.messages import ChatMessage, ChatSession
from chatlib.models import BaseChatModel, DeepSeekModel, FakeModel

__all__ = [
    "ChatLibError", "APIError", "RateLimitError", "AuthError", "InvalidMessageError",
    "ChatMessage", "ChatSession",
    "BaseChatModel", "DeepSeekModel", "FakeModel",
]
```

**main.py——使用方的爽感验收:**

```python
"""chatlib 演示入口:体验包化后的使用体验。"""
from chatlib import ChatSession, DeepSeekModel, FakeModel, ChatLibError
# ↑ 一行拿到所有主角:__init__.py 门面的功劳


def main() -> None:
    session = ChatSession("包化演示", system_prompt="你是助教")
    model = FakeModel("fake")               # 开发期用假模型:不花钱

    for question in ["什么是包?", "什么是异常?"]:
        session.add_user(question)
        try:
            reply = model.chat(session.to_api_format())
        except ChatLibError as e:           # 家谱一网打尽
            reply = f"(服务异常:{e})"
        session.add_assistant(reply)

    session.show()


if __name__ == "__main__":
    main()
```

## 3.3 .gitignore:哪些东西不进 Git

```
# week2_project/.gitignore
.venv/              # 虚拟环境:几百 MB 的库文件,别人用 requirements.txt 重建
__pycache__/        # Python 的字节码缓存:机器生成,永远不进版本库
*.pyc
contacts.json       # 运行时产生的数据文件(视项目而定)
.env                # 【预告】Day 13 起最重要的一行:API Key 所在,泄露=盗刷
```

原则:**源代码进 Git,"可再生的"和"含秘密的"不进**。`.env` 这行今天先写上,Day 13 你会感谢这个习惯。

---

# 【常见错误与排错手册】Day 10 专属篇

**错误 1:`ModuleNotFoundError: No module named 'chatlib'`。** 三大原因:①运行位置不对——必须从**项目根目录**(chatlib 的上一级)运行 `python main.py`;②包里缺 `__init__.py`;③装了库但激活的是另一个虚拟环境(pip -V 查房间)。

**错误 2:`ImportError: cannot import name 'X' from 'chatlib'`。** X 没在 `__init__.py` 转口,或模块里根本没定义它(拼写!)。

**错误 3:循环导入(circular import)。** a.py import b,b.py 又 import a → `ImportError: cannot import name ... (most likely due to a circular import)`。病根是职责划分不清。解法:把共同依赖的东西抽到第三个模块(我们把异常单独放 exceptions.py,正是为了让 messages 和 models 都能安全地 import 它而互不 import)。

**错误 4:改了模块代码,重新 import 不生效。** 模块只执行一次(缓存)。交互模式里改完代码要重启解释器;正常"改完重新运行脚本"不受影响。

**错误 5:except 顺序写反,具体异常永远接不到。** `except Exception` 写在 `except ValueError` 前面 → 一切都被前者拦截。**从具体到宽泛排列**(编译器不报错,全靠自觉)。

**错误 6:`except ValueError, KeyError:` 老语法。** Python 3 多类型捕获必须打包成元组:`except (ValueError, KeyError):`。

**错误 7:finally 里 return 吞掉异常。** finally 中写 return 会把正在传播的异常直接抹掉——语言的阴暗角落,记住"finally 只打扫,不 return"。

**错误 8:自定义异常忘继承 Exception。** `class MyError:` 裸类 → `raise MyError()` 报 "exceptions must derive from BaseException"。必须 `class MyError(Exception):`。

---

# 【课堂笔记】Day 10 知识点速查表

**模块与包**
- 模块 = .py 文件;包 = 含 `__init__.py` 的文件夹;import 时**执行**模块(仅一次,后走缓存)
- 三种导入:`import m`(稳)/ `from m import x`(常用)/ `from m import *`(禁)
- `__name__`:直接运行 = `"__main__"`,被 import = 模块名 → 守门自测代码
- 模块顶层只放 import/常量/定义;有动作的代码进函数
- `__init__.py` 门面转口:`from chatlib import ChatMessage` 的幕后
- 循环导入:抽公共依赖到第三模块(exceptions.py 的站位理由)

**虚拟环境**
- `python -m venv .venv` → 激活(Win: `.venv\Scripts\activate` / mac: `source .venv/bin/activate`)→ 提示符带 (.venv)
- `pip freeze > requirements.txt`(进 Git);`pip install -r requirements.txt` 复原
- .venv 不进 Git;VS Code 右下角选对房间

**异常四件套**:try 干活,except 救火,else 庆功,finally 打扫
- `except XxxError as e`:拿到异常对象;多 except **从具体到宽泛**
- 多类型:`except (A, B):`;裸 `raise` 原样上抛;`raise X from e` 转译保因果
- 自定义:继承 Exception 建家谱;用类型传递"该怎么办"

**三条军规**:①只捕获能处理的 ②严禁吞异常(至少留案底)③捕获具体、try 块小
**EAFP**:先斩后奏,类型转换首选;业务规则校验仍用 if
**错误二分法**:代码写错了 → 崩(修代码);世界不完美 → 接(补救)

---

# 【附录】课堂答疑实录(晚自习整理)

**问 1:__pycache__ 文件夹是什么?能删吗?**

答:Python 把模块编译成字节码(.pyc)缓存在这里,下次 import 提速。能删,会自动重建;永远不进 Git(今天 .gitignore 里写了)。看到它出现,反而说明你的模块被 import 过——一个无害的脚印。

**问 2:import 放文件中间行不行?我见过函数里写 import 的。**

答:语法允许,规范不许(PEP 8:import 集中在文件顶部,顺序为标准库 → 第三方 → 自家模块,三组间空行)。函数内 import 有两个正当例外:①打破循环导入的应急手段;②重量级库的延迟加载(用到才 import,加快启动)。没有这两种理由就是坏风格。

**问 3:venv 和 conda 到底用哪个?**

答:本课程前 50 天统一 venv(标准库自带、轻量、够用)。conda 的优势在"连非 Python 的依赖(CUDA、编译器)一起管",所以 Day 51 起的 GPU 微调环境会用它(AutoDL 镜像预装)。两者心智模型相同:建房间→进房间→装东西→记清单。会一个,另一个看五分钟文档就会。

**问 4:except Exception 真的一次都不能写吗?课件自己也写了。**

答:能写,但只在两个位置:①**程序的最外层兜底**(主循环/服务入口),防止一个意外把整个服务打死,且必须记录完整日志;②**批处理循环内**(处理 1000 个文档,一个坏文档不该终止全部),同样必须记录哪个坏了为什么坏。共同点:都在"边界"上,都留案底。在业务逻辑深处写 except Exception,就是把 bug 藏进地毯。

**问 5:raise APIError(...) from e 和不写 from e 有什么实际区别?**

答:traceback 的完整度。带 from e:报错时显示两段案情,"底层的 JSONDecodeError 直接导致了上层的 APIError",排查时能看到最初的案发现场;不带:只剩上层异常,底层线索断了。成本是六个字符,收益是排错半小时,转译异常时永远带上 from e。

**问 6:为什么错误要分"编程错误"和"环境错误"?都是错,都得修啊。**

答:因为**修的人和修的方式完全不同**。编程错误(传空 messages、拼错键名)= 开发者的锅,正确响应是"大声崩溃 + 修代码",任何"补救"都是掩盖;环境错误(断网、限流、文件被占)= 世界的锅,代码没毛病,正确响应是"重试/降级/友好提示",崩溃反而是失职。写每个 try 之前问一句"这错是谁的锅",答案就决定了姿势。这个二分法是异常处理判断力的心脏,比全部语法加起来都重要。

**问 7:chatlib 这个包 Day 25 就要被 LangChain 替代,现在花一下午造它值吗?**

答:值,三笔账:①**能力账**——包结构、异常体系、门面模式的手艺,换任何框架都带得走,这是"造轮子学原理"的经典路径;②**理解账**——Day 25 你看 LangChain 的 BaseChatModel、它的异常层次、它的 __init__.py,每一样都"似曾相识",学习成本骤降(我们反复说的"发明过再学习");③**面试账**——"我自己实现过一个支持多厂商、带异常体系的模型抽象层"是比"我会用 LangChain"高一档的叙事。工具会过时,造过工具的人不会。

**问 8:明天学文件操作,和今天的 load_config 那些有什么不同?**

答:今天你是"照抄使用"文件读写(Day 07 的模板函数、今天的 with open),明天正式拆解:open 的模式(r/w/a/rb)、with 上下文管理器的原理(它就是 try/finally 的语法糖——今天的 finally 知识直接派上用场)、编码问题(UTF-8 vs GBK 乱码之谜)、pathlib 的现代路径操作,以及 os/datetime/re 一批标准库。明天结束后,Day 07 那两个"模板函数"的每一行你都能讲出所以然,而且能批量处理整个文件夹的文档——RAG 文档处理(Day 28)的前置技能正式点亮。

---

# 【明日预告】Day 11:文件操作与常用标准库

明天是第一阶段的"杂项装备日",也是含金量极高的一天:上午——文件读写全解(txt/csv/json、with 原理、UTF-8 编码之谜),Day 07 模板函数转正;下午——标准库四大金刚:os/pathlib(路径与批量文件)、datetime(时间戳翻译官,Day 05 彩蛋兑现)、random、**re 正则表达式入门**(Day 02 手机号提取"完美方案"的兑现)。实操:**批量文档读取与关键词统计工具**——扫描整个文件夹的文本文件,统计词频,输出报告。这是 RAG 文档处理流水线(Day 28)的第一块真实积木。

**睡前自检清单**:
- [ ] 能解释 `if __name__ == "__main__"` 的原理(考完这个四天悬案就翻篇)
- [ ] venv 三连(创建/激活/freeze)能盲打
- [ ] 三条军规 + 错误二分法能复述
- [ ] week2_project 包结构搭建完成,main.py 与各模块自测全通
- [ ] LeetCode:LC 20(有效的括号——栈的应用)、LC 125(验证回文串)
- [ ] 作业完成并 push,绿格子连续第 10 天
