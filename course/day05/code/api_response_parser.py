# =============================================
# API 响应解析器
# 需求编号:REQ-D05-001
# 这是 Day 12 首次真实调用 API 的完整彩排:
#   届时唯一的区别是——raw_response 不再是写死的字符串,
#   而是 requests 库从 api.deepseek.com 真实收回来的
# =============================================
import json

# ---- 样例报文:与真实 DeepSeek API 返回结构一字不差 ----
raw_response = """
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "created": 1751702400,
  "model": "deepseek-chat",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Python是一种简洁优雅的编程语言,特别适合数据处理与AI应用开发。"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 12,
    "completion_tokens": 25,
    "total_tokens": 37
  }
}
"""

# ---- 定价常量(虚拟价,以官网为准) ----
PRICE_INPUT_PER_M = 1.0      # 输入:元/百万 token
PRICE_OUTPUT_PER_M = 4.0     # 输出:元/百万 token

# ---- 第一步:解析(字符串 → 字典) ----
data = json.loads(raw_response)
print(type(data))            # <class 'dict'> 确认解析成功

# ---- 第二步:提取核心字段 ----
# 回答正文:必要字段,用方括号——没有它说明调用失败,崩溃即报警。
# 这一行是大模型应用开发的"第一名句",从 Day 12 用到毕业设计:
content = data["choices"][0]["message"]["content"]

# 结束原因:length 意味着回答被 max_tokens 截断(Day 16 详解)
finish_reason = data["choices"][0]["finish_reason"]

# 模型名:可选展示信息,用 get 更稳
model = data.get("model", "未知模型")

# 用量:可选字段,双层防御——外层 get 空字典兜底,内层 get 数字 0 兜底
usage = data.get("usage", {})
tokens_in = usage.get("prompt_tokens", 0)
tokens_out = usage.get("completion_tokens", 0)
tokens_total = usage.get("total_tokens", 0)

# ---- 第三步:成本计算 ----
cost = (tokens_in / 1_000_000 * PRICE_INPUT_PER_M
        + tokens_out / 1_000_000 * PRICE_OUTPUT_PER_M)

# ---- 第四步:格式化报告(Day 02 的对齐语法) ----
print("=" * 50)
print(f"{'API 调用报告':^46}")
print("=" * 50)
print(f"{'模型':<8}{model}")
print(f"{'结束原因':<8}{finish_reason}")
print(f"{'输入tokens':<10}{tokens_in:>6}")
print(f"{'输出tokens':<10}{tokens_out:>6}")
print(f"{'总tokens':<10}{tokens_total:>6}")
print(f"{'本次成本':<8}{cost:.6f} 元")
print("-" * 50)
print("模型回答:")
print(content)
print("=" * 50)

# ---- 第五步:反向练习——组装并序列化一份请求体 ----
# 这就是 Day 12 要"发出去"的东西,今天先学会打包
request_body = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "system", "content": "你是一个乐于助人的AI助手"},
        {"role": "user", "content": "用一句话介绍Python"}
    ],
    "temperature": 0.7,
    "max_tokens": 200,
    "stream": False
}

request_json = json.dumps(request_body, ensure_ascii=False, indent=2)
print("请求体 JSON(即将在 Day 12 发往 api.deepseek.com):")
print(request_json)

# 无损往返验证(需求验收项)。assert:断言,"我断定此事为真,若假立刻报错"
assert json.loads(request_json) == request_body
print("✓ 序列化-解析往返验证通过")

# ---- 加练:字段缺失的容错测试 ----
# 残缺报文:没有 usage(某些代理接口真的会这样)
raw_no_usage = '{"model": "deepseek-chat", "choices": [{"index": 0, "message": {"role": "assistant", "content": "你好!"}, "finish_reason": "stop"}]}'

data2 = json.loads(raw_no_usage)
usage2 = data2.get("usage", {})                    # 没有 usage → 空字典,不崩
print(usage2.get("total_tokens", 0))               # 空字典再 get → 0,依然不崩
content2 = data2["choices"][0]["message"]["content"]   # 必要字段照常方括号
print(content2)                                    # 你好!
print("✓ 容错测试通过")
