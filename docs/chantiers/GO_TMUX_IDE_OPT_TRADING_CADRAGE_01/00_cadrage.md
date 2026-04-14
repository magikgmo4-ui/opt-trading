---
doc_id: GO_TMUX_IDE_OPT_TRADING_CADRAGE_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module:
go_id: GO_TMUX_IDE_OPT_TRADING_CADRAGE_01
status: active
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - tmux
  - tmux-ide
  - ssh
  - ide
  - continuity
surface: chantier
source_kind: canonical
updated_at: 2026-04-14
links:
  - docs/governance/SESSION_DOCUMENTATION_GATE.md
  - docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md
  - docs/index/REPRISE.md
  - docs/index/GO_INDEX.md
  - docs/chantiers/
---

# 00_cadrage — GO_TMUX_IDE_OPT_TRADING_CADRAGE_01

## Identité
- GO : GO_TMUX_IDE_OPT_TRADING_CADRAGE_01
- Repo : opt-trading
- Branche : sot/mainline
- Statut : active
- Type de travail : bundle de transfert / cadrage IDE terminale

## Intention
- cadrer une base IDE terminale canonique pour `opt-trading` via `tmux` / `tmux-ide`, exploitable en SSH distant et transmissible sans ambiguïté

## Produits finaux voulus / objectifs du chantier
- une session IDE terminale stable et reattachable pour `opt-trading`
- un layout opératoire adapté au repo canonique
- un bundle de transfert minimal avec prompts, instructions et `ide.yml`
- une base de reprise claire pour les GO suivants

## État de départ retenu
- besoin validé : préparer une utilisation propre de `tmux-ide` pour `opt-trading`
- hypothèse par défaut retenue : machine Linux distante en SSH avec repo local et GitHub comme remote
- bundle de transfert déjà préparé hors repo dans la session courante
- références canoniques explicites imposées pour le chantier : gate session, hiérarchie produit, reprise, index GO, dossier `docs/chantiers/`

## Objectif du lot
- poser un point d’entrée canonique minimal pour la trajectoire `tmux-ide` côté `opt-trading`
- fixer le besoin initial, la cible finale, le plan validé, l’état établi courant, le gap restant et le next GO

## Plan validé
1. relire la gate de session et le canon de continuité produit
2. confirmer le mode cible : SSH distant / repo local / GitHub remote
3. préparer le bundle de transfert IDE
4. poser un `ide.yml` de base
5. prévoir `doctor` / `validate` / `start`
6. définir le point de reprise canonique

## État établi courant
- besoin initial : usage `tmux-ide` pour `opt-trading`
- cible finale : session terminale outillée et reattachable, alignée sur le canon repo
- plan validé : bundle puis validation machine réelle
- état courant : bundle préparé, cadrage canonique ouvert

## Gap restant
- valider la machine cible réelle
- adapter les panes aux commandes réellement utiles
- confirmer l’emplacement repo réel sur la machine cible
- exécuter la validation réelle de `tmux-ide` sur environnement cible

## Next GO
- GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01

## Séparation des couches
- machine owner / thread machine : cible par défaut `admin-trading`, thread SSH distant, à revalider contre l’état réel
- rôle actif IA/IDE : architecture / outillage / orchestration terminale
- rôle repo / produit : `opt-trading` comme repo canonique, `sot/mainline` comme branche de continuité

## Critères PASS / FAIL
- PASS si : la trajectoire `tmux-ide` est cadrée sans ambiguïté et qu’un point de reprise canonique existe
- FAIL si : le chantier reste dépendant d’un contexte de conversation sans trace durable minimale

## Point de vigilance
- risque principal : confondre IDE terminale distante, repo local réel et simple remote GitHub
- point d’arrêt acceptable : cadrage canonique déposé avant implémentation réelle machine
