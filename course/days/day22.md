# Day 22: 前端速成

> **零基础大模型应用开发 70 天培训课程** | 第 22/70 天 | 大模型基础理论与 Prompt 工程


——————




## 本周学习路线图

> **第 4 周: Web 开发基础**

```
HTML/JS → FastAPI → SSE 流式 → 数据库
                    ↓
            周末项目: 网页版 ChatGPT 克隆
```

本周每一天环环相扣，请按顺序学习，不要跳天。



## 深度讲义

### 22.1 HTML 聊天界面骨架

```html
<!DOCTYPE html>
<html>
<head>
  <title>AI Chat</title>
  <style>
    #chat-box { height: 400px; overflow-y: auto; border: 1px solid #ccc; padding: 10px; }
    .user { text-align: right; color: blue; }
    .assistant { text-align: left; color: green; }
  </style>
</head>
<body>
  <div id="chat-box"></div>
  <input id="input" type="text" placeholder="输入消息...">
  <button onclick="send()">发送</button>
  <script>
    async function send() {
      const input = document.getElementById('input');
      const msg = input.value;
      // Day 24 将对接 FastAPI 后端
      appendMessage('user', msg);
      input.value = '';
    }
    function appendMessage(role, text) {
      const box = document.getElementById('chat-box');
      box.innerHTML += `<div class="${role}">${text}</div>`;
      box.scrollTop = box.scrollHeight;
    }
  </script>
</body>
</html>
```


## 常见错误与避坑

- ⚠️ 只看不练 — 必须动手敲代码
- ⚠️ 跳过基础直接调 API — 每天知识环环相扣
- ⚠️ 不写注释 — 企业级代码必须可读

## 课堂练习

- 📝 复习 Day 21 的核心知识点
- 📝 完成今日实操项目并提交 Git
- 📝 用 3 句话总结今天学到了什么


## 课程衔接说明



### ⬅️ 昨日回顾

**Day 21** 学习了「周测 + 综合练习」，今天的知识直接建立在昨天之上。

### 🔗 今日定位

承接 Day 16 流式概念，为 Day 24 前后端联调做准备。

### ➡️ 明日预告

**Day 23** 将学习「FastAPI 后端开发（上）」，今天务必打牢基础。


### 今日时间安排

| 时段 | 内容 |
|------|------|
| 09:00-12:00 上午 | HTML/CSS 快速入门（只学够用的） |
| 09:00-12:00 上午 | JavaScript 基础、fetch 请求 |
| 14:00-17:30 下午 | 🛠️ 写一个静态聊天界面页面 |
| 19:00-21:00 晚自习 | 美化聊天界面，添加暗色模式 |



## 一、今日学习目标



完成今天的学习后，你将能够:

- HTML/CSS 快速入门（只学够用的）
- JavaScript 基础、fetch 请求

### 核心技能点

- **HTML**
- **CSS**
- **JS fetch**

### 与课程主线的关系

今天是 **第 2 阶段（大模型基础理论与 Prompt 工程）** 的第 8 天。

> 今日主题「前端速成」是整条 70 天学习路径中的关键一环。请对照总路线图理解今天学什么、为什么学、后面哪里会用到。



## 二、理论精讲（纳米级拆解）


### 2.1 HTML/CSS 快速入门（只学够用的）

#### 核心概念

**HTML/CSS 快速入门（只学够用的）** 是今日学习的重要内容。

#### 为什么学？

在大模型应用开发中，这个知识点将在后续项目中直接用到:
- 与 Day 20 的知识形成递进
- 为 Day 25 的实操项目提供基础

#### 学习要点

1. 理解概念定义（用自己的话复述）
2. 跟着课件代码敲一遍（不要复制粘贴）
3. 完成课后练习巩固

#### 常见错误

- 只看不练 → 必须动手写代码
- 跳过基础 → 每天知识环环相扣，不要跳天

### 2.2 JavaScript 基础、fetch 请求

#### 核心概念

**JavaScript 基础、fetch 请求** 是今日学习的重要内容。

#### 为什么学？

在大模型应用开发中，这个知识点将在后续项目中直接用到:
- 与 Day 20 的知识形成递进
- 为 Day 25 的实操项目提供基础

#### 学习要点

1. 理解概念定义（用自己的话复述）
2. 跟着课件代码敲一遍（不要复制粘贴）
3. 完成课后练习巩固

#### 常见错误

- 只看不练 → 必须动手写代码
- 跳过基础 → 每天知识环环相扣，不要跳天

## 三、下午实操预告

今日下午核心项目: **静态聊天界面**
- 写一个静态聊天界面页面



## 下午实操：项目实战



### 项目名称

**静态聊天界面**

### 推荐项目目录结构（企业级标准）

```text
day22_project/
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
# 文件名: day22_main.py
# 主题: Day 22 — 静态聊天界面
# ================================

"""
Day 22 实操项目入口。

学习要点:
1. 复习昨天所学
2. 完成今日「静态聊天界面」核心功能
3. 添加必要注释，提交 Git
"""


def main():
    """主函数 — 按今日课纲逐步实现"""
    print("Day 22: 静态聊天界面")
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
5. **提交**: `git add . && git commit -m "Day 22: 静态聊天界面"`



## 知识小测




**Q1.** 请用自己的话解释「HTML」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 19-22 所学填写）
- 后续应用: 将在 Day 29 左右用到

</details>

**Q2.** 请用自己的话解释「CSS」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 19-22 所学填写）
- 后续应用: 将在 Day 29 左右用到

</details>

**Q3.** 请用自己的话解释「JS fetch」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 19-22 所学填写）
- 后续应用: 将在 Day 29 左右用到

</details>


### 上机题

请不看课件，独立完成今日「实操项目」的核心功能。限时 60 分钟。



## 课后作业



### 必做

1. 完成今日实操项目「静态聊天界面」
2. 提交代码到 GitHub（commit message: `Day 22: 静态聊天界面`）
3. 在学习笔记中记录 3 个今天学到的新知识点

### 晚自习

- 美化聊天界面，添加暗色模式

### 选做

1. 阅读官方文档中与今日主题相关的章节
2. 尝试优化今日代码（更优雅的错误处理、更清晰的注释）


——————

**第 22/70 天 · 零基础大模型应用开发 70 天培训课程**

> 坚持每一天，70 天后你将成为一名合格的大模型应用开发者。
