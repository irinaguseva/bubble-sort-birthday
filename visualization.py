"""
Визуализация результатов: гистограммы, сравнение с теорией.
"""

import math
import random
import matplotlib.pyplot as plt
import numpy as np

from algorithms import passes_from_inversions
from birthday import birthday_collision


def plot_rayleigh_distribution(n: int = 1000, trials: int = 5000, seed: int = 42):
    """
    Гистограмма (n - P_n)/sqrt(n) с наложенной плотностью Ray(1).
    """
    rng = random.Random(seed)
    values = []

    for _ in range(trials):
        arr = list(range(n))
        rng.shuffle(arr)
        passes = passes_from_inversions(arr)
        values.append((n - passes) / math.sqrt(n))

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(values, bins=50, density=True, alpha=0.6, label="Эмпирика")

    # Теоретическая плотность Ray(1): f(x) = x * exp(-x^2/2)
    x = np.linspace(0, 4, 200)
    ax.plot(x, x * np.exp(-x ** 2 / 2), 'r-', linewidth=2, label="Ray(1) плотность")

    ax.set_xlabel(r'$X_n = (n - P_n)/\sqrt{n}$')
    ax.set_ylabel('Плотность')
    ax.set_title(f'Сходимость к распределению Рэлея (n={n})')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('rayleigh_convergence.png', dpi=150)
    plt.show()


def plot_birthday_vs_bubble(n: int = 365, trials: int = 3000, seed: int = 42):
    """
    Сравнение распределений C_n и P_n.
    """
    rng = random.Random(seed)
    c_values = []
    p_values = []

    for _ in range(trials):
        c = birthday_collision(n, rng)
        c_values.append((c - 1) / math.sqrt(n))

        arr = list(range(n))
        rng.shuffle(arr)
        p = passes_from_inversions(arr)
        p_values.append((n - p) / math.sqrt(n))

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    for ax, vals, label in [
        (axes[0], c_values, r'$(C_n - 1)/\sqrt{n}$'),
        (axes[1], p_values, r'$(n - P_n)/\sqrt{n}$'),
    ]:
        ax.hist(vals, bins=40, density=True, alpha=0.6, label="Эмпирика")
        x = np.linspace(0, 4, 200)
        ax.plot(x, x * np.exp(-x ** 2 / 2), 'r-', linewidth=2, label="Ray(1)")
        ax.set_xlabel(label)
        ax.set_ylabel('Плотность')
        ax.legend()
        ax.grid(True, alpha=0.3)

    axes[0].set_title('Birthday problem')
    axes[1].set_title('Bubble sort')

    plt.tight_layout()
    plt.savefig('birthday_vs_bubble.png', dpi=150)
    plt.show()


def plot_optimization_paradox(seed: int = 42):
    """
    График: отношение операций (оптимизированная / базовая) vs n.
    """
    from experiments import experiment_optimization_overhead

    n_values = [10, 20, 50, 100, 200, 500, 1000, 2000]
    res = experiment_optimization_overhead(n_values, trials=200, seed=seed)

    ns = sorted(res.keys())
    ratios = [res[n]["ratio"] for n in ns]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(ns, ratios, 'bo-', linewidth=2, markersize=8)
    ax.axhline(y=1.0, color='r', linestyle='--', label='Без изменений')
    ax.set_xscale('log')
    ax.set_xlabel('n (размер массива)')
    ax.set_ylabel('Отношение операций (опт. / базовая)')
    ax.set_title('Парадокс оптимизаций: оптимизация добавляет работы')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('optimization_paradox.png', dpi=150)
    plt.show()


if __name__ == "__main__":
    print("Строим график сходимости к Рэлею...")
    plot_rayleigh_distribution()

    print("Строим сравнение birthday problem и bubble sort...")
    plot_birthday_vs_bubble()

    print("Строим график парадокса оптимизаций...")
    plot_optimization_paradox()