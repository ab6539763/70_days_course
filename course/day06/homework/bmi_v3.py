# =============================================
# Day 06 作业 · 编程题 1:BMI 3.0(函数化重构)
# 对比 Day 03 版:两段校验循环 → 一个函数调两次(DRY 落地)
# =============================================

def read_positive_float(prompt: str) -> float:
    """读取一个正的小数,不合法就重问,保证返回合法值。"""
    while True:
        text = input(prompt).strip()
        # 删掉第一个小数点后全是数字,且值为正 → 合法
        if text.replace(".", "", 1).isdigit() and float(text) > 0:
            return float(text)                   # return 兼职 break
        print("请输入正数!")


def bmi_level(bmi: float) -> str:
    """BMI 分级:纯函数,只 return 不 print,可独立测试。"""
    if bmi >= 28:
        return "肥胖"
    if bmi >= 24:
        return "偏胖"
    if bmi >= 18.5:
        return "正常"
    return "偏瘦"


def main() -> None:
    """主流程:输入 → 计算 → 输出。"""
    weight = read_positive_float("体重(公斤):")
    height = read_positive_float("身高(米,如 1.75):")
    bmi = weight / (height ** 2)                 # 幂运算替代 height*height
    print(f"BMI = {bmi:.1f},分级:{bmi_level(bmi)}")

    # 纯函数的红利:一行 assert 就是一个测试
    assert bmi_level(22.0) == "正常"
    assert bmi_level(28.0) == "肥胖"


if __name__ == "__main__":
    main()
