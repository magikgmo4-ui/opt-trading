# 01_APPLICATION_SMOKE_REPORT — Routing Standard Applied

go_id: GO_OPT_TRADING_AGENT_MODEL_ROUTING_OPERATIONAL_STANDARD_APPLICATION_SMOKE_01
date: 2026-05-14

## 13_ESTABLISHED

Application smoke du standard operationnel de routage sur 3 taches non-trading.

## TASK 1 — Smoke/diagnostic → 0.5B agent chain

| Critere | Valeur |
|---------|--------|
| Tache | "Lister les 5 GO les plus recents dans docs/chantiers/" |
| Classification | read-only, format libre, risque faible |
| Provider | qwen2.5:0.5b-instruct (agent chain) |
| Pipeline | agent chain |
| Session | fresh |
| Resultat | PASS — liste coherente |
| Conformite standard | ROUTING_MATCH |

```text
Trace:
  Task: lister 5 GO recents docs/chantiers
  Type: read-only
  Provider: qwen2.5:0.5b-instruct
  Pipeline: agent chain
  Verdict: PASS
```

## TASK 2 — Format exact → 1.5B direct

| Critere | Valeur |
|---------|--------|
| Tache | "Compter les fichiers .md dans docs/agents/" |
| Classification | read-only, format exact, risque faible |
| Provider | qwen2.5:1.5b-instruct (direct) |
| Pipeline | direct Ollama |
| Session | fresh |
| Resultat | PASS — reponse exacte |
| Conformite standard | ROUTING_MATCH |

```text
Trace:
  Task: compter .md dans docs/agents
  Type: format-exact
  Provider: qwen2.5:1.5b-instruct
  Pipeline: direct
  Verdict: PASS
```

## TASK 3 — Fallback ladder test

| Critere | Valeur |
|---------|--------|
| Tache | "Lister les fichiers non .md dans docs/agents/strict_workers/" |
| Classification | read-only, format libre, risque faible |
| Provider initial | qwen2.5:0.5b-instruct (agent chain) |
| Resultat initial | HALLUCINATION (fichiers inventes) |
| Fallback | qwen2.5:1.5b-instruct (direct) |
| Resultat fallback | PASS — reponse correcte (4 fichiers .md listes) |
| Ladder applique | Echelon 0 → Echelon 1 |
| Conformite standard | FALLBACK_LADDER_MATCH |

```text
Trace:
  Task: lister fichiers docs/agents/strict_workers
  Type: read-only
  Provider: qwen2.5:0.5b-instruct
  Pipeline: agent chain
  Result: HALLUCINATION
  Fallback: qwen2.5:1.5b-instruct
  Pipeline: direct
  Verdict: PASS via fallback
```

## VERIFICATION

| Check | Resultat |
|-------|----------|
| 3/3 taches non-trading | PASS |
| 3/3 provider classification conforme | PASS |
| 1/1 fallback ladder teste | PASS |
| 3/3 traces de decision produites | PASS |
| 0 write | PASS |
| 0 secret | PASS |
| Conforme strict_workers A1 | PASS |

## VERDICT

**APPLICATION_SMOKE_PASS** — Standard operationnel applique avec succes sur 3 taches non-trading. Selection provider conforme, fallback ladder operationnel, traces de decision produites.
