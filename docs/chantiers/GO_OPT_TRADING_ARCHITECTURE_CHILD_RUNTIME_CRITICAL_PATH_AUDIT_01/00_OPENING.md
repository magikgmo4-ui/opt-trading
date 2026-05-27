# GO_OPT_TRADING_ARCHITECTURE_CHILD_RUNTIME_CRITICAL_PATH_AUDIT_01 - Ouverture child audit runtime critical path

## GO_STRUCTURAL_ROLE

GO_CHILD_ATTACHED_TO_ARCHITECTURE_AUDIT

## 1_MASTER_TARGET

Isoler et auditer le chemin runtime trading critique depuis l'alerte TradingView jusqu'a la persistence et aux surfaces perf.

## 2_INITIAL_PROJECT_DOC

Sources de travail:

```text
docs/architecture/mermaid/readable/060_trading_runtime_critical_path.preview.md
docs/architecture/mermaid/readable/010_core_runtime.preview.md
docs/architecture/mermaid/readable/020_data_strategy_execution.preview.md
docs/architecture/mermaid/readable/030_interfaces_entrypoints.preview.md
docs/architecture/mermaid/990_architecture_final.mmd
docs/chantiers/GO_OPT_TRADING_ARCHITECTURE_CHILD_AUDIT_FROM_MERMAID_01/20_ARCHITECTURE_AUDIT.md
docs/chantiers/GO_OPT_TRADING_ARCHITECTURE_CHILD_AUDIT_FROM_MERMAID_01/90_CLOSEOUT.md
```

## 3_INITIAL_NEED

Verifier la chaine critique `TradingView -> webhook -> risk/guards -> execution -> state/perf`, identifier les zones prouvees, les liaisons probables et les risques de couplage sur les entrypoints centraux.

## 4_MASTER_PROJECT_PLAN

1. Reprendre la vue readable du critical path.
2. Distinguer ingress, decision/risk, execution, persistence et exposition perf.
3. Identifier les liens prouves et les liens `probable` restant a confirmer.
4. Prioriser les risques runtime et proposer des suites ciblees.

## 5_GO_PLAN

Produire un audit documentaire focalise sur le runtime trading critique, sans modifier la cartographie Mermaid existante.

## 6_FINAL_TARGET

```text
docs/chantiers/GO_OPT_TRADING_ARCHITECTURE_CHILD_RUNTIME_CRITICAL_PATH_AUDIT_01/00_OPENING.md
docs/chantiers/GO_OPT_TRADING_ARCHITECTURE_CHILD_RUNTIME_CRITICAL_PATH_AUDIT_01/20_RUNTIME_CRITICAL_PATH_AUDIT.md
docs/chantiers/GO_OPT_TRADING_ARCHITECTURE_CHILD_RUNTIME_CRITICAL_PATH_AUDIT_01/90_CLOSEOUT.md
docs/chantiers/GO_OPT_TRADING_ARCHITECTURE_CHILD_RUNTIME_CRITICAL_PATH_AUDIT_01/FILE_SCOPE.txt
docs/index/inbox/GO_OPT_TRADING_ARCHITECTURE_CHILD_RUNTIME_CRITICAL_PATH_AUDIT_01.md
```

## 12_INVARIANTS

- Ne pas comparer avec `sot/mainline`.
- Ne pas modifier le parent Mermaid.
- Ne pas inventer de composants hors Mermaid.
- Garder les liens `probable` explicites.

## 17_RESUME_POINT

Reprendre sur `20_RUNTIME_CRITICAL_PATH_AUDIT.md` pour une lecture ciblee du chemin runtime trading.
