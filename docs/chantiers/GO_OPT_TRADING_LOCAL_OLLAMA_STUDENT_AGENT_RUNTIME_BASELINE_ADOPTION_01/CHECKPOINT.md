# CHECKPOINT

GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_RUNTIME_BASELINE_ADOPTION_01

## État

Chaîne Student/Ollama complet : **FULL_PASS**

| Segment | Verdict |
|---------|:-------:|
| Provider local CPU | PASS |
| Smoke canonique | PASS |
| Politique rétention | MERGED |
| Enforcement scripts | MERGED |
| Smoke post-purge | PASS |
| Baseline adoption | DRAFT |

## Règles d'adoption figées

1. Runtime local = `qwen2.5:0.5b-instruct` via Ollama
2. Session fraîche obligatoire pour smoke fiable
3. Rotation après 10 runs ou 7 jours ou PROMPT_ERROR
4. Prewarm recommandé avant chaque utilisation
5. Cold smoke ~52-60s, warm smoke ~5-10s
6. n_ctx=4096 → ~600 tokens d'historique maximum

## Liens

- Baseline: `RUNTIME_BASELINE_ADOPTION_01.md`
- Runbook: `RUNBOOK_AGENT_STARTUP_WITH_SESSION_GUARDS_01.md`
