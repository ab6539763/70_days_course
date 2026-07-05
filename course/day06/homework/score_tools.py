# =============================================
# Day 06 作业 · 编程题 3:成绩工具集
# 考点:*args、默认参数、sorted 不动原列表、assert 自测
# =============================================

def stats(*scores) -> dict:
    """任意个成绩的统计:最高/最低/平均。"""
    if not scores:                                # 防空:*args 收到空元组
        return {"max": 0, "min": 0, "avg": 0}
    return {
        "max": max(scores),
        "min": min(scores),
        "avg": sum(scores) / len(scores),
    }


def top_n(scores: list, n: int = 3) -> list:
    """前 n 高的成绩。用 sorted(不是 sort):绝不修改调用方的原列表。"""
    return sorted(scores, reverse=True)[:n]      # 降序排 + 切片取前 n


def pass_rate(scores: list, line: int = 60) -> float:
    """及格率(0~1)。分数线可调,默认 60。"""
    if not scores:
        return 0.0
    passed = [s for s in scores if s >= line]
    return len(passed) / len(scores)


def main() -> None:
    data = [92, 45, 85, 58, 77, 63]

    print(stats(*data))                          # 列表 * 解包成位置参数——*args 的反向
    print(top_n(data))                           # 默认前 3
    print(top_n(data, n=2))                      # 关键字参数覆盖
    print(f"{pass_rate(data):.1%}")

    # ---- assert 自测:纯函数的红利 ----
    assert stats(90, 80)["avg"] == 85
    assert stats() == {"max": 0, "min": 0, "avg": 0}
    assert top_n([3, 1, 2], n=2) == [3, 2]
    assert pass_rate([60, 59]) == 0.5
    original = [3, 1, 2]
    top_n(original)
    assert original == [3, 1, 2]                 # 验证原列表未被修改!
    print("✓ 全部测试通过")


if __name__ == "__main__":
    main()
