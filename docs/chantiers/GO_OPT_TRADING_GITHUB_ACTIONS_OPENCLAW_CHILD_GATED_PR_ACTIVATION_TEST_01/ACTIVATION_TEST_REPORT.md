---
doc_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_ACTIVATION_TEST_01_REPORT
doc_type: activation_test_report
go_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_ACTIVATION_TEST_01
created_at: 2026-05-25
---

# Activation Test Report — gated-pr.yml

## 1. workflow_dispatch

```bash
gh workflow run gated-pr.yml --ref sot/mainline -f reason=manual
```

**Résultat :** ✅ Dispatch réussi — plus de HTTP 422
**Run ID :** 26412206983

## 2. Exécution workflow_dispatch

**Résultat :** ✅ Run exécutée (pas de 0s / "workflow file issue")
**Conclusion :** `failure` — attendu car `gate/preflight` n'a pas de contexte PR (pas de diff)

## 3. Micro-PR checks

**PR #788** — `go/GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_ACTIVATION_TEST_01` → `sot/mainline`

| Check | Status | Durée |
|---|---|---|
| gate/preflight | ✅ PASS | 7s |
| gate/file-scope | ✅ PASS | 8s |
| gate/no-lock-overlap | ✅ PASS | 6s |
| gate/tests | ✅ PASS | 6s |

## 4. Critères PASS

| Critère | Résultat |
|---|---|
| `workflow_dispatch` reconnu (plus de HTTP 422) | ✅ |
| Run manuel ne finit plus en 0s "workflow file issue" | ✅ |
| PR vers `sot/mainline` déclenche les checks `gate/*` | ✅ |
| `gate/preflight` → PASS | ✅ |
| `gate/file-scope` → PASS | ✅ |
| `gate/no-lock-overlap` → PASS | ✅ |
| `gate/tests` → PASS | ✅ |

## 5. Conclusion

**Le workflow `gated-pr.yml` est pleinement actif et fonctionnel.**

- Le YAML est valide et parsé correctement par GitHub Actions.
- `workflow_dispatch` manuel fonctionne (run exécutée, échec contenu attendu sans PR).
- Les PR vers `sot/mainline` déclenchent les 4 jobs `gate/*`.
- Les 4 jobs passent pour une PR docs-only conforme FILE_SCOPE.

Prochaine étape : `GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_REQUIRED_CHECKS_01`
(promouvoir les checks `gate/*` en required checks dans les règles de protection de branche).
