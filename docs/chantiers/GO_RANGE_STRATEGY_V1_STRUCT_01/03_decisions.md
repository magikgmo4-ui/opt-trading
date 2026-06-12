---
doc_id: GO_RANGE_STRATEGY_V1_STRUCT_01_DECISIONS
doc_type: decision
repo: opt-trading
project: trading
module: range_strategy_v1
go_id: GO_RANGE_STRATEGY_V1_STRUCT_01
status: active
lifecycle_stage: validation
topic_keys:
  - opt-trading
  - trading
  - range_strategy
  - decisions
surface: trading
source_kind: canonical
updated_at: 2026-04-14
links:
  - docs/ot/trading/22_RANGE_STRATEGY_V1_STRUCT_01.md
  - docs/chantiers/GO_RANGE_STRATEGY_V1_STRUCT_01/00_cadrage.md
---

# 03_decisions — GO_RANGE_STRATEGY_V1_STRUCT_01

## Décision 1
- sujet : couche documentaire principale du chantier
- option retenue : ancrer le contenu métier principal dans `docs/ot/trading/`
- raison du choix : le lot relève du canon trading du repo
- impact : la note de stratégie n'est plus portée seulement comme report transversal

## Décision 2
- sujet : forme chantier retenue
- option retenue : ouvrir un vrai dossier `docs/chantiers/GO_RANGE_STRATEGY_V1_STRUCT_01/`
- raison du choix : respecter la structure canonique locale `00/01/02/03/90`
- impact : meilleure reprise, meilleure traçabilité, meilleur alignement avec la méthode uniforme

## Décision 3
- sujet : noyau initial d'actifs
- option retenue : `AUD/NZD`, `USD/CHF`, `XAUUSD`
- raison du choix : couvrir trois profils complémentaires de marché range sans élargir prématurément le périmètre
- impact : stratégie V1 bornée, comparable et plus simple à documenter

## Décision 4
- sujet : nature du produit final visé à ce stade
- option retenue : cadre stratégique humainement exécutable, journalisable et testable
- raison du choix : éviter de confondre cadrage canonique et système automatique déjà validé
- impact : aucune sur-promesse runtime ni statistique dans ce lot

## Décision 5
- sujet : mutation transverse des couches `governance`, `master_pack`, `index`, `next`, `opportunities`, `product_targets`
- option retenue : lecture obligatoire, mutation minimale seulement si un nouveau fait canonique transverse est réellement établi
- raison du choix : éviter de polluer les couches globales avec un lot trading encore localisé
- impact : priorité donnée au dossier chantier et à la couche trading ; les couches transverses ne doivent être étendues que si la continuité globale du repo l'exige

## RISKS

- À qualifier.
