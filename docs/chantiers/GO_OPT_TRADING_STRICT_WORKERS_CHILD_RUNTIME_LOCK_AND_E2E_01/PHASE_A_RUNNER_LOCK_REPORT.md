---
doc_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_RUNTIME_LOCK_AND_E2E_01_PHASE_A_REPORT
doc_type: phase_report
repo: opt-trading
project: opt-trading
module: agents
go_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_RUNTIME_LOCK_AND_E2E_01
parent_go_id: GO_OPT_TRADING_STRICT_WORKERS_PARENT_01
machine: fantome
status: pass_phase_a
lifecycle_stage: phase_a_complete
topic_keys:
  - strict_workers
  - runner_lock
  - phase_a
surface: docs/chantiers
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_RUNTIME_LOCK_AND_E2E_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "Phase A PASS — runner verrouille, pret pour Phase B PATCH_DRAFT"
updated_at: 2026-05-13
links:
  - docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_RUNTIME_LOCK_AND_E2E_01/00_INITIAL_PROJECT_DOC.md
  - scripts/ai/workers/run_task.sh
  - scripts/ai/workers/_validate_job.py
  - scripts/ai/workers/tasks.index.json
  - scripts/ai/workers/models.registry.json
---

# Phase A Report — Runner Lock

## Verdict

**PASS** — Runner strict_workers verrouille, operationnel, valide contre smoke READ_INVENTORY.

## Livrables

| Fichier | SHA (dernier) | Role |
| --- | --- | --- |
| `scripts/ai/workers/run_task.sh` | `39c2553` | Runner principal — charge job packet, valide, produit prompt structure |
| `scripts/ai/workers/_validate_job.py` | `39c2553` | Validateur Python — regles metier (tasks.index, models.registry, scope, denied patterns) |

## Fonctionnement

```text
run_task.sh <job_packet.json>
  ↓
git status clean check
  ↓
_validate_job.py → valide contre tasks.index.json + models.registry.json
  ↓
PASS → produit PROMPT structure (denied_commands, denied_inputs, invariants)
FAIL → produit FAILED report, exit 1
  ↓
Le prompt est pret a etre envoye au worker model
```

## Tests

### Test 1 — Smoke READ_INVENTORY (valide)

| Element | Resultat |
| --- | --- |
| Job packet | `GO_STRICT_WORKERS_READONLY_SMOKE_01.json` |
| Validation | **PASS** |
| Worker route | qwen3.5-plus (VERIFIED) |
| Valid workers | big-pickle, gpt-5-nano, kimi-k2.5, minimax-m2.5, qwen3.5-plus |
| Prompt genere | `reports/ai/workers/GO_STRICT_WORKERS_READONLY_SMOKE_01_PROMPT.txt` (69 lignes) |
| Garde-fous affiches | denied_commands (8), denied_inputs (9), global_invariants (7) |

### Test 2 — Job invalide (negatif)

| Erreur detectee | Description |
| --- | --- |
| UNKNOWN_TASK_TYPE | `NONEXISTENT_TASK` non present dans tasks.index.json |
| NO_VERIFIED_WORKER | `unknown-model` absent du registry VERIFIED |
| DEFAULT_WORKER_NOT_VERIFIED | `unknown-model` non VERIFIED |
| INPUT_NOT_FOUND | `.env` inexistant |
| DENIED_INPUT | `.env` match denied pattern `.env` |
| OUTPUT_NOT_ALLOWED | Sortie non autorisee dans `/etc/passwd` |
| **Total** | **6 erreurs detectees, 0 faux negatifs** |

## Garde-fous actifs

| Mecanisme | Description |
| --- | --- |
| Git clean check | Bloque si `git diff` ou `git status --porcelain` non vide |
| Timeout | 120s max par job |
| tasks.index.json | Valide task_type, required_sections, denied_commands/inputs |
| models.registry.json | Seuls les modeles VERIFIED autorises |
| Scope allowed_inputs | Verifie existence + absence de denied patterns |
| Scope allowed_outputs | Verifie que la sortie est dans le perimetre autorise |
| Sorties | DRAFT_ONLY obligatoire, 500 lignes max |
| Aucun write runtime | Le runner ne modifie jamais le repo |

## Limites (hors scope Phase A)

- Le runner produit un PROMPT, pas une execution automatisee
- Le worker model doit etre appele manuellement ou via un orchestrateur externe
- Pas de sandboxing process (le modele s'execute dans OpenCode, qui a ses propres garde-fous)
- Pas de verification post-execution automatique (a faire en Phase B/C)

## NEXT

Phase B — PATCH_DRAFT borne : creer un job packet PATCH_DRAFT, le router via le runner vers glm-5.1, produire un patch DRAFT_ONLY non applique.

## RISKS

- À qualifier.
