---
doc_id: GO_STRATEGY_SIGNAL_MONITORING_PIPELINE_01_INITIAL_PROJECT_DOC
repo: opt-trading
go_id: GO_STRATEGY_SIGNAL_MONITORING_PIPELINE_01
doc_type: initial_project_doc
status: initial_validated
lifecycle_stage: planning
surface: strategy_signal_monitoring
source_kind: user_validated_plan
created_at: 2026-05-17
branch: go/GO_STRATEGY_SIGNAL_MONITORING_PIPELINE_01
parent_go: GO_STRATEGY_SIGNAL_MONITORING_PIPELINE_01
---

# GO_STRATEGY_SIGNAL_MONITORING_PIPELINE_01 - Initial Project Doc

## 1_MASTER_TARGET

Créer un module indépendant de monitoring de stratégie qui combine :

- TradingView alerts ;
- choix et routage d'alertes ;
- screener headless ;
- sources métriques externes, notamment TradingView, Coinglass, exchange APIs et autres sources utiles ;
- charts, screenshots et lecture vision ;
- indicateurs techniques et métriques de contexte ;
- scoring de signal ;
- enregistrement durable des sorties ;
- monitoring de performance stratégie.

Le module doit s'intégrer à l'existant `opt-trading` sans casser les surfaces actuelles.

---

## 2_INITIAL_PROJECT_DOC

Ce document est la fiche de référence initiale du chantier parent.

Règle : il contient le plan initial intégral validé au démarrage du chantier. Il reste figé sauf changement explicite ou implicite du projet.

---

## 3_INITIAL_NEED

Demande initiale :

> TradingView + choix alerte + screener headless TradingView / Coinglass / autre source utile / charts / indicateurs / données métriques / screener + enregistrer sortie + monitoring stratégie.

Besoin opérationnel :

- capter les signaux entrants depuis TradingView ;
- recroiser ces signaux avec un screener indépendant ;
- enrichir le signal avec données marché et métriques dérivées ;
- intégrer les charts et screenshots comme preuve ou contexte ;
- produire une sortie normalisée exploitable par Telegram, Google Sheets, perf engine, desk pro et bot vision ;
- mesurer la performance de la stratégie avant tout passage live.

---

## 4_MASTER_PROJECT_PLAN

### Direction générale

Construire une chaîne fermée :

```text
TradingView Alerts
  -> Webhook / Signal Intake
  -> Headless Screener
  -> Metric Enrichment
  -> Chart / Vision Review
  -> Strategy Scoring
  -> Output Recorder
  -> Telegram / Desk Output
  -> Monitoring / Perf Engine
```

### Axes majeurs

1. Intake / ingestion de signaux.
2. Screening headless multi-source.
3. Enrichissement métrique.
4. Lecture chart / screenshot.
5. Scoring stratégie.
6. Journalisation canonique.
7. Notification opératoire.
8. Monitoring statistique.
9. Backtest / replay / paper-trading avant live.

---

## 5_GO_PLAN

### Parent GO

`GO_STRATEGY_SIGNAL_MONITORING_PIPELINE_01`

### Sous-GO proposés

| GO | Rôle |
| --- | --- |
| `GO_TRADINGVIEW_ALERT_ROUTER_01` | Recevoir, normaliser et router les alertes TradingView. |
| `GO_HEADLESS_SCREENER_ENGINE_01` | Scanner symboles, timeframes et conditions sans UI manuelle. |
| `GO_MARKET_METRICS_ENRICHMENT_01` | Ajouter OI, funding, liquidations, volume, volatilité, trend. |
| `GO_CHART_VISION_REVIEW_01` | Lire screenshots/charts via vision et produire des confirmations. |
| `GO_STRATEGY_SIGNAL_SCORING_01` | Calculer score, confiance, invalidation, TP et risque. |
| `GO_SIGNAL_OUTPUT_RECORDER_01` | Enregistrer JSONL, CSV, Google Sheets et artefacts. |
| `GO_TELEGRAM_SIGNAL_NOTIFIER_01` | Envoyer sortie Telegram structurée. |
| `GO_STRATEGY_MONITORING_DASHBOARD_01` | Suivre winrate, expectancy, drawdown, erreurs et drift. |

---

## 6_FINAL_TARGET

Livrable cible de phase 1 :

```text
Une alerte TradingView entrante
  -> normalisée en signal_event
  -> enrichie par métriques externes
  -> confirmée ou rejetée par screener headless
  -> scorée
  -> enregistrée
  -> notifiée
  -> suivie dans monitoring/perf engine
```

Le module ne déclenche pas d'exécution live dans cette phase.

---

## 7_CANONICAL_STATE

État validé de départ :

- TradingView sert de déclencheur et de surface chart, pas de source unique de vérité.
- Le screener headless sert de vérification indépendante.
- Coinglass et autres sources métriques servent au contexte marché.
- Les screenshots/charts servent de preuve visuelle et d'entrée pour bot vision.
- Les sorties doivent être enregistrées avant notification.
- Google Sheets, JSONL et perf engine sont les surfaces de suivi.
- Telegram est une sortie opératoire, pas le registre canonique.
- Aucun live trading automatique n'est autorisé par ce chantier initial.

---

## 8_VALIDATED_PLAN

Étapes validées :

1. Créer le chantier parent sur branche dédiée.
2. Documenter le plan intégral validé.
3. Définir un schéma canonique `signal_event`.
4. Préparer le routeur webhook TradingView.
5. Préparer le screener headless minimal.
6. Préparer les adaptateurs métriques externes.
7. Préparer l'enregistrement des sorties.
8. Préparer le monitoring de stratégie.
9. Préparer les sous-GO d'implémentation.

---

## 9_SELECTED_SOLUTION

Solution retenue : architecture modulaire event-driven.

Chaque signal doit passer par un objet canonique :

```json
{
  "timestamp": "2026-05-17T21:00:00-04:00",
  "symbol": "BTCUSDT",
  "timeframe": "1h",
  "source": "tradingview_alert",
  "strategy": "SMC_ICT_CHOCH_BOS",
  "direction": "short",
  "entry_zone": [104500, 105200],
  "invalidation": 106100,
  "tp1": 102800,
  "tp2": 100500,
  "confidence_score": 0.72,
  "market_context": {
    "trend": "bearish_retest",
    "funding": "positive",
    "open_interest": "rising",
    "liquidation_cluster": "below_price"
  },
  "screener_confirmations": {
    "tradingview": true,
    "coinglass": true,
    "vision_chart": true
  },
  "status": "candidate"
}
```

---

## 10_SELECTED_SETUP

### Entrées

- TradingView webhook alerts.
- Headless chart/screener adapter.
- Coinglass metrics adapter.
- Exchange/OHLCV adapter.
- Screenshot/chart capture adapter.
- Google Sheets manual/context input, si utile.

### Traitement

- Normalisation signal.
- Déduplication.
- Validation source.
- Enrichissement métrique.
- Confirmation multi-timeframe.
- Scoring stratégie.
- Qualification : candidate / confirmed / rejected / expired.

### Sorties

- `signals.jsonl`.
- `signals.csv`.
- Google Sheets.
- Telegram.
- Rapport monitoring.
- Artefacts screenshots/charts.

---

## 11_KEY_DECISIONS

- Le chantier parent est structurant et doit vivre sur branche dédiée.
- Le périmètre initial est doc-only.
- Le live trading est hors périmètre initial.
- La sortie enregistrée est obligatoire avant toute notification.
- TradingView n'est pas une vérité unique.
- Le screener headless doit recroiser les signaux.
- Le monitoring statistique est obligatoire pour valider la stratégie.

---

## 12_INVARIANTS

Ne pas rouvrir sans raison explicite :

- pas d'exécution live dans ce GO parent initial ;
- pas de dépendance exclusive à TradingView ;
- pas de notification sans journalisation ;
- pas de mélange signal / exécution / backtest dans un même module ;
- pas de modification destructive des modules existants ;
- pas de score stratégie sans preuve source et contexte métrique ;
- pas d'élargissement aux index globaux sans instruction ou changement global prouvé.

---

## 13_ESTABLISHED

- Le repo cible est `magikgmo4-ui/opt-trading`.
- La branche canonique est `sot/mainline`.
- Le chantier parent est `GO_STRATEGY_SIGNAL_MONITORING_PIPELINE_01`.
- La branche dédiée est `go/GO_STRATEGY_SIGNAL_MONITORING_PIPELINE_01`.
- La matrice documentaire canonique lue est `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`.

---

## 14_HYPOTHESIS

À valider lors de l'état des lieux repo :

- présence déjà partielle de modules Telegram ;
- présence déjà partielle de perf engine ;
- présence déjà partielle de Google Sheets adapter ;
- présence déjà partielle de bot vision OpenAI ;
- présence déjà partielle de screener ou watchlist runtime ;
- existence d'un schéma market/runtime réutilisable.

Aucune de ces hypothèses ne doit être traitée comme établie avant vérification réelle dans le repo.

---

## 15_REMAINING_GAP

Manques à combler :

- inventaire réel des modules existants ;
- choix du format définitif `signal_event`; 
- mapping des sources disponibles ;
- mode de capture screenshots/charts ;
- stratégie de persistance ;
- définition du score minimal ;
- seuils de validation/rejet ;
- dashboard de monitoring ;
- protocole backtest / replay / paper-trading.

---

## 16_TODO

1. Recroiser le repo pour identifier les modules existants liés à TradingView, Telegram, screener, vision, perf engine, Google Sheets et watchlist.
2. Créer `signal_event.schema.json` dans le sous-GO adapté.
3. Créer le routeur webhook TradingView.
4. Créer un screener headless minimal sans exécution live.
5. Ajouter adaptateurs métriques externes.
6. Ajouter enregistreur JSONL/CSV.
7. Ajouter stub Telegram.
8. Ajouter monitoring report.
9. Ouvrir les sous-GO un par un selon les dépendances réelles.

---

## 17_RESUME_POINT

Reprise opérationnelle :

```text
Repartir de GO_STRATEGY_SIGNAL_MONITORING_PIPELINE_01.
Lire ce 00_INITIAL_PROJECT_DOC.
Vérifier l'état réel du repo depuis sot/mainline.
Inventorier les modules existants.
Créer le premier sous-GO : GO_TRADINGVIEW_ALERT_ROUTER_01 ou GO_SIGNAL_OUTPUT_RECORDER_01 selon ce que le repo contient déjà.
```

---

## 18_TO_DOCUMENT

Blocs à documenter ensuite :

- `SIGNAL_EVENT_SCHEMA_01`
- `SOURCE_ADAPTER_MATRIX_01`
- `HEADLESS_SCREENER_RUNTIME_CONTRACT_01`
- `METRIC_ENRICHMENT_CONTRACT_01`
- `SIGNAL_SCORING_RULES_01`
- `OUTPUT_RECORDER_CONTRACT_01`
- `MONITORING_STRATEGY_REPORT_01`

---

## 19_TO_REMEMBER

### MEM_CANDIDATE

- `GO_STRATEGY_SIGNAL_MONITORING_PIPELINE_01` : chantier parent pour transformer TradingView + screeners + métriques + charts/vision en signaux scorés, enregistrés et monitorés.

### SAVE_MEMORY

- À valider après inventaire réel du repo et premier sous-GO d'implémentation.
