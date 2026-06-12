---
doc_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01_CADRAGE
doc_type: cadrage
status: draft_doc_only
module: governance_openclaw_mcp_policy_yaml_draft
go_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01
created_at: 2026-05-13
runtime_binding: false
validator_created: false
---

# 00_CADRAGE

## 1_MASTER_TARGET

Formaliser OpenClaw comme une gouvernance MCP deny-by-default, ou chaque capability est explicitement classee, gatee, tracee et evaluee avant toute promotion vers un format executable.

## 2_INITIAL_PROJECT_DOC

Sources obligatoires lues ou recroisees :

- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_CHATGPT_ORCHESTRATION_RECONCILIATION_01/` via ref Git `go/GO_OPENCLAW_GOVERNANCE_CHATGPT_ORCHESTRATION_RECONCILIATION_01`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_BOUNDARY_SPEC_01/` via ref Git `go/GO_OPENCLAW_GOVERNANCE_MCP_BOUNDARY_SPEC_01`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_HUMAN_REVIEW_GATES_01/` via ref Git `go/GO_OPENCLAW_GOVERNANCE_HUMAN_REVIEW_GATES_01`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_AGENT_TRACE_EVALS_PROFILE_01/` via ref Git `go/GO_OPENCLAW_GOVERNANCE_AGENT_TRACE_EVALS_PROFILE_01`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01/`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01/02_POLICY_SCHEMA_FIELDS.md`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01/03_CAPABILITY_POLICY_CLASSES.md`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01/08_DENY_BY_DEFAULT_RULES.md`
- `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01/10_POLICY_EXAMPLES_DRAFT.md`
- `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md`
- `docs/index/BRANCH_STATE.md`
- `docs/index/GO_INDEX.md`
- `docs/index/ACTIVE_STREAMS.md`
- `docs/index/REPRISE.md`

Les chantiers precedents absents du worktree courant ont ete lus comme objets Git par branche dediee, sans checkout, merge, cherry-pick ni modification de ces branches.

## 3_INITIAL_NEED

Transformer le schema canonique MCP Policy valide dans `GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01` en brouillon YAML/JSON documentaire, exploitable plus tard par OpenClaw, MCP, Codex, strict workers et Ollama Lab.

Le besoin est de disposer d'une forme proche machine-readable tout en restant strictement non executable :

- aucune policy chargee ;
- aucun runtime branche ;
- aucun validator cree ;
- aucune config active modifiee ;
- aucune capability implicite autorisee.

## 4_MASTER_PROJECT_PLAN

Plan applique :

1. Verifier l'etat Git reel et la branche dediee.
2. Identifier et isoler les chemins hors scope signales.
3. Relire les socles MCP Boundary, Human Gates, Trace/Evals et Policy Schema.
4. Creer un draft YAML documentaire.
5. Creer un mapping JSON documentaire.
6. Relier capabilities, classes, gates, traces, evals, strict workers et Ollama Lab.
7. Ajouter checklist et exigences futures de validator sans implementation.
8. Creer une inbox locale sans modifier les index globaux.

## 6_FINAL_TARGET

`GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01`

Final target : produire les 12 fichiers chantier et l'inbox locale qui documentent le draft YAML/JSON MCP Policy, sans runtime, sans validator et sans chargement effectif.

## 7_CANONICAL_STATE

Etat Git reel verifie :

```text
Worktree principal:
C:\Users\ghost\opt-trading

git status --short --branch:
## go/GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_EXECUTION_RETRY_01...origin/go/GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_EXECUTION_RETRY_01

git status --porcelain=v1 -uall:
<vide>
```

```text
Worktree dedie au chantier courant:
C:\Users\ghost\opt-trading-mcp-policy-yaml-draft

git status --short --branch:
## go/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01

git branch --show-current:
go/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01

git log --oneline -5:
fa7558f2 docs: define OpenClaw MCP policy schema
e34b9952 Merge pull request #343 from magikgmo4-ui/go/GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RUNTIME_GUARDS_FIX_01
b21a6cd1 Merge pull request #344 from magikgmo4-ui/go/GO_OPT_TRADING_SESSION_CLOSEOUT_MULTI_CHAIN_01
7b70b223 docs: global session closeout -- 4 chains closed
f6bd872b fix: guard admin-trading paper test runtime

git remote -v:
origin https://github.com/magikgmo4-ui/opt-trading.git (fetch)
origin https://github.com/magikgmo4-ui/opt-trading.git (push)
```

Fichiers hors scope admin-trading laisses intacts :

- `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_EXECUTION_RETRY_01/00_GO_OPEN.md`
- `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_EXECUTION_RETRY_01/10_RUNTIME_GATE_CHECK.md`
- `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_EXECUTION_RETRY_01/90_CLOSEOUT.md`
- `docs/index/inbox/GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_EXECUTION_RETRY_01.md`

Note : le prompt signale deux chemins admin-trading non suivis hors scope. Le recontrole reel au moment de ce GO ne montre aucun fichier non suivi dans le worktree principal et confirme que les chemins admin-trading visibles ci-dessus sont suivis et propres. Ils restent hors scope et ne sont ni modifies, ni stages, ni supprimes.

## 8_VALIDATED_PLAN

Le plan valide pour ce GO est strictement documentaire :

- utiliser le schema MCP Policy comme source canonique ;
- produire un YAML draft dans un fichier Markdown ;
- produire un mapping JSON draft dans un fichier Markdown ;
- borner tous les exemples par `runtime_binding: false` ;
- declarer `unknown_capability: BLOCKED_BY_DEFAULT` ;
- declarer `NEVER_ALLOWED` sans approval path ;
- conserver les index globaux intacts ;
- stager uniquement le dossier du chantier courant et son inbox locale.

## 9_SELECTED_SOLUTION

Solution retenue : brouillon policy-as-documentation.

Le YAML et le JSON mapping sont des artefacts de specification. Ils peuvent guider un futur validator ou gateway, mais ne sont pas installes, charges, executes, importes, parses ou connectes a un runtime dans ce GO.

## 12_INVARIANTS

- Documentation seulement.
- Aucun runtime.
- Aucun trade.
- Aucun sudo.
- Aucun secret.
- Aucun shell libre.
- Aucun merge.
- Aucun push force.
- Aucun cleanup de branche.
- Aucun auto-fix.
- Ne jamais utiliser `git add -A`.
- Stager uniquement `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01/` et `docs/index/inbox/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01.md`.
- Ne pas modifier `docs/index/GO_INDEX.md`.
- Ne pas modifier `docs/index/ACTIVE_STREAMS.md`.
- Ne pas modifier `docs/index/REPRISE.md`.
- Ne pas modifier `docs/index/BRANCH_STATE.md`.
- Ne pas modifier `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md`.
- Toute capability inconnue ou non definie explicitement est `BLOCKED_BY_DEFAULT`.
- `NEVER_ALLOWED` n'a aucun chemin d'approbation.

## 13_ESTABLISHED

- `GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01` est valide en `PASS_DOC_ONLY` au commit `fa7558f2`.
- La chaine canonique etablie est : MCP Boundary -> Human Review Gates -> Trace/Evals Profile -> MCP Policy Schema.
- Les classes canoniques sont `READ_ONLY`, `READ_SANITIZED`, `WRITE_GATED`, `RUNTIME_GATED`, `HUMAN_APPROVAL_REQUIRED`, `BLOCKED_BY_DEFAULT`, `NEVER_ALLOWED`.
- Les gates humains separent docs, index globaux, Git push, merge, branch delete, runtime, Ollama install, model pull, service restart, secret redaction, trade, MCP write, remote exec et database mutation.
- Les traces `TRACE_*` et evals `EVAL_*` sont des obligations documentaires avant verdict.

## 14_HYPOTHESIS

- Un futur validator lira une representation YAML/JSON equivalente, mais ce GO ne choisit pas encore parser, langage, runtime, stockage ou gateway.
- Les noms de champs du draft sont volontairement stables pour minimiser la friction de conversion ulterieure.
- Les capabilities Ollama Lab restent lab/local et non production.

## 15_REMAINING_GAP

- Pas de validator statique.
- Pas de schema formel JSON Schema.
- Pas de policy runtime.
- Pas de trace store.
- Pas de gateway MCP branchee sur cette policy.
- Les chemins admin-trading signales hors scope restent a ignorer dans tout prochain staging ; `git add -A` reste interdit.

## 16_TODO

- Creer les 12 fichiers chantier.
- Creer l'inbox locale.
- Verifier que les index globaux ne sont pas modifies.
- Verifier que le draft ne contient aucun script executable.
- Committer uniquement les livrables du chantier courant.

## 17_RESUME_POINT

Reprise depuis `GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01` valide `PASS_DOC_ONLY`.

Le point de vigilance operationnel est le staging borne : ne pas utiliser `git add -A` et ne pas inclure de chemins admin-trading hors scope.

## 18_TO_DOCUMENT

- Principes YAML policy.
- Draft YAML documentaire complet.
- Mapping JSON documentaire.
- Entrees capabilities par classe.
- Bindings gate/trace/eval.
- Bindings strict workers.
- Bindings Ollama Lab.
- Regles `NEVER_ALLOWED` et `BLOCKED_BY_DEFAULT`.
- Checklist de validation documentaire.
- Exigences futures d'un validator, sans implementation.

## 19_TO_REMEMBER

Le draft YAML/JSON MCP Policy est une specification, pas une policy active. Toute action absente du draft est bloquee par defaut, et toute action `NEVER_ALLOWED` reste sans approval path dans la frontiere MCP.

## RISKS

- À qualifier.
