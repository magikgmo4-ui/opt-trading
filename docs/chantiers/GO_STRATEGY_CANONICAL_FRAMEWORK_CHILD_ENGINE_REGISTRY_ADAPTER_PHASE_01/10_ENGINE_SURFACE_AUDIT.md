---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_ENGINE_REGISTRY_ADAPTER_PHASE_01
doc_type: audit
---

# 10_ENGINE_SURFACE_AUDIT

## Résumé

| Engine | strategy_id ? | Source | Importe modules/strategy/ ? |
|--------|--------------|--------|---------------------------|
| trading_realtime_v1 | OUI | hardcodé `xau_session_open_v1` | NON |
| trading_lab_v1 | OUI | profil YAML, fallback hardcodé | NON |
| decision_engine | NON (via symbol) | engine names coïncident avec registry | NON |
| signal_router | OUI | champ SignalIn/NormalizedSignal | NON |
| proposition_engine | OUI | pass-through NormalizedSignal | NON |
| notification_dispatcher | OUI | template parameter | NON |

## Détail par engine

### 1. trading_realtime_v1

- `runtime_loop_v1.py:13` : `STRATEGY_ID = "xau_session_open_v1"` — hardcodé
- `event_bridge_v1.py:11` : `STRATEGY_ID = "xau_session_open_v1"` — hardcodé
- Aucun import modules/strategy/

### 2. trading_lab_v1

- `trading_lab_v1.py:396` : lit strategy_id depuis profil YAML, fallback `"xau_session_open_v1"`
- Aucun import modules/strategy/

### 3. decision_engine

- `strategy_logic.py` : enum Engine = `COINM_SHORT`, `USDTM_LONG`, `GOLD_CFD_LONG`
- Ces noms coïncident avec des entrées registry, mais pas de validation
- Aucun import modules/strategy/

### 4. signal_router

- `schema.py:21` : `SignalIn.strategy_id: str = ""` (optionnel)
- `schema.py:33` : `NormalizedSignal.strategy_id: str` (requis)
- `router.py:44` : fallback sur `engine` si strategy_id absent
- Aucun import modules/strategy/

### 5. proposition_engine

- `schema.py:13` : `NormalizedSignal.strategy_id: str`
- `builder_prompt.py:12` : inclus dans prompt OpenClaw
- Aucun import modules/strategy/

### 6. notification_dispatcher

- `events.py:38` : template `"Strategy: <code>{strategy_id}</code>"`
- Aucun import modules/strategy/

## Conclusion

Tous les engines sont découplés de `modules/strategy/`. L'adapter devra :
- Ne casser aucun import existant.
- Être optionnel — importable sans risque.
- Servir de point de lecture registry unique pour les engines qui veulent valider leurs strategy_id.
