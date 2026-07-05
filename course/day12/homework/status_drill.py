# =============================================
# Day 12 作业 · 编程题 3:状态码分诊演习(不花钱)
# 考点:字典驱动的分诊表(注册表模式又一战)、httpbin 演练场
# =============================================
import requests

# 分诊表:状态码 → (诊断, 处置)。字典驱动,加新状态码只改这里
TRIAGE = {
    200: ("正常", "解析响应继续业务"),
    401: ("认证失败", "检查 API Key(重试无用)"),
    429: ("限流", "等待 3-5 秒后重试(指数退避更佳)"),
    500: ("服务器错误", "稍后重试"),
    503: ("服务过载", "稍后重试"),
}


def drill(code: int) -> None:
    """向 httpbin 请求指定状态码并按分诊表处置。"""
    try:
        resp = requests.get(f"https://httpbin.org/status/{code}", timeout=10)
    except requests.RequestException as e:            # 网络层问题统一兜底
        print(f"  {code}: 请求失败({type(e).__name__})")
        return

    verdict, action = TRIAGE.get(resp.status_code, ("未知状态", "查文档"))
    print(f"  {resp.status_code}: {verdict:<8}{action}")


if __name__ == "__main__":
    print("状态码分诊演习:")
    for code in [200, 401, 429, 500, 503]:
        drill(code)
