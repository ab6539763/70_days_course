#!/usr/bin/env python3
"""
将 Markdown 课件转换为 PPTX 演示文稿。
每节课程按 ## 标题自动分页，代码块保留等宽字体。
"""

import re
import sys
from pathlib import Path

try:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
except ImportError:
    print("请先安装: pip install python-pptx")
    sys.exit(1)


def parse_sections(md_content: str) -> list[dict]:
    """按 ## 标题解析 Markdown 为幻灯片章节。"""
    sections = []
    current = {"title": "封面", "body": []}
    
    for line in md_content.split("\n"):
        if line.startswith("## "):
            if current["body"] or current["title"] != "封面":
                sections.append(current)
            current = {"title": line[3:].strip(), "body": []}
        elif line.startswith("# "):
            current["title"] = line[2:].strip()
        else:
            current["body"].append(line)
    
    if current["body"] or current["title"]:
        sections.append(current)
    
    return sections


def clean_text(lines: list[str], max_chars: int = 800) -> str:
    """清理 Markdown 标记，截断过长文本。"""
    text = "\n".join(lines)
    text = re.sub(r"```[\w]*\n", "[代码]\n", text)
    text = re.sub(r"```", "", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"<details>.*?</details>", "", text, flags=re.DOTALL)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text[:max_chars] + ("..." if len(text) > max_chars else "")


def md_to_pptx(md_path: Path, pptx_path: Path):
    """将单个 Markdown 文件转为 PPTX。"""
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    content = md_path.read_text(encoding="utf-8")
    sections = parse_sections(content)
    
    # 封面
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    title_box = slide.shapes.add_textbox(Inches(1), Inches(2.5), Inches(11), Inches(2))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = sections[0]["title"] if sections else md_path.stem
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0x1a, 0x56, 0xdb)
    
    # 内容页
    for sec in sections[1:]:
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # 标题
        title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12), Inches(0.8))
        tf = title_box.text_frame
        p = tf.paragraphs[0]
        p.text = sec["title"]
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = RGBColor(0x1a, 0x56, 0xdb)
        
        # 正文
        body_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.2), Inches(12), Inches(5.8))
        tf = body_box.text_frame
        tf.word_wrap = True
        body_text = clean_text(sec["body"])
        
        for i, para in enumerate(body_text.split("\n")):
            if not para.strip():
                continue
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = para.strip()
            p.font.size = Pt(14)
            p.space_after = Pt(6)
    
    pptx_path.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(pptx_path))
    print(f"  ✓ {pptx_path.name}")


def main():
    courseware_dir = Path("/workspace/courseware")
    output_dir = Path("/workspace/output/pptx")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    md_files = sorted(courseware_dir.rglob("day*.md"))
    print(f"转换 {len(md_files)} 个 Markdown 文件为 PPTX...")
    
    for md_path in md_files:
        rel = md_path.relative_to(courseware_dir)
        pptx_path = output_dir / rel.with_suffix(".pptx")
        md_to_pptx(md_path, pptx_path)
    
    print(f"\n完成！PPTX 文件保存在: {output_dir}")


if __name__ == "__main__":
    main()
