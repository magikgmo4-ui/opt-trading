# Commit Transfer Inventory

## Etabli

- branche source analysee : `origin/go/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01`
- base canonique : `origin/sot/mainline`
- methode source : `docs/chantiers/GO_OPT_TRADING_DOC_OPS_BRANCH_ARBITRATION_EXECUTION_01/06_commit_transfer_inventory.md` via `f7ea0b46`
- statut de comparaison releve :
  - `ahead = 11`
  - `behind = 191`
- decision directrice : **ne pas merger aveuglement la branche parent**

## Commits source utiles

| Commit | Type | Fichiers touches | Risque | Transfert recommande | Decision |
| --- | --- | --- | --- | --- | --- |
| `26446c7` | docs parent | `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/00_PARENT_CADRAGE.md` | low | `import-file` | `integrer` |
| `fe0de1f` | docs parent | `.../01_SYNTHESE_OLLAMA_LOCAL.md` | low | `import-file` | `integrer` |
| `6f70668` | docs parent | `.../02_MACHINE_QUALIFICATION_PLAN.md` | low | `import-file` | `integrer` |
| `e75ca74` | docs parent | `.../03_SECURITY_BASELINE.md` | low | `import-file` | `integrer` |
| `bea2aff` | docs parent | `.../04_INTEGRATION_MAP.md` | low | `import-file` | `integrer` |
| `9fe2042` | docs parent | `.../05_INFRA_RANKING_AND_USAGE.md` | low | `import-file` | `integrer` |
| `773a39f` | docs parent | `.../06_DECISION_LAB_STUDENT_OPENCLAW_ORCHESTRATION.md` | low | `import-file` | `integrer` |
| `71eec9a` | docs parent | `.../07_LAB_USAGE_SCOPE.md` | low | `import-file` | `integrer` |
| `718bf9d` | checkpoint | `.../90_PARENT_CHECKPOINT.md` | low | `import-file` | `integrer` |
| `d4c4693` | index global | `docs/index/BRANCH_STATE.md` | high | `manual` | `rejeter comme import direct` |
| `367458e` | index local de branche | `docs/index/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01_INDEX_ENTRY.md` | medium | `reference-only` | `differer` |

## Fichiers presents sur la branche parent

### A transferer comme socle parent utile

- `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/00_PARENT_CADRAGE.md`
- `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/01_SYNTHESE_OLLAMA_LOCAL.md`
- `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/02_MACHINE_QUALIFICATION_PLAN.md`
- `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/03_SECURITY_BASELINE.md`
- `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/04_INTEGRATION_MAP.md`
- `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/05_INFRA_RANKING_AND_USAGE.md`
- `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/06_DECISION_LAB_STUDENT_OPENCLAW_ORCHESTRATION.md`
- `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/07_LAB_USAGE_SCOPE.md`
- `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/90_PARENT_CHECKPOINT.md`

### A ignorer comme transfert aveugle

- `docs/index/BRANCH_STATE.md`
- `docs/index/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01_INDEX_ENTRY.md`

## Preuves externes utiles a importer manuellement

- `6572ae8` (`GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01`)
  - utile pour rattacher `student` au parent avec preuves runtime reelles
  - **a importer comme faits**, pas comme merge de dossier child

## Raisons

- la branche parent prouve correctement le dossier `Local Ollama`
- elle est en revanche fortement en retard sur `sot/mainline`
- elle ne porte pas les surfaces canoniques courantes `GO_CLOSED_INDEX.md` et `GO_PARENT_THREAD_MAP.md`
- son `BRANCH_STATE.md` ne doit donc pas etre reintroduit aveuglement dans la ligne canonique courante

## Risques

- merge global de la branche = risque eleve de regression documentaire des index globaux
- import direct de `BRANCH_STATE.md` = risque de perdre des decisions de classement plus recentes
- import direct de `GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01_INDEX_ENTRY.md` = risque de dupliquer ou contourner les surfaces canoniques actuelles

## Decision de transfert

- **integrer** le socle parent `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/*`
- **differer** l'index entry de branche comme simple reference locale
- **rejeter** tout merge aveugle des index globaux
- **importer manuellement** les faits du child `6572ae8` dans les nouveaux documents du parent
