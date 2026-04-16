---
doc_id: GO_CONTINUITE_PRODUIT_MULTI_CHANTIER_CANON_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module:
go_id: GO_CONTINUITE_PRODUIT_MULTI_CHANTIER_CANON_01
status: pass
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - continuity
  - product_continuity
  - hierarchy
  - canon
surface: governance
source_kind: canonical
updated_at: 2026-04-16
links:
  - docs/index/GO_INDEX.md
  - docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md
  - docs/governance/AUDIT_CONTINUITE_PRODUIT_OPT_TRADING.md
  - docs/index/REPRISE.md
  - docs/governance/SESSION_DOCUMENTATION_GATE.md
---

# 00_cadrage — GO_CONTINUITE_PRODUIT_MULTI_CHANTIER_CANON_01

## Objet

Ouvrir un dossier chantier dédié minimal pour `GO_CONTINUITE_PRODUIT_MULTI_CHANTIER_CANON_01`, déjà référencé dans `docs/index/GO_INDEX.md` mais sans dossier `docs/chantiers/` dédié observé.

---

## Besoin initial

Rattacher explicitement à un dossier chantier le GO qui canonise la hiérarchie produit multi-chantier, afin d’éviter qu’il reste uniquement porté par l’index et par des documents de gouvernance transverses.

---

## Intention

Préserver un point de reprise documentaire clair pour la canonisation de la hiérarchie produit, sans rouvrir artificiellement un chantier déjà établi comme `pass` dans le canon courant.

---

## Produits finaux voulus / objectifs du chantier

- un dossier chantier dédié minimal pour ce GO
- un rattachement explicite aux documents canoniques qui portent la hiérarchie produit
- une trace de continuité propre entre index, gouvernance et reprise
- une base documentaire stable pour les GO dérivés ou rattachés à la hiérarchie produit

---

## Cible finale

Disposer d’un dossier `docs/chantiers/GO_CONTINUITE_PRODUIT_MULTI_CHANTIER_CANON_01/` servant de point d’entrée chantier pour une décision déjà canonisée côté produit.

---

## Plan validé

1. constater la présence du GO dans `GO_INDEX.md`
2. constater l’absence de dossier chantier dédié
3. ouvrir un `00_cadrage.md` minimal de rattachement
4. conserver le statut connu `pass`
5. ne pas reconstruire artificiellement un historique détaillé non déjà établi dans le repo

---

## ETABLI

- `GO_CONTINUITE_PRODUIT_MULTI_CHANTIER_CANON_01` est référencé dans `docs/index/GO_INDEX.md`
- l’index indique :
  - type : gouvernance / continuité produit
  - statut : `pass`
  - titre court : hiérarchie produit multi-chantier canonisée
  - dernier état connu : structuration Couche 0 / Anneau A / Anneau B posée comme source canonique de continuité produit
- les documents de référence déjà explicitement liés dans l’index sont :
  - `docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md`
  - `docs/governance/AUDIT_CONTINUITE_PRODUIT_OPT_TRADING.md`
- aucun dossier chantier dédié n’a été observé sous `docs/chantiers/GO_CONTINUITE_PRODUIT_MULTI_CHANTIER_CANON_01/` avant la présente ouverture

---

## Gap restant

- enrichir plus tard ce dossier seulement si un lot de closeout, de décisions ou de reprise dédié doit être rattaché explicitement à ce GO
- éviter toute duplication inutile avec les documents de gouvernance déjà canoniques

---

## Rôles séparés

### Rôle repo / produit
- `opt-trading` porte le canon de continuité produit multi-chantier

### Rôle IA / IDE
- ouvrir le point d’ancrage chantier minimal
- ne pas rouvrir un chantier clos sans besoin réel

### Rôle machine
- aucun runtime engagé
- chantier documentaire uniquement

---

## Next GO

Aucun nouveau GO imposé à ce stade.

Les suites doivent rester pilotées par les besoins réels de continuité produit, non par la seule création du présent dossier dédié.

---

## REPRISE

### Reprise globale
- `docs/index/REPRISE.md`

### Point de reprise local
- `docs/chantiers/GO_CONTINUITE_PRODUIT_MULTI_CHANTIER_CANON_01/00_cadrage.md`

---

## Statut

**PASS — dossier chantier dédié minimal désormais ouvert en rattachement d’un GO déjà canonisé**
