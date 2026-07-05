# Day 01 晚自习补充:Git / GitHub 详细配置手册

> 本手册配合课件"晚自习"一节使用,覆盖从零注册到成功推送的每一步,以及最常见的三个卡点。

## 一、安装 Git

| 系统 | 步骤 |
|------|------|
| Windows | 访问 https://git-scm.com/downloads 下载 `.exe`,安装时**全部保持默认选项**一路下一步 |
| macOS | 终端输入 `git --version`,未安装时系统会自动弹出"安装命令行开发者工具"的引导,点安装即可 |

验证:终端执行 `git --version`,输出 `git version 2.x.x` 即成功。

## 二、一次性全局配置(自报家门)

Git 要求每一次提交都带上"记账人"签名。以下两条命令只需执行一次:

```bash
git config --global user.name "zhangsan"
git config --global user.email "zhangsan@example.com"
```

- 邮箱建议与 GitHub 注册邮箱一致,这样 GitHub 才能把提交计入你的贡献日历(绿格子);
- 验证:`git config --global --list` 应能看到刚才两项。

## 三、注册 GitHub 与创建仓库

1. 访问 https://github.com/ → Sign up,用常用邮箱注册;
2. 用户名建议"名字拼音 + dev/ai"(如 `zhangsan-dev`),它会出现在你的简历里;
3. 登录后右上角 `+` → `New repository`:
   - Repository name:`llm-course-70days`
   - Description:`我的 70 天大模型应用开发学习记录`
   - 可见性:**Public**(公开)
   - 勾选 `Add a README file`
4. 点击 `Create repository`。

## 四、克隆仓库到本地

```bash
# 切换到想存放代码的目录(示例;macOS 可用 cd ~/)
cd D:\

# 从仓库页面绿色 Code 按钮复制 HTTPS 地址
git clone https://github.com/你的用户名/llm-course-70days.git
```

完成后用 VS Code 打开 `llm-course-70days` 文件夹,今后所有课程代码都写在这里。

## 五、每日提交三连(务必背下来)

```bash
git status                                    # ① 看看改了什么(红色 = 未暂存)
git add day01/                                # ② 把改动放上"打包台"(暂存区)
git commit -m "Day01: 完成环境搭建与信息卡片程序"  # ③ 盖章记账
git push                                      # ④ 推送到 GitHub
```

提交信息(-m 后面的文字)规范:
- 以 `DayXX:` 开头,方便日后按天检索;
- 用动词说清做了什么:"完成 xx"、"修复 xx"、"新增 xx";
- 不要写"更新"、"改了点东西"这种废话。

## 六、三个最常见的卡点

### 卡点 1:`git push` 报 `Authentication failed`

GitHub 自 2021 年 8 月起不再接受账号密码推送。解决方式二选一:

**方式 A(推荐):浏览器授权。** 首次 push 时会弹出 "Sign in with your browser",点击后在浏览器完成登录授权即可,凭据会被 Git Credential Manager 记住。

**方式 B:Personal Access Token(PAT)。**
1. GitHub → 右上角头像 → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token (classic);
2. 勾选 `repo` 权限,有效期建议 90 天,生成后**立即复制保存**(只显示一次);
3. push 时用户名照常填,密码位置粘贴这串 token。

### 卡点 2:`git push` 报 `rejected ... fetch first`

原因:云端仓库有本地没有的提交(比如你创建仓库时勾选的 README)。
解决:先拉取再推送:

```bash
git pull origin main
git push
```

### 卡点 3:中文文件名在 `git status` 里显示成 `\346\226\207...` 乱码

这不是错误,只是显示编码问题。执行一次:

```bash
git config --global core.quotepath false
```

## 七、自检

- [ ] `git --version` 有输出
- [ ] `git config --global --list` 能看到 user.name 和 user.email
- [ ] GitHub 仓库 `llm-course-70days` 已创建且为 Public
- [ ] 本地能看到克隆下来的文件夹
- [ ] 今天的 day01 代码已 push,GitHub 页面能看到,贡献日历出现绿格子
