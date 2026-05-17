# Décision — Prochaine phase paper-mode

## État courant (Phase 0 — PASS)

| Critère                       | Valeur      | Seuil Phase 1 | Gap     |
| ----------------------------- | ----------- | ------------- | ------- |
| Runs sans fail                | 13          | ≥ 30          | -17     |
| Jours d'observation           | 1 (dense)   | ≥ 14          | -13     |
| Kill switch testé             | NON         | OUI           | manque  |
| Telegram end-to-end testé     | NON         | OUI           | manque  |
| Win rate                      | 100%        | ≥ 50%         | OK      |
| P&L cumulé paper              | +5694.39    | > 0           | OK      |

**Conclusion : les prérequis de Phase 1 ne sont pas encore atteints.**
L'expansion multi-signal (option B) est prématurée tant que les
garde-fous (C) ne sont pas validés et que le seuil de 30 runs n'est
pas atteint.

---

## Analyse des options

### A — Observation continue mono-signal

| Avantages                                   | Risques / Coûts |
| ------------------------------------------- | --------------- |
| Zéro effort, timer déjà actif               | Aucun           |
| Atteint 30 runs automatiquement             |                 |
| Données stables avant expansion             |                 |
| Conforme aux critères Phase 1               |                 |

**Effort** : zéro. **Déjà en cours.**

**Déclencheur de sortie** : 30 runs sans fail + 14 jours → passer à B.

---

### B — Paper élargi BTC/ETH/SOL

| Avantages                                   | Risques / Coûts                       |
| ------------------------------------------- | ------------------------------------- |
| Valide le pipeline multi-ticker             | Prérequis Phase 1 non atteints        |
| Plus représentatif d'une prod réelle        | Kill switch non testé                 |
| Nourrit plus de données journal             | Telegram non testé                    |
| Accélère l'accumulation de runs             | Complexité journal multi-run/day      |

**Effort** : moyen — nouveau GO d'implémentation.

**Blocage** : ne peut pas démarrer avant validation C (kill switch + Telegram)
et atteinte du seuil A (30 runs).

---

### C — Tester kill switch + Telegram avant multi-signal

| Avantages                                   | Risques / Coûts                       |
| ------------------------------------------- | ------------------------------------- |
| Valide les garde-fous critiques             | Effort faible (tests manuels)         |
| Débloque le prérequis Phase 1               |                                       |
| Peut s'exécuter en parallèle de A           |                                       |
| Aucun risque (dry-run)                      |                                       |

**Effort** : faible — tests manuels + GO de validation documenté.

**Peut être lancé immédiatement en parallèle de A.**

---

### D — Préparer GO_LIVE_ACTIVATION doc-only

| Avantages                                   | Risques / Coûts             |
| ------------------------------------------- | --------------------------- |
| Vision du chemin vers live                  | Aucun (doc-only)            |
| Permet d'anticiper les gaps restants        |                             |
| Décision live repoussée à un GO séparé      |                             |

**Effort** : faible — documentation pure.

**Peut être lancé en parallèle de A + C, ou après.**

---

## Recommandation

```
C en premier → A en parallèle → B quand seuil atteint → D après B
```

### Séquence détaillée

**Immédiat (parallèle) :**
- **A** : observation continue — timer tourne déjà, rien à faire
- **C** : valider kill switch + Telegram → débloquer prérequis Phase 1

**Quand A ≥ 30 runs ET C validé :**
- **B** : paper élargi BTC/ETH/SOL — GO d'implémentation dédié

**Quand B stable ≥ 30 runs :**
- **D** : GO_LIVE_ACTIVATION doc-only pour préparer la décision live

### Prochains GOs à créer

| GO                                                              | Priorité | Quand                     |
| --------------------------------------------------------------- | -------- | ------------------------- |
| GO_OPENCLAW_OPT_TRADING_KILL_SWITCH_TELEGRAM_VALIDATION_01     | HAUTE    | Maintenant                |
| GO_OPENCLAW_OPT_TRADING_PAPER_MODE_MULTI_SIGNAL_IMPL_01        | MOYENNE  | Après A≥30 + C validé     |
| GO_LIVE_ACTIVATION_PAPER_TO_LIVE_PROTOCOL_01                   | BASSE    | Après B≥30 runs           |

## Invariants conservés quelle que soit l'option

- No live trade / No Bitget order
- No automatic Sheets write
- Controlled-write manuel uniquement
- Rollback systemd disponible
- No secrets in repo or logs
- Kill switch non testé = expansion bloquée
