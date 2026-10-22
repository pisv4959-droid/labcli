# Разбор параметров командной строки.

import argparse
from calc import series, integration, sorting, arrays


def build_parser():
    parser = argparse.ArgumentParser(
        prog="mathtool",
        description="mathtool — расчёты над уравнениями и числовыми последовательностями",
        allow_abbrev=False,
    )
    subparsers = parser.add_subparsers(dest="command")

    # --- solve ---
    p_solve = subparsers.add_parser("solve", help="решение уравнения", allow_abbrev=False)
    p_solve.add_argument("-a", type=int, help="коэффициент A")
    p_solve.add_argument("-b", type=int, help="коэффициент B")
    p_solve.add_argument("-c", type=int, help="коэффициент C")

    # --- stats ---
    p_stats = subparsers.add_parser("stats", help="показатели последовательности", allow_abbrev=False)
    p_stats.add_argument("--input", help="имя файла с числами")

    # --- series ---
    p_series = subparsers.add_parser("series", help="сумма ряда", allow_abbrev=False)
    p_series.add_argument("--func", required=True, choices=sorted(series.FORMULAS), help="какой ряд суммировать")
    group = p_series.add_mutually_exclusive_group(required=True)
    group.add_argument("--terms", type=int, help="количество слагаемых")
    group.add_argument("--eps", type=float, help="точность")

    # --- integrate ---
    p_integrate = subparsers.add_parser("integrate", help="численное интегрирование", allow_abbrev=False)
    p_integrate.add_argument("--func", required=True, choices=sorted(integration.FUNCTIONS), help="какую функцию интегрировать")
    p_integrate.add_argument("--from", dest="start", type=float, required=True, help="нижний предел")
    p_integrate.add_argument("--to", type=float, required=True, help="верхний предел")
    p_integrate.add_argument("--steps", type=int, required=True, help="количество шагов")

    # --- fill ---
    p_fill = subparsers.add_parser("fill", help="генерация массива", allow_abbrev=False)
    p_fill.add_argument("-c", "--count", type=int, required=True, help="количество элементов")
    p_fill.add_argument("--min", type=int, default=arrays.MIN_VALUE, help="минимум")
    p_fill.add_argument("--max", type=int, default=arrays.MAX_VALUE, help="максимум")
    p_fill.add_argument("--seed", type=int, help="начальное значение генератора")
    p_fill.add_argument("-o", "--output", help="файл для сохранения")

    # --- sort ---
    p_sort = subparsers.add_parser("sort", help="сортировка массива", allow_abbrev=False)
    p_sort.add_argument("-m", "--method", required=True, choices=sorted(sorting.METHODS), help="метод сортировки")
    p_sort.add_argument("--order", choices=["asc", "desc"], default="asc", help="направление")
    p_sort.add_argument("-i", "--input", help="файл с массивом")
    p_sort.add_argument("-o", "--output", help="файл для результата")

    # --- search ---
    p_search = subparsers.add_parser("search", help="двоичный поиск", allow_abbrev=False)
    p_search.add_argument("-v", "--value", type=int, required=True, help="искомое число")
    p_search.add_argument("-i", "--input", help="файл с массивом")

    return parser