"""
Day 1 交互采集模块
负责通过终端 input() 向用户提问，并循环直至输入合法。
"""

from .validators import validate_age, validate_motto, validate_non_empty


def prompt_name() -> str:
    """采集并校验姓名。"""
    while True:
        raw = input("请输入您的姓名：")
        ok, err = validate_non_empty(raw, "姓名")
        if ok:
            return raw.strip()
        print(f"  ⚠ {err}")


def prompt_age() -> int:
    """采集并校验年龄。"""
    while True:
        raw = input("请输入您的年龄（正整数）：")
        ok, age, err = validate_age(raw)
        if ok:
            return age  # type: ignore[return-value]
        print(f"  ⚠ {err}")


def prompt_city() -> str:
    """采集并校验城市。"""
    while True:
        raw = input("请输入您所在的城市：")
        ok, err = validate_non_empty(raw, "城市")
        if ok:
            return raw.strip()
        print(f"  ⚠ {err}")


def prompt_job() -> str:
    """采集职业或学习目标。"""
    while True:
        raw = input("请输入您的职业或学习目标：")
        ok, err = validate_non_empty(raw, "职业")
        if ok:
            return raw.strip()
        print(f"  ⚠ {err}")


def prompt_motto() -> str:
    """采集座右铭，允许为空则给默认值。"""
    raw = input("请输入一句座右铭或学习目标（可回车跳过）：")
    if not raw.strip():
        return "70 天后，我要独立做出自己的大模型应用。"
    while True:
        ok, motto, err = validate_motto(raw)
        if ok:
            return motto
        print(f"  ⚠ {err}")
        raw = input("请重新输入座右铭：")


def prompt_profile() -> dict:
    """
    依次采集所有字段，返回 profile 字典。

    该字典结构与 Day 5 JSON、Day 14 对话配置一脉相承：
    键为英文字符串，值为 Python 基本类型。

    返回:
        {
            "name": str,
            "age": int,
            "city": str,
            "job": str,
            "motto": str,
        }
    """
    print("\n--- 请按提示填写个人信息 ---\n")
    profile = {
        "name": prompt_name(),
        "age": prompt_age(),
        "city": prompt_city(),
        "job": prompt_job(),
        "motto": prompt_motto(),
    }
    print("\n--- 信息采集完成 ---\n")
    return profile
