"""
Tests for outcome_tracker + calibration_engine + reliability_engine — PR10.
"""

from __future__ import annotations

import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from modules.market_thesis.outcome_models import (
    OutcomeWindow,
    ThesisOutcome,
    determine_actual_direction,
    is_prediction_correct,
    TRACKING_WINDOWS,
)
from modules.market_thesis.calibration_engine import (
    CalibrationResult,
    calibrate,
)
from modules.market_thesis.reliability_engine import (
    ReliabilityReport,
    evaluate_reliability,
)


# ── Outcome models ──────────────────────────────────────────────────────

class TestOutcomeModels(unittest.TestCase):
    def test_determine_bullish(self):
        self.assertEqual(determine_actual_direction(5.0), "bullish")

    def test_determine_bearish(self):
        self.assertEqual(determine_actual_direction(-3.0), "bearish")

    def test_determine_neutral(self):
        self.assertEqual(determine_actual_direction(0.2), "neutral")

    def test_determine_unknown(self):
        self.assertEqual(determine_actual_direction(None), "unknown")

    def test_correct_bullish(self):
        self.assertTrue(is_prediction_correct("bullish", "bullish"))

    def test_correct_bearish(self):
        self.assertTrue(is_prediction_correct("bearish", "bearish"))

    def test_incorrect_opposite(self):
        self.assertFalse(is_prediction_correct("bullish", "bearish"))

    def test_wait_never_correct(self):
        self.assertFalse(is_prediction_correct("wait", "bullish"))

    def test_unknown_never_correct(self):
        self.assertFalse(is_prediction_correct("bullish", "unknown"))

    def test_outcome_creation(self):
        outcome = ThesisOutcome(
            thesis_id="thesis_BTC_01",
            symbol="BTC",
            generated_at=datetime(2026, 6, 15, 12, 0, 0, tzinfo=timezone.utc),
            predicted_direction="bullish",
            predicted_confidence=70,
            predicted_prob_bull=60,
            predicted_prob_range=25,
            predicted_prob_bear=15,
            price_t0=66000,
        )
        self.assertEqual(outcome.symbol, "BTC")
        self.assertFalse(outcome.resolved)

    def test_outcome_with_windows(self):
        outcome = ThesisOutcome(
            thesis_id="t1",
            symbol="BTC",
            generated_at=datetime.now(timezone.utc),
            predicted_direction="bullish",
            predicted_confidence=70,
            predicted_prob_bull=60,
            predicted_prob_range=25,
            predicted_prob_bear=15,
            price_t0=66000,
            windows=[
                OutcomeWindow(hours=1, price=66100, return_pct=0.15),
                OutcomeWindow(hours=24, price=67000, return_pct=1.5),
            ],
        )
        self.assertEqual(len(outcome.windows), 2)
        self.assertEqual(outcome.windows[1].return_pct, 1.5)

    def test_tracking_windows_values(self):
        self.assertEqual(TRACKING_WINDOWS, [1, 4, 24, 48, 168])


# ── Calibration engine ──────────────────────────────────────────────────

class TestCalibrationEngine(unittest.TestCase):
    def setUp(self):
        self.now = datetime.now(timezone.utc)

    def _make_outcome(self, symbol="BTC", direction="bullish", confidence=70,
                      prob_bull=60, prob_bear=15, correct=True, return_pct=3.0,
                      actual_dir="bullish", hours_ago=24):
        return ThesisOutcome(
            thesis_id=f"thesis_{symbol}_{hours_ago}",
            symbol=symbol,
            generated_at=self.now - timedelta(hours=hours_ago),
            predicted_direction=direction,
            predicted_confidence=confidence,
            predicted_prob_bull=prob_bull,
            predicted_prob_range=100 - prob_bull - prob_bear,
            predicted_prob_bear=prob_bear,
            price_t0=66000,
            windows=[
                OutcomeWindow(hours=24, price=66000 * (1 + return_pct / 100),
                             return_pct=return_pct,
                             resolved_at=self.now),
            ],
            actual_direction=actual_dir,
            correct=correct,
            resolved=True,
            resolved_at=self.now,
        )

    def test_empty_calibration(self):
        result = calibrate("BTC")
        self.assertEqual(result.symbol, "BTC")
        self.assertEqual(result.sample_size, 0)

    def test_calibration_with_mock_data(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Patch outcome store root
            import modules.market_thesis.outcome_store as store
            import modules.market_thesis.calibration_engine as calib
            orig_root = store.OUTCOME_ROOT
            store.OUTCOME_ROOT = Path(tmpdir)

            try:
                # Save some outcomes manually
                outcomes = [
                    self._make_outcome("BTC", "bullish", 80, 70, 10, True, 5.0, "bullish", 24),
                    self._make_outcome("BTC", "bullish", 75, 60, 20, True, 2.0, "bullish", 48),
                    self._make_outcome("BTC", "bullish", 65, 50, 30, False, -3.0, "bearish", 72),
                    self._make_outcome("BTC", "bearish", 70, 20, 60, True, -4.0, "bearish", 96),
                    self._make_outcome("BTC", "bullish", 90, 80, 5, True, 1.0, "bullish", 120),
                ]
                for o in outcomes:
                    store.save_outcome(o)

                result = calibrate("BTC", limit=10)
                self.assertEqual(result.sample_size, 5)
                self.assertGreater(result.accuracy_pct, 0)
                self.assertGreater(result.correct_count, 0)

            finally:
                store.OUTCOME_ROOT = orig_root

    def test_accuracy_calculation(self):
        # 4 correct out of 5 = 80%
        with tempfile.TemporaryDirectory() as tmpdir:
            import modules.market_thesis.outcome_store as store
            orig_root = store.OUTCOME_ROOT
            store.OUTCOME_ROOT = Path(tmpdir)
            try:
                for i in range(5):
                    correct = i < 4  # first 4 correct, last incorrect
                    o = self._make_outcome(
                        "BTC", "bullish", 70, 60, 20,
                        correct=correct,
                        return_pct=3.0 if correct else -3.0,
                        actual_dir="bullish" if correct else "bearish",
                        hours_ago=24 + i,
                    )
                    store.save_outcome(o)

                result = calibrate("BTC", limit=10)
                self.assertEqual(result.correct_count, 4)
                self.assertEqual(result.incorrect_count, 1)
                self.assertEqual(result.accuracy_pct, 80.0)

            finally:
                store.OUTCOME_ROOT = orig_root

    def test_confidence_error_overconfident(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            import modules.market_thesis.outcome_store as store
            orig_root = store.OUTCOME_ROOT
            store.OUTCOME_ROOT = Path(tmpdir)
            try:
                # 4 outcomes with high confidence, only 2 correct (50% real accuracy)
                for i in range(4):
                    correct = i < 2
                    o = self._make_outcome(
                        "BTC", "bullish", 90, 70, 10,
                        correct=correct,
                        return_pct=3.0 if correct else -3.0,
                        actual_dir="bullish" if correct else "bearish",
                        hours_ago=24 + i,
                    )
                    store.save_outcome(o)

                result = calibrate("BTC", limit=10)
                self.assertGreater(result.confidence_error, 30)  # 90% predicted vs 50% actual

            finally:
                store.OUTCOME_ROOT = orig_root


# ── Reliability engine ──────────────────────────────────────────────────

class TestReliabilityEngine(unittest.TestCase):
    def setUp(self):
        self.now = datetime.now(timezone.utc)

    def test_empty_reliability(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            import modules.market_thesis.outcome_store as store
            orig_root = store.OUTCOME_ROOT
            store.OUTCOME_ROOT = Path(tmpdir)
            try:
                report = evaluate_reliability("BTC")
                self.assertEqual(report.symbol, "BTC")
                self.assertEqual(report.sample_size, 0)
                self.assertEqual(report.reliability_score, 0)
                self.assertIn(report.grade, ("insufficient", "poor"))
            finally:
                store.OUTCOME_ROOT = orig_root

    def test_reliability_high_sample(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            import modules.market_thesis.outcome_store as store
            orig_root = store.OUTCOME_ROOT
            store.OUTCOME_ROOT = Path(tmpdir)
            try:
                from modules.market_thesis.outcome_models import ThesisOutcome, OutcomeWindow

                # 200 outcomes, 80% correct
                for i in range(200):
                    correct = i < 160
                    o = ThesisOutcome(
                        thesis_id=f"thesis_BTC_{i}",
                        symbol="BTC",
                        generated_at=self.now - timedelta(hours=24 + i % 100),
                        predicted_direction="bullish",
                        predicted_confidence=78,
                        predicted_prob_bull=60,
                        predicted_prob_range=25,
                        predicted_prob_bear=15,
                        price_t0=66000,
                        windows=[OutcomeWindow(
                            hours=24,
                            price=66000 * (1 + (3.0 if correct else -3.0) / 100),
                            return_pct=3.0 if correct else -3.0,
                            resolved_at=self.now,
                        )],
                        actual_direction="bullish" if correct else "bearish",
                        correct=correct,
                        resolved=True,
                        resolved_at=self.now,
                    )
                    store.save_outcome(o)

                report = evaluate_reliability("BTC")
                self.assertGreater(report.sample_size, 100)
                self.assertGreater(report.reliability_score, 50)
                self.assertIn(report.grade, ("excellent", "good", "fair"))

            finally:
                store.OUTCOME_ROOT = orig_root

    def test_reliability_score_bounded(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            import modules.market_thesis.outcome_store as store
            orig_root = store.OUTCOME_ROOT
            store.OUTCOME_ROOT = Path(tmpdir)
            try:
                report = evaluate_reliability("MU")
                self.assertGreaterEqual(report.reliability_score, 0)
                self.assertLessEqual(report.reliability_score, 100)
            finally:
                store.OUTCOME_ROOT = orig_root

    def test_reliability_grade_strings(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            import modules.market_thesis.outcome_store as store
            orig_root = store.OUTCOME_ROOT
            store.OUTCOME_ROOT = Path(tmpdir)
            try:
                report = evaluate_reliability("AVGO")
                self.assertIn(report.grade, ("excellent", "good", "fair", "poor", "insufficient"))
            finally:
                store.OUTCOME_ROOT = orig_root


if __name__ == "__main__":
    unittest.main()
