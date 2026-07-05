# =============================================
# 命令行待办事项管理器
# 需求编号:REQ-D04-001
# 架构:主循环 + 分发器(Day 03) + 双列表数据层(Day 04)
# 本项目是 Day 14《命令行 AI 助手》的结构预演:
#   todos → messages,"添加待办" → "append 消息 + 调 API",架构复用 80%+
#
# 已知欠账(将在后续课程偿还):
#   1. 程序退出数据即失 → Day 05 JSON 序列化 + Day 11 文件读写解决
#   2. 主循环太胖、编号校验写了两遍 → Day 06 函数重构
#   3. 待办只有内容一个字段 → Day 05 字典建模(内容+时间+优先级)
# =============================================

# ---- 数据层:两个核心列表,程序运行期间的全部"状态" ----
todos = []            # 待办事项
done_list = []        # 已完成事项

while True:
    # ---- 菜单 ----
    print()
    print("=" * 38)
    print(f"   待办管理器   待办 {len(todos)} 项 / 完成 {len(done_list)} 项")
    print("=" * 38)
    print("  1 查看  2 添加  3 完成  4 删除  5 统计  0 退出")
    choice = input("请选择:").strip()

    # ---- 功能 1:查看 ----
    if choice == "1":
        if not todos and not done_list:            # 真值规则:双空 = 什么都没有
            print("清单空空如也,用功能 2 添加第一件事吧!")
        if todos:
            print("【待办】")
            for i, task in enumerate(todos, start=1):     # enumerate:编号+内容
                print(f"  {i}. {task}")
        if done_list:
            print("【已完成】")
            for task in done_list:
                print(f"  ✓ {task}")               # 已完成不需要编号(不再被操作)

    # ---- 功能 2:添加 ----
    elif choice == "2":
        task = input("输入待办内容:").strip()      # 清洗:老规矩
        if not task:                               # 拦空输入(真值规则)
            print("内容不能为空!")
        elif task in todos:                        # 拦重复(in 判断)
            print(f"「{task}」已在清单里了")
        else:
            todos.append(task)                     # 核心动作:append
            print(f"已添加:「{task}」")

    # ---- 功能 3:完成 ----
    elif choice == "3":
        if not todos:
            print("没有待办事项可完成")
        else:
            num_text = input(f"完成第几项?(1-{len(todos)}):").strip()
            # 编号校验:先 isdigit 防非数字,再范围防越界
            if not num_text.isdigit() or not (1 <= int(num_text) <= len(todos)):
                print("编号无效!")
            else:
                idx = int(num_text) - 1            # 用户编号从 1 起,索引从 0 起:减 1 换算
                finished = todos.pop(idx)          # pop:删掉并"递过来"
                done_list.append(finished)         # 接力 append——一删一增完成"移动"
                print(f"完成:「{finished}」,漂亮!")

    # ---- 功能 4:删除(带二次确认)----
    elif choice == "4":
        if not todos:
            print("没有待办事项可删除")
        else:
            num_text = input(f"删除第几项?(1-{len(todos)}):").strip()
            if not num_text.isdigit() or not (1 <= int(num_text) <= len(todos)):
                print("编号无效!")
            else:
                idx = int(num_text) - 1
                # 二次确认:删除不可逆,给用户反悔的机会(产品思维)
                confirm = input(f"确定删除「{todos[idx]}」?(y/n):").strip().lower()
                if confirm == "y":
                    removed = todos.pop(idx)
                    print(f"已删除:「{removed}」")
                else:
                    print("已取消")

    # ---- 功能 5:统计 ----
    elif choice == "5":
        total = len(todos) + len(done_list)
        if total == 0:
            print("暂无数据")
        else:
            rate = len(done_list) / total          # 完成率 = 已完成 / 总数
            print(f"待办 {len(todos)} | 已完成 {len(done_list)} | 完成率 {rate:.1%}")

    # ---- 退出 ----
    elif choice == "0":
        total = len(todos) + len(done_list)
        print(f"本次共管理 {total} 项事务,再见!")
        break

    else:
        print(f"没有选项 [{choice}]")
