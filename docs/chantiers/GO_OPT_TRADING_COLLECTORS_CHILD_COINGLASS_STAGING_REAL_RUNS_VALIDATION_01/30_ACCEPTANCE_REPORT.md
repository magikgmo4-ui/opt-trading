---
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_STAGING_REAL_RUNS_VALIDATION_01
doc_type: acceptance_report
repo: opt-trading
status: open
created_at: 2026-05-23
---

# 30_ACCEPTANCE_REPORT

À remplir après `--validate --required 3` exit 0.

---

## VERDICT

```text
PASS_STAGING_REAL / FAIL_STAGING_REAL

Date : ~
Opérateur : ~
```

---

## CRITÈRES_PASS

| Critère | Résultat | Détail |
|---|---|---|
| 3 runs capturés | ~ | timestamps : ~, ~, ~ |
| ≥ 1 detection/run (conf ≥ 0.60) | ~ | |
| extracted_value non-null sur ≥ 1 detection/run | ~ | |
| latest.json présent et valide | ~ | |
| events.jsonl contient 3 entrées qualifiées | ~ | |
| --validate --required 3 exit 0 | ~ | |
| /desk/vision ok=true | ~ | |
| /desk/ui panel "Coinglass Vision" visible | ~ | |

---

## OBSERVATIONS

```text
[à remplir — qualité des captures, comportement OpenAI Vision,
 latence, coût estimé, anomalies éventuelles]
```

---

## PROCHAINE_ÉTAPE

```text
Si PASS_STAGING_REAL :
→ La stack est prête pour une évaluation de promotion prod.
→ Ouvrir un GO dédié si activation planifiée (hors scope de ce GO).

Si FAIL_STAGING_REAL :
→ Documenter la cause dans 90_REPRISE_POINT.md.
→ Corriger avant de relancer.
```
