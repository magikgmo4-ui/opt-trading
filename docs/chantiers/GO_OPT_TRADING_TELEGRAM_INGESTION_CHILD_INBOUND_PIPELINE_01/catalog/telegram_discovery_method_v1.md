# Telegram Discovery Method V1

## Date: 2026-06-05
## Status: OPERATIONAL — replaces username guessing with real search

---

## 1. Method

```
WEB_OSINT → TELEGRAM_SEARCH → SAMPLE(200 msgs) → PARSE → QUALIFY → ACTIVE
```

| Step | Action | Tool |
|---|---|---|
| 1 | Search keywords on Telegram | Telethon SearchRequest / Telegram in-app search |
| 2 | For each result: sample 200 messages | collector_telegram --limit 200 |
| 3 | Parse messages (regex only, no LLM) | parse_telegram_message |
| 4 | Count complete setups (direction+entry+sl+tp) | batch_qualify |
| 5 | If >= 10 complete → promote ACTIVE | signal_tracker |
| 6 | If < 10 but > 0 → WATCH | Keep collecting |
| 7 | If 0 → REJECTED or CONTEXT_ONLY | Route to context |

---

## 2. Why not username guessing

- 115 catalog usernames tested → 0 valid
- Telegram usernames can't be guessed
- Clones/fakes use different names than originals
- Search by content, not by name

---

## 3. Search Keywords

Defined in `configs/telegram/discovery_keywords.json`:
- 8 buckets, 80+ keywords
- Priority P0: XAU/Gold, BTC/ETH
- Priority P1: Forex, OI/Funding, Whale/On-chain
- Priority P2: Alts, Communities, Macro/News

---

## 4. Candidate Schema

Each discovered channel is stored in `discovery_candidates.json`:
```json
{
  "alias": "channel_username",
  "source": "telegram_search",
  "search_keyword": "gold signals free",
  "bucket": "XAU_GOLD",
  "status": "DISCOVERY",
  "expected_assets": ["XAUUSD"],
  "expected_format": "BUY/SELL + ENTRY + SL + TP",
  "sample_limit": 200,
  "complete_setups": 0,
  "tp_only_count": 0,
  "parse_rate": 0,
  "candidate_score": 0,
  "next_action": "collect_sample"
}
```

---

## 5. How to use

```bash
# Step 1: Search Telegram for channels
bash modules/analysis_bundles/scripts/discover_telegram_channels.sh

# Step 2: Sample messages from discovered candidates
# (run on admin-trading): add candidates to channels.json, run collector

# Step 3: Sync + qualify
bash modules/analysis_bundles/scripts/sync_admin_trading.sh
bash modules/analysis_bundles/scripts/batch_qualify.sh

# Step 4: Promote ACTIVE channels
# Update _CHANNEL_PRIORITY in telegram_screener_bridge.py
```

---

## 6. Results so far

| Method | Tested | Valid | Active |
|---|---|---|---|
| Proven channels (manual) | 13 | 13 | 0 |
| XAU username guessing | 20 | 17 | 3 |
| Catalog guessing | 115 | 0 | 0 |
| **TOTAL** | **148** | **30** | **5** |

Next: Telegram Search-based discovery using real keywords.
