---
doc_id: GO_OPT_TRADING_AI_TEAM_SETUP_MVP_01_SMOKE_PLAN
doc_type: spec
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_AI_TEAM_SETUP_MVP_01
status: open
lifecycle_stage: spec
surface: chantier
source_kind: canonical
updated_at: 2026-05-05
links:
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CANON_01/01_architecture_cible.md
  - modules/ai_team_mvp/runner.py
  - modules/ai_team_mvp/tasks/read_inventory.json
---

# 03_SMOKE_PLAN — Smoke READ_INVENTORY

## Objectif

Prouver que le runner read-only fonctionne, que le contrat Strict Workers est respecte, et que la sortie DRAFT_ONLY est exploitable.

## Preconditions

- Runner `modules/ai_team_mvp/runner.py` executable
- Task packet `modules/ai_team_mvp/tasks/read_inventory.json` valide
- Aucun fichier sensible touche
- Aucune operation Git executee

## Etapes du smoke

### 1. Validation task packet

Verifier que `read_inventory.json` est syntaxiquement valide et contient les champs requis :

```bash
python3 -c "import json; d=json.load(open('modules/ai_team_mvp/tasks/read_inventory.json')); print('OK:', d['task_id'])"
```

### 2. Execution runner (dry-run)

```bash
cd /opt/trading && python3 modules/ai_team_mvp/runner.py tasks/read_inventory.json
```

### 3. Verification sortie

- La sortie contient les sections `13_ESTABLISHED`, `14_HYPOTHESIS`, `15_REMAINING_GAP`, `16_TODO`, `VERDICT_DRAFT_ONLY`
- La sortie liste au moins un chantier actif
- La sortie contient le statut DRAFT_ONLY explicite

### 4. Verification non-regression

```bash
git diff --stat   # doit etre vide (aucune ecriture)
find . -name ".env" -newer modules/ai_team_mvp/runner.py  # doit etre vide
```

### 5. Verification denied_inputs

Le runner ne doit avoir lu aucun fichier correspondant aux denied_inputs patterns.

## Criteres de reussite

| Critere | Seuil |
|:--------|:------|
| Runner s'execute sans erreur | OBLIGATOIRE |
| Sortie au format DRAFT_ONLY | OBLIGATOIRE |
| 13_ESTABLISHED present et non vide | OBLIGATOIRE |
| VERDICT_DRAFT_ONLY explicite | OBLIGATOIRE |
| Aucun git write | OBLIGATOIRE |
| Aucun denied_input lu | OBLIGATOIRE |
| Au moins 1 chantier listé | SOUHAITE |

## Verdict attendu

PASS si tous les criteres OBLIGATOIRES sont satisfaits.
FAIL sinon, avec gap documente.
