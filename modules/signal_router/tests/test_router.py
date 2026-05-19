import sys
import unittest
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent.parent))

from app.router import route, parse_incoming, normalize
from app.schema import SignalValidationError


VALID_RAW = {
    "engine": "strat_v1",
    "signal": "BUY",
    "symbol": "BTCUSDT",
    "tf": "1h",
    "price": "65000",
    "tp": "67000",
    "sl": "63000",
    "reason": "breakout",
    "strategy_id": "breakout_v2",
}


class TestParseIncoming(unittest.TestCase):
    def test_valid_buy(self):
        s = parse_incoming(VALID_RAW)
        self.assertEqual(s.signal, "BUY")
        self.assertEqual(s.symbol, "BTCUSDT")
        self.assertAlmostEqual(s.price, 65000.0)
        self.assertAlmostEqual(s.tp, 67000.0)
        self.assertAlmostEqual(s.sl, 63000.0)

    def test_valid_sell_lowercase(self):
        raw = {**VALID_RAW, "signal": "sell"}
        s = parse_incoming(raw)
        self.assertEqual(s.signal, "SELL")

    def test_symbol_uppercased(self):
        raw = {**VALID_RAW, "symbol": "btcusdt"}
        s = parse_incoming(raw)
        self.assertEqual(s.symbol, "BTCUSDT")

    def test_missing_price_raises(self):
        raw = {k: v for k, v in VALID_RAW.items() if k != "price"}
        with self.assertRaises(SignalValidationError):
            parse_incoming(raw)

    def test_invalid_signal_raises(self):
        raw = {**VALID_RAW, "signal": "HOLD"}
        with self.assertRaises(SignalValidationError):
            parse_incoming(raw)

    def test_optional_tp_sl_none(self):
        raw = {k: v for k, v in VALID_RAW.items() if k not in ("tp", "sl")}
        s = parse_incoming(raw)
        self.assertIsNone(s.tp)
        self.assertIsNone(s.sl)

    def test_invalid_price_type(self):
        raw = {**VALID_RAW, "price": "not_a_number"}
        with self.assertRaises(SignalValidationError):
            parse_incoming(raw)


class TestNormalize(unittest.TestCase):
    def test_normalized_signal_fields(self):
        signal_in = parse_incoming(VALID_RAW)
        ns = normalize(signal_in)
        self.assertEqual(ns.ticker, "BTCUSDT")
        self.assertEqual(ns.side, "BUY")
        self.assertEqual(ns.strategy_id, "breakout_v2")
        self.assertIsNotNone(ns.signal_id)
        self.assertGreater(ns.timestamp, 0)

    def test_strategy_id_falls_back_to_engine(self):
        raw = {k: v for k, v in VALID_RAW.items() if k != "strategy_id"}
        signal_in = parse_incoming(raw)
        ns = normalize(signal_in)
        self.assertEqual(ns.strategy_id, "strat_v1")

    def test_to_dict_keys(self):
        signal_in = parse_incoming(VALID_RAW)
        d = normalize(signal_in).to_dict()
        for key in ("signal_id", "ticker", "side", "price", "timestamp", "strategy_id", "tf"):
            self.assertIn(key, d)


class TestRoute(unittest.TestCase):
    def test_full_route(self):
        ns = route(VALID_RAW)
        self.assertEqual(ns.status if hasattr(ns, "status") else "ok", "ok")
        self.assertEqual(ns.ticker, "BTCUSDT")
        self.assertEqual(ns.side, "BUY")

    def test_route_invalid_raises(self):
        with self.assertRaises(SignalValidationError):
            route({"signal": "BUY", "symbol": "BTC"})


if __name__ == "__main__":
    unittest.main()
