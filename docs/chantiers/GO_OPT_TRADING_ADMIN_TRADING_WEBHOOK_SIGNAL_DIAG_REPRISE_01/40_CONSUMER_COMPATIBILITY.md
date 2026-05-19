---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_REPRISE_01_CONSUMER_COMPATIBILITY
doc_type: consumer_compatibility
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_REPRISE_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-05
---

# 40_CONSUMER_COMPATIBILITY - Producer Consumer Compatibility

## Producteur retenu

- producer: `Webhook / TradingView`
- artefact vise: `signal_event`

## Consommateurs retenus

- consumer direct present: `GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_REPRISE_01`
- consumer direct futur: `Desk Pro`
- consumer indirect futur: `Bot Vision Headless` via `visual_context_ref`
- consumer indirect futur: `Desk Bridge` via `desk_snapshot_ref`

## Matrice de compatibilite

| Producer | Artifact | Consumer | Required fields | Optional fields | Blocking gaps |
| --- | --- | --- | --- | --- | --- |
| Webhook / TradingView | raw alert payload | `WEBHOOK_SIGNAL_DIAG_REPRISE_01` | `engine`, `signal`, `symbol`, `tf`, `price`, `sl` | `tp`, `reason`, `key` | pas de `event_type`; pas de `timestamp` canonique avant normalisation; pas de provenance payload stable |
| `tv_webhook()` normalizer | runtime event V0 (`evt`) | `WEBHOOK_SIGNAL_DIAG_REPRISE_01` | `engine`, `signal`, `symbol`, `tf`, `_ts` | `price`, `tp`, `sl`, `reason`, `qty`, `risk_usd`, `risk_real_usd`, `_ip` | `source`, `event_type`, `status`, `errors`, `payload_hash/raw_payload_ref` non explicites |
| Webhook / TradingView | `signal_event` V1 canonique | Desk Pro futur | `source`, `event_type`, `engine`, `symbol`, `timeframe`, `direction`, `timestamp`, `status` | `payload_hash`, `raw_payload_ref`, `meta`, `risk_context`, `visual_context_ref`, `desk_snapshot_ref`, `errors` | le runtime actuel necessite encore un mapping ou une evolution producteur pour provenance + statut explicite |
| Bot Vision Headless / Desk Bridge | enriched references | Desk Pro futur | `symbol`, `timeframe`, `timestamp` alignes avec `signal_event` | `visual_context_ref`, `desk_snapshot_ref` | depend de GO suivants; hors producteur webhook pur |

## Lecture compatibilite

- le producer actuel est compatible avec une lecture diagnostique immediate
- le producer actuel n'est pas encore strictement isomorphe au contrat `signal_event` V1, car plusieurs semantiques restent implicites
- Desk Pro futur peut rester compatible si la consommation se fait sur le contrat V1 et non sur les noms internes V0
- `visual_context_ref` et `desk_snapshot_ref` ne sont pas des gaps bloquants pour ce GO, mais des champs de raccordement pour les child GO suivants
