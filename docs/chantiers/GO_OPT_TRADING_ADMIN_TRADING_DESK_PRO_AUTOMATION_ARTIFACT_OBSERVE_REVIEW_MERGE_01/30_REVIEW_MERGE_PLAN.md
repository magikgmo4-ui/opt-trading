---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_REVIEW_MERGE_01_30_REVIEW_MERGE_PLAN
doc_type: chantier/plan
repo: opt-trading
machine: cursor-ai
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_REVIEW_MERGE_01
status: active
scope: doc-only
updated_at: 2026-05-12
links:
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_REVIEW_MERGE_01/20_BRANCH_STACK_ANALYSIS.md
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_REVIEW_MERGE_01/40_SELECTED_DECISION.md
---

# 30_REVIEW_MERGE_PLAN

## PR a ouvrir

Ouvrir une PR vers `sot/mainline` avec :

```text
head: go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_STABILITY_WINDOW_01
base: sot/mainline
```

Titre recommande :

```text
feat: add admin-trading desk pro dry-run artifact output
```

## Pourquoi ce head

`STABILITY_WINDOW_01` est le head actif sur `admin-trading` et contient toute la sequence utile :

- implementation artifact output
- observation du trigger naturel
- observation de stabilite supplementaire

Merger seulement `OBSERVE_01` serait incomplet, car le commit `2908ff32` resterait non merge.

## Controle attendu dans la PR

Points a verifier pendant la revue :

- `.gitignore` limite bien le tracking de `runtime/`
- `modules/desk_pro/dry_run.py` ne declenche pas trade, webhook, Telegram ou systemd
- `modules/desk_pro/desk_pro_dry_run.sh` reste compatible avec l'execution timer existante
- `tests/test_desk_pro_artifact_output.py` couvre la production `latest.json`, `latest.md`, `history.jsonl`
- les closeouts `OBSERVE_01` et `STABILITY_WINDOW_01` confirment des effets de bord interdits absents

## Commandes de verification recommandees avant merge

```bash
PYTHONPATH=/opt/trading python -m pytest \
  tests/test_signal_event_adapter.py \
  tests/test_admin_trading_contract_compatibility_smoke.py \
  tests/test_desk_pro_dry_run.py \
  tests/test_desk_pro_artifact_output.py \
  -q
```

Si la PR est testee sur `cursor-ai`, adapter `PYTHONPATH` a la racine locale du depot.

## Apres merge

Ne pas reprendre `tmux-ide` directement.

Ouvrir un GO separe pour :

1. verifier que la PR desk-pro est mergee
2. basculer `admin-trading:/opt/trading` sur `sot/mainline`
3. tirer `origin/sot/mainline`
4. confirmer worktree clean
5. seulement ensuite relancer le cadrage `tmux-ide`

## RISKS

- À qualifier.
