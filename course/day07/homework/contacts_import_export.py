# =============================================
# Day 07 作业 · 编程题 2:通讯录导入导出
# 隐藏教学:处理外部数据的三板斧——逐行、校验、坏行不搞崩整体
# (Day 28 批量加载文档、Day 52 清洗训练数据,同一套板斧)
# =============================================


def export_contacts(contacts: list, filename: str = "contacts_export.txt") -> None:
    """导出为 CSV 风格文本:每行 姓名,手机号,邮箱,分组。"""
    lines = [f"{c['name']},{c['phone']},{c['email']},{c.get('group', '未分组')}"
             for c in contacts]                        # 推导式:每人一行
    text = "\n".join(lines)                            # join 拼接(Day 02 复利)
    with open(filename, "w", encoding="utf-8") as f:   # 文件模板的裸用版
        f.write(text)
    print(f"已导出 {len(lines)} 位联系人 → {filename}")


def import_contacts(contacts: list, filename: str = "contacts_export.txt") -> None:
    """从 CSV 风格文本导入:跳过坏行并报告;重名跳过。"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"文件 {filename} 不存在!")
        return

    added, skipped = 0, 0
    for line_no, line in enumerate(text.split("\n"), start=1):
        line = line.strip()
        if not line:                                   # 空行:安静跳过
            continue
        parts = line.split(",")
        if len(parts) != 4:                            # 字段数不对:坏行
            print(f"  第 {line_no} 行格式错误,跳过:{line[:20]}")
            skipped += 1
            continue
        name, phone, email, group = parts              # 拆包(正好 4 段才能拆)
        if any(c["name"] == name for c in contacts):   # 重名跳过
            skipped += 1
            continue
        contacts.append({"name": name, "phone": phone, "email": email, "group": group})
        added += 1
    print(f"导入完成:新增 {added},跳过 {skipped}")


def main() -> None:
    """演示:导出 → 清空 → 导入(含一条坏行测试)。"""
    contacts = [
        {"name": "张三", "phone": "13812345678", "email": "z@x.com", "group": "研发"},
        {"name": "李四", "phone": "13900001111", "email": "l@x.com", "group": "产品"},
    ]
    export_contacts(contacts)

    # 人为往导出文件里追加一条坏行,测试容错
    with open("contacts_export.txt", "a", encoding="utf-8") as f:
        f.write("\n这是一条坏数据没有逗号")

    fresh: list = []
    import_contacts(fresh)
    print(f"导入后共 {len(fresh)} 位")
    assert len(fresh) == 2                             # 坏行被跳过,好数据全进
    print("✓ 容错测试通过")


if __name__ == "__main__":
    main()
