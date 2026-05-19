# OT-MODULE-03 — VALIDATED_PROMPT_FACTORY (ADOPTION) — REPORT

Date (America/Montreal) : 2026-03-14

## 1. RÉSUMÉ EXÉCUTIF
- Adoption opérateur minimale réalisée : parcours nominal documenté, 3 cas standard bornés, et menu aligné sur ces cas.
- Aucun changement de mission du module ; patchs limités à l’adoption réelle (doc + menu + kanban).
- Preuves : génération rejouée sur 3 cas standard (patch/bundle/chatgpt) + 1 cas d’échec propre.

## 2. ÉTAT RÉEL ÉTABLI
- Module : `modules/validated_prompt_factory/`
- Modes disponibles : `chatgpt_session`, `trae_module`, `trae_patch`, `bundle_transfer`
- Entrées standard disponibles :
  - `inputs/synthesis_registry_central.txt`
  - `inputs/synthesis_bundle_transfer.txt`
  - `inputs/synthesis_example.txt`
- Sorties :
  - Via Python : dossier `--output-dir` (recommandé côté Windows)
  - Via `cmd.sh` : `modules/validated_prompt_factory/output/` (fichiers `prompt_<mode>.txt`)

## 3. PARCOURS OPÉRATEUR NOMINAL RETENU
### Lancer
- Linux / Git Bash : depuis `modules/validated_prompt_factory/`
  - `./cmd.sh generate <mode> <input_file>`
  - `./menu.sh` (parcours menu)
- Windows natif : utiliser Python
  - `python modules/validated_prompt_factory/app/validated_prompt_factory.py --input <file> --mode <mode> --output-dir <dir>`

### Choisir le mode
- `trae_patch` : produire un prompt strict de patch (cas nominal opérateur).
- `bundle_transfer` : produire un prompt de bundle ZIP (livraison ciblée).
- `chatgpt_session` : produire un prompt de cadrage conversationnel (optionnel).

### Entrée à fournir
- Un fichier texte structuré contenant toutes les sections requises (validation bloquante).
- Headers acceptés en texte brut ou Markdown (ex: `## CONTEXTE`).

### Output à récupérer
- Le chemin exact est affiché : `Success: Generated <path>`.
- Le fichier est `prompt_<mode>.txt`.
- Le fichier est écrasé à chaque génération pour un même mode.

## 4. CAS STANDARD RETENUS (MAX 3)
1) Patch Trae (nominal)
   - Input : `modules/validated_prompt_factory/inputs/synthesis_registry_central.txt`
   - Mode : `trae_patch`
   - Output (preuves) : `state/vpf_adoption_2026-03-14/prompt_trae_patch.txt`
2) Bundle transfer (nominal)
   - Input : `modules/validated_prompt_factory/inputs/synthesis_bundle_transfer.txt`
   - Mode : `bundle_transfer`
   - Output (preuves) : `state/vpf_adoption_2026-03-14/prompt_bundle_transfer.txt`
3) Session ChatGPT (optionnel)
   - Input : `modules/validated_prompt_factory/inputs/synthesis_example.txt`
   - Mode : `chatgpt_session`
   - Output (preuves) : `state/vpf_adoption_2026-03-14/prompt_chatgpt_session.txt`

## 5. ÉCARTS PROUVÉS ET CORRECTIONS APPLIQUÉES
### ÉTABLI (post-hardening)
- Validation d’entrée bloquante + échec explicite si section manquante.
- Tolérance aux en-têtes Markdown.
- Template bundle_transfer inclut la continuité (contraintes/risques/suite/reprise).

### CORRECTIONS (ADOPTION)
- `menu.sh` : les entrées par défaut pointent vers les inputs standard (patch/bundle/example) pour réduire l’ambiguïté opérateur.
- `README.md` : parcours nominal et cas standard explicités, sorties clarifiées.

## 6. PREUVES D’EXÉCUTION
Voir les commandes et sorties dans le closing (ou logs de terminal) et les fichiers générés sous `state/vpf_adoption_2026-03-14/`.

## 7. KANBAN (SOURCE OF TRUTH)
- `opt_trading_kanban_source_of_truth_2026-03-13_updated.md` mis à jour : OT-MODULE-03 ajouté et point de reprise basculé.

## 8. POINT DE REPRISE EXACT
> **GO_OT_MODULE_04_VALIDATED_PROMPT_FACTORY_LINUX_WRAPPERS_SMOKE**

