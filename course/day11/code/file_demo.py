# =============================================
# Day 11 · 上午演示代码 1:文件读写全解
# 文件:file_demo.py
# 铁律 1:凡 open 必 with;铁律 2:必带 encoding="utf-8"
# =============================================
import csv
import json

# ---- 1. with 写文件(w 会清空!追加用 a) ----
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("第一行笔记\n")                   # \n 手动换行
    f.write("第二行笔记\n")
# 出了缩进块自动 close(哪怕中途异常)——with 是 try/finally 的封装

with open("notes.txt", "a", encoding="utf-8") as f:     # a:追加,不清空
    f.write("第三行:追加的\n")

# ---- 2. 读的三种姿势 ----
# 姿势一:一口吞(小文件/要整体处理)
with open("notes.txt", "r", encoding="utf-8") as f:
    content = f.read()
print(repr(content))

# 姿势二:行列表(注意每行末尾带 \n!)
with open("notes.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
print(lines)                                  # ['第一行笔记\n', ...]
clean_lines = [line.strip() for line in lines]        # 标准动作:逐行 strip
print(clean_lines)

# 姿势三:流式逐行(推荐:内存里永远只有一行)
with open("notes.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:                          # 跳过空行:处理真实文件的标配
            continue
        print(f"处理:{line}")

# ---- 3. 编码之谜演示:故意制造一次乱码 ----
with open("gbk_file.txt", "w", encoding="gbk") as f:   # 模拟老系统导出
    f.write("你好,老系统")

try:
    with open("gbk_file.txt", "r", encoding="utf-8") as f:
        f.read()
except UnicodeDecodeError as e:
    print(f"用 UTF-8 读 GBK 文件:{type(e).__name__}(翻译规则不对)")

with open("gbk_file.txt", "r", encoding="gbk") as f:   # 换对翻译规则
    print("用 GBK 读:", f.read())

# ---- 4. CSV 读写 ----
rows = [
    ["姓名", "岗位", "评分"],
    ["张三", "大模型工程师", 92],
    ["李四", "产品经理, AI方向", 88],          # 字段里有逗号:csv 模块自动加引号保护
]
with open("staff.csv", "w", encoding="utf-8", newline="") as f:
    # newline="":csv + open 的固定搭配(防 Windows 空行)
    writer = csv.writer(f)
    writer.writerows(rows)

with open("staff.csv", "r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)                # 第一行自动当表头,每行是字典
    for row in reader:
        # csv 读出来的一切都是字符串!评分要用得 int()——input 老坑重演
        print(f"{row['姓名']}{row['岗位']},评分 {int(row['评分'])}")

# ---- 5. JSON 文件:load/dump 转正(四大函数集齐) ----
config = {"model": "deepseek-chat", "temperature": 0.7, "tags": ["生产", "客服"]}

with open("config.json", "w", encoding="utf-8") as f:
    json.dump(config, f, ensure_ascii=False, indent=2)    # dump:对象→文件

with open("config.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)                                  # load:文件→对象

assert loaded == config
print("✓ json 往返无损;四大函数集齐:loads/dumps 管字符串,load/dump 管文件")
