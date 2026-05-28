# 20_RUNTIME_FLOW

## Flux d'exécution

```
Opérateur
  │
  ├─ écrit GO_PROMPT (fichier texte ou JSON)
  │
  └─→ scripts/automation_ops/run_semiauto_pilot.sh <prompt_path>
         │
         └─→ python3 -m modules.automation_ops.semiauto_pilot.pilot_runner <prompt_path>
                │
                ├─ build_empty() → contrat partiel (run_id, go_id, parent_go_id, mode=dry_run)
                │
                ├─ _populate_from_prompt()
                │    ├─ vérifier existence fichier
                │    ├─ parser JSON overrides (optionnel)
                │    └─ peupler actions_planned / actions_executed / stop_conditions
                │
                ├─ stop_conditions.check()
                │    ├─ PASS → continuer
                │    └─ TRIGGERED → verdict=STOP_CONDITION_TRIGGERED, exit 2
                │
                ├─ contract["verdict"] = "PASS_DRY_RUN"
                │
                └─ proof_writer.write()
                     ├─ artifacts/automation_ops/semiauto_pilot/<run_id>/proof.json
                     └─ artifacts/automation_ops/semiauto_pilot/<run_id>/proof_summary.md
                          │
                          └─→ exit 0 (PASS_DRY_RUN)
```

## Invocation manuelle

```bash
# depuis la racine du repo
echo "run pilot" > /tmp/my_go_prompt.txt
bash scripts/automation_ops/run_semiauto_pilot.sh /tmp/my_go_prompt.txt
```

## Invocation avec stop condition JSON

```bash
cat > /tmp/stop_test.json <<'EOF'
{
  "stop_conditions": [{"name": "manual_block", "triggered": true}]
}
EOF
bash scripts/automation_ops/run_semiauto_pilot.sh /tmp/stop_test.json
# exit code = 2 (STOP_CONDITION_TRIGGERED)
```
