import unittest

from algorithms.knapsack import solve_knapsack_dp
from algorithms.greedy import solve_knapsack_greedy


class KnapsackTests(unittest.TestCase):
    def test_assignment_example_dp(self):
        packages = [
            {"id": "P1", "weight": 5, "value": 50},
            {"id": "P2", "weight": 2, "value": 30},
            {"id": "P3", "weight": 7, "value": 45},
            {"id": "P4", "weight": 1, "value": 15},
            {"id": "P5", "weight": 8, "value": 40},
        ]
        result = solve_knapsack_dp(packages, 20)
        self.assertEqual(result["total_value"], 140)
        self.assertLessEqual(result["total_weight"], 20)

    def test_greedy_counterexample(self):
        packages = [
            {"id": "A", "weight": 10, "value": 60},
            {"id": "B", "weight": 20, "value": 100},
            {"id": "C", "weight": 30, "value": 120},
        ]
        dp = solve_knapsack_dp(packages, 50)
        greedy = solve_knapsack_greedy(packages, 50)
        self.assertEqual(dp["total_value"], 220)
        self.assertEqual(greedy["total_value"], 160)
        self.assertGreaterEqual(dp["total_value"], greedy["total_value"])

    def test_zero_capacity(self):
        packages = [{"id": "A", "weight": 1, "value": 10}]
        self.assertEqual(solve_knapsack_dp(packages, 0)["total_value"], 0)

    def test_empty_list(self):
        self.assertEqual(solve_knapsack_dp([], 10)["total_value"], 0)

    def test_selected_packages_fit(self):
        packages = [
            {"id": "A", "weight": 3, "value": 5},
            {"id": "B", "weight": 4, "value": 7},
            {"id": "C", "weight": 5, "value": 8},
        ]
        result = solve_knapsack_dp(packages, 7)
        self.assertLessEqual(result["total_weight"], 7)
        self.assertEqual(result["total_value"], sum(p["value"] for p in result["selected_packages"]))


if __name__ == "__main__":
    unittest.main()
