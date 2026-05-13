---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RUNTIME_GUARDS_FIX_01_20_GUARD_GAP_ANALYSIS
doc_type: chantier/analysis
repo: opt-trading
machine: cursor-ai
go_id: GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RUNTIME_GUARDS_FIX_01
status: active
scope: bounded-runtime-guard
checked_at: 2026-05-13
---

# 20_GUARD_GAP_ANALYSIS

## Gaps issus de PR #338

| Gap | Risque |
| --- | --- |
| `RUNNER_MODE` absent | le mode paper n'est pas prouve |
| `SIMULATION_MODE` absent | simulation obligatoire non prouvee |
| `TRADE_ALLOWED` absent | blocage ordre reel non prouve |
| `active_engine=COINM_SHORT` | contexte agressif deja actif pendant un test paper |
| guards runtime non detectables | `PAPER_TEST` peut atteindre le chemin execution sans preflight explicite |
| ledger perf non exclu pour `PAPER_TEST` | risque de journalisation live-like avant simulation paper |

## Analyse du code avant patch

Le bloc `PAPER_TEST` utilisait bien l'adaptateur `paper`, mais trop tard dans le flux:

1. le payload etait accepte;
2. le risk quote etait calcule;
3. le ledger perf pouvait etre appele;
4. l'evenement pouvait etre journalise;
5. Telegram pouvait etre notifie;
6. seulement ensuite, `executor.execute(order, "paper")` etait appele.

Cette sequence ne satisfaisait pas l'invariant: aucun effet runtime si les guards ne sont pas PASS.

## Decision

Le guard doit etre execute avant:

- `enforce_lock`;
- risk sizing;
- ledger perf;
- `record_event`;
- Telegram;
- position update;
- execution paper.

En cas d'echec, le webhook doit retourner `409` avec une cause explicite et sans secret.
