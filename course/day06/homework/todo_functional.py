# =============================================
# Day 06 作业 · 编程题 4:待办管理器函数化
# 考点:三层架构完整落地(工具层/功能层/入口层)
# 明天周测综合项目《通讯录管理系统》的直接热身
# =============================================


# ──────────────── 工具层 ────────────────

def find_by_index(todos: list, num_text: str) -> dict | None:
    """把用户输入的编号转成待办项字典;非法或越界返回 None。

    dict | None 表示"返回字典或 None"(Python 3.10+ 写法),
    调用方必须处理 None——把"可能失败"写进类型里。
    """
    if not num_text.isdigit():
        return None
    idx = int(num_text) - 1                    # 人类编号 → 索引
    if not (0 <= idx < len(todos)):
        return None
    return todos[idx]


def format_todo(todo: dict) -> str:
    """单条待办的展示格式。只 return 不 print。"""
    mark = "✓" if todo["done"] else "□"
    return f"{mark} [{todo['priority']}] {todo['task']}"


# ──────────────── 功能层 ────────────────

def show_todos(todos: list) -> None:
    """功能:带编号显示全部待办。"""
    if not todos:
        print("清单空空如也!")
        return                                 # 提前返回:空清单直接走人
    for i, todo in enumerate(todos, start=1):
        print(f"  {i}. {format_todo(todo)}")


def add_todo(todos: list) -> None:
    """功能:添加待办(查空、查重、选优先级)。"""
    task = input("待办内容:").strip()
    if not task:
        print("内容不能为空!")
        return
    if any(t["task"] == task for t in todos):  # any:有任一重复即 True
        print("已存在同名待办!")
        return
    priority = input("优先级(高/中/低,默认中):").strip() or "中"   # or 兜底默认
    todos.append({"task": task, "priority": priority, "done": False})
    print(f"已添加:「{task}」")


def finish_todo(todos: list) -> None:
    """功能:按编号标记完成。"""
    show_todos(todos)
    if not todos:
        return
    todo = find_by_index(todos, input("完成第几项?").strip())
    if todo is None:                           # 工具层用 None 报告失败,这里处理
        print("编号无效!")
        return
    todo["done"] = True                        # 改字段即完成(Day 05 重构的红利)
    print(f"完成:「{todo['task']}」")


# ──────────────── 入口层 ────────────────

def main() -> None:
    """程序入口:字典驱动菜单。"""
    todos: list = []                           # 程序状态

    menu = {
        "1": ("查看待办", lambda: show_todos(todos)),
        "2": ("添加待办", lambda: add_todo(todos)),
        "3": ("完成待办", lambda: finish_todo(todos)),
        # lambda 打包带参调用(编程题 5 的技巧提前用上)
    }

    while True:
        print()
        print("=" * 30)
        for key, (name, _) in menu.items():
            print(f"  {key}. {name}")
        print("  0. 退出")
        choice = input("请选择:").strip()

        if choice == "0":
            print("再见!")
            break
        if choice not in menu:
            print(f"没有选项 [{choice}]")
            continue
        _, func = menu[choice]
        func()


if __name__ == "__main__":
    main()
