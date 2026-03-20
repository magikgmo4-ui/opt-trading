# CROSS TOPOLOGY CANON — CARTE MINIMALE TRANSVERSE

Date : 2026-03-20
Branche : `audit/opt-trading-20260320a`
Mission : `GO_CROSS_TOPLOGY_CANON_01`

## 1. Rôle
Ce document fixe une carte canonique minimale transverse du périmètre pour éviter toute confusion entre :
- repo/branche
- sous-projet intégré
- module
- machine/runtime
- projet séparé
- hors bundle

## 2. Tableau canonique transverse

| Périmètre | Classification | Support canonique de référence | Statut | Usage / rôle | Point de reprise suivant |
|---|---|---|---|---|---|
| `opt-trading / sot/mainline` | repo/branche | `opt-trading / sot/mainline` | CANONIQUE / ACTIF | pivot principal de lecture, reprise et décision | `GO_CROSS_TOPLOGY_CANON_01` |
| `opt-trading / sot/build` | repo/branche | branche `sot/build` | ÉTABLI / TÉMOIN INTERMÉDIAIRE | repère historique de consolidation | `GO_REPO_BRANCH_PM_KANBAN_01` |
| `opt-trading / main` | repo/branche | branche `main` | HISTORIQUE / RÉSIDUEL | témoin historique, extraction ciblée seulement si besoin | `GO_REPO_BRANCH_PM_KANBAN_01` |
| `opt-trading / fix/desk-ui-toolbox` | repo/branche | branche `fix/desk-ui-toolbox` | ARCHIVE / SPÉCIALISÉE | archive UI / Desk Pro | `GO_REPO_BRANCH_PM_KANBAN_01` |
| `opt-trading / feat/*` auditées | repo/branche | branches `feat/*` classées | CLOSE / ABSORBÉ | jalons absorbés, non réactivés | `GO_REPO_BRANCH_PM_KANBAN_01` |
| `opt-trading / antigravity/main` | repo/branche | branche `antigravity/main` | ARCHIVE / LABORATOIRE | isolat expérimental hors canon | `GO_REPO_BRANCH_PM_KANBAN_01` |
| `opt-trading / backup/main-before-filter` | repo/branche | branche `backup/main-before-filter` | ARCHIVE / FROIDE | mémoire historique | `GO_REPO_BRANCH_PM_KANBAN_01` |
| `student` | sous-projet intégré | `opt-trading/student/` + docs/scripts associés | ÉTABLI / INTÉGRÉ / PARTIELLEMENT FORMALISÉ | surface opérateur interne à `opt-trading` | `GO_STUDENT_CANONICAL_SURFACE_01` |
| `api collector` | module | module collector dans `opt-trading` | PRÉSENT / À QUALIFIER | collecte de données interne | `GO_API_COLLECTOR_CANONICAL_MODULE_01` |
| `admin-trading` | machine/runtime | docs, runbooks, snapshots, matrices | ÉTABLI / DOCUMENTÉ | hub runtime principal | `GO_RUNTIME_SURFACES_CANONICAL_MAP_01` |
| `db-layer` | machine/runtime | docs, runbooks, snapshots, matrices | ÉTABLI / DOCUMENTÉ | cible infra / data, pas un repo | `GO_RUNTIME_SURFACES_CANONICAL_MAP_01` |
| `cursor-ai` | machine/runtime | docs, snapshots, mappings | ÉTABLI / DOCUMENTÉ | surface opérateur Windows | `GO_RUNTIME_SURFACES_CANONICAL_MAP_01` |
| `localcms` | projet séparé | `localcms / feature/localcms-shared-explorer-cms-installer-v1` + `tools/localcms-dev-host` | ÉTABLI / SÉPARÉ | chantier CMS distinct de `opt-trading` | `GO_LOCALCMS_CANON_DECISION_01` |
| `openclaw` | hors bundle | support canonique séparé requis | HORS BUNDLE | chantier séparé, non réintroduit dans cette passe | `GO_OPENCLAW_CANONICAL_REENTRY_01` |
| `hf_trading` | hors bundle à qualifier plus tard | repo visible mais non qualifié dans cette passe | À QUALIFIER | périmètre potentiel séparé | `GO_HF_TRADING_AUDIT_01` |
| `algo_hf` | hors bundle à qualifier plus tard | repo visible mais non qualifié dans cette passe | À QUALIFIER | périmètre potentiel séparé | `GO_ALGO_HF_AUDIT_01` |
| `Magikgmo` | projet séparé historique | `Magikgmo / main` | HISTORIQUE / ABSORBÉ | mémoire historique seulement, pas de pilotage actif | aucune |

## 3. Règles d'interprétation
- `sot/mainline` reste le pivot canonique unique pour `opt-trading`.
- `student` n'est pas traité comme repo séparé dans cette passe.
- `api collector` est traité comme module interne tant qu'aucun support canonique distinct n'est établi.
- `admin-trading`, `db-layer`, `cursor-ai` sont des surfaces runtime, pas des repos.
- `localcms` reste séparé de `opt-trading`.
- `openclaw` reste hors bundle.
- `hf_trading` et `algo_hf` restent non qualifiés à ce stade.

## 4. Point de reprise
- `GO_CROSS_TOPLOGY_CANON_01`
