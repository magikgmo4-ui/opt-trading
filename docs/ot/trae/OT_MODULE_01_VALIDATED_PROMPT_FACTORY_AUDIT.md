# OT-MODULE-01 — AUDIT DE VALIDATED PROMPT FACTORY

## 1. CONTEXTE DE DÉPART
- **Sources lues** : `docs/master_pack/00_current_state_and_standards.md`
- **État supposé** : Module standard avec wrappers `cmd` et `menu`.
- **Réalité observée** : Structure non standard. Pas de dossier `scripts/`. Scripts à la racine ou manquants.

## 2. INVENTAIRE STRUCTUREL
### Fichiers présents :
- `factory_cmd.sh` (Probable wrapper CMD)
- `factory_menu.sh` (Probable wrapper MENU)
- `prompt_factory.py` (Script Python principal)
- `prompts/` (Dossier de données)
- `README.md`
- `requirements.txt`

### Manquants (vs Standard) :
- Pas de dossier `scripts/` (Scripts à la racine du module).
- Pas de `sanity_check.sh` apparent.

## 3. ANALYSE REGISTRY
- **Modules Registry** : Déclaré comme `active`.
- **Wrappers Registry** :
    - `menu-validated_prompt_factory` -> pointe vers `modules/validated_prompt_factory/factory_menu.sh`.
    - `cmd-validated_prompt_factory` -> pointe vers `modules/validated_prompt_factory/factory_cmd.sh`.

## 4. CONCLUSION AUDIT
Le module est **FONCTIONNEL MAIS NON STANDARD**.
Il ne respecte pas la convention `modules/<name>/scripts/cmd.sh`.
Cependant, les wrappers pointent vers les bons fichiers existants.
Le risque est faible, mais la maintenance est légèrement plus complexe car il faut savoir que les scripts sont à la racine.

**Action recommandée** : Ne pas déplacer les scripts (risque de casser les symlinks existants), mais documenter cette exception ou valider que cela fonctionne tel quel.
