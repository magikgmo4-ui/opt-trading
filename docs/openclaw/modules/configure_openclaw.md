---
doc_id: OPENCLAW_MODULE_CONFIGURE_OPENCLAW
doc_type: module_fiche
module: configure_openclaw
path: modules/configure_openclaw/
go_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_EXTRACTION_01
updated_at: 2026-05-30
statut: actif
---

# configure_openclaw — Fiche opérateur

Façade opérateur standardisée pour la configuration OpenClaw au niveau utilisateur.

## Rôle

- Lancer la configuration OpenClaw
- Valider la config courante
- Lire / écrire des chemins de configuration
- Gérer les agents et l'identité de workspace
- Ouvrir le dashboard OpenClaw

## Scripts

```bash
bash scripts/cmd.sh status          # état config courante
bash scripts/cmd.sh validate        # valide la config
bash scripts/cmd.sh config-file     # chemin du fichier config actif
bash scripts/cmd.sh wizard          # assistant configuration interactif
bash scripts/cmd.sh dashboard       # ouvre le dashboard OpenClaw
bash scripts/cmd.sh agents-*        # gestion agents
bash scripts/cmd.sh get <key>       # lire une valeur
bash scripts/cmd.sh set <key> <val> # écrire une valeur
bash scripts/cmd.sh unset <key>     # effacer une valeur
bash scripts/menu.sh                # menu interactif
bash scripts/sanity_check.sh        # validation installation
bash scripts/install_shortcuts.sh   # installe wrappers /usr/local/bin
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
docs/PROMPT_STANDARD.txt
```

## Intégration

- S'insère dans la chaîne documentée par `menu_openclaw`
- S'appuie sur le binaire `openclaw` et la config utilisateur active
- Travaille avec `openclaw_config_modulaire` (distinctions ci-dessous)

## Distinction configure_openclaw vs openclaw_config_modulaire

| Module | Rôle |
| --- | --- |
| `configure_openclaw` | Façade opérateur sur la configuration **live** |
| `openclaw_config_modulaire` | Gestion modulaire `config.d/` avec apply safe + rollback |

## Statut

```
actif — composant de configuration / post-install de la suite OpenClaw
```
