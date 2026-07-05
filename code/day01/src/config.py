"""
Day 1 项目配置模块
存放与业务逻辑无关的常量，便于统一修改 UI 与路径。
"""

from pathlib import Path

# 项目根目录：code/day01/
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# 输出目录，存放生成的名片文本
OUTPUT_DIR = PROJECT_ROOT / "output"

# 默认输出文件名
DEFAULT_CARD_FILENAME = "card.txt"

# 名片边框宽度（字符数），修改此处即可改变整体版式
CARD_WIDTH = 40

# 座右铭最大允许长度，防止终端输出过长
MAX_MOTTO_LENGTH = 200

# 年龄合法范围（含边界）
MIN_AGE = 1
MAX_AGE = 120
