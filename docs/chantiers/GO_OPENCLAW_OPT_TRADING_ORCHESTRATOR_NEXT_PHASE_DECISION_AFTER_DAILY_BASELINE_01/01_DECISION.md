# Décision — Prochaine phase après baseline finale

## Contexte de décision

La baseline daily session observability est complète et validée (PR #506).
Toutes les options ci-dessous partent d'un état stable : timer actif,
journal opérationnel, Sheets sync prêt, controlled-write PASS.

## Analyse des options

### A — Observation continue 7-14 jours

| Avantages                                             | Risques / Coûts                  |
| ----------------------------------------------------- | -------------------------------- |
| Aucun changement de code                              | Aucun (état déjà validé)         |
| Accumulation de données réelles                       | ~0.2s CPU/jour                   |
| Détection de drift temporel ou dégradation lente      |                                  |
| Alimente les options B, C, D avec plus de données     |                                  |

**Effort** : zéro — le timer tourne déjà.

**Déclencheur de sortie** : 7-14 runs accumulés sans anomalie → passer à C ou D.

---

### B — Multi-signal paper-mode BTC/ETH/SOL

| Avantages                                             | Risques / Coûts                  |
| ----------------------------------------------------- | -------------------------------- |
| Test de montée en charge multi-ticker                 | Changement de code (nouveau GO)  |
| Plus représentatif d'un vrai pipeline prod            | Complexité journal multi-run/day |
| Valide la gestion de run_ids simultanés               | Scope élargi                     |

**Effort** : moyen — nouveau GO d'implémentation requis.

**Prérequis** : observation A recommandée en premier (données mono-signal stables).

---

### C — Dashboard métriques LocalCMS

| Avantages                                             | Risques / Coûts                  |
| ----------------------------------------------------- | -------------------------------- |
| Visibilité agrégée sur P&L, win-rate, durée           | Implémentation LocalCMS (Go)     |
| Décision basée sur données, pas sur logs bruts        | Nouveau endpoint + template       |
| Peut être lancé en parallèle de A                     |                                  |

**Effort** : moyen — endpoint `/metrics` + lecture JSON + rendu HTML.

**Peut être initié en parallèle de A.**

---

### D — Préparation live trading (doc-only)

| Avantages                                             | Risques / Coûts                  |
| ----------------------------------------------------- | -------------------------------- |
| Vision claire du chemin paper → live                  | Aucun (doc-only)                 |
| Planification des garde-fous (API keys, risk, audit)  |                                  |
| Décision de passage live repoussée à un GO séparé     |                                  |

**Effort** : faible — documentation pure, aucune activation.

**Peut être initié en parallèle de A ou après C.**

---

## Recommandation

```
A + C en parallèle → puis D
```

1. **A (observation continue)** : aucun changement, le timer tourne. Laisser
   s'accumuler 7-14 runs quotidiens. Zéro risque, zéro effort.

2. **C (dashboard métriques)** : lancer en parallèle. Ajoute de la valeur
   immédiate sur les données existantes sans modifier le pipeline.

3. **D (préparation live — doc-only)** : initier après C, une fois la
   visibilité métriques établie. Documenter les critères et garde-fous
   avant toute décision de passage live.

4. **B (multi-signal)** : reporter jusqu'à stabilisation de A + C.
   La complexité multi-ticker mérite une baseline mono-signal plus longue.

## Invariants à conserver quelle que soit l'option choisie

- No live trade / No Bitget order
- No automatic Sheets write
- Controlled-write manuel uniquement
- LocalCMS read-only
- Rollback systemd disponible :
  `sudo systemctl disable --now daily-session.timer daily-session.service`
- Aucun secret dans le repo ou les logs

## RISKS

- À qualifier.
