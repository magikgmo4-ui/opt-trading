# TRADING DUAL STACK — CORE SPEC V1

Date (America/Montreal) : 2026-04-03

## 1. RÔLE

Ce document matérialise la **spec canonique V1 du noyau commun** pour le chantier trading dual stack.

Il traduit le cadrage de `00_TRADING_DUAL_STACK_LAB_REALTIME_V1.md` en objets plus opératoires, sans encore lancer l’implémentation.

Ce document couvre :
- le découpage `frame / strategy / execution / analytics` ;
- la structure de config V1 ;
- le schéma d’événements V1 ;
- le schéma trade/log V1 ;
- la première famille de variantes Gold/session.

---

## 2. PORTÉE V1

### Instrument
- `XAUUSD`

### Timezone
- `America/Montreal`

### Fenêtres initiales
- `18:00`
- `00:00`

### Mode de départ
- **LAB** : actif au niveau spec
- **REAL-TIME** : limité à `observation` puis `validation`
- **full auto** : hors périmètre V1

---

## 3. NOYAU COMMUN — DÉCOUPAGE CANONIQUE

## 3.1 `frame`

### Rôle
Le `frame` contient le **cadre trader invariant**.

### Contenu minimum
- timezone
- sessions
- kill zones
- limites journalières
- discipline
- règles risk globales
- cooldowns
- interdictions d’exécution

### Décision
Aucune stratégie ne peut bypasser le `frame`.

---

## 3.2 `strategy`

### Rôle
La `strategy` décrit les conditions de détection et de qualification des setups.

### Contenu minimum
- identifiant stratégie
- identifiants de variantes
- conditions mécaniques
- filtres activables
- règles de direction
- règles d’invalidation

### Décision
Une stratégie ne gère pas l’état du risque global ni les limites journalières ;
ces éléments restent dans `frame`.

---

## 3.3 `execution`

### Rôle
`execution` décrit comment un signal est traité une fois détecté.

### Modes V1 autorisés
- `observation`
- `validation`
- `autonomous_candidate` (déclaratif seulement ; pas à exécuter en V1)

### Contenu minimum
- mode
- règles de confirmation
- règles d’ouverture
- règles de sizing
- règles de gestion de position
- règles de sortie

### Décision
Le moteur d’exécution ne décide pas si une stratégie est valide “de fond” ;
il applique un signal déjà validé par `frame + strategy`.

---

## 3.4 `analytics`

### Rôle
`analytics` standardise les journaux, métriques et comparaisons.

### Contenu minimum
- event journal
- trade journal
- rapports par variante
- comparaisons lab/live
- métriques de dérive

### Décision
Le **journal d’événements** est la source primaire.
Le **journal de trades** est dérivé.

---

## 4. STRUCTURE DE CONFIG V1

## 4.1 Objet racine recommandé

```yaml
version: "v1"
profile_id: "xauusd_dual_stack_v1"

frame:
  timezone: "America/Montreal"
  symbol: "XAUUSD"
  sessions: []
  discipline: {}
  risk: {}
  constraints: {}

strategy:
  strategy_id: "xau_session_open_v1"
  family: "session_open"
  variants: []
  filters: {}

execution:
  mode: "observation"
  entry_policy: {}
  sizing_policy: {}
  management_policy: {}
  exit_policy: {}

analytics:
  event_journal: {}
  trade_journal: {}
  reporting: {}
  comparison: {}
```

---

## 4.2 `frame.sessions`

```yaml
sessions:
  - session_id: "gold_open_18h"
    enabled: true
    start_local: "18:00"
    end_local: "18:30"
    signal_window_start: "18:00"
    signal_window_end: "18:10"
    max_trades_per_session: 1

  - session_id: "midnight_00h"
    enabled: true
    start_local: "00:00"
    end_local: "00:30"
    signal_window_start: "00:00"
    signal_window_end: "00:10"
    max_trades_per_session: 1
```

### Règles
- tous les horaires sont interprétés en `America/Montreal` ;
- `signal_window_*` borne la période de détection ;
- `start_local/end_local` borne la session opératoire totale ;
- la détection d’un setup hors fenêtre retourne un `decision_state = blocked_by_frame`.

---

## 4.3 `frame.discipline`

```yaml
discipline:
  max_trades_per_day: 2
  stop_day_after_losses: 2
  cooldown_after_trade_minutes: 15
  allow_reentry_same_setup: false
  allow_outside_sessions: false
  allow_overlapping_positions: false
```

### Règles
- `max_trades_per_day` s’applique au couple `(profile_id, local_date)` ;
- `cooldown_after_trade_minutes` s’applique après fermeture ou annulation selon politique runtime ;
- `allow_reentry_same_setup: false` interdit une seconde ouverture sur le même `setup_instance_id`.

---

## 4.4 `frame.risk`

```yaml
risk:
  risk_per_trade_pct: 1.0
  rr_min: 2.0
  move_be_at_r: 1.0
  partial_tp_plan:
    enabled: false
  max_stop_distance_points: null
  min_valid_stop_distance_points: null
```

### Règles
- le risk engine consomme ces paramètres dans LAB et REAL-TIME ;
- `rr_min` est un filtre d’acceptation ;
- `move_be_at_r` est une règle de gestion, non une règle de détection.

---

## 4.5 `frame.constraints`

```yaml
constraints:
  max_spread_points: null
  news_lock_enabled: false
  htf_filter_required: false
  deny_if_data_incomplete: true
```

### Règles
- `deny_if_data_incomplete: true` bloque tout signal si les données nécessaires à la variante sont incomplètes ;
- `max_spread_points` est optionnel en V1 mais le champ existe dès maintenant.

---

## 5. STRATEGY SPEC V1

## 5.1 Identité stratégie

```yaml
strategy:
  strategy_id: "xau_session_open_v1"
  family: "session_open"
  model: "mechanical"
```

### But
Classifier mécaniquement les comportements d’ouverture/session autour de :
- la première M5 ;
- les 5 premières M1 ;
- sweep ou non ;
- FVG ou non ;
- direction potentielle.

---

## 5.2 Première famille de variantes retenue

### Nomenclature canonique
- `xau_open_sweep_fvg`
- `xau_open_no_sweep_fvg`
- `xau_open_sweep_no_fvg`
- `xau_open_no_sweep_no_fvg`

### Sens
Chaque variante décrit une **classe mécanique**.
Elle ne signifie pas automatiquement “trade executable”.

---

## 5.3 Définition minimale par variante

```yaml
variants:
  - variant_id: "xau_open_sweep_fvg"
    enabled: true
    require_sweep: true
    require_fvg: true
    require_reclaim: false
    direction_mode: "contextual"

  - variant_id: "xau_open_no_sweep_fvg"
    enabled: true
    require_sweep: false
    require_fvg: true
    require_reclaim: false
    direction_mode: "contextual"

  - variant_id: "xau_open_sweep_no_fvg"
    enabled: true
    require_sweep: true
    require_fvg: false
    require_reclaim: false
    direction_mode: "contextual"

  - variant_id: "xau_open_no_sweep_no_fvg"
    enabled: true
    require_sweep: false
    require_fvg: false
    require_reclaim: false
    direction_mode: "contextual"
```

### Décision
En V1, `direction_mode` peut rester `contextual` au niveau spec, tant que la logique de classification directionnelle est explicitée dans le runner futur.

---

## 5.4 Filtres activables

```yaml
filters:
  require_session_window: true
  require_complete_open_sequence: true
  htf_bias_enabled: false
  spread_filter_enabled: false
  news_filter_enabled: false
```

### Décision
Les filtres non activés doivent exister dans la spec pour éviter un futur refactor structurel.

---

## 6. EXECUTION SPEC V1

## 6.1 Modes

```yaml
execution:
  mode: "observation"
```

### Valeurs autorisées V1
- `observation`
- `validation`
- `autonomous_candidate`

### Règle
- `autonomous_candidate` existe pour permettre les comparaisons et l’étiquetage, mais ne doit pas déclencher d’ordres en V1.

---

## 6.2 `entry_policy`

```yaml
entry_policy:
  order_type: "virtual"
  require_manual_validation: false
  min_rr_required: true
  deny_if_frame_blocked: true
```

### Interprétation par mode
- en `observation` : `order_type` reste virtuel / simulé ;
- en `validation` : `require_manual_validation: true` ;
- en `autonomous_candidate` : on ne fait que mesurer la faisabilité, sans exécution réelle.

---

## 6.3 `sizing_policy`

```yaml
sizing_policy:
  sizing_mode: "risk_percent"
  source_risk_pct: "frame.risk.risk_per_trade_pct"
  quantity_rounding_rule: "instrument_specific"
```

### Décision
Le sizing n’est pas libre par variante en V1 ;
il dépend d’un risk engine commun.

---

## 6.4 `management_policy`

```yaml
management_policy:
  move_be_enabled: true
  move_be_at_r: 1.0
  partial_tp_enabled: false
  trailing_enabled: false
```

---

## 6.5 `exit_policy`

```yaml
exit_policy:
  hard_stop_required: true
  hard_tp_required: false
  session_forced_exit_enabled: false
  record_mfe_mae: true
```

### Décision
Même sans TP dur, la politique doit produire `rr_planned`, `mfe`, `mae`, `time_in_trade`.

---

## 7. EVENT SCHEMA V1

## 7.1 Rôle

L’event journal capture **tous les événements de décision**, pas seulement les trades.

---

## 7.2 Champs minimum obligatoires

```yaml
event:
  event_id: string
  event_ts: datetime
  profile_id: string
  mode: string
  symbol: string
  timeframe_context: object
  session_name: string
  local_date: string
  timezone: string
  strategy_id: string
  variant_id: string | null
  setup_instance_id: string | null
  event_type: string
  decision_state: string
  direction: string | null
  signal_ts: datetime | null
  filters_state: object
  frame_state: object
  raw_features: object
  notes: string | null
```

---

## 7.3 `event_type` — valeurs minimales V1

- `session_opened`
- `setup_detected`
- `setup_classified`
- `setup_blocked`
- `trade_candidate_created`
- `trade_opened`
- `trade_closed`

---

## 7.4 `decision_state` — valeurs minimales V1

- `observed`
- `accepted`
- `blocked_by_frame`
- `blocked_by_filters`
- `blocked_by_risk`
- `awaiting_validation`
- `rejected_manual`
- `closed`

---

## 7.5 Exemple canonique

```json
{
  "event_id": "evt_20260403_180001_xau_session_open_v1_001",
  "event_ts": "2026-04-03T18:00:01-04:00",
  "profile_id": "xauusd_dual_stack_v1",
  "mode": "observation",
  "symbol": "XAUUSD",
  "session_name": "gold_open_18h",
  "local_date": "2026-04-03",
  "timezone": "America/Montreal",
  "strategy_id": "xau_session_open_v1",
  "variant_id": "xau_open_sweep_fvg",
  "setup_instance_id": "setup_20260403_1800_gold_open_001",
  "event_type": "setup_classified",
  "decision_state": "observed",
  "direction": "bullish",
  "signal_ts": "2026-04-03T18:05:00-04:00",
  "filters_state": {
    "require_session_window": true,
    "require_complete_open_sequence": true,
    "htf_bias_enabled": false
  },
  "frame_state": {
    "session_allowed": true,
    "max_trades_per_day_ok": true,
    "cooldown_ok": true
  },
  "raw_features": {
    "sweep_detected": true,
    "fvg_detected": true,
    "m5_open_candle_captured": true,
    "m1_first_5_complete": true
  },
  "notes": null
}
```

---

## 8. TRADE / LOG SCHEMA V1

## 8.1 Rôle

Le trade journal décrit uniquement les positions simulées ou exécutées.

---

## 8.2 Champs minimum obligatoires

```yaml
trade:
  trade_id: string
  event_id_origin: string
  profile_id: string
  mode: string
  symbol: string
  strategy_id: string
  variant_id: string
  setup_instance_id: string
  session_name: string
  local_date: string
  timezone: string
  direction: string
  entry_ts: datetime
  exit_ts: datetime | null
  entry: number
  sl: number
  tp_plan: object | null
  risk_pct: number
  rr_planned: number
  result: string | null
  r_realized: number | null
  mfe: number | null
  mae: number | null
  time_in_trade_seconds: number | null
  execution_state: string
  exit_reason: string | null
  slippage_points: number | null
```

---

## 8.3 `result` — valeurs minimales V1

- `win`
- `loss`
- `scratch`
- `open`
- `cancelled`

---

## 8.4 `execution_state` — valeurs minimales V1

- `virtual_open`
- `virtual_closed`
- `pending_validation`
- `rejected_manual`
- `candidate_only`

---

## 8.5 Exemple canonique

```json
{
  "trade_id": "trd_20260403_180500_xau_001",
  "event_id_origin": "evt_20260403_180001_xau_session_open_v1_001",
  "profile_id": "xauusd_dual_stack_v1",
  "mode": "observation",
  "symbol": "XAUUSD",
  "strategy_id": "xau_session_open_v1",
  "variant_id": "xau_open_sweep_fvg",
  "setup_instance_id": "setup_20260403_1800_gold_open_001",
  "session_name": "gold_open_18h",
  "local_date": "2026-04-03",
  "timezone": "America/Montreal",
  "direction": "bullish",
  "entry_ts": "2026-04-03T18:05:00-04:00",
  "exit_ts": "2026-04-03T18:18:00-04:00",
  "entry": 3225.4,
  "sl": 3221.9,
  "tp_plan": {
    "type": "rr_multiple",
    "rr_target": 2.0
  },
  "risk_pct": 1.0,
  "rr_planned": 2.0,
  "result": "win",
  "r_realized": 2.0,
  "mfe": 2.4,
  "mae": 0.6,
  "time_in_trade_seconds": 780,
  "execution_state": "virtual_closed",
  "exit_reason": "tp_virtual",
  "slippage_points": 0.0
}
```

---

## 9. ANALYTICS SPEC V1

## 9.1 Rapports minimums

### Par trade
- résultat
- R réalisé
- MAE
- MFE
- durée

### Par variante
- `sample_size`
- `winrate`
- `expectancy`
- `profit_factor`
- `max_drawdown`
- distribution par session
- distribution par jour

### Par mode
- `observation`
- `validation`
- `autonomous_candidate`

### Par comparaison lab/live
- `signal_count_delta`
- `execution_rate_delta`
- `winrate_delta`
- `expectancy_delta`
- `slippage_delta`

---

## 9.2 Friction réaliste LAB — champs réservés dès V1

```yaml
lab_realism:
  spread_points_simulated: number | null
  slippage_points_simulated: number | null
  entry_delay_seconds_simulated: number | null
  missed_trade_flag: boolean | null
```

### Décision
Même si la simulation de friction n’est pas encore implémentée, les champs sont réservés dès la spec V1.

---

## 10. DÉCISIONS DE DESIGN V1

### D1
Un seul **risk engine** partagé.

### D2
Un seul **format d’événement** partagé.

### D3
Le **trade journal** est dérivé du **journal d’événements**.

### D4
Le focus V1 reste **Gold / XAUUSD / sessions 18:00 et 00:00 / timezone America/Montreal**.

### D5
La famille de variantes V1 est d’abord **classificatoire** avant d’être pleinement exécutoire.

### D6
Le full auto est explicitement exclu du périmètre V1.

---

## 11. POINT DE REPRISE NATUREL APRÈS CETTE SPEC

### Suite recommandée
Matérialiser soit :
1. les **schémas machine-lisibles** (`json` / `yaml` / `md examples`) ;
2. soit le **squelette LAB V1** qui consomme cette spec ;
3. mais ne pas ouvrir encore l’exécution réelle.

### Trigger naturel suivant proposé
`GO_OT_TRADING_LAB_V1_SCHEMA_MATERIALIZATION_01`

---

## 12. RÉSUMÉ COURT

Cette spec V1 fige le noyau commun du chantier trading dual stack.

Elle établit :
- la séparation `frame / strategy / execution / analytics` ;
- la structure de config V1 ;
- le schéma d’événements V1 ;
- le schéma trade/log V1 ;
- la première famille de variantes Gold/session ;
- les garde-fous de périmètre V1.

## RISKS

- À qualifier.
