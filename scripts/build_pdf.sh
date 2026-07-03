#!/bin/bash
# 将 Markdown 课件批量转换为 PDF
# 依赖: pandoc + texlive-xetex (中文支持)

set -e

COURSEWARE_DIR="/workspace/courseware"
OUTPUT_DIR="/workspace/output/pdf"
mkdir -p "$OUTPUT_DIR"

# 检查 pandoc
if ! command -v pandoc &> /dev/null; then
    echo "正在安装 pandoc..."
    apt-get update -qq && apt-get install -y -qq pandoc texlive-xetex texlive-fonts-recommended > /dev/null 2>&1
fi

echo "转换 Markdown 课件为 PDF..."

count=0
while IFS= read -r -d '' md_file; do
    rel_path="${md_file#$COURSEWARE_DIR/}"
    pdf_file="$OUTPUT_DIR/${rel_path%.md}.pdf"
    pdf_dir=$(dirname "$pdf_file")
    mkdir -p "$pdf_dir"
    
    pandoc "$md_file" \
        -o "$pdf_file" \
        --pdf-engine=xelatex \
        -V mainfont="Noto Sans CJK SC" \
        -V geometry:margin=2cm \
        -V fontsize=11pt \
        --toc \
        --toc-depth=2 \
        2>/dev/null || {
            # 降级：无中文引擎时用 HTML 转 PDF
            pandoc "$md_file" -o "$pdf_file" -V geometry:margin=2cm 2>/dev/null || true
        }
    
    if [ -f "$pdf_file" ]; then
        echo "  ✓ ${rel_path%.md}.pdf"
        ((count++)) || true
    fi
done < <(find "$COURSEWARE_DIR" -name "day*.md" -print0 | sort -z)

echo ""
echo "完成！共转换 $count 个 PDF 文件"
echo "输出目录: $OUTPUT_DIR"
