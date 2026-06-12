---
doc_id: GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01_10_SOURCE_STATE
doc_type: chantier/source_state
repo: opt-trading
machine: cursor-ai
go_id: GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01
status: active
scope: doc-only
snapshot_date: 2026-05-09
links:
  - docs/index/REPRISE.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/BRANCH_STATE.md
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_PROMPT_01/70_FINAL_PROMPT.md
---

# 10_SOURCE_STATE

## État canonique du repo au moment du run

### Branche canonique

- `sot/mainline`
- HEAD : `9123687` (Merge pull request #267 from GO_OPT_TRADING_DOC_OPS_WHY_MARKDOWN_PARSER_01)
- PR #266 mergée : GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_PROMPT_01 ✓
- PR #267 mergée : GO_OPT_TRADING_DOC_OPS_WHY_MARKDOWN_PARSER_01 ✓

### Branche de travail

- `go/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01`
- Créée depuis `sot/mainline` le 2026-05-09
- Preuve : `git branch --show-current` retourne la branche attendue (ETAT_VERIFIE — session active)

### Résumé du parc branches (ETAT_DECLARE)

Source : `docs/index/BRANCH_STATE.md` (updated_at: 2026-04-28)

- Branches remote : 55 (déclaré)
- Branches locales : 36 (déclaré)
- Entrées suivies dans le tableau : 72
- Branches non mergées dans `sot/mainline` : 129 (mesuré live via `git branch -r --no-merged`)
- Dont branches go/ hors admin : 68 non mergées (mesuré live)

> Note : l'écart entre 55 déclarées dans BRANCH_STATE.md (2026-04-28) et 129 non-mergées mesurées live indique que BRANCH_STATE.md peut être partiel ou que le périmètre de comptage diffère. Classé HYPOTHESE.

### Sources lues lors du run

| Source | Type de preuve | Statut |
| --- | --- | --- |
| `docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_PROMPT_01/70_FINAL_PROMPT.md` | Lecture directe | ETAT_VERIFIE |
| `docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_PROMPT_01/20_ATTENTION_CENTER_SPEC.md` | Lecture directe | ETAT_VERIFIE |
| `docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_PROMPT_01/30_READONLY_SOURCES_MATRIX.md` | Lecture directe | ETAT_VERIFIE |
| `docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_PROMPT_01/40_SCORING_P0_P1_P2.md` | Lecture directe | ETAT_VERIFIE |
| `docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_PROMPT_01/50_MACHINE_STATE_RULES.md` | Lecture directe | ETAT_VERIFIE |
| `docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_PROMPT_01/60_EXPORT_FORMAT.md` | Lecture directe | ETAT_VERIFIE |
| `bundles/claude-artifacts/README.md` | Lecture directe | ETAT_VERIFIE |
| `bundles/claude-artifacts/NO_COMMIT_RULES.md` | Lecture directe | ETAT_VERIFIE |
| `bundles/claude-artifacts/CHECKLIST_EXECUTION.md` | Lecture directe | ETAT_VERIFIE |
| `docs/index/ACTIVE_STREAMS.md` | Lecture directe | ETAT_VERIFIE |
| `docs/index/REPRISE.md` | Lecture directe | ETAT_VERIFIE |
| `docs/index/NEXT_GO_CANDIDATES.md` | Lecture directe | ETAT_VERIFIE |
| `docs/index/BRANCH_STATE.md` | Lecture directe | ETAT_VERIFIE |
| `git log --oneline -10 sot/mainline` | Commande live | ETAT_VERIFIE |
| `git branch -r --no-merged origin/sot/mainline` | Commande live | ETAT_VERIFIE |

### Sources NON lues lors de ce run

- GitHub PR / branches via API : connecteur GitHub non activé dans cette session — ETAT_DECLARE depuis les docs seulement
- Google Drive : non connecté — hors scope
- Calendar : non connecté — hors scope
- Asana / ClickUp : non connecté — hors scope
- `reports/` : répertoire non présent ou vide dans ce run — non vérifié
- Snapshot repo read-only dédié : non configuré — le repo actif est utilisé en lecture seule par convention

### Conformité read-only

Mode read-only respecté : aucun fichier modifié hors `docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01/` et `docs/index/inbox/`.

## RISKS

- À qualifier.
