# =============================================
# Day 09 · 下午演示代码 1:魔术方法与 @property
# 文件:magic_methods_demo.py
# 魔术方法 = Python 的"通用插座协议":接上后 print/len/==/in/[] 全部可用
# =============================================


class ChatMessage:
    """装上了四个魔术方法的消息类。"""

    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

    def __str__(self) -> str:
        """print(对象) 时调用:给'人'看的样子。"""
        return f"[{self.role}] {self.content}"

    def __repr__(self) -> str:
        """调试回显/容器内显示:给'开发者'看,惯例是能复原对象的代码。"""
        return f"ChatMessage({self.role!r}, {self.content!r})"    # !r 对值取 repr

    def __eq__(self, other) -> bool:
        """== 时调用:比内容(默认比内存地址,基本没用)。"""
        if not isinstance(other, ChatMessage):
            return NotImplemented      # 跟非同类比:表态"我不会",把话筒递给对方
        return self.role == other.role and self.content == other.content

    def __len__(self) -> int:
        """len(对象) 时调用。"""
        return len(self.content)


msg = ChatMessage("user", "你好")
print(msg)                                     # [user] 你好          __str__
print([msg])                                   # [ChatMessage('user', '你好')]  __repr__
print(msg == ChatMessage("user", "你好"))       # True                __eq__
print(len(msg))                                # 2                   __len__


class ChatSession:
    """容器级魔术方法 + @property 的会话类。"""

    def __init__(self, name: str):
        self._name = name              # 单下划线:内部属性,外人别直接碰(君子协定)
        self.messages: list = []

    # ── 容器协议 ──
    def __len__(self) -> int:
        """len(session) = 消息条数。"""
        return len(self.messages)

    def __contains__(self, keyword: str) -> bool:
        """'关键词 in session' = 任何消息包含该关键词。"""
        return any(keyword in m.content for m in self.messages)

    def __getitem__(self, index):
        """session[0] / session[-1] / session[1:3]:索引和切片全给。"""
        return self.messages[index]

    # ── @property:读像属性,内核是方法 ──
    @property
    def message_count(self) -> int:
        """消息数:每次读都现算,永远新鲜(计算属性)。"""
        return len(self.messages)

    @property
    def name(self) -> str:
        """name 的读取通道。"""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """name 的写入通道:校验后才放行(写入安检)。

        ⚠️ 这里必须写 self._name(带下划线的存储属性)!
        写 self.name 会再次触发 setter → 无限递归 → RecursionError
        """
        if not value.strip():
            raise ValueError("会话名不能为空")
        self._name = value.strip()


s = ChatSession("演示")
s.messages.append(ChatMessage("user", "什么是RAG?"))
s.messages.append(ChatMessage("assistant", "RAG是检索增强生成……"))

print(len(s))                 # 2          __len__
print("RAG" in s)             # True       __contains__
print(s[-1])                  # __getitem__ + __str__
print(s.message_count)        # 2          property:没有括号!

s.name = "  新名字  "          # setter 自动清洗
print(s.name)                 # 新名字
try:
    s.name = "   "            # 空名被安检拦下
except ValueError as e:
    print(f"拦截成功:{e}")


# ── __call__:让对象长出函数的脸 ──
class Translator:
    """可调用对象:造出来像对象,用起来像函数(= 有状态的函数)。

    行业地位:LangChain Runnable、PyTorch nn.Module(model(x))、
    FastAPI 中间件,全构建在这个协议上。
    """

    def __init__(self, target_lang: str):
        self.target_lang = target_lang        # 配置存在对象身上

    def __call__(self, text: str) -> str:
        """对象被'当函数调用'时自动执行:translator(text)。"""
        return f"[翻译成{self.target_lang}] {text}"


to_english = Translator("英文")
to_japanese = Translator("日文")
print(to_english("你好世界"))                  # 对象后面直接加括号!
print(to_japanese("你好世界"))                 # 像函数,但记得自己的配置
print(callable(to_english))                   # True
