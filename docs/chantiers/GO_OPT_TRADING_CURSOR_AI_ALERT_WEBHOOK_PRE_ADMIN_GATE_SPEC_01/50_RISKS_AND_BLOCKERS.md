---
doc_id: GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_PRE_ADMIN_GATE_SPEC_01_50_RISKS_AND_BLOCKERS
doc_type: chantier/risks_and_blockers
repo: opt-trading
machine: cursor-ai
status: active
links:
  - bundles/NO_RUNTIME_NO_SENSITIVE_RULES.md
  - docs/chantiers/GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_ALERT_WEBHOOK_APPLICATION_ACTIVE_01/30_APPLICATION_REQUIREMENTS.md
---

# 50_RISKS_AND_BLOCKERS

Risques identifies et blockers pour alert_webhook avant ouverture admin-trading.

## Risques

### Risque 1 — Alerte reelle declenchee accidentellement

- **Scenario** : un operateur copie le template, remplit les champs avec des donnees reelles, et le push.
- **Impact** : l'alerte pourrait etre lue comme un signal de trading par admin-trading.
- **Mitigation** : flags `trade_allowed: false`, `admin_trading_runtime: false` actifs. Validation matrix check 3-4.

### Risque 2 — Secret ou token committe

- **Scenario** : un operateur ajoute un endpoint webhook reel avec token dans le template.
- **Impact** : fuite de credentials, acces non autorise au webhook.
- **Mitigation** : validation matrix check 2 et 8. `NO_RUNTIME_NO_SENSITIVE_RULES.md`.

### Risque 3 — Endpoint reel reference

- **Scenario** : une URL de production est ajoutee dans un fichier doc.
- **Impact** : un operateur pourrait l'utiliser par erreur.
- **Mitigation** : validation matrix check 8. Seul `127.0.0.1` ou `localhost` autorise en doc.

### Risque 4 — Runtime involontaire

- **Scenario** : un operateur ajoute un script d'envoi de payload dans `scripts/` ou `modules/`.
- **Impact** : execution de code non intentionnelle.
- **Mitigation** : validation matrix check 1 (non-doc files).

### Risque 5 — Confusion template vs application

- **Scenario** : un operateur pense que le template JSON est une application active.
- **Impact** : mauvaises decisions basees sur un template doc-only.
- **Mitigation** : le flag `mode: test_only` doit toujours etre present. Documenter explicitement.

### Risque 6 — Ouverture admin-trading sans validation

- **Scenario** : un operateur saute la spec de gate et ouvre admin-trading directement.
- **Impact** : violation des invariants cursor-ai.
- **Mitigation** : ce GO documente les criteres. La phrase "chantiers pour admin-trading" est requise.

## Blockers

| Blocker | Condition de levee |
| --- | --- |
| Demande explicite absente | L'operateur doit dire "chantiers pour admin-trading" |
| Validation matrix non PASSEE | Tous les checks 1-9 doivent etre PASS |
| `trade_allowed: true` | Ne jamais passer a `true` sans decision explicite |
| `admin_trading_runtime: true` | Ne jamais passer a `true` sans decision explicite |
| Secret dans le diff | Revert, rotation, documentation |

## Regle d'escalade

Si un risque se materialise :
1. Documenter l'incident dans le GO courant.
2. Revert si commit contenant l'element dangereux.
3. Rotation des tokens si applicable.
4. Reviser la spec de gate si necessaire.
