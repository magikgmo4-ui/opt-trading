---
doc_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_INPUT_CAPTURE_ANALYSIS_OUTPUT_PIPELINE_01_SCOPE
doc_type: scope_and_objective
repo: opt-trading
go_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_INPUT_CAPTURE_ANALYSIS_OUTPUT_PIPELINE_01
parent_go_id: GO_OPT_TRADING_COLLECTORS_BOT_VISION_PARENT_01
status: open
lifecycle_stage: planning
created_at: 2026-05-30
updated_at: 2026-05-30
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PF_ID: PF_BOT_VISION_HEADLESS
---

# 00_SCOPE_AND_OBJECTIVE.md

## 1_CANONICAL_STATE

`PF_BOT_VISION_HEADLESS` est ré-ouvert en mode **ACTIVE_EXPANSION**.

La surface n'est plus seulement "faire un screenshot" — le scope est élargi à un pipeline complet :

```
INPUT → CAPTURE → ANALYSIS → OUTPUTS → DATA CENTER → DESKPRO
```

## 2_MASTER_TARGET

Alimenter DeskPro avec un pipeline headless robuste capable de :

- choisir les bonnes adresses / écrans / assets
- capturer les bons visuels
- analyser les screenshots
- produire des outputs utiles (images, analyse, setups, Telegram)
- pousser un maximum de données structurées vers Data Center
- rendre ces données exploitables côté DeskPro

## 3_PIPELINE_CANONIQUE

```
INPUT SURFACE
  ├── URL / adresses
  ├── pages / écrans
  ├── assets suivis
  ├── charts
  ├── indices
  └── screeners
       ↓
CAPTURE SURFACE
  ├── screenshot stable (Playwright)
  ├── viewport / zone capturée
  ├── multi-écrans / multi-sections
  └── reproductibilité
       ↓
ANALYSIS SURFACE
  ├── OCR / lecture visuelle
  ├── détection setup
  ├── extraction niveaux / tendance / signal
  └── classification type de contenu
       ↓
OUTPUT SURFACE
  ├── images brutes
  ├── images annotées
  ├── analyses textuelles
  ├── setup cards
  ├── payload Telegram
  └── payload structuré Data Center
       ↓
DATA CENTER HANDOFF
  └── schéma max data out
       ↓
DESKPRO CONSUMPTION
  └── données exploitables côté DeskPro
```

## 4_OBJECTIFS_CLES

| Axe | Objectif |
|-----|----------|
| Input expansion | Catalogue canonique des adresses, écrans, assets, charts, indices, screeners |
| Capture validation | Screenshot stable, viewport maîtrisé, multi-écrans, reproductible |
| Analysis enrichment | OCR, détection setup, extraction niveaux/tendance/signal, classification |
| Output generation | Images brutes + annotées, analyses, setup cards, Telegram, Data Center |
| Downstream integration | Schéma max data out, ingestion Data Center, consommation DeskPro |

## 5_INVARIANTS

- `PF_BOT_VISION_HEADLESS` reste OPEN jusqu'à preuve end-to-end
- Pas de close gate tant que input/capture/analyse/output/data-center ne sont pas prouvés
- Data Center ne remplace pas la validation de la couche vision
- DeskPro doit être pensé comme destination produit
- Chaque screenshot doit avoir un type
- Chaque type doit avoir un analyseur dédié
- Chaque capture doit produire un JSON
- Telegram ne doit pas recevoir tout le bruit
- Data Center reçoit le maximum

## 6_ETABLI

- Le premier niveau de run texte existe déjà
- La fermeture précédente était prématurée
- Le vrai besoin est un pipeline vision headless de production
- Le pipeline doit supporter une expansion des sources d'entrée
- Le pipeline doit produire plusieurs formes de sortie

## 7_HYPOTHESES_A_VALIDER

- Certaines sources nécessiteront un mapping URL → viewport → zones d'intérêt
- Toutes les pages ne demanderont pas le même type de capture
- Certains outputs pourront être générés directement depuis l'analyse
- Le schéma Data Center devra distinguer : raw_capture / extracted_signal / generated_summary / distribution_payload
