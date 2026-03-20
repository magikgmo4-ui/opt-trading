# Duplicates Audit

This audit focuses on overlap between `deepseek_hub`, `deepseek_student`, and `wrappers` inside `/opt/trading/student`.

## Findings

### 1. Command Layer Overlap

- canonical facade: `/opt/trading/student/scripts/student_cmd.sh`
- hub runtime command: `/opt/trading/student/scripts/deepseek_hub/deepseek_hub_cmd.sh`
- student helper command: `/opt/trading/student/scripts/deepseek_student/deepseek_student_cmd.sh`
- compatibility wrapper command: `/opt/trading/student/scripts/wrappers/deepseek_student_cmd.sh`

Assessment:

- `student_cmd.sh` is intentionally thin and should stay
- `deepseek_hub_cmd.sh` is the main operational engine today
- `deepseek_student/deepseek_student_cmd.sh` is a focused helper for `sanity`, `pull`, `test`, `roadmap`
- `wrappers/deepseek_student_cmd.sh` is a richer operator wrapper with status, timers, summary, roadmap helpers

Conclusion:

- there is functional overlap between `deepseek_student/deepseek_student_cmd.sh` and `wrappers/deepseek_student_cmd.sh`
- they should not both remain as peer primary entrypoints long term

Recommendation:

- keep `student_cmd.sh` as the only official facade
- keep `deepseek_hub_cmd.sh` as the internal engine
- keep `wrappers/deepseek_student_cmd.sh` as the surviving module-level operator convenience command
- classify `deepseek_student/deepseek_student_cmd.sh` as a narrow helper implementation used for focused module actions only

Decision:

- survivor for interactive module-level usage: `/opt/trading/student/scripts/wrappers/deepseek_student_cmd.sh`
- retained helper backend: `/opt/trading/student/scripts/deepseek_student/deepseek_student_cmd.sh`

### 2. Shortcut Installer Overlap

- `/opt/trading/student/bin/install_shortcuts.sh`
- `/opt/trading/student/scripts/deepseek_hub/install_shortcuts.sh`
- `/opt/trading/student/scripts/deepseek_student/install_shortcuts.sh`

Assessment:

- three installers exist with overlapping purpose
- only `bin/install_shortcuts.sh` matches the new canonical root cleanly

Recommendation:

- keep `/opt/trading/student/bin/install_shortcuts.sh` as the single official installer
- treat the two module installers as legacy/internal until refactored or retired

### 3. Sanity Layer Overlap

- `/opt/trading/student/scripts/student_sanity_check.sh`
- `/opt/trading/student/scripts/deepseek_hub/sanity_check_deepseek_hub.sh`
- `/opt/trading/student/scripts/deepseek_student/sanity_check.sh`
- `/opt/trading/student/scripts/deepseek_student/sanity_check_deepseek_student.sh`
- `/opt/trading/student/scripts/wrappers/deepseek_student_sanity_check.sh`

Assessment:

- multiple sanity layers exist for different scopes
- this is acceptable short term, but naming is crowded and potentially confusing

Recommendation:

- keep `student_sanity_check.sh` as the only top-level official sanity command
- document the others as internal or scoped checks

### 4. Menu Layer Overlap

- `/opt/trading/student/scripts/student_menu.sh`
- `/opt/trading/student/scripts/deepseek_hub/deepseek_hub_menu.sh`
- `/opt/trading/student/scripts/deepseek_student/menu.sh`
- `/opt/trading/student/scripts/wrappers/deepseek_student_menu.sh`
- `/opt/trading/student/scripts/wrappers/desk_pro_student_menu.sh`

Assessment:

- `student_menu.sh` currently delegates to the hub menu
- `deepseek_student/menu.sh` is more of a module wrapper menu
- wrapper menus remain valid but should not be mistaken for root entrypoints

Recommendation:

- keep one official top-level menu only
- reclassify wrapper menus by purpose in docs

## Priority Cleanup Targets

1. normalize installer ownership around `/opt/trading/student/bin/install_shortcuts.sh`
2. reduce direct operator exposure of `deepseek_student/deepseek_student_cmd.sh` now that `wrappers/deepseek_student_cmd.sh` is the chosen facade
3. document menu and sanity scopes so users stop calling the wrong layer

---

## Caller Audit — État 2026-03-20 (GO_STUDENT_CLEANUP_DUPLICATES_01)

> Vérification locale des appels actifs effectuée le 2026-03-20.
> Sources inspectées : `student/scripts/`, `student/bin/`, `opt-trading/modules/`, `opt-trading/scripts/student/`.

### Classification par niveau de risque

| Script doublon | Callers actifs trouvés dans `student/` | Callers actifs hors `student/` | Niveau de risque retrait | Décision |
|---|---|---|---|---|
| `deepseek_student/cmd.sh` | aucun caller externe (dispatcher interne vers `deepseek_student_cmd.sh`) | `modules/deepseek_student/scripts/cmd.sh` (legacy source upstream) | MOYEN — cmd.sh encore routé depuis legacy source | CONSERVER — helper interne, pas de shortcut global depuis `bin/` |
| `deepseek_student/deepseek_student_cmd.sh` | `deepseek_student/cmd.sh` (dispatch `roadmap\|pull\|test\|sanity`) | `modules/deepseek_hub/scripts/deepseek_hub_cmd.sh` via alias `cmd-deepseek_student` (global) | ÉLEVÉ — appelé indirectement via alias global si shortcut mal configuré | CONSERVER — backend narrow scope confirmé, supprimer uniquement après validation live que `cmd-deepseek_student` pointe vers `wrappers/` |
| `deepseek_student/sanity_check.sh` | aucun caller actif trouvé | aucun | FAIBLE | CONSERVER — structure check générique du module, inoffensif |
| `deepseek_student/sanity_check_deepseek_student.sh` | `deepseek_student/deepseek_student_cmd.sh` commande `sanity` | aucun | FAIBLE — appelé uniquement par le backend | CONSERVER — backend scope clair |
| `deepseek_student/menu.sh` | aucun caller actif trouvé dans `student/` | aucun | FAIBLE | CONSERVER — menu module générique, pas d'exposition globale |
| `scripts/deepseek_hub/install_shortcuts.sh` | aucun caller programmatique trouvé | aucun | FAIBLE — usage manuel uniquement | CONSERVER — marquer explicitement `legacy/internal` dans doc |
| `scripts/deepseek_student/install_shortcuts.sh` | aucun caller programmatique trouvé | aucun | FAIBLE — usage manuel uniquement | CONSERVER — marquer explicitement `legacy/internal` dans doc |

### Résultat principal

**Aucun retrait physique justifié dans cette passe.**

Le seul risque réel concerne `deepseek_student/deepseek_student_cmd.sh` :
- `modules/deepseek_hub/scripts/deepseek_hub_cmd.sh` appelle `cmd-deepseek_student roadmap` via l'alias global.
- Si cet alias pointe encore vers `modules/deepseek_student/scripts/cmd.sh` (legacy installer) plutôt que vers `student/scripts/wrappers/deepseek_student_cmd.sh` (canonical), la chaîne d'appel reste sur la couche legacy.
- **Vérification requise en live** : `readlink -f /usr/local/bin/cmd-deepseek_student`.

### Prochaine action sûre

Documenter les scopes dans `DUPLICATES_AUDIT.md` (cette section). Pas de suppression avant validation live.
