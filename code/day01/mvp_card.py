#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mvp_card.py —— Day 1 十分钟最小可用版
适合第一次接触 Python 的学员先跑通再读企业级拆分代码。

用法: python mvp_card.py
"""

# 欢迎语
print("=== 个人信息卡片 MVP ===\n")

# 采集：注意 input 返回的都是字符串
name = input("姓名：")
city = input("城市：")
job = input("职业：")
motto = input("座右铭（可空）：") or "努力学习，天天进步"

# 年龄需要单独校验
while True:
    raw_age = input("年龄：").strip()
    if raw_age.isdigit() and 1 <= int(raw_age) <= 120:
        age = int(raw_age)
        break
    print("请输入 1-120 之间的整数")

# 输出：f-string 格式化
print("\n-------- 你的名片 --------")
print(f"姓名：{name}")
print(f"年龄：{age} 岁")
print(f"城市：{city}")
print(f"职业：{job}")
print(f"座右铭：{motto}")
print("--------------------------\n")
