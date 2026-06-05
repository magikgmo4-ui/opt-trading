---
doc_id: GO_OPT_TRADING_ORCHESTRATOR_CHILD_PROPOSITION_ENGINE_V1_01
doc_type: gate
repo: opt-trading
go_id: GO_OPT_TRADING_ORCHESTRATOR_CHILD_PROPOSITION_ENGINE_V1_01
parent_go: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
status: open
lifecycle_stage: gate
surface: modules/proposition_engine
updated_at: 2026-05-16
---

# 00_GATE — Proposition Engine V1

## CONTEXTE

GO-06 du backlog orchestrateur. Débloqué par :
- GO-01 `openclaw_operator_bridge` — MERGED (PR #456)
- GO-03 `signal_router` — MERGED (PR #458)
- Smoke engines — PASS (decision_engine, opportunity_ranker, probability_engine)

## OBJECTIF

Créer `modules/proposition_engine/` — module qui :
1. Reçoit un `NormalizedSignal` (output de `signal_router`)
2. Interroge les engines existants (decision_engine, opportunity_ranker, probability_engine) via leurs APIs Python directes
3. Compose un contexte analytique enrichi
4. Appelle OpenClaw builder via `openclaw_operator_bridge` avec ce contexte
5. Retourne une `Proposition` JSON structurée

## CONTRAT

### Input

```python
@dataclass
class PropositionRequest:
    signal: NormalizedSignal   # de signal_router
    request_id: str = ""       # UUID auto si vide
    dry_run: bool = False      # skip OpenClaw call, retourne stub
    timeout_s: int = 90
```

### Output

```python
@dataclass
class Proposition:
    request_id: str
    signal_id: str
    action: str        # BUY | SELL | HOLD | SKIP
    size_pct: float    # % du capital (0.0–1.0)
    entry: float
    sl: float | None
    tp: float | None
    confidence: float  # 0.0–1.0
    rationale: str
    engines_context: dict   # snapshot engines (decision, ranker, probability)
    duration_ms: int
    dry_run: bool
    status: str        # ok | error | timeout | skipped
    error: str | None = None
```

### Erreurs

```python
class PropositionError(Exception): pass
class EngineError(PropositionError): pass
class BridgeError(PropositionError): pass
```

## ARCHITECTURE

```
proposition_engine/
├── __init__.py
├── README.md
├── app/
│   ├── __init__.py
│   ├── __main__.py          # CLI: python3 -m app <signal_id> [--dry-run]
│   ├── schema.py            # PropositionRequest, Proposition, erreurs
│   ├── engines.py           # wrapper Python direct des 3 engines
│   ├── builder_prompt.py    # compose le prompt OpenClaw
│   └── engine.py            # PropositionEngine.propose()
├── tests/
│   └── test_proposition.py  # tests mock bridge + engines
└── scripts/
    ├── cmd.sh               # propose/dry/sanity/test
    └── sanity.sh
```

## GATES D'IMPLÉMENTATION

### GATE 1 — Structure + schema
- [ ] `app/schema.py` : PropositionRequest, Proposition, erreurs
- [ ] `app/__init__.py`, `__init__.py`
- Vérifié : `python3 -c "from app.schema import Proposition"`

### GATE 2 — Engines wrapper
- [ ] `app/engines.py` : `query_engines(signal)` → dict engines_context
- [ ] Utilise `DecisionEngine`, `OpportunityRanker`, `ProbabilityEngine` directement via import Python
- [ ] Retourne snapshot normalisé par symbol
- Vérifié : `python3 -c "from app.engines import query_engines"`

### GATE 3 — Builder prompt
- [ ] `app/builder_prompt.py` : `compose_prompt(signal, engines_ctx)` → str
- [ ] Format [EVALUATE] avec contexte structuré
- Vérifié : `python3 -c "from app.builder_prompt import compose_prompt"`

### GATE 4 — PropositionEngine
- [ ] `app/engine.py` : `PropositionEngine.propose(request)` → Proposition
- [ ] dry_run mode : skip OpenClaw, retourne stub cohérent
- [ ] appel bridge via `OperatorBridge.send(BridgeRequest(action="evaluate", ...))`
- [ ] parse réponse OpenClaw → Proposition (fallback gracieux si parse échoue)
- Vérifié : `python3 -m app BTCUSDT BUY 65000 1h --dry-run`

### GATE 5 — Tests + sanity
- [ ] `tests/test_proposition.py` : ≥ 8 tests (schema, engines mock, prompt, dry-run, error cases)
- [ ] `scripts/sanity.sh` : structure + imports + dry-run smoke
- [ ] `scripts/cmd.sh` : propose/dry/sanity/test
- Vérifié : tous tests PASS, `scripts/cmd.sh sanity` PASS

## INVARIANTS

```text
NO_LIVE_TRADE — proposition_engine ne déclenche aucun trade
DRY_RUN_ALWAYS_SAFE — dry_run=True ne touche pas le gateway OpenClaw
PARSE_NEVER_CRASHES — si OpenClaw répond du texte non-parseable, retourne Proposition(action=HOLD, confidence=0, rationale=raw_text)
ENGINES_BEST_EFFORT — si un engine échoue, engines_context contient l'erreur mais propose() continue
```

## MACHINE

db-layer (même machine que operator_bridge + gateway)

## PRÉREQ VÉRIFIÉS

```text
openclaw_operator_bridge : MERGED ✓
signal_router             : MERGED ✓
decision_engine sample    : PASS ✓ (GO_LONG BTCUSDT, conf=0.85)
opportunity_ranker sample : PASS ✓ (score=0.71, priority=HIGH)
probability_engine sample : PASS ✓ (prob_long=0.72, conf=0.45)
```

## RISKS

- À qualifier.
