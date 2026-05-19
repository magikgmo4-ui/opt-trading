# App Bridges Gates

## Airtable

Bridge existant : `modules/airtable_bridge/` (client REST, 4 payloads, fail-open).

| Action | READ_ONLY | DRAFT_ONLY | WRITE_GATED |
|---|---|---|---|
| Lire les tables (Trades, Signals, Backtests, GO_Status) | ✅ autorisé | ✅ autorisé | ✅ autorisé |
| Écrire un record | ❌ bloqué | ❌ bloqué | ✅ avec validation |
| Modifier un record existant | ❌ bloqué | ❌ bloqué | ❌ interdit V1 |
| Supprimer un record | ❌ bloqué | ❌ bloqué | ❌ interdit |

Règles : fail-open (jamais bloquant), batch max 10, retry 3x sur 429, timeout 10s.
Interdits : devenir DB canonique, stocker secrets, remplacer le registry.

## ClickUp

Bridge existant : `execute_clickup.py` (cockpit partiel, 4/6 espaces).

| Action | READ_ONLY | DRAFT_ONLY | WRITE_GATED |
|---|---|---|---|
| Lire les tâches / espaces | ✅ autorisé | ✅ autorisé | ✅ autorisé |
| Proposer un statut (PATCH_DRAFT) | ❌ bloqué | ✅ draft-only | ✅ avec validation |
| Créer une tâche GO | ❌ bloqué | ❌ bloqué | ❌ interdit V1 |
| Marquer PASS sans preuve repo | ❌ bloqué | ❌ bloqué | ❌ interdit |

Règles : ne pas modifier le script `execute_clickup.py` existant, tout passage par le cockpit ClickUp est loggé.
Interdits : créer un GO canonique, marquer PASS sans commit correspondant.

## Botpress

Bridge existant : `docs/chantiers/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01/` (cadrage, API contract, safety gate).

| Action | READ_ONLY | DRAFT_ONLY | WRITE_GATED |
|---|---|---|---|
| Router un intent (screener, analysis, journal, status, help) | ✅ autorisé | ✅ autorisé | ✅ autorisé |
| Écrire dans Botpress (conversation) | ❌ bloqué | ✅ draft-only | ❌ interdit V1 |
| Déclencher un trade | ❌ bloqué | ❌ bloqué | ❌ interdit |
| Push git via Botpress | ❌ bloqué | ❌ bloqué | ❌ interdit |

Règles : safety gate obligatoire, dry_run=true par défaut, pas de trade réel V1.
Interdits : trade réel, git push, bypass safety gate.

## Telegram

Bridge : notification seulement.

| Action | READ_ONLY | DRAFT_ONLY | WRITE_GATED |
|---|---|---|---|
| Envoyer une notification | ✅ autorisé | ✅ autorisé | ✅ autorisé |
| Lire des messages | ❌ bloqué | ❌ bloqué | ❌ interdit V1 |
| Commande destructive | ❌ bloqué | ❌ bloqué | ❌ interdit |

Règles : notification only, pas de commande entrante interprétée.
Interdits : trade réel, modification repo, lecture de credentials.

## Google Sheets

Bridge : journal / reporting.

| Action | READ_ONLY | DRAFT_ONLY | WRITE_GATED |
|---|---|---|---|
| Lire une feuille de journal | ✅ autorisé | ✅ autorisé | ✅ autorisé |
| Ajouter une ligne de log | ❌ bloqué | ✅ draft-only | ✅ avec validation |
| Modifier une cellule existante | ❌ bloqué | ❌ bloqué | ❌ interdit |

Règles : reporting only, pas source canonique de vérité.
Interdits : devenir source canonique, stocker des données de trading critiques.
