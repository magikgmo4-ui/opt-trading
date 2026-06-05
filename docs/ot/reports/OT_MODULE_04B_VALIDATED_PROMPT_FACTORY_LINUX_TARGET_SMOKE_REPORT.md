# OT-MODULE-04B — VALIDATED_PROMPT_FACTORY (LINUX TARGET SMOKE) — REPORT

Date (America/Montreal) : 2026-03-14

## 1. RÉSUMÉ EXÉCUTIF
- Smoke exécuté sur une vraie cible Linux (`admin-trading`) et prouvé par commandes + sorties.
- Wrappers testés : `cmd.sh` (list-modes + 2 générations) et `sanity.sh`.
- `menu.sh` non testé : interactif (non propre en non-interactif SSH).
- Réserve de OT-MODULE-04 levée.

## 2. ENVIRONNEMENT LINUX RÉEL
### Machine / user / shell / repo
- Hostname : `admin-trading`
- User : `ghost`
- Shell : `/bin/bash`
- Repo path : `/opt/trading`
- Module path : `/opt/trading/modules/validated_prompt_factory`

### Runtime observé
- Bash : `GNU bash, version 5.2.15(1)-release (x86_64-pc-linux-gnu)`
- Python : `Python 3.11.2` (`/usr/bin/python3`)
- Git : `git version 2.39.5`
- Repo HEAD : `f774757`

## 3. COMMANDES EXÉCUTÉES (EXACTES)
Toutes les commandes ont été exécutées depuis le poste Windows via SSH (alias SSH : `admin-trading`).

### 3.1 Identification environnement
```bash
ssh -o BatchMode=yes -o ConnectTimeout=5 admin-trading 'echo HOST=$(hostname); echo USER=$(whoami); echo SHELL=$SHELL; echo PWD=$(pwd); command -v bash; bash --version | head -n 1; command -v python3 || true; python3 --version 2>/dev/null || true; command -v python || true; python --version 2>/dev/null || true; command -v git; git --version; cd /opt/trading && git rev-parse --short HEAD'
```

### 3.2 cmd.sh list-modes
```bash
ssh -o BatchMode=yes -o ConnectTimeout=5 admin-trading 'cd /opt/trading/modules/validated_prompt_factory && ./cmd.sh list-modes'
```

### 3.3 cmd.sh generate trae_patch (input standard)
```bash
ssh -o BatchMode=yes -o ConnectTimeout=5 admin-trading 'cd /opt/trading/modules/validated_prompt_factory && ./cmd.sh generate trae_patch inputs/synthesis_registry_central.txt'
```

### 3.4 cmd.sh generate bundle_transfer (input standard)
```bash
ssh -o BatchMode=yes -o ConnectTimeout=5 admin-trading 'cd /opt/trading/modules/validated_prompt_factory && ./cmd.sh generate bundle_transfer inputs/synthesis_bundle_transfer.txt'
```

### 3.5 sanity.sh
```bash
ssh -o BatchMode=yes -o ConnectTimeout=5 admin-trading 'cd /opt/trading/modules/validated_prompt_factory && ./sanity.sh'
```

### 3.6 Échec propre (input standard)
```bash
ssh -o BatchMode=yes -o ConnectTimeout=5 admin-trading 'cd /opt/trading/modules/validated_prompt_factory && ./cmd.sh generate trae_patch inputs/synthesis_failure_missing_section.txt; echo EXIT_CODE=$?'
```

## 4. RÉSULTATS OBSERVÉS (EXTRAITS)
### 4.1 list-modes
- `Available modes:` + 4 modes listés.

### 4.2 trae_patch
- `Success: Generated /opt/trading/modules/validated_prompt_factory/output/prompt_trae_patch.txt`

### 4.3 bundle_transfer
- `Success: Generated /opt/trading/modules/validated_prompt_factory/output/prompt_bundle_transfer.txt`

### 4.4 sanity.sh
- `Checking Help... OK`
- `Checking Generation (chatgpt_session)... OK`
- `Checking Failure (missing section)... OK`
- `Sanity Check Passed.`

### 4.5 échec propre
- `Error: Missing sections in synthesis: POINT DE REPRISE`
- `EXIT_CODE=2`

## 5. ÉCARTS PROUVÉS ET CORRECTIONS APPLIQUÉES
### ÉCARTS
- Inputs standard manquants sur la cible Linux (seul `synthesis_example.txt` présent).
- Une exécution `./sanity.sh` a échoué après transfert (CRLF → `/usr/bin/env: « bash\r »`).

### CORRECTIONS (MINIMALES, BLOQUANTES POUR LE SMOKE)
- Inputs standard copiés à l’identique dans `inputs/` (pas de contenu inventé).
- Normalisation LF des scripts `.sh` côté repo (évite le `bash\r`).

## 6. VERDICT
**PASS (réserve levée)** pour le smoke wrappers sur Linux réel (cmd + sanity).

## 7. POINT DE REPRISE EXACT
> **GO_OT_MODULE_05_VALIDATED_PROMPT_FACTORY_GLOBAL_WRAPPERS_VALIDATE**


## RISKS

- À qualifier.
