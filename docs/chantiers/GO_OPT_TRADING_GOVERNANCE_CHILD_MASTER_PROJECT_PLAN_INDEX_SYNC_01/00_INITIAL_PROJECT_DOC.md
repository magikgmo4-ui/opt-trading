# GO_OPT_TRADING_GOVERNANCE_CHILD_MASTER_PROJECT_PLAN_INDEX_SYNC_01

| Champ | Valeur |
|---|---|
| GO | `GO_OPT_TRADING_GOVERNANCE_CHILD_MASTER_PROJECT_PLAN_INDEX_SYNC_01` |
| GO_STRUCTURAL_ROLE | GO_CHILD_ATTACHED_TO_PARENT |
| PF_ID | PF_GOVERNANCE_TRANSPORT |
| MASTER_TARGET_ID | MT_GOVERNANCE_MASTER_PROJECT_PLAN_INDEX_SYNC |
| MASTER_PROJECT_PLAN_ID | MPP_GOVERNANCE_MASTER_PROJECT_PLAN_INDEX |
| PARENT_GO_ID | `GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_FINAL_REGISTRY_01` |
| Objet | Synchroniser les index globaux comme MASTER_PROJECT_PLAN_INDEX cohérent |
| Base | `sot/mainline` |
| Branche | `go/GO_OPT_TRADING_GOVERNANCE_CHILD_MASTER_PROJECT_PLAN_INDEX_SYNC_01` |

## 1_MASTER_TARGET

Les index globaux doivent être lus comme `MASTER_PROJECT_PLAN_INDEX` :

```
PF_* -> 1_MASTER_TARGET -> 4_MASTER_PROJECT_PLAN -> parent de continuité -> child/bundle -> NEXT_GO / CLOSE_GATE
```

## 4_MASTER_PROJECT_PLAN

### Phases

| Phase | Action |
|---|---|
| A | Lecture / audit des documents sources |
| B | Création dossier chantier |
| C | Patch des index globaux si divergence |
| D | Production tables MASTER_PROJECT_PLAN_INDEX |
| E | Bundle target + closeout |

### Gates

| Gate | Critère |
|---|---|
| Gate 1 | `PRODUCT_FINAL_SURFACE_REGISTRY_01.md` reste source PF de référence |
| Gate 2 | `GO_INDEX.md` contient section MASTER_PROJECT_PLAN_INDEX cohérente |
| Gate 3 | `ACTIVE_STREAMS.md` reflète flux actifs par PF/MPP |
| Gate 4 | `NEXT_GO_CANDIDATES.md` expose next primaire global + next par PF |
| Gate 5 | `REPRISE.md` indique point de reprise opérationnel |
| Gate 6 | Chantiers hors PF listés séparément |
| Gate 7 | Aucun parent fermé par ce patch |
| Gate 8 | Patch doc-only, sans runtime |

## 6_FINAL_TARGET

À la fin du GO, on doit pouvoir ouvrir le repo et comprendre :

1. quelles surfaces `PF_*` existent
2. quel `MASTER_PROJECT_PLAN_ID` porte chacune
3. quel parent de continuité est actif, à créer ou à fermer
4. quel next GO primaire est recommandé
5. quels chantiers sont hors pilotage immédiat

## 12_INVARIANTS

- Pas de fermeture de parent dans ce GO
- Pas de création de nouveau `PF_*`
- Pas de modification runtime
- Pas de modification de `GO_CLOSED_INDEX.md` ni `BRANCH_STATE.md`
- Index mis à jour seulement si divergence réelle

## 17_RESUME_POINT

```text
docs/index/NEXT_GO_CANDIDATES.md → NEXT_GO primaire global:
GO_OPT_TRADING_GOVERNANCE_CHILD_MASTER_PROJECT_PLAN_INDEX_SYNC_01
```
