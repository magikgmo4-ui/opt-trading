---
doc_id: OPENCLAW_MODULE_OPENCLAW_CONFIG_MODULAIRE
doc_type: module_fiche
module: openclaw_config_modulaire
path: modules/openclaw_config_modulaire/
go_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_EXTRACTION_01
updated_at: 2026-05-30
statut: actif
---

# openclaw_config_modulaire — Fiche opérateur

Gestion modulaire de la configuration OpenClaw avec apply safe, validation et rollback.

## Rôle

- Garder un `openclaw.json` racine court
- Externaliser `agents` et `tools` dans `~/.openclaw/config.d/`
- Sauvegarder avant application (backup automatique)
- Valider la config puis permettre un rollback si nécessaire

## Fichiers gérés

```
~/.openclaw/openclaw.json              — config racine
~/.openclaw/config.d/agents.json5     — config agents
~/.openclaw/config.d/tools.json5      — config tools
```

## Scripts

```bash
bash scripts/cmd.sh status    # état config modulaire
bash scripts/cmd.sh backup    # sauvegarde avant apply
bash scripts/cmd.sh apply     # apply safe (backup + validate + apply)
bash scripts/cmd.sh validate  # valide la config courante
bash scripts/cmd.sh health    # health gateway post-apply
bash scripts/cmd.sh probe     # probe gateway post-apply
bash scripts/cmd.sh rollback  # rollback vers le dernier backup
bash scripts/cmd.sh paths     # chemins clés gérés
bash scripts/apply_safe.sh    # script apply safe direct
bash scripts/rollback.sh      # script rollback direct
bash scripts/sanity_check.sh  # validation installation
bash scripts/install_shortcuts.sh  # installe wrappers /usr/local/bin
```

## Contenu

```
app/openclaw_root_template.json5
app/agents.json5
app/tools.json5
scripts/cmd.sh
scripts/apply_safe.sh
scripts/rollback.sh
scripts/sanity_check.sh
scripts/install_shortcuts.sh
docs/README.md
```

## Intégration

- Déployable via `install_module_openclaw`
- S'articule avec `gateway_openclaw` : après apply config, redémarrer le gateway
  et vérifier `health` + `probe`

## Distinction openclaw_config_modulaire vs configure_openclaw

| Module | Rôle |
| --- | --- |
| `openclaw_config_modulaire` | Config modulaire `config.d/` + apply safe + rollback |
| `configure_openclaw` | Façade opérateur sur la configuration live (get/set/wizard) |

## Statut

```
actif — composant de configuration structurelle de la suite OpenClaw
```
