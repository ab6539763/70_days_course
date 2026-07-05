# =============================================
# 命令行通讯录管理系统(第一周综合考核项目)
# 需求编号:REQ-D07-001
# 架构:入口层 main / 功能层 / 工具层(纯函数) / 数据层(内存⇄JSON文件)
# 考核点:字典建模、三层架构、输入校验、JSON 持久化、注册表菜单
# =============================================
import json

DATA_FILE = "contacts.json"


# ──────────────── 持久化模板(Day 11 讲原理,今天照抄使用) ────────────────

def save_json(data, filename: str) -> None:
    """把 Python 对象保存为 JSON 文件。(模板函数,Day 11 讲原理)"""
    with open(filename, "w", encoding="utf-8") as f:      # 打开文件准备写(w)
        json.dump(data, f, ensure_ascii=False, indent=2)  # dump 不带 s:直写文件


def load_json(filename: str, default=None):
    """从 JSON 文件加载 Python 对象;文件不存在返回 default。(模板函数)"""
    try:                                                   # 尝试打开(Day 10 讲 try)
        with open(filename, "r", encoding="utf-8") as f:   # 打开文件准备读(r)
            return json.load(f)                            # load 不带 s:直读文件
    except FileNotFoundError:                              # 第一次运行没有文件:正常
        return default if default is not None else []


# ──────────────── 工具层:纯函数,全部可 assert 测试 ────────────────

def is_valid_phone(phone: str) -> bool:
    """校验手机号:11 位纯数字。"""
    return phone.isdigit() and len(phone) == 11


def is_valid_email(email: str) -> bool:
    """校验邮箱:含且只含一个 @,且不在开头。(Day 03 作业规则的函数化)"""
    return email.count("@") == 1 and not email.startswith("@")


def mask_phone(phone: str) -> str:
    """手机号脱敏。第一周写的最后一遍——从此永远复用这一份。"""
    return phone[:3] + "****" + phone[-4:]


def format_contact(c: dict) -> str:
    """单个联系人的展示行。"""
    return f"{c['name']:<8}{mask_phone(c['phone']):<15}[{c.get('group', '未分组')}]"


def find_by_index(contacts: list, num_text: str) -> dict | None:
    """用户编号 → 联系人字典;非法或越界返回 None。"""
    if not num_text.isdigit():
        return None
    idx = int(num_text) - 1                                # 人类编号 → 索引
    if not (0 <= idx < len(contacts)):
        return None
    return contacts[idx]


# ──────────────── 功能层:交互,调用工具层 ────────────────

def list_contacts(contacts: list) -> None:
    """功能 1:带编号显示全部联系人。"""
    if not contacts:
        print("通讯录为空,先添加一个吧!")
        return
    for i, c in enumerate(contacts, start=1):
        print(f"  {i}. {format_contact(c)}")


def add_contact(contacts: list) -> None:
    """功能 2:添加联系人(全字段校验)。"""
    name = input("姓名:").strip()
    if not name:
        print("姓名不能为空!")
        return
    if any(c["name"] == name for c in contacts):           # any + 生成器:查重
        print(f"「{name}」已存在!")
        return

    while True:                                            # 校验循环:手机号
        phone = input("手机号(11位):").strip()
        if is_valid_phone(phone):
            break
        print("手机号必须是 11 位数字!")

    while True:                                            # 校验循环:邮箱
        email = input("邮箱:").strip()
        if is_valid_email(email):
            break
        print("邮箱格式不对!")

    group = input("分组(回车=未分组):").strip() or "未分组"     # or 兜底默认

    contacts.append({"name": name, "phone": phone, "email": email, "group": group})
    print(f"已添加:{name}")


def search_contacts(contacts: list) -> None:
    """功能 3:按关键词模糊搜索姓名或手机号。"""
    keyword = input("关键词:").strip()
    if not keyword:
        print("关键词不能为空!")
        return
    # 推导式过滤:姓名或手机号"包含"关键词即命中
    hits = [c for c in contacts if keyword in c["name"] or keyword in c["phone"]]
    if not hits:
        print(f"没有匹配「{keyword}」的联系人")
        return
    print(f"命中 {len(hits)} 位:")
    for c in hits:
        print(f"  {format_contact(c)}")


def edit_contact(contacts: list) -> None:
    """功能 4:按编号逐字段修改(回车跳过=不改)。"""
    list_contacts(contacts)
    if not contacts:
        return
    c = find_by_index(contacts, input("修改第几位?").strip())
    if c is None:
        print("编号无效!")
        return

    # 逐字段:显示旧值,回车跳过,输入新值则校验后覆盖
    new_name = input(f"姓名({c['name']}):").strip()
    if new_name:
        c["name"] = new_name

    new_phone = input(f"手机号({mask_phone(c['phone'])}):").strip()
    if new_phone:
        if is_valid_phone(new_phone):
            c["phone"] = new_phone
        else:
            print("手机号无效,保留原值")

    new_group = input(f"分组({c.get('group', '未分组')}):").strip()
    if new_group:
        c["group"] = new_group

    print(f"已更新:{format_contact(c)}")


def delete_contact(contacts: list) -> None:
    """功能 5:按编号删除,二次确认。"""
    list_contacts(contacts)
    if not contacts:
        return
    num_text = input("删除第几位?").strip()
    c = find_by_index(contacts, num_text)
    if c is None:
        print("编号无效!")
        return
    confirm = input(f"确定删除「{c['name']}」?(y/n):").strip().lower()
    if confirm == "y":
        contacts.remove(c)                     # 按值删:c 就是列表里的那个字典
        print("已删除")
    else:
        print("已取消")


def group_stats(contacts: list) -> None:
    """功能 6:分组统计——字典计数器的实战。"""
    if not contacts:
        print("通讯录为空")
        return
    counter: dict = {}
    for c in contacts:
        g = c.get("group", "未分组")
        counter[g] = counter.get(g, 0) + 1     # 焊死的三行,今天变现
    for group, num in sorted(counter.items(), key=lambda kv: -kv[1]):   # 人数降序
        print(f"  {group}:{num} 人")


# ──────────────── 入口层 ────────────────

def main() -> None:
    """入口:加载 → 主循环 → 落盘。数据生命周期的全程管理。"""
    contacts = load_json(DATA_FILE, default=[])            # 启动:磁盘唤醒数据
    print(f"已加载 {len(contacts)} 位联系人")

    menu = {
        "1": ("查看全部", lambda: list_contacts(contacts)),
        "2": ("添加", lambda: add_contact(contacts)),
        "3": ("搜索", lambda: search_contacts(contacts)),
        "4": ("修改", lambda: edit_contact(contacts)),
        "5": ("删除", lambda: delete_contact(contacts)),
        "6": ("分组统计", lambda: group_stats(contacts)),
    }

    while True:
        print("\n" + "=" * 32)
        print("      通讯录管理系统 v1.0")
        print("=" * 32)
        for key, (name, _) in menu.items():
            print(f"  {key}. {name}")
        print("  0. 保存并退出")
        choice = input("请选择:").strip()

        if choice == "0":
            save_json(contacts, DATA_FILE)                 # 退出:落盘
            print(f"已保存 {len(contacts)} 位联系人,再见!")
            break
        if choice not in menu:
            print(f"没有选项 [{choice}]")
            continue
        menu[choice][1]()                                  # 取函数并执行


# ──────────────── 工具层自测(运行前先跑一遍) ────────────────
assert is_valid_phone("13812345678")
assert not is_valid_phone("1381234567")        # 10 位:不合法
assert not is_valid_phone("1381234567a")       # 带字母:不合法
assert is_valid_email("a@b.com")
assert not is_valid_email("@b.com")            # @ 在开头
assert not is_valid_email("a@b@c.com")         # 两个 @
assert mask_phone("13812345678") == "138****5678"


if __name__ == "__main__":
    main()
