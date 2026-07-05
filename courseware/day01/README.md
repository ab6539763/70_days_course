# Day 1 课件索引

| 文件 | 说明 |
|------|------|
| [旁白导读.md](./旁白导读.md) | 学前读：心态、衔接、误区 |
| [Day01-开发环境与第一行代码.md](./Day01-开发环境与第一行代码.md) | **主课件（≥30000字）** |
| [需求文档.md](./需求文档.md) | 个人信息卡片 PRD |
| [架构设计.md](./架构设计.md) | 模块划分与接口 |
| [流程图与示意图.md](./流程图与示意图.md) | Mermaid / ASCII 图 |
| [课堂笔记精华.md](./课堂笔记精华.md) | 可打印一页纸 |
| [作业与标准答案.md](./作业与标准答案.md) | 8 套作业 + 答案 |

## 配套代码

路径：`../../code/day01/`

```bash
cd code/day01
python mvp_card.py          # 10 分钟 MVP
python -m src.main          # 企业级拆分版
python -m unittest tests.test_validators  # 单元测试
```

## 字数说明

主课件 `Day01-开发环境与第一行代码.md` 由 `scripts/generate_day01_courseware.py` 生成并校验，正文字数 **≥ 30000**。

## 下一日

[Day 02 运算符与字符串](../day02/)（待发布）
