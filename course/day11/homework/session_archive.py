# =============================================
# Day 11 作业 · 编程题 1:会话存档管理器
# 考点:pathlib 建目录/glob、时间戳文件名、json 文件读写
# Day 14 的 /save 与"恢复上次会话"功能的后勤系统
# 亮点:时间戳命名 %Y%m%d_%H%M%S 保证"字典序=时间序",命名即索引
# =============================================
import json
from datetime import datetime
from pathlib import Path

SESSIONS_DIR = Path("sessions")


def save_session_auto(session_data: dict) -> str:
    """存档会话:自动建目录 + 时间戳命名,返回文件路径。"""
    SESSIONS_DIR.mkdir(exist_ok=True)                 # 不存在就建,存在不报错
    name = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    path = SESSIONS_DIR / name
    with open(path, "w", encoding="utf-8") as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)
    return str(path)


def list_sessions() -> list:
    """列出所有存档路径,按文件名排序(时间戳命名 → 字典序即时间序)。"""
    if not SESSIONS_DIR.exists():
        return []
    return sorted(SESSIONS_DIR.glob("session_*.json"))


def load_latest() -> dict | None:
    """加载最新存档;没有则 None。"""
    sessions = list_sessions()
    if not sessions:
        return None
    with open(sessions[-1], "r", encoding="utf-8") as f:    # 排序后最后一个=最新
        return json.load(f)


if __name__ == "__main__":
    import time

    p1 = save_session_auto({"name": "会话1", "messages": []})
    time.sleep(1.1)                    # 保证时间戳不同(秒级精度)
    p2 = save_session_auto({"name": "会话2", "messages": []})

    assert len(list_sessions()) >= 2
    latest = load_latest()
    assert latest["name"] == "会话2"   # 最新的是后存的
    print(f"✓ 存档管理器测试通过,最新存档:{latest['name']}")
