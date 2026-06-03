# 30_EXTERNAL_INTEGRATIONS_ACTIVE_INVENTORY

## Tableau complet des intégrations externes

| # | Intégration | Statut | Fichier principal | Type credential | Méthode actuelle | Méthode canonique | Risque | Gap |
|---|-------------|--------|-------------------|-----------------|-----------------|-------------------|--------|-----|
| 1 | **Telegram** | ACTIVE | `shared/telegram_notify.py` | BOT_TOKEN + CHAT_ID_* | `.env` vars | `.env` + role `telegram_collector.env` | MEDIUM | `groupAllowFrom` vide (voir doc 40) |
| 2 | **GitHub Actions** | ACTIVE | `.github/workflows/*.yml` | GITHUB_TOKEN (auto) | Token injecté runner | Conforme — aucun changement requis | LOW | Aucun |
| 3 | **OpenAI / OpenRouter** | ACTIVE | `~/.openclaw/openclaw.json` | API_KEY (openai), OAuth (codex) | Géré par openclaw CLI | Conforme — via openclaw configure | LOW | Rotation non documentée |
| 4 | **TradingView webhook** | ACTIVE | `webhook_server.py` | TV_WEBHOOK_KEY | `.env` | `.env` + `webhook_receiver.env` role | MEDIUM | Pas de rotation automatique |
| 5 | **Bitget Exchange** | CONFIGURED | `modules/auth/bitget_credentials.py` | API_KEY + SECRET + PASSPHRASE | `.secrets/bitget.env` | Conforme (.secrets/ + example) | HIGH | Read-only profile — vérifier scope réel |
| 6 | **OpenClaw Gateway** | ACTIVE | `modules/gateway_openclaw/` | Aucun (loopback, no auth token requis) | tmux session openclaw-gateway | Conforme | LOW | groupAllowFrom Telegram (voir doc 40) |
| 7 | **OpenClaw Operator Bridge** | ACTIVE | `modules/openclaw_operator_bridge/app/bridge.py` | OPENCLAW_GATEWAY_URL (loopback) | env var | Conforme | LOW | Si gateway down → fallback stub |
| 8 | **Botpress** | CONFIGURED (stub) | `adapter_botpress_openclaw.py` | OPENCLAW_GATEWAY_URL, OPENCLAW_TIMEOUT_MS | env vars | env vars + rate limiter + circuit breaker | MEDIUM | Intent EXECUTE_TRADE bloqué — adapter jamais appelé en prod |
| 9 | **SSHFS remote** | ACTIVE | `/etc/opt-trading/shared_sshfs_permanent.env` | SSH key (IDENTITY_FILE), REMOTE_HOST/USER | Fichier système `/etc/` | Conforme (fichier système, hors git) | MEDIUM | Chemin clé SSH à auditer |
| 10 | **Google Sheets** | CONFIGURED | `configs/env/roles/google_sheets.env.example` | SERVICE_ACCOUNT_JSON_PATH | Role file (non déployé) | Conforme si role file chargé | LOW | Service account JSON doit être hors git |
| 11 | **tmux multi-machine** | OPERATIONAL | `modules/openclaw_tmux_operator/` | SSH implicite (openclaw user) | SSH via config | Conforme | LOW | machine_runtime_map.yml à auditer |
| 12 | **OpenClaw MCP** | ACTIVE | `modules/governance/openclaw_mcp_policy_validator/` | Aucun credential externe | N/A | N/A | LOW | Policy statique uniquement |
| 13 | **Binance / Coinglass** | CONFIGURED | `configs/env/roles/market_data_readonly.env.example` | BINANCE_API_KEY, COINGLASS_API_KEY | Role file (non déployé) | Conforme si role file chargé | LOW | Coinglass = headless browser, API non prouvée |
| 14 | **ClickUp** | ABSENT | — | — | Aucune référence trouvée dans le repo | N/A | N/A | Pas de preuve d'intégration |
| 15 | **Desk Pro / LocalCMS** | INTERNAL | `modules/desk_pro/`, `modules/localcms/` | OPS_ADMIN_KEY | `.env` | Conforme | LOW | Read-only LocalCMS, aucune écriture |

---

## Détail par intégration critique

### Telegram (ACTIVE — WARNING)

- **Bot connecté** : gateway health confirme `@ghost_admin_trading_bot` actif
- **Canaux configurés** : CHAT_ID_PIPELINE, CHAT_ID_OPS, CHAT_ID_PUSH dans `.env`
- **Problème** : `groupPolicy=allowlist` mais `groupAllowFrom` absent → messages groupe droppés
- **Fix** : voir `40_TELEGRAM_GROUP_POLICY_AND_ALLOWLIST.md`

### GitHub Actions (ACTIVE — CONFORME)

```
7 workflows actifs :
  gated-pr.yml                            ← validation PR gate
  gh-actions-registry-validation.yml      ← validation registry
  openclaw-mcp-policy-static-validator.yml ← governance policy
  openclaw-skill-policy-warning-only.yml  ← skill policy
  strict-workers-schedule.yml             ← schedule workers
  strict-workers-smoke.yml                ← smoke test
  strict-workers-validate.yml             ← validation
```

Tous en `permissions: contents: read`. Aucun secret externe requis. Token GitHub auto.

### OpenAI / OpenRouter via OpenClaw (ACTIVE — CONFORME)

```
Auth profiles :
  openai:default       → mode api_key
  openai-codex:default → mode oauth

Modèles actifs :
  openai/gpt-5.4
  openrouter/qwen/qwen3-32b
  openrouter/qwen/qwen3-coder-30b-a3b-instruct
  openrouter/deepseek/deepseek-r1
  openrouter/qwen/qwen3-14b
```

Géré exclusivement par `openclaw configure` — conforme.

### Bitget (CONFIGURED — À AUDITER)

- Profil `readonly_main` — scope lecture seule à vérifier (pas de trading autorisé par les clés)
- Fichier `.secrets/bitget.env` non versionné, conforme
- **Gap** : vérifier que le scope API est bien limité à la lecture sur la console Bitget

---

## Check anti-leak — résultat

```bash
git diff -- . ':!*.png' ':!*.jpg' | grep -Ei 'token|secret|api_key|api_hash|password|bearer|webhook'
```

Résultat : **CLEAN** — aucun secret dans le diff courant.

---

## ClickUp — verdict

Aucune référence à ClickUp dans :
- `modules/`
- `scripts/`
- `.github/workflows/`
- `configs/`
- `docs/`

**Verdict : ABSENT du repo.** Intégration non initiée.
