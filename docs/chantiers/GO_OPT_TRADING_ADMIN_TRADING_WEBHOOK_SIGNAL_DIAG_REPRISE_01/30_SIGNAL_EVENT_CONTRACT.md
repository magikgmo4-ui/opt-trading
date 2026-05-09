---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_REPRISE_01_SIGNAL_EVENT_CONTRACT
doc_type: signal_event_contract
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_REPRISE_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-05
---

# 30_SIGNAL_EVENT_CONTRACT - Signal Event Contract V1

## Objet

Definir un contrat canonique `signal_event` V1 consumable par les GO suivants sans dependre des noms internes `signal`, `tf` et `_ts` du runtime actuel.

## JSON schema documentaire minimal

```json
{
  "type": "object",
  "required": [
    "source",
    "event_type",
    "engine",
    "symbol",
    "timeframe",
    "direction",
    "timestamp",
    "status"
  ],
  "properties": {
    "source": {"type": "string", "enum": ["tradingview.webhook"]},
    "event_type": {"type": "string", "const": "signal_event"},
    "engine": {"type": "string"},
    "symbol": {"type": "string"},
    "timeframe": {"type": "string"},
    "direction": {"type": "string", "enum": ["BUY", "SELL"]},
    "timestamp": {"type": "string", "format": "date-time"},
    "status": {"type": "string", "enum": ["accepted", "rejected", "skipped", "error"]},
    "payload_hash": {"type": ["string", "null"]},
    "raw_payload_ref": {"type": ["string", "null"]},
    "meta": {"type": ["object", "null"]},
    "risk_context": {"type": ["object", "null"]},
    "visual_context_ref": {"type": ["string", "null"]},
    "desk_snapshot_ref": {"type": ["string", "null"]},
    "errors": {"type": "array"}
  }
}
```

## Mapping V0 runtime -> V1 canonique

| Runtime actuel | Contrat V1 | Statut |
| --- | --- | --- |
| `engine` | `engine` | direct |
| `symbol` | `symbol` | direct |
| `tf` | `timeframe` | rename |
| `signal` | `direction` | rename |
| `_ts` | `timestamp` | rename |
| constante route `/tv` | `source` | derive |
| constante de contrat | `event_type` | derive |
| persistance reussie de `evt` | `status=accepted` | derive |
| `price`, `tp`, `sl`, `reason` | `meta` | regroupement recommande |
| `qty`, `risk_usd`, `risk_real_usd` | `risk_context` | regroupement recommande |
| `_ip` | hors contrat canonique ou `meta.debug.client_ip` | optionnel |

## Required fields

- `source`
- `event_type`
- `engine`
- `symbol`
- `timeframe`
- `direction`
- `timestamp`
- `status`

## Optional fields

- `payload_hash`
- `raw_payload_ref`
- `meta`
- `risk_context`
- `visual_context_ref`
- `desk_snapshot_ref`
- `errors`

## Error semantics

- `accepted`: le signal a franchi les validations et un evenement normalise est persiste
- `rejected`: erreur de validation metier ou d'acces, typiquement `400`, `403` ou `409`
- `skipped`: signal volontairement ignore sans prise en compte downstream, par exemple `already_buy` / `already_sell`
- `error`: erreur serveur inattendue ou panne d'integration aval

Etat actuel du runtime :

- seul le chemin `accepted` est persiste comme evenement `evt`
- `rejected` est aujourd'hui porte par `HTTPException.detail`, pas par un objet `signal_event` persiste
- `skipped` peut etre retourne en HTTP `200` sans ecriture d'evenement

## No-trade semantics

- `no-trade` n'est pas un type d'evenement separe dans le runtime actuel
- en V1, le comportement `no-trade` doit etre encode via `status=skipped`
- tant que le producteur n'ecrit pas explicitement les `skipped`, un consumer ne doit pas deduire leur absence depuis `state/events.jsonl`

## Timestamp semantics

- `timestamp` V1 represente le moment d'acceptation/normalisation par le serveur webhook
- le champ runtime source est `_ts`
- format attendu: ISO-8601 UTC compatible `datetime.fromisoformat`
- aucun timestamp d'origine TradingView distinct n'est actuellement expose

## Payload provenance semantics

- objectif prefere: fournir au moins un des deux champs `payload_hash` ou `raw_payload_ref`
- etat actuel: aucun des deux n'est produit
- decision V1: ces champs restent optionnels pour la compatibilite read-only immediate, mais deviennent fortement recommandes avant toute chaine de replay, smoke global ou forensic deeper

## Compatibilite avec Desk Pro futur consumer

- Desk Pro ne doit pas consommer directement les alias V0 (`signal`, `tf`, `_ts`)
- Desk Pro futur doit se brancher sur les noms V1 (`direction`, `timeframe`, `timestamp`, `status`)
- `engine` reste requis pour conserver la semantique de routage et la coherence avec les metrics actuelles
- `visual_context_ref` et `desk_snapshot_ref` sont prepares pour la phase ou le webhook sera enrichi par Bot Vision et Desk Bridge

## Verdict de definition

`signal_event` V1 peut etre defini proprement en l'etat, a condition d'accepter une couche de mapping documentaire entre le runtime actuel et le contrat canonique futur.
