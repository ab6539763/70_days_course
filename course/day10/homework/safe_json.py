# =============================================
# Day 10 作业 · 编程题 1:safe_load_json 转正版
# 考点:多路 except、损坏文件的工程化处置(备份而不是无限踩坑)
# =============================================
import json
import os


def safe_load_json(filename: str, default=None):
    """安全加载 JSON:不存在给默认,损坏则备份坏文件后给默认。"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default                              # 首次运行的正常情况:安静兜底
    except json.JSONDecodeError as e:
        broken_name = filename + ".broken"
        os.rename(filename, broken_name)            # 坏文件挪走:下次启动不再撞上
        print(f"[警告] {filename} 已损坏(第 {e.lineno} 行),已备份为 {broken_name}")
        return default


if __name__ == "__main__":
    # 情况 1:文件不存在
    assert safe_load_json("no_such.json", default=[]) == []

    # 情况 2:正常文件
    with open("good.json", "w", encoding="utf-8") as f:
        json.dump({"ok": True}, f)
    assert safe_load_json("good.json") == {"ok": True}

    # 情况 3:损坏文件
    with open("bad.json", "w", encoding="utf-8") as f:
        f.write("{'单引号': 非法}")
    assert safe_load_json("bad.json", default={}) == {}
    assert os.path.exists("bad.json.broken")        # 坏文件被备份
    assert not os.path.exists("bad.json")           # 原位置已清空

    # 打扫测试现场
    os.remove("good.json")
    os.remove("bad.json.broken")
    print("✓ safe_load_json 三种情况全部通过")
