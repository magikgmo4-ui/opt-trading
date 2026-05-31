---
doc_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_FLEET_MATRIX_01_INIT
doc_type: initial_project_doc
parent_go: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01
repo: opt-trading
go_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_FLEET_MATRIX_01
status: open
created_at: 2026-05-30
---

# 00_INITIAL_PROJECT_DOC — Child Fleet Matrix

## 1_MASTER_TARGET

Adresser GAP 5 : produire une vue unifiée `docs/openclaw/fleet/` de la fleet
depuis la perspective OpenClaw — statut par machine, preuves runtime, rôle
dans l'orchestration, gaps restants (dont mobile NOT_PROVEN).

## 2_CONTEXT

```
GAP 5 (parent) — Fleet / machines pas complètement prouvées

État réel au 2026-05-30 (sources : runtime_health + mémoire session) :
  admin-trading  = WARN EXPECTED  — service/timer optionnels, classifiés
  db-layer       = WARN EXPECTED  — hôte OpenClaw gateway (18789)
  cursor-ai      = PASS/healthy   — Windows/SSH (PR #592/#595/#600)
  fantome        = PASS 12/12     — (PR #589/#590)
  student        = WARN EXPECTED  — Ollama lab, WARN classifiés
  mobile         = NOT_PROVEN     — Termux, aucune preuve runtime OpenClaw
```

`GO_OPT_TRADING_RUNTIME_HEALTH_FLEET_WARN_CLASSIFICATION_01` = CLOSED.
Warn classification déjà faite. Manque : vue OpenClaw + mobile documenté.

## 3_SCOPE

- Doc-only — 0 runtime modifié
- Produit `docs/openclaw/fleet/INDEX.md`
- Référence les preuves existantes (runtime_health GOs)
- Documente mobile NOT_PROVEN avec conditions de fermeture
- Met à jour `docs/openclaw/INDEX.md`

## 4_DELIVERABLES

| Fichier | Contenu |
| --- | --- |
| `FILE_SCOPE.txt` | Scope gate (présent dès J1) |
| `00_INITIAL_PROJECT_DOC.md` | Ce document |
| `docs/openclaw/fleet/INDEX.md` | Matrice fleet OpenClaw (6 machines) |
| `docs/openclaw/INDEX.md` | fleet/ ajouté aux surfaces |
| `20_ACCEPTANCE_REPORT.md` | Rapport PASS |

## 5_INVARIANTS

- 0 runtime modifié
- FILE_SCOPE.txt présent dès le premier commit
- Parent non fermé
- Index globaux non touchés
