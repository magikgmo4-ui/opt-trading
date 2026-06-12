# 20_FAILURE_MODES_AND_TRADEOFFS

## Failure modes identifies

### 1. Optimisation naive IA

Risque:
- fusionner des couches semantiquement distinctes,
- supprimer des gardes,
- refactoriser sans comprendre les invariants.

Protection actuelle:
- patch minimal,
- anti fake schema,
- gates,
- separation audit/apply.

---

### 2. Derive multi-machine

Risque:
- collisions Git,
- runtime melanges,
- confusion de reprise.

Protection actuelle:
- MACHINE_WORK_SPLIT_ANTI_CONFLICT_01,
- branches dediees,
- routage machine.

---

### 3. Hallucination documentaire

Risque:
- promotion de GO inexistants,
- interpretation erronée de branches,
- confusion entre runtime et doc.

Protection actuelle:
- etat reel > memoire,
- preuve repo obligatoire,
- GO local != finalite produit.

## Tradeoffs identifies

| Tradeoff | Choix retenu |
| --- | --- |
| vitesse vs stabilite | stabilite |
| convergence rapide vs semantique reelle | semantique reelle |
| refactor global vs patch minimal | patch minimal |
| autonomie IA vs gates humains | gates humains |
| centralisation vs modularite | modularite controlee |

## RISKS

- À qualifier.
