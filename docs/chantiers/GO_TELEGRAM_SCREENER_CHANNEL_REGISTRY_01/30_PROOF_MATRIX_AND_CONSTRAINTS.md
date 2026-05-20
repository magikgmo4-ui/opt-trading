---
doc_id: GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01_PROOF_MATRIX_AND_CONSTRAINTS
doc_type: matrix
repo: opt-trading
go_id: GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01
status: active
source_kind: canonical
updated_at: 2026-05-19
---

# 30_PROOF_MATRIX_AND_CONSTRAINTS - Preuves et contraintes

## Contraintes sécurité

- aucun token Telegram dans le repo
- aucun channel_id/chat_id réel dans le repo
- ingestion inbound doit être opt-in (enabled=false par défaut)
- pas de couplage direct avec exécution trade (inbound → observation/event → gating)

## Preuves attendues (avant toute ingestion réelle)

| Preuve | Description | Critère |
| --- | --- | --- |
| Fixtures messages | corpus de messages (trade/setup/news) anonymisés | parsers testables offline |
| Parser dry-run | parse message → event envelope (GO_EVENT_TAXONOMY_01) | aucun side effect |
| Routing separation | inbound ne réutilise pas les destinations outbound | pas de boucles |
| Kill-switch | blocage exécution / ordres | invariants tests |

## Signal vs execute

Le screener inbound produit des **claims** et des **observations**, jamais des ordres:

- autorisé: WATCH/OBSERVE/CANDIDATE/INVALIDATED/REPLAY_READY
- interdit: BUY/SELL/EXECUTE/ORDER SENT

## Ancrage umbrella

- `MASTER_TARGET` : encadrer l'inbound screener du produit final total
- `Kanban bundle` : reste la carte de navigation principale
- `Prochain item Kanban exact` : `GO_DESKPRO_INPUT_EXPANSION_01`
- `Gaps encore ouverts` : fixtures messages anonymisees, parse contracts, separation inbound/outbound prouvee en implementation, kill-switch inbound dedie
