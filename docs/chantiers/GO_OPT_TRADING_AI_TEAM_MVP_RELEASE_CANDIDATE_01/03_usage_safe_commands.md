---
doc_id: GO_OPT_TRADING_AI_TEAM_MVP_RELEASE_CANDIDATE_01_USAGE_SAFE_COMMANDS
doc_type: runbook
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_AI_TEAM_MVP_RELEASE_CANDIDATE_01
status: open
lifecycle_stage: runbook
surface: chantier
source_kind: canonical
updated_at: 2026-05-05
---

# 03_USAGE_SAFE_COMMANDS — Commandes d'usage safe

## Pre-requis

```bash
cd /opt/trading
python3 --version  # >= 3.11
```

## Commandes safe (read-only ou write dans drafts/)

### READ_INVENTORY

```bash
python3 modules/ai_team_mvp/runner.py modules/ai_team_mvp/tasks/read_inventory.json
```

Scan des chantiers et GO_INDEX. Sortie stdout + `.observer_output_last.txt`. 0 git write.

### DOC_DRAFT

```bash
python3 modules/ai_team_mvp/runner.py modules/ai_team_mvp/tasks/observer_doc_draft.json
```

Produit un brouillon documentaire structure. Sortie dans `drafts/documenter_*.md`. Write limite a `drafts/`.

### ANALYZE_INVENTORY

```bash
# D'abord sauver l'output Observer
python3 modules/ai_team_mvp/runner.py modules/ai_team_mvp/tasks/read_inventory.json \
  2>&1 | tee modules/ai_team_mvp/drafts/.observer_output_last.txt > /dev/null

# Puis lancer l'analyse
python3 modules/ai_team_mvp/runner.py modules/ai_team_mvp/tasks/analyze_inventory.json
```

Classifie les chantiers par domaine et statut. Sortie dans `drafts/analyzer_*.md`.

### PATCH_DRAFT

```bash
python3 modules/ai_team_mvp/runner.py modules/ai_team_mvp/tasks/patch_draft.json
```

Produit une PROPOSITION de patch (NEVER applied). Sortie dans `drafts/patches/analyzer_patch_draft_*.md`.

### ORCHESTRATOR_CHAIN (3 etapes)

```bash
python3 modules/ai_team_mvp/runner.py modules/ai_team_mvp/tasks/orchestrator_chain_v2.json
```

Execute sequentiellement : READ_INVENTORY → ANALYZE_INVENTORY → DOC_DRAFT. Arret au premier echec.

## Commandes de verification

```bash
# Verifier qu'aucun git write n'a eu lieu
git diff --stat

# Verifier que le fichier cible PATCH_DRAFT n'est pas modifie
md5sum modules/ai_team_mvp/README.md

# Lister les sorties
ls modules/ai_team_mvp/drafts/
ls modules/ai_team_mvp/drafts/patches/

# Valider les registres JSON
python3 -c "import json; json.load(open('modules/ai_team_mvp/registry/workers.registry.json')); print('workers OK')"
python3 -c "import json; json.load(open('modules/ai_team_mvp/registry/tasks.registry.json')); print('tasks OK')"
python3 -c "import json; json.load(open('modules/ai_team_mvp/registry/outputs.registry.json')); print('outputs OK')"
```

## Commandes interdites (jamais via le runner)

```bash
# Ces commandes ne doivent JAMAIS etre executees par ou depuis le runner :
git add, git commit, git push, git rebase, git merge
git diff, git apply, patch
rm -rf, chmod -R, chown -R
```

## Ajout d'un nouveau task packet

1. Creer le fichier `<task_id>.json` dans `modules/ai_team_mvp/tasks/`.
2. Respecter le contrat Strict Workers (no_secrets, no_git_write, DRAFT_ONLY, etc.).
3. Ajouter le handler dans `runner.py` si nouveau task_type.
4. Ajouter l'entree dans `tasks.registry.json`.
5. Executer le smoke.
6. Mettre a jour `outputs.registry.json`.
7. Documenter dans le chantier GO approprie.

## Reprise apres interruption

```bash
# 1. Verifier l'etat du runner
python3 -c "from modules.ai_team_mvp.runner import TASK_HANDLERS; print(list(TASK_HANDLERS.keys()))"

# 2. Verifier les registres
python3 -c "import json; d=json.load(open('modules/ai_team_mvp/registry/tasks.registry.json')); print([t['task_type'] for t in d['tasks']])"

# 3. Relancer la tache souhaitee
python3 modules/ai_team_mvp/runner.py modules/ai_team_mvp/tasks/<task>.json
```
