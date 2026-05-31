---
doc_id: OPENCLAW_MODULE_MODEL_PROVIDER_OPENCLAW
doc_type: module_fiche
module: model_provider_openclaw
path: modules/model_provider_openclaw/
go_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_EXTRACTION_01
updated_at: 2026-05-30
statut: actif
---

# model_provider_openclaw — Fiche opérateur

Module V1 de politique provider/modèle pour OpenClaw. Centralise et borne la sélection des providers, modèles, paramètres par défaut et fallbacks pour les agents OpenClaw.

## Règle V1

```
Aucun agent OpenClaw ne choisit directement son provider/modèle.
Toute résolution passe par model_provider_openclaw.
```

## Agents couverts

```
orchestrateur
builder
reviewer
lab
```

## Fichiers de configuration

```
config/providers_policy.yaml      — politique globale des providers autorisés
config/agent_model_matrix.yaml    — matrice agent → provider/modèle/bornes/fallback
```

## Scripts

```bash
bash scripts/cmd.sh status                      # état politique provider
bash scripts/cmd.sh sanity                      # validation installation
bash scripts/cmd.sh show-agent orchestrateur    # détails agent spécifique
bash scripts/cmd.sh export-json                 # export JSON de la politique
bash scripts/menu.sh                            # menu interactif
bash scripts/sanity_check.sh                    # validation installation
bash scripts/install_shortcuts.sh               # installe wrappers /usr/local/bin
```

## Contenu

```
app/model_provider_openclaw.py    — logique lecture/validation/export
config/providers_policy.yaml
config/agent_model_matrix.yaml
docs/model_provider_openclaw.doc.md  — doctrine et règles V1
scripts/cmd.sh
scripts/menu.sh
scripts/sanity_check.sh
scripts/install_shortcuts.sh
```

## Intégration

- Installable via `install_module_openclaw`
- Les agents OpenClaw (orchestrateur, builder, reviewer, lab) le consultent
  avant toute sélection de provider/modèle

## Statut

```
actif — couche de politique provider/modèle V1
```
