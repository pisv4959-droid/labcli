"""Точка входа приложения mathtool.

mathtool — расчёты над уравнениями и числовыми последовательностями.
"""

import os
import sys

# Коррекция пути: позволяет запускать файл из любого каталога.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cli import build_parser
from calc import equation, stats, series, integration


def handle_solve(args):
    """Обработчик команды solve."""
    if args.a is None and args.b is None and args.c is None:
        try:
            a = int(input("Введите A: "))
            b = int(input("Введите B: "))
            c = int(input("Введите C: "))
        except EOFError:
            raise ValueError("не удалось прочитать коэффициенты")
    elif args.a is not None and args.b is not None and args.c is not None:
        a, b, c = args.a, args.b, args.c
    else:
        raise ValueError("укажите все три коэффициента либо ни одного")

    equation.check_coefficients({"A": a, "B": b, "C": c})
    kind, d, roots = equation.solve(a, b, c)

    if kind == "квадратное":
        print("Уравнение квадратное")
        print(f"D = {d}")
    else:
        print("Уравнение линейное")

    if len(roots) == 0:
        print("Действительных корней нет")
    elif len(roots) == 1:
        print(f"x = {roots[0]:.3f}")
    else:
        print(f"x1 = {roots[0]:.3f}")
        print(f"x2 = {roots[1]:.3f}")

    return 0


def handle_stats(args):
    """Обработчик команды stats."""
    if args.input:
        with open(args.input, encoding="utf-8-sig") as handle:
            source = handle.readlines()
    else:
        source = sys.stdin.readlines()

    values = []
    for line in source:
        for word in line.split():
            try:
                values.append(float(word))
            except ValueError:
                raise ValueError(f"{word} не является числом")

    stats.validate(values)

    report = [
        ("Количество",     len(values),                  "d"),
        ("Сумма",          stats.total(values),          ".3f"),
        ("Ср. арифм.",     stats.mean(values),           ".3f"),
        ("Сумма кв.",      stats.sum_of_squares(values), ".3f"),
        ("Ср. кв.",        stats.rms(values),            ".3f"),
        ("Дисперсия",      stats.variance(values),       ".3f"),
        ("СКО",            stats.std_dev(values),        ".3f"),
        ("Станд. откл.",   stats.std_dev_sample(values), ".3f"),
        ("Наименьшее",     stats.minimum(values),        ".3f"),
        ("Наибольшее",     stats.maximum(values),        ".3f"),
        ("Положительных",  stats.count_positive(values), "d"),
        ("Отрицательных",  stats.count_negative(values), "d"),
    ]

    for label, value, form in report:
        if value is None:
            print(f"{label}: НЕ СУЩЕСТВУЕТ")
        else:
            print(f"{label}: {value:{form}}")

    return 0


def handle_series(args):
    """Обработчик команды series."""
    term, formula = series.FORMULAS[args.func]

    if args.terms is not None:
        series.validate_terms(args.terms)
    else:
        series.validate_eps(args.eps)

    if args.terms is not None:
        result, count = series.sum_by_count(term, args.terms)
    else:
        result, count = series.sum_by_eps(term, args.eps)

    print(formula)
    print(f"Слагаемых: {count}")
    print(f"Сумма ряда: {result:.{series.DIGITS}f}")

    return 0


def handle_integrate(args):
    """Обработчик команды integrate."""
    func, formula, _, _, _ = integration.FUNCTIONS[args.func]

    integration.validate_bounds(args.func, args.start, args.to)
    integration.validate_steps(args.steps)

    result = integration.integrate(func, args.start, args.to, args.steps)

    print(formula)
    print(f"Значение интеграла: {result:.4f}")

    return 0


HANDLERS = {
    "solve": handle_solve,
    "stats": handle_stats,
    "series": handle_series,
    "integrate": handle_integrate,
}


def main(argv):
    """Точка входа. Возвращает код завершения."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    try:
        return HANDLERS[args.command](args)
    except (ValueError, OSError) as error:
        print(f"ОШИБКА: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))