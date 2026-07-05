# =============================================
# Day 07 作业 · 编程题 3:第一周知识地图
# 一个程序演示七天的代表技能:
#   D5 JSON 解析 → D4 推导式过滤 → D2 清洗打码 →
#   D5 字典计数器 → D6 函数分层 → D3 循环菜单 → D1/D2 f-string 对齐
# 哪一步卡住,那一天就是薄弱点——精确定位,精确补强
# =============================================
import json

# ---- 模拟数据:用户评论 JSON 数组(D5:JSON 是字符串!) ----
RAW_JSON = """
[
  {"name": "张三", "content": "  这个产品真垃圾,太难用了  ", "stars": 1},
  {"name": "李四", "content": "整体不错,推荐购买", "stars": 5},
  {"name": "王五", "content": "客服是傻子吗?半天不回", "stars": 2},
  {"name": "赵六", "content": "  物流很快   包装完好  ", "stars": 4}
]
"""

BANNED_WORDS = ["垃圾", "傻子", "废物"]        # 常量:全大写(D1 规范)


# ──────────────── 工具层(D6:纯函数) ────────────────

def clean_content(text: str) -> str:
    """清洗评论:去两端空白、规范空格、敏感词等长打码。(D2 流水线)"""
    result = " ".join(text.strip().split())
    for word in BANNED_WORDS:
        result = result.replace(word, "*" * len(word))
    return result


def load_comments() -> list:
    """解析内置 JSON,顺手清洗每条 content。(D5 loads + D4 遍历加工)"""
    comments = json.loads(RAW_JSON)
    for c in comments:
        c["content"] = clean_content(c["content"])
    return comments


def bad_reviews(comments: list) -> list:
    """三星以下差评。(D4 推导式过滤)"""
    return [c for c in comments if c["stars"] < 3]


def star_stats(comments: list) -> dict:
    """各星级数量。(D5 字典计数器)"""
    counter: dict = {}
    for c in comments:
        counter[c["stars"]] = counter.get(c["stars"], 0) + 1
    return counter


# ──────────────── 功能层(D6:交互) ────────────────

def show_comments(comments: list, title: str) -> None:
    """对齐展示评论列表。(D1/D2 f-string 对齐)"""
    print(f"\n【{title}】共 {len(comments)} 条")
    for c in comments:
        stars = "★" * c["stars"] + "☆" * (5 - c["stars"])
        print(f"  {c['name']:<6}{stars:<7}{c['content']}")


def show_stats(comments: list) -> None:
    """星级分布统计。"""
    print("\n【星级分布】")
    for stars, n in sorted(star_stats(comments).items(), reverse=True):
        print(f"  {stars} 星:{'█' * n} {n} 条")


# ──────────────── 入口层(D3:循环菜单) ────────────────

def main() -> None:
    comments = load_comments()

    while True:
        print("\n" + "=" * 30)
        print("  1 全部评论  2 差评  3 统计  0 退出")
        choice = input("请选择:").strip()

        if choice == "0":
            print("再见!")
            break
        elif choice == "1":
            show_comments(comments, "全部评论")
        elif choice == "2":
            show_comments(bad_reviews(comments), "差评(<3星)")
        elif choice == "3":
            show_stats(comments)
        else:
            print(f"没有选项 [{choice}]")


if __name__ == "__main__":
    main()
