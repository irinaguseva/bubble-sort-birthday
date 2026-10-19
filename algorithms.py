"""
Реализация алгоритмов сортировки пузырьком из статьи
Jichu Jiang, "Relating bubble sort to birthday problem", 2024.

Algorithm 1: Bubble sort (базовая версия)
Algorithm 2: Static single-assignment form (для анализа)
Algorithm 3: Optimization (досрочный выход при отсутствии обменов)
Algorithm 4: Variant of optimization (с break после первого обмена)
"""

from typing import List, Tuple


def bubble_sort_basic(arr: List[int]) -> Tuple[List[int], int]:
    """
    Algorithm 1: Базовая сортировка пузырьком.

    Returns:
        (отсортированный массив, число проходов)
    """
    a = arr.copy()
    n = len(a)
    passes = n  # без оптимизации всегда n проходов

    for i in range(n):
        for j in range(n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]

    return a, passes


def bubble_sort_optimized(arr: List[int]) -> Tuple[List[int], int, int]:
    """
    Algorithm 3: Оптимизация с досрочным выходом.

    Returns:
        (отсортированный массив, число проходов, число булевых присваиваний)
    """
    a = arr.copy()
    n = len(a)
    passes = 0
    bool_assignments = 0

    for i in range(n):
        passes += 1
        swapped = False
        bool_assignments += 1  # ξ ← F

        for j in range(n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
                bool_assignments += 1  # ξ ← T

        if not swapped:
            break

    return a, passes, bool_assignments


def bubble_sort_variant(arr: List[int]) -> Tuple[List[int], int, int]:
    """
    Algorithm 4: Вариант оптимизации с break после первого обмена.

    Returns:
        (отсортированный массив, число проходов, число булевых присваиваний)
    """
    a = arr.copy()
    n = len(a)
    passes = 0
    bool_assignments = 0

    for i in range(n):
        passes += 1
        swapped = False
        bool_assignments += 1

        j = 0
        while j < n - i - 1:
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
                bool_assignments += 1
                break  # break после первого обмена
            j += 1

        if not swapped:
            break

        # продолжаем с того же места
        for k in range(j + 1, n - i - 1):
            if a[k] > a[k + 1]:
                a[k], a[k + 1] = a[k + 1], a[k]

    return a, passes, bool_assignments


def count_inversions(arr: List[int]) -> List[int]:
    """
    Вычисляет V_{n,i} — число инверсий, где меньший элемент — i-й наименьший.

    Returns:
        список V[0..n-1], где V[i] — число инверсий для i-го наименьшего элемента
    """
    n = len(arr)
    # Сортируем с индексами, чтобы знать ранг каждого элемента
    indexed = sorted(enumerate(arr), key=lambda x: x[1])
    rank = [0] * n
    for r, (orig_idx, _) in enumerate(indexed):
        rank[orig_idx] = r

    V = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                # инверсия: меньший элемент — arr[j], его ранг rank[j]
                V[rank[j]] += 1

    return V


def passes_from_inversions(arr: List[int]) -> int:
    """
    Вычисляет P_n = max(V_{n,i} + 1) — число проходов через инверсии.
    """
    V = count_inversions(arr)
    return max(V) + 1 if V else 0