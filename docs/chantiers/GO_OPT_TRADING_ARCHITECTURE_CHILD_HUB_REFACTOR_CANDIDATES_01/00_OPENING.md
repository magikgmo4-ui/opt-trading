# GO_OPT_TRADING_ARCHITECTURE_CHILD_HUB_REFACTOR_CANDIDATES_01 - Ouverture child hub refactor candidates

## GO_STRUCTURAL_ROLE

GO_CHILD_ATTACHED_TO_ARCHITECTURE_AUDIT

## 1_MASTER_TARGET

Transformer les constats d'audit architecture en candidats de refactor concrets, priorises et verifiables, sans refactorer le code ni modifier la cartographie Mermaid.

## 2_INITIAL_PROJECT_DOC

Sources de travail:

```text
docs/chantiers/GO_OPT_TRADING_ARCHITECTURE_CHILD_AUDIT_FROM_MERMAID_01/20_ARCHITECTURE_AUDIT.md
docs/chantiers/GO_OPT_TRADING_ARCHITECTURE_CHILD_AUDIT_FROM_MERMAID_01/90_CLOSEOUT.md
docs/chantiers/GO_OPT_TRADING_ARCHITECTURE_CHILD_RUNTIME_CRITICAL_PATH_AUDIT_01/20_RUNTIME_CRITICAL_PATH_AUDIT.md
docs/chantiers/GO_OPT_TRADING_ARCHITECTURE_CHILD_RUNTIME_CRITICAL_PATH_AUDIT_01/90_CLOSEOUT.md
docs/chantiers/GO_OPT_TRADING_ARCHITECTURE_CHILD_REGISTRY_OWNERSHIP_AUDIT_01/20_REGISTRY_OWNERSHIP_AUDIT.md
docs/chantiers/GO_OPT_TRADING_ARCHITECTURE_CHILD_REGISTRY_OWNERSHIP_AUDIT_01/90_CLOSEOUT.md
docs/architecture/mermaid/readable/000_index.preview.md
```

## 3_INITIAL_NEED

Identifier les hubs critiques, les responsabilites melangees, les risques de regression et les decoupes de refactor les plus sures, avec un ordre de priorite et des NEXT_GO par hub.

## 4_MASTER_PROJECT_PLAN

1. Reprendre les hubs critiques identifies par l'audit parent.
2. Croiser avec les audits runtime et registry ownership.
3. Distinguer refactor candidates immediats, differes et a ne pas traiter sans preuve supplementaire.
4. Produire un plan priorise de children de refactor ou de preuve preparatoire.

## 5_GO_PLAN

Produire un rapport de candidats refactor hubs uniquement, sans changement code ni mise a jour Mermaid.

## 6_FINAL_TARGET

```text
docs/chantiers/GO_OPT_TRADING_ARCHITECTURE_CHILD_HUB_REFACTOR_CANDIDATES_01/00_OPENING.md
docs/chantiers/GO_OPT_TRADING_ARCHITECTURE_CHILD_HUB_REFACTOR_CANDIDATES_01/20_HUB_REFACTOR_CANDIDATES.md
docs/chantiers/GO_OPT_TRADING_ARCHITECTURE_CHILD_HUB_REFACTOR_CANDIDATES_01/90_CLOSEOUT.md
docs/chantiers/GO_OPT_TRADING_ARCHITECTURE_CHILD_HUB_REFACTOR_CANDIDATES_01/FILE_SCOPE.txt
docs/index/inbox/GO_OPT_TRADING_ARCHITECTURE_CHILD_HUB_REFACTOR_CANDIDATES_01.md
```

## 12_INVARIANTS

- Ne pas modifier la cartographie Mermaid.
- Ne pas comparer avec `sot/mainline`.
- Ne pas refactorer le code.
- Produire seulement une priorisation verifiable.

## 17_RESUME_POINT

Reprendre sur `20_HUB_REFACTOR_CANDIDATES.md` pour transformer l'audit en plan de refactor priorise.
