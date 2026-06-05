# OT-MODULE-02 — VALIDATED_PROMPT_FACTORY (HARDENING) — REPORT

Date (America/Montreal) : 2026-03-14

## 1. RÉSUMÉ EXÉCUTIF
- Objectif tenu : durcissement minimal du module `validated_prompt_factory` après usage réel, sans refactor large ni changement de mission.
- Durcissements appliqués uniquement sur écarts prouvés : validation d’entrée désormais bloquante, parsing d’en-têtes Markdown, contrôle du répertoire de sortie, test d’échec ajouté à `sanity.sh`, README aligné.
- Preuves produites : 2 cas réels rejoués + 1 cas d’échec propre.

## 2. CORPUS RELU (PRIORITAIRE)
- `docs/master_pack/mission_starter_pack/00_mission_start_guide.md`
- `docs/master_pack/00_current_state_and_standards.md`
- `workflow_ai/WORKFLOW.md`
- `workflow_ai/templates/specs.md`
- `workflow_ai/templates/tasks.md`
- `registry/modules_registry.yaml`
- `registry/wrappers_registry.yaml`
- `modules/validated_prompt_factory/README.md`
- `modules/validated_prompt_factory/app/validated_prompt_factory.py`
- `modules/validated_prompt_factory/cmd.sh`
- `modules/validated_prompt_factory/menu.sh`
- `modules/validated_prompt_factory/sanity.sh`
- Livrables module_01 :
  - `OT_MODULE_01_VALIDATED_PROMPT_FACTORY_REAL_USE_REPORT.md`
  - `OT_MODULE_01_VALIDATED_PROMPT_FACTORY_REAL_USE_GAP_REPORT.md`
  - `OT_MODULE_01_VALIDATED_PROMPT_FACTORY_REAL_USE_CLOSING.txt`

## 3. ÉTAT RÉEL (ÉTABLI)
- Module présent : `modules/validated_prompt_factory/`
- Déclaré dans les registries :
  - [modules_registry.yaml](file:///c:/Users/ghost/opt-trading/registry/modules_registry.yaml#L5-L14)
  - [wrappers_registry.yaml](file:///c:/Users/ghost/opt-trading/registry/wrappers_registry.yaml#L5-L30)
- Modes : `chatgpt_session`, `trae_module`, `trae_patch`, `bundle_transfer`

## 4. ÉCARTS PROUVÉS (CLASSÉS) ET CORRECTIONS

### GAP-01 — Validation d’entrée non bloquante (CRITIQUE)
- Constat : une synthèse incomplète produisait un prompt avec champs “Non spécifié” (risque d’usage réel).
- Correction : la génération échoue désormais si une section requise manque (message explicite + code de sortie non nul).
- Preuve : cas d’échec `inputs/synthesis_failure_missing_section.txt` (sans `POINT DE REPRISE`) rejoué.

### GAP-02 — En-têtes Markdown non reconnus (UTILE)
- Constat : une synthèse structurée en `## CONTEXTE` / `## OBJECTIF` n’était pas détectée.
- Correction : parsing tolère les préfixes Markdown (`#`, `##`, etc.).
- Preuve : le cas d’échec utilise des en-têtes `## ...` et est correctement interprété (manque détecté sur `POINT DE REPRISE`).

### GAP-03 — Répertoire de sortie non robuste (UTILE)
- Constat : si `--output-dir` pointe vers un fichier existant, comportement ambigu.
- Correction : erreur explicite si le chemin existe et n’est pas un répertoire.

### NON RETENU
- Ajouter des options CLI supplémentaires (`--strict/--lenient`) : non nécessaire pour le durcissement minimal.
- Intégration `ops_menu_hub` / refactor structure module : hors périmètre hardening.

## 5. REJEU CAS RÉELS (PREUVES)

### 5.1 Cas réel 1 — Registry central (mode `trae_patch`)
- Entrée : `modules/validated_prompt_factory/inputs/synthesis_registry_central.txt`
- Commande :
```bash
python modules/validated_prompt_factory/app/validated_prompt_factory.py ^
  --input modules/validated_prompt_factory/inputs/synthesis_registry_central.txt ^
  --mode trae_patch ^
  --output-dir state/vpf_hardening_2026-03-14
```
- Sortie : `state/vpf_hardening_2026-03-14/prompt_trae_patch.txt`

### 5.2 Cas réel 2 — Bundle transfer (mode `bundle_transfer`)
- Entrée : `modules/validated_prompt_factory/inputs/synthesis_bundle_transfer.txt`
- Commande :
```bash
python modules/validated_prompt_factory/app/validated_prompt_factory.py ^
  --input modules/validated_prompt_factory/inputs/synthesis_bundle_transfer.txt ^
  --mode bundle_transfer ^
  --output-dir state/vpf_hardening_2026-03-14
```
- Sortie : `state/vpf_hardening_2026-03-14/prompt_bundle_transfer.txt`

## 6. TEST D’ÉCHEC PROPRE (PREUVE)
- Entrée : `modules/validated_prompt_factory/inputs/synthesis_failure_missing_section.txt`
- Commande :
```bash
python modules/validated_prompt_factory/app/validated_prompt_factory.py ^
  --input modules/validated_prompt_factory/inputs/synthesis_failure_missing_section.txt ^
  --mode trae_patch ^
  --output-dir state/vpf_hardening_2026-03-14
```
- Résultat attendu : échec avec message “Missing sections … POINT DE REPRISE”.

## 7. UX MINIMALE (CMD/MENU/SANITY)
### ÉTABLI
- Cohérence logique : `cmd.sh` appelle le script Python et propage l’échec en cas de synthèse invalide.
- `menu.sh` appelle les modes via `cmd.sh` (input par défaut = `synthesis_example.txt`, conforme).
- `sanity.sh` inclut désormais un test positif + un test négatif.

### À CONFIRMER (HORS PREUVE WINDOWS)
- Exécution réelle des wrappers bash (`cmd.sh` / `sanity.sh`) sur Linux cible (WSL non installé sur ce poste).

## 8. DOC + CONTINUITÉ
- README aligné sur le comportement réel (validation d’entrée bloquante, en-têtes Markdown, exécution Python Windows).
- Kanban mis à jour : `opt_trading_kanban_source_of_truth_2026-03-13_updated.md`.

## 9. FICHIERS MODIFIÉS
- `modules/validated_prompt_factory/app/validated_prompt_factory.py`
- `modules/validated_prompt_factory/sanity.sh`
- `modules/validated_prompt_factory/README.md`
- `modules/validated_prompt_factory/inputs/synthesis_failure_missing_section.txt`
- `opt_trading_kanban_source_of_truth_2026-03-13_updated.md`

## 10. VERDICT FINAL
**PASS** : module durci sans dérive, preuves fournies, continuité compatible.

## 11. POINT DE REPRISE EXACT
> **GO_OT_MODULE_03_VALIDATED_PROMPT_FACTORY_ADOPTION**


## RISKS

- À qualifier.
