"""Разбор параметров командной строки."""

import argparse

from calc import series, integration


def build_parser():
    """Создаёт и возвращает разборщик параметров."""
    parser = argparse.ArgumentParser(
        prog="mathtool",
        description="mathtool — расчёты над уравнениями "
                    "и числовыми последовательностями",
        allow_abbrev=False,
    )

    subparsers = parser.add_subparsers(dest="command")

    # --- solve ---
    p_solve = subparsers.add_parser(
        "solve",
        help="решение уравнения вида A*x^2 + B*x + C = 0",
        allow_abbrev=False,
    )
    p_solve.add_argument("-a", type=int, help="коэффициент A")
    p_solve.add_argument("-b", type=int, help="коэффициент B")
    p_solve.add_argument("-c", type=int, help="коэффициент C")

    # --- stats ---
    p_stats = subparsers.add_parser(
        "stats",
        help="показатели последовательности",
        allow_abbrev=False,
    )
    p_stats.add_argument("--input", help="имя файла с числами")

    # --- series ---
    p_series = subparsers.add_parser(
        "series",
        help="сумма ряда",
        allow_abbrev=False,
    )
    p_series.add_argument(
        "--func",
        required=True,
        choices=sorted(series.FORMULAS),
        help="какой ряд суммировать",
    )
    group = p_series.add_mutually_exclusive_group(required=True)
    group.add_argument("--terms", type=int, help="количество слагаемых")
    group.add_argument("--eps", type=float, help="точность")

    # --- integrate ---
    p_integrate = subparsers.add_parser(
        "integrate",
        help="численное интегрирование",
        allow_abbrev=False,
    )
    p_integrate.add_argument(
        "--func",
        required=True,
        choices=sorted(integration.FUNCTIONS),
        help="какую функцию интегрировать",
    )
    p_integrate.add_argument(
        "--from",
        dest="start",
        type=float,
        required=True,
        help="нижний предел интегрирования",
    )
    p_integrate.add_argument(
        "--to",
        type=float,
        required=True,
        help="верхний предел интегрирования",
    )
    p_integrate.add_argument(
        "--steps",
        type=int,
        required=True,
        help="количество шагов",
    )

    return parser