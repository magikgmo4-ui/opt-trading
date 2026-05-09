---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_REPRISE_01_PAYLOAD_FIELDS_AUDIT
doc_type: payload_fields_audit
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_REPRISE_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-05
---

# 20_PAYLOAD_FIELDS_AUDIT - Payload Fields Audit

## Regle de classement

- `CONFIRMED` = champ present tel quel dans le payload ou l'evenement normalise
- `DERIVED` = champ non stocke tel quel mais calculable de facon fiable
- `MISSING` = champ absent du runtime actuel et non derivable proprement
- `OPTIONAL` = champ facultatif acceptable en V1
- `HYPOTHESIS` = champ propose mais non prouvable proprement sur l'etat actuel

## Audit des champs cibles

| Champ cible | Etat | Source runtime actuelle | Note |
| --- | --- | --- | --- |
| `source` | DERIVED | ingress `/tv` + producteur webhook | aucun champ `source` explicite dans `evt`; la provenance est inferable depuis la route productrice |
| `symbol` | CONFIRMED | `payload.symbol` -> `evt.symbol` | champ present et consomme par metrics / dashboard |
| `timeframe` | DERIVED | `payload.tf` -> `evt.tf` | V1 doit renommer `tf` en `timeframe` |
| `event_type` | MISSING | aucun champ dedie | la valeur canonique `signal_event` doit etre ajoutee par contrat ou mapping |
| `direction` | DERIVED | `payload.signal` -> `evt.signal` | V1 peut normaliser `BUY` / `SELL` comme direction canonique; `LONG` / `SHORT` reste derive pour perf |
| `timestamp` | DERIVED | `evt._ts` | `_ts` existe et est parse en ISO-8601; V1 doit l'exposer sous `timestamp` |
| `raw_payload_ref` ou `payload_hash` | MISSING | aucun champ dedie | pas de reference brute ni hash persiste dans l'evenement normalise actuel |
| `risk_context_ref` | OPTIONAL | aucun ref; `qty`, `risk_usd`, `risk_real_usd` inline | V1 peut rester compatible avec un objet ou une ref risque facultative |
| `visual_context_ref` | OPTIONAL | aucun champ actuel | champ de couplage futur pour Bot Vision, hors producteur webhook actuel |
| `status` | DERIVED | reponse HTTP / chemins de sortie | les evenements persistes impliquent `accepted`; `skipped` et `rejected` existent au niveau reponse/exception mais pas comme champ persiste |
| `errors` | MISSING | erreurs seulement en `HTTPException.detail` | aucune liste d'erreurs dans l'evenement persiste |

## Champs runtime observes hors liste cible

| Champ observe | Etat | Note |
| --- | --- | --- |
| `engine` | CONFIRMED | champ critique du runtime actuel; doit rester requis en V1 meme s'il n'etait pas dans la liste minimale initiale |
| `price` | CONFIRMED | valeur de marche lue dans le payload et persistee |
| `tp` | CONFIRMED | take profit lu et persiste |
| `sl` | CONFIRMED | stop loss lu et persiste; conditionne la quote de risque |
| `reason` | CONFIRMED | libre / potentiellement vide |
| `qty` | DERIVED | produit par `risk_quote()` avant persistance |
| `risk_usd` | DERIVED | produit par `risk_quote()` |
| `risk_real_usd` | DERIVED | produit par `risk_quote()` |
| `_ip` | OPTIONAL | utile pour audit local; pas recommande comme champ consumer canonique |
| `key` | HYPOTHESIS | present seulement en entree; explicitement retire de l'evenement persiste (`key: None`) |

## Lecture retenue

Le runtime actuel expose deja un noyau exploitable (`engine`, `signal`, `symbol`, `tf`, `_ts`, `qty`, `risk_*`), mais le contrat `signal_event` V1 demande encore une canonisation de noms et l'ajout logique de semantiques `event_type`, `status`, `errors` et `payload provenance`.
