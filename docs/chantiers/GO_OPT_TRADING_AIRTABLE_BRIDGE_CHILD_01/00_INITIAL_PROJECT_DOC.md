---
doc_id: GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: airtable_bridge
go_id: GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01
parent_go_id: GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01
machine: fantome
status: draft_canonical
lifecycle_stage: opening
topic_keys:
  - opt-trading
  - airtable
  - bridge
  - child
  - implementation
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: Implémenter le module airtable_bridge (client API, payloads, scripts)
updated_at: 2026-05-19
links:
  - docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/05_IMPLEMENTATION_SPEC.md
  - docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/08_SESSION_INDEPENDENT_REPRISE.md
  - docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/99_VERDICT.md
  - bundles/GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01_IDE_BUNDLE/manifest.json
  - bundles/GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01_IDE_BUNDLE/GO_PROMPT_01_IMPLEMENT_MODULE.md
  - bundles/GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01_IDE_BUNDLE/GO_PROMPT_02_VALIDATE_MODULE.md
---

# GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01 — 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Implémenter le module `airtable_bridge` non bloquant pour opt-trading (client API REST Airtable, payloads trades/signals, scripts de sanity/cmd/menu), documenter le module, et produire le closeout.

## 2_PARENT_HERITAGE

Le parent `GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01` est VERDICT_GO_LIMITED (merge). Il fournit :

| Heritage | Fichier |
| --- | --- |
| Implementation spec | `05_IMPLEMENTATION_SPEC.md` — structure module, API, regles client, invariants |
| Session reprise | `08_SESSION_INDEPENDENT_REPRISE.md` — point de reprise autonome |
| Verdict | `99_VERDICT.md` — GO_LIMITED, Airtable retenu pour journal/signaux/validation |
| Schema | `03_AIRTABLE_SCHEMA_TRADING_JOURNAL_V1.md` — tables Trades, Signals, Backtests, GO_Status |
| Architecture | `02_INTEGRATION_ARCHITECTURE.md` — flux et integration |

## 3_BORNES_DU_CHILD

Ce child est strictement borne a :

1. **Module airtable_bridge** — creer `modules/airtable_bridge/` avec :
   - `app/client.py` — client API REST Airtable (POST, batch max 10, retry exponentiel, handle 429, timeout safe)
   - `app/payloads.py` — payloads structures (trade, signal, backtest, go_status)
   - `scripts/sanity_check.sh` — test env + API
   - `scripts/cmd.sh` — commande unique pour appel bridge
   - `scripts/menu.sh` — menu interactif
   - `.env.example` — template de configuration (sans secrets)
   - `README.md` — documentation du module
2. **Doc closeout** — `90_CLOSEOUT.md` avec checklist, verdict, NEXT_GO
3. **Scope doc-only** — aucun runtime, aucun secret, aucune modification des index globaux

## 4_PLAN_D_EXECUTION

### Phase A — Module structure

```text
1. Creer modules/airtable_bridge/app/client.py
   - POST /v0/{base_id}/{table}
   - batch max 10 records
   - retry exponentiel (3 tentatives)
   - handle 429 (rate limit)
   - timeout 10s
   - fail-open : jamais bloquer, logger et retourner vide
2. Creer modules/airtable_bridge/app/payloads.py
   - Classes/Layouts pour trade, signal, backtest, go_status
   - Validation de base (champs requis, types)
3. Creer modules/airtable_bridge/scripts/sanity_check.sh
   - Verifier AIRTABLE_API_KEY et AIRTABLE_BASE_ID presents
   - Tester un GET sur l'API Airtable
4. Creer modules/airtable_bridge/scripts/cmd.sh
   - Appel unique : usage, validation, POST, sortie
5. Creer modules/airtable_bridge/scripts/menu.sh
   - Menu interactif : sanity, send trade, send signal, exit
6. Creer modules/airtable_bridge/.env.example
   - AIRTABLE_API_KEY=
   - AIRTABLE_BASE_ID=
7. Creer modules/airtable_bridge/README.md
```

### Phase B — Validation

```text
1. Verifier module tree complet
2. Verifier .env.example sans secrets
3. Verifier scripts sans execution reelle
4. Verifier client.py sans credentials hardcodes
5. git status clean (fichiers sources non modifies)
```

### Phase C — Closeout

```text
1. Produire 90_CLOSEOUT.md
2. Checklist par phase
3. Verdict: PASS / BLOCKED / REMAINING_GAP
4. NEXT_GO recommande
```

## 5_INVARIANTS (herites du parent)

```text
- Aucun secret, .env, token, cle expose
- Aucune commande git destructive (commit, push, rebase, merge)
- Aucun write runtime non valide
- Toute sortie = DRAFT_ONLY
- Validation finale externe (modele fort / humain / Git diff)
- Seuls les modeles VERIFIED du registry sont autorises
- Ne pas modifier les index globaux (GO_INDEX, BRANCH_STATE, MACHINE_WORK_SPLIT)
- Ne pas modifier les modules existants
```

## 6_GARDE_FOUS_ADDITIONNELS (child)

```text
- Module airtable_bridge cree en /modules/ — jamais modifier core
- .env.example sans vraies valeurs
- scripts/sanity_check.sh en dry-run (verifier sans envoyer)
- client.py: timeout 10s, retry max 3, fail-open
- Aucun endpoint productif appele
```

## 7_CANONICAL_STATE

```text
- Branche: go/GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01
- Base: sot/mainline (merge parent orchestration)
- Machine: fantome
- Perimetre: docs/chantiers/GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01/ + modules/airtable_bridge/
- Statut initial: cadrage
```

## 8_DEPENDANCES

```text
- Implementation spec: docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/05_IMPLEMENTATION_SPEC.md
- IDE bundle: bundles/GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01_IDE_BUNDLE/ (ready_for_review)
- Airtable API: https://airtable.com/api (documentation REST)
```

## 9_RISQUES

| Risque | Mitigation |
| --- | --- |
| API Airtable change | Spec figee sur REST v0, compatible ascendante |
| Token expose dans le code | .env.example template, validation externe avant commit |
| Module cassant le core | Fail-open : jamais bloquer, logger uniquement |
| Scripts non testables sans vrai token | sanity_check.sh en dry-run, validation structurelle |

## 10_CRITERES_PASS

```text
Phase A PASS si :
- modules/airtable_bridge/ present avec app/, scripts/, .env.example, README.md
- client.py: POST, batch, retry, timeout, fail-open implementes
- payloads.py: trade, signal, backtest, go_status structures
- scripts/ : sanity_check.sh, cmd.sh, menu.sh presents

Phase B PASS si :
- Aucun secret expose
- Aucune modification des modules existants
- .env.example sans valeurs reelles
- scripts executables sans erreur de syntaxe

PASS global = Phase A + Phase B + closeout documente
```

## 11_NEXT_GO

```text
Apres PASS: GO_OPT_TRADING_STRICT_WORKERS_CHILD_AIRTABLE_INTEGRATION_01
- Worker Airtable pour synchro modeles/matrices via le bridge
- Job packets WRITE_GATED pour ecriture dans Airtable
```

## 12_RESUME_POINT

```text
fantome
→ AIRTABLE_BRIDGE_CHILD_01
→ Branche: go/GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01
→ Phase A en premier (module structure)
→ Implementation spec: 05_IMPLEMENTATION_SPEC.md
→ IDE bundle: bundles/GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01_IDE_BUNDLE/
→ Garde-fous stricts (fail-open, pas de secrets, pas de modifications core)
```
