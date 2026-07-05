# 项目一《命令行多轮对话 AI 助手》设计文档(Day 13 晚 · 预习版参考答案)

## 一、模块划分:复用清单 vs 新写清单

| 模块 | 来源 | 说明 |
|------|------|------|
| chatlib_v3(模型层/异常/重试) | Day 13 成果 | **整体复用,零新代码** |
| ChatSession / ChatMessage | Day 09-10 完全体 | 多轮记忆的容器 |
| parse_command(指令解析) | Day 07 上机题 2 | (指令, 参数) 元组 |
| 会话存档管理(时间戳命名/列出/加载) | Day 11 作业 | /save /load 的后勤 |
| .env / check_env 启动自检 | Day 13 作业 | 入口第一步 |
| **main.py 主循环 + 指令分发** | **新写** | 预计 < 150 行 |

结论:两周积累的复利具象化——新写代码不到 150 行。

## 二、主循环流程(文字版流程图)

```
启动 → load_dotenv → check_env(缺 Key 给指引退出)
     → 询问:恢复上次会话?(load_latest)还是新会话?
     → 建 ChatSession(system_prompt 打底)
循环:
     读输入并 strip
     ├─ 空输入 → continue
     ├─ Ctrl+C / EOFError → 优雅道别(询问是否保存)→ break
     ├─ parse_command 判定指令:
     │    /exit  → 询问保存 → break
     │    /clear → session.messages 清到只剩 system → 提示
     │    /save [文件名] → 存档(无参则时间戳自动命名)
     │    /history → 打印全部对话
     │    未知 /xx → 提示可用指令
     └─ 正常对话:
          session.add_user(text)
          reply = model.chat(session.to_api_format())   ← @retry 铠甲已就位
            ├─ AuthError → 提示查 Key,break
            ├─ 其他 ChatLibError → 提示,把刚 add 的 user 消息 pop 回滚!
            └─ 成功 → session.add_assistant(reply) → 打印 + token 记账
          超长检查:len(session) 过大 → trim 提示
```

## 三、指令表

| 指令 | 行为 | 对应零件 |
|------|------|---------|
| /exit | 询问保存后退出 | break + save |
| /clear | 清空记忆(保留 system) | messages 切片 |
| /save [名] | 存档 JSON | Day 11 存档管理 |
| /history | 带角色标签打印全部 | session.show() |
| /help | 打印本表 | 字典驱动 |

## 四、风险清单(预计最容易出 bug 的三处 + 预案)

1. **API 失败后的状态一致性**:add_user 之后调用失败,user 消息已进历史但没有对应回答——下轮请求会发给模型一个"没头的问题"。预案:失败时 `session.messages.pop()` 回滚刚加的消息;
2. **/clear 误伤 system**:直接 clear() 会把人设也清掉。预案:保留第一条 system(`messages[:1]`),测试用例必须覆盖;
3. **存档文件名的用户输入**:/save 我的对话.json 里可能有非法字符/路径穿越。预案:只取文件名部分(Path(name).name),空参数走时间戳默认。
