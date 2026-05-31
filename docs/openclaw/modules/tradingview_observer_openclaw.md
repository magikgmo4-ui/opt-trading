---
doc_id: OPENCLAW_MODULE_TRADINGVIEW_OBSERVER_OPENCLAW
doc_type: module_fiche
module: tradingview_observer_openclaw
path: modules/tradingview_observer_openclaw/
go_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_EXTRACTION_01
updated_at: 2026-05-30
statut: actif
plateforme: Windows / PowerShell
---

# tradingview_observer_openclaw — Fiche opérateur

Skill OpenClaw permettant de lire TradingView Desktop via le wrapper opt-trading read-only.
Module **Windows uniquement** — entrypoint PowerShell.

## Règle fondamentale

```
Read-only strict.
OpenClaw ne modifie jamais TradingView, les alertes, ou admin-trading.
```

## Prérequis

```
Wrapper modules/tradingview_observer/ opérationnel (Phase 3-6)
TradingView Desktop lancé avec CDP sur 127.0.0.1:9222
Node.js v24+ disponible
```

## Entrypoint

```powershell
.\run.ps1 sanity     # 7 checks (CDP, CLI, state, quote, alerts, mutation locked)
.\run.ps1 snapshot   # sanity + export 6 JSON dans output/
.\run.ps1 bridge     # export bridge packet V1 (dry-run, sans transfert)
```

## Flow de sécurité

```
OpenClaw → run.ps1 → cmd.ps1 → app/observer_runner.ps1 → TV CLI → CDP 9222
                              ↳ sanity_check.ps1
                              ↳ export_bridge_packet.ps1
```

OpenClaw n'accède **jamais** directement à CDP ou au CLI tradingview-mcp.

## Outputs (après snapshot)

```
modules/tradingview_observer/output/
  latest_status.json          — santé CDP + chart
  latest_quote.json           — OHLC courant
  latest_state.json           — état graphique (symbole, TF, études)
  latest_alert_inventory.json — inventaire alertes
  latest_values.json          — valeurs indicateurs
  latest_report.json          — rapport combiné
  latest_bridge_packet.json   — bridge packet V1 (après bridge)
```

## Contenu module

```
run.ps1       — entrypoint PowerShell
skill.md      — définition skill OpenClaw complète
README.md     — documentation opérateur
```

## Forbidden (ne jamais faire)

```
- Accéder directement au port 9222 (CDP)
- Appeler tradingview-mcp directement
- Appeler observer_runner.ps1 directement
- Créer / supprimer / modifier une alerte
- Configurer un webhook
- Exécuter un trade
- Modifier admin-trading
- Lancer tv launch (demander à l'opérateur si TradingView est fermé)
- Committer les fichiers output/latest_*.json
```

## Modes d'échec

| Erreur | Cause | Action |
| --- | --- | --- |
| CDP port closed | TradingView Desktop fermé | Demander à l'opérateur de lancer TV |
| tradingview-mcp CLI missing | Installation incomplète | Signaler le chemin manquant |
| JSON parse error | Données corrompues | Relire, signaler l'erreur |
| report missing | Snapshot non exécuté | Lancer snapshot d'abord |
| Wrapper not found | Module non installé | Vérifier arborescence opt-trading |

## Statut

```
actif — skill OpenClaw read-only TradingView Desktop
plateforme: Windows / PowerShell
```
