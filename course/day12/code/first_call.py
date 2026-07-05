# =============================================
# first_call.py —— 你与大模型的第一次真实通话
# 每一行都是过去 12 天的某一课,注释里标了出处
# 运行前:
#   PowerShell:  $env:DEEPSEEK_API_KEY = "sk-你的key"
#   macOS/Linux: export DEEPSEEK_API_KEY="sk-你的key"
# =============================================
import os
import requests

API_URL = "https://api.deepseek.com/chat/completions"       # 常量(Day 01)

api_key = os.environ.get("DEEPSEEK_API_KEY")                 # 环境变量(Day 11/12)
if not api_key:
    raise RuntimeError("请先设置 DEEPSEEK_API_KEY 环境变量")   # 该崩就崩(Day 10)

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

# ── 当堂实验(逐个解开注释体验) ──
# 实验 1:把 Key 改错一个字母再跑 → 401,raise_for_status 抛 HTTPError
# 实验 2:把 "messages" 拼成 "message" → 400(你的锅)
# 实验 3:注释掉 raise_for_status,用错 Key 跑 → KeyError: 'choices'
#         (体会"漏了这行,错误在离真相很远的地方爆炸")
