# GO_STRICT_WORKERS_A4_TEST_N3 — NEGATIVE

test_id: N3
test_description: WRITE_GATED avec input contenant un motif secret-like
expected: REFUSE
actual: REFUSE
verdict: PASS_NEGATIVE

## 13_ESTABLISHED

Job packet `GO_STRICT_WORKERS_A4_NEGATIVE_N3_SECRET_INPUT` soumis. Le champ `allowed_inputs` contient `**/.env.secret.backup` qui matche les motifs denies `.env` et `secret` dans `denied_inputs`.

## COMPORTEMENT OBSERVE

Le runner a detecte que l'input contient des motifs interdits (.env, secret). Job REFUSE.
Regle violee : R4 — Input contient un motif de secret.

## VERIFICATION

- [x] Refus conforme (R4)
- [x] Aucun write effectue
- [x] Aucun acces au fichier sensible
- [x] Garde-fous Phase A/B actifs

## VERDICT

PASS_NEGATIVE — Test N3 reussi. Le runner refuse un job avec input secret-like.
