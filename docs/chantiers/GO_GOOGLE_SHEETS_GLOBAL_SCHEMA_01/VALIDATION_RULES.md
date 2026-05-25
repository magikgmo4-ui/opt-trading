---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01_VALIDATION_RULES
doc_type: validation_rules
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01
status: active
source_kind: canonical
updated_at: 2026-05-25
links:
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/CANONICAL_SHEETS.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/PRODUCER_CONSUMER_MAP.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_COLUMNS_CONTRACTS_01/10_COLUMNS_CONTRACTS.md
  - modules/validation_gate/README.md
---

# VALIDATION_RULES — Google Sheets global schema (V1)

## Objectif

Définir les règles de validation V1 permettant de valider :

- les fixtures (CSV/JSONL) associées aux tabs canoniques
- les lectures read-only (consumers) sans drift de schéma
- les écritures contrôlées (uniquement si un writer existe déjà et est explicitement activé)

Ce document est doc-first et fixtures-first : aucune dépendance à Google Sheets live.

## Portée

Sources normatives V1 :

- `CANONICAL_SHEETS.md` (liste des tabs + write_mode/read_mode)
- `10_COLUMNS_CONTRACTS.md` (contrats de colonnes tab par tab)

Hors-scope :

- toute écriture Sheets transverse non explicitement prouvée/activée
- tout collector live / API externe
- toute logique applicative nouvelle (ce child produit uniquement des règles)

## Terminologie

```text
row = ligne d’un tab (équivalent en fixture CSV ou en future lecture Sheets)
tab = worksheet / table logique (nom canonique)
contract = définition stable des colonnes et invariants pour un tab
fixture = dataset de test statique (CSV/JSONL) aligné sur un tab
```

## Sévérités V1

```text
FAIL  = violation bloquante (schéma invalide, risque de write incohérent, PK impossible)
WARN  = déviation tolérable mais à corriger (champ optionnel manquant, valeur inconnue non critique)
INFO  = observation (statistiques, coverage, hints)
```

Règle de base :

- toute fixture doit être 0 FAIL
- WARN acceptables uniquement si explicitement listés comme tolérances V1

## Règles globales (tous tabs)

### R1 — tab_name canonique

- FAIL si le tab n’est pas dans `CANONICAL_SHEETS.md`
- FAIL si la fixture utilise un nom différent (ex: `sheet1` au lieu de `daily_sessions`) sans mapping explicite (à documenter dans un futur child)

### R2 — schema_version

- `schema_version = v1` requis pour `sheets_registry` et recommandé partout ailleurs
- FAIL si `schema_version` existe et n’est pas reconnu (`v1` uniquement en V1)

### R3 — colonnes : required vs nullable

- FAIL si une colonne required du contrat est absente
- FAIL si une colonne required est présente mais vide/null
- WARN si une colonne nullable manque (si le contrat l’autorise)
- FAIL si une colonne inconnue est présente et que le mode de validation est `strict=true` (fixtures)
- WARN si une colonne inconnue est présente et `strict=false` (lecture tolérante)

### R4 — enums

- FAIL si une valeur enum est hors liste pour une colonne required
- WARN si une valeur enum est hors liste pour une colonne nullable et que la colonne est optionnelle (tolérance explicite requise)

### R5 — timestamps ISO UTC

Format unique V1 :

```text
YYYY-MM-DDTHH:MM:SSZ
```

- FAIL si une colonne de type `iso_utc_ts` ne respecte pas ce format
- WARN si une colonne timestamp est vide mais nullable

### R6 — primary key (PK) candidate

Pour chaque tab, une PK candidate est définie dans `CANONICAL_SHEETS.md` et/ou `10_COLUMNS_CONTRACTS.md`.

- FAIL si une ou plusieurs colonnes de PK candidate sont absentes
- FAIL si une PK candidate résolue est vide/null
- FAIL si la PK candidate est dupliquée dans une fixture (duplicate detection)

### R7 — duplicate detection

Duplicate = même PK candidate pour deux rows du même tab.

- FAIL sur fixtures
- WARN en lecture read-only si le consumer est en mode “best-effort” (à expliciter par consumer)

### R8 — *_ref (source_ref, payload_ref, snapshot_ref…)

Principes :

- un `*_ref` est une référence (path/id), pas un payload complet
- aucun secret / token / URL sensible dans un `*_ref`

Règles :

- FAIL si une colonne `*_ref` contient un JSON complet (heuristique : commence par `{` ou `[` et longueur > seuil)
- FAIL si un `*_ref` pointe vers un schéma non déterministe (ex: “latest” sans pin) pour une fixture
- WARN si un `*_ref` est vide et nullable

### R9 — write_mode constraints

Rappel `CANONICAL_SHEETS.md` :

- `doc_only` = aucune écriture
- `controlled_write (dry-run default)` = écriture possible uniquement si explicitement activée

Règles :

- FAIL si une tentative d’écriture (writer) cible un tab dont `write_mode != controlled_write`
- FAIL si write sans drapeau d’activation explicite (controlled-write), si applicable
- FAIL si write sans validation préalable “0 FAIL” des rows candidates

### R10 — read-only consumer expectations

Tout consumer read-only doit :

- refuser de “réparer” en écrivant (no side effects)
- reporter : nombre de rows, FAIL/WARN/INFO counts, et top reasons
- être déterministe sur les inputs (fixtures) : mêmes inputs => mêmes verdicts

## Règles spécifiques (extraits)

### daily_sessions

- `run_id` required, unique (FAIL duplicate)
- `status` enum: `success|fail|warn`
- `started_at` required iso_utc_ts
- `ended_at` nullable iso_utc_ts, mais FAIL si `ended_at < started_at`

### strategy_events

- `event_id` required, unique
- `event_type` required
- `event_ts` required iso_utc_ts
- `payload_ref` nullable, mais si présent doit référencer un artefact stable (fixture JSONL)

### market_metrics

- `as_of + symbol + metric_name` unique
- `value` float required
- `source_ref` nullable ; si présent, doit pointer vers view/artefact (pas vers un producer root)

## Validation gates (fixtures-first)

Ce document définit le “quoi valider”. L’“exécution des checks” peut être outillée.

Le module `validation_gate` existant dans le repo introduit des notions réutilisables :

- verdicts bornés (`APPROVED/REJECTED/HOLD/NEEDS_REVIEW`)
- séparation “auto-check” vs “operator approval”

Règle V1 pour le schéma Sheets :

- le schéma/fixtures doit d’abord produire un résultat strict “0 FAIL”
- toute exception (WARN tolérés) doit être documentée explicitement (liste de tolérances)
- l’approval opérateur (si utilisée) n’autorise jamais une violation FAIL

## Migration safety checks (V1)

- FAIL si suppression d’une colonne required sans bump de version
- FAIL si changement de type (ex: float -> string) sans migration_notes explicités
- WARN si ajout de colonne nullable (compatible) sans fixture mise à jour

