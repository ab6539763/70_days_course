# =============================================
# Day 11 作业 · 编程题 2:日志分析器
# 考点:逐行处理、正则提取(分组)、计数器、集合去重
# =============================================
import re

LOG = """2026-07-16 10:01:22 INFO 用户登录成功 ip=192.168.1.5
2026-07-16 10:03:45 WARN 响应超时 ip=10.0.0.12 耗时=3.2s
2026-07-16 10:05:01 ERROR 数据库连接失败 ip=192.168.1.5
2026-07-16 10:06:33 INFO 用户查询订单 ip=172.16.0.3
2026-07-16 10:08:19 ERROR API限流 ip=10.0.0.12"""

# ① 级别计数:字典计数器
level_counter: dict = {}
# ② ERROR 详情收集
errors: list = []
# ③ IP 收集:集合去重
ips: set = set()

# 每行的通用模式:日期 时间 级别 消息
# 分组:(时间部分)(级别)(其余消息)——模式旁写人话是纪律
LINE_PATTERN = r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+) (.+)$"
IP_PATTERN = r"ip=(\d+\.\d+\.\d+\.\d+)"          # \. 转义:匹配字面的点

for line in LOG.split("\n"):
    m = re.match(LINE_PATTERN, line.strip())
    if not m:                                     # 匹配不上的行:跳过(容错)
        continue
    timestamp, level, message = m.group(1), m.group(2), m.group(3)

    level_counter[level] = level_counter.get(level, 0) + 1

    if level == "ERROR":
        errors.append(f"{timestamp}{message}")

    ip_match = re.search(IP_PATTERN, message)
    if ip_match:                                  # search 可能 None:先判再用
        ips.add(ip_match.group(1))

print("级别统计:", level_counter)
print("ERROR 详情:")
for e in errors:
    print(f"  {e}")
print("出现过的 IP:", sorted(ips))

assert level_counter == {"INFO": 2, "WARN": 1, "ERROR": 2}
assert len(ips) == 3
print("✓ 日志分析器测试通过")
