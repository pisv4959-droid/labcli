"""
main — приложение работы №1.
Решение уравнений вида A*x^2 + B*x + C = 0.

Сохраняется без изменений как исходный вариант первой работы.
Актуальная версия приложения — mathtool.py.
"""

import sys
import math

MAX_VALUE = 10000


def print_help():
    print("mathtool — решение уравнений вида A*x^2 + B*x + C = 0")
    print()
    print("Использование:")
    print("    python mathtool.py                         вывод справки")
    print("    python mathtool.py --help                  вывод справки")
    print("    python mathtool.py solve                   ввод коэффициентов с клавиатуры")
    print("    python mathtool.py solve -a 1 -b -3 -c 2   решение с заданными коэффициентами")
    print()
    print("Коэффициенты A, B, C — целые числа, по модулю не превышающие 10000.")


def parse_args(argv):
    args = argv[1:]

    if len(args) == 0 or args[0] == "--help":
        print_help()
        sys.exit(0)

    if args[0] != "solve":
        print("ОШИБКА: неизвестная команда", file=sys.stderr)
        sys.exit(1)

    if len(args) == 1:
        try:
            a = input("Введите A: ")
            b = input("Введите B: ")
            c = input("Введите C: ")
        except EOFError:
            print("ОШИБКА: не удалось прочитать коэффициенты", file=sys.stderr)
            sys.exit(1)
        return a, b, c

    if len(args) == 7:
        if args[1] != "-a" or args[3] != "-b" or args[5] != "-c":
            print("ОШИБКА: неизвестный параметр", file=sys.stderr)
            sys.exit(1)
        return args[2], args[4], args[6]

    print("ОШИБКА: неверный набор параметров", file=sys.stderr)
    sys.exit(1)


def to_int(value):
    try:
        return int(value)
    except ValueError:
        print("ОШИБКА: коэффициент не является целым числом", file=sys.stderr)
        sys.exit(1)


def check_range(*values):
    for v in values:
        if abs(v) > MAX_VALUE:
            print("ОШИБКА: значение вне допустимого диапазона", file=sys.stderr)
            sys.exit(1)


def solve_quadratic(a, b, c):
    print("Уравнение квадратное")
    d = b * b - 4 * a * c
    print(f"D = {d}")

    if d > 0:
        x1 = (-b + math.sqrt(d)) / (2 * a)
        x2 = (-b - math.sqrt(d)) / (2 * a)
        print(f"x1 = {x1:.3f}")
        print(f"x2 = {x2:.3f}")
    elif d == 0:
        x = -b / (2 * a)
        print(f"x = {x:.3f}")
    else:
        print("Действительных корней нет")


def solve_linear(b, c):
    print("Уравнение линейное")
    x = -c / b
    print(f"x = {x:.3f}")


def solve(a, b, c):
    if a == 0:
        if b != 0:
            solve_linear(b, c)
        else:
            print("ОШИБКА: это не уравнение, неизвестное отсутствует", file=sys.stderr)
            sys.exit(1)
    else:
        solve_quadratic(a, b, c)


def main():
    a_str, b_str, c_str = parse_args(sys.argv)
    a = to_int(a_str)
    b = to_int(b_str)
    c = to_int(c_str)
    check_range(a, b, c)
    solve(a, b, c)
    sys.exit(0)


if __name__ == "__main__":
    main()