# =============================================
# Day 11 · 演示代码 2:pathlib / datetime / re
# 文件:stdlib_demo.py
# =============================================
import re
from datetime import datetime, timedelta
from pathlib import Path

# ════════ pathlib:文件系统的遥控器 ════════

# 拼路径用 /:自动适配 Windows\ 和 mac/(消灭转义地狱)
p = Path("docs") / "reports" / "q3.txt"
print(p)

# 路径对象的属性(全是 property:Day 09 知识在标准库的真身)
p = Path("docs/深度学习入门.pdf")
print(p.name)          # 深度学习入门.pdf
print(p.stem)          # 深度学习入门
print(p.suffix)        # .pdf(Day 02 切片取后缀的正规军)
print(p.parent)        # docs

# 建目录 / 小文件快捷读写
Path("output").mkdir(exist_ok=True)
Path("output/note.txt").write_text("你好", encoding="utf-8")
print(Path("output/note.txt").read_text(encoding="utf-8"))

# glob:批量找文件(今天下午实操的心脏;Day 28 DirectoryLoader 的内核)
Path("output/sub").mkdir(exist_ok=True)
Path("output/a.txt").write_text("a", encoding="utf-8")
Path("output/sub/b.txt").write_text("b", encoding="utf-8")
print(list(Path("output").glob("*.txt")))       # 当前层
print(list(Path("output").rglob("*.txt")))      # 递归连子目录

# ════════ datetime:时间的翻译官 ════════

now = datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))        # 格式化(f=format)
print(now.strftime("%Y%m%d_%H%M%S"))            # 做文件名的标准姿势

dt = datetime.strptime("2026-07-05 09:00", "%Y-%m-%d %H:%M")    # 解析(p=parse)
print(dt)

# Day 05 的 1751702400 之谜正式破案
print(datetime.fromtimestamp(1751702400))       # Unix 时间戳 → 人话
print(int(now.timestamp()))                     # 反向

# 时间运算
deadline = now + timedelta(days=7)
print(f"作业截止:{deadline.strftime('%m月%d日')}")
print((deadline - now).days, (deadline - now).total_seconds())

# ════════ re 正则:入门套餐 ════════

text = "联系张经理 13812345678 或李助理 15987654321,座机 021-6543-2100"

# findall:全部匹配。模式解读:1 + [3-9]一位 + \d{9} 九位数字
phones = re.findall(r"1[3-9]\d{9}", text)       # r 前缀:写正则的肌肉记忆
print(phones)          # 座机不会被误抓

# search:第一个匹配,返回 Match 或 None(用前必判!)
text2 = "订单A2026,联系 zhang.san@deepseek.com"
m = re.search(r"(\w[\w.]*)@([\w.]+)", text2)    # 括号分组:用户名/域名
if m:
    print(m.group(0), "|", m.group(1), "|", m.group(2))

# sub:模式替换(手机脱敏的正则版)
print(re.sub(r"1[3-9]\d{9}", "1**********", "手机 13812345678 已登记"))

# split:模式切分(Day 02 中文逗号之坑的终极解:中英文标点通吃)
print(re.split(r"[,;,;]\s*", "苹果,香蕉; 橙子,梨"))

# 常用成品模式(高频直接抄)
URL_PATTERN = r"https?://\S+"                    # 网址
print(re.findall(URL_PATTERN, "见 https://docs.deepseek.com 和 http://a.b/c"))
