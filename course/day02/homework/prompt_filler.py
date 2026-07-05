# =============================================
# Day 02 作业 · 编程题 3:Prompt 模板填充器
# 考点:replace 链式替换;理解"模板先存后填"与 f-string 的区别
# 伏笔:这就是 Day 25 LangChain PromptTemplate 的手工版
# =============================================

# 模板是普通字符串:{role} 等只是普通字符,没有 f 前缀就不会被立即求值。
# 这正是模板的价值:可以存在文件/数据库里,运行时才决定填什么
template = "你是一名{role}。请用{tone}的语气,回答用户关于{topic}的问题,回答不超过{limit}字。"

# 收集四个填充值(顺手清洗)
role = input("角色(如:资深法律顾问):").strip()
tone = input("语气(如:严谨专业):").strip()
topic = input("主题(如:劳动合同):").strip()
limit = input("字数上限(如:200):").strip()

# 链式 replace:每次替换返回新串,接力传递
prompt = (template
          .replace("{role}", role)
          .replace("{tone}", tone)
          .replace("{topic}", topic)
          .replace("{limit}", limit))
# (括号包住整个表达式后可以换行书写,长链式调用的规范排版)

print("-" * 40)
print("生成的 Prompt:")
print(prompt)
