"""Test that every UI button maps to a real intent — no fallback to /read/system."""
from __future__ import annotations
import unittest
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from modules.voice_operator.engine.intent_router import route, INTENT_PATTERNS, list_intents


class TestIntentRouterAllButtons(unittest.TestCase):
    """Every UI button phrase must resolve to a non-unknown intent."""

    def test_etat_systeme(self):
        for phrase in ["etat systeme", "status systeme", "etat du systeme", "health"]:
            r = route(phrase)
            self.assertEqual(r.intent, "system_status", f"phrase='{phrase}'")
            self.assertNotEqual(r.intent, "unknown", f"phrase='{phrase}'")
            self.assertEqual(r.endpoint, "/read/system")

    def test_rapport_marche(self):
        for phrase in ["rapport marche", "vue marche", "market view", "snapshot marche", "rapport des marches",
                       "rapport marché", "vue marché", "marché", "market report"]:
            r = route(phrase)
            self.assertEqual(r.intent, "market_view", f"phrase='{phrase}'")
            self.assertNotEqual(r.intent, "unknown", f"phrase='{phrase}'")
            self.assertEqual(r.endpoint, "/read/composite")

    def test_analyse_btc(self):
        for phrase in ["analyse btc", "btc complet", "btc detail", "analyse bitcoin", "btc analyse"]:
            r = route(phrase)
            self.assertEqual(r.intent, "btc_full", f"phrase='{phrase}'")
            self.assertNotEqual(r.intent, "unknown", f"phrase='{phrase}'")

    def test_analyse_gold(self):
        for phrase in ["analyse gold", "analyse or", "gold complet", "or complet", "analyse xau"]:
            r = route(phrase)
            self.assertEqual(r.intent, "gold_full", f"phrase='{phrase}'")
            self.assertNotEqual(r.intent, "unknown", f"phrase='{phrase}'")

    def test_resume_spcx(self):
        for phrase in ["resume spcx", "resume SPCX", "SPCX resume", "spcx complet", "spcx full",
                       "resumer spcx", "spcx resumer"]:
            r = route(phrase)
            self.assertEqual(r.intent, "spcx_full", f"phrase='{phrase}'")
            self.assertNotEqual(r.intent, "unknown", f"phrase='{phrase}'")

    def test_alertes_telegram(self):
        for phrase in ["alertes telegram", "telegram alerts", "signaux telegram", "telegram signals"]:
            r = route(phrase)
            self.assertEqual(r.intent, "telegram_alerts", f"phrase='{phrase}'")
            self.assertNotEqual(r.intent, "unknown", f"phrase='{phrase}'")

    def test_setups_actifs(self):
        for phrase in ["setups actifs", "setups", "setup actifs", "all setups", "tous les setups"]:
            r = route(phrase)
            self.assertEqual(r.intent, "setups_all", f"phrase='{phrase}'")
            self.assertNotEqual(r.intent, "unknown", f"phrase='{phrase}'")

    def test_setup_btc(self):
        for phrase in ["setup btc", "setup bitcoin"]:
            r = route(phrase)
            self.assertEqual(r.intent, "setup_detail", f"phrase='{phrase}'")
            self.assertNotEqual(r.intent, "unknown", f"phrase='{phrase}'")
            self.assertEqual(r.params.get("symbol"), "BTC")

    def test_setup_gold(self):
        for phrase in ["setup gold", "setup or", "setup xau", "setup xauusd"]:
            r = route(phrase)
            self.assertEqual(r.intent, "setup_detail", f"phrase='{phrase}'")
            self.assertNotEqual(r.intent, "unknown", f"phrase='{phrase}'")
            self.assertEqual(r.params.get("symbol"), "XAUUSD")

    def test_setup_spcx(self):
        for phrase in ["setup spcx", "setup spacex"]:
            r = route(phrase)
            self.assertEqual(r.intent, "setup_detail", f"phrase='{phrase}'")
            self.assertNotEqual(r.intent, "unknown", f"phrase='{phrase}'")
            self.assertEqual(r.params.get("symbol"), "SPCX")

    def test_score_btc(self):
        for phrase in ["score btc", "score bitcoin"]:
            r = route(phrase)
            self.assertEqual(r.intent, "score_detail", f"phrase='{phrase}'")
            self.assertNotEqual(r.intent, "unknown", f"phrase='{phrase}'")
            self.assertEqual(r.params.get("symbol"), "BTC")

    def test_score_gold(self):
        for phrase in ["score gold", "score or", "score xau"]:
            r = route(phrase)
            self.assertEqual(r.intent, "score_detail", f"phrase='{phrase}'")
            self.assertNotEqual(r.intent, "unknown", f"phrase='{phrase}'")
            self.assertEqual(r.params.get("symbol"), "XAUUSD")

    def test_score_spcx(self):
        for phrase in ["score spcx", "score spacex", "note spcx"]:
            r = route(phrase)
            self.assertEqual(r.intent, "score_detail", f"phrase='{phrase}'")
            self.assertNotEqual(r.intent, "unknown", f"phrase='{phrase}'")
            self.assertEqual(r.params.get("symbol"), "SPCX")

    def test_rapport_quotidien(self):
        for phrase in ["rapport quotidien", "rapport daily", "daily report", "rapport journalier"]:
            r = route(phrase)
            self.assertEqual(r.intent, "daily_report", f"phrase='{phrase}'")
            self.assertNotEqual(r.intent, "unknown", f"phrase='{phrase}'")

    def test_priorites(self):
        for phrase in ["priorites", "priorite", "top priorites", "quoi regarder", "que regarder"]:
            r = route(phrase)
            self.assertEqual(r.intent, "priorities", f"phrase='{phrase}'")
            self.assertNotEqual(r.intent, "unknown", f"phrase='{phrase}'")

    def test_attention(self):
        for phrase in ["attention", "avertissements", "quoi surveiller", "points attention"]:
            r = route(phrase)
            self.assertEqual(r.intent, "attention", f"phrase='{phrase}'")
            self.assertNotEqual(r.intent, "unknown", f"phrase='{phrase}'")

    def test_resume_executif(self):
        for phrase in ["resume executif", "exec summary", "resume", "bref"]:
            r = route(phrase)
            self.assertEqual(r.intent, "exec_summary", f"phrase='{phrase}'")
            self.assertNotEqual(r.intent, "unknown", f"phrase='{phrase}'")

    def test_top_movers(self):
        for phrase in ["top movers", "movers", "bouge", "mouvements"]:
            r = route(phrase)
            self.assertEqual(r.intent, "top_movers", f"phrase='{phrase}'")
            self.assertNotEqual(r.intent, "unknown", f"phrase='{phrase}'")

    def test_watchlist_ia(self):
        for phrase in ["watchlist ia", "ia watchlist", "ai watchlist", "watchlist ai"]:
            r = route(phrase)
            self.assertEqual(r.intent, "watchlist_ia", f"phrase='{phrase}'")
            self.assertNotEqual(r.intent, "unknown", f"phrase='{phrase}'")

    def test_watchlist_spatial(self):
        for phrase in ["watchlist spatial", "spatial watchlist", "space watchlist", "watchlist space", "spatiale"]:
            r = route(phrase)
            self.assertEqual(r.intent, "watchlist_spatial", f"phrase='{phrase}'")
            self.assertNotEqual(r.intent, "unknown", f"phrase='{phrase}'")

    def test_unknown_command_fallback(self):
        r = route("commande inconnue xyz123")
        self.assertEqual(r.intent, "unknown")
        self.assertEqual(r.endpoint, "/read/system")
        self.assertEqual(r.confidence, 0.0)

    def test_no_command_falls_to_system_unintentionally(self):
        all_intents = set()
        registered = {p[1] for p in INTENT_PATTERNS}
        self.assertNotIn("unknown", registered)
        self.assertIn("system_status", registered)
        self.assertIn("market_view", registered)
        self.assertIn("btc_full", registered)
        self.assertIn("gold_full", registered)
        self.assertIn("spcx_full", registered)
        self.assertIn("telegram_alerts", registered)
        self.assertIn("setups_all", registered)
        self.assertIn("setup_detail", registered)
        self.assertIn("score_detail", registered)
        self.assertIn("daily_report", registered)
        self.assertIn("priorities", registered)
        self.assertIn("attention", registered)
        self.assertIn("exec_summary", registered)
        self.assertIn("top_movers", registered)
        self.assertIn("watchlist_ia", registered)
        self.assertIn("watchlist_spatial", registered)

    def test_all_composite_intents_have_type(self):
        for keywords, intent_id, endpoint, params in INTENT_PATTERNS:
            if endpoint == "/read/composite":
                self.assertIn("type", params, f"Intent '{intent_id}' missing 'type' in params")
