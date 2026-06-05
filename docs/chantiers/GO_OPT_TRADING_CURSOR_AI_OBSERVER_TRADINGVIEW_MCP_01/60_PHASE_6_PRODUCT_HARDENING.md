# 60_PHASE_6 — Hardening produit

## Objectif

Transformer l'integration en outil stable, documente, securise et testable.

## Statut

**PASS** — Scripts durcis, sanity produit cree, outputs proteges, documentation complete.

Date : 2026-05-04

---

## Checklist de hardening

| # | Axe | Statut | Detail |
|---|-----|--------|--------|
| 1 | `$ErrorActionPreference = 'Stop'` | PASS | Tous les scripts |
| 2 | `$PSNativeCommandUseErrorActionPreference = $true` | PASS | Tous les scripts PS7+ |
| 3 | Validation modes autorises | PASS | cmd.ps1 liste allowed/forbidden |
| 4 | Rejet explicite mutation | PASS | `-AllowMutation` gate verifiee |
| 5 | Chemins bases sur `$PSScriptRoot` | PASS | Plus de `$MyInvocation` fragile |
| 6 | Verification tradingview-mcp | PASS | Check existence avant appel |
| 7 | Verification output/ | PASS | Creation automatique si absent |
| 8 | Messages d'erreur clairs | PASS | FR/EN mix, timestamps |
| 9 | Exit code fiable | PASS | 0 = success, non-zero = error |
| 10 | Timestamps ISO | PASS | Tous les exports + logs |
| 11 | Sorties protegees git | PASS | output/.gitignore ignore *.json |
| 12 | Product sanity global | PASS | 12 checks dans product_sanity.ps1 |
| 13 | Documentation operateur | PASS | README mis a jour |
| 14 | OpenClaw skill securise | PASS | Bridge mode ajoute, forbidden liste complete |

---

## Fichiers modifies / durcis

### Wrapper (`modules/tradingview_observer/`)

| Fichier | Changements |
|---------|-------------|
| `cmd.ps1` | `$PSScriptRoot`, mode validation (allowed/forbidden), `-Bridge` mode, meilleur usage |
| `sanity_check.ps1` | `$PSNativeCommandUseErrorActionPreference`, timestamps, check mutation verrouille, output formate |
| `app/observer_runner.ps1` | `$PSNativeCommandUseErrorActionPreference`, verification CLI, UTF8 sans BOM, compteur exports/errors, exit code conditionnel |
| `export_bridge_packet.ps1` | `$PSScriptRoot`, `[System.IO.File]::WriteAllText` pour UTF8 sans BOM |
| `README.md` | Modes documentes, tableau des sorties, bridge et product sanity |
| `product_sanity.ps1` | **NOUVEAU** — 12 checks : wrapper, OpenClaw, CLI, gitignore, sanity, snapshot, bridge, OC run, report, packet, git clean, mutation lock |

### OpenClaw (`modules/tradingview_observer_openclaw/`)

| Fichier | Changements |
|---------|-------------|
| `run.ps1` | `[ValidateSet]` pour Action, `$ErrorActionPreference`, `$PSNativeCommandUseErrorActionPreference`, mode `bridge` ajoute, output formate |
| `skill.md` | Mode `bridge` documente, forbidden liste etendue, section bridge packet ajoutee |
| `README.md` | Flow de securite, modes, bridge documente |

---

## Modes autorises (wrapper)

```
sanity    — infrastructure + TV health (7 checks)
snapshot  — sanity + export 6 JSON
bridge    — bridge packet V1 (dry-run)
status    — CDP + chart state
state     — studies on chart
quote     — OHLC current
values    — indicator values
alerts    — alert inventory
```

## Modes explicitement interdits

```
alert_create
alert_delete
webhook_update
trade
mutation
admin_push
```

Ces modes necessitent le flag `-AllowMutation` et un GO explicite.

---

## Sanity produit (12 checks)

| # | Check | Description |
|---|-------|-------------|
| 1 | Wrapper present | `cmd.ps1` existe |
| 2 | OpenClaw skill present | `run.ps1` existe |
| 3 | tradingview-mcp CLI present | `index.js` accessible |
| 4 | output/.gitignore present | Protege contre commits |
| 5 | cmd.ps1 sanity PASS | Infrastructure checks |
| 6 | cmd.ps1 snapshot PASS | Export JSON fonctionnel |
| 7 | export_bridge_packet.ps1 PASS | Bridge dry-run OK |
| 8 | OpenClaw run.ps1 PASS | OC skill sain |
| 9 | latest_report.json existe | Sortie valide |
| 10 | latest_bridge_packet.json existe | Bridge packet present |
| 11 | Git: no live JSON tracked | Aucun output committe |
| 12 | No unguarded mutation | Scripts proteges |

---

## Securite renforcee

- **UTF8 sans BOM** : `[System.IO.File]::WriteAllText` evite les artefacts BOM dans les JSON
- **Timestamps** : chaque check a un timestamp HH:mm:ss pour tracabilite
- **Exit codes** : 0 = all good, >0 = problems, conditionnel (snapshot tolere 1-2 erreurs)
- **Mutation gate** : flag `-AllowMutation` verifie dans cmd.ps1 et observer_runner.ps1

---

## Limites restantes

| Limite | Cause | Impact |
|--------|-------|--------|
| Webhook/payload invisible | API TradingView ne les expose pas | Pas de visibilite sur les webhooks configures |
| Alert delete partial | API REST partielle | Suppression non fiable via MCP |
| TV Desktop requis | CDP necessite TV Desktop ouvert | Le produit ne fonctionne pas sans TV Desktop |
| tradingview-mcp PR #76 | Patch local requis | Ne fonctionne pas avec le main upstream |

---

## Verdict Phase 6

**PASS** — Produit local durci, scripts robustes, sanity 12/12 defini.

## Next GO

`GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_FINAL_CLOSEOUT_01`

Objectif : closeout produit local complet, PR prete a merge.

## RISKS

- À qualifier.
