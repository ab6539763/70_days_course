# Day 05 思考记录(参考范例)

## 思考题 1:两数之和的字典解法为什么快?

双层循环:外层 n 次 × 内层平均 n/2 次 ≈ n² 级比对(1 万个数约 5 千万次)。

字典版:遍历一次共 n 步,每步"查搭档在不在"是哈希直取(常数时间),总量 n 级。

快在:**"挨个找搭档"被"算出搭档的位置"替代**——哈希把查找从线性降为常数。这是"选对数据结构 = 换一个数量级性能"的经典案例,也是今天哈希原理的第一次实战变现。

```python
# 字典解法参考
def two_sum(nums, target):
    seen = {}                          # 值 → 下标
    for i, n in enumerate(nums):
        need = target - n              # 我需要的搭档
        if need in seen:               # 哈希直查:一步
            return [seen[need], i]
        seen[n] = i                    # 没配上,把自己登记进去
```

## 思考题 2:模型输出的 JSON 会怎么"不标准"?怎么处理?

常见不标准形态:
1. 前后夹带解释文字("好的,以下是JSON:{...} 希望对你有帮助");
2. 用 Markdown 代码块包裹(```json ... ```);
3. 尾逗号、单引号、未转义的内嵌引号;
4. 半截 JSON(被 max_tokens 截断,finish_reason=length)。

工程处理思路(约束 + 提取 + 容错):
1. Prompt 严格约束"只输出 JSON,不要任何其他文字"(Day 17/18);
2. 解析前先"掏":用 find("{") 和 rfind("}") 切片抠出 JSON 主体;
3. try/except 包住 loads,失败就重试或让模型自己修(Day 18);
4. 治本:用 API 的 JSON Mode / Function Calling 保证格式(Day 18/19)。
