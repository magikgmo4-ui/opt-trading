---
doc_id: GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01_50_GAPS_AND_ADJUSTMENTS
doc_type: chantier/gaps
repo: opt-trading
machine: cursor-ai
go_id: GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01
status: active
scope: doc-only
run_date: 2026-05-09
links:
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01/30_CLAUDE_OUTPUT_CAPTURE.md
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01/40_P0_P1_P2_RESULTS.md
---

# 50_GAPS_AND_ADJUSTMENTS

## Gaps observés lors du run

### GAP-01 — Live Artifact HTML non généré

- description : Le prompt cible la création d'un "Live Artifact" HTML interactif dans Claude Cowork. Dans ce run, l'exécution s'est faite en mode session textuelle Claude Cowork sans génération d'un artefact HTML distinct.
- impact : Le rendu visuel cockpit dynamique (sections cliquables, filtrables) n'est pas disponible dans ce run.
- bloquant pour le PASS : Non — le prompt reste exécutable et la sortie P0/P1/P2 est produite.
- ajustement proposé : Pour un run complet avec Live Artifact HTML, utiliser la commande "Créer un Live Artifact nommé OPT_TRADING_ATTENTION_CENTER_01" dans une interface Claude Cowork avec support artefact activé.
- classification : GAP MINEUR — non bloquant

### GAP-02 — Connecteur GitHub API non activé

- description : Le prompt liste GitHub PR / branches / issues comme source P0 si le connecteur est disponible. Dans ce run, le connecteur GitHub API n'est pas activé. Les états PR sont lus depuis le git local et les docs uniquement.
- impact : Les PR ouvertes sur GitHub (si différentes de l'état git local) ne sont pas visibles directement. La liste des PRs mergées est issue de `git log --oneline` et non de l'API GitHub.
- bloquant pour le PASS : Non — le git local est une source autorisée et suffisante.
- ajustement proposé : Activer le connecteur GitHub MCP pour enrichir BRANCHES_AND_PRS avec les vraies PR ouvertes, labels, reviewers.
- classification : GAP MINEUR — non bloquant

### GAP-03 — Snapshot repo read-only dédié non configuré

- description : La matrice `30_READONLY_SOURCES_MATRIX.md` recommande un snapshot `repo-readonly/opt-trading-snapshot` comme surface préférée. Ce snapshot n'est pas configuré. Le repo actif est utilisé en lecture seule par convention.
- impact : Risque théorique d'incohérence si le repo actif change pendant le run. En pratique, aucune modification n'a eu lieu pendant le run.
- bloquant pour le PASS : Non.
- ajustement proposé : Si le workflow évolue vers une exécution fréquente, configurer un snapshot dédié.
- classification : GAP INFORMATIF — non bloquant

### GAP-04 — `reports/` non vérifié

- description : Le prompt mentionne `reports/` comme source P1 pour les rapports exportés. Ce répertoire n'a pas été confirmé présent ou vide dans ce run.
- impact : Possibles rapports antérieurs non consultés.
- bloquant pour le PASS : Non — le run ne dépend pas de rapports antérieurs.
- ajustement proposé : Vérifier `ls reports/` en début de run futur.
- classification : GAP MINEUR — non bloquant

### GAP-05 — Machine states tous ETAT_DECLARE (hors cursor-ai)

- description : Aucun log technique récent ni commande live n'est disponible pour admin-trading, student, db-layer, android/termux/tmux. Tous sont classés ETAT_DECLARE. C'est conforme aux règles `50_MACHINE_STATE_RULES.md`, mais cela signifie que la vue MULTI_MACHINE_VIEW reste limitée.
- impact : Le cockpit ne peut pas détecter un problème runtime sur ces machines sans source technique directe.
- bloquant pour le PASS : Non — la règle est de classifier correctement, pas d'avoir des ETAT_VERIFIE sur toutes les machines.
- ajustement proposé : Pour enrichir MULTI_MACHINE_VIEW, brancher un connecteur runtime ou demander un rapport machine explicite en début de run.
- classification : GAP STRUCTUREL — attendu, non bloquant

---

## Évaluation globale des gaps

| Gap | Sévérité | Bloquant PASS ? |
| --- | --- | --- |
| GAP-01 Live Artifact HTML | Mineur | Non |
| GAP-02 GitHub API | Mineur | Non |
| GAP-03 Snapshot dédié | Informatif | Non |
| GAP-04 reports/ non vérifié | Mineur | Non |
| GAP-05 Machine states ETAT_DECLARE | Structurel attendu | Non |

**Aucun gap bloqueur détecté.**

---

## Ajustements recommandés pour les runs suivants

1. Lancer le run dans une interface Claude Cowork avec support artefact HTML activé pour produire le cockpit visuel.
2. Activer le connecteur GitHub MCP pour enrichir la vue BRANCHES_AND_PRS.
3. Vérifier `ls reports/` en début de run.
4. Envisager un snapshot repo read-only dédié si la fréquence des runs augmente.
5. Pour MULTI_MACHINE_VIEW enrichie, demander un rapport machine ou un log daté avant le run.

## RISKS

- À qualifier.
