---
doc_id: OPENCLAW_MODULE_MENU_OPENCLAW
doc_type: module_fiche
module: menu_openclaw
path: modules/menu_openclaw/
go_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_EXTRACTION_01
updated_at: 2026-05-30
statut: actif
---

# menu_openclaw — Fiche opérateur

Hub opérateur compact pour relier les modules OpenClaw déjà présents dans `opt-trading`.

## Rôle

- Offrir un point d'entrée unique vers la suite OpenClaw
- Lister les menus déclarés dans la registry OpenClaw
- Ouvrir rapidement le menu d'un module par `module_id`
- Servir de point d'appui de reprise pour la chaîne OpenClaw

## Scripts

```bash
bash scripts/cmd.sh status              # état du hub
bash scripts/cmd.sh list-menus          # liste tous les menus déclarés
bash scripts/cmd.sh list-menus-numbered # liste numérotée
bash scripts/cmd.sh open-menu <id>      # ouvre le menu d'un module
bash scripts/cmd.sh useful              # commandes utiles
bash scripts/cmd.sh paths               # chemins clés de la suite
bash scripts/menu.sh                    # menu interactif hub
bash scripts/sanity_check.sh            # validation installation
bash scripts/install_shortcuts.sh       # installe wrappers /usr/local/bin
```

## Contenu

```
scripts/cmd.sh
scripts/menu.sh
scripts/sanity_check.sh
scripts/install_shortcuts.sh
scripts/commandes_utiles.sh
docs/README.md
docs/RUNBOOK.txt
docs/GO_OPENCLAW_*.md
```

## Chaîne de référence (ordre d'installation/usage)

```
1. install_module_openclaw    — installe les modules
2. openclaw_config_modulaire  — config modulaire + apply safe
3. gateway_openclaw           — démarre le gateway
4. configure_openclaw         — configure le runtime
5. doctor_openclaw            — diagnostique
6. evidence_openclaw          — capture preuves
```

## Note

`menu_openclaw` fédère la suite — il ne duplique pas les commandes des sous-modules.
Hub de navigation et de reprise, pas module runtime autonome.

## Statut

```
actif — hub de navigation de la suite OpenClaw
```
