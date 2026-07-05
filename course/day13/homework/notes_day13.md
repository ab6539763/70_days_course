# Day 13 思考记录(参考范例)

## 思考题 1:@retry 的异步化改造清单

1. wrapper 变 `async def wrapper`,内部 `return await func(...)`;
2. `time.sleep(delay)` → `await asyncio.sleep(delay)`(不堵调度器);
3. 用 `asyncio.iscoroutinefunction(func)` 判断被装饰对象,或提供 retry / async_retry 双版本。

通用规律:**同步工具搬进异步世界,所有"会等"的操作都要换异步版**。业界的 tenacity 库同时支持两种,原理正是如此。

## 思考题 2:四样东西选一样送给两周前的自己

我选 dotenv:配置管理的痛(临时环境变量天天失效)从 Day 12 才爆发,但如果 Day 01 就有 .env 习惯,Git 泄密风险也从第一天就被堵死,且它学习成本最低(两行)。

第二候选是装饰器:它是读懂框架"魔法一行"的钥匙,但两周前没有闭包和一等公民的地基,提前学吸收不了——**知识有依赖顺序,这正是课程把它排在 Day 13 的理由**。

元认知收获:每周做一次"如果重来我会调整什么"的复盘,学习路径会持续自我优化。
