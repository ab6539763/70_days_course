# =============================================
# Day 11 作业 · 编程题 3:通讯录导入导出 2.0(csv 模块版)
# 对比 Day 07 的手工版:字段里带逗号时,csv 模块自动加引号保护
# =============================================
import csv

FIELDS = ["name", "phone", "email", "group"]


def export_csv(contacts: list, filename: str) -> None:
    """导出联系人到 CSV(表头 + 数据行)。"""
    with open(filename, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)     # DictWriter:按字段名写
        writer.writeheader()                              # 先写表头
        for c in contacts:
            # 只取规定字段,缺的用空串补(get 兜底:向后兼容)
            writer.writerow({k: c.get(k, "") for k in FIELDS})
    print(f"已导出 {len(contacts)} 位 → {filename}")


def import_csv(filename: str) -> list:
    """从 CSV 导入:校验必填字段,不合格跳过并报行号。"""
    contacts: list = []
    try:
        with open(filename, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            # enumerate 从 2 起:第 1 行是表头,数据从第 2 行开始(报行号要对得上)
            for line_no, row in enumerate(reader, start=2):
                if not row.get("name", "").strip() or not row.get("phone", "").strip():
                    print(f"  第 {line_no} 行缺必填字段,跳过")
                    continue
                contacts.append(dict(row))                # row 是特殊字典,转普通 dict
    except FileNotFoundError:
        print(f"文件 {filename} 不存在")
    return contacts


if __name__ == "__main__":
    data = [
        {"name": "张三, Jr.", "phone": "13812345678", "email": "z@x.com", "group": "研发"},
        {"name": "李四", "phone": "13900001111", "email": "l@x.com", "group": "产品"},
        {"name": "", "phone": "123", "email": "", "group": ""},        # 坏数据:缺姓名
    ]
    export_csv(data, "test_contacts.csv")
    back = import_csv("test_contacts.csv")

    assert len(back) == 2                          # 坏行被跳过
    assert back[0]["name"] == "张三, Jr."           # 带逗号的字段安然无恙:csv 模块的价值
    print("✓ csv 模块版导入导出测试通过")

    import os
    os.remove("test_contacts.csv")                 # 打扫测试现场
