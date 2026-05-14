# 50_MONITORING_REQUIREMENTS

## Current State

| Component | Status | Gap |
|-----------|--------|-----|
| Service logs | AVAILABLE | journalctl only |
| Events log | AVAILABLE | events.jsonl |
| Metrics endpoint | AVAILABLE | /api/metrics |
| Telegram alerts | AVAILABLE | TELEGRAM_ENABLED |
| Real-time dashboard | MISSING | No live dashboard |
| Alert thresholds | MISSING | No configurable alerts |
| P&L tracking | PARTIAL | Basic position tracking |

## Required Monitoring

| Monitor | Priority | Status |
|---------|----------|--------|
| Position open/close | P0 | PARTIAL |
| P&L per trade | P0 | MISSING |
| Daily P&L | P0 | MISSING |
| Risk limit breaches | P0 | MISSING |
| Service health | P1 | AVAILABLE |
| Guard status | P1 | AVAILABLE |
| Execution latency | P2 | MISSING |

## Recommendations

1. Enable Telegram alerts (already configured)
2. Add P&L calculation to position tracking
3. Implement daily P&L summary
4. Add configurable alert thresholds
5. Create real-time dashboard

## Status: PARTIAL

Basic monitoring exists. Production requires enhanced monitoring.
