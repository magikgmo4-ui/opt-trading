# GO_STRICT_WORKERS_A4_TEST_N1 — NEGATIVE

test_id: N1
test_description: WRITE_GATED sans explicit_write_approval
expected: REFUSE
actual: REFUSE
verdict: PASS_NEGATIVE

## 13_ESTABLISHED

Job packet `GO_STRICT_WORKERS_A4_NEGATIVE_N1_NO_APPROVAL` soumis au runner. Le packet est de type WRITE_GATED mais ne contient pas le champ obligatoire `explicit_write_approval`.

## COMPORTEMENT OBSERVE

Le runner a detecte l'absence de `explicit_write_approval` et a REFUSE le job.
Regle violee : R1 — `explicit_write_approval` absent.

## VERIFICATION

- [x] Refus conforme (R1)
- [x] Aucun write effectue
- [x] Message d'erreur explicite : "REFUSE: explicit_write_approval missing for WRITE_GATED job"
- [x] Runner lock intact

## VERDICT

PASS_NEGATIVE — Test N1 reussi. Le runner refuse correctement un job WRITE_GATED sans approval.
