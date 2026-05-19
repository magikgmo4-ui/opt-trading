# OT-MODULE-01 — VALIDATED_PROMPT_FACTORY (REAL USE) — REPORT

Date (America/Montreal) : 2026-03-14

## 1. RÉSUMÉ EXÉCUTIF
- Le module `validated_prompt_factory` est présent, déclaré dans les registries, et exécutable via Python sur l’état réel du repo.
- Deux cas réels ont été rejoués et des prompts exploitables ont été générés : (1) registry central (mode `trae_patch`), (2) bundle_transfer (mode `bundle_transfer`).
- Un écart prouvé a été détecté sur le mode `bundle_transfer` (continuité absente : contraintes/risques/suite/point de reprise non rendus) et corrigé par patch minimal dans le template.

## 2. ÉTAT RÉEL CONSTATÉ
### 2.1 Présence / structure module
- Module : `modules/validated_prompt_factory/`
- Code : `modules/validated_prompt_factory/app/validated_prompt_factory.py`
- Entrypoints présents : `cmd.sh`, `menu.sh`, `sanity.sh`
- Modes supportés (code) : `chatgpt_session`, `trae_module`, `trae_patch`, `bundle_transfer`

### 2.2 Registry central (preuve repo)
- Module déclaré : [modules_registry.yaml](file:///c:/Users/ghost/opt-trading/registry/modules_registry.yaml#L5-L14)
- Wrappers déclarés : [wrappers_registry.yaml](file:///c:/Users/ghost/opt-trading/registry/wrappers_registry.yaml#L5-L30)

## 3. CAS TEST 1 — REGISTRY CENTRAL (MODE TRAE_PATCH)
### 3.1 Entrée (synthèse)
- Fichier : `modules/validated_prompt_factory/inputs/synthesis_registry_central.txt`
- Intent : produire un prompt de patch strict (pas de nouveau module) pour aligner `registry/modules_registry.yaml` + `registry/wrappers_registry.yaml`.

### 3.2 Commande rejouée (preuve)
```bash
python modules/validated_prompt_factory/app/validated_prompt_factory.py ^
  --input modules/validated_prompt_factory/inputs/synthesis_registry_central.txt ^
  --mode trae_patch ^
  --output-dir state/vpf_real_use_2026-03-14
```
Sortie observée :
- `Success: Generated state/vpf_real_use_2026-03-14\prompt_trae_patch.txt`

### 3.3 Sortie produite (preuve)
- Fichier : `state/vpf_real_use_2026-03-14/prompt_trae_patch.txt`
- Vérification métier :
  - Le prompt impose “MODE PATCH” + interdiction de créer un module.
  - Les contraintes incluent “doc canonique + kanban + point de reprise”.
  - Le point de reprise est présent et explicite.

## 4. CAS TEST 2 — BUNDLE TRANSFER (MODE BUNDLE_TRANSFER)
### 4.1 Entrée (synthèse)
- Fichier : `modules/validated_prompt_factory/inputs/synthesis_bundle_transfer.txt`
- Intent : produire un prompt de bundle ZIP strict (liste explicite) pour livraison documentaire via la surface `shared`.

### 4.2 Commande rejouée (preuve)
```bash
python modules/validated_prompt_factory/app/validated_prompt_factory.py ^
  --input modules/validated_prompt_factory/inputs/synthesis_bundle_transfer.txt ^
  --mode bundle_transfer ^
  --output-dir state/vpf_real_use_2026-03-14
```
Sortie observée :
- `Success: Generated state/vpf_real_use_2026-03-14\prompt_bundle_transfer.txt`

### 4.3 Sortie produite (preuve)
- Fichier : `state/vpf_real_use_2026-03-14/prompt_bundle_transfer.txt`
- Vérification métier :
  - Le prompt liste explicitement les fichiers à inclure.
  - Le prompt contient désormais contraintes + risques + suite + point de reprise (après patch minimal).

## 5. ÉCARTS PROUVÉS
- GAP-01 (corrigé) : le template `bundle_transfer` ne rendait pas les champs de continuité (`CONTRAINTES`, `DEPENDANCES`, `SUITE`, `POINT DE REPRISE`) alors qu’ils font partie des sections attendues et du workflow (doc+kanban+reprise).

## 6. PATCH MINIMAL APPLIQUÉ (SI ÉCART)
- Fichier modifié : `modules/validated_prompt_factory/app/validated_prompt_factory.py`
- Changement : extension du template `bundle_transfer` pour inclure :
  - CONTRAINTES
  - RISQUES/DEPENDANCES
  - SUITE
  - POINT DE REPRISE

## 7. VALIDATION FINALE
### ÉTABLI
- Génération de prompts prouvée sur 2 cas utiles (registry central + bundle_transfer).
- Les prompts produits sont structurés et exploitables en session.

### À CONFIRMER
- Exécution via wrappers `cmd.sh`/`sanity.sh` sur cible Linux (scripts bash) : non rejouée ici (environnement Windows), à valider en hardening.

## 8. KANBAN (SOURCE OF TRUTH)
- Kanban mis à jour : `opt_trading_kanban_source_of_truth_2026-03-13_updated.md` (section validated_prompt_factory).

## 9. POINT DE REPRISE EXACT
> **GO_OT_MODULE_02_VALIDATED_PROMPT_FACTORY_HARDENING**

