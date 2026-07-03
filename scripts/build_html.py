#!/usr/bin/env python3
"""将 Markdown 课件批量转换为独立 HTML 页面（可在浏览器中打印为 PDF）。"""

import re
from pathlib import Path

try:
    import markdown
    from markdown.extensions.tables import TableExtension
    from markdown.extensions.fenced_code import FencedCodeExtension
    from markdown.extensions.toc import TocExtension
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown", "-q"])
    import markdown
    from markdown.extensions.tables import TableExtension
    from markdown.extensions.fenced_code import FencedCodeExtension
    from markdown.extensions.toc import TocExtension

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
  body {{ font-family: "Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
         max-width: 900px; margin: 0 auto; padding: 2rem; line-height: 1.8; color: #333; }}
  h1 {{ color: #1a56db; border-bottom: 2px solid #1a56db; padding-bottom: 0.5rem; }}
  h2 {{ color: #1e40af; margin-top: 2rem; }}
  h3 {{ color: #374151; }}
  code {{ background: #f3f4f6; padding: 2px 6px; border-radius: 4px; font-size: 0.9em; }}
  pre {{ background: #1f2937; color: #e5e7eb; padding: 1rem; border-radius: 8px; overflow-x: auto; }}
  pre code {{ background: none; color: inherit; }}
  table {{ border-collapse: collapse; width: 100%; margin: 1rem 0; }}
  th, td {{ border: 1px solid #d1d5db; padding: 8px 12px; text-align: left; }}
  th {{ background: #f9fafb; }}
  blockquote {{ border-left: 4px solid #1a56db; margin: 1rem 0; padding: 0.5rem 1rem;
                background: #eff6ff; }}
  details {{ margin: 1rem 0; padding: 1rem; background: #f9fafb; border-radius: 8px; }}
  @media print {{ body {{ max-width: 100%; }} pre {{ white-space: pre-wrap; }} }}
</style>
</head>
<body>
{content}
</body>
</html>"""


def md_to_html(md_path: Path, html_path: Path):
    text = md_path.read_text(encoding="utf-8")
    title_match = re.search(r"^# (.+)$", text, re.MULTILINE)
    title = title_match.group(1) if title_match else md_path.stem

    md = markdown.Markdown(extensions=[
        TableExtension(), FencedCodeExtension(), TocExtension(),
        "nl2br", "sane_lists"
    ])
    html_body = md.convert(text)
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(HTML_TEMPLATE.format(title=title, content=html_body), encoding="utf-8")


def main():
    courseware = Path("/workspace/courseware")
    output = Path("/workspace/output/html")
    files = sorted(courseware.rglob("day*.md"))
    print(f"转换 {len(files)} 个 Markdown 为 HTML...")
    for md in files:
        rel = md.relative_to(courseware)
        html = output / rel.with_suffix(".html")
        md_to_html(md, html)
        print(f"  ✓ {rel}")
    print(f"\n完成！HTML 保存在: {output}")
    print("提示: 在浏览器中打开 HTML 文件，使用 Ctrl+P 可打印/保存为 PDF")


if __name__ == "__main__":
    main()
