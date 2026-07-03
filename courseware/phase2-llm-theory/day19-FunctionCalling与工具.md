# Day 19: Function Calling 与工具

> **培训阶段**: 第二阶段 大模型理论与 API | **第 3 周 | **学习时长**: 约 6-8 小时  
> **今日关键词**: Function Calling 完整流程、工具 Schema、多工具场景、天气+计算器助手

---

## 📍 课程导航

### 上节回顾
**Day 18** 我们学习了 Prompt 工程进阶：

- Chain-of-Thought、Self-Consistency、Tree of Thoughts
- 提示词注入攻击识别与防御策略
- JSON Mode 结构化输出
- Function Calling 初探与工具 Schema 定义

今天将 **完整实现** Function Calling，打造能查天气、做计算的多工具 AI 助手。

### 本节学习目标
完成本日学习后，你将能够：

1. 掌握 Function Calling 的完整请求-响应循环
2. 编写规范的 OpenAI 兼容工具 Schema
3. 处理多工具场景下的工具选择与并行调用
4. 实现健壮的错误处理与降级策略
5. 独立完成「天气 + 计算器」多工具助手项目

### 与后续课程的衔接
- **Day 8** 函数定义与调用 → 工具函数就是普通 Python 函数
- **Day 11** 异常处理 → 工具执行失败时的容错
- **Day 18** Function Calling 初探 → 今天是完整实现
- **Day 21** 周测项目 → 整合多轮对话 + 工具调用
- **Day 39+** Agent 开发 → Function Calling 是 Agent 的核心能力
- **Day 25+** RAG → 检索也可以封装为一个 Tool

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：Function Calling 完整流程

#### 1.1 完整交互时序

```
轮次 1：用户提问
  App → API: messages=[{user: "北京天气"}], tools=[weather, calculator]
  API → App: assistant message + tool_calls=[{get_weather, {city:"北京"}}]

轮次 2：执行工具
  App: result = get_weather("北京") → "晴 25°C"
  App → API: messages=[..., assistant, {tool: "晴 25°C"}]

轮次 3：生成回答
  API → App: assistant message: "北京今天晴天，气温 25°C"
```

#### 1.2 消息类型扩展

| role | 用途 | 何时出现 |
|------|------|----------|
| system | 系统指令 | 对话开始 |
| user | 用户输入 | 每轮用户发言 |
| assistant | 模型回复 | 每轮模型回复 |
| tool | 工具执行结果 | 工具调用后 |
| assistant (含 tool_calls) | 模型决定调用工具 | 需要工具时 |

```python
# 完整 messages 示例
messages = [
    {"role": "system", "content": "你是智能助手，可以查天气和做计算。"},
    {"role": "user", "content": "北京今天天气怎么样？"},
    {
        "role": "assistant",
        "content": None,
        "tool_calls": [{
            "id": "call_abc123",
            "type": "function",
            "function": {
                "name": "get_weather",
                "arguments": '{"city": "北京"}'
            }
        }]
    },
    {
        "role": "tool",
        "tool_call_id": "call_abc123",
        "content": "晴，25°C，湿度 40%，东南风 3 级"
    },
    {
        "role": "assistant",
        "content": "北京今天天气晴朗，气温 25°C，湿度 40%，东南风 3 级，适合外出活动。"
    },
]
```

#### 1.3 核心循环模式

```python
# day19/tool_agent.py
"""Function Calling 核心循环"""

import os
import json
import requests
from typing import Callable

API_KEY = os.getenv("DEEPSEEK_API_KEY")
URL = "https://api.deepseek.com/v1/chat/completions"


class ToolAgent:
    def __init__(self, tools: list, functions: dict[str, Callable], system_prompt: str = ""):
        self.tools = tools
        self.functions = functions
        self.messages = []
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})

    def chat(self, user_input: str, max_iterations: int = 5) -> str:
        """处理用户输入，自动处理工具调用循环"""
        self.messages.append({"role": "user", "content": user_input})

        for _ in range(max_iterations):
            response = self._call_api()
            assistant_msg = response["choices"][0]["message"]
            self.messages.append(assistant_msg)

            # 没有工具调用 → 返回最终回答
            if not assistant_msg.get("tool_calls"):
                return assistant_msg["content"] or ""

            # 执行所有工具调用
            for tool_call in assistant_msg["tool_calls"]:
                result = self._execute_tool(tool_call)
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": result,
                })

        return "抱歉，处理超时，请简化您的问题。"

    def _call_api(self) -> dict:
        resp = requests.post(URL, json={
            "model": "deepseek-chat",
            "messages": self.messages,
            "tools": self.tools,
        }, headers={"Authorization": f"Bearer {API_KEY}"}, timeout=60)
        resp.raise_for_status()
        return resp.json()

    def _execute_tool(self, tool_call: dict) -> str:
        func_name = tool_call["function"]["name"]
        try:
            func_args = json.loads(tool_call["function"]["arguments"])
        except json.JSONDecodeError as e:
            return f"参数解析错误: {e}"

        if func_name not in self.functions:
            return f"未知工具: {func_name}"

        try:
            result = self.functions[func_name](**func_args)
            return str(result)
        except TypeError as e:
            return f"参数错误: {e}"
        except Exception as e:
            return f"工具执行失败: {e}"
```

---

### 9:45 - 10:30 | 模块二：工具 Schema 设计规范

#### 2.1 Schema 结构

```python
{
    "type": "function",
    "function": {
        "name": "函数名（snake_case）",
        "description": "清晰描述函数功能，帮助模型判断何时调用",
        "parameters": {
            "type": "object",
            "properties": {
                "参数名": {
                    "type": "string/number/boolean/array",
                    "description": "参数说明，越详细越好",
                    "enum": ["可选值1", "可选值2"],  # 可选
                }
            },
            "required": ["必填参数列表"]
        }
    }
}
```

#### 2.2 好 Schema vs 差 Schema

```python
# ❌ 差的 Schema
bad_tool = {
    "type": "function",
    "function": {
        "name": "search",
        "description": "搜索",
        "parameters": {
            "type": "object",
            "properties": {
                "q": {"type": "string"},
            },
        },
    },
}

# ✅ 好的 Schema
good_tool = {
    "type": "function",
    "function": {
        "name": "search_web",
        "description": "在互联网上搜索信息。当用户询问最新新闻、实时数据或你不确定的事实时使用。",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "搜索关键词，应简洁准确",
                },
                "max_results": {
                    "type": "integer",
                    "description": "返回结果数量，默认 5",
                },
            },
            "required": ["query"],
        },
    },
}
```

#### 2.3 Schema 设计原则

| 原则 | 说明 | 示例 |
|------|------|------|
| 描述要具体 | 说明何时该调用、何时不该调用 | 「当用户询问天气时使用」 |
| 参数名语义化 | 用完整单词，不用缩写 | `city` 而非 `c` |
| 描述每个参数 | 帮助模型生成正确参数 | `description` 字段必填 |
| 用 enum 限制选项 | 避免无效参数值 | `enum: ["celsius", "fahrenheit"]` |
| 合理设置 required | 必填参数最小化 | 只标记真正必需的 |

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：多工具场景

#### 3.1 工具选择策略

模型根据以下信息决定调用哪个工具：

1. **工具 description**：是否匹配用户意图
2. **用户问题内容**：需要哪种能力
3. **system prompt**：是否指定了工具使用规则

```python
MULTI_TOOL_SYSTEM = """
你是智能助手，可以使用以下工具：
- get_weather：查询城市天气
- calculate：数学计算

规则：
1. 需要实时数据（天气）时，必须调用工具，不要编造
2. 数学计算必须调用 calculate，不要心算
3. 普通聊天不需要调用工具
4. 如果一个问题需要多个工具，依次调用
"""
```

#### 3.2 并行 vs 串行工具调用

```python
# 用户：北京和上海今天天气分别怎么样？
# 模型可能一次返回两个 tool_calls（并行）
tool_calls = [
    {"function": {"name": "get_weather", "arguments": '{"city": "北京"}'}},
    {"function": {"name": "get_weather", "arguments": '{"city": "上海"}'}},
]

# 用户：北京天气怎么样，气温乘以 2 是多少？
# 模型会串行调用：先 get_weather → 再 calculate
```

#### 3.3 工具路由装饰器

```python
# day19/tool_registry.py
"""工具注册与管理"""

from functools import wraps
from typing import Callable


class ToolRegistry:
    def __init__(self):
        self._tools = {}
        self._schemas = []

    def register(self, name: str = None, description: str = "", **param_info):
        """装饰器：注册工具函数"""
        def decorator(func: Callable):
            tool_name = name or func.__name__
            self._tools[tool_name] = func

            # 自动生成 Schema
            schema = {
                "type": "function",
                "function": {
                    "name": tool_name,
                    "description": description or func.__doc__ or "",
                    "parameters": {
                        "type": "object",
                        "properties": param_info,
                        "required": [k for k, v in param_info.items()
                                     if v.get("required", True)],
                    },
                },
            }
            self._schemas.append(schema)
            return func
        return decorator

    @property
    def tools(self) -> list:
        return self._schemas

    @property
    def functions(self) -> dict:
        return self._tools


# 使用
registry = ToolRegistry()

@registry.register(
    description="获取指定城市的当前天气",
    city={"type": "string", "description": "城市名称"},
)
def get_weather(city: str) -> str:
    data = {"北京": "晴 25°C", "上海": "多云 22°C"}
    return data.get(city, f"暂无{city}数据")

@registry.register(
    description="计算数学表达式",
    expression={"type": "string", "description": "数学表达式"},
)
def calculate(expression: str) -> str:
    return str(eval(expression))
```

---

## 🌆 下午课程（14:00 - 17:00）

### 14:00 - 17:00 | 模块四：天气 + 计算器助手完整项目

#### 4.1 项目结构

```
day19/
├── assistant/
│   ├── __init__.py
│   ├── tools.py          # 工具函数实现
│   ├── schemas.py        # 工具 Schema 定义
│   ├── agent.py          # ToolAgent 核心
│   └── cli.py            # 命令行交互
├── tests/
│   └── test_tools.py     # 工具单元测试
└── main.py               # 入口
```

#### 4.2 工具实现

```python
# day19/assistant/tools.py
"""工具函数实现"""

import math
import re
from datetime import datetime


# 模拟天气数据（实际项目可对接真实 API）
WEATHER_DB = {
    "北京": {"condition": "晴", "temp": 25, "humidity": 40, "wind": "东南风 3 级"},
    "上海": {"condition": "多云", "temp": 22, "humidity": 65, "wind": "东风 2 级"},
    "广州": {"condition": "雨", "temp": 28, "humidity": 85, "wind": "南风 4 级"},
    "深圳": {"condition": "晴", "temp": 30, "humidity": 70, "wind": "西南风 2 级"},
}


def get_weather(city: str, unit: str = "celsius") -> str:
    """获取城市天气"""
    # 模糊匹配
    for key in WEATHER_DB:
        if city in key or key in city:
            data = WEATHER_DB[key]
            temp = data["temp"]
            if unit == "fahrenheit":
                temp = round(temp * 9 / 5 + 32, 1)
                unit_str = "°F"
            else:
                unit_str = "°C"
            return (
                f"{key}：{data['condition']}，"
                f"气温 {temp}{unit_str}，"
                f"湿度 {data['humidity']}%，"
                f"{data['wind']}"
            )
    return f"抱歉，暂无「{city}」的天气数据。支持的城市：{', '.join(WEATHER_DB.keys())}"


def calculate(expression: str) -> str:
    """安全计算数学表达式"""
    # 白名单：只允许数字、运算符和常用函数
    allowed_pattern = r'^[\d\s+\-*/().%,\s]+$'
    if not re.match(allowed_pattern, expression.replace(" ", "")):
        # 检查是否包含安全函数
        safe_expr = expression
        for func in ["sqrt", "sin", "cos", "tan", "log", "abs", "pow", "pi", "e"]:
            safe_expr = safe_expr.replace(func, "")
        if not re.match(r'^[\d\s+\-*/().%,\s]+$', safe_expr.replace(" ", "")):
            return "错误：表达式包含不允许的字符"

    # 安全命名空间
    safe_dict = {
        "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos,
        "tan": math.tan, "log": math.log, "abs": abs,
        "pow": pow, "pi": math.pi, "e": math.e,
    }

    try:
        result = eval(expression, {"__builtins__": {}}, safe_dict)
        return f"{expression} = {result}"
    except ZeroDivisionError:
        return "错误：除数不能为零"
    except Exception as e:
        return f"计算错误: {e}"


def get_current_time(timezone: str = "Asia/Shanghai") -> str:
    """获取当前时间"""
    now = datetime.now()
    return now.strftime(f"当前时间：%Y-%m-%d %H:%M:%S（{timezone}）")
```

#### 4.3 Schema 定义

```python
# day19/assistant/schemas.py
"""工具 Schema 定义"""

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": (
                "获取指定城市的当前天气信息，包括天气状况、温度、湿度和风力。"
                "当用户询问某个城市的天气、气温、是否下雨等问题时使用。"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "中国城市名称，如「北京」「上海」「广州」",
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "温度单位，默认摄氏度",
                    },
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": (
                "计算数学表达式的值。支持加减乘除、括号、百分号和常用数学函数。"
                "当用户提出数学计算问题，或需要对数字进行运算时使用。"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，如 '2 + 3 * 4'、'sqrt(16)'、'100 * 0.8'",
                    },
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前日期和时间。当用户询问现在几点、今天日期等问题时使用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "时区，默认 Asia/Shanghai",
                    },
                },
            },
        },
    },
]

FUNCTION_MAP = {
    "get_weather": get_weather,
    "calculate": calculate,
    "get_current_time": get_current_time,
}
```

#### 4.4 Agent 核心

```python
# day19/assistant/agent.py
"""多工具 Agent 核心"""

import os
import json
import requests
from .schemas import TOOL_SCHEMAS, FUNCTION_MAP

API_KEY = os.getenv("DEEPSEEK_API_KEY")
URL = "https://api.deepseek.com/v1/chat/completions"

SYSTEM_PROMPT = """你是「小智」智能助手，可以使用工具来回答问题。

## 能力
- 查询城市天气（get_weather）
- 数学计算（calculate）
- 查询当前时间（get_current_time）

## 规则
1. 需要实时数据时必须调用工具，不要编造
2. 数学计算必须调用 calculate，不要心算
3. 友好、简洁地回答用户
4. 工具失败时，诚实告知用户
"""


class Assistant:
    def __init__(self):
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.tools = TOOL_SCHEMAS
        self.functions = FUNCTION_MAP

    def chat(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})
        return self._run_loop()

    def _run_loop(self, max_iter: int = 5) -> str:
        for i in range(max_iter):
            data = self._api_call()
            msg = data["choices"][0]["message"]
            self.messages.append(msg)

            if not msg.get("tool_calls"):
                return msg.get("content", "")

            for tc in msg["tool_calls"]:
                result = self._exec_tool(tc)
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tc["id"],
                    "content": result,
                })
                print(f"  [工具] {tc['function']['name']}({tc['function']['arguments']}) → {result}")

        return "处理超时，请重试。"

    def _api_call(self) -> dict:
        resp = requests.post(URL, json={
            "model": "deepseek-chat",
            "messages": self.messages,
            "tools": self.tools,
            "temperature": 0.3,
        }, headers={"Authorization": f"Bearer {API_KEY}"}, timeout=60)
        resp.raise_for_status()
        return resp.json()

    def _exec_tool(self, tool_call: dict) -> str:
        name = tool_call["function"]["name"]
        try:
            args = json.loads(tool_call["function"]["arguments"])
            func = self.functions.get(name)
            if not func:
                return f"未知工具: {name}"
            return func(**args)
        except Exception as e:
            return f"执行失败: {e}"

    def clear(self):
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
```

#### 4.5 命令行交互

```python
# day19/main.py
"""天气+计算器助手 - 入口"""

from assistant.agent import Assistant


def main():
    bot = Assistant()
    print("=" * 50)
    print("  小智助手 - 支持天气查询、数学计算、时间查询")
    print("  输入 quit 退出 | clear 清除历史")
    print("=" * 50)

    while True:
        user_input = input("\n你: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("再见！")
            break
        if user_input.lower() == "clear":
            bot.clear()
            print("对话历史已清除。")
            continue

        print("小智: ", end="")
        reply = bot.chat(user_input)
        print(reply)


if __name__ == "__main__":
    main()
```

#### 4.6 测试用例

```python
# day19/tests/test_tools.py
"""工具函数单元测试"""

import sys
sys.path.insert(0, "..")
from assistant.tools import get_weather, calculate


def test_weather():
    assert "25" in get_weather("北京")
    assert "暂无" in get_weather("火星")

def test_calculate():
    assert "20" in calculate("10 + 10")
    assert "错误" in calculate("1 / 0")
    assert "错误" in calculate("import os")

if __name__ == "__main__":
    test_weather()
    test_calculate()
    print("所有测试通过！")
```

**测试对话**

```
你: 北京今天天气怎么样？
  [工具] get_weather({"city": "北京"}) → 北京：晴，气温 25°C...
小智: 北京今天天气晴朗，气温 25°C，湿度 40%，东南风 3 级，适合外出。

你: 1000 打 8 折再减 50 是多少？
  [工具] calculate({"expression": "1000 * 0.8 - 50"}) → 1000 * 0.8 - 50 = 750.0
小智: 1000 打 8 折是 800 元，再减 50 元，最终是 750 元。

你: 北京比上海热多少度？
  [工具] get_weather({"city": "北京"}) → ...
  [工具] get_weather({"city": "上海"}) → ...
  [工具] calculate({"expression": "25 - 22"}) → 25 - 22 = 3.0
小智: 北京 25°C，上海 22°C，北京比上海热 3 度。
```

---

## 🌙 晚自习（19:00 - 21:00）

### 19:00 - 20:00 | 项目完善

#### 可选增强

1. **流式输出**：结合 Day 16 的 stream，工具调用后的最终回答用流式显示
2. **对话历史持久化**：用 Day 14 的文件操作保存对话到 JSON
3. **真实天气 API**：对接和风天气或 OpenWeatherMap API
4. **工具调用日志**：记录每次工具调用的参数和结果

### 20:00 - 21:00 | 自习答疑

- 完成天气+计算器助手项目
- 测试至少 10 个不同问题
- 预习 Day 20 多模态与 Embedding

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | Function Calling 完整交互时序 | |
| 2 | tool 角色消息的使用 | |
| 3 | ToolAgent 核心循环模式 | |
| 4 | 工具 Schema 设计规范 | |
| 5 | 多工具选择与并行调用 | |
| 6 | 工具注册装饰器模式 | |
| 7 | 安全的 calculate 实现 | |
| 8 | 错误处理与降级策略 | |
| 9 | 天气+计算器助手完整项目 | |
| 10 | 工具函数单元测试 | |

---

## 📝 课后作业

### 必做题

1. **完成助手项目**：实现并测试天气+计算器+时间查询助手
2. **添加新工具**：实现 `translate` 工具（模拟翻译即可），注册到 Agent
3. **Git 提交**：`git commit -m "Day 19: Function Calling 多工具助手"`

### 选做题

4. 对接真实天气 API（和风天气免费版）
5. 实现工具调用的流式输出
6. 添加工具调用次数限制（防止无限循环）

---

## 💡 常见问题 FAQ

**Q1: 模型不调用工具，直接编造答案怎么办？**

A: 检查 Schema 的 description 是否够清晰；在 system prompt 中强调「必须调用工具」；降低 temperature。

**Q2: 模型调用了错误的工具怎么办？**

A: 优化各工具的 description，明确区分使用场景。可以在 system prompt 中给出使用示例。

**Q3: 工具调用陷入无限循环怎么办？**

A: 设置 `max_iterations` 上限（通常 5 次足够）。检查工具返回值是否清晰，避免模型反复调用。

**Q4: 多个 tool_calls 必须按顺序执行吗？**

A: 同一轮返回的多个 tool_calls 可以并行执行（互不依赖时）。有依赖关系时模型会分轮调用。

**Q5: Function Calling 和 Agent 是什么关系？**

A: Function Calling 是 Agent 的核心能力之一。Agent = LLM + 工具调用 + 规划 + 记忆。Day 39+ 会系统学习 Agent。

---

## 🔮 明日预习

**Day 20: 多模态与嵌入模型**

明天你将学习：

- 多模态 API（图片理解、图片生成）
- Embedding 向量表示原理
- 余弦相似度计算
- **相似问题匹配工具**（RAG 的雏形）

**预习建议**：思考「如何让 AI 判断两个问题是否相似？」

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 19*
