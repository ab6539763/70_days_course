# =============================================
# Day 12 · 上午演示代码:requests 库基础
# 文件:http_demo.py
# 依赖:pip install requests(在 .venv 里!装完 pip freeze 更新清单)
# =============================================
import requests

# ---- 1. GET:向公开测试接口"取件" ----
# httpbin.org:练 HTTP 的公益网站,会把你的请求原样描述给你
response = requests.get("https://httpbin.org/get", timeout=10)
print(response.status_code)      # 200
print(type(response.text))       # <class 'str'>:响应体的原始文本

data = response.json()           # 糖:等价于 json.loads(response.text)——Day 05 直接接轨
print(type(data))                # <class 'dict'>

# ---- 2. POST:寄出一个 JSON ----
payload = {"name": "张三", "question": "什么是HTTP?"}

response = requests.post(
    "https://httpbin.org/post",
    json=payload,               # ★ json= 三合一糖:自动 dumps + Content-Type + 编码
    timeout=10,                 # ★ timeout 是纪律不是选项:没有它可能永远卡死
)
print(response.status_code)
print(response.json()["json"])   # httpbin 把你寄的货原样回显在 "json" 字段

# ---- 3. 请求头 + 错误处理的标准三层(Day 10 军规的网络落地) ----
url = "https://httpbin.org/status/401"      # 这个地址故意返回 401,用来练分诊

headers = {
    "Authorization": "Bearer sk-demo-key",   # 认证头格式铁律:Bearer + 空格 + Key
}

try:
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()          # ★ 非 2xx 抛 HTTPError
                                     #   不写这句:4xx/5xx 静默拿到错误响应,
                                     #   在下游的"第一名句"处莫名 KeyError
    print(resp.json())
except requests.Timeout:
    print("请求超时,稍后重试")        # 环境错误:接住补救
except requests.ConnectionError:
    print("网络不通,检查网络")
except requests.HTTPError as e:
    print(f"HTTP 错误:{e.response.status_code}")    # 分状态码处置:429 重试/401 查 Key

# ---- 4. 状态码速查(打印一遍加深记忆) ----
STATUS_GUIDE = {
    200: "成功:解析响应",
    400: "请求有误:修代码(你的锅)",
    401: "未认证:查 API Key(你的锅)",
    402: "余额不足:充值",
    429: "限流:等待后重试(唯一可重试的 4xx)",
    500: "服务器错误:稍后重试(它的锅)",
}
for code, action in STATUS_GUIDE.items():
    print(f"  {code}{action}")
