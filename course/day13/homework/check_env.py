# =============================================
# Day 13 作业 · 编程题 3⑤:环境自检脚本
# 以后每个项目的标准启动自检:缺谁报谁,全齐放行
# =============================================
import os
import sys

from dotenv import load_dotenv

load_dotenv()

REQUIRED_VARS = ["DEEPSEEK_API_KEY"]             # 列表驱动:项目变了只改这里
OPTIONAL_VARS = ["APP_ENV"]


def check_env() -> bool:
    """检查必需环境变量;缺失则逐个报告,返回是否通过。"""
    missing = [v for v in REQUIRED_VARS if not os.environ.get(v)]
    if missing:
        print("环境自检失败,缺少以下变量:")
        for v in missing:
            print(f"  - {v}(请在 .env 中配置,参考 .env.example)")
        return False

    for v in REQUIRED_VARS:
        value = os.environ[v]
        print(f"  ✓ {v} = {value[:6]}...(已脱敏)")     # Day 02 脱敏手艺:绝不打印全值
    for v in OPTIONAL_VARS:
        print(f"  · {v} = {os.environ.get(v, '(未设置,使用默认)')}")
    return True


if __name__ == "__main__":
    if not check_env():
        sys.exit(1)                              # 非零退出码:告诉调用方"自检失败"
    print("环境自检通过,可以启动")
