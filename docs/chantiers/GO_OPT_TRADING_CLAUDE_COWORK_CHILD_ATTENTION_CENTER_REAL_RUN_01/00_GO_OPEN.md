---
doc_id: GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01_00_GO_OPEN
doc_type: chantier/go_open
repo: opt-trading
machine: cursor-ai
go_id: GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01
status: active
scope: doc-only
opened_at: 2026-05-09
base: sot/mainline
branch: go/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01
parent_go: GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_PROMPT_01
links:
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_PROMPT_01/70_FINAL_PROMPT.md
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01/10_SOURCE_STATE.md
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01/20_REAL_RUN_PROTOCOL.md
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01/30_CLAUDE_OUTPUT_CAPTURE.md
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01/40_P0_P1_P2_RESULTS.md
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01/50_GAPS_AND_ADJUSTMENTS.md
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01/60_EXPORT_REPORT.md
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01/90_CLOSEOUT.md
  - docs/index/inbox/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01.md
---

# 00_GO_OPEN

## Identifiant

`GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01`

## Objectif

Exécuter le premier run réel du prompt `OPT_TRADING_ATTENTION_CENTER_01` dans Claude Cowork / Live Artifact et documenter le résultat.

## Contexte

- PR #266 est mergée : le prompt `OPT_TRADING_ATTENTION_CENTER_01` est intégré au trunk canonique `sot/mainline`.
- Le pack `bundles/claude-artifacts/` est `product_closed`.
- Ce GO sert à exécuter le prompt, capturer la sortie réelle, classer les résultats en P0/P1/P2, et vérifier les critères PASS/FAIL.

## Périmètre

- doc-only
- aucun runtime
- aucun modules/
- aucun admin-trading
- aucun TradingView MCP
- aucun DOC_OPS BLOCKED
- aucun index global modifié

## Base et branche

- Base : `sot/mainline` (HEAD: 782e5a1 / PR #266 merge, puis 9123687 / PR #267 merge)
- Branche dédiée : `go/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01`

## Structure du chantier

| Fichier | Rôle |
| --- | --- |
| `00_GO_OPEN.md` | Ouverture GO, contexte, périmètre |
| `10_SOURCE_STATE.md` | État du repo et sources lues au moment du run |
| `20_REAL_RUN_PROTOCOL.md` | Protocole d'exécution du prompt |
| `30_CLAUDE_OUTPUT_CAPTURE.md` | Capture de la sortie réelle du run |
| `40_P0_P1_P2_RESULTS.md` | Classement des résultats en P0/P1/P2 |
| `50_GAPS_AND_ADJUSTMENTS.md` | Gaps observés et ajustements proposés |
| `60_EXPORT_REPORT.md` | Export journalisé (contenu proposé, non committé automatiquement) |
| `90_CLOSEOUT.md` | Fermeture du GO avec verdict PASS/FAIL |

## Critères PASS

- Le prompt est exécutable dans Claude Cowork.
- La sortie produit une liste exploitable P0/P1/P2.
- Les sources réellement lues sont identifiables.
- Aucun état machine non prouvé n'est présenté comme ETAT_VERIFIE.
- Le mode read-only est respecté.
- Aucun gap bloqueur n'est détecté.
- Le rapport/export est défini ou capturé.
- Le diff Git reste limité à docs/.
- Aucun runtime, aucun modules/, aucun secret.

## Critères FAIL

- Claude écrit ou propose d'écrire sans GO explicite.
- Claude invente des états machine.
- Claude mélange hypothèses et faits établis.
- Claude ne produit pas de classement P0/P1/P2 exploitable.
- Claude dépend d'une source non autorisée ou non documentée.
- Le prompt n'est pas directement utilisable.

## RISKS

- À qualifier.
