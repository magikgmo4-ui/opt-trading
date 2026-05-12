---
doc_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01_40_IDE_YML_DECISION
doc_type: chantier/decision
repo: opt-trading
machine: admin-trading
go_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01
status: active
scope: doc-only
links:
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01/60_ADMIN_TRADING_PROBE_RESULTS.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01/30_TMUX_IDE_PROBE.md
---

# 40_IDE_YML_DECISION

## État établi — ETAT_DECLARE (probe 2026-05-11)

Source : `GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01/60_ADMIN_TRADING_PROBE_RESULTS.md`

| Élément | Résultat établi |
| --- | --- |
| `ide.yml` dans `/opt/trading` | ABSENT |

---

## Re-probe live ide.yml — À CAPTURER

```bash
ssh admin-trading "cd /opt/trading && test -f ide.yml && echo 'ide.yml: PRESENT' && cat ide.yml || echo 'ide.yml: absent'"
```

Sortie :
```
ide.yml: absent
```

---

## Décision ide.yml

```
ETAT_VERIFIE — ide.yml
Résultat:
ide.yml: absent
Décision:
Ne pas créer ide.yml dans ce GO.
La création ide.yml dépend d'abord:
1. arbitrage de la branche active admin-trading;
2. qualification install tmux-ide compatible linux x64;
3. validation explicite d'un GO d'installation/configuration.
```

### ide.yml est absent — re-probe confirmé 2026-05-12

`ide.yml` ne doit **pas** être créé dans ce GO.

Deux blocages préalables non levés :
1. Branche admin-trading non canonique (GO Git arbitration requis)
2. tmux-ide incompatible linux x64 (EBADPLATFORM — analyse compatibilité requise)

La création de `ide.yml` est **non autorisée dans ce GO** sans levée de ces deux gates.

### Contenu recommandé pour ide.yml (proposition — non appliquée)

```yaml
# ide.yml — admin-trading:/opt/trading
# À créer dans un GO dédié avec gate PASS
version: 1
machine: admin-trading
repo: /opt/trading
sessions:
  - name: opt-trading
    root: /opt/trading
    windows:
      - name: main
        panes:
          - shell
```

> Ce contenu est une proposition documentaire. Il ne doit pas être écrit sur admin-trading sans GO explicite.

### Gate de création ide.yml

Conditions requises avant création :

- [ ] tmux-ide installé et disponible (gate PASS from 30_TMUX_IDE_PROBE.md)
- [ ] contenu ide.yml validé par l'opérateur
- [ ] GO dédié ouvert avec instruction explicite
- [ ] test `tmux-ide doctor` prévu après création

---

## Verdict ide.yml courant

- Re-probe live (2026-05-12) : **ABSENT (ETAT_VERIFIE)**
- Verdict courant : **gate non franchie — création bloquée par GAP_01 (branche) + GAP_02 (tmux-ide EBADPLATFORM)**
