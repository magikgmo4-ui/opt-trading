---
doc_id: OPT_TRADING_CLAUDE_COWORK_LIVE_ARTIFACTS_PARENT_01_FULL_RESPONSE_CAPTURE
doc_type: response_capture
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01
status: open
lifecycle_stage: cadrage_parent
topic_keys:
  - claude_cowork
  - live_artifacts
  - attention_center
  - governance_dashboard
  - openclaw_orchestrator
surface: docs/chantiers
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "Section 17_RESUME_POINT"
updated_at: 2026-04-26
links:
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01/02_REMAINING_GAP.md
---

# Capture complete — Live Artifacts Claude Cowork adaptes au workflow opt-trading

## 1_MASTER_TARGET

Un Live Artifact dans Claude Cowork doit etre traite comme un poste de pilotage dynamique, pas comme une documentation canonique.

Role optimal dans le workflow :

```text
Repo / docs / commits / closeouts = verite canonique
Live Artifact Claude = vue dynamique de pilotage
Claude Cowork = operateur / assistant d'execution
OpenClaw = orchestrateur local / agent runtime
GitHub / Drive / fichiers locaux = sources consultees
```

## 7_CANONICAL_STATE — Interpretation adaptee au setup

### Ce que ce n'est pas

Un Live Artifact ne doit pas devenir :

| Mauvais usage | Pourquoi |
| --- | --- |
| Source officielle du projet | Trop dynamique, peut refleter une vue partielle |
| Remplacant de `docs/index/GO_INDEX.md` | Risque de divergence avec le repo |
| Remplacant des closeouts | Les closeouts doivent rester versionnes |
| Remplacant des commits Git | Pas de preuve durable suffisante |
| Endroit ou Claude decide seul quoi modifier | Trop dangereux sans garde-fous |

### Ce que ca doit etre

Un Live Artifact doit devenir :

| Bon usage | Role |
| --- | --- |
| Dashboard operateur | Montrer l'etat courant |
| Centre d'attention | Identifier ce qui merite action |
| Vue de reprise | Afficher les prochains GO possibles |
| Panneau multi-sources | Croiser GitHub, Drive, fichiers locaux, calendrier |
| Surface de lecture | Aider a decider, pas decider a la place de l'operateur |
| Interface de coordination | Claude / OpenClaw / GitHub / Drive / machines |

## 9_SELECTED_SOLUTION

Modele recommande : `Attention Center`.

Premier Live Artifact utile :

```text
OPT_TRADING_ATTENTION_CENTER_01
```

Objectif : repondre a une seule question operationnelle :

```text
Qu'est-ce qui necessite mon attention maintenant, sans rouvrir 15 conversations ou fichiers ?
```

## Structure recommandee du Live Artifact

### 1. Vue GO_XXXX actifs

Sources probables :

```text
docs/index/GO_INDEX.md
docs/index/REPRISE.md
docs/index/GO_CLOSED_INDEX.md
docs/chantiers/*/
```

Champs d'affichage :

| Champ | Utilite |
| --- | --- |
| GO_ID | Identifiant canonique |
| Statut | OPEN / ACTIVE / BLOCKED / CLOSED |
| Branche liee | Si chantier avec branche dediee |
| Dernier checkpoint | Dernier etat etabli |
| Prochaine action | NEXT_GO / TODO |
| Risque | faible / moyen / eleve |
| Source | fichier exact consulte |

Regle :

```text
Le Live Artifact peut afficher les GO.
Il ne doit pas inventer de GO.
```

### 2. Ce qui necessite mon attention

Categories utiles :

| Categorie | Exemple |
| --- | --- |
| PR ouvertes | PR GitHub en attente de review |
| Branches actives | Branches non fusionnees ou non documentees |
| Docs modifies recemment | Plans, closeouts, reprises |
| TODO non fermes | TODO dans docs/chantiers |
| Gaps d'indexation | chantier sans entree index |
| Conflits potentiels | divergence branche locale / remote |
| Reprises disponibles | `SESSION_REPRISE.txt`, `BRANCH_STATE.md`, closeout incomplet |
| Actions sensibles | push, merge, suppression, modification de fichiers |

Sortie attendue :

```text
ATTENTION_NOW

P0 — Action requise
- GO_X : raison exacte
- Source : fichier / PR / branche

P1 — A verifier
- GO_Y : manque preuve Git
- Source : ...

P2 — Surveillance
- GO_Z : pas bloquant mais a suivre
```

### 3. Vue multi-machines

Machines connues :

```text
admin-trading
student
db-layer
cursor-ai
android / termux / tmux
```

Vue utile :

| Machine | Role | Etat attendu | Dernier point connu | Attention |
| --- | --- | --- | --- | --- |
| admin-trading | runtime trading / services | repo propre, services stables | a lire depuis docs | verifier service |
| student | lab / Ollama / tests | branche dediee si chantier | a etablir | possible drift |
| db-layer | OpenClaw / backend / data | repo distinct | en preparation | migration Claude |
| cursor-ai | Windows IDE | orchestration GUI | actif | Git sync |
| Android | acces SSH / tmux | client distant | cle creee | setup a finir |

Regle :

```text
Le Live Artifact peut montrer l'etat declare.
Il ne doit pas supposer que la machine est saine sans commande reelle.
```

### 4. Vue GitHub / branches / PR

Elements a afficher :

| Element | Pourquoi |
| --- | --- |
| PR ouvertes | A reviewer / merger / fermer |
| Branches recentes | Risque de dette |
| Branches sans PR | A qualifier |
| Branches liees a GO | Continuite |
| Branches orphelines | Nettoyage potentiel |
| Dernier commit par branche | Etat reel |

Regle canonique :

```text
Une branche vue dans le Live Artifact n'est pas automatiquement validee.
Validation = git fetch + git status + git branch -vv + docs indexees.
```

### 5. Vue documentation canonique

Fichiers importants a lire :

```text
docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
docs/index/GO_INDEX.md
docs/index/GO_CLOSED_INDEX.md
docs/index/REPRISE.md
docs/chantiers/*/SESSION_REPRISE.txt
docs/chantiers/*/BRANCH_STATE.md
docs/chantiers/*/closeout*.md
```

Affichage recommande :

| Bloc | Role |
| --- | --- |
| Derniers docs modifies | detecter activite recente |
| Docs sans index | detecter dette documentaire |
| Chantiers sans closeout | detecter fermeture incomplete |
| Chantiers sans BRANCH_STATE | detecter branche non documentee |
| Reprises disponibles | redemarrage rapide |

## 12_INVARIANTS

### Invariant 1 — La source de verite reste Git

```text
Le Live Artifact lit.
Git prouve.
Les docs canonisent.
Les commits historisent.
Les closeouts ferment.
```

### Invariant 2 — Pas de decision implicite

Le Live Artifact peut dire :

```text
Probable action recommandee : verifier PR #X
```

Il ne doit pas dire :

```text
PR #X doit etre mergee
```

sans audit reel.

### Invariant 3 — Pas d'ecriture sans GO

Le Live Artifact ne devrait pas modifier :

```text
repo
Drive
GitHub
fichiers locaux
index
branches
```

sans consigne claire du type :

```text
GO_APPLY
GO_COMMIT
GO_PUSH
GO_CLOSEOUT
```

## 13_ESTABLISHED

Les Live Artifacts Claude Cowork sont compris ici comme une surface de supervision dynamique et persistante, pouvant servir a rouvrir, rafraichir et iterer une vue operationnelle.

Pour `opt-trading`, le premier artefact doit rester en lecture seule et tirer sa valeur de la capacite a agreger les sources deja canoniques : repo, docs, GitHub, Drive, calendrier ou autres connecteurs autorises.

## 14_HYPOTHESIS

Trois Live Artifacts sont probablement utiles, mais a creer separement.

### A. OPT_TRADING_ATTENTION_CENTER_01

Role : quotidien / immediat.

Contient :

```text
- GO actifs
- PR ouvertes
- branches a traiter
- docs de reprise
- blockers
- prochaine action recommandee
```

### B. OPT_TRADING_GOVERNANCE_DASHBOARD_01

Role : gouvernance projet.

Contient :

```text
- conformite GO naming
- presence BRANCH_STATE
- presence closeout
- indexation docs/chantiers
- separation OPEN / CLOSED
- gaps documentaires
```

### C. OPENCLAW_ORCHESTRATOR_PREP_01

Role : preparation orchestrateur.

Contient :

```text
- etat OpenClaw
- machines disponibles
- connecteurs MCP
- acces tmux / ssh
- modules candidats
- risques securite
- plan de deploiement
```

## 15_REMAINING_GAP

Avant d'en faire un outil vraiment solide, il manque :

| Gap | Pourquoi |
| --- | --- |
| Definir les sources exactes autorisees | Eviter que Claude lise trop large |
| Definir le dossier local de travail Claude | Reduire le risque fichiers sensibles |
| Decider si GitHub est connecte a Claude | Pour PR/issues/branches |
| Decider si Google Drive est connecte | Pour docs externes |
| Decider si repo local est accessible | Pour lecture directe de `opt-trading` |
| Definir une regle read-only par defaut | Securite |
| Creer un prompt canonique de creation | Reproductibilite |

## 16_TODO — Setup recommande

### Etape 1 — Creer un dossier Claude dedie

Sur Windows :

```powershell
C:\Users\ghost\claude-workspace\
```

Sous-dossiers :

```text
claude-workspace/
  live-artifacts/
  snapshots/
  exported-prompts/
  repo-readonly/
  reports/
```

But : eviter de donner a Claude un acces trop large a tout le disque.

### Etape 2 — Ne pas donner acces brut a tout le repo au debut

Modele prefere :

```text
Repo reel : C:\Users\ghost\opt-trading
Copie/snapshot lecture : C:\Users\ghost\claude-workspace\repo-readonly
```

Claude lit le snapshot.
Les modifications reelles restent dans le repo via Trae / OpenCode / terminal / Git controle.

### Etape 3 — Creer le premier Live Artifact

Nom recommande :

```text
OPT_TRADING_ATTENTION_CENTER_01
```

Prompt pret a coller dans Claude Cowork :

```text
Cree un Live Artifact nomme OPT_TRADING_ATTENTION_CENTER_01.

Objectif :
Creer un tableau de bord dynamique “Ce qui necessite mon attention” pour mon workflow opt-trading.

Regles :
- Read-only par defaut.
- Ne modifie aucun fichier.
- Ne cree aucune branche.
- Ne propose aucun merge comme decision finale sans preuve Git reelle.
- La source de verite reste le repo, les docs, les commits, les closeouts.
- Le Live Artifact sert seulement de vue dynamique de pilotage.

Sources a lire si disponibles :
- docs/index/GO_INDEX.md
- docs/index/GO_CLOSED_INDEX.md
- docs/index/REPRISE.md
- docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
- docs/chantiers/*/SESSION_REPRISE.txt
- docs/chantiers/*/BRANCH_STATE.md
- docs/chantiers/*/closeout*.md
- GitHub PRs et branches si le connecteur GitHub est disponible
- Google Drive seulement si explicitement connecte et pertinent

Sections du dashboard :
1. ATTENTION_NOW
   - P0 : action requise
   - P1 : a verifier
   - P2 : surveillance

2. GO_ACTIVE
   - GO_ID
   - statut
   - branche liee
   - dernier checkpoint
   - prochaine action
   - source documentaire

3. BRANCHES_AND_PRS
   - PR ouvertes
   - branches sans PR
   - branches avec risque de dette
   - branches liees a un GO

4. DOC_GOVERNANCE
   - chantiers sans closeout
   - chantiers sans BRANCH_STATE
   - chantiers non indexes
   - docs recents importants

5. MULTI_MACHINE_VIEW
   - admin-trading
   - student
   - db-layer
   - cursor-ai
   - android/termux
   - etat declare uniquement, pas d'hypothese non verifiee

6. NEXT_GO_RECOMMENDATION
   - proposer une seule prochaine action prioritaire
   - distinguer ETABLI, HYPOTHESE, TODO
   - toujours citer la source utilisee

Format :
- Dashboard clair
- Tableaux
- Filtres par priorite
- Bouton ou section Refresh si disponible
- Ne jamais masquer les incertitudes
```

## 8_VALIDATED_PLAN

Plan d'integration propre :

| Phase | Action | Resultat |
| --- | --- | --- |
| P1 | Creer le Live Artifact read-only | Vue dynamique sans risque |
| P2 | Le connecter aux docs locales / Drive | Lecture des reprises |
| P3 | Ajouter GitHub | PR / branches / issues visibles |
| P4 | Ajouter scoring d'attention | P0 / P1 / P2 |
| P5 | Ajouter vue multi-machines | Etat operateur |
| P6 | Ajouter export rapport | Generer resume de session |
| P7 | Relier a OpenClaw | Orchestration future |

## 11_KEY_DECISIONS

### Decision recommandee 1

```text
Live Artifact = interface de pilotage
Repo = verite
```

### Decision recommandee 2

```text
Read-only par defaut
Ecriture seulement via GO explicite
```

### Decision recommandee 3

```text
Un Live Artifact par fonction
Pas un mega-dashboard unique des le depart
```

### Decision recommandee 4

```text
Premier artefact = ATTENTION_CENTER
Deuxieme = GOVERNANCE_DASHBOARD
Troisieme = OPENCLAW_ORCHESTRATOR_PREP
```

## 17_RESUME_POINT

Reprise operationnelle :

```text
Creer dans Claude Cowork :
OPT_TRADING_ATTENTION_CENTER_01

But :
Dashboard dynamique “Ce qui necessite mon attention”.

Contraintes :
- read-only
- source de verite = repo/docs/Git
- aucune modification sans GO explicite
- distinguer ETABLI / HYPOTHESE / TODO
- afficher GO actifs, PR, branches, docs, gaps, reprises
```

## Verdict final capture

Pour le workflow `opt-trading`, les Live Artifacts Claude sont pertinents comme couche de supervision.

Architecture correcte :

```text
Claude Live Artifact
= cockpit dynamique

Claude Cowork
= operateur assiste

OpenClaw
= orchestrateur local / agent runtime

GitHub + repo + docs
= verite canonique

GO_XXXX
= unite de travail controlee
```

Le premier artefact a creer devrait etre :

```text
OPT_TRADING_ATTENTION_CENTER_01
```

Pas un outil qui travaille directement dans le repo.
Un outil qui indique :

```text
Voici ce qui merite ton attention.
Voici pourquoi.
Voici la source.
Voici le prochain GO logique.
```

## RISKS

- À qualifier.
