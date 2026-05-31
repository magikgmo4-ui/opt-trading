---
doc_id: OPENCLAW_MODULE_EVIDENCE_OPENCLAW
doc_type: module_fiche
module: evidence_openclaw
path: modules/evidence_openclaw/
go_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_EXTRACTION_01
updated_at: 2026-05-30
statut: actif
---

# evidence_openclaw — Fiche opérateur

Module de capture de preuves OpenClaw et de génération d'un prompt documentaire fondé sur ces preuves.

## Rôle

- Détecter le workspace du default agent
- Exporter des fichiers de preuve dans ce workspace
- Générer un prompt strict pour la documentation OpenClaw à partir de ces preuves

## Scripts

```bash
bash scripts/cmd.sh detect-workspace   # détecte le workspace agent actif
bash scripts/cmd.sh status             # état du module
bash scripts/cmd.sh export-docs        # exporte les preuves dans le workspace
bash scripts/cmd.sh print-doc-prompt   # affiche le prompt documentaire généré
bash scripts/cmd.sh evidence-dir       # chemin du répertoire de preuves
bash scripts/cmd.sh show-files         # liste les fichiers de preuves exportés
bash scripts/menu.sh                   # menu interactif
bash scripts/sanity_check.sh           # validation installation
bash scripts/install_shortcuts.sh      # installe wrappers /usr/local/bin
```

## Preuves exportées

Destination : `docs_evidence/openclaw_current_state/` dans le workspace OpenClaw détecté.

```
01_doctor_status.txt      # résultat doctor status
02_configure_status.txt   # résultat configure status
03_doctor_quick.txt       # résultat doctor quick
04_workspace_context.txt  # contexte workspace
90_PROMPT_DOCS.txt        # prompt documentaire généré
```

## Contenu

```
scripts/cmd.sh
scripts/menu.sh
scripts/sanity_check.sh
scripts/install_shortcuts.sh
docs/README.md
docs/RUNBOOK.txt
docs/ETABLI.txt
docs/GO_OPENCLAW_*.md
```

## Intégration

- Dépend de `doctor_openclaw` et `configure_openclaw` (si leurs wrappers sont disponibles)
- Écrit dans le workspace du default agent détecté (pas dans opt-trading directement)

## Note

Sa valeur est dans la **preuve exportée** et le **prompt documentaire** — pas dans le pilotage runtime.
Ne pas mélanger avec les modules gateway/configure.

## Statut

```
actif — module de preuve et de continuité documentaire
```
