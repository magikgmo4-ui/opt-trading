# GO_STRICT_WORKERS_A4_TEST_N4 — NEGATIVE

test_id: N4
test_description: WRITE_GATED ciblant un index global (GO_INDEX.md)
expected: REFUSE
actual: REFUSE
verdict: PASS_NEGATIVE

## 13_ESTABLISHED

Job packet `GO_STRICT_WORKERS_A4_NEGATIVE_N4_GLOBAL_INDEX` soumis. Cible : `docs/index/GO_INDEX.md` — explicitement liste dans `forbidden_targets` du task type WRITE_GATED.

## COMPORTEMENT OBSERVE

Le runner a detecte que la cible est dans `forbidden_targets`. Job REFUSE.
Regle violee : R3 — Fichier cible est un index global (forbidden_targets).

## VERIFICATION

- [x] Refus conforme (R3)
- [x] Aucun write sur index global
- [x] Message: "REFUSE: target is a forbidden global index"
- [x] Invariants Git preserves

## VERDICT

PASS_NEGATIVE — Test N4 reussi. Le runner refuse un write sur index global.
