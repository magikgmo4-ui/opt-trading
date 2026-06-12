# Rotation Schedule — Credentials — 2026-06-11

Aucune valeur secrète dans ce document. Uniquement : env_var, provider, criticité,
TTL recommandé, dernière rotation connue, prochaine rotation prévue, statut.

**Statuts :**
- `FRESH` — dans le TTL, aucune action requise
- `UNKNOWN` — date de création inconnue, vérification manuelle recommandée
- `N/A` — non-secret (resource ID, URL, feature flag) — pas de rotation
- `DISABLED` — credential désactivé, non déployé

---

## 1. Secrets actifs à rotation obligatoire

| Env Var | Provider | Type | Criticité | TTL rec. | Dernière rotation | Prochaine rotation | Statut |
|---------|----------|------|-----------|----------|-------------------|--------------------|--------|
| `TV_WEBHOOK_KEY` | internal | webhook_key | CRITICAL | 90j | UNKNOWN | — | UNKNOWN |
| `OPS_ADMIN_KEY` | internal | admin_key | CRITICAL | 90j | UNKNOWN | — | UNKNOWN |
| `TELEGRAM_BOT_TOKEN` | telegram | bot_token | CRITICAL | 365j | UNKNOWN | — | UNKNOWN |
| `TELEGRAM_API_ID` | telegram | api_id | CRITICAL | permanent | initial setup | — | N/A |
| `TELEGRAM_API_HASH` | telegram | api_hash | CRITICAL | permanent | initial setup | — | N/A |
| `GH_TOKEN` | github | auth_token | CRITICAL | 90j | 2026-06-11 | 2026-09-09 | FRESH |
| `OPENAI_API_KEY` | openai | api_key | CRITICAL | 180j | UNKNOWN | — | UNKNOWN |
| `AIRTABLE_API_KEY` | airtable | api_key | HIGH | 180j | UNKNOWN | — | UNKNOWN |
| `CLICKUP_TOKEN` | clickup | auth_token | HIGH | 180j | UNKNOWN | — | UNKNOWN |
| `BOTPRESS_API_TOKEN` | botpress | auth_token (PAT) | HIGH | 90j | 2026-06-11 | 2026-09-09 | FRESH |
| `BOTPRESS_BOT_API_KEY` | botpress | api_key (BAK) | HIGH | 180j | 2026-06-11 | 2026-12-08 | FRESH |
| `BOTPRESS_WEBHOOK_SECRET` | botpress | webhook_secret | HIGH | 90j | 2026-06-11 | 2026-09-09 | FRESH |
| `FIGMA_TOKEN` | figma | personal_access_token | HIGH | 90j | 2026-06-11 | 2026-09-09 | FRESH |

---

## 2. Clés API marché — gratuites

| Env Var | Provider | Criticité | TTL rec. | Dernière rotation | Prochaine rotation | Statut |
|---------|----------|-----------|----------|-------------------|--------------------|--------|
| `COINGECKO_API_KEY` | coingecko | MEDIUM | 365j | 2026-06-11 | 2027-06-11 | FRESH |
| `ALPHAVANTAGE_API_KEY` | alphavantage | MEDIUM | 365j | 2026-06-11 | 2027-06-11 | FRESH |
| `FRED_API_KEY` | fred | MEDIUM | 365j | 2026-06-11 | 2027-06-11 | FRESH |
| `EIA_API_KEY` | eia | MEDIUM | 365j | 2026-06-11 | 2027-06-11 | FRESH |
| `FINNHUB_API_KEY` | finnhub | MEDIUM | 365j | 2026-06-11 | 2027-06-11 | FRESH |
| `TWELVEDATA_API_KEY` | twelvedata | MEDIUM | 365j | 2026-06-11 | 2027-06-11 | FRESH |

---

## 3. Infrastructure — clés SSH et ADC

| Env Var / Artefact | Provider | Criticité | TTL rec. | Dernière rotation | Prochaine rotation | Statut |
|--------------------|----------|-----------|----------|-------------------|--------------------|--------|
| `IDENTITY_FILE` (`id_ed25519`) | internal | CRITICAL | 365j | UNKNOWN | — | UNKNOWN |
| `GOOGLE_APPLICATION_CREDENTIALS` (ADC) | google | HIGH | auto-refresh | 2026-06-11 (login) | auto | N/A |
| WireGuard `WG_PRIVATE_KEY` | internal | HIGH | 365j | UNKNOWN | — | UNKNOWN |
| Termux SSH key | internal | LOW | 365j | UNKNOWN | — | UNKNOWN |

---

## 4. Non-secrets — pas de rotation

| Env Var | Type | Raison |
|---------|------|--------|
| `TELEGRAM_SESSION_PATH` | file_path | chemin local, pas un secret |
| `TELEGRAM_ALERT_CHAT_ID` / `_PIPELINE` / `_PUSH` / `_OPS` | chat_id | identifiant public Telegram |
| `TELEGRAM_ALLOWED_CHAT_IDS` / `_USER_IDS` | config | contrôle d'accès, non secret |
| `TELEGRAM_CHANNELS_CONFIG` | file_path | chemin config |
| `GOOGLE_SHEETS_SYNC_SHEET_ID` | resource_id | ID sheet public |
| `BOTPRESS_WORKSPACE_ID` / `BOT_ID` / `WEBHOOK_URL` | resource_id / url | non secrets |
| `FIGMA_FILE_KEY` / `TEAM_ID` / `USER_ID` | resource_id | non secrets |
| `AIRTABLE_BASE_ID` / `TABLE_GO_STATUS` | resource_id | non secrets |
| `OLLAMA_BASE_URL` | url | local endpoint |
| `ENABLE_*_PUBLIC` (10 flags) | feature_flag | pas de secret |
| `BINANCE_API_KEY` / `SECRET` | disabled | non déployé |

---

## 5. Résumé actions requises

| Priorité | Action | Credentials concernés |
|----------|--------|----------------------|
| 🔴 P1 | Vérifier date de création et rotater si > TTL | `TV_WEBHOOK_KEY`, `OPS_ADMIN_KEY`, `TELEGRAM_BOT_TOKEN` |
| 🟠 P2 | Vérifier date et rotater si > 180j | `OPENAI_API_KEY`, `AIRTABLE_API_KEY`, `CLICKUP_TOKEN` |
| 🟡 P3 | Vérifier date SSH key | `IDENTITY_FILE` (`id_ed25519`), `WG_PRIVATE_KEY` |
| 🟢 P4 | Aucune action — FRESH | `GH_TOKEN`, `BOTPRESS_*`, `FIGMA_TOKEN`, toutes clés marché |
| ⚪ P5 | Aucune action — N/A | ADC Google (auto-refresh), resource IDs, feature flags |

---

## 6. Prochains rappels FRESH

| Date | Action |
|------|--------|
| 2026-09-09 | Rotater : `GH_TOKEN`, `BOTPRESS_API_TOKEN`, `BOTPRESS_WEBHOOK_SECRET`, `FIGMA_TOKEN` |
| 2026-12-08 | Rotater : `BOTPRESS_BOT_API_KEY` |
| 2027-06-11 | Rotater : toutes clés marché gratuites (CoinGecko, AlphaVantage, FRED, EIA, Finnhub, TwelveData) |
