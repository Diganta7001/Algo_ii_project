def solve_knapsack_greedy(packages, capacity):
    """
    Greedy heuristic for 0/1 Knapsack: choose by descending value/weight ratio.

    This does not guarantee the optimal solution for 0/1 Knapsack.
    """
    if not isinstance(capacity, int) or capacity < 0:
        raise ValueError("capacity must be a non-negative integer")

    items = list(packages)
    for item in items:
        if not isinstance(item["weight"], int) or item["weight"] <= 0:
            raise ValueError("package weights must be positive integers")
        if not isinstance(item["value"], int) or item["value"] < 0:
            raise ValueError("package values must be non-negative integers")

    # Stable tie-breakers make results deterministic.
    ranked = sorted(
        items,
        key=lambda item: (
            item["value"] / item["weight"],
            item["value"],
            -item["weight"],
        ),
        reverse=True,
    )

    selected = []
    total_weight = 0
    total_value = 0
    for item in ranked:
        if total_weight + item["weight"] <= capacity:
            selected.append(item.copy())
            total_weight += item["weight"]
            total_value += item["value"]

    return {
        "total_value": total_value,
        "total_weight": total_weight,
        "selected_packages": selected,
    }
