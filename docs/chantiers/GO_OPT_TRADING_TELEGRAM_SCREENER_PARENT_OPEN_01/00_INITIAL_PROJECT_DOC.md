---
doc_id: GO_OPT_TRADING_TELEGRAM_SCREENER_PARENT_OPEN_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: telegram_screener
go_id: GO_OPT_TRADING_TELEGRAM_SCREENER_PARENT_OPEN_01
parent_go_id: null
status: open
lifecycle_stage: planning
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-28
updated_at: 2026-05-28
GO_STRUCTURAL_ROLE: GO_PARENT_ATTACHED_TO_MASTER_PROJECT_PLAN
PF_ID: PF_TELEGRAM_SCREENER
MASTER_PROJECT_PLAN_ID: MPP_TELEGRAM_SCREENER_OPERATIONAL
MASTER_TARGET_ID: MT_TELEGRAM_SCREENER_OPERATIONAL
PARENT_GO_ID: null
BUNDLE_TARGET: null
NEXT_ATTACH_TARGET: null
NEXT_GO: GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SCREENER_PARSER_01
topic_keys:
  - opt-trading
  - telegram_screener
  - screener_parser
  - channel_registry
  - master_project_plan
links:
  - docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01_MASTER_PROJECT_PLAN_CREATION_RULE_01.md
  - docs/index/GO_INDEX.md
  - docs/index/REPRISE.md
  - docs/chantiers/GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_TELEGRAM_SCREENER_PARENT_OPEN_01/00_INITIAL_PROJECT_DOC.md
---

# GO_OPT_TRADING_TELEGRAM_SCREENER_PARENT_OPEN_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Telegram Screener opérationnel : les canaux Telegram inbound sont lus, parsés,
filtrés et redistribués vers Desk Pro et autres surfaces consommatrices.

La règle centrale est :

```text
channel registry -> parser -> screener signal -> Desk Pro
```

Composants identifiés :
- `GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01` — registry des canaux inbound
- `GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SCREENER_PARSER_01` — parser des signaux
- `PF_DESK_PRO` — surface consommatrice principale
- `PF_TELEGRAM_INGESTION` — ingestion amont

## 2_INITIAL_PROJECT_DOC

Ce document ouvre le parent canonique `PF_TELEGRAM_SCREENER` pour la première fois.

Il fige la structure de continuité du parent : `1_MASTER_TARGET`, `4_MASTER_PROJECT_PLAN`
et `CLOSE_GATE_MASTER_TARGET` déclarés, rattachement à `PF_TELEGRAM_SCREENER`
et `MPP_TELEGRAM_SCREENER_OPERATIONAL`.

Il ne ferme pas le parent. Il ne modifie pas les index globaux.

## 3_INITIAL_NEED

`PF_TELEGRAM_SCREENER` est référencé dans `PRODUCT_FINAL_SURFACE_REGISTRY_01.md`
comme surface finale P1 avec statut "à promouvoir — parent existant partiellement".
`GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01` existe comme chantier précurseur mais
n'a pas de parent canonique `GO_PARENT_ATTACHED_TO_MASTER_PROJECT_PLAN`.

Aucun parent Telegram Screener structuré n'existait avant cette ouverture.

L'ouverture est nécessaire avant tout child GO d'implémentation afin que les child GOs
puissent être rattachés (`GO_CHILD_ATTACHED_TO_PARENT`) à un parent canonique réel.

## 4_MASTER_PROJECT_PLAN

`MPP_TELEGRAM_SCREENER_OPERATIONAL`

1. **Channel registry** : formaliser le registry des canaux Telegram inbound avec catégories, trust tiers, parsers attendus (base posée par `GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01`).
2. **Screener parser** : implémenter le parsing des signaux trade/setup/news depuis les canaux configurés.
3. **Signal production** : produire des screener signals normalisés vers Desk Pro.
4. **Filtrage et routage** : règles de filtrage par canal, trust tier, type de signal.
5. **Tests de compatibilité** : valider le parsing et la production de signaux par tests smoke.
6. **Documentation reprise** : documenter les gaps, la couverture des canaux, les parsers manquants.

## 5_GO_PLAN

Chantier parent structurel. Cette ouverture est doc-first : aucun runtime modifié.

Sous-GO proposés (à ouvrir séquentiellement selon priorité opératoire) :

| GO_ID | Cible |
|---|---|
| `GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SCREENER_PARSER_01` | Implémenter le parser des signaux screener |
| `GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_CHANNEL_REGISTRY_OPEN_01` | Promouvoir le channel registry en parent dédié |
| `GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SIGNAL_PRODUCER_01` | Produire des screener signals vers Desk Pro |

Premier child recommandé : `GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SCREENER_PARSER_01`.

## 6_FINAL_TARGET

Livrable de cette ouverture : un parent canonique `GO_OPT_TRADING_TELEGRAM_SCREENER_PARENT_OPEN_01`
structuré avec `1_MASTER_TARGET`, `4_MASTER_PROJECT_PLAN` et `CLOSE_GATE_MASTER_TARGET`
déclarés, rattaché à `PF_TELEGRAM_SCREENER` et `MPP_TELEGRAM_SCREENER_OPERATIONAL`,
prêt à recevoir les child GOs d'implémentation.

## 7_CANONICAL_STATE

- `PF_TELEGRAM_SCREENER` dans `PRODUCT_FINAL_SURFACE_REGISTRY_01.md` comme surface finale P1 "à promouvoir".
- `GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01` existe comme chantier précurseur — registry des canaux posé.
- `GO_OPT_TRADING_TELEGRAM_SCREENER_PARENT_OPEN_01` n'existait pas avant cette ouverture ; ce document en est l'acte de création.
- Aucun parser de signaux screener n'existe dans le repo.
- Aucune production de screener signals normalisés vers Desk Pro.
- `PF_TELEGRAM_INGESTION` est le producteur amont ; `PF_DESK_PRO` est le consommateur aval.

## 8_VALIDATED_PLAN

Plan validé pour cette ouverture :
- créer uniquement les documents de structure du parent ;
- ne pas modifier le runtime ;
- ne pas écrire dans les index globaux (GO_INDEX, ACTIVE_STREAMS, REPRISE) sauf si modification réelle de l'horizon ;
- créer l'entrée inbox locale courte ;
- noter le chemin de bundle/patch pour transport futur.

## 9_SELECTED_SOLUTION

Telegram Screener est un pipeline de traitement de signaux : registry → parser → signal → Desk Pro.
Le découplage channel/parser/signal est la contrainte architecturale centrale. Chaque couche
doit être déclarée, versionnée et testée indépendamment.

`GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01` est adopté comme fondation du channel registry.

## 10_SELECTED_SETUP

Structure cible :

```text
modules/telegram_screener/
  registry/
    channels.json        <- registry des canaux configurés
    channel_schema.json  <- schéma de validation des canaux
  parsers/
    trade_parser.py
    setup_parser.py
    news_parser.py
  signals/
    signal_producer.py
    signal_schema.json
  tests/
```

## 11_KEY_DECISIONS

- Le chantier est parent structurel ; aucun runtime modifié à l'ouverture.
- `GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01` est le fondement du channel registry.
- Les child GOs d'implémentation seront `GO_CHILD_ATTACHED_TO_PARENT` rattachés à ce parent.
- Pas de fermeture parent avant que `CLOSE_GATE_MASTER_TARGET` soit satisfait.

## 12_INVARIANTS

- Ne pas fermer le parent à l'ouverture.
- `GO_STRUCTURAL_ROLE: GO_PARENT_ATTACHED_TO_MASTER_PROJECT_PLAN` — permanent.
- Aucun ordre live.
- Aucune écriture Google Sheets globale.
- Aucun Telegram live.
- Aucune ingestion DB active.
- Pas de modification des index globaux sauf si le master target ou l'horizon change réellement.

## 13_ESTABLISHED

- `PF_TELEGRAM_SCREENER` identifié comme surface finale P1 dans `PRODUCT_FINAL_SURFACE_REGISTRY_01.md`.
- `MPP_TELEGRAM_SCREENER_OPERATIONAL` référencé dans `GO_INDEX.md` comme plan maître cible.
- `GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01` existant comme chantier précurseur avec registry des canaux.
- La règle `channel registry -> parser -> screener signal -> Desk Pro` canonisée.

## 14_HYPOTHESIS

À valider par les child GOs :
- Les canaux Telegram inbound peuvent être parsés de manière fiable (trade/setup/news).
- Les signaux parsés peuvent être normalisés en screener signals pour Desk Pro.
- Le filtrage par trust tier et type de signal est pertinent pour la qualité des signaux.

## 15_REMAINING_GAP

- Aucun parser de signaux screener n'existe.
- Aucune production de screener signals normalisés.
- `PF_TELEGRAM_INGESTION` amont non connecté.
- Tests de parsing absents.

## 16_TODO

1. Ouvrir `GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SCREENER_PARSER_01` — implémenter parser.
2. Formaliser le channel registry comme composant canonique.
3. Établir production de screener signals vers Desk Pro.

## 17_RESUME_POINT

Reprendre sur le premier child GO :

```text
GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_SCREENER_PARSER_01
```

---

## CLOSE_GATE_MASTER_TARGET

Le parent peut être fermé uniquement si toutes les conditions suivantes sont satisfaites :

```text
1. PF_TELEGRAM_SCREENER utilisable :
   - au moins 1 parser de signaux opérationnel
   - production de screener signals prouvée en dry-run ou smoke réel

2. Channel registry :
   - registry des canaux formalisé et versionné
   - au moins 2 canaux configurés et parsés

3. Tests de compatibilité :
   - tests smoke du parsing passant en local ou CI

4. Documentation reprise :
   - gaps, couverture des canaux et parsers manquants documentés

5. Aucun gap bloquant non documenté.
```

---

## BUNDLE / PATCH

Artefacts de transport prévus (à créer lors des child GOs d'implémentation) :

```text
bundles/GO_OPT_TRADING_TELEGRAM_SCREENER_PARENT_OPEN_01/
  TARGETS.md
  bundle_meta/target_card.json
  patches/<YYYYMMDD>_GO_OPT_TRADING_TELEGRAM_SCREENER_PARENT_OPEN_01_open.patch
```

Pour l'ouverture seule (ce document) :

```text
docs/chantiers/GO_OPT_TRADING_TELEGRAM_SCREENER_PARENT_OPEN_01/patches/
  20260528_GO_OPT_TRADING_TELEGRAM_SCREENER_PARENT_OPEN_01_opening.patch
```
