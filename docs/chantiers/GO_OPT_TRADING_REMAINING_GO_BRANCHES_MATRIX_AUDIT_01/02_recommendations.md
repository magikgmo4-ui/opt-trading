---
doc_id: GO_OPT_TRADING_REMAINING_GO_BRANCHES_MATRIX_AUDIT_01_RECOMMENDATIONS
doc_type: recommendations
repo: opt-trading
project: opt-trading
module:
  go_id: GO_OPT_TRADING_REMAINING_GO_BRANCHES_MATRIX_AUDIT_01
status: active
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - branch_audit
  - recommendations
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_REMAINING_GO_BRANCHES_MATRIX_AUDIT_01/01_branch_matrix_audit.md
point_de_reprise: "Groupes de recommandation"
updated_at: 2026-04-28
links:
  - docs/chantiers/GO_OPT_TRADING_REMAINING_GO_BRANCHES_MATRIX_AUDIT_01/01_branch_matrix_audit.md
---

# Recommendations

## 1. KEEP_ACTIVE

- `go/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01`
  Action suivante : conserver la branche active et recadrer ensuite son delta doc-only contre le parent ouvert deja canonise par la matrice et `GO_INDEX`.
- `go/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01`
  Action suivante : conserver la branche active, puis corriger le manque de ligne dans `BRANCH_STATE.md` dans un lot dedie avant tout arbitrage de suppression.

## 2. KEEP_REFERENCE

- Aucun cas solide a classer ici pour l'instant.
  Motif : les branches a delta nul sont soit closes, soit non canonisees, et ne sont pas assez prouvees comme references utiles durables.

## 3. TRANSPORT_DOCS_THEN_DELETE

- `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01`
  Action suivante : transporter le dossier parent doc-only vers `sot/mainline` pour completer la preuve canonique du parent, puis requalifier la branche support.
- `go/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01_ALIGNMENT_01`
  Action suivante : comparer son delta a `go/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01`, transporter uniquement les ecarts utiles au parent, puis supprimer la branche de support si elle devient redondante.

## 4. DELETE_AFTER_CONFIRMATION

- `go/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01_ISOLATED`
  Action suivante : confirmer qu'aucune PR ou revue ouverte ne depend encore de cette branche, puis la supprimer; elle n'a plus de delta unique.
- `go/GO_OPT_TRADING_INDEX_AGGREGATION_BATCH_01`
  Action suivante : confirmer qu'aucun suivi humain n'attend encore ce support Git, puis supprimer la branche close/pass devenue sans delta.
- `go/GO_OPT_TRADING_OPENCLAW_AGENTS_PARENT_LIVE_ARTIFACTS_01`
  Action suivante : verifier qu'aucun usage externe ne depend encore du nom de branche, puis supprimer cette reference distante a delta nul et sans preuve canonique.

## 5. NEEDS_DEEP_AUDIT

- `go/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01`
  Action suivante : qualifier le statut produit reel avant toute canonisation, car le contenu melange chantier docs, bundles et tentative de trace `BRANCH_STATE`.
- `go/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01`
  Action suivante : verifier si ce parent doit exister dans `GO_INDEX` ou s'il ne s'agit que d'un support bundle lateral non canonique.
- `go/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01`
  Action suivante : relire les 3 fichiers ajoutes pour decider s'il s'agit d'un vrai parent a ouvrir ou d'un simple artefact de travail.
- `go/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01`
  Action suivante : qualifier si le bundle ClickUp represente un parent canonique, un support externe, ou une archive de coordination.
- `go/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01`
  Action suivante : ne pas merger ni utiliser la branche pour PR; auditer separement le delta runtime/doc pollue avant toute fermeture de support Git.
- `go/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01`
  Action suivante : decider si l'Ollama local releve d'un parent actif canonique ou d'une exploration laterale a garder hors `GO_INDEX`.
- `go/GO_OPT_TRADING_OPENCLAW_AGENTS_PARENT_LONA_MCP_TMUX_EXEC_01`
  Action suivante : verifier si ce parent OpenClaw doit etre rattache a un parent deja ouvert ou rester hors canon.
- `go/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01`
  Action suivante : qualifier le parent et son bundle KG avant toute promotion, car la branche porte un corpus doc-only important mais aucun ancrage canonique courant.
- `go/GO_OPT_TRADING_REPO_SURFACES_PARENT_CARTOGRAPHY_01`
  Action suivante : verifier si ce cadrage doit etre transporte vers un parent deja canonise (`CANON_STRUCTURE` / `MATRICE_DOC_OPS`) plutot qu'ouvert comme branche autonome.
- `go/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01`
  Action suivante : traiter comme audit profond obligatoire, car la branche touche docs, reports et scripts hors simple doc-only, sans presence canonique dans les index.

## Resume operatoire

- 2 branches peuvent rester actives sans suppression immediate.
- 2 branches ressemblent a des supports de transport doc-only.
- 3 branches paraissent candidates a suppression apres confirmation.
- 10 branches restent insuffisamment prouvees ou trop ambiguës pour un geste Git direct.
