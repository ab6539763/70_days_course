# =============================================
# Day 13 · 三件套验收演示
# 文件:drill.py(与 chatlib_v3 同目录运行:python drill.py)
# =============================================
from dotenv import load_dotenv

load_dotenv()                            # 三件套之二:入口两行,.env 注入环境变量

from chatlib_v3 import FakeModel, AuthError, RateLimitError
from chatlib_v3.utils import retry


def main() -> None:
    msgs = [{"role": "user", "content": "hi"}]

    # ── 演示 1:@retry 自动恢复(观察指数退避日志) ──
    print("—— 演示 1:限流自动重试 ——")
    flaky = FakeModel(fail_times=2)

    @retry(max_retries=4, retry_on=(RateLimitError,), base_delay=0.2)
    def ask(model, messages):
        return model.chat(messages)

    print(ask(flaky, msgs))              # 前两次失败自动重试,第三次成功,调用方无感
    assert flaky.count_usage()["calls"] == 1

    # ── 演示 2:白名单外的异常不重试,秒失败 ──
    print("\n—— 演示 2:AuthError 不重试 ——")
    flaky2 = FakeModel(fail_times=5)

    @retry(max_retries=4, retry_on=(AuthError,), base_delay=0.2)   # 白名单只有 AuthError
    def ask2(model, messages):
        return model.chat(messages)

    try:
        ask2(flaky2, msgs)
        assert False
    except RateLimitError:
        print("RateLimitError 不在白名单,第一次抛出就直接上抛 ✓")

    print("\n✓ 三件套验收全部通过,chatlib_v3 战备就绪,明天项目一见")


if __name__ == "__main__":
    main()
