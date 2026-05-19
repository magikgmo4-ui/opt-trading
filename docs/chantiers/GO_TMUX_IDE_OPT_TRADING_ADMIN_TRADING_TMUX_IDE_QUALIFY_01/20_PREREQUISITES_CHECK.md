---
doc_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01_20_PREREQUISITES_CHECK
doc_type: chantier/prerequisites
repo: opt-trading
machine: admin-trading
go_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01
status: active
scope: doc-only
links:
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01/60_ADMIN_TRADING_PROBE_RESULTS.md
---

# 20_PREREQUISITES_CHECK

## Prérequis établis — ETAT_DECLARE (probe 2026-05-11)

Source : `GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01/60_ADMIN_TRADING_PROBE_RESULTS.md`

| Prérequis | Résultat établi | Version connue |
| --- | --- | --- |
| `tmux` | PASS | `tmux 3.3a` |
| `node` | PASS | `v18.20.4` |
| `npm` | PASS | `9.2.0` |
| `npx` | PASS (inclus avec npm/node) | — |

---

## Re-probe live prérequis — À CAPTURER

Commande :

```bash
ssh admin-trading "command -v tmux && tmux -V; command -v node && node --version; command -v npm && npm --version; command -v npx && npx --version"
```

Sortie réelle :
```
ETAT_VERIFIE — prérequis système
tmux: /usr/bin/tmux, version 3.3a
node: v18.20.4
npm: 9.2.0
npx: 9.2.0
Verdict:
PASS pour les prérequis de base.
```

Verdict re-probe :

| Prérequis | Résultat live |
| --- | --- |
| `tmux` | PASS — `/usr/bin/tmux`, version 3.3a |
| `node` | PASS — v18.20.4 |
| `npm` | PASS — 9.2.0 |
| `npx` | PASS — 9.2.0 |

---

## Synthèse prérequis

- Re-probe live (2026-05-12) : tous PASS.
- Verdict prérequis courant : **PASS (ETAT_VERIFIE)**
