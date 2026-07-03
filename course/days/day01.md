# Day 1: 开发环境与第一行代码

> **零基础大模型应用开发 70 天培训课程** | 第 1/70 天 | Python 编程基础


——————




## 本周学习路线图

> **第 1 周: Python 入门**

```
变量 → 字符串 → 流程控制 → 数据结构 → 函数
                    ↓
            周末项目: 命令行通讯录系统
```

本周每一天环环相扣，请按顺序学习，不要跳天。



## 常见错误与避坑

- ⚠️ 只看不练 — 必须动手敲代码
- ⚠️ 跳过基础直接调 API — 每天知识环环相扣
- ⚠️ 不写注释 — 企业级代码必须可读

## 课堂练习

- 📝 复习 Day 1 的核心知识点
- 📝 完成今日实操项目并提交 Git
- 📝 用 3 句话总结今天学到了什么


## 课程衔接说明



### ⬅️ 昨日回顾

这是课程第一天，欢迎开启大模型开发之旅！

### 🔗 今日定位

课程起点。为 Day 2 字符串处理与 Day 12 API 调用打基础。

### ➡️ 明日预告

**Day 2** 将学习「运算符与字符串」，今天务必打牢基础。


### 今日时间安排

| 时段 | 内容 |
|------|------|
| 09:00-12:00 上午 | 课程介绍、大模型行业全景与职业路径分析 |
| 09:00-12:00 上午 | 安装 Python 3.10+、VS Code、配置国内镜像源 |
| 09:00-12:00 上午 | 变量、数据类型(int/float/str/bool)、print 与 input |
| 14:00-17:30 下午 | 🛠️ 编写「个人信息卡片」程序 |
| 19:00-21:00 晚自习 | 配置 Git 与 GitHub 账号，学会提交代码 |



## 一、课程全景：为什么学这门课？



### 1. 大模型行业正在发生什么？

2023-2026 年，大模型从「实验室玩具」变成「生产力基础设施」:

| 趋势 | 具体表现 | 对开发者意味着什么 |
|------|----------|---------------------|
| API 普惠 | DeepSeek/Qwen 等低价 API | 零基础也能做出可用产品 |
| RAG 爆发 | 企业知识库问答成为标配 | 岗位需求最大的方向之一 |
| Agent 崛起 | 从聊天到自主执行任务 | 2025-2026 最热技能栈 |
| 低代码 + 代码并存 | Dify/Coze + LangChain | 懂代码的更有竞争力 |

### 2. 70 天你将获得什么？

> 毕业时你能独立开发:
> 1. 企业知识库问答系统（RAG）
> 2. 多 Agent 智能办公助手
> 3. 微调并部署自己的小模型
> 4. 一个内容充实的 GitHub 作品集


### 3. 职业路径参考

```
零基础 → Python 基础(14天) → Prompt 工程(10天) → RAG 开发(14天)
       → Agent 开发(12天) → 微调部署(10天) → 毕业设计+就业(13天)
```

岗位方向:
- **大模型应用开发工程师**（最匹配）
- AI 产品经理（技术理解力加分）
- 智能客服 / 知识库系统开发
- 独立开发者 / AI 创业


## 二、纳米级拆解：什么是「变量」？



### 1. 先用生活类比

变量就像一个**贴了标签的盒子**:
- 标签 = 变量名（如 `name`）
- 盒子里的东西 = 变量的值（如 `"张三"`）
- 你可以随时打开盒子，看看或换掉里面的东西

```python
name = "张三"      # 把字符串 "张三" 放进名为 name 的盒子
age = 25           # 把整数 25 放进名为 age 的盒子
is_student = True  # 把布尔值 True 放进名为 is_student 的盒子
```

### 2. 四大基本数据类型

| 类型 | Python 关键字 | 示例 | 用途 |
|------|--------------|------|------|
| 整数 | `int` | `42`, `-7`, `0` | 计数、年龄 |
| 浮点数 | `float` | `3.14`, `-0.5` | 价格、温度 |
| 字符串 | `str` | `"Hello"`, `'你好'` | 文本、Prompt |
| 布尔值 | `bool` | `True`, `False` | 条件判断 |

### 3. 类型查看与转换

```python
x = 42
print(type(x))        # <class 'int'>

# 类型转换（非常常用！）
age_str = "25"
age_int = int(age_str)    # str → int
price = 9.99
price_str = str(price)    # float → str
```

> **与大模型开发的联系**: API 返回的 JSON 中，所有值在解析前都是字符串。
> Day 5 你将深入学习 JSON，Day 12 你将解析 API 返回结果。
> 今天的类型转换是那一天的基础。


## 三、print 与 input：程序与用户的桥梁



### print — 输出

```python
print("Hello, World!")                    # 基础输出
print("姓名:", name, "年龄:", age)         # 多值输出
print(f"我叫{name}，今年{age}岁")       # f-string（Day 2 深入）
```

### input — 输入

```python
name = input("请输入你的名字: ")
# input 返回的永远是字符串！
# 如果期望数字，必须手动转换: int(input("请输入年龄: "))
```


## 四、下午实操：个人信息卡片



### 项目需求

编写一个命令行程序:
1. 提示用户输入姓名、年龄、城市、学习目标
2. 用 f-string 格式化输出一张精美的信息卡片
3. 将卡片保存到 `my_card.txt` 文件

### 完整参考代码

```python
# ================================
# 文件名: day01_personal_card.py
# 主题: Day 1 — 个人信息卡片
# 说明:
# 1. 使用变量存储个人信息
# 2. 练习 print / input / f-string
# 3. 为后续 Prompt 模板中的字符串格式化打基础
# ================================

def collect_user_info() -> dict:
    """交互式收集用户信息，返回字典（Day 5 将深入学习 dict）"""
    print("=" * 40)
    print("  欢迎使用「个人信息卡片」生成器")
    print("=" * 40)

    name = input("请输入你的姓名: ").strip()
    age_str = input("请输入你的年龄: ").strip()
    city = input("请输入你所在的城市: ").strip()
    goal = input("请输入你的学习目标: ").strip()

    # 类型转换：input 永远返回 str，年龄需要转为 int
    try:
        age = int(age_str)
    except ValueError:
        print("[警告] 年龄输入无效，已设为 0")
        age = 0

    return {
        "name": name,
        "age": age,
        "city": city,
        "goal": goal,
    }


def render_card(info: dict) -> str:
    """用 f-string 渲染个人信息卡片（Day 2 将深入 f-string）"""
    border = "─" * 36
    card = f"""
{border}
  📇 个人信息卡片
{border}
  姓名: {info['name']}
  年龄: {info['age']} 岁
  城市: {info['city']}
  学习目标: {info['goal']}
{border}
  生成时间: 由 Python 自动生成
{border}
"""
    return card


def main():
    info = collect_user_info()
    card_text = render_card(info)
    print(card_text)

    # 保存到文件（Day 11 将系统学习文件操作）
    output_file = "my_card.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(card_text)
    print(f"✅ 卡片已保存到 {output_file}")


if __name__ == "__main__":
    main()
```

### 运行方式

```bash
cd course/code/day01
python day01_personal_card.py
```


## 五、环境搭建完整指南



### Step 1: 安装 Python 3.10+

访问 https://www.python.org/downloads/ 下载安装包。

**Windows 注意**: 安装时勾选 ✅ `Add Python to PATH`

验证安装:

```bash
python --version
# 期望输出: Python 3.10.x 或更高
pip --version
```

### Step 2: 安装 VS Code

访问 https://code.visualstudio.com/ 下载安装。

推荐插件:
- Python (Microsoft)
- Pylance
- GitLens

### Step 3: 配置国内 pip 镜像源

```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### Step 4: 创建项目目录

```bash
mkdir llm-course-day01
cd llm-course-day01
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### Step 5: 运行第一个程序

创建 `hello.py`:

```python
print("Hello, LLM World!")
```

```bash
python hello.py
```



## 六、晚自习：Git 与 GitHub 入门



### 为什么程序员必须学 Git？

大模型应用开发全程需要版本管理:
- 每天的代码增量提交
- 毕业时 GitHub 主页是作品集核心
- 企业协作必备技能

### 安装 Git

- Windows: https://git-scm.com/download/win
- macOS: `xcode-select --install` 或 `brew install git`

### 基础命令（今晚自习掌握）

```bash
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"

# 初始化仓库
git init
git add .
git commit -m "Day 1: 个人信息卡片程序"

# 关联 GitHub 远程仓库
git remote add origin https://github.com/你的用户名/llm-course.git
git push -u origin main
```



## 七、知识自检清单



完成以下检查项，打 ✅ 表示掌握:

- [ ] 能独立安装 Python 3.10+ 并验证版本
- [ ] 能创建虚拟环境并激活
- [ ] 理解变量、int/float/str/bool 四种类型
- [ ] 能使用 print 和 input
- [ ] 能运行个人信息卡片程序
- [ ] 完成首次 git commit


## 八、课后作业



### 必做
1. 在个人信息卡片基础上，增加「爱好」和「编程经验」两个字段
2. 用 `type()` 打印每个变量的类型
3. 完成 Git 安装并提交 Day 1 代码到 GitHub

### 选做
1. 让程序支持多次输入（提示: 用 while 循环，Day 3 正式学习）
2. 了解 `black` 代码格式化工具: `pip install black && black day01_personal_card.py`



## 知识小测




**Q1.** 请用自己的话解释「Python 环境搭建」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 1-1 所学填写）
- 后续应用: 将在 Day 8 左右用到

</details>

**Q2.** 请用自己的话解释「变量与基本类型」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 1-1 所学填写）
- 后续应用: 将在 Day 8 左右用到

</details>

**Q3.** 请用自己的话解释「print/input」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 1-1 所学填写）
- 后续应用: 将在 Day 8 左右用到

</details>

**Q4.** 请用自己的话解释「Git 初识」是什么，并举一个与大模型开发相关的例子。

<details>
<summary>参考答案思路</summary>

- 定义: （学员填写）
- 例子: （结合 Day 1-1 所学填写）
- 后续应用: 将在 Day 8 左右用到

</details>


### 上机题

请不看课件，独立完成今日「实操项目」的核心功能。限时 60 分钟。



## 课后作业



### 必做

1. 完成今日实操项目「个人信息卡片程序」
2. 提交代码到 GitHub（commit message: `Day 1: 个人信息卡片程序`）
3. 在学习笔记中记录 3 个今天学到的新知识点

### 晚自习

- 配置 Git 与 GitHub 账号，学会提交代码

### 选做

1. 阅读官方文档中与今日主题相关的章节
2. 尝试优化今日代码（更优雅的错误处理、更清晰的注释）


——————

**第 1/70 天 · 零基础大模型应用开发 70 天培训课程**

> 坚持每一天，70 天后你将成为一名合格的大模型应用开发者。
