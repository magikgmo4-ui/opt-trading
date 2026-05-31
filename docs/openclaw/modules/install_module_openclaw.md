---
doc_id: OPENCLAW_MODULE_INSTALL_MODULE_OPENCLAW
doc_type: module_fiche
module: install_module_openclaw
path: modules/install_module_openclaw/
go_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_EXTRACTION_01
updated_at: 2026-05-30
statut: actif
---

# install_module_openclaw — Fiche opérateur

Installeur standard des modules OpenClaw à partir d'un registre local de bundles disponibles.

## Rôle

- Lister les modules OpenClaw installables depuis le registre local
- Copier le module choisi vers la racine cible
- Fournir une expérience `cmd/menu/sanity` comme les autres modules du projet

## Scripts

```bash
bash scripts/cmd.sh list     # liste les modules installables
bash scripts/cmd.sh install <module_id>  # installe un module
bash scripts/menu.sh         # menu interactif
bash scripts/sanity_check.sh # validation installation
bash scripts/install_shortcuts.sh  # installe wrappers /usr/local/bin
```

## Registre local

```
app/modules_registry.json
```

Modules connus dans le registre :

```
openclaw_config_modulaire
install_module_openclaw
model_provider_openclaw
configure_openclaw
doctor_openclaw
evidence_openclaw
gateway_openclaw
```

## Contenu

```
app/modules_registry.json
scripts/cmd.sh
scripts/menu.sh
scripts/sanity_check.sh
scripts/install_shortcuts.sh
docs/README.md
```

## Note

Ne pas confondre avec `install_module` (module générique projet).
`install_module_openclaw` est spécialisé pour la suite OpenClaw et son registre local.

## Statut

```
actif — point d'entrée d'installation de la suite OpenClaw
```
