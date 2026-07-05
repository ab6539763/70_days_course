# Day 1 个人信息卡片项目

## 运行方式

```bash
cd code/day01
python -m src.main
```

## 目录说明

| 文件 | 职责 |
|------|------|
| `src/config.py` | 常量配置 |
| `src/validators.py` | 输入校验 |
| `src/input_handler.py` | 交互采集 |
| `src/renderer.py` | 名片渲染 |
| `src/main.py` | 程序入口 |

## 学习建议

1. 先运行看效果
2. 从 `main.py` 倒着读调用链
3. 尝试修改 `config.py` 中的 `CARD_WIDTH`
