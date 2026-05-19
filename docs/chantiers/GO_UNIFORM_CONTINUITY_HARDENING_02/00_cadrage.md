---
doc_id: GO_UNIFORM_CONTINUITY_HARDENING_02_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
go_id: GO_UNIFORM_CONTINUITY_HARDENING_02
chantier_parent: UNIFORM_CONTINUITY_HARDENING
sous_chantier: GO_UNIFORM_CONTINUITY_HARDENING_02
intention_parent: rendre la continuité plus uniforme et rejouable en harmonisant le tronc commun des headings sur workflow / mémoire / documentation, sans créer un nouveau système de templates, sans écraser la hiérarchie parent / sous-chantier / GO, et sans refactorer le fond
cible_finale_parent: canon plus uniforme où, quand applicable, le tronc commun reste stable (Besoin initial / Cible finale / Plan validé / ETABLI / Gap restant / Next GO / REPRISE) tout en conservant les sections parent utiles à la trajectoire multi-GO
objectif_sous_chantier: figer la règle de normalisation, le lot patchable, le lot ambigu et le point de reprise canonique avant toute application
objectif_local_go: produire un référentiel canonique d’uniformisation des headings sans patch d’application
cible_locale_go: AUDIT GLOBAL + règle de normalisation retenue + lot patchable + lot ambigu + reprise
reference_canonique_principale: docs/governance/SESSION_DOCUMENTATION_GATE.md
point_de_reprise: docs/chantiers/GO_UNIFORM_CONTINUITY_HARDENING_02/00_cadrage.md
status: open
lifecycle_stage: cadrage
topic_keys:
  - continuity
  - hardening
  - headings
  - workflow
  - memory
  - documentation
surface: governance
source_kind: canonical
updated_at: 2026-04-14
links:
  - docs/governance/SESSION_DOCUMENTATION_GATE.md
  - docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md
  - docs/index/REPRISE.md
  - docs/index/GO_INDEX.md
  - docs/chantiers/GO_UNIFORM_CONTINUITY_HARDENING_01/00_cadrage.md
  - docs/chantiers/GO_UNIFORM_CONTINUITY_HARDENING_01/90_closeout.md
---

# GO_UNIFORM_CONTINUITY_HARDENING_02 — Cadrage

## Objet

Ouvrir la suite canonique du chantier parent `UNIFORM_CONTINUITY_HARDENING` pour figer une règle d’uniformisation des headings sur workflow / mémoire / documentation, sans appliquer encore les patchs.

Ce GO ne remplace pas `GO_UNIFORM_CONTINUITY_HARDENING_01`.
Il en reprend le point de reprise réel, puis sépare proprement :

- le cadrage canonique de la normalisation
- l’application docs-only sur lot fermé

---

## Besoin initial

Uniformiser plus proprement le tronc commun documentaire pour améliorer la reprise et la transmission, en restant :

- repo-first
- docs-only
- patch minimal
- sans création de template parallèle
- avec conservation des sections parent utiles

---

## Intention

Rendre la continuité plus uniforme et rejouable en harmonisant d’abord les headings et les mappings sûrs, sans refactorer le fond ni écraser la hiérarchie parent / sous-chantier / GO.

---

## Produits finaux voulus / objectifs du chantier parent

Le chantier parent vise une continuité plus stable sur workflow / mémoire / documentation avec :

- un tronc commun de headings plus uniforme
- une transmission plus lisible
- une reprise plus fiable
- une séparation explicite entre ce qui est patchable automatiquement et ce qui exige arbitrage
- un rattachement propre entre cadrage, application et reprise

---

## Cible finale du chantier parent

Obtenir un canon plus uniforme où, quand applicable, le tronc commun reste stable :

- `Besoin initial`
- `Cible finale`
- `Plan validé`
- `ETABLI`
- `Gap restant`
- `Next GO`
- `REPRISE`

Et où les sections conditionnelles restent explicites quand elles portent la trajectoire parent :

- `Intention`
- `Produits finaux voulus / objectifs du chantier parent`
- `Cible finale du chantier parent`

---

## Plan validé

### GO_1 — présent cadrage
- figer la règle de normalisation autorisée
- figer la liste exacte du lot patchable
- figer la liste exacte du lot ambigu
- figer le point de reprise canonique
- ne rien appliquer dans ce GO

### GO_2 — application docs-only
`GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01`

But :
- appliquer uniquement le lot patchable validé par le présent cadrage
- rester sur un patch minimal de headings
- produire une liste exacte des fichiers touchés et un diff synthétique

### GO_3 — optionnel
Ajuster les index de reprise seulement si la continuité active doit être basculée explicitement vers `HARDENING_02` après validation réelle de la suite.

---

## ETABLI

- aucune occurrence de `GO_UNIFORM_CONTINUITY_HARDENING_02` n’était présente dans le repo avant ce cadrage
- `GO_UNIFORM_CONTINUITY_HARDENING_01` existe déjà comme flux précédent
- le closeout `GO_UNIFORM_CONTINUITY_HARDENING_01/90_closeout.md` est en `PASS` ; `localcms` est hors-scope dans ce flux
- la gate canonique impose un tronc minimal documentaire et interdit de créer un nouveau système de templates
- `PRODUCT_CONTINUITY_HIERARCHY_01.md` place ce chantier sur la Couche 0 du socle transverse

---

## A CONFIRMER

Le scope d’application futur doit être confirmé explicitement entre :

- `.md` uniquement
- ou `.md` + closings `.txt`

Par défaut, ce cadrage retient l’option prudente :

- application future limitée aux fichiers `.md`

---

## Gap restant

Il manque encore, avant toute canonisation complète de la normalisation :

- l’application docs-only du lot patchable
- la décision explicite sur les closings `.txt`
- l’éventuelle bascule d’index si `HARDENING_02` devient le flux de reprise dominant

---

## Rôles séparés

### Rôle repo / produit
- `opt-trading` = repo canonique qui porte la gouvernance locale et la continuité de ce chantier

### Rôle IA / IDE
- cadrer la règle de normalisation
- séparer patchable et ambigu
- appliquer seulement après validation du GO d’application

### Rôle machine
- aucun runtime engagé
- chantier documentaire uniquement

---

## Next GO

`GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01`

Ce GO n’est autorisé qu’après validation du présent cadrage.

---

## Règle de normalisation retenue

### Tronc commun cible quand applicable
- `Besoin initial`
- `Cible finale`
- `Plan validé`
- `ETABLI`
- `Gap restant`
- `Next GO`
- `REPRISE`

### Sections conditionnelles à conserver si elles portent la trajectoire parent
- `Intention`
- `Produits finaux voulus / objectifs du chantier parent`
- `Cible finale du chantier parent`

### Mappings autorisés
- `Plan retenu` -> `Plan validé`
- `État établi courant` -> `ETABLI`
- `État établi retenu` -> `ETABLI`
- `Prochain GO logique` -> `Next GO`
- `Prochain GO recommandé` -> `Next GO`
- `Prochains GO retenus` -> `Next GO`
- `Next GO interne au chantier` -> `Next GO`
- `Écart restant` -> `Gap restant`
- `TODO` -> `Gap restant` ou `Next GO` selon le contenu réel
- `Cible des GO suivants` -> `Next GO` si la section décrit l’enchaînement opérationnel

### Interdictions
- ne pas créer un nouveau système de templates
- ne pas réécrire le fond
- ne pas supprimer les sections parent utiles
- ne pas aplatir parent / sous-chantier / GO
- ne pas traiter Trae comme source canonique supérieure au repo

---

## Lot patchable

Le lot patchable visé pour `GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01` est limité à la liste fermée suivante :

- `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/00B_parent_scope_and_structure.md`
- `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/00_cadrage.md`
- `docs/governance/GITHUB_PARK_CONSOLIDATION_DECISION_02.md`
- `docs/governance/BOT_VISION_CANONICAL_PRODUCT_SYNTH_01.md`
- `docs/ot/trading/22_RANGE_STRATEGY_V1_STRUCT_01.md`
- `docs/ot/reports/OT_RANGE_STRATEGY_V1_STRUCT_01.md`

Le GO d’application devra rester :

- docs-only
- patch minimal
- limité aux headings à équivalence claire

---

## Lot ambigu

Les zones suivantes ne doivent pas être patchées automatiquement dans le GO d’application :

- `docs/index/*`
- `journal/index/*`
- `workflow_ai/*`
- closings `.txt`
- audits et documents où le sens est porté principalement par tableaux, listes ou structures non-heading

---

## Périmètre explicitement exclu

Le présent GO exclut :

- toute modification runtime
- toute refonte de fond documentaire
- toute mise à jour d’index dans cette passe
- toute ouverture automatique du GO d’application
- toute normalisation forcée des familles index / matrice / workflow doctrinal

---

## REPRISE

### Reprise globale
- `docs/index/REPRISE.md`

### Reprise chantier
- repartir du constat exposé dans `GO_UNIFORM_CONTINUITY_HARDENING_01/90_closeout.md`
- utiliser le présent cadrage comme nouveau point de reprise canonique pour la suite de normalisation

### Point de reprise local
- `docs/chantiers/GO_UNIFORM_CONTINUITY_HARDENING_02/00_cadrage.md`

---

## Statut

**OPEN — cadrage canonique posé ; règle, lots et reprise figés ; application encore non ouverte**
