# 01 — Targets

## Architecture orchestrator

```
schedule_orchestrator.py (systemd timer → 10min)
│
├── Lit capture_map.json (27 assets, 9 screen types)
├── Lit trigger_config.json (5 schedules, cooldowns, market hours)
├── Lit screen_types.json (dispatch rules)
│
├── Pour chaque profil dû :
│   ├── Vérifie scheduler (intervalle + jitter)
│   ├── Vérifie market hours (délègue JS → capture_headless.js)
│   ├── Vérifie cooldown (state.json)
│   ├── RUN capture_headless.js --once
│   ├── Si échec → increment consecutive_failures
│   │   └── Si >= max_consecutive_failures → cooldown N min
│   └── Si succès → dispatch analyseur :
│       ├── CHART_TECHNICAL/ETF_CRYPTO → run_vision_pipeline --skip-capture
│       ├── DASHBOARD_MACRO → run_vision_pipeline --skip-capture --compose
│       ├── LIQUIDITY/FUNDING/OI/LS_RATIO → coinglass_ocr_analyzer → vision_context_writer
│       └── SCREENER_STOCKS → stub
│
└── Sauve state.json + cooldown.json
```

## Chemins d'état

```
data/bot_vision/orchestrator_state/
├── state.json      # {page_id: {last_run_ts, consecutive_failures, last_status}}
└── cooldown.json   # {page_id: cooldown_until_ts}
```

## Installation systemd

```bash
# Arrêter ancien timer
sudo systemctl stop bot-vision-headless-capture.timer
sudo systemctl disable bot-vision-headless-capture.timer

# Installer nouvel orchestrateur
sudo cp systemd/bot-vision-orchestrator.service /etc/systemd/system/
sudo cp systemd/bot-vision-orchestrator.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable bot-vision-orchestrator.timer
sudo systemctl start bot-vision-orchestrator.timer
```

## Usage

```bash
# Preview
python3 scripts/schedule_orchestrator.py --dry-run

# Run (systemd mode)
python3 scripts/schedule_orchestrator.py

# Force all (bypass schedule + market hours)
python3 scripts/schedule_orchestrator.py --dry-run --force-all

# Reset state
python3 scripts/schedule_orchestrator.py --reset-state

# One-shot (legacy compat)
python3 scripts/schedule_orchestrator.py --once --profile profiles.production.json --dry-run
```
