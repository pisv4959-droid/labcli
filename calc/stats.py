"""Показатели последовательности."""

import math

MAX_COUNT = 20
MAX_ABS = 10000


def validate(values):
    """Проверяет список чисел на допустимость."""
    if len(values) == 0:
        raise ValueError("последовательность пуста")
    if len(values) > MAX_COUNT:
        raise ValueError("количество чисел превышает 20")
    for v in values:
        if not math.isfinite(v):
            raise ValueError("значение не является конечным числом")
        if abs(v) > MAX_ABS:
            raise ValueError("значение вне допустимого диапазона")


def total(values):
    """Сумма чисел."""
    result = 0
    for v in values:
        result += v
    return result


def mean(values):
    """Среднее арифметическое."""
    return total(values) / len(values)


def sum_of_squares(values):
    """Сумма квадратов."""
    result = 0
    for v in values:
        result += v ** 2
    return result


def rms(values):
    """Среднее квадратическое."""
    return math.sqrt(sum_of_squares(values) / len(values))


def _sum_squared_deviations(values):
    """Сумма квадратов отклонений от среднего."""
    m = mean(values)
    result = 0
    for v in values:
        result += (v - m) ** 2
    return result


def variance(values):
    """Дисперсия."""
    return _sum_squared_deviations(values) / len(values)


def std_dev(values):
    """СКО."""
    return math.sqrt(variance(values))


def std_dev_sample(values):
    """Стандартное отклонение."""
    n = len(values)
    if n < 2:
        return None
    return math.sqrt(_sum_squared_deviations(values) / (n - 1))


def minimum(values):
    """Наименьшее значение."""
    result = values[0]
    for v in values:
        if v < result:
            result = v
    return result


def maximum(values):
    """Наибольшее значение."""
    result = values[0]
    for v in values:
        if v > result:
            result = v
    return result


def count_positive(values):
    """Количество положительных чисел."""
    result = 0
    for v in values:
        if v > 0:
            result += 1
    return result


def count_negative(values):
    """Количество отрицательных чисел."""
    result = 0
    for v in values:
        if v < 0:
            result += 1
    return result