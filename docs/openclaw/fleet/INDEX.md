---
doc_id: OPENCLAW_FLEET_INDEX
doc_type: fleet_matrix
repo: opt-trading
go_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_FLEET_MATRIX_01
updated_at: 2026-05-30
---

# docs/openclaw/fleet — Matrice fleet OpenClaw

Vue unifiée de la fleet depuis la perspective OpenClaw : statut runtime,
rôle dans l'orchestration, preuves, gaps restants.

Sources : `config/machine_runtime_map.yml`, `tests/runtime_health/`,
`GO_OPT_TRADING_RUNTIME_HEALTH_FLEET_WARN_CLASSIFICATION_01` (CLOSED 2026-05-19).

---

## Matrice synthèse

| Machine | OS | Statut runtime | Rôle OpenClaw | Preuve |
| --- | --- | --- | --- | --- |
| **admin-trading** | Linux | WARN EXPECTED | Surface principale, desk, artifacts | runtime_health WARN classifiés |
| **db-layer** | Linux | WARN EXPECTED | **Hôte gateway OpenClaw** (18789) | gateway prouvé 127.0.0.1:18789 |
| **cursor-ai** | Windows | PASS / healthy | IDE agent Windows, TradingView observer | PR #592/#595/#600 |
| **fantome** | Linux | PASS 12/12 | Machine réseau secondaire | PR #589/#590 |
| **student** | Linux | WARN EXPECTED | Ollama lab (conditionnel) | WARN classifiés, lab non actif |
| **mobile** | Android/Termux | NOT_PROVEN | Job control mobile (conditionnel) | aucune preuve runtime OpenClaw |

---

## Détail par machine

### admin-trading

```
OS       : Linux
Rôle     : surface principale ops — desk, artifacts, bot_vision, webhook
OpenClaw : non hôte gateway — client potentiel
Statut   : WARN EXPECTED (services/timers optionnels non actifs en Phase 1)

WARNs classifiés (GO_WARN_CLASSIFICATION_01) :
  service:simex-bitget          EXPECTED — optional Phase 1
  service:mimo_open_observer    EXPECTED — optional
  timer:bot_vision_step2_send   EXPECTED — timer non actif
  timer:macro_xau               EXPECTED — timer non actif
  env:TV_WEBHOOK_KEY            EXPECTED — optional
  port:openclaw_gateway         EXPECTED — gateway sur db-layer, pas admin
  artifact:desk_vision_dir      EXPECTED — dry-run Phase 1
  tmux:openclaw/trading/desk    EXPECTED — sessions down Phase 1
```

### db-layer

```
OS       : Linux
Rôle     : HÔTE PRIORITAIRE OpenClaw gateway
OpenClaw : utilisateur openclaw, session tmux openclaw-gateway, port 18789
Statut   : WARN EXPECTED (venv/env/path optionnels)

WARNs classifiés :
  venv:main                     EXPECTED — optional, non installé
  env:TELEGRAM_BOT_TOKEN        EXPECTED — optional
  port:openclaw_gateway         EXPECTED — gateway présent mais WARN si check externe
  path:/var/log/trading         EXPECTED — optional
```

### cursor-ai

```
OS       : Windows (DESKTOP-1KDQTBH → alias cursor-ai)
Rôle     : IDE agent Windows, TradingView observer (CDP 9222), observer skill
OpenClaw : source collecte = ssh_windows, health via PowerShell -EncodedCommand
Statut   : PASS / healthy / reachable

Preuves :
  PR #592  — os_family: windows, hostname_aliases, SSH PowerShell, 25 tests
  PR #595  — canonical_name_for(), alias resolution
  PR #600  — -EncodedCommand base64 (contourne cmd.exe)
  commit 4917af43 — bytes mode stdout, CLIXML stderr bypass

Skill OpenClaw : tradingview_observer_openclaw (run.ps1, read-only strict)
```

### fantome

```
OS       : Linux
Rôle     : machine réseau secondaire
OpenClaw : pas de gateway — client potentiel futur
Statut   : PASS 12/12

Preuves :
  PR #589 — fantome reachable
  PR #590 — cleanup defaults Linux, PASS

Notes :
  optional_services = []      (openclaw-gateway sur db-layer)
  optional_ports = []         (port 18789 suit db-layer)
  optional_tmux_sessions = [] (sessions à déployer via openclaw depuis db-layer)
```

### student

```
OS       : Linux (Ollama local)
Rôle     : lab Ollama conditionnel (non actif en production)
OpenClaw : OpenClaw lab (user openclaw-lab, port 18790 proposé) — NON DÉPLOYÉ
Statut   : WARN EXPECTED

WARNs classifiés :
  service:snap.ollama.listener  EXPECTED — ollama non actif
  env:TELEGRAM_BOT_TOKEN        EXPECTED — optional
  (http/artifact/tmux/log)      FALSE_POSITIVES supprimés

Condition de fermeture gap student :
  Déployer openclaw-lab sur student ET prouver health/probe sur 127.0.0.1:18790
  → hors scope Phase 1
```

### mobile

```
OS       : Android / Termux
Rôle     : job control mobile conditionnel
OpenClaw : GO_OPENCLAW_TERMUX_MOBILE_* existent (3 chantiers) — non prouvés runtime
Statut   : NOT_PROVEN

Chantiers existants :
  GO_OPENCLAW_TERMUX_MOBILE_JOB_CONTROL_01
  GO_OPENCLAW_TERMUX_MOBILE_PHASE01_SMOKE_01
  GO_OPENCLAW_TERMUX_MOBILE_RUNTIME_CONTROL_WRAPPER_01

Condition de fermeture gap mobile :
  Exécuter GO_OPENCLAW_TERMUX_MOBILE_PHASE01_SMOKE_01
  Prouver que OpenClaw peut déclencher un job Termux et recevoir un retour structuré
  → hors scope ce child (nécessite device Android actif)
```

---

## Gaps fleet restants

| Gap | Machine | Condition fermeture |
| --- | --- | --- |
| student OpenClaw lab | student | Déployer openclaw-lab (port 18790) + prouver health |
| mobile NOT_PROVEN | mobile | Smoke GO_OPENCLAW_TERMUX_MOBILE_PHASE01_SMOKE_01 sur device Android |

---

## Vérification

```bash
# État runtime_health local
cat /opt/trading/data/runtime_health/latest.json 2>/dev/null | python3 -m json.tool | head -30

# Machines dans le map
grep -E "^  [a-z]" /opt/trading/config/machine_runtime_map.yml

# Tests fleet
python3 -m unittest tests/runtime_health/test_warn_classification.py -v
python3 -m unittest tests/runtime_health/test_cursor_ai_windows.py -v
```
