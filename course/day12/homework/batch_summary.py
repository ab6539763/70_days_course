# =============================================
# Day 12 作业 · 编程题 2:批量摘要器
# 骨架:循环 + 单条容错 + 结果记账 + 报告落盘——
#       Day 28 批量向量化、Day 52 批量数据生成的原型(第三次见,闭眼能写)
# 运行:python batch_summary.py --fake(开发)/ 去掉 --fake(真实,注意用量)
# =============================================
import json
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from chatlib_v2 import DeepSeekModel, FakeModel, ChatLibError, AuthError

TEXTS = [
    "大模型应用开发工程师是当前最热门的转行方向之一,岗位要求通常包括 Python、"
    "LangChain、向量数据库和 Prompt 工程,应用层的岗位数量远多于模型层。",
    "RAG(检索增强生成)通过在生成前先检索知识库,让大模型能够回答其训练数据"
    "之外的问题,是企业知识库问答系统的核心技术方案。",
    "Function Calling 让大模型能够调用开发者定义的工具函数,从查天气到查数据库,"
    "这是 Agent 智能体能够'动手做事'的基础机制。",
]


def main() -> None:
    try:
        model = FakeModel() if "--fake" in sys.argv else DeepSeekModel()
    except AuthError:
        print("请先设置 DEEPSEEK_API_KEY")
        return

    results = []
    for i, text in enumerate(TEXTS, start=1):
        messages = [
            {"role": "system",
             "content": "你是摘要助手,用不超过20个字概括用户给的文本,只输出摘要。"},
            {"role": "user", "content": text},
        ]
        try:
            summary = model.chat(messages)
            results.append({"index": i, "source": text[:30], "summary": summary, "ok": True})
            print(f"[{i}] {summary}")
        except ChatLibError as e:                      # 单段失败:记账继续(军规)
            results.append({"index": i, "source": text[:30], "error": str(e), "ok": False})
            print(f"[{i}] 失败:{e}")

    # ── 汇总与报告落盘 ──
    ok_count = len([r for r in results if r["ok"]])
    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "results": results,
        "summary": {"ok": ok_count, "failed": len(results) - ok_count,
                    "total_tokens": model.count_usage()["tokens"]},
    }
    name = f"summary_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(name, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n完成:成功 {ok_count}/{len(results)},报告 → {name}")


if __name__ == "__main__":
    main()
