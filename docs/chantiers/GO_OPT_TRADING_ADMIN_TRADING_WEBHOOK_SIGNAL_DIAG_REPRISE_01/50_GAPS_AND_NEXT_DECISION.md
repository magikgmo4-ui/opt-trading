---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_REPRISE_01_GAPS_NEXT_DECISION
doc_type: gaps_next_decision
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_REPRISE_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-05
---

# 50_GAPS_AND_NEXT_DECISION - Gaps And Next Decision

## Schema gaps

- `event_type` n'existe pas encore explicitement dans l'evenement runtime
- `status` est implicite pour les evenements persistes et absent comme champ
- `errors` n'est pas persiste comme tableau canonique
- `timeframe`, `direction` et `timestamp` doivent etre mappes depuis `tf`, `signal` et `_ts`

## Runtime gaps

- le runtime persiste seulement les evenements `accepted`
- les chemins `skipped` et `rejected` existent au niveau HTTP mais pas comme evenements normalises persistants
- des `400 Bad Request` ont deja ete observes en runtime review, sans ecriture d'objet diagnostic structure dans `state/events.jsonl`

## Source / payload gaps

- aucun `payload_hash` ni `raw_payload_ref` n'est actuellement produit
- le payload TradingView exact amont n'est pas versionne dans cette documentation
- aucun timestamp d'origine alerte distinct du timestamp serveur n'est expose
- le champ `key` est valide en entree puis neutralise (`key: None`) dans l'evenement persiste, ce qui est conforme a la contrainte secret mais retire aussi une trace de provenance brute

## Consumer compatibility gaps

- Desk Pro futur ne doit pas consommer les alias V0 (`signal`, `tf`, `_ts`) directement
- la compatibilite cross-surface necessitera plus tard les refs `visual_context_ref` et `desk_snapshot_ref`
- la provenance payload et les statuts explicites seraient utiles avant toute integration reelle ou smoke global

## Safety gaps

- aucune preuve fonctionnelle en emission n'est autorisee ici
- aucune verification HMAC reelle n'est faite dans ce GO
- aucune requete live vers le tunnel ngrok ou vers TradingView externe n'est autorisee

## Decision

**PASS** vers `GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_HEADLESS_PIPELINE_REVIEW_01`

## Justification

- le producteur webhook et la persistance `state/events.jsonl` sont suffisamment compris pour definir `signal_event` V1
- les champs requis et optionnels sont maintenant arbitres documentairement
- les gaps restants sont reels, mais non bloquants pour ouvrir la revue du producteur `visual_context`

## Point de reprise

Si la suite est confirmee apres push, ouvrir :

`GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_HEADLESS_PIPELINE_REVIEW_01`
