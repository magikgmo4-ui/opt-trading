---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_REPRISE_01_SIGNAL_PRODUCER_CONTRACT_DRAFT
doc_type: producer_contract_draft
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_REPRISE_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-05
---

# 40_SIGNAL_PRODUCER_CONTRACT_DRAFT - Signal Producer Contract Draft

## Producer

- producer: `Webhook / TradingView`
- ingress confirme: `POST /tv`
- persistance normalisee documentee: `state/events.jsonl`
- consumer futur: `GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_01` puis `Desk Pro`

## Observation implementation actuelle

La route `POST /tv` lit actuellement un payload avec au minimum :

- `key`
- `engine`
- `signal`
- `symbol`
- `tf`
- `price`
- `tp`
- `sl`
- `reason`

Puis elle normalise un evenement interne contenant notamment :

- `engine`
- `signal`
- `symbol`
- `tf`
- `price`
- `tp`
- `sl`
- `reason`
- `_ts`
- `_ip`
- `qty`
- `risk_usd`
- `risk_real_usd`

## Brouillon contractuel propose pour `signal_event`

Format attendu: `JSON / event contract`

| Champ | Type | Statut | Note |
| --- | --- | --- | --- |
| `source` | string | requis | valeur proposee: `tradingview.webhook` |
| `symbol` | string | requis | symbole runtime consomme downstream |
| `timeframe` | string | requis | mappe depuis `tf` |
| `event_type` | string | requis | valeur proposee: `signal_event` |
| `direction` | string | requis | normaliser en `BUY` ou `SELL`; un mapping secondaire vers `LONG` ou `SHORT` peut rester derive |
| `timestamp` | string ISO-8601 | requis | mappe depuis `_ts` ou horodatage equivalent du producer |
| `raw_payload_ref` ou `payload_hash` | string | requis | permet de referencer le payload source sans le dupliquer integralement dans le consumer |
| `risk_context_ref` | string ou null | optionnel | reference vers quote ou contexte risque aval |
| `visual_context_ref` | string ou null | optionnel futur | reference de couplage futur avec Bot Vision si necessaire |
| `status` | string | requis | valeurs candidates: `accepted`, `rejected`, `skipped`, `error` |
| `errors` | array ou null | requis | liste vide ou details de rejet/validation |

## Champs implementation actuelle a recroiser au GO suivant

Ces champs sont observes dans le runtime actuel et devront etre arbitres au prochain GO :

- `engine`
- `price`
- `tp`
- `sl`
- `reason`
- `qty`
- `risk_usd`
- `risk_real_usd`
- `_ip`

Question ouverte pour `WEBHOOK_SIGNAL_DIAG` : ces champs sont-ils canoniques dans `signal_event`, ou doivent-ils etre reclasses sous `meta`, `risk_context` ou `execution_context` ?

## Frontiere producer/consumer retenue ici

- ce GO confirme le producer et le flux d'entree
- ce GO propose un brouillon de contrat
- le GO suivant doit valider le schema exact, la fraicheur, les statuts et les cas d'erreur
