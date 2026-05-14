# GO_STRICT_WORKERS_A4_TEST_N2 — NEGATIVE

test_id: N2
test_description: WRITE_GATED vers un fichier hors write_allowlist
expected: REFUSE
actual: REFUSE
verdict: PASS_NEGATIVE

## 13_ESTABLISHED

Job packet `GO_STRICT_WORKERS_A4_NEGATIVE_N2_OUTSIDE_ALLOWLIST` soumis. Cible : `modules/desk_pro/config.py` — hors write_allowlist (`modules/` n'est pas dans la liste des chemins autorises). Approval presente mais scope invalide.

## COMPORTEMENT OBSERVE

Le runner a detecte que `modules/desk_pro/config.py` n'est pas dans la `write_allowlist` definie dans tasks.index.json. Job REFUSE.
Regle violee : R2 — Fichier cible hors `write_allowlist`.

## VERIFICATION

- [x] Refus conforme (R2)
- [x] Aucun write effectue
- [x] Message: "REFUSE: target outside write_allowlist"
- [x] Garde-fous actifs

## VERDICT

PASS_NEGATIVE — Test N2 reussi. Le runner refuse un write hors allowlist.
