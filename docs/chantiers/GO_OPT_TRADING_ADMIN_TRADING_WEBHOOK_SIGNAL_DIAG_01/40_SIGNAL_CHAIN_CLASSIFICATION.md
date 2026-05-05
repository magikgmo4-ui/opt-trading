---
doc_id: SIGNAL_DIAG_01_CLASSIFICATION
doc_type: classification
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 40_SIGNAL_CHAIN_CLASSIFICATION

## Causes eliminees

| Hypothese | Verdict | Preuve |
| --- | --- | --- |
| B: URL ngrok changee | ELIMINEE | URL actuelle = URL dans journal.md |
| C: Tunnel ngrok down | ELIMINEE | Session active, connectee |
| D: /tv route cassee | ELIMINEE | 405 Method Not Allowed (correct, POST-only) |
| E: Webhook rejette | ELIMINEE | Zero erreurs dans logs, zero requetes |
| F: Erreur reseau | ELIMINEE | Public /docs accessible depuis internet |

## Cause la plus probable

### A: TradingView alerts disabled/paused/expired — CONFIANCE ELEVEE

- ngrok metrics: **zero connections** (personne n'appelle)
- URL ngrok: inchangee (confirme dans journal.md)
- Webhook: UP et fonctionnel (pas de crash, pas de rejet)
- Dernier signal: April 1 a 07:12 — arret brutal et complet

Sous-hypotheses:
1. **Alerte TradingView desactivee manuellement**
2. **Pine Script alert expiree ou supprimee**
3. **Strategie TradingView arretee**
4. **Limite d'alertes free tier atteinte**

## Cause secondaire

### Ngrok instable — IMPACT FAIBLE

- Heartbeat timeouts frequents (May 1, May 4)
- Sessions drop puis reconnect (~1 min downtime)
- Si les drops tombent pendant une alerte TradingView, l'alerte est perdue
- Mais meme quand ngrok est UP, il n'y a zero trafic

## Niveau de confiance

**ELEVE** — La cause est cote TradingView. Le serveur est operationnel, l'URL est correcte,
le tunnel est UP. Mais personne n'appelle.
