"""Численное интегрирование методом левых прямоугольников."""

import math

MAX_STEPS = 100000


def f_ratio(x):
    """F(x) = x / (x + 1)."""
    return x / (x + 1)


def f_root(x):
    """F(x) = sqrt(x^2 + 1)."""
    return math.sqrt(x * x + 1)


FUNCTIONS = {
    "ratio": (f_ratio, "F(x) = x / (x + 1)", 0, 20, False),
    "root":  (f_root,  "F(x) = sqrt(x^2 + 1)", -5, 5, True),
}


def validate_bounds(func_name, a, b):
    """Проверяет пределы интегрирования."""
    if not (math.isfinite(a) and math.isfinite(b)):
        raise ValueError("пределы должны быть конечными числами")
    if a >= b:
        raise ValueError("начальный предел должен быть меньше конечного")

    _, _, low, high, strict = FUNCTIONS[func_name]
    if strict:
        if a <= low or a >= high or b <= low or b >= high:
            raise ValueError("предел вне промежутка")
    else:
        if a < low or a > high or b < low or b > high:
            raise ValueError("предел вне промежутка")


def validate_steps(steps):
    """Проверяет количество шагов."""
    if not (1 <= steps <= MAX_STEPS):
        raise ValueError("количество шагов вне диапазона")


def integrate(func, a, b, steps):
    """Интеграл методом левых прямоугольников."""
    dx = (b - a) / steps
    result = 0
    for i in range(steps):
        x = a + i * dx
        result += func(x) * dx
    return result