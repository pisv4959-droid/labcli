# Модуль для работы с массивами: константы, генерация, поиск.

import random

MIN_VALUE = -100
MAX_VALUE = 100
MAX_COUNT = 1_000_000
MAX_SEARCH = 1000


# Генерирует список случайных чисел.
def generate_array(count, low=MIN_VALUE, high=MAX_VALUE, seed=None):
    random.seed(seed)
    return [random.randint(low, high) for _ in range(count)]


# Проверяет количество и диапазон значений.
def validate_array(values):
    if not (1 <= len(values) <= MAX_COUNT):
        raise ValueError(f"количество элементов вне диапазона 1..{MAX_COUNT}")
    for val in values:
        if not (MIN_VALUE <= val <= MAX_VALUE):
            raise ValueError(f"значение {val} вне диапазона {MIN_VALUE}..{MAX_VALUE}")


# Двоичный поиск. Возвращает индекс или None.
def binary_search(array, target):
    left = 0
    right = len(array) - 1
    while left <= right:
        mid = (left + right) // 2
        if array[mid] == target:
            return mid
        if array[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return None