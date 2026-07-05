# =============================================
# 命令行 AI 问答小程序(Day 12 实操成果)🎉
# 需求编号:REQ-D12-001
# 运行:python qa_app.py          (真实模式,需要 DEEPSEEK_API_KEY)
#       python qa_app.py --fake   (开发模式,FakeModel 不花钱)
# 注意:本程序是"单轮问答"——每问独立,AI 没有记忆(故意的痛点,Day 14 拆墙)
# =============================================
import sys
import time

from chatlib_v2 import DeepSeekModel, FakeModel, ChatLibError, RateLimitError, AuthError


def main() -> None:
    """入口:单轮问答主循环。"""
    use_fake = "--fake" in sys.argv                 # 最朴素的命令行参数解析

    try:
        model = FakeModel() if use_fake else DeepSeekModel()
    except AuthError:
        print("未检测到 API Key。请先设置环境变量:")
        print('  PowerShell:  $env:DEEPSEEK_API_KEY = "sk-..."')
        print('  macOS/Linux: export DEEPSEEK_API_KEY="sk-..."')
        return                                       # 给出路,不给 traceback

    print(f"AI 问答小程序(模型:{model.model_name})  /exit 退出")
    total_tokens = 0

    while True:                                      # Day 03 的骨架,第 N 次上岗
        try:
            question = input("\n你问:").strip()
        except KeyboardInterrupt:                    # Ctrl+C:优雅道别
            print("\n再见!")
            break

        if not question:                             # 空输入:跳过(真值规则)
            continue
        if question == "/exit":
            print("再见!")
            break

        # ── 单轮:每次都是全新的 messages(没有记忆——故意的痛点) ──
        messages = [
            {"role": "system", "content": "你是一个简洁的AI助手,回答不超过150字"},
            {"role": "user", "content": question},
        ]

        try:
            answer = model.chat(messages)
        except RateLimitError:
            print("(被限流,3 秒后自动重试……)")
            time.sleep(3)
            try:
                answer = model.chat(messages)        # 重试一次(Day 13 用装饰器优雅化)
            except ChatLibError as e:
                print(f"重试仍失败:{e}")
                continue
        except AuthError as e:
            print(f"认证失败:{e}")
            break                                    # Key 坏了,继续也没意义
        except ChatLibError as e:
            print(f"服务异常:{e},请重试")
            continue

        # ── 展示与记账 ──
        used = model.count_usage()["tokens"] - total_tokens
        total_tokens = model.count_usage()["tokens"]
        cost = total_tokens / 1_000_000 * 1.5        # 粗略均价估算(以官网为准)
        print(f"\nAI 答:{answer}")
        print(f"(本轮 {used} tokens,累计 {total_tokens} tokens ≈ {cost:.4f} 元)")

    # 体验作业:连续问"我叫小林" → "我叫什么名字?"——
    # AI 一脸无辜。因为每轮新建 messages,历史根本没发过去。
    # 这堵墙 Day 14 拆:messages 从"每轮新建"改成"持续 append"。


if __name__ == "__main__":
    main()
