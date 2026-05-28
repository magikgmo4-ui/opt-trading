---
doc_id: GO_OPT_TRADING_TELEGRAM_INGESTION_PARENT_OPEN_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: telegram_ingestion
go_id: GO_OPT_TRADING_TELEGRAM_INGESTION_PARENT_OPEN_01
parent_go_id: null
status: open
lifecycle_stage: planning
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-28
updated_at: 2026-05-28
GO_STRUCTURAL_ROLE: GO_PARENT_ATTACHED_TO_MASTER_PROJECT_PLAN
PF_ID: PF_TELEGRAM_INGESTION
MASTER_PROJECT_PLAN_ID: MPP_TELEGRAM_INGESTION_OPERATIONAL
MASTER_TARGET_ID: MT_TELEGRAM_INGESTION_OPERATIONAL
PARENT_GO_ID: null
BUNDLE_TARGET: null
NEXT_ATTACH_TARGET: null
NEXT_GO: GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_INBOUND_PARSER_01
topic_keys:
  - opt-trading
  - telegram_ingestion
  - inbound_parser
  - message_ingestion
  - master_project_plan
links:
  - docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01_MASTER_PROJECT_PLAN_CREATION_RULE_01.md
  - docs/index/GO_INDEX.md
  - docs/index/REPRISE.md
---

# GO_OPT_TRADING_TELEGRAM_INGESTION_PARENT_OPEN_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Telegram Ingestion opérationnel : les messages Telegram inbound (canaux, groupes,
bots) sont ingérés, normalisés et mis à disposition des surfaces consommatrices
(Telegram Screener, Desk Pro, Data Center).

La règle centrale est :

```text
Telegram API -> inbound parser -> normalized message -> consumers
```

Composants identifiés :
- Inbound parser Telegram — lecture des messages depuis l'API Telegram
- Normalisation des messages en format canonique
- Distribution vers PF_TELEGRAM_SCREENER, PF_DESK_PRO, PF_DATA_CENTER

## 2_INITIAL_PROJECT_DOC

Ce document ouvre le parent canonique `PF_TELEGRAM_INGESTION` pour la première fois.

Il fige la structure de continuité du parent : `1_MASTER_TARGET`, `4_MASTER_PROJECT_PLAN`
et `CLOSE_GATE_MASTER_TARGET` déclarés, rattachement à `PF_TELEGRAM_INGESTION`
et `MPP_TELEGRAM_INGESTION_OPERATIONAL`.

Il ne ferme pas le parent. Il ne modifie pas les index globaux.

## 3_INITIAL_NEED

`PF_TELEGRAM_INGESTION` est référencé dans `PRODUCT_FINAL_SURFACE_REGISTRY_01.md`
comme surface finale P1 avec statut "à créer — parent ingestion Telegram".

Aucun dossier chantier ni document parent n'existait pour ce produit avant cette ouverture.
Les modules Telegram existants (Telegram Screener, Telegram notify) sont des consommateurs
aval sans couche d'ingestion normalisée.

L'ouverture est nécessaire avant tout child GO d'implémentation afin que les child GOs
puissent être rattachés (`GO_CHILD_ATTACHED_TO_PARENT`) à un parent canonique réel.

## 4_MASTER_PROJECT_PLAN

`MPP_TELEGRAM_INGESTION_OPERATIONAL`

1. **Inbound parser** : implémenter le parser des messages Telegram inbound via l'API Telegram (telethon ou équivalent).
2. **Normalisation** : normaliser les messages en format canonique (type, timestamp, source, contenu).
3. **Distribution** : distribuer les messages normalisés vers les consommateurs (Screener, Desk Pro, Data Center).
4. **File d'attente** : gérer la file d'attente et le backpressure des messages inbound.
5. **Tests de compatibilité** : valider l'ingestion et la normalisation par tests smoke.
6. **Documentation reprise** : documenter les gaps, la couverture des sources, les parseurs manquants.

## 5_GO_PLAN

Chantier parent structurel. Cette ouverture est doc-first : aucun runtime modifié.

Sous-GO proposés (à ouvrir séquentiellement selon priorité opératoire) :

| GO_ID | Cible |
|---|---|
| `GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_INBOUND_PARSER_01` | Implémenter le parser inbound Telegram |
| `GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_MESSAGE_NORMALIZER_01` | Normaliser les messages en format canonique |
| `GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_CONSUMER_DISTRIBUTION_01` | Distribuer vers Screener, Desk Pro, Data Center |

Premier child recommandé : `GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_INBOUND_PARSER_01`.

## 6_FINAL_TARGET

Livrable de cette ouverture : un parent canonique `GO_OPT_TRADING_TELEGRAM_INGESTION_PARENT_OPEN_01`
structuré avec `1_MASTER_TARGET`, `4_MASTER_PROJECT_PLAN` et `CLOSE_GATE_MASTER_TARGET`
déclarés, rattaché à `PF_TELEGRAM_INGESTION` et `MPP_TELEGRAM_INGESTION_OPERATIONAL`,
prêt à recevoir les child GOs d'implémentation.

## 7_CANONICAL_STATE

- `PF_TELEGRAM_INGESTION` dans `PRODUCT_FINAL_SURFACE_REGISTRY_01.md` comme surface finale P1 "à créer".
- `GO_OPT_TRADING_TELEGRAM_INGESTION_PARENT_OPEN_01` n'existait pas avant cette ouverture ; ce document en est l'acte de création.
- Aucun parser inbound Telegram n'existe dans le repo.
- `PF_TELEGRAM_SCREENER` est le principal consommateur aval attendu.
- `PF_DESK_PRO` et `PF_DATA_CENTER` sont des consommateurs secondaires.

## 8_VALIDATED_PLAN

Plan validé pour cette ouverture :
- créer uniquement les documents de structure du parent ;
- ne pas modifier le runtime ;
- ne pas écrire dans les index globaux ;
- créer l'entrée inbox locale courte.

## 9_SELECTED_SOLUTION

Telegram Ingestion est le pipeline d'entrée des données Telegram. Le découplage
parser/normalisation/distribution est la contrainte architecturale centrale.

## 10_SELECTED_SETUP

Structure cible :

```text
modules/telegram_ingestion/
  parser/
    inbound_parser.py       <- lecture API Telegram
    message_schema.json     <- schéma des messages bruts
  normalizer/
    message_normalizer.py   <- normalisation en format canonique
    canonical_schema.json   <- schéma des messages normalisés
  distribution/
    consumer_router.py      <- routage vers consommateurs
  tests/
```

## 11_KEY_DECISIONS

- Le chantier est parent structurel ; aucun runtime modifié à l'ouverture.
- Les child GOs d'implémentation seront `GO_CHILD_ATTACHED_TO_PARENT` rattachés à ce parent.
- Pas de fermeture parent avant que `CLOSE_GATE_MASTER_TARGET` soit satisfait.

## 12_INVARIANTS

- Ne pas fermer le parent à l'ouverture.
- `GO_STRUCTURAL_ROLE: GO_PARENT_ATTACHED_TO_MASTER_PROJECT_PLAN` — permanent.
- Aucun ordre live.
- Pas de modification des index globaux.

## 13_ESTABLISHED

- `PF_TELEGRAM_INGESTION` identifié comme surface finale P1 dans `PRODUCT_FINAL_SURFACE_REGISTRY_01.md`.
- `MPP_TELEGRAM_INGESTION_OPERATIONAL` référencé dans `GO_INDEX.md` comme plan maître cible.
- Aucun composant d'ingestion Telegram normalisé n'existe dans le repo.

## 14_HYPOTHESIS

À valider par les child GOs :
- L'API Telegram (telethon) peut être utilisée pour ingérer les messages des canaux configurés.
- Les messages peuvent être normalisés en un format canonique unique.
- La distribution vers les consommateurs peut se faire sans perte de message.

## 15_REMAINING_GAP

- Aucun parser inbound Telegram n'existe.
- Aucune normalisation de messages.
- Aucune distribution vers les consommateurs.

## 16_TODO

1. Ouvrir `GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_INBOUND_PARSER_01` — implémenter parser inbound.
2. Formaliser le format de message canonique.
3. Établir la distribution vers Screener, Desk Pro, Data Center.

## 17_RESUME_POINT

Reprendre sur le premier child GO :

```text
GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_INBOUND_PARSER_01
```

---

## CLOSE_GATE_MASTER_TARGET

Le parent peut être fermé uniquement si toutes les conditions suivantes sont satisfaites :

```text
1. PF_TELEGRAM_INGESTION utilisable :
   - au moins 1 parser inbound opérationnel
   - ingestion prouvée en dry-run ou smoke réel

2. Normalisation :
   - format canonique des messages défini et versionné
   - au moins 2 types de messages normalisés

3. Tests de compatibilité :
   - tests smoke de l'ingestion passant en local ou CI

4. Documentation reprise :
   - gaps, couverture des sources et parseurs manquants documentés

5. Aucun gap bloquant non documenté.
```
