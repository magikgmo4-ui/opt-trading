---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RUNTIME_GUARDS_FIX_01_30_RUNTIME_GUARD_SPEC
doc_type: chantier/spec
repo: opt-trading
machine: cursor-ai
go_id: GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RUNTIME_GUARDS_FIX_01
status: active
scope: bounded-runtime-guard
checked_at: 2026-05-13
---

# 30_RUNTIME_GUARD_SPEC

## Guard detectables

`PAPER_TEST` est autorise uniquement si tous les checks suivants sont PASS:

| Guard | Attendu |
| --- | --- |
| `RUNNER_MODE` | `PAPER` |
| `SIMULATION_MODE` | true (`1`, `true`, `yes`, `on`) |
| `TRADE_ALLOWED` | false (`0`, `false`, `no`, `off`) |
| `LEDGER_PATH` | chemin finissant par `ledger_paper.json`, sans `ledger_live` |
| `active_engine` | unset ou moteur non agressif |
| adaptateur | `paper` enregistre dans l'executor |

## Moteurs agressifs

Les moteurs suivants bloquent une tentative `PAPER_TEST` si deja actifs:

```text
COINM_SHORT
USDTM_LONG
```

## Reponse d'echec

Si un guard echoue, le webhook doit bloquer avant tout effet de bord:

```json
{
  "detail": {
    "error": "PAPER_TEST_RUNTIME_GUARD_FAILED",
    "reasons": ["..."],
    "guards": {
      "runner_mode": {
        "ok": false,
        "value": "unset",
        "expected": "PAPER"
      }
    }
  }
}
```

Status HTTP attendu: `409`.

## Endpoint lecture seule

Endpoint ajoute:

```text
GET /api/paper/guards
```

Objectif: rendre le precheck observable sans envoyer de payload `PAPER_TEST`.

L'endpoint ne retourne aucun secret. Il retourne seulement les flags non secrets, l'etat `active_engine`, l'enregistrement de l'adaptateur `paper`, les booleens de guard et les raisons d'echec.

## Effets interdits avant PASS

Si un guard echoue:

- pas de ledger perf;
- pas de `events.jsonl`;
- pas de Telegram;
- pas de position update;
- pas de `executor.execute`;
- pas d'ordre reel;
- pas de trade live.
