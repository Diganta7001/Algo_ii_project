def solve_knapsack_dp(packages, capacity):
    """
    Solve 0/1 Knapsack using dynamic programming.

    Args:
        packages: iterable of dicts with keys: id, weight, value
        capacity: non-negative integer capacity

    Returns:
        dict containing total_value, total_weight, selected_packages, dp_table
    """
    if not isinstance(capacity, int) or capacity < 0:
        raise ValueError("capacity must be a non-negative integer")

    items = list(packages)
    for item in items:
        if not isinstance(item["weight"], int) or item["weight"] <= 0:
            raise ValueError("package weights must be positive integers")
        if not isinstance(item["value"], int) or item["value"] < 0:
            raise ValueError("package values must be non-negative integers")

    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        weight = items[i - 1]["weight"]
        value = items[i - 1]["value"]
        for c in range(capacity + 1):
            dp[i][c] = dp[i - 1][c]
            if weight <= c:
                include_value = value + dp[i - 1][c - weight]
                if include_value > dp[i][c]:
                    dp[i][c] = include_value

    # Reconstruct the chosen packages by walking backward through the table.
    selected = []
    remaining_capacity = capacity
    for i in range(n, 0, -1):
        if dp[i][remaining_capacity] != dp[i - 1][remaining_capacity]:
            item = items[i - 1]
            selected.append(item.copy())
            remaining_capacity -= item["weight"]

    selected.reverse()
    total_weight = sum(item["weight"] for item in selected)
    total_value = sum(item["value"] for item in selected)

    return {
        "total_value": total_value,
        "total_weight": total_weight,
        "selected_packages": selected,
        "dp_table": dp,
    }
