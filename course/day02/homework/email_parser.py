# =============================================
# Day 02 作业 · 编程题 2:邮箱信息提取器
# 考点:split 拆分、索引取元素、字符串比较前先 lower、切片脱敏
# =============================================

COMPANY_DOMAIN = "deepseek.com"        # 公司域名做成常量,换公司只改这里

email = input("请输入邮箱地址:").strip()    # 进系统先清洗,养成条件反射

# split("@") 把邮箱一刀两断,得到 [用户名, 域名] 两段
parts = email.split("@")
username = parts[0]
domain = parts[1]
# 追问:如果用户输入里没有 @,parts[1] 会抛 IndexError——
# 优雅的处理需要明天的 if 判断,后天作业里回收这个坑

# 判断是否公司邮箱:比较前统一小写,避免 DeepSeek.COM 漏判
is_company = domain.lower() == COMPANY_DOMAIN

# 脱敏:用户名首字符 + *** + @ + 域名
masked = username[0] + "***@" + domain

print(f"用户名:{username}")
print(f"域名:{domain}")
print(f"公司邮箱:{is_company}")
print(f"脱敏显示:{masked}")
