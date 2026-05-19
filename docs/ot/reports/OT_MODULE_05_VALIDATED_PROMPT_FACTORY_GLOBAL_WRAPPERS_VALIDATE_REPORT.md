# OT-MODULE-05 — VALIDATED_PROMPT_FACTORY (GLOBAL WRAPPERS VALIDATE) — REPORT

Date (America/Montreal) : 2026-03-14

## 1. RÉSUMÉ EXÉCUTIF
- Les wrappers globaux attendus pour `validated_prompt_factory` sont identifiés sans supposition (registry + script de déploiement).
- Sur Linux réel (`admin-trading`), les wrappers globaux existent, résolvent correctement vers le module, et passent les commandes nominales (list-modes + 2 générations + sanity).
- `menu-validated_prompt_factory` non rejoué : interactif, non testable proprement en non-interactif SSH.

## 2. ENVIRONNEMENT RÉEL
- Hostname : `admin-trading`
- User : `ghost`
- Shell : `/bin/bash`
- Repo : `/opt/trading`

## 3. WRAPPERS GLOBAUX ATTENDUS (PREUVES REPO)
Source de vérité :
- Registry : `registry/wrappers_registry.yaml`
- Déploiement : `scripts/deploy_wrappers_ot_wrap_01.sh`

Wrappers attendus pour ce module :
- `cmd-validated_prompt_factory` → `/usr/local/bin/cmd-validated_prompt_factory` → `/opt/trading/modules/validated_prompt_factory/cmd.sh`
- `sanity-validated_prompt_factory` → `/usr/local/bin/sanity-validated_prompt_factory` → `/opt/trading/modules/validated_prompt_factory/sanity.sh`
- `menu-validated_prompt_factory` → `/usr/local/bin/menu-validated_prompt_factory` → `/opt/trading/modules/validated_prompt_factory/menu.sh`

## 4. COMMANDES EXÉCUTÉES (EXACTES)
### 4.1 Résolution des wrappers
```bash
ssh -o BatchMode=yes -o ConnectTimeout=5 admin-trading 'for w in cmd-validated_prompt_factory sanity-validated_prompt_factory menu-validated_prompt_factory; do echo "== $w =="; command -v $w || echo MISSING; ls -l $(command -v $w) 2>/dev/null || true; readlink -f $(command -v $w) 2>/dev/null || true; done'
```

### 4.2 cmd global — list-modes
```bash
ssh -o BatchMode=yes -o ConnectTimeout=5 admin-trading 'cd /opt/trading && cmd-validated_prompt_factory list-modes'
```

### 4.3 cmd global — génération trae_patch
```bash
ssh -o BatchMode=yes -o ConnectTimeout=5 admin-trading 'cd /opt/trading && cmd-validated_prompt_factory generate trae_patch modules/validated_prompt_factory/inputs/synthesis_registry_central.txt'
```

### 4.4 cmd global — génération bundle_transfer
```bash
ssh -o BatchMode=yes -o ConnectTimeout=5 admin-trading 'cd /opt/trading && cmd-validated_prompt_factory generate bundle_transfer modules/validated_prompt_factory/inputs/synthesis_bundle_transfer.txt'
```

### 4.5 sanity global
```bash
ssh -o BatchMode=yes -o ConnectTimeout=5 admin-trading 'cd /opt/trading && sanity-validated_prompt_factory'
```

### 4.6 Échec propre (validation)
```bash
ssh -o BatchMode=yes -o ConnectTimeout=5 admin-trading 'cd /opt/trading && cmd-validated_prompt_factory generate trae_patch modules/validated_prompt_factory/inputs/synthesis_failure_missing_section.txt; echo EXIT_CODE=$?'
```

## 5. RÉSULTATS OBSERVÉS (EXTRAITS)
- Les trois wrappers globaux existent sous `/usr/local/bin` et sont des symlinks vers `/opt/trading/modules/validated_prompt_factory/*`.
- `cmd-validated_prompt_factory list-modes` : 4 modes listés.
- `cmd-validated_prompt_factory generate trae_patch ...` : `Success: Generated /opt/trading/modules/validated_prompt_factory/output/prompt_trae_patch.txt`
- `cmd-validated_prompt_factory generate bundle_transfer ...` : `Success: Generated /opt/trading/modules/validated_prompt_factory/output/prompt_bundle_transfer.txt`
- `sanity-validated_prompt_factory` : `Sanity Check Passed.`
- Échec propre : message “Missing sections … POINT DE REPRISE” + `EXIT_CODE=2`.

## 6. VERDICT
**CLOSE (PASS)** : wrappers globaux prouvés sur Linux réel.

## 7. POINT DE REPRISE EXACT
> **GO_OT_MODULE_06_VALIDATED_PROMPT_FACTORY_OPERATOR_RUNBOOK**

