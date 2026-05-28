# GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_GAP_REMEDIATION_01

| Champ | Valeur |
|---|---|
| GO | `GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_GAP_REMEDIATION_01` |
| GO_STRUCTURAL_ROLE | GO_CHILD_ATTACHED_TO_PARENT |
| PF_ID | PF_GOVERNANCE_TRANSPORT |
| MASTER_TARGET_ID | MT_GOVERNANCE_PRODUCT_SURFACE_GAP_REMEDIATION |
| MASTER_PROJECT_PLAN_ID | MPP_GOVERNANCE_PRODUCT_SURFACE_GAP_REMEDIATION |
| PARENT_GO_ID | `GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_FINAL_REGISTRY_01` |
| Objet | Remédier les écats PF/MPP identifiés dans l'audit index sync |
| Base | `sot/mainline` |
| Branche | `go/GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_GAP_REMEDIATION_01` |

## 1_MASTER_TARGET

Appliquer les corrections structurelles identifiées dans l'audit `GO_OPT_TRADING_GOVERNANCE_CHILD_MASTER_PROJECT_PLAN_INDEX_SYNC_01` :

- Créer les parents PF manquants + leur MPP
- Rattacher les PF orphelins à un MPP
- Ne pas rouvrir les index globaux verrouillés (NEXT_GO_CANDIDATES, REPRISE)

## 4_MASTER_PROJECT_PLAN

### Gaps à traiter

| # | Gap | Action | Priorité |
|---|---|---|---|
| G1 | Parents PF absents : Telegram Screener, Telegram Ingestion, Perf Engine, Data Center | Créer parents + MPP | Haute |
| G2 | `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` non rattaché à MPP | Rattacher à MPP_STRICT_WORKERS_AI_TEAM ou créer MPP dédié | Moyenne |
| G3 | Parents machines listés sans PF P3 actif dans index | Garder en section hors pilotage | Basse |
| G4 | `PF_OPENCLAW_ORCHESTRATOR_FULL` parent en attente de child | Documenter statut PASS, pas de fermeture | Information |
| G5 | `PF_FIGMA_FINANCIAL_COCKPIT` TBD_DECISION | Reporter — pas de décision produit | Reporté |

### Gates

| Gate | Critère |
|---|---|
| Gate 1 | Chaque parent PF manquant (G1) a un GO d'ouverture créé ou planifié |
| Gate 2 | `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` rattaché à un MPP (G2) |
| Gate 3 | Parents machines listés mais sans PF P3 conservés en hors-pilotage (G3) |
| Gate 4 | Aucune modification des index globaux verrouillés (NEXT_GO_CANDIDATES, REPRISE) |
| Gate 5 | Aucun parent fermé par ce GO |
| Gate 6 | Patch doc-only, sans runtime |
| Gate 7 | FILE_SCOPE.txt ne couvre que les fichiers chantier + bundle (pas d'index globaux) |

## 6_FINAL_TARGET

À la fin du GO :

1. Chaque parent PF manquant a un GO d'ouverture créé (chantier + branche) ou un plan d'ouverture documenté
2. `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` est rattaché à un MPP
3. Les parents machines sans PF P3 actif sont documentés en hors-pilotage
4. Aucun fichier hors scope n'a été modifié

## 12_INVARIANTS

- Pas de fermeture de parent dans ce GO
- Pas de création de nouveau `PF_*`
- Pas de modification runtime
- Pas de modification de `GO_CLOSED_INDEX.md` ni `BRANCH_STATE.md`
- Pas de modification de `NEXT_GO_CANDIDATES.md` ni `REPRISE.md`
- Toute création de parent GO se fait via un GO d'ouverture dédié, pas dans ce GO

## 17_RESUME_POINT

```text
PRÉDÉCESSEUR = GO_OPT_TRADING_GOVERNANCE_CHILD_MASTER_PROJECT_PLAN_INDEX_SYNC_01 (mergé)
PROCHAINE_ÉTAPE = ouvrir GO Data Center, Telegram Screener, Telegram Ingestion, Perf Engine
```
