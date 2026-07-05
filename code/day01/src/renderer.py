"""
Day 1 名片渲染模块
将 profile 字典格式化为带边框的终端输出。
渲染与打印分离：render_card 返回字符串，便于测试与写文件。
"""

from .config import CARD_WIDTH


def render_card(profile: dict, width: int = CARD_WIDTH) -> str:
    """
    将 profile 渲染为完整名片字符串。

    参数:
        profile: 包含 name/age/city/job/motto 的字典
        width: 名片宽度（字符数），默认读取 config.CARD_WIDTH

    返回:
        多行字符串，不含末尾额外换行
    """

    def horizontal_line() -> str:
        return "╔" + "═" * (width - 2) + "╗"

    def bottom_line() -> str:
        return "╚" + "═" * (width - 2) + "╝"

    def middle_line() -> str:
        return "╠" + "═" * (width - 2) + "╣"

    def content_line(text: str) -> str:
        inner_width = width - 4
        if len(text) > inner_width:
            text = text[: inner_width - 1] + "…"
        padding = inner_width - len(text)
        return f"║ {text}{' ' * padding} ║"

    def wrap_motto(motto: str, prefix: str = "  ") -> list[str]:
        inner_width = width - 4 - len(prefix)
        lines: list[str] = []
        start = 0
        while start < len(motto):
            lines.append(prefix + motto[start : start + inner_width])
            start += inner_width
        return lines if lines else [prefix]

    lines: list[str] = []
    lines.append(horizontal_line())
    lines.append(content_line("      个 人 信 息 卡 片"))
    lines.append(middle_line())
    lines.append(content_line(f"姓名：{profile['name']}"))
    lines.append(content_line(f"年龄：{profile['age']} 岁"))
    lines.append(content_line(f"城市：{profile['city']}"))
    lines.append(content_line(f"职业：{profile['job']}"))
    lines.append(middle_line())
    lines.append(content_line("座右铭："))
    for motto_line in wrap_motto(profile["motto"]):
        lines.append(content_line(motto_line.rstrip()))
    lines.append(bottom_line())
    return "\n".join(lines)


def print_card(profile: dict) -> None:
    """渲染并打印到标准输出。"""
    print(render_card(profile))
