# =============================================
# 批量文档关键词统计工具(Day 11 实操成果)
# 需求编号:REQ-D11-001
# 架构:工具层(read_text_smart/clean_text/count_keywords)+ 主流程
# 这是 Day 28 RAG 文档处理流水线的第一块真实积木:
#   批量找文件 → 容错读取 → 清洗 → 统计 → 报告落盘
# =============================================
import json
import re
from datetime import datetime
from pathlib import Path

SAMPLE_DIR = Path(__file__).parent / "sample_docs"     # 样例数据目录
KEYWORDS = ["退款", "发票", "物流", "会员", "优惠券", "投诉"]


# ──────────────── 工具层 ────────────────

def read_text_smart(path: Path) -> str | None:
    """智能读取文本:UTF-8 → GBK 逐个尝试;都失败返回 None。

    EAFP 的教科书应用:不去"检测"编码(检测本质是猜),
    直接试着读,读坏了(UnicodeDecodeError)换下一套翻译规则。
    """
    for encoding in ("utf-8", "gbk"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue                      # 这套规则不对,换下一套
        except OSError:                   # 权限/损坏等读取失败:也算坏文件
            return None
    return None                           # 所有编码都失败


def clean_text(text: str) -> str:
    """清洗:小写 → 正则去网址/邮箱 → 规范空白。"""
    text = text.lower()
    text = re.sub(r"https?://\S+", " ", text)         # 网址:http(s):// 后一串非空白
    text = re.sub(r"[\w.]+@[\w.]+", " ", text)        # 邮箱(简化模式;注释是纪律)
    return " ".join(text.split())                     # Day 02 的老朋友收尾


def count_keywords(text: str, keywords: list, counter: dict,
                   file_sets: dict, filename: str) -> None:
    """统计一个文件:词频进 counter,出现过的文件进 file_sets 的集合。

    已知局限:count 是子串匹配,"非会员"里的"会员"也会被算——
    精确方案是中文分词(jieba),Day 33 BM25 检索时正式登场。
    """
    for kw in keywords:
        n = text.count(kw)
        if n > 0:
            counter[kw] = counter.get(kw, 0) + n      # 字典计数器第 N 次上岗
            file_sets[kw].add(filename)               # 集合去重:一个文件只算一次


def make_sample_docs() -> None:
    """生成样例数据:2 个 UTF-8、1 个 GBK、1 个二进制坏文件。"""
    SAMPLE_DIR.mkdir(exist_ok=True)
    (SAMPLE_DIR / "sub").mkdir(exist_ok=True)

    (SAMPLE_DIR / "记录1.txt").write_text(
        "用户询问退款流程,客服说明退款需 7 天。用户又问发票怎么开,"
        "详情见 https://help.example.com/invoice 或联系 kefu@example.com。"
        "最后用户抱怨物流太慢,提出投诉。", encoding="utf-8")

    (SAMPLE_DIR / "sub" / "记录2.txt").write_text(
        "会员用户咨询优惠券使用规则,优惠券不能与会员折扣叠加。"
        "用户表示理解,没有投诉。", encoding="utf-8")

    (SAMPLE_DIR / "老系统导出.txt").write_text(
        "老系统记录:用户要求退款并开发票,已转人工。", encoding="gbk")   # GBK!

    (SAMPLE_DIR / "损坏文件.txt").write_bytes(bytes([0xFF, 0xFE, 0x00, 0x81, 0x99]))  # 二进制假 txt


# ──────────────── 主流程 ────────────────

def main() -> None:
    make_sample_docs()                                # 准备样例(真实场景删掉这行)
    start = datetime.now()                            # 计时起点

    counter: dict = {}
    file_sets: dict = {kw: set() for kw in KEYWORDS}  # 字典推导式:每词一个空集合
    ok_files, bad_files, total_chars = [], [], 0

    for path in SAMPLE_DIR.rglob("*.txt"):            # 递归扫描
        text = read_text_smart(path)
        if text is None:                              # 坏文件:记账,不搞崩整批
            bad_files.append(str(path))
            continue
        text = clean_text(text)
        total_chars += len(text)
        count_keywords(text, KEYWORDS, counter, file_sets, path.name)
        ok_files.append(str(path))

    elapsed = (datetime.now() - start).total_seconds()

    # ── 控制台报告:按词频降序 ──
    print(f"{'关键词':<8}{'出现次数':>8}{'涉及文件数':>10}")
    print("-" * 30)
    for kw, n in sorted(counter.items(), key=lambda kv: -kv[1]):
        print(f"{kw:<8}{n:>8}{len(file_sets[kw]):>10}")

    # ── JSON 报告落盘:时间戳文件名(报告是快照,保留历史) ──
    report = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "keyword_counts": counter,
        # 集合转 sorted 列表:JSON 六种类型里没有集合!
        "keyword_files": {kw: sorted(s) for kw, s in file_sets.items()},
        "summary": {"ok": len(ok_files), "bad": len(bad_files),
                    "total_chars": total_chars, "elapsed_seconds": elapsed},
    }
    report_name = f"report_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    with open(report_name, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n报告已保存:{report_name}")
    print(f"成功 {len(ok_files)} 个,跳过坏文件 {len(bad_files)} 个,"
          f"总字数 {total_chars},耗时 {elapsed:.3f}s")

    # ── 验收断言 ──
    assert len(ok_files) == 3 and len(bad_files) == 1     # GBK 能读,坏文件被跳过
    assert counter["退款"] >= 2                            # 两个文件都提到退款
    assert len(file_sets["投诉"]) == 2                     # "没有投诉"也含"投诉":子串匹配的已知局限
    print("✓ 验收通过")


if __name__ == "__main__":
    main()
