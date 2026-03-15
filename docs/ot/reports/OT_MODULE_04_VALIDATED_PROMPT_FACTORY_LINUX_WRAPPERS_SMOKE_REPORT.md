# OT-MODULE-04 — VALIDATED_PROMPT_FACTORY (LINUX WRAPPERS SMOKE) — REPORT

Date (America/Montreal) : 2026-03-14

## 1. RÉSUMÉ EXÉCUTIF
- Smoke exécuté sur wrappers bash du module (`cmd.sh`, `sanity.sh`) via bash Git for Windows (MSYS).
- WSL (Linux) non disponible sur ce poste (aucune distribution installée) : smoke “Linux cible” reste à confirmer.
- Aucune correction code requise pour le smoke proxy ; doc minimale ajustée pour expliciter la différence.

## 2. ENVIRONNEMENT RÉEL DE SMOKE
### ÉTABLI
- Poste : Windows (repo local `C:\Users\ghost\opt-trading`)
- Bash utilisé : `C:\Program Files\Git\usr\bin\bash.exe`
  - `GNU bash, version 5.2.37(1)-release (x86_64-pc-msys)`

### À CONFIRMER
- Linux cible : non testé (WSL sans distribution ; pas d’accès Linux distant dans ce smoke).

## 3. COMMANDES EXÉCUTÉES (WRAPPERS)
Exécutées depuis `modules/validated_prompt_factory/` via :
- `& 'C:\Program Files\Git\usr\bin\bash.exe' -lc '<cmd>'`

1) `./cmd.sh list-modes`
2) `./cmd.sh generate trae_patch inputs/synthesis_registry_central.txt`
3) `./cmd.sh generate bundle_transfer inputs/synthesis_bundle_transfer.txt`
4) `./sanity.sh`

## 4. RÉSULTATS OBSERVÉS
### ÉTABLI
- `list-modes` retourne les 4 modes attendus.
- `generate trae_patch` génère `output/prompt_trae_patch.txt`.
- `generate bundle_transfer` génère `output/prompt_bundle_transfer.txt`.
- `sanity.sh` passe (help + génération + échec attendu).

### À CONFIRMER
- `menu.sh` : non testé (interactif).
- Exécution sur Linux cible + wrappers `/usr/local/bin` : non testé.

## 5. ÉCARTS PROUVÉS ET CORRECTIONS APPLIQUÉES
### ÉCART
- Linux cible non disponible sur ce poste : impossibilité de prouver “wrappers Linux” au sens strict.

### CORRECTION (MINIMALE)
- README : ajout d’un encadré “Smoke wrappers (Linux)” pour éviter toute ambiguïté.

## 6. FICHIERS MODIFIÉS
- `modules/validated_prompt_factory/README.md`
- `opt_trading_kanban_source_of_truth_2026-03-13_updated.md`
- `OT_MODULE_04_VALIDATED_PROMPT_FACTORY_LINUX_WRAPPERS_SMOKE_REPORT.md`
- `OT_MODULE_04_VALIDATED_PROMPT_FACTORY_LINUX_WRAPPERS_SMOKE_GAP_REPORT.md`
- `OT_MODULE_04_VALIDATED_PROMPT_FACTORY_LINUX_WRAPPERS_SMOKE_CLOSING.txt`

## 7. POINT DE REPRISE EXACT
> **GO_OT_MODULE_04B_VALIDATED_PROMPT_FACTORY_LINUX_TARGET_SMOKE**

