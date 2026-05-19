---
doc_id: ADMIN_TRADING_MWS_UPDATE_10
doc_type: update_record
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_MACHINE_WORK_SPLIT_UPDATE_01
status: active
surface: chantier
updated_at: 2026-05-14
---

# 10_MACHINE_WORK_SPLIT_UPDATE — Patch appliqué

## Source

`docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md`, section `## Bloc ADMIN_TRADING` (lignes 132-160).

## Changement

Remplacement du bloc ADMIN_TRADING plat (25 entrées) par une version structurée avec sous-blocs et classification :

| Avant | Après |
| --- | --- |
| 1 bloc plat, 25 entrées | 7 sous-blocs, 61 entrées total |
| Aucune classification | ACTIVE / REFERENCE / DROP_MERGED / A_VERIFIER |
| Pas de TMUX_IDE | Sous-bloc TMUX_IDE dédié |
| 4 branches douteuses incluses sans note | A_VERIFIER explicite |

## Détail du patch

### Sous-blocs ajoutés

1. **Runtime actif** — branches en observation/pilotage runtime
2. **Desk Pro Automation** — séquence automation active
3. **Bridge & Vision Headless** — bridge guard + bot vision headless
4. **Paper Tests** — cycle paper test
5. **Production** — monitoring, risk limits, readiness
6. **Intégrations** — Telegram, TradingView, Webhook
7. **TMUX_IDE** — branches TMUX liées à admin-trading
8. **Parents** — parent branches
9. **Références** — merged/absorbed, documentation conservée
10. **DROP_MERGED** — merge candidates (cleanup après 2026-05-28)
11. **A_VERIFIER** — appartenance machine à confirmer

### Résolution de conflit

La classification `10_RECONCILIATION.md` listait 7 branches à la fois dans ACTIVE et DROP_MERGED. Résolution : ces 7 branches sont placées uniquement dans DROP_MERGED (elles sont absorbées dans mainline et n'ont plus d'activité propre).

### Branches retirées du bloc admin-trading

Aucune retirée. Les 4 branches A_VERIFIER sont conservées dans le bloc avec une note invitant à vérifier l'appartenance machine.

## Fichier modifié

`docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md` — section Bloc ADMIN_TRADING uniquement.
