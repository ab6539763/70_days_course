# Day 12:网络请求与 API 调用 —— 首次连接大模型的"魔法时刻"(关键日!)

---

# 【旁白解读】十一天的积木,今天合体点火

请允许我用一分钟盘点你此刻的装备,因为今天是它们集体上岗的日子:

- Day 01 的 f-string → 今天组装 Prompt;
- Day 03 的主循环 + 分发器 → 今天问答小程序的骨架;
- Day 04/05 的 messages 字典列表、"第一名句" `data["choices"][0]["message"]["content"]` → 今天解析**真实**响应;
- Day 05 的请求体 JSON(Day 05 下午你彩排过一字不差的版本)→ 今天**真实发出**;
- Day 09 的 DeepSeekModel(chat 里是模拟代码)→ 今天换上**真引擎**,接口纹丝不动;
- Day 10 的异常军规、Day 11 的 os.environ 预告 → 今天保护真实调用和真实的 Key。

**今天缺的只有一样:把 JSON 从你的电脑送到 api.deepseek.com 的"网线"。** 这根网线分两段:上午学 HTTP 协议(网线的语言)和 requests 库(Python 的网线接口);下午接通大模型,写出你的第一个真 AI 程序。

一个心理预期管理:今天下午当终端里第一次打印出大模型的真实回答时,请允许自己激动十秒钟——那是你 12 天、约 80 小时投入的第一次"通电"。然后冷静下来,因为工程师的工作从"能跑"才刚刚开始。

---

# 上午 · 第一节(9:00 - 10:20):HTTP 协议基础 —— 用"寄快递"一次讲穿

## 1.1 请求与响应:一来一回的快递

你每天都在用 HTTP(浏览器打开任何网页、App 的每一次刷新),它是"客户端向服务器要东西"的通信规则。全部核心概念用一张快递单讲完:

```
【HTTP 请求 = 你寄出的快递】
  请求方法(Method)   = 快递类型:GET 是"取件"(向服务器要数据)
                                POST 是"寄件"(向服务器送数据,大模型 API 用它)
  URL                = 收件地址:https://api.deepseek.com/chat/completions
  请求头(Headers)    = 快递单上的备注栏:
                         Content-Type: application/json   ← "箱子里装的是 JSON"
                         Authorization: Bearer sk-xxx     ← "我的会员卡号"(API Key!)
  请求体(Body)       = 箱子里的货:{"model": ..., "messages": [...]}
                        (GET 通常没有 Body;POST 的数据主要放这里)

【HTTP 响应 = 服务器寄回的快递】
  状态码(Status Code)= 签收回执:三位数字,一眼判断这单成没成
  响应头              = 回件的备注栏(内容类型、限流信息等)
  响应体              = 回件的货:大模型 API 场景就是 Day 05 解析过的那份 JSON
```

## 1.2 状态码:先记一个规律,再记六个常客

规律:**2xx 成功,3xx 转移,4xx 你的错,5xx 它的错**。六个常客(大模型 API 场景):

| 状态码 | 含义 | 大模型 API 场景的典型原因 | 你该怎么办 |
|--------|------|--------------------------|-----------|
| 200 | 成功 | 正常拿到回答 | 解析响应 |
| 400 | 请求有误 | 请求体 JSON 格式错/参数非法 | 修代码(你的锅) |
| 401 | 未认证 | API Key 错误/没带 | 查 Key(你的锅) |
| 402 | 余额不足 | 账户没钱了 | 充值 |
| 429 | 请求太频繁 | 触发限流 | **等待后重试**(唯一"重试有用"的 4xx) |
| 500/503 | 服务器错误/过载 | 服务方故障 | 稍后重试(它的锅) |

注意 429 和 401 的分野正好对应 Day 10 的异常家谱:RateLimitError(可重试)和 AuthError(重试无用)——**当时凭空设计的两个异常类,原型就是这两个状态码**。伏笔从来不是白埋的。

## 1.3 URL 的解剖(顺手补全)

```
https://api.deepseek.com/chat/completions?debug=1
└─┬──┘ └──────┬───────┘└───────┬───────┘ └──┬──┘
 协议      域名(哪台服务器)   路径(要哪个服务)   查询参数(?key=value,GET 常用)
```

大模型 API 的路径 `/chat/completions`(聊天补全)是 OpenAI 定下的事实标准,DeepSeek、Moonshot、通义等全部兼容——**这就是为什么 Day 09 的多态设计现实可行:大家连 URL 结构都长一样**。

---

# 上午 · 第二节(10:30 - 12:00):requests 库详解

## 2.1 安装与第一个请求

```bash
# 在 week2_project 的虚拟环境里(Day 10 的房间,Day 11 作业已装过的举手)
pip install requests
pip freeze > requirements.txt        # 清单立刻更新:Day 10 的纪律
```

```python
import requests

# GET:向一个公开测试接口"取件"
response = requests.get("https://httpbin.org/get", timeout=10)
# httpbin.org:专门用来练习 HTTP 的公益网站,会把你发的请求原样描述给你看

print(response.status_code)      # 200
print(type(response.text))       # <class 'str'>   响应体的原始文本
data = response.json()           # 快捷方法:等价于 json.loads(response.text)!
print(type(data))                # <class 'dict'>  Day 05 的知识直接接轨
```

`response.json()` 值得专门看一眼:**你以为要写的 `json.loads(response.text)`,requests 帮你包好了**。Day 05 苦练的解析功夫没有白费——你知道糖衣底下是什么。

## 2.2 POST:寄出一个 JSON

```python
import requests

payload = {"name": "张三", "question": "什么是HTTP?"}

response = requests.post(
    "https://httpbin.org/post",
    json=payload,               # ★ json= 参数:三合一的语法糖——
                                #   ①自动 json.dumps(payload)
                                #   ②自动加请求头 Content-Type: application/json
                                #   ③编码处理
    timeout=10,                 # ★ 超时(秒):没有它,服务器不回话你就永远等下去
)
print(response.status_code)
print(response.json()["json"])       # httpbin 会把你寄的货原样放在 "json" 字段里回显
```

**timeout 是纪律不是选项。** 不设超时的网络请求 = 可能永远卡住的程序(Day 03 的死循环的网络版,连 Ctrl+C 都要等它先醒)。课程规定:**每个 requests 调用必带 timeout**,普通接口 10 秒,大模型接口 60 秒(生成长文确实慢)。

## 2.3 请求头与错误处理

```python
headers = {
    "Authorization": "Bearer sk-你的Key",       # 认证头:Bearer + 空格 + Key(格式铁律)
    "Content-Type": "application/json",         # 用 json= 参数时可省略,显式写不亏
}
response = requests.post(url, headers=headers, json=payload, timeout=60)

# ── 错误处理的标准三层(Day 10 军规的网络落地) ──
try:
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()          # ★ 状态码非 2xx 时抛 requests.HTTPError
                                         #   (不写这句,4xx/5xx 不报错,静默拿到错误 JSON!)
    data = response.json()               # 可能抛 JSONDecodeError(响应不是 JSON 时)
except requests.Timeout:
    print("请求超时,稍后重试")            # 环境错误:接住补救
except requests.ConnectionError:
    print("网络不通,检查网络")            # 环境错误:接住补救
except requests.HTTPError as e:
    print(f"HTTP 错误:{e.response.status_code}")     # 分状态码处置(429 重试/401 查 Key)
```

`raise_for_status()` 是新手最容易漏的一行:**requests 认为"服务器回了话"就算成功,哪怕回的是 401**。不调用它,你会拿着一份错误 JSON 去执行"第一名句",然后 KeyError 崩在离真相很远的地方。

---

# 下午 · 第一节(14:00 - 15:30):首次调用大模型 API 🎉

## 3.1 行前检查:API Key 的领取与保管

昨天作业布置的注册,现在验收:platform.deepseek.com → API Keys → 创建。三条保管纪律,**每条都有血泪案底**:

1. **Key 只显示一次**,创建时立即复制保存;
2. **绝不写死在代码里**(下一节先临时用环境变量,Day 13 转正为 .env 方案);
3. **绝不进 Git**——GitHub 上有爬虫 7×24 小时扫描泄露的 Key,泄露到被盗刷的时间以分钟计。Day 10 的 .gitignore 里那行 `.env`,就是为今天准备的。

临时方案(今天课堂用):把 Key 存进**环境变量**——Day 11 预告的 `os.environ` 上岗:

```bash
# Windows PowerShell(当前窗口有效):
$env:DEEPSEEK_API_KEY = "sk-你的key"
# macOS / Linux:
export DEEPSEEK_API_KEY="sk-你的key"
```

```python
import os
api_key = os.environ.get("DEEPSEEK_API_KEY")     # 环境变量也是个字典!get 防御(Day 05 心法)
if not api_key:
    raise RuntimeError("未设置 DEEPSEEK_API_KEY 环境变量,请先配置")
```

## 3.2 历史性的三十行:第一次真实调用

```python
# =============================================
# first_call.py —— 你与大模型的第一次真实通话
# 每一行都是过去 12 天的某一课,注释里标了出处
# =============================================
import os
import requests

API_URL = "https://api.deepseek.com/chat/completions"       # 常量(Day 01)
api_key = os.environ.get("DEEPSEEK_API_KEY")                 # 环境变量(Day 11/12)
if not api_key:
    raise RuntimeError("请先设置 DEEPSEEK_API_KEY")           # 该崩就崩(Day 10)

headers = {"Authorization": f"Bearer {api_key}"}             # f-string 组装认证头(Day 01)

payload = {                                                  # 请求体:Day 05 彩排过的原件
    "model": "deepseek-chat",
    "messages": [
        {"role": "system", "content": "你是一个乐于助人的AI助手"},
        {"role": "user", "content": "用一句话告诉我,学会调用大模型API意味着什么?"}
    ],
    "temperature": 0.7,
    "stream": False,
}

response = requests.post(API_URL, headers=headers, json=payload, timeout=60)   # 今天的新零件
response.raise_for_status()                                  # 非 2xx 即报警(今天)
data = response.json()                                       # str → dict(Day 05)

content = data["choices"][0]["message"]["content"]           # 第一名句(Day 05)
usage = data.get("usage", {})                                # 可选字段 get 防御(Day 05)

print("AI 说:", content)
print(f"消耗 token:{usage.get('total_tokens', 0)}")
```

运行。等待两三秒。然后——**屏幕上出现了大模型认真回答你的那句话**。花十秒钟体会一下:12 天前你连变量都不会声明,现在你和世界上最先进的 AI 系统完成了一次程序级对话,而且**这段代码里没有一行是你不理解的**。

## 3.3 冷静复盘:刚才到底发生了什么

```
你的程序                        DeepSeek 服务器(云端 GPU 集群)
   │                                   │
   │ ① requests.post:                  │
   │   把 payload dumps 成 JSON,       │
   │   带上 Key,经互联网寄出            │
   │──────────────────────────────────►│
   │                                   │ ② 验 Key → 排队 → 模型推理
   │                                   │    (你的 messages 被 token 化,
   │                                   │     逐 token 生成回答)
   │ ③ 收到响应 JSON:                   │
   │◄──────────────────────────────────│
   │ ④ response.json() 解析             │
   │ ⑤ 第一名句取出 content              │
   ▼
 print 给用户
```

三个当堂实验,把理解砸实:

```python
# 实验 1:把 Key 改错一个字母再跑 → 401,raise_for_status 抛 HTTPError
#         (亲眼见一次 401,比读十遍表格记得牢)
# 实验 2:把 "messages" 拼成 "message" → 400(你的锅,4xx)
# 实验 3:注释掉 raise_for_status,再用错 Key 跑 → KeyError: 'choices'
#         (体会"漏了这行,错误在离真相很远的地方爆炸")
```

## 3.4 封装进 chatlib:模拟引擎换真引擎(Day 09 架构的兑现日)

```python
# chatlib/models.py 中 DeepSeekModel 的升级——只动 _do_request 一个方法!
import os
import requests
from chatlib.exceptions import APIError, AuthError, RateLimitError


class DeepSeekModel(BaseChatModel):
    """DeepSeek 模型:今天起是真引擎。"""

    API_URL = "https://api.deepseek.com/chat/completions"

    def __init__(self, model_name: str = "deepseek-chat", temperature: float = 0.7,
                 api_key: str = None):
        super().__init__(model_name, temperature)
        # Key 的来源顺序:参数显式传入 > 环境变量(Day 13 会插入 .env 一层)
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY", "")
        if not self.api_key:
            raise AuthError("未提供 API Key(参数或 DEEPSEEK_API_KEY 环境变量)")

    def _do_request(self, messages: list) -> str:
        """真实网络请求:Day 09 的模拟代码退役,方法名和职责不变。"""
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": self.temperature,
            "stream": False,
        }
        try:
            resp = requests.post(
                self.API_URL,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=payload,
                timeout=60,
            )
        except requests.Timeout as e:
            raise APIError("请求超时") from e                    # 转译 + from e(Day 10)
        except requests.ConnectionError as e:
            raise APIError("网络连接失败") from e

        # 状态码分诊:对应 Day 10 的异常家谱
        if resp.status_code == 401:
            raise AuthError("API Key 无效,请检查")
        if resp.status_code == 429:
            raise RateLimitError("触发限流,请稍后重试")
        if resp.status_code != 200:
            raise APIError(f"API 返回 {resp.status_code}: {resp.text[:200]}")

        data = resp.json()
        usage = data.get("usage", {})
        self._record(tokens=usage.get("total_tokens", 0))       # 真实用量记账!
        return data["choices"][0]["message"]["content"]

    def chat(self, messages: list) -> str:
        """对外接口:与 Day 09 一字不差。"""
        if not messages:
            raise ValueError("messages 不能为空")
        return self._do_request(messages)
```

**看清这次升级动了什么、没动什么**:动了——_do_request 的内部(模拟 → requests);没动——chat 的签名、BaseChatModel、FakeModel、以及所有调用方代码。`run_demo(DeepSeekModel())` 昨天怎么跑今天还怎么跑,只是回答从假的变成了真的。**这就是 Day 09 那句"接口纹丝不动"的兑现,也是你第一次亲身收获架构设计的复利。**

---

# 下午 · 第二节(15:40 - 17:30):实操——命令行 AI 问答小程序 🎉

## 4.1 需求文档

> ### 需求文档:命令行 AI 问答小程序 v1.0
>
> **需求编号**:REQ-D12-001
> **背景**:chatlib 已接通真引擎,做一个最小可用的问答程序验证全链路。**注意:本程序是"单轮问答"——每个问题独立发送,AI 不记得上一问**(多轮记忆是 Day 14 项目一的主菜,今天故意不做,体会"没有记忆"的痛)。
>
> **功能需求**:
> 1. 启动时自检:环境变量有 Key 才继续,没有则给出配置指引后退出;
> 2. 主循环:输入问题 → 调用 → 打印回答;空输入跳过;/exit 退出;
> 3. 每轮显示:回答、本轮 token 消耗、累计成本估算(输入 1 元/百万、输出 2 元/百万,以官网为准);
> 4. 异常处理:限流自动等 3 秒重试一次;认证错误提示后退出;其他 API 错误提示后继续下一轮;Ctrl+C 优雅退出(捕获 KeyboardInterrupt,道别后退出而不是抛一屏 traceback);
> 5. 开发模式:命令行参数 `--fake` 用 FakeModel(不花钱调试全流程——Day 09 测试替身的承诺兑现)。
>
> **验收标准**:真实问答全链路通;/exit、空输入、Ctrl+C、错误 Key、断网(手动关 WiFi 测)全部优雅处置。

## 4.2 参考实现(核心逻辑,完整见 code/qa_app.py)

```python
def main() -> None:
    """入口:单轮问答主循环。"""
    use_fake = "--fake" in sys.argv                 # 最朴素的命令行参数解析

    try:
        model = FakeModel() if use_fake else DeepSeekModel()
    except AuthError:
        print("未检测到 API Key。请先设置环境变量:")
        print('  PowerShell:  $env:DEEPSEEK_API_KEY = "sk-..."')
        print('  macOS/Linux: export DEEPSEEK_API_KEY="sk-..."')
        return                                       # 给出路,不给 traceback

    print(f"AI 问答小程序(模型:{model.model_name})  /exit 退出")
    total_tokens = 0

    while True:                                      # Day 03 的骨架,第 N 次上岗
        try:
            question = input("\n你问:").strip()
        except KeyboardInterrupt:                    # Ctrl+C:优雅道别
            print("\n再见!")
            break

        if not question:
            continue
        if question == "/exit":
            print("再见!")
            break

        # ── 单轮:每次都是全新的 messages(没有记忆——故意的痛点) ──
        messages = [
            {"role": "system", "content": "你是一个简洁的AI助手,回答不超过150字"},
            {"role": "user", "content": question},
        ]

        try:
            answer = model.chat(messages)
        except RateLimitError:
            print("(被限流,3 秒后自动重试……)")
            time.sleep(3)
            try:
                answer = model.chat(messages)        # 重试一次(Day 13 用装饰器优雅化)
            except ChatLibError as e:
                print(f"重试仍失败:{e}")
                continue
        except AuthError as e:
            print(f"认证失败:{e}")
            break                                    # Key 坏了,继续也没意义
        except ChatLibError as e:
            print(f"服务异常:{e},请重试")
            continue

        # ── 展示与记账 ──
        used = model.count_usage()["tokens"] - total_tokens
        total_tokens = model.count_usage()["tokens"]
        cost = total_tokens / 1_000_000 * 1.5        # 粗略均价估算(Day 01 成本课变现)
        print(f"\nAI 答:{answer}")
        print(f"(本轮 {used} tokens,累计 {total_tokens} tokens ≈ {cost:.4f} 元)")
```

## 4.3 体验作业(当堂完成):亲手撞一次"没有记忆"的墙

跑起来后,连续问两句:①"我叫小林,是转行学大模型的";②"我叫什么名字?"——AI 会一脸无辜地表示不知道。**因为每一轮我们都新建 messages,上一轮的对话根本没有发过去。** 这堵墙就是 Day 14 项目一要拆的:把 messages 从"每轮新建"改成"持续 append"(Day 04 就练过的动作),AI 就有了记忆。今天故意让你先痛一次——需求从痛点里长出来,是这门课不变的教法。

---

# 【常见错误与排错手册】Day 12 专属篇

**错误 1:401 Unauthorized。** Key 错/过期/没带。检查:环境变量拼写(DEEPSEEK_API_KEY)、Key 前后有没有混入空格引号、认证头格式 `Bearer + 空格 + Key`。注意:**新开的终端窗口读不到旧窗口设置的临时环境变量**——今天最高频的坑,重设一遍即可(Day 13 的 .env 根治)。

**错误 2:requests.exceptions.ConnectionError / Max retries exceeded。** 网络不通:检查 WiFi/代理;公司内网可能要配代理。另注意 URL 拼写(api.deepseek.com,别把 https:// 打成 http:.//)。

**错误 3:漏了 raise_for_status(或状态码分诊),KeyError: 'choices' 在下游爆炸。** 服务器回的是错误 JSON(如 `{"error": {...}}`),没有 choices。先看 `resp.status_code` 和 `resp.text`,再谈解析。

**错误 4:没设 timeout,程序卡死。** 表现:一直不动,Ctrl+C 也迟钝。每个 requests 必带 timeout=60。

**错误 5:`json=payload` 写成 `data=payload`。** data= 发的是表单格式,不是 JSON,服务器回 400。大模型 API 一律 `json=`。

**错误 6:环境变量在代码里 print 出来调试,顺手提交 Git。** Key 就这样泄露的。调试时只打印 `key[:6] + "..."`(Day 02 作业练过的脱敏!),且检查 .gitignore。

**错误 7:429 后疯狂手动重跑,越限越死。** 限流的正确姿势是**等待**(3-5 秒起步),明天的重试装饰器会带"指数退避"(每次失败等待翻倍)。

**错误 8:免费额度耗尽(402)。** 查 platform 后台用量;开发调试期间多用 `--fake`(FakeModel),真实调用留给验收——省钱习惯从第一天养成。

---

# 【课堂笔记】Day 12 知识点速查表

**HTTP 快递模型**
- 请求:方法(GET 取/POST 寄)+ URL + Headers(Content-Type、Authorization)+ Body(JSON)
- 响应:状态码 + Headers + Body
- 状态码:2xx 成 | 4xx 你的错(400 参数/401 Key/402 欠费/429 限流=唯一可重试)| 5xx 它的错(可重试)

**requests 四件套**
- `requests.post(url, headers=..., json=payload, timeout=60)`——json= 三合一糖;**timeout 必带**
- `resp.status_code` / `resp.text` / `resp.json()`(= json.loads(resp.text))
- `resp.raise_for_status()`:非 2xx 抛 HTTPError——**不写会静默拿到错误 JSON**
- 异常:Timeout / ConnectionError / HTTPError → Day 10 家谱转译

**API Key 三纪律**:只显示一次立即存 | 不写死代码 | 不进 Git(临时:os.environ;明天:.env)

**首次调用五步**:组 payload → post → raise_for_status/分诊 → resp.json() → 第一名句
**状态码分诊 → 异常家谱**:401→AuthError | 429→RateLimitError | 其他→APIError

**架构复利**:只换 _do_request 内部,chat 接口/调用方/FakeModel 全部不动
**单轮 vs 多轮**:今天每轮新建 messages(无记忆);Day 14 改成持续 append(有记忆)

---

# 【附录】课堂答疑实录(晚自习整理)

**问 1:为什么用 DeepSeek 不用 OpenAI?**

答:课程决策三因素:①**可及性**——DeepSeek 国内直连、注册即送额度、支付方便;OpenAI 在国内访问和支付都有门槛;②**兼容性**——DeepSeek 完全兼容 OpenAI 的 API 格式,你学的每一行代码换个 URL 和 Key 就能调 OpenAI,能力无损迁移;③**成本**——课程 50 天的 API 实验,DeepSeek 的价格让"每人几十块钱跑完全程"成为可能。技术上你今天已经看到了:多态架构下,换厂商是一行代码的事。

**问 2:openai 官方 SDK(`from openai import OpenAI`)和我们手写 requests,该用哪个?**

答:都要会,分工不同。SDK 是"精装修":`client.chat.completions.create(...)` 一行搞定,自动重试、类型提示齐全,**生产首选**;手写 requests 是"毛坯房",让你看见每根管线——今天先学毛坯,是因为 SDK 一旦报错(代理问题、版本冲突、流式异常),不懂底层的人只能干瞪眼。Day 16 起课程会引入 openai SDK(它也兼容 DeepSeek,base_url 一改即可),届时你会发现 SDK 的每个参数都能对应到今天的某一行。先懂毛坯再住精装,抛锚不慌。

**问 3:API Key 泄露真有那么严重?**

答:真实事故链:Key 推到 GitHub 公开仓库 → 爬虫分钟级抓取 → 被人拿去跑批量任务 → 你的额度/余额清零,甚至产生欠费。防御纵深:①.gitignore 挡住 .env(Day 10 已设);②Key 定期轮换(平台后台可作废重发);③设置用量告警(platform 后台有);④万一泄露,**立刻作废**该 Key 而不是抱侥幸。公司里 Key 泄露是要写事故报告的级别,从第一天就用对姿势。

**问 4:temperature 这些参数今天没讲,先用 0.7 对吗?**

答:对,0.7 是通用起点。今天刻意只讲"通不通",参数调优是 Day 16 的整天内容(temperature/top_p/max_tokens 逐一做对比实验)。预告一个感受:把 temperature 改成 0 再问同一个问题两次,回答几乎一样;改成 1.5,每次都放飞——后天亲手玩。

**问 5:为什么我的回答和同桌的不一样?我们问的问题一模一样。**

答:因为生成是**采样**过程:模型对下一个词给出概率分布,按概率抽签(temperature 控制抽签的"胆量")。同题不同答是特性不是 bug。这带来一个工程难题:输出不确定,怎么写测试?(Day 09 答疑说过:FakeModel 测流程,真模型测试要用"评估"而不是"断言"——Day 34 的主题。)也带来一个 Prompt 技巧:要稳定输出就调低 temperature 并约束格式(Day 17/18)。

**问 6:今天单轮问答每轮都发 system 消息,这不浪费 token 吗?**

答:是的,system 每轮都算输入 token。但这是单轮架构的固有成本,省不掉(不发 system,模型就没了人设约束)。Day 14 多轮架构下 system 只在 messages 开头出现一次,但**每轮请求仍会整体重发全部历史**(HTTP 无状态:服务器不记得你上一单快递)——所以多轮的 token 消耗是累进的,这就是 Day 04 思考题"对话历史无限增长"的成本真相,也是 Day 27 记忆压缩的存在理由。API 计费的世界里,token 就是钱,这个意识越早越好。

**问 7:能不能同时问好几个问题,并发调用加速?**

答:能,而且是生产刚需(批量处理文档摘要等场景)。方案有三档:多线程、异步 asyncio(Day 13 入门)、批量 API。但今天先不碰:并发会放大一切问题(限流更快触发、错误更难排查),先把单请求的每个环节走稳。Day 13 的 asyncio 入门会演示"同时发 3 个请求",Day 46 讲成本与延迟优化时系统展开。

**问 8:实验 3 里注释掉 raise_for_status 后,报错是 KeyError: 'choices',如果我真的在生产遇到这种错,排查思路是什么?**

答:标准思路四步:①**看完整 traceback**——定位是哪行的 KeyError;②**打印上游原料**——`print(resp.status_code, resp.text[:500])`,十有八九发现是 401/429 的错误 JSON;③**补上分诊**——status_code 检查本就该在解析之前;④**复盘为什么漏了**——通常是"先写了 happy path 忘了回来补防御"。教训沉淀成习惯:**任何外部数据(API 响应/文件/用户输入)在使用前必须先验明正身**,这是 Day 05 get 心法、Day 10 军规、今天 raise_for_status 的共同精神。

---

# 【明日预告】Day 13:进阶语法与异步入门

明天是项目一冲刺前的最后一个知识日,四样装备:①**装饰器**——Day 09 的 RetryWrapper(类版)升级为 @retry(函数版),一行给 chat 加上"指数退避重试";Day 06 思考题的闭包正式变现;②**生成器与 yield**——"边生产边交付"的机制,Day 24 流式输出的语法基础;③**typing 类型注解进阶**——list[dict]、Optional 这些写法系统化;④**python-dotenv**——.env 文件管理 API Key 的正规军方案,今天环境变量"新窗口就失效"的痛,明天根治。实操:给 chatlib 完成"重试 + 超时 + .env"三件套武装——项目一的全部零件到位。

**睡前自检清单**:
- [ ] 第一次真实调用成功,回答截图留存(纪念意义 + 作品集素材)
- [ ] 三个当堂实验(401/400/漏 raise_for_status)都亲手跑过
- [ ] 状态码六常客 + 分诊到异常家谱的映射能默写
- [ ] qa_app.py 全部验收项通过(含 --fake 模式和 Ctrl+C)
- [ ] LeetCode:LC 13(罗马数字转整数——字典映射)、LC 58(最后一个单词的长度)
- [ ] 作业完成并 push,绿格子连续第 12 天
