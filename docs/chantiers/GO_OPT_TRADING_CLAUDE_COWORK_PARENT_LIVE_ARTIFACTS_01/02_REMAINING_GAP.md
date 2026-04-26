---
doc_id: OPT_TRADING_CLAUDE_COWORK_LIVE_ARTIFACTS_PARENT_01_REMAINING_GAP
doc_type: remaining_gap
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01
status: open
lifecycle_stage: gap_analysis
topic_keys:
  - claude_cowork
  - live_artifacts
  - security
  - connectors
  - attention_center
  - remaining_gap
surface: docs/chantiers
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "Section 17_RESUME_POINT"
updated_at: 2026-04-26
links:
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01/01_FULL_RESPONSE_CAPTURE.md
---

# Remaining Gap — Claude Cowork Live Artifacts

## 1_MASTER_TARGET

Identifier ce qui manque avant de transformer l'idee `OPT_TRADING_ATTENTION_CENTER_01` en artefact Claude Cowork fiable, securise et compatible avec le canon `opt-trading`.

## 7_CANONICAL_STATE

Etat valide :

- Le Live Artifact doit rester une vue dynamique.
- Le repo/docs/Git reste la source de verite.
- Le premier artefact vise est `OPT_TRADING_ATTENTION_CENTER_01`.
- L'ecriture doit rester interdite par defaut.
- Le chantier parent est ouvert sur branche dediee.

## 15_REMAINING_GAP

### GAP_01 — Sources exactes autorisees

ETABLI :

Le Live Artifact devra lire des sources connectees ou locales.

HYPOTHESE :

Les sources utiles peuvent inclure :

```text
GitHub
Google Drive
Calendar
Asana / ClickUp
fichiers locaux
snapshot repo read-only
```

GAP :

La liste exacte des sources n'est pas encore validee.

TODO :

Creer une matrice d'autorisation :

| Source | Lecture | Ecriture | Statut cible |
| --- | --- | --- | --- |
| repo snapshot read-only | oui | non | prioritaire |
| GitHub PR / branches | oui | non par defaut | prioritaire |
| Google Drive docs | a valider | non par defaut | secondaire |
| Calendar | a valider | non par defaut | optionnel |
| Asana/ClickUp | a valider | non par defaut | optionnel |
| fichiers sensibles | non | non | interdit |

### GAP_02 — Dossier Claude dedie

ETABLI :

Il faut eviter de donner a Claude un acces large au disque.

Setup cible :

```text
C:\Users\ghost\claude-workspace\
  live-artifacts/
  snapshots/
  exported-prompts/
  repo-readonly/
  reports/
```

GAP :

Ce dossier n'est pas encore cree ni peuple.

TODO :

Preparer un script Windows PowerShell qui cree cette structure et, si valide, copie les surfaces read-only utiles.

### GAP_03 — Snapshot repo read-only

ETABLI :

Le repo actif ne doit pas etre la premiere surface donnee a Claude.

HYPOTHESE :

Un snapshot partiel est plus sur :

```text
C:\Users\ghost\claude-workspace\repo-readonly\opt-trading-snapshot
```

GAP :

La methode de snapshot n'est pas encore definie.

TODO :

Choisir entre :

| Option | Avantage | Risque |
| --- | --- | --- |
| copie simple des docs | simple | peut devenir stale |
| archive zip | transportable | refresh manuel |
| git worktree read-only | plus proche du reel | plus complexe |
| export minimal `docs/index + docs/chantiers + governance` | securise | manque peut-etre des sources |

### GAP_04 — Connecteur GitHub dans Claude

ETABLI :

Le workflow profite fortement de GitHub pour PR, branches et issues.

GAP :

On ne sait pas encore si le GitHub connecte dans Claude Cowork aura la granularite suffisante et si ses permissions peuvent rester strictement controlees.

TODO :

Valider dans Claude :

```text
- GitHub connecte ?
- acces repo opt-trading ?
- lecture PR/branches/issues ?
- ecriture possible ? si oui, la desactiver ou la traiter comme interdite par convention
```

### GAP_05 — Regle read-only executable

ETABLI :

Read-only par defaut est un invariant.

GAP :

Il manque une formulation executable et repetable pour Claude Cowork.

TODO :

Ajouter dans chaque prompt Live Artifact :

```text
MODE READ-ONLY STRICT
Tu peux lire et synthetiser.
Tu ne modifies aucun fichier, aucune branche, aucune PR, aucun document Drive, aucun calendrier, aucune tache.
Toute action d'ecriture doit etre proposee comme TODO et attendre un GO explicite.
```

### GAP_06 — Scoring d'attention

ETABLI :

Le dashboard doit classer les elements par priorite.

GAP :

Les criteres P0/P1/P2 ne sont pas encore figes.

Proposition :

| Niveau | Definition | Exemple |
| --- | --- | --- |
| P0 | Action bloquante ou risque de divergence canonique | PR ouverte qui bloque merge, branche dediee sans indexation |
| P1 | Verification requise avant travail suivant | GO actif sans `SESSION_REPRISE.txt` |
| P2 | Surveillance non bloquante | doc recent modifie, branch stale reference |

TODO :

Valider ce scoring dans un prochain document ou prompt.

### GAP_07 — Mapping GO_INDEX / BRANCH_STATE / REPRISE

ETABLI :

Les trois surfaces ne jouent pas le meme role.

GAP :

Le Live Artifact doit comprendre la hierarchie :

```text
GO_INDEX = verite de liste locale
BRANCH_STATE = surface branches seulement
REPRISE = pilotage operationnel
```

TODO :

Ajouter une section de regles de lecture dans le prompt Claude.

### GAP_08 — Multi-machines

ETABLI :

Le workflow est multi-machine.

Machines :

```text
admin-trading
student
db-layer
cursor-ai
android / termux / tmux
```

GAP :

Le Live Artifact ne doit pas presenter un etat machine comme reel sans preuve de commande.

TODO :

Marquer chaque etat machine avec une colonne :

```text
ETAT_DECLARE / ETAT_VERIFIE / HYPOTHESE
```

### GAP_09 — Relation OpenClaw

ETABLI :

OpenClaw reste candidat pour l'orchestration locale / runtime.

GAP :

Le Live Artifact ne doit pas remplacer OpenClaw.

TODO :

Documenter la frontiere :

```text
Claude Live Artifact = supervision / lecture / dashboard
OpenClaw = execution locale / orchestration agents / tmux / runtime
```

### GAP_10 — Export et journalisation

ETABLI :

Le workflow exige des traces et reprises.

GAP :

On ne sait pas encore comment exporter l'etat d'un Live Artifact vers le repo.

TODO :

Definir un format exportable :

```text
reports/YYYY-MM-DD_ATTENTION_CENTER_SUMMARY.md
```

Puis seulement apres validation, decider si cet export devient une entree documentaire repo.

### GAP_11 — Prompt canonique final

ETABLI :

Un prompt de creation a ete propose dans la capture.

GAP :

Il n'est pas encore durci en version executable finale.

TODO :

Produire :

```text
docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01/03_CLAUDE_COWORK_PROMPT_ATTENTION_CENTER.md
```

### GAP_12 — Indexation canonique du nouveau GO

ETABLI :

Le chantier parent et la branche existent.

GAP :

`docs/index/GO_INDEX.md` n'a pas encore ete modifie dans ce passage, car son contenu lu via connecteur est long et tronque cote affichage, donc une mise a jour directe par remplacement complet serait risquee.

TODO :

Traiter l'indexation dans un passage dedie avec repo local complet ou outil permettant une modification partielle fiable.

## 16_TODO — Priorisation

| Priorite | Action |
| --- | --- |
| P0 | Produire le prompt final `03_CLAUDE_COWORK_PROMPT_ATTENTION_CENTER.md` |
| P0 | Valider sources autorisees et mode read-only |
| P1 | Creer script de dossier Claude workspace |
| P1 | Definir scoring P0/P1/P2 |
| P1 | Definir export rapport |
| P2 | Cadrer artefacts secondaires `GOVERNANCE_DASHBOARD` et `OPENCLAW_ORCHESTRATOR_PREP` |

## 17_RESUME_POINT

Reprise operationnelle :

```text
Reprendre depuis ce fichier.
Prochain livrable : 03_CLAUDE_COWORK_PROMPT_ATTENTION_CENTER.md
Contrainte : read-only strict, sources explicites, aucune ecriture sans GO.
NEXT_GO : GO_OPT_TRADING_CLAUDE_COWORK_CHILD_REMAINING_GAP_01
```
