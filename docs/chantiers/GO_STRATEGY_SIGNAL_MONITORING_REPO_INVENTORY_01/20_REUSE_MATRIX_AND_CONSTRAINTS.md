---
doc_id: GO_STRATEGY_SIGNAL_MONITORING_REPO_INVENTORY_01_REUSE_MATRIX_AND_CONSTRAINTS
doc_type: reuse_matrix
repo: opt-trading
go_id: GO_STRATEGY_SIGNAL_MONITORING_REPO_INVENTORY_01
status: reference
source_kind: canonical
updated_at: 2026-05-19
---

# 20_REUSE_MATRIX_AND_CONSTRAINTS - Réutilisation vs gaps (bundle)

## Matrice (bundle "signal chain total product" → repo réel)

| Besoin bundle | Ce qui existe déjà | Réutilisation recommandée | Gap réel |
| --- | --- | --- | --- |
| Repo inventory (pré-requis) | Surfaces prouvées: webhook, 7 workers, Desk Pro, dispatcher, Telegram outbound, Sheets daily sync, bot vision family | Utiliser `10_CHAIN_SURFACE_PROOF_MAP.md` comme baseline unique | Nécessite encore taxonomy/events/routing pour une chaîne totale |
| Event taxonomy | `schemas/webhook_event_v1.json` + contrats implicites dans `modules/*/app/schema.py` | Dériver une enveloppe canonique depuis les dataclasses existantes + `signal_event` V1 (Desk Pro adapter) | Pas de doc canonique transverse "event envelope" |
| Telegram routing map | Outbound helper `shared/telegram_notify.py` + dispatcher `modules/notification_dispatcher/` | Centraliser routing à l'entrée du dispatcher (topics/chats/bots) | Pas de map canonique events→destinations |
| Telegram screener inbound | Botpress adapter `adapter_botpress_openclaw.py` (intent-based) | Garder séparé de la chaîne tradingview; réutiliser patterns safety/rate-limit/circuit | Pas de parser inbound "trades/setups" ni de registry channels |
| Desk Pro hub expansion | Desk Pro modules (api/ui/service) + dry-run synthesis 3 inputs | Continuer via dry-run + fixtures avant toute lecture de fichiers live | Besoin d’un mapping contractuel plus complet (inputs/outputs classes) |
| Google Sheets global schema | `scripts/sheets/sync_daily_session.py` (journal sync) + writer dry-run | Étendre seulement après schema global défini et gates (no live writes) | Schema transverse + writer global absent |
| Bot Vision/headless integration | Famille présente: `modules/bot_vision/`, `modules/vision_bot/`, `modules/bot_vision_step2/`, `modules/desk_analyze/` | Réutiliser family, mais imposer un survivant canonique avant E2E | Family non unifiée (interfaces multiples) |
| Perf / scoring | `modules/perf/` + `modules/perf_engine/` | Réutiliser `modules/perf_engine/` comme surface principale; brancher sur fixtures d’abord | Score latency transverse non fixé |
| Strategy registry update | `modules/strategy/registry.py` + `registry/*.yaml` | Garder registry read-only tant que backtest/gates pas prouvés | Entrée telegram latency non validée |

## Conclusion

Le repo contient déjà une base exploitable. Le verrou principal avant implémentation lourde reste la normalisation transverse (taxonomie d’événements + routing), puis l’extension Telegram inbound / Sheets global sous gates.

## Ancrage umbrella

- `MASTER_TARGET` : alimenter le produit final total sans fermer le parent umbrella
- `Kanban bundle` : reste la carte de navigation principale ; ce document ne la remplace pas
- `Prochain item Kanban exact` : `GO_EVENT_TAXONOMY_01`
- `Produit final total voulu` : chaines separees mais liees entre webhook, Desk Pro, Telegram, Sheets, Perf et runtime
- `Gaps encore ouverts` : taxonomy transverse, routing outbound, inbound Telegram screener, schema Sheets global, score latency transverse
