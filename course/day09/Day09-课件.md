# Day 09:面向对象编程(下)—— 继承、多态与魔术方法:亲手造出 LangChain 的骨架

---

# 【旁白解读】昨天、今天、明天

**昨天(Day 08)你学会了造对象**:ChatMessage 和 ChatSession 两个类已经能构造即校验、双向过海关(to_dict/from_dict)、多实例隔离。昨天还埋了三个钩子:① 类方法工厂里 `cls(...)` 而不是硬编码类名,说"继承时见效";② 属性拼错不报错的隐患,说"@property 能治";③ `print(msg)` 输出的是一串 `<__main__.ChatMessage object at 0x...>` 天书——你可能已经在作业里撞见了。

**今天(Day 09)三箭齐发,把 OOP 的下半场打完:**

- **继承与多态**:今天的主菜。你将亲手搭出课表里预告的 `BaseModel → OpenAIModel / QwenModel` 类继承结构——**这不是教学玩具,这就是 LangChain 统一调度百家模型的真实架构**(它的 BaseChatModel → ChatOpenAI / ChatTongyi 与你今天写的同构)。学完今天,Day 25 你第一次翻 LangChain 源码时会说"这不就是 Day 09 写过的吗";
- **魔术方法**:`__str__` 让 print(对象) 说人话、`__len__` 让 len(session) 直接可用、`__eq__` 让 == 比内容不比地址、`__call__` 让对象长出"函数的脸"——LangChain 的 Runnable 万物皆可 invoke,底层就是这类协议;
- **@property**:把方法伪装成属性,顺手给昨天的"拼错不报错"上一道锁。

**为什么继承在大模型开发里如此重要?** 一句话讲透行业痛点:市面上有几十家模型厂商(OpenAI、DeepSeek、通义、智谱、月之暗面……),每家 API 细节不同;但你的应用不想被任何一家绑死——今天用 DeepSeek 省钱,明天客户要求切 GPT-4o,总不能重写整个应用。解法就是**继承 + 多态**:定义一个统一的"模型基类"约定接口(`chat(messages)`),每家厂商一个子类各自实现细节,应用代码只面对基类接口。**换模型 = 换一个子类实例,一行代码。** 今天下午你会亲手实现这个"可插拔模型层",Day 12 接入真实 API 后它直接变成生产件。

---

# 上午 · 第一节(9:00 - 10:30):继承 —— 站在父类的肩膀上

## 1.1 从重复代码的味道说起

假设要支持两家模型,不用继承的写法:

```python
# 反面教材:两个类,80% 的代码一模一样
class OpenAIModel:
    def __init__(self, model_name, temperature=0.7):
        self.model_name = model_name
        self.temperature = temperature
    def count_cost(self, tokens): ...        # 一样的
    def format_info(self): ...               # 一样的
    def chat(self, messages): ...            # 只有这个不一样(各家 API 细节不同)

class QwenModel:
    def __init__(self, model_name, temperature=0.7):     # 抄一遍
        ...                                              # 全抄一遍,只有 chat 不同
```

第一周你已经被"复制粘贴"毒打过两次(Day 03 校验循环、Day 06 重构日),现在是类级别的同款问题。解法:**把共同的部分提取成父类,差异部分留给子类**:

```python
class BaseModel:
    """所有模型的父类(基类):存放共同的属性与行为。"""

    def __init__(self, model_name: str, temperature: float = 0.7):
        self.model_name = model_name
        self.temperature = temperature

    def format_info(self) -> str:
        """模型信息(所有子类通用,写一遍)。"""
        return f"{self.model_name} (temp={self.temperature})"


class OpenAIModel(BaseModel):          # 括号里写父类:OpenAIModel 继承 BaseModel
    """OpenAI 系模型。"""
    pass                               # 什么都不写,先看看能继承到什么


class QwenModel(BaseModel):
    """通义千问系模型。"""
    pass


gpt = OpenAIModel("gpt-4o")
qwen = QwenModel("qwen-plus", temperature=0.3)
print(gpt.format_info())       # gpt-4o (temp=0.7)      ← 没写 __init__ 和 format_info,
print(qwen.format_info())      # qwen-plus (temp=0.3)      全是从父类白拿的!
```

**继承的语法一行:`class 子类(父类)`。子类自动获得父类的全部属性和方法**——这就是"站在肩膀上"。术语对照:父类=基类=超类(base/super class),子类=派生类(derived class),都是一个意思。

昨天的属性查找顺序今天补全:**先对象自己 → 再自己的类 → 再父类(→ 再父类的父类,一路向上)**。gpt.format_info 在 OpenAIModel 里没有,向上到 BaseModel 找到了。

## 1.2 方法重写:子类有自己的主意

子类可以**重写(override)**父类的方法——定义同名方法,覆盖父类版本:

```python
class BaseModel:
    def __init__(self, model_name: str, temperature: float = 0.7):
        self.model_name = model_name
        self.temperature = temperature

    def chat(self, messages: list) -> str:
        """父类的 chat:一个'必须被子类重写'的占位。"""
        raise NotImplementedError("子类必须实现 chat 方法")
        # NotImplementedError:行业惯例——父类只定接口不给实现,
        # 谁忘了重写,一调用就炸出明确的提示(比默默返回 None 好一万倍)


class OpenAIModel(BaseModel):
    def chat(self, messages: list) -> str:
        """重写:OpenAI 风格的调用(今天用模拟,Day 12 换真 API)。"""
        return f"[OpenAI:{self.model_name}] 收到 {len(messages)} 条消息,回答:……"


class QwenModel(BaseModel):
    def chat(self, messages: list) -> str:
        """重写:通义风格的调用。"""
        return f"[通义:{self.model_name}] 已处理 {len(messages)} 条消息,答复:……"


msgs = [{"role": "user", "content": "你好"}]
print(OpenAIModel("gpt-4o").chat(msgs))       # 走 OpenAI 版
print(QwenModel("qwen-plus").chat(msgs))      # 走通义版
```

**查找顺序解释了重写的原理**:子类有 chat 就用子类的,搜索到此为止,父类的同名方法根本轮不到——"就近原则"。

## 1.3 super():先照抄爸爸的,再加自己的

子类经常不想**完全**推翻父类方法,而是"父类的照做,再补充自己的"。`super()` 就是"我爸爸"的引用:

```python
class OpenAIModel(BaseModel):
    def __init__(self, model_name: str, temperature: float = 0.7, api_base: str = "https://api.openai.com"):
        # 老三样(model_name/temperature)让爸爸装,别抄一遍:
        super().__init__(model_name, temperature)
        # 自己的新属性自己装:
        self.api_base = api_base


gpt = OpenAIModel("gpt-4o", api_base="https://my-proxy.com")
print(gpt.model_name, gpt.api_base)      # 父类装的 + 自己装的,都在
```

**super().__init__(...) 是继承里最高频的一行**,规则:**子类若定义了自己的 `__init__`,几乎总是要先调 super().__init__(),否则父类的出厂设置全部跳过**(model_name 都没装上,后面全崩)。这是今天排错手册的头号条目。

super() 不限于 `__init__`,任何方法都能用:

```python
class QwenModel(BaseModel):
    def chat(self, messages: list) -> str:
        print("(通义版:调用前先做敏感词预检……)")     # 自己的前置逻辑
        result = super().chat(messages)                  # 父类的照做(假设父类有通用实现)
        return result + "(已通过合规检查)"              # 自己的后置逻辑
# "前置 + 父类原样 + 后置"的三明治结构,Day 13 的装饰器是它的函数版
```

## 1.4 isinstance 与继承关系

```python
gpt = OpenAIModel("gpt-4o")

print(isinstance(gpt, OpenAIModel))    # True   它是 OpenAIModel
print(isinstance(gpt, BaseModel))      # True   ⚠️ 它也是 BaseModel!(儿子也是这家人)
print(isinstance(gpt, QwenModel))      # False  但不是隔壁家的
print(type(gpt) is OpenAIModel)        # True   type 只认"亲生类型"

# 实用建议:类型检查用 isinstance(认继承关系,符合"子类可当父类用"的精神),
# 不用 type ==(六亲不认)。isinstance 还能一次查多个:isinstance(x, (int, float))
```

昨天钩子①在此兑现:**类方法工厂里写 `cls(...)` 的回报**——

```python
class BaseModel:
    @classmethod
    def from_config(cls, config: dict) -> "BaseModel":
        """从配置字典造模型。cls 是'发起调用的那个类'。"""
        return cls(config["model_name"], config.get("temperature", 0.7))

m = QwenModel.from_config({"model_name": "qwen-plus"})
print(type(m).__name__)        # QwenModel —— 工厂认得下单的是谁!
# 若当初硬编码 return BaseModel(...),这里就只能造出 BaseModel,工厂废了一半
```

---

# 上午 · 第二节(10:40 - 12:00):多态 —— 同一句话,各自表述

## 2.1 多态:面向接口编程

**多态(polymorphism)**:不同子类对同一个方法调用作出各自的响应。它的价值要放到"使用方"的视角才能看清:

```python
def run_conversation(model: BaseModel, messages: list) -> str:
    """业务代码:只面对 BaseModel 接口,不关心具体是哪家模型。

    参数注解写 BaseModel:意思是"给我任何一个 BaseModel 的子类都行"。
    """
    print(f"使用模型:{model.format_info()}")
    return model.chat(messages)        # 同一行代码,不同子类各自表述


msgs = [{"role": "user", "content": "介绍一下你自己"}]

# 换模型 = 换一个实例,业务函数一个字不改:
print(run_conversation(OpenAIModel("gpt-4o"), msgs))
print(run_conversation(QwenModel("qwen-plus"), msgs))
```

这就是行业黑话"**面向接口编程,不面向实现编程**":run_conversation 依赖的是"chat 这个约定"(接口),不是"某家的具体实现"。好处清单:

1. **可扩展**:接入月之暗面?写一个 `KimiModel(BaseModel)` 实现 chat,业务代码零改动;
2. **可替换**:线上想省钱切换 DeepSeek,改一处实例化,别处不动;
3. **可测试**:写一个 `FakeModel(BaseModel)`,chat 返回固定文本——不花一分钱 API 费就能测完整个应用流程(**这一招 Day 14 项目一就会用**:先用 FakeModel 开发全流程,最后换真模型)。

**LangChain 的秘密现在可以说破了**:它的 `BaseChatModel` 定义了 invoke 接口,`ChatOpenAI`、`ChatTongyi`、`ChatZhipuAI` 各自实现,你的链代码 `chain = prompt | model | parser` 里的 model 换成谁都行。**Day 25 你会"学习"这个架构,今天你已经"发明"了它。**

## 2.2 鸭子类型:Python 的宽松版多态

Python 其实不强制继承也能多态——**"走起来像鸭子叫起来像鸭子,就当它是鸭子"**:

```python
class FakeModel:                       # 注意:没有继承 BaseModel!
    def format_info(self):
        return "假模型(测试专用)"
    def chat(self, messages):
        return "这是一条固定的测试回答"

print(run_conversation(FakeModel(), msgs))    # 照样能跑!
# Python 只在运行时问:"你有 format_info 和 chat 吗?有就行。"
# 这就是鸭子类型(duck typing)——不查户口(继承),只看能力(方法)
```

那还要继承干嘛?工程答案:**继承是"显式的约定 + 免费的复用"**——BaseModel 用 NotImplementedError 强制子类实现接口(忘写就炸)、共同代码写一遍。鸭子类型胜在灵活,继承胜在纪律,真实项目两者混用:核心架构用继承立规矩,边角处用鸭子类型图省事。

---

# 下午 · 第一节(14:00 - 15:30):魔术方法与 @property

## 3.1 魔术方法:教你的对象说 Python 的"母语"

双下划线包裹的方法(`__init__` 你已认识)统称**魔术方法/双下方法(dunder methods)**:你不直接调用它们,**Python 在特定时机自动调用**。掌握它们,你的类就能无缝接入 print、len、==、in 这些"母语级"操作:

```python
class ChatMessage:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

    # ── __str__:print(对象) / str(对象) 时自动调用 ──
    def __str__(self) -> str:
        """给'人'看的样子。"""
        return f"[{self.role}] {self.content}"

    # ── __repr__:交互模式回显 / repr() / 打印'对象列表'时调用 ──
    def __repr__(self) -> str:
        """给'开发者'看的样子:惯例是'能复原对象的代码'。"""
        return f"ChatMessage({self.role!r}, {self.content!r})"    # !r:对值取 repr

    # ── __eq__:== 比较时自动调用 ──
    def __eq__(self, other) -> bool:
        """内容相同即相等(默认的 == 比的是内存地址,基本没用)。"""
        if not isinstance(other, ChatMessage):
            return NotImplemented          # 跟非同类比:表态"我不会",让 Python 处理
        return self.role == other.role and self.content == other.content

    # ── __len__:len(对象) 时自动调用 ──
    def __len__(self) -> int:
        return len(self.content)


msg = ChatMessage("user", "你好")
print(msg)                         # [user] 你好          ← __str__,昨天的天书治好了
print([msg])                       # [ChatMessage('user', '你好')]   ← 列表里显示用 __repr__
print(msg == ChatMessage("user", "你好"))    # True        ← __eq__:比内容
print(len(msg))                    # 2                    ← __len__
```

**str 和 repr 的分工**(高频面试题):`__str__` 面向用户(print 的输出,追求好读),`__repr__` 面向开发者(调试时的显示,追求无歧义,惯例是合法的构造代码)。**最低配置:至少写 `__repr__`**(没有 `__str__` 时 print 会退而求其次用 `__repr__`,反之不行)。

再看容器级的魔术方法,给 ChatSession 装上:

```python
class ChatSession:
    def __init__(self, name: str):
        self.name = name
        self.messages: list = []

    def __len__(self) -> int:
        """len(session) = 消息条数。"""
        return len(self.messages)

    def __contains__(self, keyword: str) -> bool:
        """'关键词 in session' = 任何消息包含该关键词。"""
        return any(keyword in m.content for m in self.messages)

    def __getitem__(self, index):
        """session[0] / session[-1] / session[1:3] 直接可用(索引和切片全给)。"""
        return self.messages[index]


s = ChatSession("演示")
s.messages.append(ChatMessage("user", "什么是RAG?"))
s.messages.append(ChatMessage("assistant", "RAG是检索增强生成……"))

print(len(s))                # 2          __len__
print("RAG" in s)            # True       __contains__
print(s[-1])                 # [assistant] RAG是……   __getitem__ + __str__
for m in s[:1]:              # 切片也自动支持
    print(m)
```

一周前你学的 len/in/切片,今天你的自定义类全部接上了——**魔术方法就是 Python 的"通用插座协议"**。

## 3.2 `__call__`:让对象长出函数的脸

```python
class Translator:
    """一个'可调用对象':造出来像对象,用起来像函数。"""

    def __init__(self, target_lang: str):
        self.target_lang = target_lang        # 配置存在对象身上

    def __call__(self, text: str) -> str:
        """对象被'当函数调用'时自动执行:translator(text)。"""
        return f"[翻译成{self.target_lang}] {text}"


to_english = Translator("英文")          # 造对象:带配置
to_japanese = Translator("日文")

print(to_english("你好世界"))            # [翻译成英文] 你好世界  ← 对象后面直接加括号!
print(to_japanese("你好世界"))           # 像函数,但记得自己的配置

print(callable(to_english))             # True:它是"可调用的"
```

**`__call__` = 有状态的函数**:比普通函数多了"记住配置"的能力(Day 06 思考题的闭包干的也是这事,这是类版方案),比普通对象多了"直接调用"的顺手。它的行业地位:**LangChain 的 Runnable、PyTorch 的 nn.Module(model(x) 就是在调 `__call__`)、FastAPI 的中间件**,全构建在这个协议上。Day 13 讲装饰器时,"类装饰器"也靠它。

## 3.3 @property:把方法伪装成属性(昨天钩子②兑现)

```python
class ChatSession:
    def __init__(self, name: str):
        self._name = name              # 前缀单下划线:行业暗号"内部属性,外人别直接碰"
        self.messages: list = []

    # ── @property:读起来像属性,背后是方法 ──
    @property
    def message_count(self) -> int:
        """消息数:每次读都现算,永远新鲜。"""
        return len(self.messages)

    @property
    def name(self) -> str:
        """name 的读取通道。"""
        return self._name

    # ── @xxx.setter:赋值时自动过安检 ──
    @name.setter
    def name(self, value: str) -> None:
        """name 的写入通道:校验后才放行。"""
        if not value.strip():
            raise ValueError("会话名不能为空")
        self._name = value.strip()


s = ChatSession("工作")
print(s.message_count)        # 0     ← 没有括号!读属性的姿势,方法的内核
s.messages.append("x")
print(s.message_count)        # 1     ← 永远现算,不会像普通属性那样过期

s.name = "  新名字  "          # 赋值触发 setter:自动清洗
print(s.name)                 # 新名字
# s.name = "   "              # ValueError:空名被安检拦下 —— 拼错/塞脏值的隐患上了锁
```

@property 的三大用途:①**计算属性**(message_count 这类"由其他数据推导出来"的值,现算不存,永不过期);②**写入校验**(setter 安检);③**平滑演化**(今天是裸属性,明天要加校验,改成 property,**调用方代码一个字不用改**——这是它比 Java 风格 get_xxx() 方法优雅的地方)。

---

# 下午 · 第二节(15:40 - 17:30):实操——可插拔模型层

## 4.1 需求文档

> ### 需求文档:可插拔模型层 v1.0
>
> **需求编号**:REQ-D09-001
> **需求方**:「智言科技」AI 平台组
> **背景**:公司应用需要随时在 DeepSeek / OpenAI / 通义间切换(比价、容灾、客户指定)。要求建设统一的模型抽象层:业务代码只面对基类,新增厂商零侵入。Day 12 接入真实 API 后,本层直接投产。
>
> **类设计要求**:
> 1. `BaseChatModel` 基类:属性 model_name、temperature(必须用 @property + setter,校验范围 0~2);方法 `chat(messages)` 抛 NotImplementedError;`count_usage()` 统计累计调用次数与 token(通用实现);`__repr__`;类方法 `from_config(dict)`;
> 2. 子类 `DeepSeekModel` / `OpenAIModel` / `QwenModel`:各自重写 chat(今天返回模拟回答,格式各有特色,体现"同一接口各自表述");DeepSeekModel 额外有 api_base 属性(super() 的用武之地);
> 3. `FakeModel` 子类:chat 返回固定文本,供测试(多态的可测试性红利);
> 4. 演示函数 `run_demo(model: BaseChatModel)`:业务代码,任何子类实例都能跑。
>
> **验收标准**:assert 测试全过;temperature 塞 3.0 被拦;四个子类在同一个 run_demo 里轮流跑通;from_config 造出"对的型号"。

## 4.2 参考实现(核心讲解,完整见 code/model_layer.py)

```python
class BaseChatModel:
    """模型基类:统一接口 + 共同实现。LangChain BaseChatModel 的同构简化版。"""

    def __init__(self, model_name: str, temperature: float = 0.7):
        self.model_name = model_name
        self.temperature = temperature        # 注意:这行赋值会走 setter!安检从出生起生效
        self._call_count = 0                  # 内部计数:单下划线,外人别碰
        self._total_tokens = 0

    # ── temperature:property + setter,范围安检 ──
    @property
    def temperature(self) -> float:
        """采样温度(0~2)。"""
        return self._temperature

    @temperature.setter
    def temperature(self, value: float) -> None:
        if not (0 <= value <= 2):
            raise ValueError(f"temperature 必须在 0~2 之间,收到 {value}")
        self._temperature = value

    # ── 接口:子类必须实现 ──
    def chat(self, messages: list) -> str:
        """发送消息列表,返回回答。子类必须重写。"""
        raise NotImplementedError(f"{type(self).__name__} 必须实现 chat()")

    # ── 通用实现:所有子类白拿 ──
    def _record(self, tokens: int) -> None:
        """记录一次调用(内部方法:子类的 chat 里调用它)。"""
        self._call_count += 1
        self._total_tokens += tokens

    def count_usage(self) -> dict:
        """用量统计。"""
        return {"calls": self._call_count, "tokens": self._total_tokens}

    def __repr__(self) -> str:
        return f"{type(self).__name__}(model_name={self.model_name!r}, temperature={self.temperature})"

    @classmethod
    def from_config(cls, config: dict) -> "BaseChatModel":
        """配置字典 → 模型实例。cls 保证造出'下单的那个子类'。"""
        return cls(config["model_name"], config.get("temperature", 0.7))
```

```python
class DeepSeekModel(BaseChatModel):
    """DeepSeek:课程主力模型(Day 12 起接真 API)。"""

    def __init__(self, model_name: str = "deepseek-chat", temperature: float = 0.7,
                 api_base: str = "https://api.deepseek.com"):
        super().__init__(model_name, temperature)     # 老三样让爸爸装
        self.api_base = api_base                      # 自己的新属性自己装

    def chat(self, messages: list) -> str:
        """模拟 DeepSeek 风格回答(Day 12 换成 requests 真调用,接口不变!)。"""
        last = messages[-1]["content"] if messages else ""
        self._record(tokens=len(last) * 2)            # 模拟用量:复用父类的记账
        return f"(DeepSeek@{self.api_base})关于「{last[:10]}」的回答是……"


class FakeModel(BaseChatModel):
    """测试替身:不花钱、零延迟、输出可预测——多态的可测试性红利。"""

    def chat(self, messages: list) -> str:
        self._record(tokens=0)
        return "这是测试回答。"
```

```python
def run_demo(model: BaseChatModel) -> None:
    """业务代码:面对接口,不面对实现。"""
    print(f"\n>>> 当前模型:{model!r}")
    msgs = [{"role": "user", "content": "什么是多态?"}]
    print(model.chat(msgs))
    print(f"用量:{model.count_usage()}")


# 四个模型轮流跑,业务函数一字不改——多态的现场证明
for m in [DeepSeekModel(), OpenAIModel("gpt-4o"), QwenModel("qwen-plus"), FakeModel("fake")]:
    run_demo(m)
```

## 4.3 验收测试要点(完整见代码)

```python
# temperature 安检:构造时和运行时都生效
try:
    DeepSeekModel(temperature=3.0)
    assert False
except ValueError:
    pass

m = DeepSeekModel()
try:
    m.temperature = -1              # 运行时改也要过安检(setter 的价值)
    assert False
except ValueError:
    pass

# from_config 造出对的型号(cls 的价值)
m2 = QwenModel.from_config({"model_name": "qwen-max"})
assert type(m2) is QwenModel

# 基类不能直接干活(接口的纪律)
try:
    BaseChatModel("base").chat([])
    assert False
except NotImplementedError:
    pass

# isinstance 认继承
assert isinstance(DeepSeekModel(), BaseChatModel)
```

## 4.4 收尾:这个模型层的未来时间线

- **Day 12**:DeepSeekModel.chat 里的模拟代码换成 requests 真调用——**只改子类内部,接口纹丝不动**;
- **Day 13**:给 chat 加重试装饰器、从 .env 读 API Key;
- **Day 14**:项目一用 FakeModel 开发调试、交付时换 DeepSeekModel;
- **Day 25**:见到 LangChain 的 BaseChatModel 时,你会心一笑。

---

# 【常见错误与排错手册】Day 09 专属篇

**错误 1:子类写了 `__init__` 忘调 super().__init__()。** 父类的出厂设置全跳过,用到父类属性时 `AttributeError: 'X' object has no attribute 'model_name'`。头号错误,子类 __init__ 第一行先写 super()。

**错误 2:super().__init__() 忘了传参。** `TypeError: __init__() missing 1 required positional argument`——爸爸要材料,你空手喊他干活。

**错误 3:重写方法拼错名字,变成"新增"而不是"覆盖"。** `def chatt(self, ...)` 不报错,但调 chat 走的还是父类版(或炸 NotImplementedError)。这正是 NotImplementedError 占位的价值:忘实现/拼错实现都会在第一次调用时炸出来。

**错误 4:@property 的存储属性和 property 同名,无限递归。** setter 里写 `self.temperature = value`(而不是 `self._temperature`)→ 赋值又触发 setter → 无限递归 → RecursionError。**property 名不带下划线,真正存值的属性带下划线**,一对一错不了。

**错误 5:`__eq__` 忘了 isinstance 检查。** `msg == "字符串"` 时 other.role 直接 AttributeError。先查同类,异类返回 NotImplemented。

**错误 6:`__str__` 里没 return 或 return 了非字符串。** `TypeError: __str__ returned non-string`。

**错误 7:多重继承的顺序困惑。** Python 支持 `class C(A, B)`,查找顺序遵循 MRO(可用 `C.__mro__` 查看)。初学阶段的纪律:**只用单继承**,多重继承等有明确需要再学(课程内不会用到超过单继承的场景)。

**错误 8:滥用继承表达"有一个"关系。** ChatSession 继承 list?错——会话**有一批**消息(组合),不**是一种**列表(继承)。口诀:**is-a 用继承(DeepSeekModel 是一种 BaseChatModel),has-a 用组合(ChatSession 有一个 messages 列表)**。拿不准时优先组合。

---

# 【课堂笔记】Day 09 知识点速查表

**继承**
- `class 子类(父类)`:白拿父类全部属性方法;属性查找:对象 → 类 → 父类链
- 重写:同名方法就近覆盖;父类占位方法 raise NotImplementedError(忘实现即炸)
- `super().__init__(...)`:子类 __init__ 第一行的标配;super() 三明治=前置+父类+后置
- isinstance 认继承(儿子也是这家人),type 只认亲生;类型检查用 isinstance
- 工厂用 cls(...):子类下单造子类

**多态**
- 同一接口,各自表述;业务代码面对基类注解(model: BaseChatModel)
- 三大红利:可扩展(新增子类零侵入)/可替换(换模型一行)/可测试(FakeModel)
- 鸭子类型:不查户口只看能力;继承=约定+复用,鸭子=灵活;核心架构用继承
- is-a 继承,has-a 组合;拿不准优先组合

**魔术方法**
| 方法 | 触发时机 | 一句话 |
|---|---|---|
| `__str__` | print/str | 给人看 |
| `__repr__` | 调试回显/容器内 | 给开发者看(至少写它) |
| `__eq__` | == | 比内容不比地址(先 isinstance) |
| `__len__` | len() | 容器长度 |
| `__contains__` | in | 包含判断 |
| `__getitem__` | obj[i] | 索引+切片 |
| `__call__` | obj() | 有状态的函数(Runnable 的根) |

**@property**
- 读像属性,内核是方法;`@name.setter` 赋值安检
- 三用途:计算属性(现算不过期)/写入校验/平滑演化(调用方零改动)
- 命名铁律:property 不带下划线,存储属性 `self._name` 带下划线(防无限递归)
- 单下划线前缀 = "内部属性,外人别直接碰"(君子协定)

**今日核心资产**:BaseChatModel → DeepSeek/OpenAI/Qwen/Fake 可插拔模型层(Day 12 投产)

---

# 【附录】课堂答疑实录(晚自习整理)

**问 1:继承能连续好几层吗?爷爷→爸爸→儿子?**

答:能,查找顺序一路向上(对象→类→父类→祖父类→…→object,万物的终极祖先都是 object 类)。但工程上**继承层次超过三层就是坏味道**:每加一层,理解一个子类就要向上翻一层,和嵌套 if 的心智成本同理。LangChain 这样的大框架也基本控制在两三层。你自己设计时:一层抽象(Base + 直接子类)解决 90% 的问题。

**问 2:NotImplementedError 和 Python 的抽象基类(ABC)什么关系?**

答:同一个目的的两种强度。NotImplementedError 是"运行时才炸"(调用了才发现没实现);标准库的 `abc` 模块 + `@abstractmethod` 是"实例化就炸"(子类没实现接口连对象都造不出来),纪律更严。课程用前者,因为够用且零门槛;你在 LangChain 源码里会看到后者(`class BaseChatModel(ABC)`),届时把"炸的时机提前了"这句话带上就全懂了。面试如果问"如何强制子类实现方法",两个都答,加分。

**问 3:`self._name` 的单下划线到底防不防得住外人?**

答:防君子不防小人——Python 没有真正的私有(Java 的 private 那种),单下划线纯粹是**命名公约**:"这是内部实现,直接访问后果自负"。双下划线 `__name` 会触发"名字改写"(变成 `_ClassName__name`),稍微难碰一点,但也挡不住有心人。Python 的哲学是"我们都是成年人"——用公约而不是锁来管理边界。实践建议:对外的稳定接口不带下划线,内部实现带一个下划线,双下划线基本不用(除了魔术方法)。

**问 4:__eq__ 里返回 NotImplemented(不是 raise!)是什么操作?**

答:细节好问题。`NotImplemented` 是一个特殊值(不是异常),意思是"这个比较**我**不会做"。返回它之后,Python 会去问对方(`other.__eq__(self)`),对方也不会就最终判 False。如果你直接 return False,就剥夺了对方表态的机会;如果 raise,== 这种日常操作动不动就崩。所以协议规定:不认识的类型,返回 NotImplemented,把话筒递出去。这类"协议细节"不用背,写 __eq__ 时照模板抄即可。

**问 5:@property 会不会性能差?每次读都跑一遍方法。**

答:会多一次函数调用的开销,但量级是纳秒,应用开发完全无感(又是"瓶颈永远在网络和模型推理"定律)。真正要注意的是**语义**:property 应该"读起来便宜且无副作用"——如果 message_count 背后要查数据库三秒,伪装成属性就是欺骗(读代码的人以为只是取个值)。贵的操作老老实实用方法名 `fetch_message_count()`,让调用方有心理准备。

**问 6:FakeModel 这种"测试替身"在真实工作里常用吗?感觉像作弊。**

答:不但常用,而且有正式的名字和家族:测试替身(Test Double),细分 Stub(固定返回)、Mock(还能验证被怎么调用过)、Fake(简化实现)。大模型开发里它尤其重要,三个原因:①API 调用**花钱**,跑一次全流程测试几毛钱,CI 一天跑一百次就是几十块;②API **有延迟**,真调用让测试从毫秒变秒;③模型输出**不确定**,同一问题两次答案不同,没法写 assert。所以行规是:业务逻辑测试全用 Fake,只在专门的"集成测试"里少量真调。Day 14 你会全程体验这个工作流。

**问 7:什么时候用 __call__ 什么时候老老实实写个方法名?**

答:判断标准:**这个对象的"主业"是不是就是那一个动作?** Translator 的主业就是翻译,`to_english(text)` 读起来自然;ChatSession 的主业有增删改查一堆,挑哪个当 __call__ 都武断,老实用方法名。经验参照:框架里用 __call__ 的都是"本质上是个函数,只是需要携带配置/状态"的东西(模型、管道、中间件)。日常业务类 95% 不需要它。

**问 8:今天的模型层和 Day 12 的真实 API 之间,还差什么?**

答:三样,全部下周补齐:①**网线**——requests 库把消息真的发到 api.deepseek.com(Day 12);②**钥匙**——API Key 的申请与 .env 安全管理(Day 12/13);③**铠甲**——网络会超时、会断,chat 方法需要 try/except + 重试(Day 10 异常 + Day 13 装饰器)。注意这三样全是"子类内部的事":BaseChatModel 的接口、run_demo 的业务代码,一个字都不用动——这就是今天架构设计的回报。

---

# 【明日预告】Day 10:模块、包与异常处理

代码已经会组织成函数和类了,明天解决更大尺度的组织:**模块与包**——把 chat_models.py、model_layer.py 变成可以 `import` 的工具库,`if __name__ == "__main__"` 的谜底正式揭晓,再学会用 venv 虚拟环境和 requirements.txt 管理项目依赖(接手任何开源项目的第一步)。下午是**异常处理**:try/except/else/finally 的完整语法、自定义异常、raise 的进阶——今天模型层"网络会超时怎么办"的答案。实操:把第二周的类库拆分成规范的多文件包结构,并给模型层穿上第一层异常铠甲。

**睡前自检清单**:
- [ ] 能画出 BaseChatModel 家族的继承图,说清"接口"与"实现"的分工
- [ ] super().__init__ 的作用和漏写的后果能脱口而出
- [ ] 七个魔术方法的触发时机能对上号
- [ ] model_layer.py 手敲运行,assert 全过,四模型轮跑成功
- [ ] LeetCode:LC 232(用栈实现队列——类设计题)、LC 155(最小栈)
- [ ] 作业完成并 push,绿格子连续第 9 天
