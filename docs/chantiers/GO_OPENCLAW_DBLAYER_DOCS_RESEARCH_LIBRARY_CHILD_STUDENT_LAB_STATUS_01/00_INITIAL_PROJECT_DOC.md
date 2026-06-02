---
doc_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_STUDENT_LAB_STATUS_01_INIT
doc_type: initial_project_doc
parent_go: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01
repo: opt-trading
go_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_STUDENT_LAB_STATUS_01
status: closed
created_at: 2026-05-30
---

# 00_INITIAL_PROJECT_DOC — Child Student Lab Status

## 1_MASTER_TARGET

Adresser GAP 6 : documenter le statut réel du lab OpenClaw sur student depuis
la perspective du parent research library — chemin E2E prouvé, limitations
connues, contraintes d'isolation, next step.

## 2_CONTEXT

```
GAP 6 (parent) — Student / lab OpenClaw encore séparé

État réel au 2026-05-30 :
  GO_WORKSPACE_SLIM_01       = CLOSED (90_CLOSEOUT.md présent)
  GO_OLLAMA_E2E_SMOKE_01     = CLOSED (90_CLOSEOUT.md présent)
  GO_WORKSPACE_SLIM_REALIGN_01 = verdict REALIGN (branches historiques trop divergentes)

  E2E path prouvé :
    OpenClaw agent → Gateway WebSocket 127.0.0.1:18790 → provider ollama
    → Ollama 127.0.0.1:11434 → deepseek-r1:1.5b → réponse reçue
    runId OK, status ok, durationMs 937

  Limitation bloquante :
    deepseek-r1:1.5b ne supporte pas le function calling (tools)
    OpenClaw envoie systématiquement des outils → réponse 400 tools not supported
    → non opérationnel en l'état

  Next GO recommandé (par GO_OLLAMA_E2E_SMOKE_01/50_LIMITS) :
    GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_MODEL_EVALUATION_01
    Objectif : identifier un modèle Ollama compatible function calling
```

## 3_SCOPE

- Doc-only — 0 runtime modifié
- Produit `docs/openclaw/student_lab/INDEX.md`
- Référence les GOs historiques student lab (3 GOs)
- Documente contraintes d'isolation + next step
- Met à jour `docs/openclaw/INDEX.md`

## 4_DELIVERABLES

| Fichier | Contenu |
| --- | --- |
| `FILE_SCOPE.txt` | Scope gate (présent dès J1) |
| `00_INITIAL_PROJECT_DOC.md` | Ce document |
| `docs/openclaw/student_lab/INDEX.md` | Statut lab, chemin prouvé, limites, next step |
| `docs/openclaw/INDEX.md` | student_lab/ ajouté aux surfaces |
| `20_ACCEPTANCE_REPORT.md` | Rapport PASS |

## 5_INVARIANTS

- 0 runtime modifié
- FILE_SCOPE.txt présent dès J1
- Student uniquement — pas db-layer, pas admin-trading
- Isolation préservée : port 18790, user openclaw-lab
- Parent non fermé
