#!/usr/bin/env python3
"""将 Markdown 课件批量导出为 PDF（依赖 pandoc）"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DAYS_DIR = ROOT / "days"
EXPORT_DIR = ROOT / "exports" / "pdf"


def check_pandoc() -> bool:
    try:
        subprocess.run(["pandoc", "--version"], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def export_pdf():
    if not check_pandoc():
        print("❌ pandoc 未安装。请运行: apt-get install -y pandoc texlive-xetex")
        print("   或使用在线工具将 days/*.md 转为 PDF")
        sys.exit(1)

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    for md in sorted(DAYS_DIR.glob("day*.md")):
        pdf_path = EXPORT_DIR / f"{md.stem}.pdf"
        cmd = [
            "pandoc", str(md),
            "-o", str(pdf_path),
            "--pdf-engine=xelatex",
            "-V", "mainfont=Noto Sans CJK SC",
            "-V", "geometry:margin=2cm",
            "--toc",
        ]
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ {pdf_path.name}")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  {md.name}: {e.stderr.decode()[:200]}")


def export_combined():
    """合并为单本教材 PDF"""
    if not check_pandoc():
        return
    combined_md = EXPORT_DIR.parent / "full_course.md"
    parts = [f"# 零基础大模型应用开发 70 天培训课程\n\n"]
    for md in sorted(DAYS_DIR.glob("day*.md")):
        parts.append(f"\n\n---\n\n")
        parts.append(md.read_text(encoding="utf-8"))
    combined_md.write_text("".join(parts), encoding="utf-8")
    print(f"📄 Combined markdown: {combined_md}")


if __name__ == "__main__":
    export_pdf()
    export_combined()
