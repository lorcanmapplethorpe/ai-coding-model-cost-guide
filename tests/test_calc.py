import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).parents[1]))
from cost.calc import estimate, load_models, rate_row


class CalculatorTests(unittest.TestCase):
    def test_cold_and_cached_breakdown(self):
        result = estimate({"input": 0.6, "output": 3.0, "cached": 0.06}, 200000, 20000)
        self.assertAlmostEqual(result["total_usd"], 0.18)
        warm = estimate({"input": 0.6, "output": 3.0, "cached": 0.06}, 200000, 20000, 200000)
        self.assertAlmostEqual(warm["total_usd"], 0.072)
        self.assertAlmostEqual(warm["uncached_input_usd"], 0.0)

    def test_long_context_multipliers_apply_above_threshold(self):
        row = {"input": 0.6, "output": 3.0, "cached": 0.06, "long_context": {"threshold": 272000, "input_multiplier": 2, "output_multiplier": 1.5}}
        result = estimate(row, 300000, 20000, apply_long_context=True)
        self.assertAlmostEqual(result["total_usd"], 0.45)
        self.assertTrue(result["long_context_applied"])

    def test_invalid_counts_and_missing_rates(self):
        with self.assertRaises(ValueError):
            estimate({"input": 1, "output": 2}, 2, 1, 3)
        with self.assertRaises(ValueError):
            estimate({"input": 1}, 2, 1)

    def test_snapshot_has_effective_and_official_values(self):
        models = load_models(pathlib.Path(__file__).parents[1] / "cost/prices.json")
        self.assertGreaterEqual(len(models), 6)
        for model in models.values():
            self.assertIn("effective", model)
            self.assertIn("official", model)
            self.assertTrue(model["source"].startswith("https://"))
            self.assertIn("input", rate_row(model, "effective"))


if __name__ == "__main__":
    unittest.main()
