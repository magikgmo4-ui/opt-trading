---
doc_id: OPT_TRADING_GO_INDEX
doc_type: reprise
repo: opt-trading
project: opt-trading
module:
go_id:
status: reference
lifecycle_stage: governance
topic_keys:
  - opt-trading
  - go_index
  - continuity
  - governance
search_tags:
  - surface:continuite
  - doc_role:index
  - closeout:reference
surface: continuity
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Tableau canonique des chantiers"
updated_at: 2026-05-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01_PRODUCT_SURFACE_ALIGNMENT_01.md
  - docs/governance/REPO_ROLE.md
  - docs/governance/DOC_LAYERS.md
---

# GO_INDEX — opt-trading

## Objet

Ce document référence les GO non clos connus et utiles à la continuité locale de `opt-trading`.

## Rattachement maître

- l'etat reel prouve prime sur toute reconstruction documentaire
- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md` gouverne la lecture produit / parent / GO / Git
- `docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md` classe les produits/surfaces finales `PF_*`
- `docs/governance/MATRICE_GOUVERNANTE_V2.md` reste une annexe stable secondaire
- `docs/index/GO_INDEX.md` reste la verite de liste locale pour les parents, GO simples et sous-entrees retenues

---

## Snapshot global système

- 2026-04-18  
  → docs/architecture/PROJECT_SNAPSHOT_GLOBAL_2026-04-18.md  
  → vue consolidée projets / infra / chantiers / runtime

---

## Forms / LocalCMS (cadrage)

- GO_LOCALCMS_FORMS_INTEGRATION_DOC_01  
  → docs/chantiers/GO_LOCALCMS_FORMS_INTEGRATION_DOC_01/00_cadrage.md  
  → intégration future forms compatible avec localcms existant (doc-only)

---

## Règles

- l’index référence et synthétise
- il ne remplace ni le dossier chantier ni le closeout
- `GO_INDEX.md` est l’index opératoire des chantiers non clos
- le `Tableau canonique des chantiers` est la vérité de liste de `GO_INDEX.md`
- la section `Entrées` enrichit un GO déjà canonisé dans le tableau ; elle n’ouvre pas un nouveau GO à elle seule
- lorsqu’un chantier passe en `CLOSED`/`PASS`, il doit être retiré de `docs/index/GO_INDEX.md` et déplacé dans `docs/index/GO_CLOSED_INDEX.md`
- les entrées `REFERENCE` peuvent rester dans `GO_INDEX.md` si elles sont utiles à la continuité active et ne correspondent pas à une clôture
- une surface documentaire non chantier peut être citée comme source, support ou référence, mais ne doit pas être listée comme chantier dans le tableau canonique
- un repère de famille dérivé peut exister comme aide transverse non canonique ; il ne doit ni modifier la liste canonique ni porter la priorité opératoire à la place du tableau
- les liens doivent pointer vers les artefacts détaillés dès qu’ils existent
- un parent/GO ne doit pas être fermé si son `MASTER_TARGET` ne pointe pas vers un produit final utilisable ou une surface finale `PF_*` vérifiable

---

## Tableau canonique des parents produits

Ce tableau canonique contient les chantiers parents avec produit utilisable, cible produit claire ou correction structurelle de lecture produit. Les enfants, micro-GO, bundles, patchs, branches, PR, références et artefacts support sont exclus des index globaux actifs sauf demande explicite de propagation.

| PARENT_PRODUCT | STATUT | TARGET | NEXT ACTION | SOURCE |
|---|---|---|---|---|
| `GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_FINAL_REGISTRY_01` | OPEN | registre produits/surfaces finales `PF_*` | `GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_CLOSE_GATE_AUDIT_01` | `docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md` |
| `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` | OPEN | canoniser méthode multi-agents | surveiller prochains INDEX_PATCH | `docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/PARENT_STATE.md` |
| `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` | OPEN | parent machine admin-trading | maintenir le parent ; ouvrir child si besoin produit | `docs/chantiers/GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01/01_cadrage_parent.md` |
| `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` | OPEN | parent machine db-layer | maintenir le parent ; ouvrir child si besoin produit | `docs/chantiers/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01/01_cadrage_parent.md` |
| `GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01` | ACTIVE | consolider lignées runtime | figer survivant/transition/legacy/archive en gap-only | `docs/chantiers/GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01/00_cadrage.md` |
| `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03` | OPEN | réduire compat réseau/ssh | ouvrir lot de réduction compat sur `scripts/reseau_ssh` | `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md` |
| `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01` | ACTIVE | implémentation tmux-ide | exécuter `GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01` | `docs/chantiers/GO_TMUX_IDE_OPT_TRADING_CADRAGE_01/00_cadrage.md` |
| `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01` | OPEN | intégration UI producer-consumer | reprise recommandée sur `GO_OPT_TRADING_UI_LOCALCMS_INVENTORY_01` | `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/01_cadrage_parent.md` |
| `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` | OPEN | architecture équipe d'agents | utiliser comme base si GO enfant d'audit documentaire | `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/00_cadrage.md` |
| `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01` | ACTIVE | runtime tmux/opencode/openclaw | maintenir le runtime ; ouvrir suite si besoin produit | `docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md` |

## Hors pilotage immédiat (parents ouverts sans produit actif immédiat)

| PARENT | STATUT | RAISON |
|---|---|---|
| `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` | OPEN | parent réel ; chaîne TMUX close ; prochaine passe canonique non prioritaire |
| `GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01` | OPEN | bundle doc-only mergé ; closeout produit ; parent non fermé |
| `GO_OPT_TRADING_STRICT_WORKERS_PARENT_01` | OPEN | branche-only ; continuité canonique basculée sur PR #645/#646 |

---

## Priorite operatoire

- P0 : `GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_CLOSE_GATE_AUDIT_01`
- P1 : `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01`
- P2 : `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01`, `GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01`, `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03`
- P3 : `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01`, `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01`

Les GO suivants restent `OPEN` dans le tableau canonique, mais hors priorite operatoire immediate :

- `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01`
- `GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01`
- `GO_OPT_TRADING_STRICT_WORKERS_PARENT_01`
- `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01`
- `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01`
- `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01`

---

## MASTER_TARGET candidats explicites (priorite operatoire)

Les six parents ci-dessous portent une cible de niveau `1_MASTER_TARGET` deja lisible
dans leur dossier chantier. Cette section les rend explicites dans l'index sans les
fermer ni les promouvoir artificiellement.

| PARENT_PRODUCT | MASTER_TARGET candidat | SOURCE |
|---|---|---|
| `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01` | session IDE terminale stable et reattachable pour `opt-trading`, avec layout operatoire et bundle de transfert canonique | `docs/chantiers/GO_TMUX_IDE_OPT_TRADING_CADRAGE_01/00_cadrage.md` |
| `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` | doctrine multi-agents canonique, reutilisable et indexable globalement, avec continuite parent locale maitrisee | `docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/PARENT_STATE.md` |
| `GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01` | fiches runtime courtes, homogenes et non redondantes, rattachees explicitement a leurs lignees | `docs/chantiers/GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01/00_cadrage.md` |
| `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03` | famille `reseau_ssh*` consolidee autour d'un survivant canonique explicite et d'une hierarchie runtime/doc/legacy claire | `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md` |
| `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` | chantier parent canonique, autonome et reutilisable pour cadrer une architecture d'equipe d'agents specialisee | `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/00_cadrage.md` |
| `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01` | architecture d'utilisation continue ou `tmux`, `OpenCode`, `OpenClaw` et `Telegram` portent des roles separes et reprenables | `docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md` |

---

## Entrées

### GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_FINAL_REGISTRY_01
- repo : opt-trading
- type : gouvernance / produit final / surfaces finales
- statut : open
- titre court : registre canonique des produits/surfaces finales `PF_*`
- dernier état connu : registre créé ; matrice alignée via addendum ; index globaux alignés ; patch/bundle à appliquer/revoir
- lien utile : `docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md`, `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01_PRODUCT_SURFACE_ALIGNMENT_01.md`, `docs/chantiers/GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_FINAL_REGISTRY_01/00_INITIAL_PROJECT_DOC.md`

### GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
- repo : opt-trading
- type : reprise documentaire / parent OpenClaw / db-layer
- statut : open
- titre court : parent OpenClaw operateur hors continuite canonique a realigner
- dernier etat connu : parent reel de reference sur branche dediee `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` ; la chaine TMUX historique est closee
- lien utile : `docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/REPRISE_DB_LAYER_20260505.md`, `docs/index/inbox/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01.md`

### GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01
- repo : opt-trading
- type : chantier parent / ClickUp continuity / bundle d'implémentation
- statut : open
- titre court : continuité ClickUp parent et bundle d'exécution
- dernier état connu : bundle doc-only mergé localement dans sot/mainline ; closeout de phase review/merge produit ; parent non fermé
- lien utile : `docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01/00_INITIAL_PROJECT_DOC.md`, `docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01/90_CLOSEOUT.md`

### GO_OPT_TRADING_STRICT_WORKERS_PARENT_01
- repo : opt-trading
- type : chantier parent / strict workers / agents
- statut : open
- titre court : parent canonique strict workers IA a autonomie etroite
- dernier etat connu : parent historique sur branche `go/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01`, continuite canonique basculee sur PR #645/#646
- lien utile : branche `go/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01`

### GO_UNIFORM_CONTINUITY_FINAL_MASTER_PLAN_01
- repo : opt-trading
- type : gouvernance / continuité
- statut : reference
- titre court : plan maître uniforme de continuité
- lien utile : `docs/chantiers/GO_UNIFORM_CONTINUITY_FINAL_MASTER_PLAN_01/00_cadrage.md`

### GO_EXTRACTEUR_TAGS_CANONICAL_METHOD_01
- repo : opt-trading
- type : gouvernance / extraction / documentation
- statut : reference
- titre court : méthode canonique d'extraction par tags
- lien utile : `docs/governance/EXTRACTEUR_TAGS__METHODE_CANONIQUE_V1.md`
