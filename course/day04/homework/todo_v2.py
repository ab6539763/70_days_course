# =============================================
# Day 04 作业 · 编程题 5:待办管理器 v2(新增修改与排序显示)
# 考点:索引赋值改元素;sorted vs sort 的选择
# =============================================

todos = []
done_list = []

while True:
    print()
    print("=" * 44)
    print(f"   待办管理器 v2   待办 {len(todos)} 项 / 完成 {len(done_list)} 项")
    print("=" * 44)
    print("  1 查看  2 添加  3 完成  4 删除  5 统计")
    print("  6 修改  7 按长度排序显示  0 退出")
    choice = input("请选择:").strip()

    if choice == "1":
        if not todos and not done_list:
            print("清单空空如也,用功能 2 添加第一件事吧!")
        if todos:
            print("【待办】")
            for i, task in enumerate(todos, start=1):
                print(f"  {i}. {task}")
        if done_list:
            print("【已完成】")
            for task in done_list:
                print(f"  ✓ {task}")

    elif choice == "2":
        task = input("输入待办内容:").strip()
        if not task:
            print("内容不能为空!")
        elif task in todos:
            print(f"「{task}」已在清单里了")
        else:
            todos.append(task)
            print(f"已添加:「{task}」")

    elif choice == "3":
        if not todos:
            print("没有待办事项可完成")
        else:
            num_text = input(f"完成第几项?(1-{len(todos)}):").strip()
            if not num_text.isdigit() or not (1 <= int(num_text) <= len(todos)):
                print("编号无效!")
            else:
                idx = int(num_text) - 1
                finished = todos.pop(idx)
                done_list.append(finished)
                print(f"完成:「{finished}」,漂亮!")

    elif choice == "4":
        if not todos:
            print("没有待办事项可删除")
        else:
            num_text = input(f"删除第几项?(1-{len(todos)}):").strip()
            if not num_text.isdigit() or not (1 <= int(num_text) <= len(todos)):
                print("编号无效!")
            else:
                idx = int(num_text) - 1
                confirm = input(f"确定删除「{todos[idx]}」?(y/n):").strip().lower()
                if confirm == "y":
                    removed = todos.pop(idx)
                    print(f"已删除:「{removed}」")
                else:
                    print("已取消")

    elif choice == "5":
        total = len(todos) + len(done_list)
        if total == 0:
            print("暂无数据")
        else:
            rate = len(done_list) / total
            print(f"待办 {len(todos)} | 已完成 {len(done_list)} | 完成率 {rate:.1%}")

    # ---- 功能 6:修改(本次作业新增) ----
    elif choice == "6":
        if not todos:
            print("没有待办可修改")
        else:
            num_text = input(f"修改第几项?(1-{len(todos)}):").strip()
            if not num_text.isdigit() or not (1 <= int(num_text) <= len(todos)):
                print("编号无效!")
            else:
                idx = int(num_text) - 1
                new_task = input(f"「{todos[idx]}」改为:").strip()
                if not new_task:
                    print("内容不能为空!")
                elif new_task in todos:
                    print("与现有待办重复!")
                else:
                    todos[idx] = new_task          # 列表可变:索引赋值直接改
                    print("修改成功")

    # ---- 功能 7:按长度排序显示(本次作业新增) ----
    elif choice == "7":
        # 用 sorted 而不是 sort:只是"换个视角看",不能破坏用户的添加顺序
        # (原顺序也是信息:先加的先办。展示性排序永远用 sorted)
        for i, task in enumerate(sorted(todos, key=len), start=1):
            print(f"  {i}. {task}")

    elif choice == "0":
        total = len(todos) + len(done_list)
        print(f"本次共管理 {total} 项事务,再见!")
        break

    else:
        print(f"没有选项 [{choice}]")
