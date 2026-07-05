# Day 10 作业 · 编程题 4:venv 实操报告(参考范例)

> 请在自己电脑上实际操作后,用自己的命令输出替换以下内容。

## 操作记录

```bash
# ① 在项目根目录创建虚拟环境
cd week2_project
python -m venv .venv

# ② 激活(Windows PowerShell)
.venv\Scripts\Activate.ps1
# 提示符变为:(.venv) PS D:\llm-course-70days\week2_project>

# macOS/Linux 则是:
# source .venv/bin/activate

# ③ 确认在对的房间
pip -V
# pip 24.x from D:\llm-course-70days\week2_project\.venv\Lib\site-packages\pip

# ④ 安装 requests(为 Day 12 预热)
pip install requests
# Successfully installed certifi-... charset-normalizer-... idna-... requests-2.32.x urllib3-...

# ⑤ 导出依赖清单
pip freeze > requirements.txt
# 文件内容(五行):requests 及其四个依赖,各带精确版本号

# ⑥ 退出房间
deactivate

# ⑦ 重新激活,验证 requests 还在
.venv\Scripts\Activate.ps1
python -c "import requests; print(requests.__version__)"
# 2.32.x
```

## 问题回答:为什么 requirements.txt 进 Git 而 .venv 不进?

- requirements.txt 是**清单**:几行文本,记录"需要什么"(库名 + 版本);
- .venv 是**货物**:几百 MB 的实际文件,是清单的执行结果,且与操作系统/路径绑定,不可移植;
- 任何人拿到清单,`pip install -r requirements.txt` 一条命令即可在自己机器重建货物。

这是"可再生的不进 Git"原则的最典型案例(同族:__pycache__、构建产物;反例:源代码、配置模板必须进)。
