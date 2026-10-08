"""Решение уравнений вида A*x^2 + B*x + C = 0."""

import math

MAX_VALUE = 10000


def check_coefficients(coefficients):
    """Проверяет коэффициенты на допустимость."""
    for name, value in coefficients.items():
        if abs(value) > MAX_VALUE:
            raise ValueError(
                f"коэффициент {name} вне допустимого диапазона"
            )


def solve(a, b, c):
    """Решает уравнение A*x^2 + B*x + C = 0.

    Возвращает кортеж (kind, d, roots).
    """
    if a == 0:
        if b == 0:
            raise ValueError("это не уравнение, неизвестное отсутствует")
        return "линейное", None, [-c / b]

    d = b * b - 4 * a * c
    if d > 0:
        x1 = (-b + math.sqrt(d)) / (2 * a)
        x2 = (-b - math.sqrt(d)) / (2 * a)
        return "квадратное", d, [x1, x2]
    elif d == 0:
        x = -b / (2 * a)
        return "квадратное", d, [x]
    else:
        return "квадратное", d, []