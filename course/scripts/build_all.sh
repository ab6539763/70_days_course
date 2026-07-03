#!/bin/bash
# 一键生成全部课件并导出
set -e
cd "$(dirname "$0")"

echo "=== Step 1: 生成基础课件 ==="
python3 generate_course.py

echo "=== Step 2: 深度扩充 ==="
python3 enrich_content.py

echo "=== Step 3: 补充知识库 ==="
python3 supplement_knowledge.py

echo "=== Step 4: 导出 PPT ==="
pip install -q python-pptx 2>/dev/null || true
python3 export_ppt.py

echo "=== 完成 ==="
echo "Markdown: ../days/day01.md ~ day70.md"
echo "PPT:      ../exports/ppt/day01.pptx ~ day70.pptx"
wc -l ../days/*.md | tail -1
