# =============================================
# Day 06 作业 · 编程题 2:消息工厂
# 考点:纯函数 + 原地修改函数的命名约定 + 展示与逻辑分离
# 这四个函数将在 Day 14 项目一里几乎原样上岗
# =============================================

ROLE_NAMES = {"system": "[系统]", "user": "[我]", "assistant": "[AI]"}   # 模块级常量


def make_message(role: str, content: str) -> dict:
    """构造一条标准消息字典。"""
    return {"role": role, "content": content}


def add_user_message(messages: list, content: str) -> None:
    """追加一条用户消息(原地修改 messages)。"""
    messages.append(make_message("user", content))      # 函数复用函数


def add_assistant_message(messages: list, content: str) -> None:
    """追加一条 AI 消息(原地修改 messages)。"""
    messages.append(make_message("assistant", content))


def format_history(messages: list) -> str:
    """把对话历史格式化为多行字符串。只 return 不 print。"""
    lines = [f"{ROLE_NAMES.get(m['role'], '[?]')} {m['content']}" for m in messages]
    return "\n".join(lines)                              # join:Day 02 复利


def main() -> None:
    messages = [make_message("system", "你是Python学习助教")]
    for q in ["什么是函数?", "return和print区别?", "什么是纯函数?"]:
        add_user_message(messages, q)
        add_assistant_message(messages, f"关于「{q}」的解答是……")
    print(format_history(messages))                      # 打印权在调用方
    print(f"\n共 {len(messages)} 条消息")


if __name__ == "__main__":
    main()
