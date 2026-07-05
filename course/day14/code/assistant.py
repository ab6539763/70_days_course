# =============================================
# 项目一:命令行多轮对话 AI 助手(讲师参考实现)
# 需求编号:REQ-D14-001
# 运行:python assistant.py          (真实模式,需 .env 配置 DEEPSEEK_API_KEY)
#       python assistant.py --fake   (开发模式,零成本)
# 架构:main 入口 / 指令处理函数 / chatlib_v3(三层,T3)
# 每段代码的知识出生日标注在注释里——两周积累的全景回望
# =============================================
import json
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv                                   # Day 13

from chatlib_v3 import (                                          # Day 10 包结构
    ChatSession, DeepSeekModel, FakeModel,
    ChatLibError, AuthError,
)

SESSIONS_DIR = Path("sessions")                                   # Day 11 存档目录
DEFAULT_SYSTEM = "你是一位耐心的AI学习助手,回答简洁清晰"
PRICE_PER_M = 1.5                                                 # 粗略均价(元/百万token)


# ──────────────── 指令解析(Day 07 上机题 2 原件) ────────────────

def parse_command(text: str) -> tuple:
    """解析用户输入:返回 (指令, 参数) 或 ("", 正文)。"""
    text = text.strip()
    if not text.startswith("/"):
        return ("", text)
    parts = text.split(maxsplit=1)                # 最多切一刀:参数里允许空格
    command = parts[0].lower()                     # 大写指令也认(交叉测试击破点!)
    arg = parts[1].strip() if len(parts) > 1 else ""
    return (command, arg)


# ──────────────── 存档管理(Day 11 作业的手艺) ────────────────

def save_session(session: ChatSession, name: str = "") -> str:
    """存档:指定名或时间戳自动命名。只取文件名部分,防路径穿越。"""
    SESSIONS_DIR.mkdir(exist_ok=True)
    if name:
        filename = Path(name).name                 # 防 ../../etc 类输入(设计文档风险3)
        if not filename.endswith(".json"):
            filename += ".json"
    else:
        filename = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    path = SESSIONS_DIR / filename
    session.save(str(path))                        # Day 08 作业的 save
    return str(path)


def load_latest_session_path() -> Path | None:
    """最新存档路径;没有则 None(时间戳命名 → 字典序即时间序)。"""
    if not SESSIONS_DIR.exists():
        return None
    archives = sorted(SESSIONS_DIR.glob("*.json"))
    return archives[-1] if archives else None


# ──────────────── 指令处理函数(每个一个小函数:T3 单一职责) ────────────────

def do_clear(session: ChatSession) -> None:
    """F3:清空记忆但保留人设——切片保 system,不是 clear()!"""
    if session.messages and session.messages[0].role == "system":
        session.messages = session.messages[:1]
    else:
        session.messages = []
    print("记忆已清空(人设保留)")


def do_save(session: ChatSession, arg: str) -> None:
    """F3/F4:存档。"""
    path = save_session(session, arg)
    print(f"已保存 → {path}")


def do_history(session: ChatSession, model) -> None:
    """F3/F6:打印全部对话 + 总消耗。"""
    session.show()                                 # Day 10 messages.py 的方法
    usage = model.count_usage()
    cost = usage["tokens"] / 1_000_000 * PRICE_PER_M
    print(f"—— 会话总消耗:{usage['tokens']} tokens ≈ {cost:.4f} 元 ——")


def do_help() -> None:
    """F3:指令说明(字典驱动,和分发表同源维护)。"""
    print("可用指令:")
    for cmd, desc in COMMAND_DOCS.items():
        print(f"  {cmd:<18}{desc}")


COMMAND_DOCS = {
    "/exit": "退出(询问是否保存)",
    "/clear": "清空记忆(保留人设)",
    "/save [文件名]": "存档,无参数则时间戳命名",
    "/history": "查看全部对话与总消耗",
    "/help": "本说明",
}


def handle_command(command: str, arg: str, session: ChatSession, model) -> None:
    """指令分发:字典驱动(Day 05/06 注册表模式)。"""
    handlers = {
        "/clear": lambda: do_clear(session),
        "/save": lambda: do_save(session, arg),
        "/history": lambda: do_history(session, model),
        "/help": lambda: do_help(),
    }
    handler = handlers.get(command)
    if handler is None:                            # F3:未知指令兜底,不误发给模型
        print(f"未知指令 {command},输入 /help 查看可用指令")
        return
    handler()


# ──────────────── 会话准备与退出(F4/F5) ────────────────

def prepare_session() -> ChatSession:
    """启动:有存档问恢复,没有则新建(可自定义人设:F2)。"""
    latest = load_latest_session_path()
    if latest:
        choice = input(f"发现最近存档 {latest.name},恢复?(y/n):").strip().lower()
        if choice == "y":
            session = ChatSession.load(str(latest))    # Day 10 分路容错 load
            print(f"已恢复 {len(session)} 条对话")
            return session
    prompt = input("自定义人设(回车用默认):").strip()
    return ChatSession("我的助手", system_prompt=prompt or DEFAULT_SYSTEM)


def ask_save_and_exit(session: ChatSession) -> None:
    """退出前询问保存(F3 /exit 与 Ctrl+C 共用:DRY)。"""
    if len(session) > 1:                           # 只有 system 时不必问
        choice = input("\n保存本次会话?(y/n):").strip().lower()
        if choice == "y":
            print(f"已保存 → {save_session(session)}")
    print("再见!")


def print_cost_line(model, last_total: int) -> int:
    """F6:成本行。返回新的累计值供下轮计算本轮增量。"""
    total = model.count_usage()["tokens"]
    used = total - last_total
    cost = total / 1_000_000 * PRICE_PER_M
    print(f"(本轮 {used} tokens | 累计 {total} ≈ {cost:.4f} 元)")
    return total


# ──────────────── 入口 ────────────────

def main() -> None:
    """入口:自检 → 会话准备 → 主循环。"""
    load_dotenv()                                                  # Day 13
    use_fake = "--fake" in sys.argv                                # T2

    try:
        model = FakeModel() if use_fake else DeepSeekModel()
    except AuthError:                                              # T4 启动自检给指引
        print("未检测到 API Key:请复制 .env.example 为 .env 并填入 Key")
        return

    session = prepare_session()                                    # F4
    print(f"\nAI 助手已就绪(模型:{model.model_name}) /help 看指令")
    last_total = 0

    while True:                                                    # Day 03 骨架最终形态
        try:
            text = input("\n你:").strip()
        except (KeyboardInterrupt, EOFError):                      # F5-b 优雅道别
            ask_save_and_exit(session)
            break

        if not text:                                               # F5-a 空输入
            continue

        if text.startswith("/"):                                   # 指令通道
            command, arg = parse_command(text)
            if command == "/exit":
                ask_save_and_exit(session)
                break
            handle_command(command, arg, session, model)
            continue

        # ── 正常对话:三行拆墙 + 失败回滚(F1 + F5-e) ──
        session.add_user(text)                                     # ① 用户消息进历史
        try:
            reply = model.chat(session.to_api_format())            # ② 发送完整历史
        except AuthError as e:
            print(f"认证失败:{e}")
            session.messages.pop()                                 # ★ 回滚孤儿消息
            break
        except ChatLibError as e:
            print(f"服务异常:{e},本轮作废,请重试")
            session.messages.pop()                                 # ★ 回滚(风险 1)
            continue
        session.add_assistant(reply)                               # ③ AI 回答进历史

        print(f"\nAI:{reply}")
        last_total = print_cost_line(model, last_total)            # F6


if __name__ == "__main__":
    main()
