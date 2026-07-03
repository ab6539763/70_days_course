"""Day 2: 文本清洗小工具 — 去空格、统一大小写、敏感词替换"""
import re

SENSITIVE_WORDS = ["广告", "spam", "垃圾"]


def clean_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def normalize_case(text: str, mode: str = "lower") -> str:
    if mode == "lower":
        return text.lower()
    if mode == "upper":
        return text.upper()
    return text.title()


def replace_sensitive(text: str, replacement: str = "***") -> str:
    result = text
    for word in SENSITIVE_WORDS:
        result = result.replace(word, replacement)
    return result


def format_report(original: str, cleaned: str) -> str:
    return f"""原文 ({len(original)} 字符):
{original}

清洗后 ({len(cleaned)} 字符):
{cleaned}"""


def main():
    raw = input("请输入待清洗文本: ")
    step1 = clean_whitespace(raw)
    step2 = normalize_case(step1)
    step3 = replace_sensitive(step2)
    print(format_report(raw, step3))


if __name__ == "__main__":
    main()
