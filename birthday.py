"""
Задача о днях рождения и её связь с bubble sort.
"""

import random
from typing import List, Tuple


def birthday_collision(n_days: int, rng: random.Random = None) -> int:
    """
    Возвращает C_n — номер первого человека, чей день рождения совпал
    с днём рождения кого-то из предыдущих.

    Args:
        n_days: число дней в году (n)
        rng: генератор случайных чисел

    Returns:
        C_n — номер человека при первом совпадении
    """
    if rng is None:
        rng = random.Random()

    seen = set()
    person = 0
    while True:
        person += 1
        day = rng.randrange(n_days)
        if day in seen:
            return person
        seen.add(day)


def birthday_probability(n_days: int, m: int) -> float:
    """
    P{C_n > m+1} — вероятность, что первые m+1 человек имеют разные дни рождения.

    Формула: prod_{k=1}^{m} (1 - k/n)
    """
    p = 1.0
    for k in range(1, m + 1):
        p *= (1.0 - k / n_days)
    return p


def bubble_probability(n: int, m: int) -> float:
    """
    P{P_n <= n-m} — вероятность, что bubble sort завершится за n-m проходов.

    Формула: prod_{k=1}^{m} (1 - k/(n-m+k))
    """
    p = 1.0
    for k in range(1, m + 1):
        p *= (1.0 - k / (n - m + k))
    return p