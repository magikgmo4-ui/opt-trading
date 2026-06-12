---
doc_id: GO_TRADINGVIEW_MAX_ACCESS_STACK_01
doc_type: documentary_audit
status: proven
created_at: 2026-06-12
---

# GO_TRADINGVIEW_MAX_ACCESS_STACK_01 — Documentary PR

## 1. Architecture — Plan Initial Complet

### 5 Couches d'accès LLM → TradingView

| Couche | Fonction | Droits LLM | Statut |
|--------|----------|------------|--------|
| **A. Webhooks officiels** | TV pousse alertes → API | Réception signaux | ✅ PROUVÉ |
| **B. Pine Script** | Calcul setups, alertconditions | Générer logique | ✅ PROUVÉ |
| **C. CDP Orchestrator** | Contrôle TV Desktop via jobs | Lire/écrire alertes, Pine, symboles | ⏳ PARTIEL |
| **D. Bot Vision / DOM** | Captures + extraction sans OCR | Contexte visuel | ✅ PROUVÉ |
| **E. Data Center** | Stockage raw/scored | Mémoire exploitable | ✅ PROUVÉ |
| **F. Charting Library** | Terminal propriétaire | Contrôle complet | ❌ FUTUR |
| **G. Broker API** | Ordres/positions | BLOQUÉ paper-only | ❌ HORS SCOPE |

---

## 2. Ce qui est PROUVÉ (runtime admin-trading)

### Couche A — Webhooks officiels
| Item | Résultat |
|------|----------|
| Cloudflare tunnel | `spacex-tv.magikgmo4.uk` → `admin-trading:8000` ✅ |
| `/tv/spacex` endpoint | POST → `200 OK` → `spacex_snapshots.jsonl` ✅ |
| Smoke test externe | `{"ok":true,"schema":"spacex_tv_event_v1"}` ✅ |
| Migration tunnel | db-layer → admin-trading (même UUID `61045ee3`) ✅ |

### Couche B — Pine Script
| Item | Fichier |
|------|---------|
| Pine master | `pine_factory/spacex_ipo_master_v1.pine` — 13 alertcondition() |
| Alert pack | `configs/tradingview/spacex_tv_targets.yaml` — 10 alertes requises |
| Reconcile script | `scripts/ipo/spacex_tv_reconcile.py` — drift detect + job gen |

### Couche C — CDP Orchestrator
| Item | Statut |
|------|--------|
| PR #1132 — TV orchestrator | `TV_SNAPSHOT` + `TV_WRITE_GATED` opérationnel |
| PR #1133 — `/tv/spacex` endpoint | Observer-only, key validation, persistence |
| PR #1147 — alert automation | `tv_agent.ps1` fix, alert #4917725195 créée et fired |
| `AlertAutomationEngine` | 7 types d'alertes, evaluate → dispatch → analytics |
| SSH admin-trading → cursor-ai | ✅ 1ms LAN ping |
| CDP cursor-ai | ⏳ Nécessite desktop session + VBS |

### Couche D — Bot Vision / DOM extraction
| Item | Résultat |
|------|----------|
| SPCX MAX profile | 15 pages, 7 symboles, 5 sources, cron hourly |
| DOM extraction | Yahoo: price/change/volume, TV: O/H/L/C/Vol ✅ |
| visual_price | $169.09, delta 0.15% vs API ✅ |
| `capture_headless.js` | Patché avec `extractDomData()` |

### Couche E — Enriched Pipeline
| Métrique | Valeur |
|----------|--------|
| SPCX price | $160.95 |
| source_count | 2 (Yahoo + TV DOM) |
| price_trust | 0.42 |
| info_trust | 1.0 (max) |
| news_count | 40 (Google News RSS) |
| news_score | 1 |
| catalyst_score | 1.0 |
| trade_ready | 0.49 |
| pipeline_state | actif, scores non bloqués |
| SMC structures | BOS, CHOCH, FVG détectés |

---

## 3. GAPS — Ce qui manque

| # | Gap | Priorité | Bloqueur |
|---|-----|----------|----------|
| 1 | **TV webhook real fires** — 0 events depuis 18:32 UTC | P0 | Alerte #4917725195 expirée/supprimée |
| 2 | **Nasdaq live price** — `NO_PRICE_AVAILABLE_YET` | P0 | API Nasdaq ne renvoie pas de prix SPCX |
| 3 | **CDP cursor-ai** — port 9222 inactif | P0 | SSH ne peut pas lancer GUI Windows |
| 4 | **Alert dispatch** — jobs créés mais non appliqués | P1 | Dépend du CDP |
| 5 | **Coinglass → risk_proxy** — 1058 screenshots non intégrés | P2 | Non prioritaire |
| 6 | **Sector/Halo scoring** — comparables capturés non scorés | P2 | Non prioritaire |
| 7 | **URL divergence** — `hooks.magikgmo4.uk` vs `spacex-tv.magikgmo4.uk` | P3 | Deux hostnames, à unifier |

---

## 4. BLOCANTS ACTUELS

### Blocant #1 — CDP cursor-ai
```
Problème: SSH Windows ne peut pas lancer de GUI.
         TradingView doit être lancé avec --remote-debugging-port=9222.
Solution: L'utilisateur double-clique TradingView_CDP.vbs depuis le desktop.
         Tâche planifiée TradingView_CDP_User créée pour les prochains logins.
État: TV tourne (11 instances) mais SANS le flag CDP.
```

### Blocant #2 — Alerte #4917725195
```
Problème: L'alerte a tiré sur db-layer (18:30-18:32 UTC) puis s'est arrêtée.
         Après migration tunnel, 0 fires sur admin-trading.
Cause probable: Alerte expirée, clé invalide, ou condition non re-déclenchée.
Solution: Recréer via CDP avec heartbeat on_bar_close + clé correcte.
```

### Blocant #3 — Nasdaq API
```
Problème: L'API Nasdaq retourne price_status=NO_PRICE_AVAILABLE_YET.
Impact: source_count bloqué à 2 au lieu de 3, price_trust bloqué à 0.42.
Solution: Attendre que Nasdaq publie le prix SPCX. Pas d'action code.
```

---

## 5. PROCHAIN GO — GO_SPACEX_TV_HEARTBEAT_AND_ALERT_REPAIR_01

### Actions immédiates

1. **Lancer CDP** — Double-clic `TradingView_CDP.vbs` (desktop cursor-ai)
2. **Vérifier CDP** — `netstat -ano | findstr :9222` doit montrer LISTENING
3. **Auditer alerte** — `alert.list` pour vérifier #4917725195
4. **Créer heartbeat** — `SPCX_TV_HEARTBEAT_1M` via CDP
5. **Watch admin-trading** — `tail -f data/ipo/spacex/raw/spacex_snapshots.jsonl`
6. **Si heartbeat OK** → recréer alertes setup
7. **Si heartbeat FAIL** → corriger URL/key/webhook

---

## 6. FICHIERS DU STACK

```
configs/tradingview/spacex_tv_targets.yaml       — source de vérité TV
modules/tradingview_orchestrator/pine_factory/    — Pine master
scripts/ipo/spacex_tv_reconcile.py                — drift detection
modules/spcx_v2/alert_engine/engine.py            — automation engine
modules/ipo_tracking/enrichment/candle_enricher.py — pipeline_state
modules/ipo_tracking/enrichment/source_consensus.py — price_trust/visual_price
modules/ipo_tracking/collectors/rss_news.py        — Google News fallback
modules/bot_vision/headless_capture/capture_headless.js — DOM extraction
webhook_server.py                                  — /tv/spacex endpoint
docs/chantiers/GO_SPACEX_TV_AUTOMATION_MAX_01/     — automation plan
docs/chantiers/GO_SPACEX_TV_ALERT_AUTOMATION_ENGINE_01/ — alert engine
reports/tradingview/                               — drift reports
```
