import sys
import unittest
import warnings

sys.path.insert(0, "/opt/trading")

from modules.risk_engine.app.risk_calculator import RiskCalculator


class RiskPctSemanticsTests(unittest.TestCase):
    def setUp(self):
        self.rc = RiskCalculator()

    def quote(self, risk_pct):
        acct = {"equity": 10000, "risk_pct": risk_pct, "min_qty": 0.001, "qty_step": 0.001}
        return self.rc.calculate_quote(acct, "COINM_SHORT", 100.0, 90.0, {})

    def test_canonical_001_means_one_percent(self):
        with warnings.catch_warnings(record=True) as seen:
            warnings.simplefilter("always")
            q = self.quote(0.01)
        self.assertEqual(len(seen), 0)
        self.assertEqual(q["risk_usd"], 100.0)
        self.assertEqual(q["qty"], 10.0)

    def test_canonical_002_means_two_percent(self):
        with warnings.catch_warnings(record=True) as seen:
            warnings.simplefilter("always")
            q = self.quote(0.02)
        self.assertEqual(len(seen), 0)
        self.assertEqual(q["risk_usd"], 200.0)
        self.assertEqual(q["qty"], 20.0)

    def test_noncanonical_10_warns_and_means_hundred_percent(self):
        with warnings.catch_warnings(record=True) as seen:
            warnings.simplefilter("always")
            q = self.quote(1.0)
        self.assertGreaterEqual(len(seen), 1)
        self.assertEqual(q["risk_usd"], 10000.0)
        self.assertEqual(q["qty"], 1000.0)

    def test_legacy_20_warns_and_means_two_percent(self):
        with warnings.catch_warnings(record=True) as seen:
            warnings.simplefilter("always")
            q = self.quote(2.0)
        self.assertGreaterEqual(len(seen), 1)
        self.assertEqual(q["risk_usd"], 200.0)
        self.assertEqual(q["qty"], 20.0)

    def test_zero_or_invalid_stays_zero_risk(self):
        for raw in [0, "oops"]:
            with warnings.catch_warnings(record=True) as seen:
                warnings.simplefilter("always")
                q = self.quote(raw)
            self.assertEqual(len(seen), 0)
            self.assertEqual(q["risk_usd"], 0.0)
            self.assertEqual(q["qty"], 0)


if __name__ == "__main__":
    unittest.main()
