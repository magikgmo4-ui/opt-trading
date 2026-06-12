# GO_SPACEX_SUPER_DESK_PARENT_01 — Initial Project Doc

## 1_MASTER_TARGET

Construire dans `opt-trading` un système prioritaire et permanent pour SpaceX/SPCX : desk dédié, trading lab, data center, alertes, capture visuelle, reporting, et modèle d'accumulation long terme.

Le système doit servir deux buts simultanés :

1. **Court terme** : capter les conditions de momentum, IPO gap, opening range, VWAP reclaim, FVG reclaim, continuation, squeeze, news catalyst, volume spike.
2. **Long terme** : accumuler SpaceX au bon prix avec données fondamentales, SEC, Starlink, Starship, contrats, institutionnels, valorisation et régime de marché.

Invariant : **monitor-only**. Aucun ordre réel, aucun levier automatique, aucune exécution broker.

## 3_INITIAL_NEED

L'utilisateur veut utiliser toutes les sources disponibles : TradingView, indicateurs, alertes, Coinglass, funding/liquidations, Bot Vision headless, screenshots, analyse visuelle, actualités, métriques multi-timeframe, ouverture/fermeture, FVG, et toute donnée utile pour posséder SpaceX au bon prix et exploiter le leverage momentum.

## 4_MASTER_PROJECT_PLAN

### Axes

1. **Source Inventory** : cartographier les surfaces existantes du repo.
2. **SPACEX_DATA_CENTER** : stocker raw + normalized + scored.
3. **TradingView Engine** : webhook JSON, alertes, Pine, FVG/BOS/CHOCH/VWAP/ORB.
4. **Bot Vision Engine** : profils screenshots, OCR, analyse, vision context.
5. **Coinglass Context Engine** : funding/liquidation/OI direct si supporté, sinon proxy risk context.
6. **News/SEC Engine** : SEC EDGAR, Nasdaq, SpaceX, Starlink, NASA, DoD, Reuters-like/Yahoo/CNBC/MarketWatch/Benzinga/SeekingAlpha si disponible.
7. **Institutional Engine** : ETFs, analystes, lockup, secondary, 13F.
8. **Trading Lab** : setups court terme et risk notes.
9. **Accumulation Engine** : zones d'achat, stress de valorisation, qualité fondamentale.
10. **SPACEX_DESK** : UI locale + handoff Desk Pro.
11. **Alerts** : Telegram/Desk/Sheets/report JSONL.
12. **Reports** : daily + latest snapshot.

## 5_GO_PLAN

Le présent bundle V2 livre une implémentation sérieuse mais prudente :

- Aucun secret requis pour le dry-run.
- Collecteurs publics avec fallback offline.
- Écriture dans `data/ipo/spacex` et `data/data_center/views/spacex_*`.
- Scoring explicite.
- UI statique locale.
- Scripts opérateur.
- Tests smoke.

Les sources payantes/privées restent derrière variables d'environnement et contrats futurs.

## 6_FINAL_TARGET

À terme :

- `/spacex` dans Desk Pro ou page statique servie.
- Données SPCX continues.
- Alertes Telegram.
- Google Sheets export.
- Rapports journaliers.
- Dashboard court terme + long terme.
- Setup engine exploitable pour décision manuelle.

## 11_KEY_DECISIONS

- SpaceX/SPCX devient actif priorité critique.
- Monitor-only permanent.
- Raw data conservée.
- TradingView et Bot Vision sont sources techniques prioritaires.
- SEC et news sont sources fondamentales prioritaires.
- Toute donnée doit être scorée selon utilité, fraîcheur et fiabilité.

## 12_INVARIANTS

- Ne pas automatiser d'ordre réel.
- Ne pas bypasser Data Center.
- Ne pas supprimer les surfaces existantes.
- Ne pas dépendre d'une API payante pour démarrer.
- Ne pas traiter les données Coinglass crypto comme données directes SPCX : les marquer comme contexte/risk proxy.

## 17_RESUME_POINT

Lancer :

```bash
bash scripts/ipo/spacex_collect_once.sh
bash scripts/ipo/spacex_report_daily.sh
python3 -m modules.ipo_tracking.cli collect-once --offline-ok
```
