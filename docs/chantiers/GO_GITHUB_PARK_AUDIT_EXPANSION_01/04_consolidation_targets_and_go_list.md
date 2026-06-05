---
doc_id: OPT_TRADING_GO_GITHUB_PARK_CONSOLIDATION_TARGETS_AND_GO_LIST_01
doc_type: chantier_report
repo: opt-trading
project: opt-trading
go_id: GO_GITHUB_PARK_AUDIT_EXPANSION_01
status: validated
lifecycle_stage: planning
topic_keys:
  - github
  - consolidation
  - targets
  - go_list
  - ide_bundle
surface: park
source_kind: canonical
updated_at: 2026-04-14
links:
  - docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/00_cadrage.md
  - docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/00B_parent_scope_and_structure.md
  - docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/02_module_family_consolidation_audit.md
  - docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/03_file_role_cartography.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md
---

# Consolidations ciblées à effectuer — GO list

## Besoin initial

Utiliser la cartographie comme base de tri entre :

- survivant
- runtime utile
- doc/gouvernance
- legacy

pour cibler les consolidations à effectuer et lister les GO à descendre ensuite.

---

## Cible finale du chantier parent

Le chantier parent reste :

- inventaire
- audit
- consolidation

avec comme horizon final un repo :

- 100% consolidé
- aligné
- structure claire
- ordonnée
- sans parasite
- sans historique mal situé
- sans item mal structuré / indexé / situé / documenté / canonisé

---

## Cible du GO / de cette étape

Transformer la cartographie et l’audit des familles en :

- liste de consolidations ciblées
- GO priorisés
- base de bundle IDE pour exécution bornée

---

## Intention

- ne pas rouvrir un audit de parc large
- partir sur des consolidations ciblées
- utiliser la cartographie comme base de tri stable
- garder visible la cible finale du chantier parent dans les GO suivants

---

## Produits finaux voulus / objectifs du chantier

À travers les sous-chantiers de consolidation, contribuer à un repo :

- 100% consolidé
- aligné
- structure claire
- ordonnée
- sans parasite
- sans historique mal situé
- sans item mal structuré / indexé / situé / documenté / canonisé

---

## Plan appliqué

1. Reprendre la cartographie fichier par fichier.
2. Reprendre l’audit des familles de modules.
3. Regrouper les familles par niveau de consolidation.
4. Distinguer :
   - survivant
   - runtime utile
   - doc/gouvernance
   - legacy
5. Lister les GO à descendre.
6. Préparer un bundle IDE dédié.

---

## ÉTABLI

### Priorité P1 — consolidations physiques / clarifications les plus nettes

#### 1. `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03`
Famille :
- `reseau_ssh`
- `reseau_ssh_step1b`
- `reseau_ssh_step2`

Tri retenu à ce stade :
- survivant visé : `reseau_ssh_step2`
- runtime utile : `reseau_ssh_step2` + éventuels fragments encore requis durant transition
- doc/gouvernance : docs utiles de `reseau_ssh` et `reseau_ssh_step2`
- legacy : `reseau_ssh_step1b` puis reliquats anciens de `reseau_ssh`

#### 2. `GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01`
Famille :
- `bot_vision`
- `bot_vision_step2`
- `vision_bot`

Tri retenu à ce stade :
- survivant : à déterminer
- runtime utile : forte densité runtime sur les trois surfaces
- doc/gouvernance : docs de bot/bridge/inbox/vision
- legacy : nomenclature step/final redondante si survivant unique confirmé

#### 3. `GO_OPT_TRADING_PERF_FAMILY_CONSOLIDATION_01`
Famille :
- `perf`
- `perf_engine`

Tri retenu à ce stade :
- survivant probable : `perf_engine`
- runtime utile : surfaces `perf_engine`
- doc/gouvernance : contrats et docs perf
- legacy : `perf` si compat only

#### 4. `GO_OPT_TRADING_JOURNAL_FAMILY_CONSOLIDATION_01`
Famille :
- `journal_de_bord`
- `journal_engine`

Tri retenu à ce stade :
- survivant : à clarifier entre moteur et surface opérateur
- runtime utile : `journal_de_bord`
- doc/gouvernance : GO matrix, specs, closings
- legacy : aucune décision prématurée sans lecture plus fine

### Priorité P2 — stacks à cartographier puis consolider

#### 5. `GO_OPT_TRADING_DESK_STACK_ROLE_MAP_AND_CONSOLIDATION_01`
Familles :
- `desk_*`
- `desk_pro*`

But :
- clarifier noyau / runner / dashboard / orchestrateur / ingest / state
- ne pas fusionner à l’aveugle

#### 6. `GO_OPT_TRADING_OPENCLAW_STACK_REGISTRY_ALIGNMENT_01`
Famille :
- `*openclaw*`

But :
- clarifier runtime utile / gouvernance / evidence / registry coverage

#### 7. `GO_OPT_TRADING_DEEPSEEK_FAMILY_CONSOLIDATION_01`
Famille :
- `deepseek*`

But :
- clarifier contrats et survivants

#### 8. `GO_OPT_TRADING_REGISTRY_STACK_ROLE_MAP_01`
Famille :
- `registry*`

But :
- rendre lisible la stack registry reader/router/ui
- préparer règles de couverture canonique

### Priorité P3 — clarifications transverses / couverture canonique

#### 9. `GO_OPT_TRADING_TRADING_STACK_BOUNDARY_01`
Famille :
- `trading_lab_v1`
- `trading_realtime_v1`

But :
- clarifier frontière Lab vs Real-Time
- isoler le legacy embarqué

#### 10. `GO_OPT_TRADING_MODULES_REGISTRY_COVERAGE_01`
But transverse :
- traiter l’écart entre parc réel et `registry/modules_registry.yaml`
- sans lancer une régularisation massive aveugle

---

## Gap restant

Il reste à faire :

- l’exécution réelle des GO listés
- la validation du survivant effectif dans les familles ambiguës
- les patchs minimaux de consolidation
- la régularisation canonique progressive de la registry si nécessaire

---

## TODO

- lancer `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03` en premier
- descendre ensuite `vision`, `perf`, `journal`
- garder `desk*`, `openclaw*`, `deepseek*`, `registry*` comme stacks à clarifier avant fusion
- utiliser le bundle IDE dédié pour la reprise opératoire

---

## REPRISE

Ce document liste les consolidations ciblées à effectuer.
Les GO ci-dessus doivent être traités comme sous-chantiers du parent `inventaire + audit + consolidation`.

---

## Next GO

### GO immédiat retenu
`GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03`

### Suite courte recommandée
1. `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03`
2. `GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01`
3. `GO_OPT_TRADING_PERF_FAMILY_CONSOLIDATION_01`
4. `GO_OPT_TRADING_JOURNAL_FAMILY_CONSOLIDATION_01`

---

## Statut

**VALIDATED — cibles de consolidation identifiées, GO listés, bundle IDE préparé**

## RISKS

- À qualifier.
