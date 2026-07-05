# =============================================
# Day 07 · 周测上机练习:笔试编程题参考实现
# 文件:week1_quiz_practice.py
# =============================================


def word_freq(text: str) -> dict:
    """统计英文文本词频:按空白拆分、统一小写、剥两端标点。

    周测第 13 题参考实现。
    评分点:拆分(split)、清洗(strip 标点 + lower)、字典计数器、assert。
    """
    counter: dict = {}
    for raw_word in text.split():                 # 按任意空白拆
        word = raw_word.strip(".,!?").lower()     # 剥两端标点 + 小写(链式)
        if not word:                              # 纯标点剥完剩空串:跳过
            continue
        counter[word] = counter.get(word, 0) + 1  # 字典计数器
    return counter


# ---- assert 验证 ----
assert word_freq("Go go GO!") == {"go": 3}
assert word_freq("Hi, hi. Bye!") == {"hi": 2, "bye": 1}
assert word_freq("") == {}
print("✓ word_freq 全部测试通过")

# ---- 演示 ----
sample = "Python is great. Python is simple, and Python is powerful!"
for word, n in sorted(word_freq(sample).items(), key=lambda kv: -kv[1]):
    print(f"{word:<10}{n}")
