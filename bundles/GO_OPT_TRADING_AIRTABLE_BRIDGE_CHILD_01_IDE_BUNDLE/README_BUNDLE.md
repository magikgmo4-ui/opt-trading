---
doc_id: GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01_IDE_BUNDLE_README
doc_type: ide_bundle_readme
repo: opt-trading
project: opt-trading
module: airtable_bridge
go_id: GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01
status: ready
lifecycle_stage: implementation_bundle
surface: bundles
source_kind: canonical
updated_at: 2026-04-24
topic_keys:
  - airtable_bridge
  - ide_bundle
  - implementation
  - trae
  - opencode
  - cursor
links:
  - docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/08_SESSION_INDEPENDENT_REPRISE.md
  - docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/05_IMPLEMENTATION_SPEC.md
  - docs/desk_pro_trae_master_prompt_pack.md
  - docs/master_pack/00_current_state_and_standards.md
---

# IDE BUNDLE — GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01

## Objet

Bundle IDE autonome pour implémenter `modules/airtable_bridge/` dans `opt-trading`.

Ce bundle est conçu pour Trae / Cursor / OpenCode / autre IDE agentique. Il doit permettre de coder sans dépendre de la session ChatGPT.

## Point de reprise obligatoire

Lire d'abord :

1. `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
2. `docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/08_SESSION_INDEPENDENT_REPRISE.md`
3. `docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/05_IMPLEMENTATION_SPEC.md`
4. `docs/desk_pro_trae_master_prompt_pack.md`
5. `docs/master_pack/00_current_state_and_standards.md`

## Règles reprises des docs lues

- Modules petits, composables et machine-aware.
- Patchs incrémentaux et réversibles.
- Aucun secret hardcodé.
- Scripts standards requis : `sanity_check.sh`, `cmd.sh`, `menu.sh`.
- Wrappers globaux attendus : `sanity-airtable_bridge`, `cmd-airtable_bridge`, `menu-airtable_bridge`.
- Scripts internes compatibles symlink via `readlink -f`.
- Déclaration future dans `registry/modules_registry.yaml` et `registry/wrappers_registry.yaml`.
- Pas de `sudo` dans les scripts runtime.
- `/shared` utilisé pour rapports, exports et bundles si utile.
- Airtable doit rester optionnel et fail-open.

## Produit à implémenter

Créer :

```text
modules/airtable_bridge/
├── README.md
├── .env.example
├── app/
│   ├── __init__.py
│   ├── client.py
│   └── payloads.py
├── scripts/
│   ├── sanity_check.sh
│   ├── cmd.sh
│   └── menu.sh
├── tests/
│   └── test_payloads.py
└── examples/
    ├── trade_payload.json
    └── signal_payload.json
```

## Contraintes techniques

- Python standard library en priorité.
- `requests` autorisé seulement si déjà accepté par l'environnement ; sinon fallback `urllib.request`.
- Timeout obligatoire.
- Retry borné.
- Gestion 429.
- Batch Airtable max 10 records.
- Fail-open : aucune exception réseau ne doit casser opt-trading.
- `.env.example` sans secrets.

## Ordre d'exécution IDE

1. Lire ce README.
2. Lire `manifest.json`.
3. Exécuter `GO_PROMPT_01_IMPLEMENT_MODULE.md`.
4. Exécuter `GO_PROMPT_02_VALIDATE_MODULE.md`.
5. Si PASS, exécuter `GO_PROMPT_03_DOCUMENT_CLOSEOUT.md`.

## Critère PASS

- Arborescence module créée.
- Payloads validables sans réseau.
- Sanity local PASS sans secrets.
- Mode réseau skip propre si secrets absents.
- Aucun secret committé.
- Documentation module présente.
- Prochaine intégration Bot Vision documentée mais non appliquée.

## Critère FAIL

- Airtable devient dépendance critique.
- Secrets écrits dans repo.
- Script bloque si Airtable indisponible.
- Pas de wrappers standards.
- Pas de tests sans réseau.
- Refactor hors périmètre.
