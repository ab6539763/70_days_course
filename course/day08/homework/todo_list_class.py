# =============================================
# Day 08 作业 · 编程题 2:TodoList 管理类
# 考点:对象列表管理、海关对的批量使用(对象列表 ⇄ JSON)
# =============================================
import json

from todo_class import Todo         # 复用编程题 1 的类(模块导入,Day 10 正课)
# 若运行报 ImportError,把 todo_class.py 放同目录,或把 Todo 类复制过来


class TodoList:
    """待办清单:Todo 对象的容器与管家。"""

    def __init__(self):
        self.todos: list = []                       # 可变容器 → 实例属性(铁律)

    def add(self, task: str, priority: str = "中") -> bool:
        """添加;重复 task 返回 False。"""
        if any(t.task == task.strip() for t in self.todos):
            return False
        self.todos.append(Todo(task, priority))     # 构造即校验在 Todo 里把关
        return True

    def finish(self, index: int) -> bool:
        """按用户编号(1 起)标记完成;越界返回 False。"""
        idx = index - 1                              # 人类编号 → 索引
        if not (0 <= idx < len(self.todos)):
            return False
        self.todos[idx].finish()
        return True

    def pending(self) -> list:
        """未完成的 Todo 对象列表。"""
        return [t for t in self.todos if not t.done]

    def stats(self) -> dict:
        """统计:总数/完成数/完成率。"""
        total = len(self.todos)
        done = len([t for t in self.todos if t.done])
        return {
            "total": total,
            "done": done,
            "rate": done / total if total else 0.0,
        }

    def save(self, filename: str = "todos.json") -> None:
        """整个清单落盘:对象列表 → 字典列表 → JSON 文件。"""
        data = [t.to_dict() for t in self.todos]     # 逐个过海关
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, filename: str = "todos.json") -> "TodoList":
        """从磁盘复活整个清单:JSON 文件 → 字典列表 → 对象列表。"""
        book = cls()
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            return book                              # 没文件:返回空清单
        book.todos = [Todo.from_dict(d) for d in data]   # 逐个入境
        return book


# ---- 测试 ----
if __name__ == "__main__":
    tl = TodoList()
    assert tl.add("复习OOP", "高")
    assert tl.add("写作业")
    assert not tl.add("复习OOP")                # 重复被拒
    assert tl.finish(1)
    assert not tl.finish(99)                    # 越界被拒
    assert len(tl.pending()) == 1
    assert tl.stats() == {"total": 2, "done": 1, "rate": 0.5}

    tl.save("todos_test.json")
    restored = TodoList.load("todos_test.json")
    assert restored.stats() == tl.stats()       # 存档往返无损
    print("✓ TodoList 全部测试通过")
