"""
Эксперименты, подтверждающие теоретические результаты статьи.
"""

import random
import math
from typing import List, Tuple
import statistics

from algorithms import (
    bubble_sort_basic,
    bubble_sort_optimized,
    bubble_sort_variant,
    passes_from_inversions,
)
from birthday import birthday_collision, birthday_probability, bubble_probability


def experiment_rayleigh_convergence(
        n_values: List[int] = [100, 500, 1000, 5000],
        trials: int = 2000,
        seed: int = 42,
) -> dict:
    """
    Эксперимент 1: Проверка сходимости (n - P_n)/sqrt(n) к Ray(1).

    Сравниваем эмпирическое среднее и дисперсию с теоретическими:
    E[Ray(1)] = sqrt(pi/2) ≈ 1.2533
    Var[Ray(1)] = (4 - pi)/2 ≈ 0.4292
    """
    rng = random.Random(seed)
    results = {}

    for n in n_values:
        values = []
        for _ in range(trials):
            arr = list(range(n))
            rng.shuffle(arr)
            passes = passes_from_inversions(arr)
            values.append((n - passes) / math.sqrt(n))

        results[n] = {
            "mean": statistics.mean(values),
            "variance": statistics.variance(values),
            "theory_mean": math.sqrt(math.pi / 2),
            "theory_var": (4 - math.pi) / 2,
        }

    return results


def experiment_birthday_vs_bubble(
        n: int = 365,
        m: int = 22,
        trials: int = 10000,
        seed: int = 42,
) -> dict:
    """
    Эксперимент 2: Сравнение вероятностей для birthday problem и bubble sort.

    Проверяем пример 5.1 из статьи:
    P{C_358 > 23} ≈ 0.4857834
    P{P_365 <= 343} ≈ 0.4857848
    P{C_365 > 23} ≈ 0.4927028
    """
    rng = random.Random(seed)

    # Теоретические значения
    theory = {
        "birthday_n_minus_m_minus_1": birthday_probability(n - (m - 1), m),
        "bubble": bubble_probability(n, m),
        "birthday_n": birthday_probability(n, m),
    }

    # Эмпирические значения
    birthday_hits = 0
    bubble_hits = 0

    for _ in range(trials):
        c = birthday_collision(n, rng)
        if c > m + 1:
            birthday_hits += 1

        arr = list(range(n))
        rng.shuffle(arr)
        p = passes_from_inversions(arr)
        if p <= n - m:
            bubble_hits += 1

    empirical = {
        "birthday": birthday_hits / trials,
        "bubble": bubble_hits / trials,
    }

    return {"theory": theory, "empirical": empirical}


def experiment_optimization_overhead(
        n_values: List[int] = [10, 50, 100, 500, 1000],
        trials: int = 500,
        seed: int = 42,
) -> dict:
    """
    Эксперимент 3: Проверка парадокса оптимизаций.

    Сравниваем число операций (сравнений + присваиваний) для:
    - базовой версии (algorithm 1)
    - оптимизированной версии (algorithm 3)
    """
    rng = random.Random(seed)
    results = {}

    for n in n_values:
        basic_ops = []
        opt_ops = []

        for _ in range(trials):
            arr = list(range(n))
            rng.shuffle(arr)

            # Базовая: n^2/2 сравнений в среднем, но мы считаем точно
            _, _ = bubble_sort_basic(arr)
            basic_comparisons = sum(n - i - 1 for i in range(n))
            basic_ops.append(basic_comparisons)

            # Оптимизированная: сравнения + булевы присваивания
            _, passes, bool_assignments = bubble_sort_optimized(arr)
            comparisons = sum(n - i - 1 for i in range(passes))
            opt_ops.append(comparisons + bool_assignments)

        results[n] = {
            "basic_mean_ops": statistics.mean(basic_ops),
            "optimized_mean_ops": statistics.mean(opt_ops),
            "ratio": statistics.mean(opt_ops) / statistics.mean(basic_ops),
        }

    return results


def experiment_theoretical_vs_empirical(
        n_values: List[int] = [100, 500, 1000, 5000],
        trials: int = 1000,
        seed: int = 42,
) -> dict:
    """
    Эксперимент 4: Сравнение теоретических вероятностей с эмпирическими.
    """
    rng = random.Random(seed)
    results = {}

    for n in n_values:
        empirical = []
        theoretical = []

        for m in range(1, int(2 * math.sqrt(n))):
            # Эмпирическая вероятность
            hits = 0
            for _ in range(trials):
                arr = list(range(n))
                rng.shuffle(arr)
                p = passes_from_inversions(arr)
                if p <= n - m:
                    hits += 1
            empirical.append(hits / trials)
            theoretical.append(bubble_probability(n, m))

        results[n] = {"empirical": empirical, "theoretical": theoretical}

    return results


if __name__ == "__main__":
    print("=" * 60)
    print("Эксперимент 1: Сходимость к распределению Рэлея")
    print("=" * 60)
    res = experiment_rayleigh_convergence(
        n_values=[50, 100, 200, 500],   # было [100, 500, 1000, 5000]
        trials=200,                     # было 2000
    )
    for n, data in res.items():
        print(f"n = {n}:")
        print(f"  E[X_n] = {data['mean']:.4f}  (теория: {data['theory_mean']:.4f})")
        print(f"  Var[X_n] = {data['variance']:.4f}  (теория: {data['theory_var']:.4f})")

    print()
    print("=" * 60)
    print("Эксперимент 2: Birthday problem vs Bubble sort (пример 5.1)")
    print("=" * 60)
    res = experiment_birthday_vs_bubble(
        n=365, m=22,
        trials=1000,                    # было 10000
    )
    print(f"Теория:")
    print(f"  P{{C_358 > 23}} = {res['theory']['birthday_n_minus_m_minus_1']:.7f}")
    print(f"  P{{P_365 <= 343}} = {res['theory']['bubble']:.7f}")
    print(f"  P{{C_365 > 23}} = {res['theory']['birthday_n']:.7f}")
    print(f"Эмпирика:")
    print(f"  Birthday: {res['empirical']['birthday']:.4f}")
    print(f"  Bubble:   {res['empirical']['bubble']:.4f}")

    print()
    print("=" * 60)
    print("Эксперимент 3: Парадокс оптимизаций")
    print("=" * 60)
    res = experiment_optimization_overhead(
        n_values=[10, 50, 100, 200],    # было [10, 50, 100, 500, 1000]
        trials=100,                     # было 500
    )
    for n, data in res.items():
        print(f"n = {n}:")
        print(f"  Базовая:       {data['basic_mean_ops']:.0f} операций")
        print(f"  Оптимизированная: {data['optimized_mean_ops']:.0f} операций")
        print(f"  Отношение:     {data['ratio']:.4f}")