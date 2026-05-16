---
doc_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01_PRINCIPLES
doc_type: policy_yaml_principles
status: draft_doc_only
module: governance_openclaw_mcp_policy_yaml_draft
go_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01
runtime_binding: false
validator_created: false
---

# 01_POLICY_YAML_PRINCIPLES

## 1_MASTER_TARGET

Faire du draft YAML/JSON un contrat documentaire clair entre OpenClaw Governor, MCP, Codex, strict workers et Ollama Lab.

## 2_INITIAL_PROJECT_DOC

Source principale : `GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01`.

Sources liees :

- MCP Boundary : deny-by-default, no shell libre, no sudo, no secret, no trade.
- Human Gates : approval explicite, preuves, rollback, verdicts.
- Trace/Evals : trace before verdict, eval before promotion, no-secret evidence.

## 3_INITIAL_NEED

Eviter qu'un brouillon YAML soit confondu avec une policy runtime. Le document doit rester lisible, stable et transposable, mais sans effet actif.

## 4_MASTER_PROJECT_PLAN

Principes a appliquer dans chaque section du draft :

1. declarer le statut documentaire ;
2. lister les classes canoniques ;
3. lier chaque capability a une classe ;
4. lier chaque action sensible a un gate ;
5. lier chaque decision a une trace et un eval ;
6. bloquer tout champ ou action non defini ;
7. refuser les secrets, le sudo, le shell libre et le trade hors GO dedie.

## 6_FINAL_TARGET

Un draft YAML/JSON suffisamment structure pour une future traduction machine-readable, sans parser, sans validator et sans runtime.

## 7_CANONICAL_STATE

Etat canonique repris :

- `READ_ONLY` et `READ_SANITIZED` peuvent etre autorises seulement si bornes, sanitises et traces.
- `WRITE_GATED`, `RUNTIME_GATED` et `HUMAN_APPROVAL_REQUIRED` sont bloques par defaut jusqu'au gate applicable.
- `BLOCKED_BY_DEFAULT` ferme toute capability inconnue ou incomplete.
- `NEVER_ALLOWED` n'a aucun chemin d'approbation dans MCP.

## 8_VALIDATED_PLAN

Le draft YAML doit contenir :

- `metadata`
- `policy_version`
- `default_policy`
- `capability_classes`
- `gates`
- `traces`
- `evals`
- `strict_worker_roles`
- `ollama_lab_policy`
- `governor_decision_rules`
- `never_allowed`
- `blocked_by_default`
- `examples`

## 9_SELECTED_SOLUTION

Utiliser une syntaxe YAML lisible dans un fichier Markdown, puis decrire le mapping JSON equivalent dans un second fichier Markdown.

Cette solution evite de creer un artefact `.yaml` ou `.json` qui pourrait etre charge par erreur par un runtime.

## 12_INVARIANTS

- Draft documentaire seulement.
- `runtime_binding: false`.
- `validator_created: false`.
- Deny-by-default.
- Explicit allow only.
- Capability inconnue = `BLOCKED_BY_DEFAULT`.
- `NEVER_ALLOWED` = aucun approval path.
- Gate obligatoire avant action sensible.
- Trace obligatoire pour action allowed, blocked ou failed.
- Eval obligatoire avant promotion.
- Aucun secret en input, output, trace, evidence ou policy.
- Aucune auto-approval.
- Aucun runtime binding.

## 13_ESTABLISHED

Principes etablis :

| Principe | Decision |
| --- | --- |
| Draft documentaire seulement | Le YAML/JSON est conserve dans Markdown et non charge. |
| Deny-by-default | Toute capability absente est `BLOCKED_BY_DEFAULT`. |
| Explicit allow only | Une capability doit avoir id, class, status, actors, gate, trace et eval. |
| NEVER_ALLOWED sans approval | Aucun `gate_id` ne peut promouvoir `NEVER_ALLOWED`. |
| Gate before sensitive action | Write, runtime, Git, Ollama, secret redaction et trade exigent gate. |
| Trace obligatoire | Chaque verdict cite une trace. |
| Eval before promotion | Aucune capability ne passe en runtime sans eval future. |
| No secret | Les valeurs secretes ne sont jamais stockees, exposees ou exportees. |
| No runtime binding | Le draft ne modifie aucune config active. |

## 14_HYPOTHESIS

- Les futurs parsers pourront accepter une representation YAML stricte derivee de ce fichier.
- Les futurs validators devront echouer ferme si un champ obligatoire manque.
- Les futurs gateways ne devront pas interpreter ce draft sans GO dedie.

## 15_REMAINING_GAP

- Pas de validation syntaxique YAML automatisee.
- Pas de representation JSON canonique dans un fichier `.json`.
- Pas de registry policy.
- Pas de policy middleware.

## 16_TODO

- Definir le draft YAML complet dans `02_POLICY_YAML_DRAFT.md`.
- Definir le mapping JSON conceptuel dans `03_POLICY_JSON_MAPPING_DRAFT.md`.
- Verifier que les sections restent doc-only.

## 17_RESUME_POINT

Lire ce fichier avant de copier un bloc YAML de ce chantier vers un futur GO. Sans GO validator/runtime explicite, le YAML reste inertiel et documentaire.

## 18_TO_DOCUMENT

Les futurs travaux devront documenter :

- schema JSON formel ;
- parser choisi ;
- regles de fail closed ;
- emplacement autorise des policies ;
- format de trace persistante ;
- separation dev/test/runtime.

## 19_TO_REMEMBER

Un fichier ressemblant a une policy n'est pas une policy active. La promotion vers runtime exige un GO distinct, un gate humain, des traces et des evals.
