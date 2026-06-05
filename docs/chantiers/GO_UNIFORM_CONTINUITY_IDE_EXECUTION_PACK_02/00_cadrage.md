---
doc_id: GO_UNIFORM_CONTINUITY_IDE_EXECUTION_PACK_02_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module:
go_id: GO_UNIFORM_CONTINUITY_IDE_EXECUTION_PACK_02
status: active
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - continuity
  - hardening
  - ide
  - execution_pack
surface: chantier
source_kind: canonical
updated_at: 2026-04-11
links:
  - docs/chantiers/GO_UNIFORM_CONTINUITY_HARDENING_01/00_cadrage.md
  - docs/chantiers/GO_UNIFORM_CONTINUITY_HARDENING_01/01_plan.md
  - docs/chantiers/GO_UNIFORM_CONTINUITY_HARDENING_01/90_closeout.md
---

# 00_cadrage — GO_UNIFORM_CONTINUITY_IDE_EXECUTION_PACK_02

## Identité
- GO : GO_UNIFORM_CONTINUITY_IDE_EXECUTION_PACK_02
- Repo : opt-trading
- Branche : sot/mainline
- Statut : active
- Type de travail : chantier de documentation pour exécution IDE

## État de départ retenu
- état repo retenu : la méthode uniforme est posée sur les 5 repos, mais le hardening des index existants reste partiellement non appliqué via le connecteur GitHub
- artefacts existants retenus : chantier `GO_UNIFORM_CONTINUITY_HARDENING_01`, socles documentaires repo par repo, pilotes PASS déjà créés
- limites connues : le connecteur utilisé dans cette session crée et lit bien des fichiers, mais ne permet pas ici de finaliser simplement l’update en place des fichiers existants
- dépendances : un IDE ou shell Git natif capable de modifier des fichiers existants et pousser les commits

## Objectif du lot
- objectif principal : produire un paquet documentaire précis indiquant à l’IDE tout ce qu’il doit faire pour terminer le hardening et poursuivre le plan sans toucher aux fichiers GO déjà ouverts dans cette session
- résultat attendu : un dossier chantier lisible, opératoire, contenant le cadrage, le plan, le journal de contexte, les décisions et le pack d’exécution IDE

## Non-objectifs
- modifier maintenant les index existants via le connecteur
- réécrire l’historique documentaire des repos
- ouvrir un nouveau chantier métier non documenté

## Critères PASS / FAIL
- PASS si : le dossier permet à un IDE d’exécuter le hardening restant et la suite logique du plan sans ambiguïté ni recroisement
- FAIL si : les actions IDE restent implicites, incomplètes ou contradictoires avec l’état réel déjà posé

## RISKS

- À qualifier.
