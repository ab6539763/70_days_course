# =============================================
# Day 13 · 演示代码 2:生成器与异步入门
# 文件:generator_async_demo.py
# =============================================
import asyncio
import time


# ════════ 生成器:边生产边交付 ════════

def square_gen(n):
    """平方数生成器:要一个下一个,内存里永远只有一个。"""
    for i in range(n):
        yield i ** 2          # yield:交出一个值,暂停在这里等下次索取


gen = square_gen(10)
print(next(gen))              # 0    手动索取
print(next(gen))              # 1    函数从上次暂停处继续!
for sq in square_gen(5):      # for 自动 next 到耗尽
    print(sq, end=" ")        # 0 1 4 9 16
print()

# 一次性用品演示
g = square_gen(3)
print(list(g))                # [0, 1, 4]
print(list(g))                # []  耗尽了!要重新调用函数造新的

# 生成器表达式:无方括号的推导式(其实 Day 05 起一直在用)
total = sum(x ** 2 for x in range(5))
print(total)                  # 30


# ── 主战场:流式输出(Day 24 的语法地基) ──
def fake_llm_stream(answer: str):
    """模拟大模型流式输出:一次吐两个字(真实 API 逐 token 吐)。"""
    for i in range(0, len(answer), 2):
        time.sleep(0.05)                  # 模拟生成延迟
        yield answer[i:i + 2]             # 吐一块,暂停


answer = "大模型的流式输出,本质就是一个生成器:服务器边生成边吐,客户端边收边显示。"
for chunk in fake_llm_stream(answer):
    print(chunk, end="", flush=True)      # Day 01 的 end="" 伏笔正式接上:打字机!
print("\n")


# ════════ asyncio:把等待重叠起来 ════════

async def fetch_summary(doc_id: int) -> str:
    """async def:协程函数——可暂停可恢复(生成器的亲戚)。"""
    print(f"发出请求 {doc_id}")
    await asyncio.sleep(1)               # await:"这里要等,调度器先去忙别的"
    # 真实场景是异步 HTTP 请求;asyncio.sleep 模拟 1 秒网络延迟
    print(f"收到响应 {doc_id}")
    return f"文档{doc_id}的摘要"


async def main():
    start = time.time()

    # 并发:gather 把三个任务一起交给调度器 → 总耗时约 1 秒(不是 3 秒!)
    results = await asyncio.gather(
        fetch_summary(1),
        fetch_summary(2),
        fetch_summary(3),
    )
    print(results)
    print(f"总耗时:{time.time() - start:.1f}s(等待重叠的证明)")


asyncio.run(main())                      # 异步世界的总开关
# 观察输出:三个"发出请求"几乎同时,1 秒后三个"收到响应"一起到。
# 纪律:①协程调用不执行,必须 await/gather/run;
#      ②async 世界禁用 time.sleep/requests(会堵死调度器)
