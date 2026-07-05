"""chatlib 演示入口:体验包化后的使用体验。

运行方式:必须从项目根目录(week2_project/)执行:
    python main.py
"""
from chatlib import ChatSession, DeepSeekModel, FakeModel, ChatLibError, RateLimitError
# ↑ 一行拿到所有主角:__init__.py 门面的功劳


def main() -> None:
    session = ChatSession("包化演示", system_prompt="你是助教")
    model = FakeModel()                     # 开发期用假模型:不花钱

    for question in ["什么是包?", "什么是异常?"]:
        session.add_user(question)
        try:
            reply = model.chat(session.to_api_format())
        except ChatLibError as e:           # 家谱一网打尽:chatlib 的错误统一兜底
            reply = f"(服务异常:{e})"
        session.add_assistant(reply)

    session.show()

    # ---- 演示异常分路处理:注入失败的假模型 ----
    print("\n—— 异常分路演示 ——")
    flaky = FakeModel(fail_times=1)
    for attempt in (1, 2):
        try:
            print(f"第 {attempt} 次:{flaky.chat([{'role': 'user', 'content': 'hi'}])}")
        except RateLimitError as e:
            print(f"第 {attempt} 次:被限流({e}),稍后重试")

    # ---- 演示真模型(模拟版) ----
    print("\n—— DeepSeek 模拟调用 ——")
    ds = DeepSeekModel()
    print(ds.chat([{"role": "user", "content": "什么是虚拟环境?"}]))
    print(f"用量:{ds.count_usage()}")


if __name__ == "__main__":
    main()
