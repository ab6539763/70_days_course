# =============================================
# Day 10 · 下午演示代码:异常处理全家桶
# 文件:exception_demo.py
# =============================================
import json


# ---- 1. 基本形态:try 干活,except 救火 ----
def demo_basic():
    try:
        age = int("abc")                   # 抛 ValueError,下一行被跳过
        print("这行执行不到")
    except ValueError:
        print("请输入数字!")               # 出事时的补救
    print("程序继续活着")


# ---- 2. 多路捕获 + as e:拿到异常对象 ----
def load_config(filename: str) -> dict:
    """读取 JSON 配置:演示多路 except(像 elif,从上到下匹配)。"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"配置文件 {filename} 不存在,使用默认配置")
        return {}
    except json.JSONDecodeError as e:              # as e:异常对象带着案发详情
        print(f"配置文件格式坏了(第 {e.lineno} 行):{e.msg}")
        return {}


# ---- 3. 完整四件套:try 干活,except 救火,else 庆功,finally 打扫 ----
def demo_full(filename: str):
    try:
        f = open(filename, "r", encoding="utf-8")
    except FileNotFoundError:
        print("文件不存在")
    else:
        # else:try 没出事才执行——精确控制监控范围
        data = f.read()
        print(f"读到 {len(data)} 字符")
        f.close()
    finally:
        # finally:无论成败必然执行——打扫战场(关资源)
        print("清理完毕")


# ---- 4. 自定义异常家谱:用类型传递"该怎么办" ----
class APIError(Exception):
    """API 调用相关错误的基类。"""


class RateLimitError(APIError):
    """限流错误(可重试)。"""


class AuthError(APIError):
    """认证错误(重试也没用,查 Key)。"""


def call_api_mock(key: str) -> str:
    """模拟 API:演示抛出自定义异常。"""
    if not key.startswith("sk-"):
        raise AuthError(f"API Key 格式错误: {key[:6]}...")
    return "调用成功"


def demo_custom():
    # 分门别类地接:从具体到宽泛排列(elif 的"从严到宽"守则在异常上重演)
    try:
        call_api_mock("bad-key")
    except RateLimitError:
        print("被限流:等一等重试")
    except AuthError as e:
        print(f"认证失败:{e}(请检查 Key,重试无用)")
    except APIError as e:
        print(f"其他 API 错误:{e}")


# ---- 5. 裸 raise(原样上抛)与 raise ... from e(转译保因果) ----
def load_user(raw_json: str) -> dict:
    """异常链演示:底层异常转译成业务异常,from e 保留原始案发现场。"""
    try:
        return json.loads(raw_json)
    except json.JSONDecodeError as e:
        raise APIError("用户数据损坏") from e      # traceback 显示两层案情


# ---- 6. EAFP vs LBYL ----
def parse_age(text: str):
    """EAFP:先斩后奏——Python 社区推崇的风格。

    优势:① 覆盖完整(isdigit 拦不住 "1e5"、"²" 等怪输入,int 自己最清楚);
          ② 没有"检查和使用之间"的空窗。
    """
    try:
        return int(text)
    except ValueError:
        return None


# ---- 7. 军规二反面教材:吞异常(仅供认识,严禁模仿) ----
def demo_swallow_bad():
    try:
        1 / 0
    except Exception:
        pass            # ❌ 天下第一坏代码:出了任何事都装没看见


def demo_swallow_ok():
    """真需要兜底不崩时,最低要求:留下案底。"""
    try:
        1 / 0
    except Exception as e:
        print(f"[ERROR] 未预期的异常: {type(e).__name__}: {e}")


if __name__ == "__main__":
    demo_basic()
    load_config("不存在的文件.json")
    demo_full("不存在的文件.txt")
    demo_custom()

    try:
        load_user("{'bad': json}")
    except APIError as e:
        print(f"接到转译后的异常:{e}(原因:{e.__cause__})")   # __cause__:from e 存的原始异常

    print(parse_age("28"), parse_age("abc"), parse_age("1e5"))   # 28 None None
    demo_swallow_ok()
