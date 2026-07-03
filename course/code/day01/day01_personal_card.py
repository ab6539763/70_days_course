# ================================
# 文件名: day01_personal_card.py
# 主题: Day 1 — 个人信息卡片
# 说明:
# 1. 使用变量存储个人信息
# 2. 练习 print / input / f-string
# 3. 为后续 Prompt 模板中的字符串格式化打基础
# ================================

def collect_user_info() -> dict:
    """交互式收集用户信息，返回字典（Day 5 将深入学习 dict）"""
    print("=" * 40)
    print("  欢迎使用「个人信息卡片」生成器")
    print("=" * 40)

    name = input("请输入你的姓名: ").strip()
    age_str = input("请输入你的年龄: ").strip()
    city = input("请输入你所在的城市: ").strip()
    goal = input("请输入你的学习目标: ").strip()

    # 类型转换：input 永远返回 str，年龄需要转为 int
    try:
        age = int(age_str)
    except ValueError:
        print("[警告] 年龄输入无效，已设为 0")
        age = 0

    return {
        "name": name,
        "age": age,
        "city": city,
        "goal": goal,
    }


def render_card(info: dict) -> str:
    """用 f-string 渲染个人信息卡片（Day 2 将深入 f-string）"""
    border = "─" * 36
    card = f"""
{border}
  📇 个人信息卡片
{border}
  姓名: {info['name']}
  年龄: {info['age']} 岁
  城市: {info['city']}
  学习目标: {info['goal']}
{border}
  生成时间: 由 Python 自动生成
{border}
"""
    return card


def main():
    info = collect_user_info()
    card_text = render_card(info)
    print(card_text)

    # 保存到文件（Day 11 将系统学习文件操作）
    output_file = "my_card.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(card_text)
    print(f"✅ 卡片已保存到 {output_file}")


if __name__ == "__main__":
    main()
