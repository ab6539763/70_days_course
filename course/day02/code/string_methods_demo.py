# =============================================
# Day 02 · 下午演示代码:索引、切片与字符串方法
# 文件:string_methods_demo.py
# =============================================

# ---- 1. 索引:从 0 开始的储物柜编号 ----
s = "DeepSeek"
print(s[0])       # D     第一个字符是 0 号!
print(s[-1])      # k     负索引从右往左,-1 是最后一个
print(len(s))     # 8     len 是函数(独立),不是方法(长在对象上)
print(len("你好,世界"))    # 5   中文一个算一个

# ---- 2. 切片:含头不含尾 ----
print(s[0:4])     # Deep     取 0,1,2,3 号,4 号不要
print(s[:4])      # Deep     省略起点 = 从头
print(s[4:])      # Seek     省略终点 = 到尾
print(s[-4:])     # Seek     最后 4 个的惯用写法
print(s[::-1])    # keeSpeeD 步长 -1 = 反转

# 切片三个真实业务场景
phone = "13812345678"
print(phone[:3] + "****" + phone[-4:])    # 138****5678  手机号脱敏(Day 57 会复用)
filename = "第三季度财报.pdf"
print(filename[-4:])                       # .pdf         扩展名(Day 28 路由依据)
article = "大模型正在深刻改变软件开发的方式,应用层开发者迎来了历史性机遇"
print(article[:15] + "...")                # 超长文本截断预览(Day 27 记忆截断雏形)

# ---- 3. 字符串不可变:方法结果必须接住 ----
text = "  hello  "
text.strip()          # ❌ 白调用:结果没人接,原地蒸发
print(f"[{text}]")    # [  hello  ]  空格还在!
text = text.strip()   # ✅ 赋值接住
print(f"[{text}]")    # [hello]

# ---- 4. 清洗三剑客 ----
print("  张三  \n".strip())        # 张三          剥两端空白(含换行)
print("###标题###".strip("#"))    # 标题          也能剥指定字符
print("SHANGHAI".lower())          # shanghai
print("hello world".title())       # Hello World
# 标准清洗姿势:链式调用
print("  YES  ".strip().lower() == "yes")    # True(Day 14 判断 /exit 指令用这招)

# ---- 5. 查找与判断 ----
text = "Python 是大模型应用开发的第一语言"
print("大模型" in text)                     # True   最常用的包含判断
print(text.find("大模型"))                  # 8      首次出现的索引
print(text.find("Java"))                    # -1     找不到不报错,返回 -1
print("report_2026.pdf".endswith(".pdf"))   # True   文件类型路由
print("/exit 拜拜".startswith("/"))         # True   指令判断(Day 14 伏笔)
log = "ERROR: timeout. ERROR: retry failed. INFO: done"
print(log.count("ERROR"))                   # 2      统计次数

# ---- 6. 拆与拼:split / join(五星重要) ----
csv_line = "张三,28,上海,大模型工程师"
fields = csv_line.split(",")                # 拆成列表(明天 Day 04 的主角)
print(fields)                               # ['张三', '28', '上海', '大模型工程师']
print(fields[0], fields[2])                 # 张三 上海

print("the   quick  brown   fox".split())  # 不传参数:按任意空白拆,多余空格自动吞

words = ["Python", "LangChain", "RAG", "Agent"]
print(" → ".join(words))                    # 分隔符在前!读作"用箭头把 words 串起来"

# 组合拳:空格规范化(Day 28 文档清洗固定工序)
messy = "大模型   应用    开发"
print(" ".join(messy.split()))              # 大模型 应用 开发

# ---- 7. 替换 ----
text = "我喜欢Java,Java是最好的语言"
print(text.replace("Java", "Python"))       # 全部替换
print(text.replace("Java", "Python", 1))    # 只换第一个
print("138-1234-5678".replace("-", ""))     # 替换成空串 = 删除

# ---- 8. f-string 对齐:让输出像产品 ----
name = "张三"
print(f"[{name:<10}]")     # 左对齐占 10 格
print(f"[{name:>10}]")     # 右对齐
print(f"[{name:*^10}]")    # 星号填充居中

# 对齐表格实战
print(f"{'模型':<12}{'输入价':>8}{'输出价':>8}")
print("-" * 28)
print(f"{'deepseek-chat':<12}{1.0:>8.2f}{4.0:>8.2f}")
print(f"{'gpt-4o':<12}{18.0:>8.2f}{72.0:>8.2f}")
