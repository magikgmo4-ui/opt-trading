---
doc_id: OPT_TRADING_GO_GITHUB_PARK_AUDIT_EXPANSION_01_PARENT_SCOPE
doc_type: chantier_addendum
repo: opt-trading
project: opt-trading
go_id: GO_GITHUB_PARK_AUDIT_EXPANSION_01
chantier_parent: github_park_inventory_audit_consolidation
sous_chantier: GO_GITHUB_PARK_AUDIT_EXPANSION_01
intention_parent: éviter que les GO suivants soient lus comme des chantiers isolés; préserver la logique parent et la cible finale de repo; faire suivre cette logique dans les sous-chantiers
cible_finale_parent: descendre du parc vers des consolidations ciblées, pour converger vers un repo consolidé/aligné/ordonné, sans parasites ni historique mal situé
objectif_sous_chantier: séquencer l’inventaire du parc GitHub en GO spécialisés (branches↔trunks, familles de modules, cartographie fichier par rôle) sans relancer un audit global indistinct
objectif_local_go: figer la portée parent et la structure parent/sous-chantier/GO pour la série de GO de consolidation
cible_locale_go: chaque GO suivant explicite chantier parent + sous-chantier + intention/cible finale parent + objectif/cible locale GO + référence canonique principale + point de reprise
reference_canonique_principale: docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md
point_de_reprise: GO_GITHUB_PARK_BRANCH_TRUNK_CROSS_AUDIT_01 (depuis docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/00_cadrage.md)
status: validated
lifecycle_stage: cadrage
topic_keys:
  - github
  - inventaire
  - audit
  - consolidation
  - parent_chantier
  - sub_chantiers
surface: park
source_kind: canonical
updated_at: 2026-04-14
links:
  - docs/governance/SESSION_DOCUMENTATION_GATE.md
  - docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md
  - docs/index/REPRISE.md
  - docs/index/GO_INDEX.md
  - docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md
---

# GO_GITHUB_PARK_AUDIT_EXPANSION_01 — Portée parent et structure

## Objet

Figer explicitement que le vrai chantier parent est :

- inventaire
- audit
- consolidation

et que les GO qui suivent sont des **étapes** ou **sous-chantiers** de cette trajectoire plus large.

---

## Besoin initial

Éviter que les GO suivants soient lus comme des chantiers isolés sans lien avec le mouvement parent.

---

## Intention

- garder un chantier parent clair
- faire suivre cette logique dans les sous-chantiers
- ne pas perdre la cible finale de repo au fil des GO successifs

---

## Produits finaux voulus / objectifs du chantier parent

Le chantier parent vise une trajectoire complète :

- inventaire
- audit
- consolidation

avec comme horizon final un repo :

- 100% consolidé
- aligné
- à structure claire
- ordonnée
- sans parasite
- sans historique mal situé
- sans item mal structuré / indexé / situé / documenté / canonisé

---

## Cible finale du chantier parent

Descendre du parc vers des consolidations ciblées, sans rouvrir un audit global du parc à chaque étape.

---

## Next GO

Chaque GO suivant doit être documenté comme :

- une étape
- ou un sous-chantier

à l’intérieur du chantier parent.

Chaque GO doit donc faire suivre explicitement :

- le besoin initial parent
- la cible finale du chantier parent
- la cible locale du GO
- l’intention du chantier parent
- les produits finaux voulus / objectifs du chantier parent

---

## Plan validé

1. Le chantier parent reste le cadre de référence.
2. Les GO suivants descendent le travail par étapes.
3. Les sous-chantiers ne remplacent pas le parent.
4. La continuité documentaire doit conserver :
   - le parent
   - le sous-chantier
   - le point de reprise
   - la cible finale commune

---

## ÉTABLI

- la gate canonique exige désormais la propagation de l’intention et de la cible finale
- `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03` est un sous-chantier de consolidation
- le chantier parent reste `inventaire + audit + consolidation`

---

## Gap restant

- reprendre explicitement cette structure dans les prochains GO de consolidation
- garder la séparation entre cible finale parent et cible locale du GO

---

## REPRISE

Lire ce document comme addendum de portée du chantier parent.
Les sous-chantiers doivent s’y rattacher explicitement.

---

## Structure minimale à reprendre (front matter)

```yaml
chantier_parent:
sous_chantier:
intention_parent:
cible_finale_parent:
objectif_sous_chantier:
go_id:
objectif_local_go:
cible_locale_go:
reference_canonique_principale:
point_de_reprise:
```

## RISKS

- À qualifier.
