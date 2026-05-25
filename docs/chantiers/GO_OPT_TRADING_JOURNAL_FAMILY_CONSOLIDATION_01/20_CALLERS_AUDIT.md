---
doc_id: GO_OPT_TRADING_JOURNAL_FAMILY_CONSOLIDATION_01_CALLERS_AUDIT
doc_type: callers_audit
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_JOURNAL_FAMILY_CONSOLIDATION_01
status: draft_for_review
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - modules
  - journal
  - callers
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-23
links:
  - docs/chantiers/GO_OPT_TRADING_JOURNAL_FAMILY_CONSOLIDATION_01/10_FAMILY_INVENTORY.md
---

# 20_CALLERS_AUDIT

## 1. Callers de `journal_de_bord`

### Directs non-documentaires constates

Aucun caller non-documentaire repo-courant n'a ete trouve, car `modules/journal_de_bord/` est absent.

### Ancrages documentaires historiques

| Caller | Type | Lecture |
| --- | --- | --- |
| `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/02_module_family_consolidation_audit.md` | audit historique | dualite encore ouverte a cette date |
| `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/04_consolidation_targets_and_go_list.md` | plan historique | classait encore `journal_de_bord` comme runtime utile |
| `docs/governance/REPO_ROOT_POLICY.md` | gouvernance recente | acte au contraire son retrait comme surface obsolete |

### Conclusion

`journal_de_bord` n'a plus de callers runtime dans l'etat courant du repo.

## 2. Callers de `journal_engine`

### Directs non-documentaires constates

| Caller | Type | Preuve | Lecture |
| --- | --- | --- | --- |
| `modules/desk_pro_orchestrator/app/desk_pro_orchestrator.py` | caller metier | registre `journal_engine -> modules.journal_engine.app.journal_engine` | moteur integre au pipeline Desk Pro |
| `scripts/admin_trading/desk_pro_copy_latest_to_shared.sh` | caller artefact | copie `journal_engine.json` | artefact runtime attendu |
| `scripts/ai/menu/opt_trading_menu.json` | surface ops | expose `journal_engine` dans le menu | presence operateur/documentee |
| `modules/journal_engine/scripts/cmd.sh` | wrapper module | lance `python3 -m modules.journal_engine.app.journal_engine` | wrapper actif |

### Ancrages documentaires recents

| Caller | Type | Lecture |
| --- | --- | --- |
| `docs/deploy_module_multi_machine_continuity.md` | review de deploiement | `journal_engine` juge reel mais pas standard-deployable en l'etat |
| `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_OBSERVABILITY_01/40_OUTPUT_ARTIFACT_OBSERVABILITY.md` | observabilite | artefact `journal_engine.json` attendu |

### Conclusion

`journal_engine` est bien consomme aujourd'hui comme moteur de journalisation dans le pipeline Desk Pro.

## 3. Reponse callers

1. `journal_de_bord` n'a plus de callers runtime actuels dans le repo courant.
2. `journal_engine` a des callers metier et artefact reels.
3. Le conflit de famille releve surtout d'un decalage entre l'audit historique et l'etat courant du parc.
