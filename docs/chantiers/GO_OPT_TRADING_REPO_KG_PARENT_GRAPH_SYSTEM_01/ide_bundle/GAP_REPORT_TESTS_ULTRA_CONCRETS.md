# GAP_REPORT_TESTS_ULTRA_CONCRETS — Repo KG V1

GO_ID: GO_OPT_TRADING_REPO_KG_TESTS_ULTRA_CONCRETS_01
STATUS: OPEN
DATE: 2026-05-06

## GAP_01 — Branche en retard sur sot/mainline

**Severite**: LOW (doc-only, rattrapable)
**Description**: La branche `go/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01` ne contient pas les derniers merges mainline (ClickUp cockpit, apps plan). Les dossiers `GO_OPT_TRADING_CLICKUP_*` et `GO_OPT_TRADING_APPS_PARENT_VALIDATED_PLAN_01` sont absents.
**Action**: Rebaser ou realigner la branche sur `sot/mainline` avant merge.
**Impact**: Aucun fonctionnel (doc-only). Les schemas et specs restent valides.

## GAP_02 — Indexation non appliquee

**Severite**: LOW (pavee, prete)
**Description**: Le patch d'indexation dans `12_indexation_alignment_gap_and_patch.md` est specifie mais non applique a `GO_INDEX.md`, `BRANCH_STATE.md`, `REPRISE.md`.
**Action**: Appliquer le patch controle dans un commit separe.
**Impact**: Le Repo KG n'est pas encore reference dans les index canoniques.

## GAP_03 — Schema vs modules non mappes

**Severite**: MEDIUM (gap de couverture)
**Description**: 88 modules inventories mais le schema V1 ne liste pas explicitement chaque module. La structure de nodes MODULE couvre le concept mais le mapping reel reste a generer.
**Action**: Le Producer devra scanner les modules reels et generer les nodes dynamiquement (pas un mapping statique).
**Impact**: Le schema est generique, le Producer est prevu pour combler ce gap.

## GAP_04 — Branches non mappees

**Severite**: LOW
**Description**: 105 branches GO locales+remote. Le schema prevoit des nodes BRANCH et BRANCH_WORK_MAP. Le Producer devra scanner dynamiquement.
**Action**: Producer implemente le scan branches.
**Impact**: Couvert par Producer spec V1.

## GAP_05 — Acceptance tests formels non crees

**Severite**: LOW
**Description**: `10_acceptance_tests_v1.md` et `11_security_and_no_secret_policy.md` sont listes comme TODO dans SESSION_REPRISE.txt mais pas encore crees.
**Action**: Creer ces documents avant implementation Producer.
**Impact**: Bloque la phase d'acceptance formelle uniquement.

## GAP_06 — Bundle /bundles/ absent

**Severite**: LOW
**Description**: La surface `/bundles/` est absente du repo. Le bundle IDE est dans `docs/chantiers/.../ide_bundle/`.
**Action**: Documente dans `13_resume_note_bundles_surface_absent.md`. Migration vers `/bundles/` si GO dedie.
**Impact**: Aucun. Le bundle est accessible et fonctionnel.

## Resume

| GAP | Severite | Action |
| --- | --- | --- |
| 01 | LOW | Rebaser branche sur mainline |
| 02 | LOW | Appliquer patch indexation |
| 03 | MEDIUM | Producer scan dynamique modules |
| 04 | LOW | Producer scan dynamique branches |
| 05 | LOW | Creer acceptance tests |
| 06 | LOW | Non bloquant |

Aucun gap bloquant pour continuer.

## RISKS

- À qualifier.
