# =============================================
# Day 14 延伸题 2:记忆窗口自动化(Day 27 的预演)
# 进阶方案:先存档再遗忘——
#   工作记忆(messages)小而快,归档记忆(磁盘 JSON)全而慢。
#   这就是 Day 27 记忆管理和 Day 44 Agent 长期记忆的原始思想。
# =============================================
import sys
import os
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from chatlib_v3 import ChatSession, FakeModel

MAX_MESSAGES = 21          # system + 10 轮
TRIM_TO_ROUNDS = 8
ARCHIVE_DIR = Path("archive_demo")


def auto_manage_memory(session: ChatSession) -> None:
    """超限时:先归档完整历史,再截断工作记忆。"""
    if len(session) <= MAX_MESSAGES:
        return
    ARCHIVE_DIR.mkdir(exist_ok=True)
    archive_path = ARCHIVE_DIR / f"auto_archive_{datetime.now().strftime('%H%M%S_%f')}.json"
    session.save(str(archive_path))                # 完整记录先落盘
    session.trim(max_rounds=TRIM_TO_ROUNDS)       # 再遗忘
    print(f"(较早的对话已归档遗忘,完整记录:{archive_path})")


if __name__ == "__main__":
    import shutil

    session = ChatSession("长对话", system_prompt="你是助手")
    model = FakeModel()

    # 模拟 12 轮对话:超过 10 轮上限,触发自动归档+截断
    for i in range(12):
        session.add_user(f"第 {i+1} 个问题")
        session.add_assistant(model.chat(session.to_api_format()))
        auto_manage_memory(session)

    # 触发过截断后,工作记忆始终被压在上限之内
    assert len(session) <= MAX_MESSAGES
    assert session.messages[0].role == "system"        # 人设永不丢
    assert list(ARCHIVE_DIR.glob("*.json"))            # 归档存在
    print(f"✓ 工作记忆 {len(session)} 条,归档 {len(list(ARCHIVE_DIR.glob('*.json')))} 份")

    shutil.rmtree(ARCHIVE_DIR)                         # 打扫演示现场
