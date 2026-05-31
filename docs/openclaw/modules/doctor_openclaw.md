---
doc_id: OPENCLAW_MODULE_DOCTOR_OPENCLAW
doc_type: module_fiche
module: doctor_openclaw
path: modules/doctor_openclaw/
go_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_EXTRACTION_01
updated_at: 2026-05-30
statut: actif
---

# doctor_openclaw — Fiche opérateur

Façade standardisée de diagnostic et de réparation prudente pour OpenClaw.

## Rôle

- Lancer les checks `doctor` (quick ou deep)
- Vérifier `config validate`, `gateway health`, `gateway probe`
- Proposer une réparation safe
- Générer un token gateway si nécessaire

## Scripts

```bash
bash scripts/cmd.sh quick           # check rapide
bash scripts/cmd.sh deep            # check approfondi
bash scripts/cmd.sh repair-safe     # réparation non destructive
bash scripts/cmd.sh generate-token  # génère un token gateway
bash scripts/cmd.sh validate        # valide la config
bash scripts/cmd.sh health          # health gateway
bash scripts/cmd.sh probe           # probe gateway
bash scripts/cmd.sh logs            # logs gateway
bash scripts/cmd.sh status          # état global
bash scripts/cmd.sh dashboard       # dashboard OpenClaw
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
```

## Intégration

- Travaille avec `gateway_openclaw` (pilotage runtime) et `configure_openclaw` (config live)
- Sert de couche de vérification avant et après tout changement de config

## Distinction doctor_openclaw vs gateway_openclaw

| Module | Rôle |
| --- | --- |
| `doctor_openclaw` | Diagnostic + vérification de santé |
| `gateway_openclaw` | Pilotage runtime du gateway (start/stop/attach) |

## Statut

```
actif — façade de diagnostic de la suite OpenClaw
```
