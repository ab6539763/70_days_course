# 零基础大模型应用开发 — 70 天培训课程课件

> 参考 SVM/K-Means/PCA 课件风格：纳米级粒度拆解 · 项目驱动 · 完整可运行代码 · 环环相扣

## 课程概览

| 项目 | 说明 |
|------|------|
| 培训周期 | 70 天（10 周），每天约 6-8 小时 |
| 目标学员 | 零编程基础或少量基础的转行者、在校生、产品经理 |
| 培养目标 | 独立开发 RAG、Agent、微调小模型并部署上线 |
| 技术栈 | Python、LangChain、LlamaIndex、OpenAI/DeepSeek/Qwen、FastAPI、向量数据库、Docker |

## 目录结构

```
course/
├── README.md              # 本文件
├── OUTLINE.md             # 70 天详细课表
├── days/                  # 每日 Markdown 课件（day01.md ~ day70.md）
├── code/                  # 每日配套代码（day01/ ~ day70/）
├── scripts/
│   ├── generate_course.py     # 课件生成器
│   ├── enrich_content.py      # 内容深度扩充
│   ├── supplement_knowledge.py # 补充知识库
│   ├── export_pdf.py          # 导出 PDF
│   └── export_ppt.py          # 导出 PPT
└── exports/
    ├── pdf/               # PDF 导出目录
    └── ppt/               # PPT 导出目录
```

## 六阶段路线图

| 阶段 | 天数 | 主题 | 阶段项目 |
|------|------|------|----------|
| 一 | Day 1-14 | Python 编程基础 | 命令行多轮对话 AI 助手 |
| 二 | Day 15-24 | 大模型理论与 Prompt 工程 | 网页版 ChatGPT 克隆 |
| 三 | Day 25-38 | LangChain 与 RAG 开发 | 企业级知识库问答系统 |
| 四 | Day 39-50 | Agent 智能体开发 | 多 Agent 智能办公助手 |
| 五 | Day 51-57 | 模型微调与部署 | Docker 容器化部署 |
| 六 | Day 58-70 | 毕业设计与就业冲刺 | 毕业设计 + 模拟面试 |

## 快速开始

### 1. 生成/更新全部课件

```bash
cd course/scripts
python generate_course.py      # 生成 70 天基础课件
python enrich_content.py       # 深度扩充内容
python supplement_knowledge.py # 补充专题知识
```

### 2. 阅读课件

从 [Day 1](days/day01.md) 开始按顺序学习，每天课件包含：

- 课程衔接说明（与前后天关联）
- 今日时间安排
- 纳米级理论精讲
- 完整项目代码
- 课堂练习与知识小测
- 课后作业

### 3. 运行代码

```bash
cd course/code/day01
python day01_personal_card.py
```

### 4. 导出 PDF / PPT

```bash
# PDF（需要 pandoc + texlive-xetex）
pip install -r scripts/requirements.txt
python scripts/export_pdf.py

# PPT（需要 python-pptx）
python scripts/export_ppt.py
```

## 每日课件索引

| 周 | 天数 | 课件 |
|----|------|------|
| 第 1 周 | Day 1-7 | [day01](days/day01.md) · [day02](days/day02.md) · [day03](days/day03.md) · [day04](days/day04.md) · [day05](days/day05.md) · [day06](days/day06.md) · [day07](days/day07.md) |
| 第 2 周 | Day 8-14 | [day08](days/day08.md) · [day09](days/day09.md) · [day10](days/day10.md) · [day11](days/day11.md) · [day12](days/day12.md) · [day13](days/day13.md) · [day14](days/day14.md) |
| 第 3 周 | Day 15-21 | [day15](days/day15.md) · [day16](days/day16.md) · [day17](days/day17.md) · [day18](days/day18.md) · [day19](days/day19.md) · [day20](days/day20.md) · [day21](days/day21.md) |
| 第 4 周 | Day 22-24 | [day22](days/day22.md) · [day23](days/day23.md) · [day24](days/day24.md) |
| 第 5 周 | Day 25-31 | [day25](days/day25.md) · [day26](days/day26.md) · [day27](days/day27.md) · [day28](days/day28.md) · [day29](days/day29.md) · [day30](days/day30.md) · [day31](days/day31.md) |
| 第 6 周 | Day 32-38 | [day32](days/day32.md) · [day33](days/day33.md) · [day34](days/day34.md) · [day35](days/day35.md) · [day36](days/day36.md) · [day37](days/day37.md) · [day38](days/day38.md) |
| 第 7 周 | Day 39-45 | [day39](days/day39.md) · [day40](days/day40.md) · [day41](days/day41.md) · [day42](days/day42.md) · [day43](days/day43.md) · [day44](days/day44.md) · [day45](days/day45.md) |
| 第 8 周 | Day 46-50 | [day46](days/day46.md) · [day47](days/day47.md) · [day48](days/day48.md) · [day49](days/day49.md) · [day50](days/day50.md) |
| 第 9 周 | Day 51-57 | [day51](days/day51.md) · [day52](days/day52.md) · [day53](days/day53.md) · [day54](days/day54.md) · [day55](days/day55.md) · [day56](days/day56.md) · [day57](days/day57.md) |
| 第 10 周 | Day 58-70 | [day58](days/day58.md) · [day59](days/day59.md) · [day60](days/day60.md) · [day61](days/day61.md) · [day62](days/day62.md) · [day63](days/day63.md) · [day64](days/day64.md) · [day65](days/day65.md) · [day66](days/day66.md) · [day67](days/day67.md) · [day68](days/day68.md) · [day69](days/day69.md) · [day70](days/day70.md) |

## 课件特色

1. **纳米级粒度**：每个概念从「人话类比」到「代码实现」逐步拆解
2. **环环相扣**：每天有「课程衔接说明」，明确与前后天的知识关联
3. **项目驱动**：4 个阶段项目 + 1 个毕业设计贯穿始终
4. **完整代码**：关键天提供可直接运行的企业级代码
5. **多格式导出**：支持 Markdown / PDF / PPT 三种格式
