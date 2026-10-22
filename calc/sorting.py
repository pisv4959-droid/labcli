# Модуль сортировок. Изменяют переданный список, возвращают None.

from calc.arrays import MIN_VALUE, MAX_VALUE


# Проверяет, нужно ли менять элементы местами (в зависимости от направления).
def is_out_of_order(a, b, descending):
    if descending:
        return a < b
    return a > b


# Сортировка пузырьком (Bubble sort).
def bubble_sort(array, descending=False):
    n = len(array)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if is_out_of_order(array[j], array[j + 1], descending):
                array[j], array[j + 1] = array[j + 1], array[j]
                swapped = True
        if not swapped:
            break


# Сортировка выбором (Selection sort).
def selection_sort(array, descending=False):
    n = len(array)
    for i in range(n - 1):
        best = i
        for j in range(i + 1, n):
            if is_out_of_order(array[best], array[j], descending):
                best = j
        array[i], array[best] = array[best], array[i]


# Сортировка вставками (Insertion sort).
def insertion_sort(array, descending=False):
    n = len(array)
    for i in range(1, n):
        current = array[i]
        j = i
        while j > 0 and is_out_of_order(array[j - 1], current, descending):
            array[j] = array[j - 1]
            j -= 1
        array[j] = current


# Сортировка подсчётом (Counting sort).
def counting_sort(array, descending=False):
    counters = [0] * (MAX_VALUE - MIN_VALUE + 1)
    for val in array:
        counters[val - MIN_VALUE] += 1

    k = 0
    indices = range(len(counters))
    if descending:
        indices = reversed(indices)

    for idx in indices:
        for _ in range(counters[idx]):
            array[k] = idx + MIN_VALUE
            k += 1


METHODS = {
    "bubble": bubble_sort,
    "selection": selection_sort,
    "insertion": insertion_sort,
    "counting": counting_sort,
}