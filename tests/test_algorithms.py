"""
Тесты корректности алгоритмов.
"""

import random
import pytest
from algorithms import (
    bubble_sort_basic,
    bubble_sort_optimized,
    bubble_sort_variant,
    count_inversions,
    passes_from_inversions,
)


def test_bubble_sort_basic():
    arr = [3, 1, 4, 1, 5, 9, 2, 6]
    result, passes = bubble_sort_basic(arr)
    assert result == sorted(arr)
    assert passes == len(arr)


def test_bubble_sort_optimized():
    arr = [3, 1, 4, 1, 5, 9, 2, 6]
    result, passes, _ = bubble_sort_optimized(arr)
    assert result == sorted(arr)
    assert passes <= len(arr)


def test_bubble_sort_variant():
    arr = [3, 1, 4, 1, 5, 9, 2, 6]
    result, passes, _ = bubble_sort_variant(arr)
    assert result == sorted(arr)


def test_count_inversions():
    arr = [3, 1, 2]
    V = count_inversions(arr)
    # инверсии: (3,1), (3,2) — меньшие элементы 1 и 2 (ранги 0 и 1)
    assert V == [1, 1, 0]


def test_passes_from_inversions():
    arr = [3, 1, 2]
    assert passes_from_inversions(arr) == 2


def test_sorted_array():
    arr = list(range(10))
    assert passes_from_inversions(arr) == 1  # один проход, без обменов


def test_reverse_array():
    n = 10
    arr = list(range(n, 0, -1))
    assert passes_from_inversions(arr) == n


def test_random_consistency():
    """Проверяем, что формула P_n = max(V_i + 1) работает."""
    rng = random.Random(42)
    for _ in range(100):
        n = rng.randint(1, 20)
        arr = list(range(n))
        rng.shuffle(arr)

        # Через инверсии
        p_theory = passes_from_inversions(arr)

        # Через симуляцию
        _, p_sim, _ = bubble_sort_optimized(arr)

        assert p_theory == p_sim, f"Mismatch for {arr}: {p_theory} vs {p_sim}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])