import random
import time
import pandas as pd

from algorithms.knapsack import solve_knapsack_dp
from algorithms.greedy import solve_knapsack_greedy


def run_benchmarks(max_n=80, capacity=100, repeats=3, seed=42):
    """
    Benchmark DP and Greedy on deterministic pseudo-random package sets.
    Each reported runtime is the median across repeats.
    """
    rng = random.Random(seed)
    rows = []
    counts = sorted(set([10, 20, 30, 40, 50, 60, 70, 80, 100, 120, 150, 180, 200]))
    counts = [n for n in counts if n <= max_n]
    if max_n not in counts:
        counts.append(max_n)
    counts = sorted(set(counts))

    for n in counts:
        packages = [
            {"id": f"P{i+1}", "weight": rng.randint(1, 25), "value": rng.randint(1, 100)}
            for i in range(n)
        ]
        dp_times = []
        greedy_times = []
        dp_result = None
        greedy_result = None

        for _ in range(max(1, repeats)):
            start = time.perf_counter()
            dp_result = solve_knapsack_dp(packages, int(capacity))
            dp_times.append((time.perf_counter() - start) * 1000)

            start = time.perf_counter()
            greedy_result = solve_knapsack_greedy(packages, int(capacity))
            greedy_times.append((time.perf_counter() - start) * 1000)

        dp_value = dp_result["total_value"]
        greedy_value = greedy_result["total_value"]
        gap = ((dp_value - greedy_value) / dp_value * 100) if dp_value else 0.0
        rows.append({
            "Package count": n,
            "Capacity (kg)": int(capacity),
            "DP value": dp_value,
            "Greedy value": greedy_value,
            "Optimality gap (%)": round(gap, 2),
            "DP time (ms)": round(sorted(dp_times)[len(dp_times) // 2], 4),
            "Greedy time (ms)": round(sorted(greedy_times)[len(greedy_times) // 2], 4),
        })
    return pd.DataFrame(rows)
