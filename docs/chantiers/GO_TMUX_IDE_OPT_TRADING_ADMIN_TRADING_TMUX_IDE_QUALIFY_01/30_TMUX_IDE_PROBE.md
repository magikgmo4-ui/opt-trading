---
doc_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01_30_TMUX_IDE_PROBE
doc_type: chantier/probe
repo: opt-trading
machine: admin-trading
go_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01
status: active
scope: doc-only
links:
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01/60_ADMIN_TRADING_PROBE_RESULTS.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01/20_PREREQUISITES_CHECK.md
---

# 30_TMUX_IDE_PROBE

## État établi — ETAT_DECLARE (probe 2026-05-11)

Source : `GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01/60_ADMIN_TRADING_PROBE_RESULTS.md`

| Élément | Résultat établi |
| --- | --- |
| `command -v tmux-ide` | FAIL — commande absente |
| `tmux-ide` via npx | FAIL — non détecté |

---

## Re-probe live tmux-ide — À CAPTURER

### Vérification commande globale

```bash
ssh admin-trading "command -v tmux-ide || echo 'tmux-ide: absent'"
```

Sortie :
```
tmux-ide: absent
```

### Vérification via npx (sans installation)

```bash
ssh admin-trading "npx --yes tmux-ide --version 2>&1 || echo 'npx tmux-ide: inaccessible ou absent'"
```

Sortie :
```
FAIL
Erreur: EBADPLATFORM
Package détecté: @opentui/core-darwin-arm64@0.1.107
Plateforme attendue: darwin arm64
Plateforme réelle: linux x64
```

> Le package `tmux-ide` dépend de `@opentui/core-darwin-arm64`, binaire natif macOS arm64.
> Il est incompatible avec la plateforme `linux x64` de `admin-trading`.
> Ce n'est pas un problème d'absence réseau — le package existe sur npm mais ne peut pas s'exécuter sur cette machine.

### Vérification présence locale dans le repo

```bash
ssh admin-trading "cd /opt/trading && ls node_modules/.bin/tmux-ide 2>/dev/null || echo 'tmux-ide: absent dans node_modules'"
```

Sortie :
```
tmux-ide: absent dans node_modules
```

---

## Interprétation

| Cas | Signification | Verdict |
| --- | --- | --- |
| `command -v tmux-ide` retourne un chemin | tmux-ide installé globalement | PASS — disponible |
| `npx tmux-ide --version` retourne une version | tmux-ide accessible via npx | PASS — disponible via npx |
| `node_modules/.bin/tmux-ide` présent | tmux-ide installé localement dans le repo | PASS — disponible localement |
| Tous FAIL | tmux-ide absent, installation requise | PARTIAL_PASS — gate à franchir |

---

## Verdict tmux-ide courant (ETAT_VERIFIE — 2026-05-12)

```
ETAT_VERIFIE — tmux-ide
command -v tmux-ide:
absent
npx --yes tmux-ide --version:
FAIL
Erreur:
EBADPLATFORM
Package détecté: @opentui/core-darwin-arm64@0.1.107
Plateforme attendue: darwin arm64
Plateforme réelle: linux x64
Verdict:
tmux-ide non qualifié.
Ne pas installer dans ce GO.
Ouvrir un GO séparé d'analyse d'installation / compatibilité seulement après arbitrage Git admin-trading.
```

- Re-probe live (2026-05-12) : **FAIL — EBADPLATFORM**
- Verdict courant : **FAIL (ETAT_VERIFIE)** — tmux-ide absent et incompatible plateforme linux x64

---

## Gate d'installation

L'installation de `tmux-ide` sur `admin-trading` est **non autorisée dans ce GO** sans gate explicite.

La qualification ici constate l'absence et prépare la décision d'installation pour le GO suivant.

Commande d'installation (à réserver pour un GO dédié avec gate PASS) :

```bash
# Sur admin-trading, dans /opt/trading :
npm install -g tmux-ide
# OU
npm install --save-dev tmux-ide
```

> Ne pas exécuter dans ce GO.
