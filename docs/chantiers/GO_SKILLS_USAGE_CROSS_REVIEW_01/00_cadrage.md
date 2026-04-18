---
doc_id: GO_SKILLS_USAGE_CROSS_REVIEW_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module:
go_id: GO_SKILLS_USAGE_CROSS_REVIEW_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - doctrine
  - refactor
  - consolidation
  - skills
  - bundles
  - module_durable
  - guardrails
surface: chantier
source_kind: canonical
updated_at: 2026-04-17
links:
  - docs/governance/SESSION_DOCUMENTATION_GATE.md
  - docs/governance/DOC_LAYERS.md
  - docs/governance/REPO_ROLE.md
  - docs/ot/trae/03_MISSION_CLASSES_V1.txt
  - docs/ot/trae/04_SKILLS_V1.txt
  - docs/ot/trae/04_SKILLS_V1_OPERATING_SPEC_01.txt
  - docs/index/REPRISE.md
  - docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md
  - docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/03_decisions.md
  - docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/04_branch_trunk_cross_audit_target.md
  - docs/ot/closings/OT_OPT_TRADING_DOC_AUTOMATION_MODULE_DECISION_01_CLOSING.txt
---

# 00_cadrage — GO_SKILLS_USAGE_CROSS_REVIEW_01

## Identité
- GO : GO_SKILLS_USAGE_CROSS_REVIEW_01
- Repo : opt-trading
- Branche : sot/mainline
- Statut : open
- Type de travail : doctrine d’usage (choix des leviers)
- Classification retenue : module durable — parent doctrinal d’usage
- Rôle recommandé : architecte workflow + gardien de périmètre

## Besoin initial
Comparer et structurer, dans le cadre réel de `opt-trading`, les bons usages :
- refactor borné
- consolidation ciblée
- skills de contrôle
- bundles de transfert
- modules durables

afin d’obtenir un mode opératoire cohérent, borné, reprenable, repo-first, sans canon parallèle.

## Intention
Définir une doctrine d’usage claire :
- quel levier employer selon la nature du chantier
- comment éviter la dérive de scope et la dérive de canon
- comment adapter l’outillage à cette doctrine sans sur-architecture

## Cible finale
Un modèle opératoire où :
- la consolidation ciblée traite les problèmes de cohérence, hiérarchie et continuité
- le refactor borné traite les problèmes internes à un périmètre local
- les skills industrialisent seulement les procédures stables de contrôle (doc-only)
- les modules durables portent les vraies capacités réutilisables du repo
- les bundles servent uniquement au transfert / exécution inter-session ou inter-machine
- le tout reste repo-first, sans canon parallèle, avec reprise autonome depuis le repo

## Plan validé
1. analyser les usages du refactor, de la consolidation et des skills dans `opt-trading`
2. recroiser ces usages par rôles (machine / IA-IDE / repo-produit)
3. dégager des versions opératoires plus optimales
4. retenir une recommandation par défaut
5. dériver un petit noyau de skills utiles (contrôle)
6. adapter ensuite l’outillage réel à cette doctrine
7. figer le tout dans le repo pour sortir la continuité de la session

## Doctrine par levier (règles d’usage)

### Consolidation ciblée
- but : réduire la dette de cohérence (structure, hiérarchie, continuité) sans refactor transverse par défaut
- forme : GO borné par famille / périmètre ; patch minimal de consolidation ; preuves et reprise explicites
- interdit : consolidation “large” non classée et non séquencée

### Refactor borné
- but : améliorer l’interne d’un périmètre déjà borné (module/famille/zone)
- prérequis : consolidation et tri déjà posés ; scope explicite ; rollback simple
- interdit : refactor transverse par défaut, ou refactor qui reclassifie silencieusement la gouvernance/canon

### Skills (industrialisation de contrôle)
- but : accélérer les opérations fréquentes, répétables, bornées et diffables
- garde-fou : un skill ne doit pas devenir une mission entière ni une gouvernance concurrente
- contrainte : doc-only, repo-first, runtime-honesty, output stable (références : 04_SKILLS_V1 + addendum)

### Bundles (transfert / exécution)
- but : transfert inter-machine, inter-session, ou exécution IDE bornée
- statut : support secondaire ; ne remplace jamais le repo
- garde-fou : liste de contenu, destination, validations à rejouer, point de reprise

### Module durable (actif repo)
- but : créer/stabiliser une capacité réutilisable du repo (structure + scripts + validations)
- contrainte : n’ouvrir un module durable que si un besoin dur est prouvé (fréquence, exécution hors Trae, validation rejouable hors conversation, incidents répétés malgré doc-only)

## Version recommandée (par défaut)
Version B — équilibre opératoire :
- consolidation ciblée
- refactor borné
- petit noyau de skills de contrôle
- bundle seulement pour transfert
- module durable quand la logique devient un actif repo

## Noyau de skills (contrôle) retenu
Réutiliser le noyau V1 existant :
- 4.1 classify_mission
- 4.2 extract_established_state
- 4.3 detect_contradictions
- 4.4 assess_shared_and_portability
- 4.5 review_scope_compliance
- 4.6 build_execution_report

## Garde-fous anti-canon parallèle
- repo-first : l’état réel du repo prime sur mémoire, prompts, sessions et supports secondaires
- pas de canon cockpit : cockpit local/distant = surfaces d’opération, pas source de vérité
- pas de canon bundle : un bundle reste un support secondaire et doit pointer vers le canon repo
- pas de “super-skill” : les skills n’absorbent ni la mission, ni l’exécution, ni la gouvernance

## ETABLI
- repo canonique : `opt-trading`
- branche canonique de continuité : `sot/mainline`
- bundles : supports secondaires explicitement bornés par `docs/index/REPRISE.md`
- socle skills V1 existant, avec addendum opératoire stabilisé
- décision close “doc automation” : SKILLS_ONLY tant qu’aucun besoin dur hors Trae n’est prouvé
- le sous-chantier runtime/double cockpit existe déjà et doit être traité comme déclinaison opératoire dérivée

## Gap restant
- rattacher explicitement, dans les sous-chantiers dérivés, ce parent doctrinal comme racine logique
- stabiliser, par zones, des exemples repo-first de “consolidation ciblée” vs “refactor borné” (sans ouvrir de refactor transverse)
- décider, si besoin, d’un lot d’alignement minimal des index (sans élargir la matrice active)

## Next GO
- GO_SKILLS_USAGE_CROSS_REVIEW_01_APPLY_01 (si et seulement si des contradictions réelles sont observées entre chantiers dérivés et doctrine)

## Déclinaisons rattachées (dérivées)
- runtime / double cockpit : `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01`
- convergence branches ↔ trunk (anti-canon parallèle) : `GO_GITHUB_PARK_AUDIT_EXPANSION_01/04_branch_trunk_cross_audit_target.md`

## Séparation des couches
- rôle machine : exécution réelle, runtime, transferts
- rôle IA / IDE : outillage, assistance, contrôle, rédaction bornée
- rôle repo / produit : canon versionné, continuité, chantiers, closeouts
