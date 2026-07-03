"""Day 5: 解析模拟 API 返回的 JSON"""
import json

MOCK_API_RESPONSE = """
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "model": "deepseek-chat",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "你好！我是 AI 助手，有什么可以帮你的？"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 20,
    "total_tokens": 30
  }
}
"""


def parse_api_response(json_str: str) -> dict:
    data = json.loads(json_str)
    return {
        "model": data["model"],
        "reply": data["choices"][0]["message"]["content"],
        "role": data["choices"][0]["message"]["role"],
        "total_tokens": data["usage"]["total_tokens"],
    }


def main():
    result = parse_api_response(MOCK_API_RESPONSE)
    print("=" * 40)
    print(f"模型: {result['model']}")
    print(f"角色: {result['role']}")
    print(f"回复: {result['reply']}")
    print(f"Token 消耗: {result['total_tokens']}")
    print("=" * 40)


if __name__ == "__main__":
    main()
