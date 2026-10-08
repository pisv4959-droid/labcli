"""Суммы знакочередующихся рядов."""

import math

MAX_TERMS = 10000
MAX_EPS = 0.0001
MAX_ITERATIONS = 100000
DIGITS = math.ceil(-math.log10(MAX_EPS))


def sign(n):
    """Знак слагаемого с номером n."""
    return -1 if n % 2 == 0 else 1


def term_third(n):
    """Слагаемое ряда third."""
    return sign(n) / (3 * n)


def term_sqplus(n):
    """Слагаемое ряда sqplus."""
    return sign(n) / (n * n + 1)


FORMULAS = {
    "third":  (term_third,  "S = 1/3 - 1/6 + 1/9 - 1/12 + ..."),
    "sqplus": (term_sqplus, "S = 1/(1^2+1) - 1/(2^2+1) + 1/(3^2+1) - ..."),
}


def validate_terms(terms):
    """Проверяет количество слагаемых."""
    if not (1 <= terms <= MAX_TERMS):
        raise ValueError("количество слагаемых вне диапазона")


def validate_eps(eps):
    """Проверяет точность."""
    if not (math.isfinite(eps) and 0 < eps <= MAX_EPS):
        raise ValueError("точность вне диапазона")


def sum_by_count(term, count):
    """Сумма ряда по количеству слагаемых."""
    result = 0
    for n in range(1, count + 1):
        result += term(n)
    return result, count


def sum_by_eps(term, eps):
    """Сумма ряда по достигнутой точности."""
    result = 0
    n = 0
    while True:
        n += 1
        value = term(n)
        result += value
        if abs(value) < eps:
            return result, n
        if n >= MAX_ITERATIONS:
            raise ValueError("точность не достигнута")