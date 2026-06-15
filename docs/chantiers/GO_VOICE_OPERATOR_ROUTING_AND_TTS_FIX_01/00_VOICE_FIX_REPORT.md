# GO_VOICE_OPERATOR_ROUTING_AND_TTS_FIX_01 — Report

## Fixes Applied

### P0 — Intent Routing Fixed

**`modules/voice_operator/engine/intent_router.py`**:

- Added `"rapport marche"`, `"rapport des marches"`, `"market report"` → `market_view`
- Added `"resume spcx"`, `"spcx resume"`, `"spcx summary"`, `"resume SPCX"`, `"SPCX resume"` → `spcx_full`
- Placed BEFORE the generic `"resume"` pattern (line 75) to avoid fallback to `exec_summary`

### P1 — TTS Speaks spoken_text

**`modules/localcms/app/main.py`** line 2234:

```diff
- if (ttsReady) speak(oneLine);
+ if (ttsReady) speak(lastOneLine);
```

Now speaks `rich.spoken_text` (richer, more natural) instead of `oneLine`.

### P2 — TTS Rate + Pitch

```diff
- u.lang = 'fr-FR'; u.rate = 1.1;
+ u.lang = 'fr-FR';
+ u.rate = 0.88;
+ u.pitch = 0.95;
```

Slower, more natural voice.

### P3 — Improved spoken_text

- **spcx_full**: Now reads real data fields (price, VWAP, edge score, confidence, top setup, source quality, no execution signal)
- **market_view**: Now includes symbol count
- **exec_summary**: Already had rich text, unchanged

## Test Verification

```bash
# P0: routing tests
curl "http://localhost:8700/voice/query?q=Rapport%20marche"  # → intent=market_view
curl "http://localhost:8700/voice/query?q=Resume%20SPCX"      # → intent=spcx_full
curl "http://localhost:8700/voice/query?q=Resume%20executif"   # → intent=exec_summary
```

## Mode

- Monitor-only, no broker, no orders, no execution
- TTS is browser native (no API cost)
- Decision Support Only
