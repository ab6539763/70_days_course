# =============================================
# Day 05 · 下午演示代码:json 模块四大函数
# 文件:json_demo.py
# 记忆图:
#   JSON字符串 --loads--> Python对象 --dumps--> JSON字符串
#   带 s 管字符串(今天);load/dump 不带 s 管文件(Day 11)
# =============================================
import json                      # 标准库,无需安装

# ---- 1. loads:解析(收到的报文 → 能操作的字典) ----
raw = '{"name": "张三", "age": 28, "skills": ["python", "sql"], "is_vip": true}'
print(type(raw))                 # <class 'str'>:现在还是文本,动不了字段

data = json.loads(raw)           # 解析
print(type(data))                # <class 'dict'>:活了
print(data["name"])              # 张三
print(data["skills"][0])         # python
print(data["is_vip"])            # True:JSON 的 true 自动翻译成 Python 的 True

# 类型自动翻译:object→dict, array→list, string→str,
#               number→int/float, true/false→True/False, null→None

# ---- 2. dumps:序列化(字典 → 能发送/保存的文本) ----
request = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "user", "content": "你好"}
    ],
    "temperature": 0.7,
    "stream": False
}

text = json.dumps(request)
print(text)                      # False 变成了 false:Python → JSON 自动翻译

# 两个必会参数:
# ensure_ascii=False → 中文原样输出(不加会变成 \u4f60\u597d 天书)
# indent=2           → 缩进美化(调试/存盘用;网络传输不加,省流量)
pretty = json.dumps(request, ensure_ascii=False, indent=2)
print(pretty)

# ---- 3. 无损往返:持久化和网络通信的本质 ----
original = {"task": "学JSON", "tags": ["重点", "API"], "hours": 3.5, "done": None}
roundtrip = json.loads(json.dumps(original, ensure_ascii=False))
print(roundtrip == original)     # True:完美还原

# ---- 4. 解析失败:JSONDecodeError 三大来源 ----
# ① 单引号  ② 尾逗号  ③ 大写的 True/False/None
bad = "{'name': '张三'}"          # 单引号:Python 字典合法,JSON 非法
try:                              # try/except Day 10 正式学,今天先见一面:
    json.loads(bad)               # "尝试解析,失败也别崩,进 except"
except json.JSONDecodeError as e:
    print(f"解析失败:{e}")        # Expecting property name enclosed in double quotes
