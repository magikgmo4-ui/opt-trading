# 30_JSON_EXPORT_COMMAND_PLAN

## 1_MASTER_TARGET

Definir le plan d'execution du premier export JSON reel du WHY runtime graph en restant strictement read-only.

## WHY

Le repo doit d'abord prouver qu'un export borne peut etre produit et verifie sans mutation runtime, sans render et sans elargir le scope aux couches differees.

## 7_CANONICAL_STATE

Preconditions constatees :

- `origin/sot/mainline` contient `PR #498` ;
- la branche cible `go/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_JSON_EXPORT_REAL_01` existe localement comme ref ;
- le worktree courant ne peut pas encore switcher proprement sur cette base a cause de fichiers non suivis qui seraient ecrases par le fast-forward.

## 8_EXECUTION_PLAN

Plan minimal retenu :

1. Resoudre le chevauchement local entre fichiers non suivis et fichiers maintenant suivis upstream, sans perte d'information.
2. Basculer sur `go/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_JSON_EXPORT_REAL_01` une fois la base locale nettoyee.
3. Lire les surfaces documentaires amont retenues.
4. Produire un unique fichier JSON borne, par exemple `artifacts/why-runtime-graph/minimal/runtime_graph_minimal_v1.json`.
5. Verifier l'artefact avec des checks texte simples et un diff stable.

## 9_COMMAND_SKETCH

Commande cible a valider une fois le worktree alignable :

```text
git switch go/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_JSON_EXPORT_REAL_01
<commande read-only d'export documentaire -> JSON>
git diff -- artifacts/why-runtime-graph/minimal/runtime_graph_minimal_v1.json
```

Le choix de la commande d'export reste volontairement non force ici tant qu'aucun binaire, script ou generateur canonique n'est encore etabli sur la base mergee.

## 10_ACCEPTED_FALLBACK

Si aucun generateur canonique n'existe encore apres alignement de la base, le premier livrable executable acceptable reste :

- un script read-only local au GO ;
- un unique JSON minimal ;
- aucune mutation hors dossier d'artefacts ;
- aucune dependance a un render graphique.

## 12_INVARIANTS

- Pas de `git pull` destructif.
- Pas de stash implicite de fichiers utilisateur.
- Pas de rendu graphique.
- Pas de mutation runtime ou CI.
- Pas d'index global additionnel.

## 17_RESUME_POINT

Le prochain passage executable doit d'abord remettre le worktree sur la base mergee de `PR #498`, puis produire un seul JSON borne en lecture seule.
