"""
Day 1 输入校验模块
纯函数设计：不依赖 input()，方便单元测试（tests/test_validators.py）。
"""

from .config import MAX_AGE, MAX_MOTTO_LENGTH, MIN_AGE


def validate_non_empty(value: str, field_name: str) -> tuple[bool, str]:
    """
    校验字符串非空（去除首尾空白后）。

    参数:
        value: 用户原始输入
        field_name: 字段中文名，用于错误提示

    返回:
        (是否通过, 错误消息) —— 通过时错误消息为空字符串
    """
    cleaned = value.strip()
    if not cleaned:
        return False, f"{field_name}不能为空，请重新输入。"
    return True, ""


def validate_age(raw: str) -> tuple[bool, int | None, str]:
    """
    校验年龄字符串是否为合法正整数。

    参数:
        raw: 用户输入的年龄字符串

    返回:
        (是否通过, 转换后的整数或 None, 错误消息)
    """
    stripped = raw.strip()
    if not stripped.isdigit():
        return False, None, "年龄必须是正整数，不能包含字母或符号。"

    age = int(stripped)
    if age < MIN_AGE or age > MAX_AGE:
        return False, None, f"年龄请在 {MIN_AGE}-{MAX_AGE} 之间。"

    return True, age, ""


def validate_motto(raw: str) -> tuple[bool, str, str]:
    """
    校验座右铭长度。

    参数:
        raw: 用户输入的座右铭

    返回:
        (是否通过, 处理后的文本, 错误消息)
    """
    motto = raw.strip()
    if len(motto) > MAX_MOTTO_LENGTH:
        return (
            False,
            "",
            f"座右铭不能超过 {MAX_MOTTO_LENGTH} 个字符，当前 {len(motto)} 个。",
        )
    return True, motto, ""
