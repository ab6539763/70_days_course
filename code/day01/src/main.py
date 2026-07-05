"""
Day 1 程序入口
个人信息卡片 —— 零基础大模型应用开发课程第一个完整项目

运行: python -m src.main
"""

from pathlib import Path

from .config import DEFAULT_CARD_FILENAME, OUTPUT_DIR
from .input_handler import prompt_profile
from .renderer import print_card


def save_card_to_file(content: str, filename: str = DEFAULT_CARD_FILENAME) -> Path | None:
    """
    将名片内容写入 output 目录。

    参数:
        content: render_card 返回的字符串
        filename: 文件名

    返回:
        成功时返回文件路径，失败返回 None
    """
    try:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        filepath = OUTPUT_DIR / filename
        # utf-8 显式指定，避免 Windows 默认编码问题
        filepath.write_text(content, encoding="utf-8")
        return filepath
    except OSError as exc:
        print(f"  ⚠ 保存文件失败：{exc}")
        return None


def ask_yes_no(prompt: str) -> bool:
    """
    询问是/否，接受 y/yes/是 为肯定。

    参数:
        prompt: 提示语

    返回:
        True 表示用户确认
    """
    while True:
        raw = input(prompt).strip().lower()
        if raw in ("y", "yes", "是", "好", "ok"):
            return True
        if raw in ("n", "no", "否", "不"):
            return False
        print("  请输入 y/是 或 n/否")


def main() -> None:
    """主流程：欢迎 → 采集 → 展示 → 可选保存。"""
    print("=" * 44)
    print("  零基础大模型应用开发 · Day 1")
    print("  项目：个人信息卡片 Personal Info Card")
    print("=" * 44)

    profile = prompt_profile()
    print_card(profile)

    if ask_yes_no("\n是否将名片保存到 output/card.txt？(y/n)："):
        from .renderer import render_card

        path = save_card_to_file(render_card(profile))
        if path:
            print(f"  ✓ 已保存至：{path.resolve()}")

    print("\n感谢使用！明天 Day 2 我们将学习字符串清洗——Prompt 模板的基础。")
    print("今晚记得：Git commit + push 今日代码。\n")


if __name__ == "__main__":
    main()
