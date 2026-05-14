# GO_STRICT_WORKERS_A4_TEST_N5 — NEGATIVE

test_id: N5
test_description: PATCH_DRAFT tentant un write direct sans passer par WRITE_GATED
expected: REFUSE
actual: REFUSE
verdict: PASS_NEGATIVE

## 13_ESTABLISHED

Job packet `GO_STRICT_WORKERS_A4_NEGATIVE_N5_PATCH_DRAFT_WRITE` soumis. Le task type est PATCH_DRAFT (A2, draft-only) mais le packet tente d'ecrire directement sur `BRANCH_STATE.md`. PATCH_DRAFT n'a pas le droit de write — c'est le role de WRITE_GATED (A4).

## COMPORTEMENT OBSERVE

Le runner a detecte que le task type PATCH_DRAFT (A2) n'est pas WRITE_GATED (A4) et que le packet demande un write. Job REFUSE.
Regle violee : Promotion A2→A4 non automatique. PATCH_DRAFT reste draft-only.

## VERIFICATION

- [x] Refus conforme
- [x] A2 ne peut pas faire de write
- [x] Seul A4 (WRITE_GATED) peut ecrire avec approval
- [x] Garde-fous Phase A/B actifs

## VERDICT

PASS_NEGATIVE — Test N5 reussi. PATCH_DRAFT ne peut pas ecrire ; la promotion A2→A4 necessite un job WRITE_GATED explicite.
