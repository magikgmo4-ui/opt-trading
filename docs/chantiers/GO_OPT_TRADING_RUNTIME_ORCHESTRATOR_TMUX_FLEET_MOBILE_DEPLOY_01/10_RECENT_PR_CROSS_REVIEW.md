# 10 — RECENT_PR_CROSS_REVIEW

## PR #614 — External apps orchestration runner (squelette)

**Merge:** 3750e5cb — branche `go/GO_OPT_TRADING_STRICT_WORKERS_CHILD_EXTERNAL_APPS_ORCHESTRATION_RUNNER_01`

Ajoute:
- `docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_EXTERNAL_APPS_ORCHESTRATION_RUNNER_01/`
- `scripts/ai/workers/orchestration/README.md`
- `scripts/ai/workers/orchestration/external_apps_orchestration_contract.json`
- `scripts/ai/workers/orchestration/sample_request.readonly.json`
- `scripts/ai/workers/orchestration/sample_response.pass.json`

**Décision:** Squelette non-exécutant. Ce GO ne le modifie pas, ne le double pas.

## PR #613 — Runner contract impact

Non tracée dans le log récent. Présumée absorbée par PR #614.

## PR #609 — Merge main

`ea3d447d` — Merge de la branche main. Pas d'impact direct.

## PR #608 — Controlled execution 8 job packets

`1b522fe0` — Promotion de 8 job packets. Pas d'impact direct.

## PR #607 — DeskPro watchdog impact

`3a382e0f` — Watchdog déjà intégré dans `scripts/deskpro_watchdog.sh` (190 lignes). Ce GO le consume, ne le modifie pas.

## PR #605 — Fleet warn classification

`bbcf364c` — Classification des WARN fleet. Impact direct : `fleet_orchestrator.py` gère déjà `EXPECTED` vs unknown. Ce GO valide que `WARN` n'est accepté que si classifié `EXPECTED`.

## PR #604/#600/#595 — cursor-ai Windows attach

- `a6c92e65` (PR #604) — Closeout cursor-ai PASS/reachable/ssh_windows
- `3e7e654e` (PR #600) — -EncodedCommand pour SSH PowerShell
- `00fd7ef9` (PR #595) — hostname_aliases resolve

**Impact:** cursor-ai reachable via ssh_windows, pas tmux Linux forcé. Confirmé.

## PR #607 — DeskPro watchdog

`3a382e0f` — `scripts/deskpro_watchdog.sh` avec classification infra vs business (filtre webhook_activity:fail). Ce GO utilise watchdog comme test de niveau 6.

## Synthèse

| PR | Impact sur ce GO | Action |
|---|---|---|
| #614 | Élevé — ne pas recréer le squelette | Consommer seulement |
| #613 | Faible — présumé absorbé | Surveillance |
| #605 | Moyen — classification WARN | Valider EXPECTED |
| #604/#600/#595 | Faible — cursor-ai Windows | Pas tmux Linux |
| #607 | Faible — watchdog existant | Utiliser en test |
