# Day 22: 前端速成

> **培训阶段**: 第二阶段 大模型理论与 API | **第 4 周 | **学习时长**: 约 6-8 小时  
> **今日关键词**: HTML、CSS、JavaScript、fetch、静态聊天界面

---

## 📍 课程导航

### 上节回顾
**Day 21** 我们完成了第 3 周总结：

- 理论周测检验 Day 15-20 知识掌握
- 全能 AI 助手综合项目（多轮对话 + 工具调用 + 流式输出）
- 识别知识薄弱点并补漏

从本周开始，我们将把命令行 AI 助手 **升级为 Web 应用**——这是大模型应用交付的标准形态。

### 本节学习目标
完成本日学习后，你将能够：

1. 理解 HTML 页面结构和常用标签
2. 使用 CSS 美化页面布局与样式
3. 编写基础 JavaScript 实现交互逻辑
4. 使用 `fetch` API 发送 HTTP 请求
5. 搭建一个可运行的静态聊天界面原型

### 与后续课程的衔接
- **Day 1** 字符串与变量 → JavaScript 语法类似 Python
- **Day 5** JSON → fetch 请求/响应都是 JSON
- **Day 12** API 调用 → 今天用 JavaScript fetch 替代 Python requests
- **Day 16** 流式输出 → Day 24 前端将对接 SSE 流式接口
- **Day 23-24** FastAPI 后端 → 今天的前端将与后端联调
- **Day 25+** RAG → Web 界面是 RAG 应用的用户入口

---

## 🌅 上午课程（9:00 - 12:00）

### 9:00 - 9:45 | 模块一：HTML 基础

#### 1.1 HTML 是什么

**HTML（HyperText Markup Language）** 是网页的骨架，用标签描述页面结构。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>我的第一个网页</title>
</head>
<body>
    <h1>你好，大模型！</h1>
    <p>这是一个段落。</p>
</body>
</html>
```

#### 1.2 常用 HTML 标签

| 标签 | 作用 | 示例 |
|------|------|------|
| `<h1>`-`<h6>` | 标题 | `<h1>主标题</h1>` |
| `<p>` | 段落 | `<p>一段文字</p>` |
| `<div>` | 容器/区块 | `<div>内容区域</div>` |
| `<span>` | 行内容器 | `<span>高亮文字</span>` |
| `<input>` | 输入框 | `<input type="text">` |
| `<button>` | 按钮 | `<button>点击</button>` |
| `<textarea>` | 多行输入 | `<textarea rows="3"></textarea>` |
| `<ul>/<li>` | 无序列表 | `<ul><li>项目</li></ul>` |
| `<img>` | 图片 | `<img src="photo.jpg" alt="描述">` |
| `<a>` | 链接 | `<a href="https://...">链接</a>` |

#### 1.3 聊天界面 HTML 骨架

```html
<!-- day22/index.html -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 聊天助手</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-container">
        <!-- 顶部标题栏 -->
        <header class="header">
            <h1>🤖 AI 聊天助手</h1>
            <button id="clearBtn" class="btn-secondary">清除对话</button>
        </header>

        <!-- 聊天消息区域 -->
        <main class="chat-area" id="chatArea">
            <div class="message assistant">
                <div class="avatar">🤖</div>
                <div class="bubble">
                    你好！我是 AI 助手，有什么可以帮你的吗？
                </div>
            </div>
        </main>

        <!-- 底部输入区域 -->
        <footer class="input-area">
            <textarea
                id="userInput"
                placeholder="输入你的问题..."
                rows="1"
            ></textarea>
            <button id="sendBtn" class="btn-primary">发送</button>
        </footer>
    </div>

    <script src="app.js"></script>
</body>
</html>
```

---

### 9:45 - 10:30 | 模块二：CSS 基础

#### 2.1 CSS 是什么

**CSS（Cascading Style Sheets）** 控制页面的外观：颜色、布局、字体、间距。

```css
/* 选择器 { 属性: 值; } */
h1 {
    color: #333;
    font-size: 24px;
    text-align: center;
}
```

#### 2.2 选择器

| 选择器 | 示例 | 匹配 |
|--------|------|------|
| 标签 | `p { }` | 所有 `<p>` |
| 类 | `.message { }` | class="message" |
| ID | `#chatArea { }` | id="chatArea" |
| 后代 | `.message .bubble { }` | message 内的 bubble |

#### 2.3 Flexbox 布局

```css
/* 水平排列，垂直居中 */
.container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
}
```

#### 2.4 聊天界面样式

```css
/* day22/style.css */

/* 全局重置 */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: #f0f2f5;
    height: 100vh;
}

/* 应用容器 */
.app-container {
    max-width: 800px;
    margin: 0 auto;
    height: 100vh;
    display: flex;
    flex-direction: column;
    background: #fff;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
}

/* 顶部标题栏 */
.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 24px;
    border-bottom: 1px solid #e8e8e8;
    background: #fff;
}

.header h1 {
    font-size: 18px;
    color: #333;
}

/* 聊天区域 */
.chat-area {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 16px;
}

/* 消息气泡 */
.message {
    display: flex;
    gap: 12px;
    max-width: 85%;
}

.message.user {
    align-self: flex-end;
    flex-direction: row-reverse;
}

.message.assistant {
    align-self: flex-start;
}

.avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
}

.message.user .avatar {
    background: #e3f2fd;
}

.message.assistant .avatar {
    background: #f3e5f5;
}

.bubble {
    padding: 12px 16px;
    border-radius: 12px;
    line-height: 1.6;
    font-size: 15px;
    word-wrap: break-word;
}

.message.user .bubble {
    background: #1976d2;
    color: #fff;
    border-bottom-right-radius: 4px;
}

.message.assistant .bubble {
    background: #f5f5f5;
    color: #333;
    border-bottom-left-radius: 4px;
}

/* 输入区域 */
.input-area {
    display: flex;
    gap: 12px;
    padding: 16px 24px;
    border-top: 1px solid #e8e8e8;
    background: #fff;
}

.input-area textarea {
    flex: 1;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 12px;
    font-size: 15px;
    resize: none;
    outline: none;
    font-family: inherit;
    max-height: 120px;
}

.input-area textarea:focus {
    border-color: #1976d2;
}

/* 按钮 */
.btn-primary {
    background: #1976d2;
    color: #fff;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-size: 15px;
    cursor: pointer;
    transition: background 0.2s;
}

.btn-primary:hover {
    background: #1565c0;
}

.btn-primary:disabled {
    background: #bbb;
    cursor: not-allowed;
}

.btn-secondary {
    background: transparent;
    color: #666;
    border: 1px solid #ddd;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 13px;
    cursor: pointer;
}

.btn-secondary:hover {
    background: #f5f5f5;
}

/* 加载动画 */
.typing-indicator {
    display: flex;
    gap: 4px;
    padding: 8px 0;
}

.typing-indicator span {
    width: 8px;
    height: 8px;
    background: #999;
    border-radius: 50%;
    animation: bounce 1.4s infinite;
}

.typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
.typing-indicator span:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
    0%, 60%, 100% { transform: translateY(0); }
    30% { transform: translateY(-8px); }
}
```

---

### 10:30 - 10:45 | 课间休息

---

### 10:45 - 12:00 | 模块三：JavaScript 基础

#### 3.1 JavaScript 与 Python 对比

| 概念 | Python | JavaScript |
|------|--------|------------|
| 变量 | `name = "张三"` | `let name = "张三"` |
| 常量 | 约定大写 | `const PI = 3.14` |
| 函数 | `def add(a, b):` | `function add(a, b) { }` |
| 条件 | `if x > 0:` | `if (x > 0) { }` |
| 循环 | `for i in items:` | `for (const i of items) { }` |
| 打印 | `print("hi")` | `console.log("hi")` |
| 字典 | `{"key": "val"}` | `{"key": "val"}` 或 `{key: "val"}` |
| 列表 | `[1, 2, 3]` | `[1, 2, 3]` |

#### 3.2 DOM 操作

**DOM（Document Object Model）** 是 HTML 的编程接口，JavaScript 通过 DOM 操作页面元素。

```javascript
// 获取元素
const chatArea = document.getElementById("chatArea");
const userInput = document.querySelector("#userInput");
const sendBtn = document.getElementById("sendBtn");

// 修改内容
chatArea.innerHTML = "<p>新内容</p>";

// 创建元素
const div = document.createElement("div");
div.className = "message user";
div.innerHTML = `<div class="bubble">你好</div>`;
chatArea.appendChild(div);

// 事件监听
sendBtn.addEventListener("click", () => {
    const text = userInput.value.trim();
    if (text) {
        sendMessage(text);
        userInput.value = "";
    }
});

// 键盘事件：Enter 发送，Shift+Enter 换行
userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendBtn.click();
    }
});
```

#### 3.3 异步编程与 fetch

```javascript
// 回调 → Promise → async/await（现代写法）

// 使用 async/await 调用 API
async function callAPI(message) {
    try {
        const response = await fetch("https://api.example.com/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                message: message,
            }),
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();
        return data.reply;
    } catch (error) {
        console.error("API 调用失败:", error);
        return "抱歉，服务暂时不可用。";
    }
}
```

> 💡 **与 Day 12 的联系**：Python 的 `requests.post()` 对应 JavaScript 的 `fetch()`。请求体都是 JSON，只是语法不同。

---

## 🌆 下午课程（14:00 - 17:00）

### 14:00 - 17:00 | 模块四：静态聊天界面实战

#### 4.1 完整 JavaScript 实现

```javascript
// day22/app.js
// 静态聊天界面 - 前端逻辑

// 配置（Day 23 将指向 FastAPI 后端）
const CONFIG = {
    // 暂时直接调用 API（Day 23 改为后端地址）
    apiUrl: "http://localhost:8000/api/chat",
    useMock: true,  // true: 使用模拟回复，false: 调用真实 API
};

// DOM 元素
const chatArea = document.getElementById("chatArea");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const clearBtn = document.getElementById("clearBtn");

// 对话历史
let messages = [];

// 初始化
document.addEventListener("DOMContentLoaded", () => {
    sendBtn.addEventListener("click", handleSend);
    clearBtn.addEventListener("click", handleClear);
    userInput.addEventListener("keydown", handleKeydown);
    userInput.addEventListener("input", autoResize);
});

// 发送消息
async function handleSend() {
    const text = userInput.value.trim();
    if (!text) return;

    // 显示用户消息
    appendMessage("user", text);
    userInput.value = "";
    autoResize();

    // 禁用输入
    setLoading(true);

    try {
        const reply = await sendToAPI(text);
        appendMessage("assistant", reply);
    } catch (error) {
        appendMessage("assistant", "抱歉，出现了错误，请稍后重试。");
        console.error(error);
    } finally {
        setLoading(false);
        userInput.focus();
    }
}

// 调用 API
async function sendToAPI(text) {
    messages.push({ role: "user", content: text });

    if (CONFIG.useMock) {
        // 模拟回复（开发阶段使用）
        await sleep(800);
        const mockReplies = [
            "这是一个很好的问题！让我来帮你分析...",
            "根据我的理解，这个问题可以从以下几个方面来看...",
            "感谢你的提问！我的建议是...",
        ];
        const reply = mockReplies[Math.floor(Math.random() * mockReplies.length)]
            + `\n\n（你说了：「${text}」）`;
        messages.push({ role: "assistant", content: reply });
        return reply;
    }

    const response = await fetch(CONFIG.apiUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: messages }),
    });

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();
    const reply = data.reply;
    messages.push({ role: "assistant", content: reply });
    return reply;
}

// 添加消息到界面
function appendMessage(role, content) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${role}`;

    const avatar = role === "user" ? "👤" : "🤖";
    const formattedContent = formatContent(content);

    messageDiv.innerHTML = `
        <div class="avatar">${avatar}</div>
        <div class="bubble">${formattedContent}</div>
    `;

    chatArea.appendChild(messageDiv);
    chatArea.scrollTop = chatArea.scrollHeight;
}

// 格式化内容（简单的 Markdown 支持）
function formatContent(text) {
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/`([^`]+)`/g, "<code>$1</code>")
        .replace(/\n/g, "<br>");
}

// 清除对话
function handleClear() {
    messages = [];
    chatArea.innerHTML = `
        <div class="message assistant">
            <div class="avatar">🤖</div>
            <div class="bubble">对话已清除。有什么可以帮你的吗？</div>
        </div>
    `;
}

// 加载状态
function setLoading(loading) {
    sendBtn.disabled = loading;
    userInput.disabled = loading;

    if (loading) {
        const indicator = document.createElement("div");
        indicator.className = "message assistant";
        indicator.id = "loadingIndicator";
        indicator.innerHTML = `
            <div class="avatar">🤖</div>
            <div class="bubble">
                <div class="typing-indicator">
                    <span></span><span></span><span></span>
                </div>
            </div>
        `;
        chatArea.appendChild(indicator);
        chatArea.scrollTop = chatArea.scrollHeight;
    } else {
        const indicator = document.getElementById("loadingIndicator");
        if (indicator) indicator.remove();
    }
}

// 键盘事件
function handleKeydown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        handleSend();
    }
}

// 自动调整输入框高度
function autoResize() {
    userInput.style.height = "auto";
    userInput.style.height = Math.min(userInput.scrollHeight, 120) + "px";
}

// 工具函数
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
```

#### 4.2 本地预览

```bash
# 方法一：用 Python 启动简单 HTTP 服务器
cd ~/llm-course/day22
python3 -m http.server 3000
# 浏览器访问 http://localhost:3000

# 方法二：VS Code Live Server 扩展
# 右键 index.html → Open with Live Server
```

#### 4.3 项目结构

```
day22/
├── index.html      # 页面结构
├── style.css       # 样式
├── app.js          # 交互逻辑
└── assets/         # 静态资源（图片等）
```

#### 4.4 界面效果

```
┌─────────────────────────────────────────┐
│  🤖 AI 聊天助手              [清除对话]  │
├─────────────────────────────────────────┤
│                                         │
│  🤖  你好！我是 AI 助手...              │
│                                         │
│                    你好，请介绍一下自己 👤│
│                                         │
│  🤖  我是一个 AI 助手，可以...          │
│                                         │
├─────────────────────────────────────────┤
│  [输入你的问题...          ] [发送]     │
└─────────────────────────────────────────┘
```

#### 4.5 响应式设计补充

```css
/* 移动端适配 */
@media (max-width: 600px) {
    .app-container {
        max-width: 100%;
        height: 100vh;
    }

    .header h1 {
        font-size: 16px;
    }

    .message {
        max-width: 90%;
    }

    .input-area {
        padding: 12px 16px;
    }
}
```

---

## 🌙 晚自习（19:00 - 21:00）

### 19:00 - 20:00 | 前端知识补充

#### 浏览器开发者工具

```
F12 打开开发者工具
├── Elements：查看/修改 HTML 和 CSS
├── Console：查看 JavaScript 日志和错误
├── Network：查看 HTTP 请求（Day 23 调试用）
└── Application：查看本地存储
```

#### 常见错误排查

| 现象 | 可能原因 | 解决 |
|------|----------|------|
| 页面空白 | JS 报错 | 查看 Console |
| 样式不生效 | CSS 路径错误 | 检查 link href |
| 按钮无反应 | 事件未绑定 | 检查 addEventListener |
| fetch 失败 | CORS 跨域 | Day 24 配置后端 CORS |

### 20:00 - 21:00 | 自习答疑

- 完成静态聊天界面，mock 模式可正常对话
- 尝试修改 CSS，自定义主题色
- 预习 Day 23 FastAPI 基础

---

## ✅ 今日知识清单

| 序号 | 知识点 | 掌握程度自评（1-5） |
|------|--------|---------------------|
| 1 | HTML 页面结构与常用标签 | |
| 2 | CSS 选择器与 Flexbox 布局 | |
| 3 | JavaScript 基础语法 | |
| 4 | DOM 操作（获取/创建/修改元素） | |
| 5 | 事件监听（click、keydown） | |
| 6 | async/await 异步编程 | |
| 7 | fetch API 发送 HTTP 请求 | |
| 8 | 聊天界面 HTML/CSS/JS 实现 | |
| 9 | 本地 HTTP 服务器预览 | |
| 10 | 浏览器开发者工具使用 | |

---

## 📝 课后作业

### 必做题

1. **聊天界面**：完成 day22 三个文件，mock 模式下可正常对话
2. **样式定制**：修改主题色（按钮、用户气泡），截图保存
3. **Git 提交**：`git commit -m "Day 22: 前端速成与静态聊天界面"`

### 选做题

4. 添加「暗色模式」切换按钮
5. 实现消息时间戳显示
6. 添加 Markdown 渲染（引入 marked.js 库）

---

## 💡 常见问题 FAQ

**Q1: 我需要精通前端才能做大模型开发吗？**

A: 不需要。大模型应用开发工程师的核心是 Python 后端和 AI 逻辑。前端能看懂、能改模板即可。复杂 UI 可借助 AI 工具生成。

**Q2: 为什么今天不直接对接大模型 API？**

A: 前端直接调用 API 会暴露 API Key，不安全。Day 23-24 通过 FastAPI 后端代理 API 调用，这是标准架构。

**Q3: fetch 和 Python requests 有什么区别？**

A: 功能类似，fetch 是浏览器内置的 HTTP 客户端，returns Promise。语法不同但概念一致。

**Q4: 页面在本地打开（file://）fetch 报错怎么办？**

A: 用 `python3 -m http.server` 启动本地服务器，通过 `http://localhost` 访问。file:// 协议有安全限制。

---

## 🔮 明日预习

**Day 23: FastAPI 后端开发（上）**

明天你将学习：

- FastAPI 框架安装与项目结构
- 路由、请求体、响应体
- Pydantic 数据验证
- **AI 对话 REST API 实现**

**预习建议**：`pip install fastapi uvicorn`，确保 Python 环境就绪。

---

*课程讲义 · 零基础大模型应用开发 70 天培训 · Day 22*
