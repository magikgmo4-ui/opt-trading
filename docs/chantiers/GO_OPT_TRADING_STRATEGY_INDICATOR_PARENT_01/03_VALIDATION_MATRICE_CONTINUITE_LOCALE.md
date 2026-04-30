---
doc_id: GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01_VALIDATION_MATRICE_CONTINUITE_LOCALE
doc_type: chantier_validation_matrix
repo: opt-trading
project: opt-trading
module: strategy_indicator
go_id: GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01
status: draft
lifecycle_stage: validation
chantier_parent: GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01
sous_chantier: GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_01
topic_keys:
  - opt-trading
  - strategy_indicator
  - continuity
  - local_indexation
  - global_indexes
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section 17_RESUME_POINT"
updated_at: 2026-04-30
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01/00_CADRAGE.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01/02_PLAN_COMPLET_LOGIQUE.md
  - docs/index/inbox/GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01.md
---

# VALIDATION MATRICE — continuité locale du parent

## 1_MASTER_TARGET

Valider explicitement que le parent `GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01` porte sa continuité locale dans son propre dossier chantier, afin d'éviter de modifier les index globaux à chaque micro-évolution du sous-chantier.

## 2_INITIAL_PROJECT_DOC

Document parent de référence :

`docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01/00_CADRAGE.md`

Document de plan complet :

`docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01/02_PLAN_COMPLET_LOGIQUE.md`

## 3_INITIAL_NEED

Fixer la règle opératoire suivante pour ce parent :

- la continuité courante du chantier est sauvegardée localement dans `docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01/` ;
- les index globaux ne sont pas modifiés à chaque étape ;
- une entrée courte atomique existe dans `docs/index/inbox/` pour préparer l'agrégation future ;
- les index globaux sont réservés aux batchs d'agrégation, aux ouvertures/fermetures significatives ou aux changements de statut structurants.

## 4_MASTER_PROJECT_PLAN

### Règle validée

Le parent agit comme conteneur de continuité locale.

Les fichiers suivants constituent la continuité locale immédiate :

```text
docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01/
  00_CADRAGE.md
  01_MASTER_PLAN.md
  02_PLAN_COMPLET_LOGIQUE.md
  03_VALIDATION_MATRICE_CONTINUITE_LOCALE.md
  BRANCH_STATE.md
```

Le child conserve sa continuité propre ici :

```text
docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_01/
  00_CADRAGE.md
  01_SPEC.md
  02_RULES.md
  03_TODO.md
  REPRISE.md
```

L'indexation globale différée est préparée ici :

```text
docs/index/inbox/GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01.md
```

## 7_CANONICAL_STATE

- Parent créé.
- Child initial créé.
- Plan complet logique créé.
- Continuité locale validée dans le dossier parent.
- Inbox atomique créée.
- Aucun index global (`GO_INDEX.md`, `ACTIVE_STREAMS.md`, `NEXT_GO_CANDIDATES.md`, `REPRISE.md`) n'est modifié dans cette étape.

## 8_VALIDATED_PLAN

### Quand modifier seulement le chantier parent

Modifier seulement le dossier parent si :

- on ajoute une décision locale ;
- on met à jour un TODO local ;
- on ajoute une hypothèse à valider ;
- on documente un point de reprise ;
- on ajoute un sous-fichier de plan ou de preuve sans changement global de statut.

### Quand modifier `docs/index/inbox/`

Modifier l'entrée inbox si :

- le résumé atomique du parent change ;
- un child est ajouté ;
- le point de reprise global du parent change ;
- une agrégation future doit voir une nouvelle information courte.

### Quand modifier les index globaux

Modifier les index globaux seulement si :

- le parent est officiellement ajouté à la liste canonique globale ;
- le parent passe actif / bloqué / clos ;
- le next GO global change ;
- un batch d'agrégation d'index est explicitement ouvert ;
- une fermeture de parent exige propagation.

## 11_KEY_DECISIONS

- `GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01` garde sa continuité dans son dossier parent.
- L'entrée `docs/index/inbox/GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01.md` sert de tampon atomique.
- Les gros index globaux ne sont pas une surface de journalisation quotidienne.
- L'agrégation vers les index globaux reste un acte séparé et batché.

## 12_INVARIANTS

- Ne pas modifier `GO_INDEX.md` à chaque micro-avancement.
- Ne pas modifier `ACTIVE_STREAMS.md` à chaque note locale.
- Ne pas modifier `NEXT_GO_CANDIDATES.md` sans changement réel du prochain GO global.
- Ne pas modifier `REPRISE.md` global si la reprise locale est suffisante.
- Garder la continuité locale lisible dans le parent.
- Garder une entrée inbox courte par parent.

## 13_ESTABLISHED

- La continuité locale du parent est maintenant explicitement documentée.
- La règle d'indexation différée est fixée pour ce parent.
- Le chantier reste conforme à la méthode : continuité locale complète + inbox atomique + agrégation globale par batch.

## 15_REMAINING_GAP

- L'agrégation globale n'est pas encore faite.
- Le parent n'est pas encore fermé.
- Le child oil macro n'a pas encore son schema machine-readable.

## 16_TODO

1. À la reprise, rebaser la branche sur `origin/sot/mainline`.
2. Corriger les frontmatters signalés si encore présents.
3. Continuer dans le parent sans toucher les index globaux tant que le statut global ne change pas.
4. Ouvrir ensuite `GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_SCHEMA_02`.

## 17_RESUME_POINT

Reprendre ici :

```bash
git fetch --all --prune
git checkout go/GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01
git rebase origin/sot/mainline
```

Puis relire :

```text
docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01/02_PLAN_COMPLET_LOGIQUE.md
docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01/03_VALIDATION_MATRICE_CONTINUITE_LOCALE.md
```

## 18_TO_DOCUMENT

- `STRATEGY_INDICATOR_PARENT_CLOSEOUT_01`
- `OIL_MACRO_SCHEMA_V1`
- `INDEX_AGGREGATION_BATCH_IF_NEEDED`

## 19_TO_REMEMBER

- La continuité du parent strategy / indicator est locale au dossier parent.
- Les index globaux ne sont pas modifiés à chaque micro-étape.
- L'entrée inbox atomique sert de tampon avant agrégation globale.
