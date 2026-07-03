# Day 16: 大模型 API 核心参数

> **培训阶段**: 第二阶段 大模型理论与 API | **第 3 周** | **学习时长**: 约 6-8 小时  
> **今日关键词**: temperature、top_p、max_tokens、角色 system/user/assistant、流式输出 stream

---

## 📍 课程导航

### 上节回顾
**Day 15** 我们学习了：

- NLP 发展史与 Transformer 架构原理
- 预训练 → SFT → RLHF 三阶段训练流程
- Token 概念、tiktoken 实操与成本估算
- 主流大模型盘点与选型建议

今天在此基础上，深入掌握 **API 调用的「旋钮」**——每一个参数如何影响模型行为。

### 本节学习目标
完成本日学习后，你将能够：

1. 理解并正确设置 `temperature`、`top_p`、`max_tokens` 等核心参数
2. 掌握 `presence_penalty`、`frequency_penalty`、`stop` 等进阶参数
3. 设计合理的 `system` / `user` / `assistant` 角色消息结构
4. 实现流式输出（stream），打造逐字显示的 AI 对话体验
5. 通过对比实验总结不同场景下的参数调优策略

### 与后续课程的衔接
- **Day 5** JSON 格式 → 今天 API 请求体就是 JSON，`messages` 数组是核心结构
- **Day 8** 函数封装 → 今天将把 API 调用封装为可复用的 `chat()` 函数
- **Day 12** 首次 API 调用 → 今天补全当时略过的参数细节
- **Day 17-18** Prompt 工程 → 参数调优与 Prompt 设计相辅相成
- **Day 24** FastAPI SSE 流式接口 → 今天的 stream 代码将升级为 Web 服务

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：API 请求结构回顾

#### 1.1 Chat Completions API 基本结构

```python
# Day 12 基础调用回顾 + Day 16 完整参数
import os
import requests

API_KEY = os.getenv("DEEPSEEK_API_KEY")
BASE_URL = "https://api.deepseek.com/v1/chat/completions"

def chat(messages: list, **kwargs) -> dict:
    """通用聊天 API 封装"""
    payload = {
        "model": kwargs.get("model", "deepseek-chat"),
        "messages": messages,
        "temperature": kwargs.get("temperature", 1.0),
        "top_p": kwargs.get("top_p", 1.0),
        "max_tokens": kwargs.get("max_tokens", 4096),
        "stream": kwargs.get("stream", False),
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(BASE_URL, json=payload, headers=headers, timeout=60)
    response.raise_for_status()
    return response.json()
```

#### 1.2 messages 数组：对话的载体

```python
messages = [
    {"role": "system", "content": "你是一个专业的 Python 编程助手。"},
    {"role": "user", "content": "什么是列表推导式？"},
    {"role": "assistant", "content": "列表推导式是 Python 中..."},
    {"role": "user", "content": "给我一个例子"},
]
```

**messages 规则**

| 规则 | 说明 |
|------|------|
| 顺序 | 按时间顺序排列，模拟真实对话 |
| role 取值 | `system`、`user`、`assistant`（部分 API 支持 `tool`） |
| system 位置 | 通常放在最前面，全局生效 |
| 多轮对话 | 需把历史 user/assistant 消息都传入 |

> 💡 **与 Day 15 的联系**：messages 中所有 content 的 Token 之和计入输入 Token，占用上下文窗口。

---

### 9:45 - 10:30 | 模块二：核心生成参数详解

#### 2.1 temperature（温度）

**作用**：控制输出的随机性/创造性。

```
temperature = 0.0          temperature = 1.0          temperature = 2.0
┌─────────────┐           ┌─────────────┐           ┌─────────────┐
│ 几乎确定性   │           │ 平衡创造与准确 │           │ 高度随机     │
│ 每次输出相同  │           │ 默认推荐值   │           │ 可能不连贯   │
└─────────────┘           └─────────────┘           └─────────────┘
```

| 场景 | 推荐 temperature | 原因 |
|------|-----------------|------|
| 代码生成 | 0.0 - 0.2 | 需要精确、可复现 |
| 数据分析/提取 | 0.0 - 0.3 | 需要准确的事实 |
| 通用对话 | 0.5 - 0.8 | 自然且有变化 |
| 创意写作 | 0.8 - 1.2 | 需要多样性和灵感 |
| 头脑风暴 | 1.0 - 1.5 | 追求新颖想法 |

**原理简述**：temperature 缩放 logits（未归一化概率），越高则概率分布越平坦，低概率 Token 也有机会被选中。

```python
# day16/temperature_experiment.py
"""同一问题，不同 temperature 的输出对比"""

import os
import requests

API_KEY = os.getenv("DEEPSEEK_API_KEY")
URL = "https://api.deepseek.com/v1/chat/completions"

def ask(prompt: str, temperature: float) -> str:
    resp = requests.post(URL, json={
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": 100,
    }, headers={"Authorization": f"Bearer {API_KEY}"}, timeout=30)
    return resp.json()["choices"][0]["message"]["content"]

prompt = "用一个比喻解释什么是云计算"
for temp in [0.0, 0.5, 1.0, 1.5]:
    print(f"\n=== temperature={temp} ===")
    print(ask(prompt, temp))
```

#### 2.2 top_p（核采样）

**作用**：只从累积概率达到 top_p 的 Token 中采样。

| top_p | 效果 |
|-------|------|
| 1.0 | 考虑所有 Token（默认） |
| 0.9 | 排除最低 10% 概率的 Token |
| 0.1 | 只考虑最高概率的少数 Token |

**temperature vs top_p**

| 维度 | temperature | top_p |
|------|-------------|-------|
| 调节方式 | 缩放所有概率 | 截断低概率 Token |
| 推荐 | 二选一调节，不要同时大幅调整 | 一般固定 top_p=1，调 temperature |

> 💡 **实践建议**：优先调 temperature，top_p 保持默认 1.0。同时大幅调整两者会让行为难以预测。

#### 2.3 max_tokens（最大输出 Token 数）

**作用**：限制模型生成的最大 Token 数量。

```python
# 短回答场景
payload = {"max_tokens": 150, ...}  # 约 100 字中文

# 长文生成场景
payload = {"max_tokens": 4096, ...}  # 约 3000 字中文
```

**注意事项**

| 要点 | 说明 |
|------|------|
| 仅限制输出 | 不计入输入 Token |
| 上下文窗口 | 输入 Token + max_tokens ≤ 上下文窗口 |
| 费用控制 | max_tokens 越大，最大可能费用越高 |
| 截断 | 达到 max_tokens 时输出可能被截断（无完整结束） |

```python
# 计算安全的 max_tokens
from day15.token_counter import count_tokens  # 假设在同项目

input_tokens = count_tokens(system_prompt + user_message)
context_window = 64000  # DeepSeek-V3
safe_max_tokens = context_window - input_tokens - 100  # 留 100 Token 缓冲
```

#### 2.4 presence_penalty 与 frequency_penalty

**presence_penalty（存在惩罚）**：惩罚已出现过的 Token（不管出现几次），鼓励谈论新话题。

**frequency_penalty（频率惩罚）**：按出现次数惩罚，减少重复用词。

| 参数 | 范围 | 效果 | 适用场景 |
|------|------|------|----------|
| presence_penalty | -2.0 ~ 2.0 | 减少重复主题 | 长文创作 |
| frequency_penalty | -2.0 ~ 2.0 | 减少重复用词 | 避免「很好很好很好」 |

```python
# 减少重复的推荐设置
payload = {
    "presence_penalty": 0.6,
    "frequency_penalty": 0.3,
}
```

#### 2.5 stop（停止序列）

**作用**：遇到指定字符串时立即停止生成。

```python
# 生成 JSON 时，遇到闭合括号停止
payload = {
    "stop": ["\n\n", "```"],
}

# 多轮对话中防止模型模拟用户
payload = {
    "stop": ["\n用户:", "\nUser:"],
}
```

#### 2.6 参数速查表

| 参数 | 类型 | 默认值 | 作用 |
|------|------|--------|------|
| model | str | — | 模型名称 |
| messages | list | — | 对话消息数组 |
| temperature | float | 1.0 | 随机性控制 |
| top_p | float | 1.0 | 核采样 |
| max_tokens | int | 模型默认 | 最大输出长度 |
| presence_penalty | float | 0 | 主题重复惩罚 |
| frequency_penalty | float | 0 | 用词重复惩罚 |
| stop | list[str] | null | 停止序列 |
| stream | bool | false | 流式输出 |
| n | int | 1 | 生成几个回答 |
| seed | int | null | 随机种子（部分模型支持） |

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：角色（Role）详解

#### 3.1 三种核心角色

```
┌─────────────────────────────────────────────────────────┐
│  system（系统）                                          │
│  · 设定 AI 的身份、能力边界、行为规则                      │
│  · 用户看不到（部分 UI 会展示）                           │
│  · 对整个对话全局生效                                     │
├─────────────────────────────────────────────────────────┤
│  user（用户）                                            │
│  · 用户的输入/问题                                       │
│  · 每轮对话触发一次模型回复                               │
├─────────────────────────────────────────────────────────┤
│  assistant（助手）                                       │
│  · 模型的历史回复                                        │
│  · 用于多轮对话的上下文                                   │
│  · 也可用于 Few-shot 示例（Day 17）                      │
└─────────────────────────────────────────────────────────┘
```

#### 3.2 system prompt 设计原则

**好的 system prompt**

```python
system_prompt = """你是一位资深 Python 编程导师，专门帮助零基础学员学习编程。

## 你的特点
- 用通俗易懂的语言解释概念，善用类比
- 代码示例简洁，不超过 20 行
- 鼓励学员动手实践

## 你的限制
- 只回答 Python 和编程相关问题
- 不提供有害或违法内容
- 不确定时坦诚说「我不确定」

## 输出格式
- 先给出简短回答，再展开详细解释
- 代码用 ```python 代码块包裹
"""
```

**差的 system prompt**

```python
# ❌ 太模糊
system_prompt = "你是一个有帮助的助手。"

# ❌ 太长太啰嗦（浪费 Token）
system_prompt = "请你扮演一个非常非常专业的..." * 100

# ❌ 自相矛盾
system_prompt = "详细回答所有问题，但每个回答不超过 10 个字。"
```

#### 3.3 多轮对话管理

```python
# day16/chat_session.py
"""多轮对话会话管理"""

class ChatSession:
    def __init__(self, system_prompt: str = "你是一个有帮助的AI助手。"):
        self.messages = [{"role": "system", "content": system_prompt}]

    def send(self, user_input: str, chat_func) -> str:
        """发送用户消息，获取 AI 回复"""
        self.messages.append({"role": "user", "content": user_input})
        response = chat_func(self.messages)
        assistant_msg = response["choices"][0]["message"]["content"]
        self.messages.append({"role": "assistant", "content": assistant_msg})
        return assistant_msg

    def clear_history(self, keep_system: bool = True):
        """清除对话历史"""
        if keep_system:
            self.messages = [self.messages[0]]
        else:
            self.messages = []

    def get_token_estimate(self) -> int:
        """估算当前对话的 Token 数"""
        total = 0
        for msg in self.messages:
            total += len(msg["content"])
        return total // 2  # 粗略估算，精确计算用 tiktoken
```

#### 3.4 角色实战：不同场景的 system prompt

| 场景 | system prompt 要点 |
|------|-------------------|
| 代码助手 | 指定语言、代码风格、是否解释 |
| 翻译官 | 源语言、目标语言、正式/口语 |
| 数据分析师 | 输出格式（表格/JSON）、精度要求 |
| 客服机器人 | 语气、知识范围、转人工条件 |
| 写作助手 | 文体、字数、受众 |

```python
# 场景示例：JSON 数据提取助手
extractor_system = """你是数据提取专家。用户会给你一段非结构化文本，你需要提取关键信息并以 JSON 格式返回。

规则：
1. 只返回 JSON，不要其他文字
2. JSON 必须可以被 Python json.loads() 解析
3. 缺失字段用 null 表示
4. 日期格式统一为 YYYY-MM-DD
"""
```

---

## 🌆 下午课程（14:00 - 17:00）

### 14:00 - 15:15 | 模块四：流式输出（Stream）

#### 4.1 为什么需要流式输出

| 对比 | 非流式 | 流式 |
|------|--------|------|
| 用户体验 | 等待数秒后一次性显示 | 逐字显示，类似打字 |
| 首字延迟 | 等于总生成时间 | 通常 < 1 秒 |
| 实现复杂度 | 简单 | 需处理 SSE 数据流 |
| 适用场景 | 批处理、短回答 | 聊天 UI、长文生成 |

#### 4.2 流式 API 原理

```
客户端                          服务端
   │                              │
   │  POST /chat/completions      │
   │  {"stream": true}            │
   │ ─────────────────────────→   │
   │                              │
   │  data: {"choices":[{"delta": │
   │    {"content":"你"}}]}        │
   │ ←─────────────────────────   │
   │  data: {"choices":[{"delta": │
   │    {"content":"好"}}]}        │
   │ ←─────────────────────────   │
   │  data: {"choices":[{"delta": │
   │    {"content":"！"}}]}       │
   │ ←─────────────────────────   │
   │  data: [DONE]                │
   │ ←─────────────────────────   │
```

**响应格式**：Server-Sent Events (SSE)，每行以 `data: ` 开头。

#### 4.3 Python 流式输出实现

```python
# day16/stream_chat.py
"""流式输出聊天实现"""

import os
import json
import requests
import sys

API_KEY = os.getenv("DEEPSEEK_API_KEY")
URL = "https://api.deepseek.com/v1/chat/completions"


def stream_chat(messages: list, **kwargs) -> str:
    """流式聊天，逐字打印，返回完整回复"""
    payload = {
        "model": kwargs.get("model", "deepseek-chat"),
        "messages": messages,
        "temperature": kwargs.get("temperature", 0.7),
        "max_tokens": kwargs.get("max_tokens", 2048),
        "stream": True,
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.post(URL, json=payload, headers=headers, stream=True, timeout=60)
    response.raise_for_status()

    full_content = ""
    print("AI: ", end="", flush=True)

    for line in response.iter_lines():
        if not line:
            continue
        line = line.decode("utf-8")
        if not line.startswith("data: "):
            continue
        data = line[6:]  # 去掉 "data: " 前缀
        if data == "[DONE]":
            break
        chunk = json.loads(data)
        delta = chunk["choices"][0].get("delta", {})
        content = delta.get("content", "")
        if content:
            print(content, end="", flush=True)
            full_content += content

    print()  # 换行
    return full_content


def interactive_chat():
    """交互式流式聊天"""
    messages = [
        {"role": "system", "content": "你是一个友好的AI助手，回答简洁明了。"}
    ]
    print("流式聊天助手（输入 quit 退出）\n")

    while True:
        user_input = input("你: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            print("再见！")
            break
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})
        reply = stream_chat(messages)
        messages.append({"role": "assistant", "content": reply})
        print()


if __name__ == "__main__":
    interactive_chat()
```

#### 4.4 流式输出的错误处理

```python
# day16/stream_robust.py
"""健壮的流式输出——含错误处理"""

import json
import requests


def safe_stream_chat(messages: list) -> str:
    """带错误处理的流式聊天"""
    try:
        response = requests.post(URL, json={
            "model": "deepseek-chat",
            "messages": messages,
            "stream": True,
        }, headers={"Authorization": f"Bearer {API_KEY}"}, stream=True, timeout=60)

        if response.status_code != 200:
            error_body = response.json()
            raise Exception(f"API 错误 {response.status_code}: {error_body}")

        full_content = ""
        for line in response.iter_lines():
            if not line:
                continue
            line = line.decode("utf-8")
            if line.startswith("data: "):
                data = line[6:]
                if data == "[DONE]":
                    break
                try:
                    chunk = json.loads(data)
                    # 检查是否有错误
                    if "error" in chunk:
                        raise Exception(chunk["error"]["message"])
                    content = chunk["choices"][0].get("delta", {}).get("content", "")
                    if content:
                        print(content, end="", flush=True)
                        full_content += content
                except json.JSONDecodeError:
                    continue  # 跳过无法解析的行

        return full_content

    except requests.exceptions.Timeout:
        print("\n⚠️ 请求超时，请重试")
        return ""
    except requests.exceptions.ConnectionError:
        print("\n⚠️ 网络连接失败")
        return ""
```

---

### 15:15 - 15:30 | 课间休息

---

### 15:30 - 17:00 | 模块五：参数对比实验

#### 5.1 综合实验框架

```python
# day16/parameter_lab.py
"""API 参数对比实验室"""

import os
import json
import time
import requests
from dataclasses import dataclass, asdict

API_KEY = os.getenv("DEEPSEEK_API_KEY")
URL = "https://api.deepseek.com/v1/chat/completions"


@dataclass
class ExperimentResult:
    params: dict
    response: str
    latency: float
    output_tokens: int


def run_experiment(prompt: str, params: dict) -> ExperimentResult:
    """运行单次实验"""
    messages = [{"role": "user", "content": prompt}]
    payload = {"model": "deepseek-chat", "messages": messages, **params}

    start = time.time()
    resp = requests.post(URL, json=payload,
                         headers={"Authorization": f"Bearer {API_KEY}"}, timeout=60)
    latency = time.time() - start
    data = resp.json()

    return ExperimentResult(
        params=params,
        response=data["choices"][0]["message"]["content"],
        latency=round(latency, 2),
        output_tokens=data["usage"]["completion_tokens"],
    )


def compare_experiments(prompt: str, param_sets: list[dict]) -> None:
    """对比多组参数的输出"""
    results = []
    for params in param_sets:
        print(f"\n{'='*60}")
        print(f"参数: {params}")
        result = run_experiment(prompt, params)
        results.append(result)
        print(f"延迟: {result.latency}s | 输出 Token: {result.output_tokens}")
        print(f"回答: {result.response[:200]}...")

    # 保存实验结果
    with open("day16/experiment_results.json", "w", encoding="utf-8") as f:
        json.dump([asdict(r) for r in results], f, ensure_ascii=False, indent=2)


# 实验一：temperature 对比
TEMPERATURE_TESTS = [
    {"temperature": 0.0, "max_tokens": 200},
    {"temperature": 0.7, "max_tokens": 200},
    {"temperature": 1.5, "max_tokens": 200},
]

# 实验二：惩罚参数对比
PENALTY_TESTS = [
    {"temperature": 0.7, "max_tokens": 300},
    {"temperature": 0.7, "max_tokens": 300, "frequency_penalty": 0.8},
    {"temperature": 0.7, "max_tokens": 300, "presence_penalty": 0.8},
]

if __name__ == "__main__":
    prompt = "请列举 5 个学习 Python 的好处，每个好处用一句话说明。"
    print("实验一：Temperature 对比")
    compare_experiments(prompt, TEMPERATURE_TESTS)
```

#### 5.2 场景化参数推荐配置

```python
# day16/presets.py
"""不同场景的参数预设"""

PRESETS = {
    "code": {
        "temperature": 0.1,
        "max_tokens": 2048,
        "description": "代码生成：低温度，高精确度",
    },
    "chat": {
        "temperature": 0.7,
        "max_tokens": 1024,
        "description": "日常对话：平衡自然与准确",
    },
    "creative": {
        "temperature": 1.0,
        "max_tokens": 4096,
        "presence_penalty": 0.5,
        "description": "创意写作：高温度，鼓励新颖",
    },
    "extract": {
        "temperature": 0.0,
        "max_tokens": 1024,
        "description": "数据提取：零温度，确保格式",
    },
    "translate": {
        "temperature": 0.3,
        "max_tokens": 2048,
        "description": "翻译：低温度，忠实原文",
    },
}


def get_preset(scene: str) -> dict:
    """获取场景预设参数"""
    if scene not in PRESETS:
        raise ValueError(f"未知场景: {scene}，可选: {list(PRESETS.keys())}")
    preset = PRESETS[scene].copy()
    preset.pop("description", None)
    return preset
```

#### 5.3 下午综合项目：可配置 AI 聊天 CLI

```python
# day16/smart_chat_cli.py
"""可配置参数的 AI 聊天命令行工具"""

import argparse
import os
from stream_chat import stream_chat

PRESETS = {
    "code": {"temperature": 0.1, "system": "你是 Python 编程专家。"},
    "chat": {"temperature": 0.7, "system": "你是友好的AI助手。"},
    "creative": {"temperature": 1.0, "system": "你是有创意的写作助手。"},
}


def main():
    parser = argparse.ArgumentParser(description="AI 聊天 CLI")
    parser.add_argument("--preset", choices=PRESETS.keys(), default="chat")
    parser.add_argument("--temperature", type=float, default=None)
    parser.add_argument("--max-tokens", type=int, default=2048)
    args = parser.parse_args()

    preset = PRESETS[args.preset]
    temperature = args.temperature if args.temperature is not None else preset["temperature"]
    messages = [{"role": "system", "content": preset["system"]}]

    print(f"模式: {args.preset} | temperature: {temperature}")
    print("输入 quit 退出\n")

    while True:
        user_input = input("你: ").strip()
        if user_input.lower() == "quit":
            break
        messages.append({"role": "user", "content": user_input})
        print("AI: ", end="")
        reply = stream_chat(messages, temperature=temperature, max_tokens=args.max_tokens)
        messages.append({"role": "assistant", "content": reply})
        print()


if __name__ == "__main__":
    main()
```

**运行**

```bash
python3 day16/smart_chat_cli.py --preset code --temperature 0.2
```

---

## 🌙 晚自习（19:00 - 21:00）

### 19:00 - 20:00 | 参数调优方法论

#### 调参流程

```
1. 确定场景类型（代码/对话/创意/提取）
     ↓
2. 选择预设参数作为起点
     ↓
3. 准备 3-5 个测试 Prompt（覆盖典型和边界情况）
     ↓
4. 每次只调一个参数，对比输出
     ↓
5. 记录最佳参数组合，写入配置
```

#### 常见误区

| 误区 | 正确做法 |
|------|----------|
| temperature 和 top_p 同时大幅调整 | 优先调 temperature |
| system prompt 越长越好 | 精简、结构化 |
| max_tokens 设太大浪费钱 | 根据实际需求设置 |
| 忽略多轮对话的 Token 累积 | 定期清理历史或摘要压缩 |

### 20:00 - 21:00 | 自习答疑

- 完成参数对比实验，保存结果到 JSON
- 运行 `smart_chat_cli.py`，体验不同 preset
- 预习 Day 17 Prompt 工程基础

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | Chat Completions API 完整请求结构 | |
| 2 | messages 数组与多轮对话管理 | |
| 3 | temperature 含义与场景化设置 | |
| 4 | top_p 核采样原理 | |
| 5 | max_tokens 与上下文窗口关系 | |
| 6 | presence/frequency_penalty 去重 | |
| 7 | stop 停止序列 | |
| 8 | system/user/assistant 角色设计 | |
| 9 | 流式输出 stream 原理与实现 | |
| 10 | SSE 数据流解析 | |
| 11 | 参数对比实验方法 | |
| 12 | 场景化参数预设配置 | |

---

## 📝 课后作业

### 必做题

1. **参数实验报告**：对同一 Prompt 分别用 temperature=0、0.7、1.5 调用 API，截图或保存输出，写 200 字对比分析

2. **流式聊天升级**：在 `stream_chat.py` 基础上添加：
   - 显示 Token 用量（从最后一个 chunk 的 usage 字段获取，或调用后单独计算）
   - 支持 `/clear` 命令清除历史
   - 支持 `/temp 0.5` 命令动态修改 temperature

3. **Git 提交**：`git commit -m "Day 16: API 核心参数与流式输出"`

### 选做题

4. 实现一个「参数推荐器」：输入场景描述（如「我要写 Python 代码」），自动推荐参数配置
5. 对比流式和非流式调用的首字延迟（time to first token）
6. 阅读 OpenAI/DeepSeek API 文档，整理两家 API 的参数差异表

---

## 💡 常见问题 FAQ

**Q1: temperature=0 时每次输出完全一样吗？**

A: 大多数模型在 temperature=0 时近似确定性，但部分模型仍有微小随机性。如需完全可复现，可设置 `seed` 参数（如果 API 支持）。

**Q2: 流式输出时如何获取 Token 用量？**

A: 部分 API 在最后一个 chunk 中包含 `usage` 字段。如果没有，可在流式结束后用 tiktoken 计算输入输出 Token 数。

**Q3: system prompt 可以中途修改吗？**

A: 技术上可以（在 messages 数组中替换），但不推荐。中途修改 system prompt 可能导致对话风格不一致。建议开启新会话。

**Q4: max_tokens 设太小会怎样？**

A: 输出会在达到限制时突然截断，可能话说一半。对于需要完整 JSON 的场景，截断会导致解析失败。

**Q5: 多轮对话历史太长怎么办？**

A: 策略一：滑动窗口，只保留最近 N 轮。策略二：对早期对话做摘要压缩。策略三：使用支持更长上下文的模型。Day 25+ RAG 阶段也会涉及上下文管理。

---

## 🔮 明日预习

**Day 17: Prompt 工程基础**

明天你将学习：

- Prompt 四要素：角色、任务、上下文、格式
- Zero-shot、One-shot、Few-shot 提示策略
- 角色扮演与输出格式约束
- **10 个典型场景的 Prompt 模板**

**预习建议**：回顾今天的 system prompt 设计，思考如何写出让 AI 输出更精准、更稳定的 Prompt。

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 16*
