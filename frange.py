def frange(start, stop=None, step=None):
    """Функция-генератор для формирования последовательности
    из вещественных чисел от start до stop через step"""
    start = float(start)
    if step is None:
        step = 1.0
    if stop is None:
        stop = start + 0.0
        start = 1.0

    count = 0
    while True:
        current = float(start + count * step)
        if step > 0 and current >= stop:
            break
        elif step < 0 and current <= stop:
            break
        yield current
        count += 1
