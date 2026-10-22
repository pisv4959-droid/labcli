# Точка входа приложения mathtool.

import os
import sys
import time

# Коррекция пути: позволяет запускать файл из любого каталога.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cli import build_parser
from calc import equation, stats, series, integration, arrays, sorting
from calc.arrays import MIN_VALUE, MAX_VALUE


# Измеряет время выполнения операции и выводит в stderr.
def measure_time(name, operation, *params):
    start = time.perf_counter()
    result = operation(*params)
    elapsed = time.perf_counter() - start
    print(f"Время операции {name}: {elapsed:.6f} с", file=sys.stderr)
    return result


# Чтение массива из файла или с клавиатуры.
def read_array(path):
    if path:
        with open(path, encoding="utf-8-sig") as handle:
            text = handle.read()
    else:
        lines = []
        while True:
            try:
                line = input("Введите элементы (пустая строка — конец): ")
                if not line.strip():
                    break
                lines.append(line)
            except EOFError:
                break
        text = " ".join(lines)

    text = text.replace(",", " ")
    words = text.split()
    
    try:
        values = [int(w) for w in words]
    except ValueError:
        raise ValueError("элемент массива не является целым числом")
        
    arrays.validate_array(values)
    return values


# Запись массива в файл или на экран.
def write_array(path, values):
    result_str = " ".join(str(x) for x in values)
    if path:
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(result_str + "\n")
        print(f"Записано элементов: {len(values)} в файл {path}")
    else:
        print(result_str)


def handle_solve(args):
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
        ("Количество", len(values), "d"),
        ("Сумма", stats.total(values), ".3f"),
        ("Ср. арифм.", stats.mean(values), ".3f"),
        ("Сумма кв.", stats.sum_of_squares(values), ".3f"),
        ("Ср. кв.", stats.rms(values), ".3f"),
        ("Дисперсия", stats.variance(values), ".3f"),
        ("СКО", stats.std_dev(values), ".3f"),
        ("Станд. откл.", stats.std_dev_sample(values), ".3f"),
        ("Наименьшее", stats.minimum(values), ".3f"),
        ("Наибольшее", stats.maximum(values), ".3f"),
        ("Положительных", stats.count_positive(values), "d"),
        ("Отрицательных", stats.count_negative(values), "d"),
    ]
    for label, value, form in report:
        if value is None:
            print(f"{label}: НЕ СУЩЕСТВУЕТ")
        else:
            print(f"{label}: {value:{form}}")
    return 0


def handle_series(args):
    term, formula = series.FORMULAS[args.func]
    if args.terms is not None:
        series.validate_terms(args.terms)
        result, count = series.sum_by_count(term, args.terms)
    else:
        series.validate_eps(args.eps)
        result, count = series.sum_by_eps(term, args.eps)
    print(formula)
    print(f"Слагаемых: {count}")
    print(f"Сумма ряда: {result:.{series.DIGITS}f}")
    return 0


def handle_integrate(args):
    func, formula, _, _, _ = integration.FUNCTIONS[args.func]
    integration.validate_bounds(args.func, args.start, args.to)
    integration.validate_steps(args.steps)
    result = integration.integrate(func, args.start, args.to, args.steps)
    print(formula)
    print(f"Значение интеграла: {result:.4f}")
    return 0


def handle_fill(args):
    if not (1 <= args.count <= arrays.MAX_COUNT):
        raise ValueError(f"количество элементов вне диапазона 1..{arrays.MAX_COUNT}")
    
    # Используем импортированные MIN_VALUE и MAX_VALUE
    if not (MIN_VALUE <= args.min <= args.max <= MAX_VALUE):
        raise ValueError("некорректные границы значений")

    result = measure_time(
        "fill", 
        arrays.generate_array, 
        args.count, args.min, args.max, args.seed
    )
    write_array(args.output, result)
    return 0


def handle_sort(args):
    array = read_array(args.input)
    method = sorting.METHODS[args.method]
    descending = (args.order == "desc")
    
    measure_time(
        f"sort ({args.method})", 
        method, 
        array, descending
    )
    
    write_array(args.output, array)
    print("Массив отсортирован.")
    return 0


def handle_search(args):
    if abs(args.value) > arrays.MAX_SEARCH:
        raise ValueError(f"искомое значение по модулю не должно превышать {arrays.MAX_SEARCH}")
        
    array = read_array(args.input)
    
    for i in range(len(array) - 1):
        if array[i] > array[i + 1]:
            raise ValueError("массив не упорядочен по возрастанию")

    index = measure_time(
        "search", 
        arrays.binary_search, 
        array, args.value
    )

    if index is None:
        print(f"Значение {args.value} не найдено.")
        return 1
        
    print(f"Значение {args.value} имеет элемент с индексом {index + 1}.")
    return 0


HANDLERS = {
    "solve": handle_solve,
    "stats": handle_stats,
    "series": handle_series,
    "integrate": handle_integrate,
    "fill": handle_fill,
    "sort": handle_sort,
    "search": handle_search,
}


def main(argv):
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