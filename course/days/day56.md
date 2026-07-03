# Day 56: 应用部署工程化

> **零基础大模型应用开发 70 天培训课程** | 第 56/70 天 | 模型微调与部署


——————





## 深度讲义

### 56.1 Docker Compose 编排

```yaml
version: '3.8'
services:
  api:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://db:5432/chat
    depends_on:
      - db
      - chroma

  db:
    image: postgres:15
    volumes:
      - pg_data:/var/lib/postgresql/data

  chroma:
    image: chromadb/chroma:latest
    volumes:
      - chroma_data:/chroma/chroma

volumes:
  pg_data:
  chroma_data:
```


## 常见错误与避坑

- ⚠️ 只看不练 — 必须动手敲代码
- ⚠️ 跳过基础直接调 API — 每天知识环环相扣
- ⚠️ 不写注释 — 企业级代码必须可读

## 课堂练习

- 📝 复习 Day 55 的核心知识点
- 📝 完成今日实操项目并提交 Git
- 📝 用 3 句话总结今天学到了什么


## 课程衔接说明



### ⬅️ 昨日回顾

**Day 55** 学习了「本地部署与推理服务」，今天的知识直接建立在昨天之上。

### 🔗 今日定位

承接 Day 37 知识库项目，实现生产级部署。

### ➡️ 明日预告

**Day 57** 将学习「周测 + 安全与合规专题」，今天务必打牢基础。


### 今日时间安排

| 时段 | 内容 |
|------|------|
| 09:00-12:00 上午 | Docker 入门: 镜像、容器、Dockerfile 编写 |
| 09:00-12:00 上午 | Docker Compose 编排(应用 + 向量库 + 数据库)、云服务器部署上线 |
| 14:00-17:30 下午 | 🛠️ 把知识库项目容器化并部署到公网可访问 |
| 19:00-21:00 晚自习 | 编写 docker-compose.yml 并测试 |



## 一、今日学习目标



完成今天的学习后，你将能够:

- Docker 入门: 镜像、容器、Dockerfile 编写
- Docker Compose 编排(应用 + 向量库 + 数据库)、云服务器部署上线

### 核心技能点

- **Docker**
- **Docker Compose**
- **云部署**

### 与课程主线的关系

今天是 **第 5 阶段（模型微调与部署）** 的第 6 天。

> 今日主题「应用部署工程化」是整条 70 天学习路径中的关键一环。请对照总路线图理解今天学什么、为什么学、后面哪里会用到。



## 二、理论精讲（纳米级拆解）


### 2.1 Docker 入门: 镜像、容器、Dockerfile 编写

#### 核心概念

| 概念 | 类比 | 说明 |
|------|------|------|
| 镜像 Image | 安装光盘 | 只读模板 |
| 容器 Container | 运行中的程序 | 镜像的实例 |
| Dockerfile | 安装说明书 | 构建镜像的脚本 |
| Docker Compose | 批量启动器 | 多容器编排 |

#### 示例 Dockerfile

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2.2 Docker Compose 编排(应用 + 向量库 + 数据库)、云服务器部署上线

#### RAG 完整链路

```
文档 → 加载 → 分割 → 向量化 → 存储 → 检索 → 增强生成 → 回答
```

#### 核心公式（通俗版）

> 用户问题 → 转成向量 → 在知识库中找最相似的文本块 → 塞进 Prompt → 大模型生成回答

#### 关键参数

| 参数 | 作用 | 调优建议 |
|------|------|----------|
| chunk_size | 每个文本块大小 | 300-1000 字符 |
| chunk_overlap | 块之间重叠 | chunk_size 的 10-20% |
| top_k | 检索返回数量 | 3-10 |
| similarity_threshold | 相似度阈值 | 0.5-0.8 |

## 三、下午实操预告

今日下午核心项目: **Docker 容器化部署**
- 把知识库项目容器化并部署到公网可访问



## 下午实操：项目实战



### 项目名称

**Docker 容器化部署**

### 推荐项目目录结构（企业级标准）

```text
day56_project/
├─ src/
│  ├─ __init__.py
│  └─ main.py
├─ data/
├─ outputs/
├─ tests/
├─ requirements.txt
└─ README.md
```

### 代码骨架

```python
# ================================
# 文件名: day56_main.py
# 主题: Day 56 — Docker 容器化部署
# ================================

"""
Day 56 实操项目入口。

学习要点:
1. 复习昨天所学
2. 完成今日「Docker 容器化部署」核心功能
3. 添加必要注释，提交 Git
"""


def main():
    """主函数 — 按今日课纲逐步实现"""
    print("Day 56: Docker 容器化部署")
    # TODO: 按课件逐步实现
    pass


if __name__ == "__main__":
    main()
```

### 实现步骤（纳米级拆解）

1. **需求确认**: 阅读今日课纲，明确输入/输出
2. **环境准备**: 激活 venv，`pip install` 今日所需依赖
3. **核心实现**: 按上午所学知识点逐步编码
4. **自测**: 手动运行 3 个以上测试用例
5. **提交**: `git add . && git commit -m "Day 56: Docker 容器化部署"`



## 知识小测




**Q1.** 请用自己的话解释「Docker」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 53-56 所学填写）
- 后续应用: 将在 Day 63 左右用到

</details>

**Q2.** 请用自己的话解释「Docker Compose」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 53-56 所学填写）
- 后续应用: 将在 Day 63 左右用到

</details>

**Q3.** 请用自己的话解释「云部署」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 53-56 所学填写）
- 后续应用: 将在 Day 63 左右用到

</details>


### 上机题

请不看课件，独立完成今日「实操项目」的核心功能。限时 60 分钟。



## 课后作业



### 必做

1. 完成今日实操项目「Docker 容器化部署」
2. 提交代码到 GitHub（commit message: `Day 56: Docker 容器化部署`）
3. 在学习笔记中记录 3 个今天学到的新知识点

### 晚自习

- 编写 docker-compose.yml 并测试

### 选做

1. 阅读官方文档中与今日主题相关的章节
2. 尝试优化今日代码（更优雅的错误处理、更清晰的注释）


——————

**第 56/70 天 · 零基础大模型应用开发 70 天培训课程**

> 坚持每一天，70 天后你将成为一名合格的大模型应用开发者。
