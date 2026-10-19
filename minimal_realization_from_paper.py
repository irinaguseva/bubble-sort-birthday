"""
Реализация четырёх алгоритмов из статьи
Jichu Jiang, "Relating bubble sort to birthday problem", 2024.
Приложение A, алгоритмы 1–4.
"""


def bubble_sort(a):
    """Algorithm 1: Bubble sort."""
    a = a.copy()
    n = len(a)
    for i in range(1, n + 1):
        for j in range(1, n - i + 1):
            if a[j - 1] > a[j]:
                a[j - 1], a[j] = a[j], a[j - 1]
    return a


def bubble_sort_optimized(a):
    """Algorithm 3: Optimization of bubble sort."""
    a = a.copy()
    n = len(a)
    for i in range(1, n + 1):
        xi = False
        for j in range(1, n - i + 1):
            if a[j - 1] > a[j]:
                a[j - 1], a[j] = a[j], a[j - 1]
                xi = True
        if not xi:
            return a
    return a


def bubble_sort_variant(a):
    """Algorithm 4: Variant of optimization of bubble sort."""
    a = a.copy()
    n = len(a)
    for i in range(1, n + 1):
        xi = False
        j = 1
        while j <= n - i:
            if a[j - 1] > a[j]:
                a[j - 1], a[j] = a[j], a[j - 1]
                xi = True
                break
            j += 1
        if not xi:
            return a
        for k in range(j + 1, n - i + 1):
            if a[k - 1] > a[k]:
                a[k - 1], a[k] = a[k], a[k - 1]
    return a