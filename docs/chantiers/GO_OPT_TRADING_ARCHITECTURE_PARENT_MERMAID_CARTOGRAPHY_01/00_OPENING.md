# GO_OPT_TRADING_ARCHITECTURE_PARENT_MERMAID_CARTOGRAPHY_01 — Ouverture chantier parent Mermaid Architecture

## GO_STRUCTURAL_ROLE

GO_PARENT_ATTACHED_TO_MASTER_PROJECT_PLAN

## 1_MASTER_TARGET

Produire une cartographie Mermaid end-to-end, validée, lisible et exportable du dépôt logiciel, fondée sur un Evidence Pack réel, avec livrable final :

```text
docs/architecture/mermaid/990_architecture_final.mmd
```

## 2_INITIAL_PROJECT_DOC

Document initial figé :

```text
docs/architecture/PLAN_CARTOGRAPHIE_MERMAID.md
```

Ce document contient la méthode complète : Evidence Pack, pipeline, Kanban, prompts par passe, fichiers `.mmd`, validation et export.

## 3_INITIAL_NEED

Cartographier l’intégralité du dépôt en Mermaid de manière incrémentale, sans dépasser les limites de contexte et sans inventer l’architecture.

## 4_MASTER_PROJECT_PLAN

Pipeline validé :

1. Passe 0 — Accès repo et Evidence Pack.
2. Passe 1 — Initialisation et Kanban.
3. Passe 2 — Core, configuration, infrastructure interne.
4. Passe 3 — Données, flux métier, stratégie, pricing.
5. Passe 4 — API, interfaces, workers, CLI, exécution.
6. Passe 5 — Assemblage et résolution des conflits.
7. Passe 6 — Design, thématisation et optimisation graphique.
8. Produit final — `990_architecture_final.mmd`.

## 5_GO_PLAN

Ouvrir le chantier parent, installer la méthode dans le repo, préparer le script d’extraction et laisser l’IA/IDE produire l’Evidence Pack réel depuis la machine locale.

## 6_FINAL_TARGET

Pour cette ouverture :

```text
docs/architecture/PLAN_CARTOGRAPHIE_MERMAID.md
scripts/make-architecture-evidence.sh
.vscode/tasks.json
docs/architecture/evidence/08_notes_open_questions.md
docs/architecture/evidence/.gitkeep
docs/architecture/mermaid/.gitkeep
docs/chantiers/GO_OPT_TRADING_ARCHITECTURE_PARENT_MERMAID_CARTOGRAPHY_01/00_OPENING.md
docs/index/inbox/GO_OPT_TRADING_ARCHITECTURE_PARENT_MERMAID_CARTOGRAPHY_01.md
```

## 7_CANONICAL_STATE

Plan validé. Chantier parent ouvert. Le repo ne doit pas encore contenir les Mermaid détaillés tant que l’Evidence Pack réel n’a pas été généré localement.

## 8_VALIDATED_PLAN

- Installer le document de méthode.
- Installer le script `scripts/make-architecture-evidence.sh`.
- Installer la tâche VS Code optionnelle.
- Préparer les dossiers `evidence/` et `mermaid/`.
- Lancer l’extraction localement depuis l’IDE.
- Utiliser les prompts par passe du document initial.

## 9_SELECTED_SOLUTION

Méthode Evidence Pack first : toute relation Mermaid doit venir de l’arborescence, des manifests, des imports, des entrypoints ou de la documentation.

## 10_SELECTED_SETUP

Structure cible :

```text
docs/architecture/
  PLAN_CARTOGRAPHIE_MERMAID.md
  evidence/
  mermaid/
scripts/make-architecture-evidence.sh
.vscode/tasks.json
docs/chantiers/GO_OPT_TRADING_ARCHITECTURE_PARENT_MERMAID_CARTOGRAPHY_01/
docs/index/inbox/GO_OPT_TRADING_ARCHITECTURE_PARENT_MERMAID_CARTOGRAPHY_01.md
```

## 11_KEY_DECISIONS

- Ne pas générer de diagramme détaillé sans Evidence Pack réel.
- Ne pas modifier les index globaux pour cette ouverture.
- Versionner la méthode, le script, la tâche IDE et l’entrée inbox.
- Utiliser des identifiants Mermaid stables en snake_case.

## 12_INVARIANTS

- Ne jamais inventer un fichier, une dépendance ou un flux.
- Les inconnues doivent être marquées `TODO` ou `UNKNOWN`.
- Les relations incertaines doivent rester pointillées et libellées `probable`.
- Le fichier final de référence reste `docs/architecture/mermaid/990_architecture_final.mmd`.
- Les index globaux ne changent pas sans changement réel de master target ou d’horizon.

## 13_ESTABLISHED

Le plan de cartographie Mermaid est validé et prêt à être appliqué localement.

## 14_HYPOTHESIS

Aucune hypothèse d’architecture repo n’est validée tant que l’Evidence Pack local n’est pas généré.

## 15_REMAINING_GAP

- Générer l’Evidence Pack réel dans le repo.
- Produire `000_plan.mmd` à partir de `00_repo_identity.md`, `01_tree.txt`, `02_manifests.md`.
- Produire ensuite les Mermaid partiels par passe.
- Fusionner et valider la syntaxe Mermaid.

## 16_TODO

```bash
git switch -c go/GO_OPT_TRADING_ARCHITECTURE_PARENT_MERMAID_CARTOGRAPHY_01
git apply GO_OPT_TRADING_ARCHITECTURE_PARENT_MERMAID_CARTOGRAPHY_01.patch
chmod +x scripts/make-architecture-evidence.sh
./scripts/make-architecture-evidence.sh
git status --short
git add docs/architecture scripts .vscode docs/chantiers/GO_OPT_TRADING_ARCHITECTURE_PARENT_MERMAID_CARTOGRAPHY_01 docs/index/inbox/GO_OPT_TRADING_ARCHITECTURE_PARENT_MERMAID_CARTOGRAPHY_01.md
git commit -m "docs: open mermaid architecture cartography chantier"
git push -u origin go/GO_OPT_TRADING_ARCHITECTURE_PARENT_MERMAID_CARTOGRAPHY_01
```

## 17_RESUME_POINT

Reprendre après application du patch à l’étape : lancer `./scripts/make-architecture-evidence.sh`, puis générer `docs/architecture/mermaid/000_plan.mmd` avec les fichiers :

```text
docs/architecture/evidence/00_repo_identity.md
docs/architecture/evidence/01_tree.txt
docs/architecture/evidence/02_manifests.md
```

## 18_TO_DOCUMENT

TAGS :

- `GO_STRUCTURAL_ROLE`
- `1_MASTER_TARGET`
- `2_INITIAL_PROJECT_DOC`
- `4_MASTER_PROJECT_PLAN`
- `7_CANONICAL_STATE`
- `16_TODO`
- `17_RESUME_POINT`

## 19_TO_REMEMBER

### MEM_CANDIDATE

- Pour les chantiers Mermaid architecture, utiliser une méthode Evidence Pack first avant toute cartographie détaillée.
- Le livrable final canonique est `docs/architecture/mermaid/990_architecture_final.mmd`.

### SAVE_MEMORY

NO_MEMORY par défaut sauf demande explicite.
