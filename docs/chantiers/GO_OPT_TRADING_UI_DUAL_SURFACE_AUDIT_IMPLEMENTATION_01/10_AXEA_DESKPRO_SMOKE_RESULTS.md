---
go_id: GO_OPT_TRADING_UI_DUAL_SURFACE_AUDIT_IMPLEMENTATION_01
doc_type: axe_a_results
repo: opt-trading
status: PASS
created_at: 2026-05-18
surface: desk_pro — smoke / dry-run validation
runtime_mutation: false
---

# 10_AXEA_DESKPRO_SMOKE_RESULTS

---

## Verdict

```text
AXE A — DESK PRO SMOKE — PASS
```

---

## Contexte d'exécution

| Champ | Valeur |
| --- | --- |
| Date | 2026-05-18 |
| Branch | `sot/mainline` |
| Python | `/home/ghost/miniforge3/bin/python3` |
| pytest | non installé — tests exécutés via `python3 -c` |
| Fixtures | `tests/fixtures/admin_trading_contract_smoke/` |

---

## Résultats sanity

```
bash modules/desk_pro/scripts/sanity_check.sh
→ PASS: wrapper sanity OK
  name=desk_pro
  path=/opt/trading/modules/desk_pro
  scripts/ présent
  menu.sh exécutable
  cmd.sh exécutable
```

---

## Résultats dry-run (3 cas)

| Cas | Input | Résultat attendu | Obtenu | Verdict |
| --- | --- | --- | --- | --- |
| v0_minimal via adapter | `signal_event_v0_minimal.json` + `desk_snapshot_minimal.json` | `event_type=signal_event`, `status=WARN` | conforme | PASS |
| v1 already normalized | `signal_event_v0_complete.json` → v1 + snapshot | `direction=BUY`, `status=WARN` | conforme | PASS |
| visual_context v1 | v0_minimal + `visual_context_v1_minimal.json` + snapshot | `capture_id` matched | conforme | PASS |

---

## Note technique — pytest vs unittest

```text
Les tests dans tests/test_desk_pro_dry_run.py utilisent le style pytest
(classe sans héritage unittest.TestCase, plain assert).
python3 -m unittest → NO TESTS RAN (comportement normal).
pytest non installé dans l'environnement.
Solution : exécution directe via python3 -c avec sys.path.insert(0, '/opt/trading').
```

---

## Gaps confirmés post-smoke

| Gap | Priorité | Action |
| --- | --- | --- |
| pytest non installé | moyenne | `pip install pytest` dans venv si besoin campagne complète |
| Port `perf_app.py` non documenté | moyenne | grep `uvicorn.run` ou TMUX session |
| `test_desk_pro_combined_input_smoke.py` non rejoué | basse | à exécuter si pytest disponible |
| `test_desk_pro_artifact_output.py` non rejoué | basse | idem |

---

## 17_RESUME_POINT

```text
Axe A PASS — Desk Pro dry-run opérationnel.
Axe B (localcms consumer) : post-seuil Phase 1 ≥2026-05-30.
Prochaine action Desk Pro : confirmer port perf_app.py + lancer combined_input_smoke.
```
