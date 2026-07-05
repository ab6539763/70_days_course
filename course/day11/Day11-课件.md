# Day 11:文件操作与常用标准库 —— RAG 文档处理的前置技能点亮日

---

# 【旁白解读】昨天、今天、明天

**昨天(Day 10)你搭好了 chatlib 包**,异常铠甲也穿上了。今天是第一阶段(Python 基础)的倒数第三天,主题是"**和真实世界的数据打交道**"——真实世界的数据住在文件里:客服记录是 txt、报表是 csv、配置和存档是 json、公司制度是 pdf 和 word。

今天要结清的历史欠账,一只手数不过来:

1. Day 07 起"照抄使用"的 `with open(...)` 模板函数——今天逐行拆解转正;
2. Day 07 答疑的"encoding='utf-8' 和 ensure_ascii=False 管两层"——今天画图讲透编码;
3. Day 05 彩蛋"时间戳 1751702400 的翻译官 datetime"——今天上岗;
4. Day 02 手机号提取的"完美方案是正则表达式"——今天兑现;
5. 昨天作业里 os.rename 的"顺便预习"——今天 os/pathlib 正课。

**为什么课表说今天是"RAG 文档处理的前置技能"?** 提前看一眼 Day 28 的工作:把一批 PDF/Word/Markdown 文档读进来 → 清洗 → 切块 → 向量化入库。其中"批量找到文件、读出文本、处理编码、清洗内容"全是今天的技能;Day 28 只是把"读 txt"换成"用库读 PDF",骨架今天就定型。**今天下午的实操"批量文档关键词统计工具",就是 Day 28 文档流水线的第一块真实积木。**

今天的路线:上午——文件读写全解(open 模式、with 原理、编码之谜、csv/json 实战);下午——标准库四大金刚(os/pathlib、datetime、random 补遗、re 正则入门)+ 实操。

---

# 上午 · 第一节(9:00 - 10:30):文件读写全解

## 1.1 open:文件世界的大门

```python
# 最原始的形态(先看懂,马上升级成 with)
f = open("notes.txt", "w", encoding="utf-8")    # ① 开门:拿到文件对象
f.write("第一行笔记\n")                           # ② 干活:写入(\n 手动换行!)
f.write("第二行笔记\n")
f.close()                                        # ③ 关门:必须!不关有三宗罪(见下)
```

`open(路径, 模式, encoding)` 三个参数逐个说:

**模式(mode)——今天记四个,见七个:**

| 模式 | 含义 | 文件不存在时 | 文件已存在时 |
|------|------|------------|------------|
| `"r"` | 读(默认) | **报 FileNotFoundError** | 从头读 |
| `"w"` | 写 | 创建 | **清空重写!⚠️** |
| `"a"` | 追加(append) | 创建 | 在末尾续写 |
| `"rb"` / `"wb"` | 二进制读/写 | 同上 | 同上(图片/PDF/模型文件用,不带 encoding) |

**头号事故预警:`"w"` 模式一开门就把原文件清空**——手滑用 w 打开重要文件,内容瞬间蒸发,Git 也救不了没提交过的东西。写日志、攒记录用 `"a"`;确定要覆盖才用 `"w"`。

**不 close 的三宗罪**:①写入的内容可能滞留在缓冲区没真正落盘(程序一崩,"写过的"数据消失);②文件被占用,别的程序(甚至你自己)打不开;③操作系统的文件句柄是有限资源,批量处理几千个文件不关会耗尽。——但人总会忘记关门,于是有了 with。

## 1.2 with:自动关门的语法糖(昨天 finally 的直接应用)

```python
# with 版:代码块结束(无论正常走完还是中途异常),自动 close
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("第一行笔记\n")
    f.write("第二行笔记\n")
# 出了这个缩进块,f 已经自动关好——包括中途抛异常的情况!

# with 的本质就是昨天学的 try/finally 的封装:
#   f = open(...)
#   try:
#       ...你的代码...
#   finally:
#       f.close()
# 这类"进门自动准备、出门自动打扫"的对象叫"上下文管理器"。
# 铁律:凡是 open,必是 with open。本课程此后出现裸 open 一律算错误
```

## 1.3 读的三种姿势

```python
# 姿势一:read() —— 整个文件一口吞成一个字符串
with open("notes.txt", "r", encoding="utf-8") as f:
    content = f.read()
print(content)              # 适合:小文件、要整体处理(比如 json.load 内部就是它)

# 姿势二:readlines() —— 按行吞成列表(每行末尾带着 \n!)
with open("notes.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
print(lines)                # ['第一行笔记\n', '第二行笔记\n']  ← 注意 \n 还在
clean_lines = [line.strip() for line in lines]      # 标准动作:推导式逐行 strip

# 姿势三:直接 for 遍历文件对象 —— 一行一行流式读(推荐!)
with open("notes.txt", "r", encoding="utf-8") as f:
    for line in f:                       # 每轮只读一行进内存
        line = line.strip()
        if not line:                     # 跳过空行:处理真实文件的标配
            continue
        print(f"处理:{line}")
# 为什么推荐姿势三?1GB 的日志文件,read() 要把 1GB 全塞进内存;
# for 逐行读,内存里永远只有一行。"流式处理"思想的第一次登场——
# Day 24 的大模型流式输出、Day 28 的大文档处理,同一个思想
```

## 1.4 编码之谜:为什么总要写 encoding="utf-8"

计算机只存 0 和 1,"文字 ↔ 字节"的翻译规则就是**编码**。麻烦在于规则不止一套:

```
"你好" --UTF-8 编码--> e4 bd a0 e5 a5 bd      (每个汉字 3 字节,全球通用,事实标准)
"你好" --GBK 编码-->   c4 e3 ba c3            (每个汉字 2 字节,中文 Windows 的历史遗产)

用 GBK 规则去读 UTF-8 字节 → 得到 "浣犲ソ" 之类的乱码(字节没坏,翻译错了)
用 UTF-8 规则去读 GBK 字节 → UnicodeDecodeError 或 乱码
```

**乱码的本质:写和读用了两套翻译规则。** 而 Windows 上 Python 的 open 默认编码是 GBK(跟随系统),macOS/Linux 默认 UTF-8——**同一份代码换台电脑就乱码**,这就是必须显式写 `encoding="utf-8"` 的原因:把翻译规则钉死,不给操作系统发挥空间。

Day 07 答疑的"两层"现在可以画全了:

```
Python 字典 --json.dumps(ensure_ascii=False)--> JSON 字符串(中文保持中文)
JSON 字符串 --open(..., encoding="utf-8") + write--> 磁盘上的字节
             ↑ 第一层:对象→文本的翻译       ↑ 第二层:文本→字节的翻译
```

两层各管各的,都配置好,中文数据才能全程健康。**课程铁律:所有 open 必带 encoding="utf-8"。** 收到别人的乱码文件怎么办?试着用 `encoding="gbk"` 读——国内老系统导出的 csv 十有八九是它。

## 1.5 CSV:表格数据的通用格式

CSV(逗号分隔值)= 用文本存表格,Excel 能直接打开。Day 07 作业你已手工拼过 CSV,今天用标准库 csv 模块转正(它处理了手工 split 搞不定的边角:字段里带逗号、带引号):

```python
import csv

# ── 写 CSV ──
rows = [
    ["姓名", "岗位", "评分"],                 # 表头
    ["张三", "大模型工程师", 92],
    ["李四", "产品经理, AI方向", 88],          # ← 字段里有逗号!手工 join 会翻车,csv 模块自动加引号
]
with open("staff.csv", "w", encoding="utf-8", newline="") as f:
    # newline="":csv 模块的固定搭配,防止 Windows 上写出空行(记住即可)
    writer = csv.writer(f)
    writer.writerows(rows)                    # 一次写多行(writerow 单行)

# ── 读 CSV:字典方式(推荐,按列名取,不用记第几列) ──
with open("staff.csv", "r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)                # 自动把第一行当表头
    for row in reader:                        # 每行是一个字典!
        print(f"{row['姓名']}{row['岗位']},评分 {row['评分']}")
        # 注意:csv 读出来的一切都是字符串,评分要用还得 int(row['评分'])
        # ——input 返回 str 的老坑,在文件世界重演
```

CSV 的未来出场:Day 28 的 CSVLoader 加载表格类知识、Day 34 的评估测试集、Day 52 的数据集清洗,格式都是它。

## 1.6 JSON 文件读写:load/dump 转正

Day 05 记忆图的"文件半区"正式启用,Day 07 模板函数逐行看懂:

```python
import json

config = {"model": "deepseek-chat", "temperature": 0.7, "tags": ["生产", "客服"]}

# dump(不带 s):对象 → 直接写进文件(= dumps + write 二合一)
with open("config.json", "w", encoding="utf-8") as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

# load(不带 s):文件 → 直接读成对象(= read + loads 二合一)
with open("config.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)

assert loaded == config       # 往返无损
# 至此 json 四大函数全部服役:loads/dumps 管字符串(网络),load/dump 管文件(磁盘)
```

---

# 上午 · 第二节(10:40 - 12:00):标准库四大金刚(上)——路径与时间

## 2.1 os 与 pathlib:文件系统的遥控器

os 是老牌模块(昨天作业用过 os.rename/os.remove),pathlib 是现代面向对象版(Day 08 的知识:路径也成了对象)。**课程主用 pathlib,os 认识常用款**:

```python
from pathlib import Path

# ── 造路径对象 ──
p = Path("docs") / "reports" / "q3.txt"     # 用 / 拼路径!自动适配 Windows\ 和 mac/
print(p)                                     # docs/reports/q3.txt(mac)或 docs\reports\q3.txt(Win)
# 对比字符串拼接 "docs" + "\\" + ...:pathlib 一举消灭平台差异和转义地狱(Day 02 错误 7)

# ── 路径对象的常用属性(全是 property!Day 09 的知识在标准库里的真身) ──
p = Path("docs/深度学习入门.pdf")
print(p.name)          # 深度学习入门.pdf     文件全名
print(p.stem)          # 深度学习入门          不带扩展名
print(p.suffix)        # .pdf                扩展名(Day 02 切片取后缀的正规军!)
print(p.parent)        # docs                所在目录

# ── 存在性与类型 ──
print(p.exists())      # 文件/目录是否存在
print(p.is_file(), p.is_dir())

# ── 建目录 / 读写小文件的快捷方式 ──
Path("output").mkdir(exist_ok=True)         # exist_ok=True:已存在不报错
Path("output/note.txt").write_text("你好", encoding="utf-8")     # 一行写小文件
text = Path("output/note.txt").read_text(encoding="utf-8")       # 一行读小文件
# (快捷方式适合小文件;大文件仍用 with open 流式处理)

# ── ★ glob:批量找文件——今天下午实操的心脏 ──
docs_dir = Path("docs")
for txt_file in docs_dir.glob("*.txt"):          # 当前目录下所有 .txt
    print(txt_file)
for any_txt in docs_dir.rglob("*.txt"):          # r = recursive:连子目录一起翻
    print(any_txt)
# glob 的通配符:* 任意字符,? 单个字符,[abc] 候选集
# Day 28 的 DirectoryLoader("docs/", glob="**/*.pdf") 就是它的框架包装
```

os 模块保留节目(pathlib 覆盖不到/不顺手的):`os.rename`(改名/移动)、`os.remove`(删文件)、`os.environ`(环境变量——**Day 13 读 API Key 就靠它**,先记住名字)。

## 2.2 datetime:时间的翻译官(Day 05 彩蛋兑现)

```python
from datetime import datetime, timedelta

# ── 现在 ──
now = datetime.now()
print(now)                                   # 2026-07-16 14:30:52.123456

# ── 格式化输出:strftime(f = format,时间→字符串) ──
print(now.strftime("%Y-%m-%d %H:%M:%S"))     # 2026-07-16 14:30:52
print(now.strftime("%Y%m%d_%H%M%S"))         # 20260716_143052  ← 做文件名的标准姿势
# 格式代码速记:%Y 四位年 %m 月 %d 日 %H 时 %M 分 %S 秒(区分大小写!%m 月 %M 分)

# ── 解析字符串:strptime(p = parse,字符串→时间) ──
dt = datetime.strptime("2026-07-05 09:00", "%Y-%m-%d %H:%M")

# ── 时间戳互转:Day 05 的 1751702400 之谜正式破案 ──
ts = 1751702400
print(datetime.fromtimestamp(ts))            # 2026-07-05 …… API 返回的 created 字段翻译成人话
print(now.timestamp())                       # 反向:时间 → 秒数

# ── 时间运算:timedelta ──
deadline = now + timedelta(days=7)           # 一周后
print(f"作业截止:{deadline.strftime('%m月%d日')}")
elapsed = deadline - now                     # 两个时间相减得 timedelta
print(elapsed.days, elapsed.total_seconds()) # 7 604800.0
```

datetime 的高频岗位:给会话/日志打时间戳(Day 14 的对话记录带时间)、按日期命名存档文件、计算 API 调用耗时(`(t2 - t1).total_seconds()`,Day 46 性能监控的雏形)。

## 2.3 random 补遗(30 秒)

Day 03 用过 randint,补三个常用款:`random.choice(列表)` 随机挑一个(测试数据生成)、`random.shuffle(列表)` 原地打乱(Day 52 数据集洗牌)、`random.random()` 0~1 浮点(概率抽样)。

---

# 下午 · 第一节(14:00 - 15:10):re 正则表达式入门(Day 02 的"完美方案"兑现)

## 3.1 正则是什么:描述文本模式的迷你语言

Day 02 的手机号提取用 `find("138")`,只能抓 138 开头的——因为字符串方法只会找"写死的字面文本"。正则表达式(regular expression)描述的是**模式**:"1 开头,第二位是 3-9,后面再来 9 个数字"——一条规则,通吃所有手机号。

```python
import re

text = "联系张经理 13812345678 或李助理 15987654321,座机 021-6543-2100"

# findall:找出所有匹配,返回列表——今天用得最多的函数
phones = re.findall(r"1[3-9]\d{9}", text)
print(phones)          # ['13812345678', '15987654321']  座机不会被误抓
```

解剖这条模式 `r"1[3-9]\d{9}"`:

```
r"..."      原始字符串(Day 02 转义课的 r 前缀):让 \d 不被 Python 转义层干扰。
            写正则,永远带 r 前缀,肌肉记忆
1           字面的 1:就匹配字符"1"
[3-9]       字符集:这一位可以是 3 到 9 中任何一个
\d          数字字符(等价于 [0-9])
{9}         前面的东西重复 9 次
```

## 3.2 今天要会的模式零件(入门套餐,够用到 Day 28)

| 零件 | 含义 | 例子 |
|------|------|------|
| `\d` / `\w` / `\s` | 数字 / 字母数字下划线 / 空白 | `\d{4}` 四位数字 |
| `.` | 任意一个字符(除换行) | `a.c` 匹配 abc、a7c |
| `*` / `+` / `?` | 重复 0+ 次 / 1+ 次 / 0 或 1 次 | `\d+` 一串数字 |
| `{n}` / `{n,m}` | 恰好 n 次 / n 到 m 次 | `\d{11}` |
| `[abc]` / `[^abc]` | 候选集 / 排除集 | `[3-9]` |
| `^` / `$` | 开头 / 结尾锚点 | `^https` 以 https 开头 |
| `()` | 分组:单独提取某部分 | 见下方邮箱例子 |
| `\.` | 转义:匹配字面的点 | 域名里的点 |

```python
# ── 常用四函数 ──
text = "订单A2026,金额 3580 元,联系 zhang.san@deepseek.com,备注:加急"

# ① findall:全部匹配
print(re.findall(r"\d+", text))                    # ['2026', '3580']

# ② search:找第一个,返回 Match 对象(没有则 None——用前必判!)
m = re.search(r"(\w[\w.]*)@([\w.]+)", text)        # 括号分组:用户名 和 域名
if m:                                              # Day 02 排错手册"find 返回 -1"的正则版
    print(m.group(0))      # zhang.san@deepseek.com   整体
    print(m.group(1))      # zhang.san                第 1 组
    print(m.group(2))      # deepseek.com             第 2 组

# ③ sub:按模式替换(replace 的模式版)
masked = re.sub(r"1[3-9]\d{9}", "1**********", "手机 13812345678 已登记")
print(masked)                                      # 手机脱敏的正则版

# ④ split:按模式切分(split 的模式版)
parts = re.split(r"[,;,;]\s*", "苹果,香蕉; 橙子,梨")     # 中英文逗号分号通吃
print(parts)               # ['苹果', '香蕉', '橙子', '梨']  ← Day 02 错误 6(中文逗号)的终极解
```

## 3.3 使用纪律:正则是好仆人、坏主人

三条纪律:①**能用字符串方法就别用正则**——`text.startswith("http")` 比 `re.match(r"^http", text)` 快且好读,正则只在"模式"复杂到字符串方法搞不定时出场;②**写注释**——三个月后没人看得懂 `r"(\w[\w.]*)@([\w.]+)"`,模式旁边必须写人话;③**测试极端输入**——正则的坑都在边角(空串、超长、部分匹配),写完就拿怪数据打一轮。正则的深水区(贪婪/非贪婪、环视、性能陷阱)不在今天范围,入门套餐够用到 Day 28,真实需要时再查手册——工程师的正则大多是"现查现写现测"。

**未来出场预告**:Day 18 从大模型输出里抠 JSON(`re.search(r"\{.*\}", output, re.DOTALL)`)、Day 28 文档清洗(删页眉页脚模式)、Day 52 数据集清洗(过滤含网址的样本)。

---

# 下午 · 第二节(15:20 - 17:30):实操——批量文档关键词统计工具

## 4.1 需求文档

> ### 需求文档:批量文档关键词统计工具 v1.0
>
> **需求编号**:REQ-D11-001
> **需求方**:「智言科技」知识管理组
> **背景**:公司积累了一批客服问答记录(txt 文件,编码不一,有 UTF-8 有 GBK),散落在多级子目录里。知识管理组想知道:哪些主题词出现最频繁(为下一步建设知识库(Day 28-30)确定优先级)。
>
> **功能需求**:
> 1. 递归扫描指定目录下所有 .txt 文件(rglob);
> 2. 逐个读取,**自动处理编码**:先试 UTF-8,失败再试 GBK,都失败则记录为坏文件并跳过(昨天的军规:坏文件不搞崩整批);
> 3. 文本清洗:小写化、正则去除网址和邮箱(噪音)、去多余空白;
> 4. 统计给定关键词表中每个词的出现次数(字典计数器)+ 每个词出现在几个文件中(集合!);
> 5. 生成报告:控制台对齐输出 + 保存为带时间戳的 JSON 报告文件(`report_20260716_1530.json`);
> 6. 处理摘要:成功/失败文件数、总字数、耗时(datetime 计时)。
>
> **技术要求**:pathlib 路径、with open、三层函数架构、异常处理按 Day 10 军规。
>
> **验收标准**:附带的样例数据目录(含一个 GBK 文件和一个假"坏文件")全部正确处理;报告数据准确。

## 4.2 流程图

```
 指定目录
    │ rglob("*.txt")
    ▼
 文件列表 ──逐个──► 读取(UTF-8 → 失败试 GBK → 再失败记坏账跳过)
                        │
                        ▼
                   清洗(小写/去网址邮箱/规范空白)
                        │
                        ▼
                   统计(词频计数器 + 出现文件集合)
                        │
    ┌───────────────────┴────────────────┐
    ▼                                    ▼
 控制台报告(对齐输出)            JSON 报告落盘(时间戳文件名)
```

对照 Day 02 的清洗流水线和 Day 28 的文档流水线:**同一个形状,中间站在换工作内容**。这是第三次见到这个架构了——它就是数据工程的"标准姿势"。

## 4.3 核心实现讲解(完整代码见 code/keyword_stats.py)

```python
def read_text_smart(path: Path) -> str | None:
    """智能读取文本:UTF-8 → GBK 逐个尝试;都失败返回 None。

    EAFP 的教科书应用:不去'检测'编码(检测本质是猜),
    直接试着读,读坏了(UnicodeDecodeError)换下一种。
    """
    for encoding in ("utf-8", "gbk"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue                      # 这套翻译规则不对,换下一套
        except OSError:                   # 文件读不了(权限/损坏):也是坏文件
            return None
    return None                           # 所有编码都失败


def clean_text(text: str) -> str:
    """清洗:小写 → 正则去网址/邮箱 → 规范空白。"""
    text = text.lower()
    text = re.sub(r"https?://\S+", " ", text)         # 网址:http(s):// 后面一串非空白
    text = re.sub(r"[\w.]+@[\w.]+", " ", text)        # 邮箱(简化模式,注释是纪律)
    return " ".join(text.split())                     # Day 02 的老朋友收尾


def count_keywords(text: str, keywords: list, counter: dict,
                   file_sets: dict, filename: str) -> None:
    """统计一个文件:词频进 counter,出现过的文件进 file_sets 的集合。"""
    for kw in keywords:
        n = text.count(kw)                            # 出现次数(Day 02 的 count)
        if n > 0:
            counter[kw] = counter.get(kw, 0) + n      # 焊死的三行第 N 次上岗
            file_sets[kw].add(filename)               # 集合自动去重:一个文件只算一次
```

主流程(节选):

```python
def main() -> None:
    start = datetime.now()                            # 计时起点
    keywords = ["退款", "发票", "物流", "会员", "优惠券", "投诉"]

    counter: dict = {}
    file_sets: dict = {kw: set() for kw in keywords}  # 字典推导式:每个词一个空集合
    ok_files, bad_files, total_chars = [], [], 0

    for path in Path("sample_docs").rglob("*.txt"):   # 递归扫描
        text = read_text_smart(path)
        if text is None:                              # 坏文件:记账,不搞崩整批
            bad_files.append(str(path))
            continue
        text = clean_text(text)
        total_chars += len(text)
        count_keywords(text, keywords, counter, file_sets, path.name)
        ok_files.append(str(path))

    elapsed = (datetime.now() - start).total_seconds()

    # ── 控制台报告:按词频降序 ──
    print(f"{'关键词':<8}{'出现次数':>8}{'涉及文件数':>10}")
    for kw, n in sorted(counter.items(), key=lambda kv: -kv[1]):
        print(f"{kw:<8}{n:>8}{len(file_sets[kw]):>10}")

    # ── JSON 报告落盘:时间戳文件名 ──
    report = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "keyword_counts": counter,
        "keyword_files": {kw: sorted(s) for kw, s in file_sets.items()},   # 集合转列表:JSON 不认集合!
        "summary": {"ok": len(ok_files), "bad": len(bad_files),
                    "total_chars": total_chars, "elapsed_seconds": elapsed},
    }
    report_name = f"report_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    with open(report_name, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n报告已保存:{report_name}(成功 {len(ok_files)},跳过 {len(bad_files)},耗时 {elapsed:.2f}s)")
```

三个值得咀嚼的细节:①**字典推导式** `{kw: set() for kw in keywords}`——推导式家族的字典版,今天顺手解锁;②**集合转列表再进 JSON**——JSON 六种类型里没有集合,serialize 前必须转(排错手册见);③**每个文件名进集合而不是列表**——同一文件里词出现 10 次,"涉及文件数"也只该算 1,集合的去重语义精确匹配需求(Day 04 的选型心法验证)。

## 4.4 样例数据与验收

code/sample_docs/ 里预置了 4 个文件:2 个 UTF-8、1 个 GBK(用代码生成,模拟老系统导出)、1 个二进制假 txt(坏文件)。运行验收:GBK 被正确读出、坏文件被记账跳过、双份报告数据一致。

---

# 【常见错误与排错手册】Day 11 专属篇

**错误 1:用 "w" 模式打开重要文件,内容瞬间清空。** w 一开门就清空。追加用 "a";读用 "r"。已经清空的:去 Git 找上一次提交(`git checkout -- 文件`)——每日提交的价值时刻。

**错误 2:UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc4...。** 文件是 GBK(0xc4 是典型 GBK 首字节)。用 encoding="gbk" 读,或用今天的 read_text_smart 逐个试。

**错误 3:Windows 路径 `"C:\new\test.txt"` 里 \n \t 被转义。** Day 02 老坑重犯。三选一:r 前缀原始字符串、正斜杠、**pathlib(推荐,根治)**。

**错误 4:readlines 的行尾 \n 忘 strip,比较永远不相等。** `line == "退款"` 恒 False,因为实际是 `"退款\n"`。逐行处理第一件事:strip。

**错误 5:JSON 不认集合/日期。** `TypeError: Object of type set is not JSON serializable`。落盘前手动转换:集合 → sorted(列表);datetime → strftime 字符串。

**错误 6:csv 写文件忘 newline="",Windows 上隔行出现空行。** csv + open 的固定搭配,背下来。

**错误 7:正则忘 r 前缀,\d 之类偶尔失灵。** `"\d"` 在普通字符串里侥幸能用,`"\b"` 就会坏(被 Python 先转义成退格符)。写正则永远 r 前缀,不给侥幸留机会。

**错误 8:re.search 返回 None 直接 .group()。** `AttributeError: 'NoneType' object has no attribute 'group'`。search/match 可能没找到,先 `if m:` 再用——find 返回 -1、get 返回 None、search 返回 None,三兄弟同一个防御姿势。

---

# 【课堂笔记】Day 11 知识点速查表

**文件读写**
- 铁律 1:凡 open 必 with;铁律 2:必带 encoding="utf-8"
- 模式:r 读(不存在报错)/ **w 写(清空!)**/ a 追加 / rb·wb 二进制
- 读三姿势:read() 一口吞 / readlines() 行列表(带 \n!)/ **for line in f 流式(推荐)**
- 乱码本质:写读两套翻译规则;Windows 默认 GBK 是万恶之源
- 两层翻译:ensure_ascii=False(对象→文本)+ encoding="utf-8"(文本→字节)

**csv**:`csv.writer(f).writerows(rows)`;读用 `csv.DictReader`(每行一个字典);open 加 `newline=""`;读出全是 str
**json 文件**:`json.dump(obj, f, ensure_ascii=False, indent=2)` / `json.load(f)`——四大函数集齐

**pathlib**
- `Path("a") / "b" / "c.txt"` 拼路径(跨平台);`.name/.stem/.suffix/.parent`(全是 property)
- `.exists()/.is_file()`;`mkdir(exist_ok=True)`;`read_text/write_text` 小文件快捷
- **glob("*.txt") / rglob("*.txt")**:批量找文件(Day 28 DirectoryLoader 的内核)

**datetime**
- `datetime.now()`;strftime 时间→字符串(%Y%m%d_%H%M%S 做文件名);strptime 反向
- `fromtimestamp(ts)` 翻译 Unix 时间戳;timedelta 时间加减;计时:两 now 相减 .total_seconds()

**re 正则(入门套餐)**
- 永远 r 前缀;零件:\d \w \s . * + ? {n} [a-z] ^ $ ()分组 \.转义
- 四函数:findall(全找)/ search(第一个,**判 None**)/ sub(模式替换)/ split(模式切分)
- 手机号:`r"1[3-9]\d{9}"`;网址:`r"https?://\S+"`
- 纪律:能字符串方法就不正则;模式必写注释;极端输入必测

**新解锁**:字典推导式 `{k: set() for k in keys}`;集合进 JSON 前转列表

---

# 【附录】课堂答疑实录(晚自习整理)

**问 1:read_text_smart 为什么不用"检测编码"的库(如 chardet)?**

答:可以用,但要理解它的本质:编码检测是**统计学猜测**(看字节分布像哪种编码),猜错率不为零,尤其短文本。我们的场景只有两个候选(UTF-8/GBK),逐个试错(EAFP)百分百准确且零依赖。候选编码多而未知时(处理国际化数据)再引入 chardet,并把它的结果当"建议"而不是"真理"。工程原则:能穷举就不要猜。

**问 2:with 能同时开两个文件吗?比如边读边写。**

答:能,一行逗号分隔:`with open(a, "r", encoding="utf-8") as fin, open(b, "w", encoding="utf-8") as fout:`。边读边写是"大文件转换"的标准姿势(逐行读入 → 处理 → 逐行写出,内存恒定)。另外自己写的类也能支持 with——实现 `__enter__` 和 `__exit__` 两个魔术方法即可(Day 09 家族的新成员,课程用到时再展开)。

**问 3:为什么 Day 07 的模板函数用 try/except 包 open,今天的 read_text_smart 也是?不能先 exists() 检查吗?**

答:能但不优。exists() 是 LBYL:检查和打开之间存在空窗(检查时在、打开时被别的程序删了/占了),而且 exists 只能防"不存在",防不了"存在但没权限"、"存在但编码错"。try/except 一网打尽所有打开失败的情形,这正是昨天 EAFP 一节说的"没有检查-使用空窗"的实例。文件操作是 EAFP 的主场。

**问 4:正则那张零件表根本记不住怎么办?**

答:不用记全,记住三样就够:①手机号和网址两个成品模式(高频直接抄);②`\d+`、`.*` 两个万金油;③"其他零件存在,用时查表"这个事实。真实工作流是:描述需求 → 查手册/问 AI 生成模式 → **用测试数据验证** → 加注释入库。第三步才是核心能力——AI 能帮你写正则,但验证对错、防住边角的责任在你。

**问 5:统计词频为什么用 text.count(kw) 而不是正则?会不会误伤?**

答:好眼力,会。count("会员") 会把"非会员"里的"会员"也算上——中文没有空格分词,子串匹配天然有误伤。今天接受这个粗糙(报告用途是"哪个主题热",量级对就行);精确方案是**中文分词**(jieba 库,把句子切成词再统计),属于 NLP 传统技术。有意思的是:Day 33 的混合检索里 BM25 算法同样需要分词,届时 jieba 正式登场——今天的"不完美"又一次成为未来课程的钩子。

**问 6:report 文件名带时间戳,那岂不是每跑一次多一个文件?**

答:对,这是刻意的设计选择:**报告是"快照",要保留历史**(对比上周和本周的词频变化就靠历史报告);如果每次覆盖同一个文件,历史就没了。反之,"当前状态"类数据(通讯录、会话存档)才用固定名覆盖。存储策略跟着数据语义走:快照留历史,状态存最新。顺带一提,生产系统的日志轮转(log rotation)就是这个思想的自动化版。

**问 7:今天学的东西和 pandas 是什么关系?我听说处理数据都用 pandas。**

答:pandas 是数据分析的重型武器(表格数据的全能操作),确实强大,但本课程刻意不引入它,两个原因:①我们的场景(文档处理、JSON 搬运)用标准库足够,引入重依赖违反"最小工具"原则;②pandas 有自己的一套心智模型(DataFrame),学习成本不低,而大模型应用开发者对它的需求远低于数据分析师。课程唯一可能碰它的地方是 Day 52 数据集处理(那时给最小速成)。如果你转数据分析方向,pandas 是必修;当前路线,标准库优先。

**问 8:明天就要真的调大模型 API 了,今晚该做什么准备?**

答:三件事:①**注册 DeepSeek 开放平台账号**(platform.deepseek.com),实名认证,创建 API Key——新用户有免费额度,课程实验绰绰有余;Key 生成后**立刻复制保存到本地记事本**(只显示一次),明天课上用;②确认 week2_project 的 venv 里已装 requests(Day 10 作业装过的举手);③把 Day 05 的 api_response_parser.py 翻出来重看一遍——明天的真实响应和它一字不差,你已经解析过一百遍了。明天是 70 天里的第一个"魔法时刻",睡好。

---

# 【明日预告】Day 12:网络请求与 API 调用(关键日!)

明天上午:HTTP 协议基础(GET/POST、状态码、Header、Body——用"寄快递"类比一次讲穿)+ requests 库详解;下午:**首次调用 DeepSeek API**——把 Day 05 彩排过的请求体真实发往 api.deepseek.com,拿回真实的 AI 回答;然后把这次调用封装进 chatlib 的 DeepSeekModel(Day 09 的模拟代码换成真引擎,接口纹丝不动——架构设计的回报日);最后写一个命令行 AI 问答小程序 🎉。两周的每一块积木,明天合体点火。

**睡前自检清单**:
- [ ] DeepSeek 平台已注册,API Key 已创建并保存
- [ ] with open + encoding 的铁律、w 模式的危险能脱口而出
- [ ] rglob 批量找文件、read_text_smart 双编码读取能默写思路
- [ ] keyword_stats.py 运行通过,双份报告数据一致
- [ ] LeetCode:LC 383(赎金信——字典计数器又一战)、LC 242(有效的字母异位词)
- [ ] 作业完成并 push,绿格子连续第 11 天
