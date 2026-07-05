# =============================================
# Day 07 作业 · 编程题 1:通讯录"即时保存"改造
# 核心改动:注册表带元数据(是否写操作),主循环统一落盘
# 只展示改动后的 main;工具层/功能层与课堂版 contacts_app.py 相同,
# 实际使用时可整体复制过来(Day 10 学模块后就能 import 复用了)
# =============================================
import json

DATA_FILE = "contacts.json"


def save_json(data, filename: str) -> None:
    """保存 JSON 文件(模板函数)。"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_json(filename: str, default=None):
    """加载 JSON 文件;不存在返回 default(模板函数)。"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default if default is not None else []


def mask_phone(phone: str) -> str:
    """手机号脱敏。"""
    return phone[:3] + "****" + phone[-4:]


def list_contacts(contacts: list) -> None:
    """带编号显示全部联系人。"""
    if not contacts:
        print("通讯录为空!")
        return
    for i, c in enumerate(contacts, start=1):
        print(f"  {i}. {c['name']:<8}{mask_phone(c['phone']):<15}[{c.get('group', '未分组')}]")


def add_contact(contacts: list) -> None:
    """添加联系人(精简校验版,完整版见课堂代码)。"""
    name = input("姓名:").strip()
    if not name or any(c["name"] == name for c in contacts):
        print("姓名为空或已存在!")
        return
    while True:
        phone = input("手机号(11位):").strip()
        if phone.isdigit() and len(phone) == 11:
            break
        print("手机号必须是 11 位数字!")
    group = input("分组(回车=未分组):").strip() or "未分组"
    contacts.append({"name": name, "phone": phone, "email": "", "group": group})
    print(f"已添加:{name}")


def delete_contact(contacts: list) -> None:
    """按编号删除(精简版)。"""
    list_contacts(contacts)
    if not contacts:
        return
    num = input("删除第几位?").strip()
    if not num.isdigit() or not (1 <= int(num) <= len(contacts)):
        print("编号无效!")
        return
    removed = contacts.pop(int(num) - 1)
    print(f"已删除:{removed['name']}")


def main() -> None:
    """入口:每次写操作后自动落盘。"""
    contacts = load_json(DATA_FILE, default=[])
    print(f"已加载 {len(contacts)} 位联系人")

    # 注册表升级:第三个元素标记"是否写操作"——注册表带元数据,
    # 主循环统一处理保存,比在每个函数里各写一遍 save 优雅(DRY)
    menu = {
        "1": ("查看全部", lambda: list_contacts(contacts), False),
        "2": ("添加", lambda: add_contact(contacts), True),
        "3": ("删除", lambda: delete_contact(contacts), True),
    }

    while True:
        print("\n" + "=" * 32)
        for key, (name, _, _) in menu.items():
            print(f"  {key}. {name}")
        print("  0. 退出")
        choice = input("请选择:").strip()

        if choice == "0":
            save_json(contacts, DATA_FILE)          # 退出仍保存一次,双保险
            print("再见!")
            break
        if choice not in menu:
            print(f"没有选项 [{choice}]")
            continue

        _, func, is_write = menu[choice]
        func()
        if is_write:                                # 写操作 → 立即落盘
            save_json(contacts, DATA_FILE)
            print("(已自动保存)")


if __name__ == "__main__":
    main()
