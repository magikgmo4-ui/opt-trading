from modules.ipo_tracking.scoring.spacex_score import derive_technical, score_snapshot


def test_score_snapshot_offline_empty_is_monitor_only():
    snapshot = {"market": {"bars": []}, "news": {"articles": []}, "sec": {"recent_filings": []}}
    snapshot["technical"] = derive_technical(snapshot["market"])
    scores = score_snapshot(snapshot)
    assert scores["monitor_only"] is True
    assert "trade_ready_score" in scores
