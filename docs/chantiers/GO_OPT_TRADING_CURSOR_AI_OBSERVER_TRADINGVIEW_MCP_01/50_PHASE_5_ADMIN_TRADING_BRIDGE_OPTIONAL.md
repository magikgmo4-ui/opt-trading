# 50_PHASE_5 — Pont optionnel admin-trading

## Objectif

Déterminer si les exports TradingView Observer peuvent alimenter desk/admin-trading sans modifier le runtime existant et sans automatiser l'ingestion avant validation.

## Statut

**PASS** — Pont évalué, bridge packet V1 défini, option de transfert décidée, aucun runtime modifié.

Date : 2026-05-04

---

## 1. Contexte

### Exports disponibles (observer → output/)

| Fichier | Contenu | Stable |
|---------|---------|--------|
| `latest_report.json` | Rapport combiné (status + state + quote + alerts + values) | Oui |
| `latest_status.json` | Santé CDP + chart state | Oui |
| `latest_quote.json` | OHLC courant du symbole | Oui |
| `latest_state.json` | Études / indicateurs sur le graphique | Oui |
| `latest_alert_inventory.json` | Inventaire complet des alertes (REST API) | Oui |
| `latest_values.json` | Valeurs visibles des indicateurs | Oui |

### Architecture existante admin-trading

```
admin-trading (Linux)
  ├── desk_snapshot_ingest    : lit inbox SFTP → latest.json + history.jsonl
  ├── desk_analyze            : lit latest.json → rapport consolidé + Binance + OpenAI
  ├── desk_pro / desk_pro_runner / desk_pro_orchestrator / desk_pro_dashboard
  ├── webhook (canonique)     : réception webhooks TradingView natifs
  ├── risk_engine             : évaluation risque
  ├── shared_files_sftp       : serveur SFTP /srv/sftp/shared_files/shared/
  ├── shared_sshfs_permanent  : montage client /shared
  └── winscp_transfer         : transferts Windows ↔ Linux
```

### Position de l'observer

```
cursor-ai (Windows)
  └── modules/tradingview_observer/      ← données live TradingView
  └── modules/tradingview_observer_openclaw/  ← skill OpenClaw sécurisé

admin-trading (Linux) — distant, séparé, aucun lien direct
```

---

## 2. Consommateurs identifiés (13_ESTABLISHED)

### Candidats réels pouvant consommer les données observer

| Module | Rôle | Compatibilité observer |
|--------|------|----------------------|
| `desk_snapshot_ingest` | Ingère screenshots PNG → `latest.json` | Faible — attend des PNG nommés, pas des JSON structurés |
| `desk_analyze` | Consolide `latest.json` + Binance + OpenAI vision | Moyen — pourrait lire un bridge packet au lieu de screenshots |
| `desk_pro_dashboard` | Dashboard admin-trading | Faible — pas de surface d'ingestion JSON documentée |
| `webhook` | Réception webhooks TV natifs | Nul — canal canonique séparé, ne doit pas être remplacé |
| `risk_engine` | Évaluation risque | Nul — aucune ingestion directe de données marché |

### Chemins existants

- **SFTP** : `/srv/sftp/shared_files/shared/` → surface partagée entre cursor-ai et admin-trading
- **WinSCP** : transferts Windows → Linux via le module `winscp_transfer`
- **SSHFS** : montage permanent `/shared` sur admin-trading (via `shared_sshfs_permanent`)

---

## 3. Bridge Packet V1 — Spécification

### Format

```json
{
  "schema": "tradingview_observer_bridge_v1",
  "source_machine": "cursor-ai",
  "source_module": "modules/tradingview_observer",
  "generated_at": "<iso_timestamp>",
  "symbol": "BITGET:BTCUSDT.P",
  "timeframe": "480",
  "quote": {
    "symbol": "BITGET:BTCUSDT.P",
    "close": 80632.8,
    "exchange": "Bitget",
    "type": "swap"
  },
  "state_summary": {
    "studies_count": 7,
    "studies_names": ["Bollinger Bands", "EMA 20/50/100/200", "..."],
    "visible_values_count": 3
  },
  "alerts_summary": {
    "total": 10,
    "active": 0,
    "expired": 10,
    "unknown": 0
  },
  "limits": {
    "webhook_payload_visible": false,
    "alert_delete_programmatic": "partial",
    "trading_mutation_allowed": false
  },
  "raw_files": {
    "latest_report": "not_embedded — see output/latest_report.json",
    "latest_quote": "not_embedded — see output/latest_quote.json",
    "latest_state": "not_embedded — see output/latest_state.json",
    "latest_values": "not_embedded — see output/latest_values.json",
    "latest_alerts": "not_embedded — see output/latest_alert_inventory.json"
  },
  "transfer_policy": "dry-run only — no automated transfer, no admin-trading ingestion, no SSH"
}
```

### Décision V1

> Le bridge V1 transporte une synthèse, pas les fichiers bruts complets.
> Les fichiers bruts restent locaux sauf GO explicite.
> Aucun prix OHLC complet n'est inclus (seulement `close`), protégeant contre l'ingestion accidentelle.

### Script associé

`modules/tradingview_observer/export_bridge_packet.ps1` — dry-run local, lit `latest_report.json`, produit `latest_bridge_packet.json`.

---

## 4. Options de transfert

### Option A — Manuel local seulement (RECOMMANDÉ Phase 5)

```
cursor-ai garde les JSON.
OpenClaw lit localement.
Aucun transfert vers admin-trading.
```

**Avantages** : Zéro risque, aucun service touché, aucune surface d'attaque.
**Inconvénients** : Pas de consommation admin-trading.
**Quand** : Aucun besoin immédiat admin-trading prouvé.

### Option B — Shared folder contrôlé (PRÉPARÉE)

```
cursor-ai exporte bridge_packet.json → WinSCP/manuel → /srv/sftp/shared_files/shared/...
admin-trading peut lire manuellement le packet.
```

**Avantages** : Transfert manuel contrôlé, réutilise l'infra SFTP existante.
**Inconvénients** : Nécessite une action manuelle Windows → Linux (WinSCP).
**Quand** : Prochain GO dédié `SHARED_PACKET_01`.

### Option C — Ingestion admin-trading future (SPÉCIFIÉE)

```
admin-trading dispose d'un script read-only qui lit un bridge packet validé.
Aucune activation automatique sans GO séparé.
```

**Avantages** : Intégration propre dans la stack admin-trading.
**Inconvénients** : Nécessite développement côté admin-trading (nouveau module), tests de sécurité.
**Quand** : GO dédié `PACKET_INGEST_REVIEW_01` côté admin-trading.

### Verdict

**Option A retenue pour Phase 5** — aucun besoin immédiat admin-trading prouvé.

L'Option B est préparée (bridge packet V1 existe, script d'export fonctionnel, surface SFTP documentée) mais non activée.

L'Option C est spécifiée comme GO futur possible.

---

## 5. Mode manuel contrôlé (implémenté)

1. L'utilisateur exécute `export_bridge_packet.ps1` **manuellement**.
2. Le script lit `latest_report.json` (déjà produit par l'observer).
3. Il génère `latest_bridge_packet.json` localement.
4. Aucun transfert automatique n'est effectué.
5. Le fichier est ignoré par git (`.gitignore` couvre `output/*.json`).

---

## 6. Prérequis pour une ingestion future

Ce qui serait nécessaire avant d'activer l'Option B ou C :

| Prérequis | Statut |
|-----------|--------|
| Bridge packet V1 défini et stable | **FAIT** |
| Script export dry-run fonctionnel | **FAIT** |
| Validation manuelle du contenu du packet | **À FAIRE** |
| Module admin-trading de lecture du packet | **NON FAIT** (GO séparé) |
| Transfert SFTP/WinSCP automatisé | **NON FAIT** (GO séparé) |
| Tests de non-régression webhook | **NON FAIT** |
| Validation desk/risk de non-impact | **NON FAIT** |

---

## 7. Invariants respectés

- [x] admin-trading reste runtime webhook canonique
- [x] Le pont Phase 5 est une revue / préparation, pas une ingestion active
- [x] Aucun service systemd modifié
- [x] Aucun webhook remplacé
- [x] Aucun trade réel
- [x] Aucun ordre
- [x] Aucune mutation TradingView
- [x] Aucune suppression d'alerte
- [x] Aucun fichier live JSON sensible committé
- [x] `output/latest_*.json` non committé
- [x] Aucun secret, .env, token committé

---

## 8. Verdict Phase 5

**PASS** — Option A (local manuel), bridge packet V1 défini et scripté, Options B/C documentées pour GO futurs.

## 9. Next GO recommandé

`GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_PRODUCT_HARDENING_01`

Objectif : durcir le produit local sans pont admin-trading actif.

## RISKS

- À qualifier.
