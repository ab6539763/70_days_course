"""Day 3: 猜数字游戏"""
import random

def guess_number_game():
    target = random.randint(1, 100)
    attempts = 0
    print("🎮 猜数字游戏！范围 1-100")

    while True:
        guess_str = input("请输入你的猜测: ")
        try:
            guess = int(guess_str)
        except ValueError:
            print("请输入有效整数！")
            continue

        attempts += 1
        if guess < target:
            print("太小了！")
        elif guess > target:
            print("太大了！")
        else:
            print(f"🎉 恭喜！用了 {attempts} 次猜对了！")
            break


def multiplication_table():
    for i in range(1, 10):
        row = "  ".join(f"{i}×{j}={i*j:2d}" for j in range(1, i + 1))
        print(row)


if __name__ == "__main__":
    guess_number_game()
