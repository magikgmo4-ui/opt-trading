---
doc_id: GO_UNIFORM_CONTINUITY_IDE_EXECUTION_PACK_02_DECISIONS
doc_type: decision
repo: opt-trading
project: opt-trading
module:
go_id: GO_UNIFORM_CONTINUITY_IDE_EXECUTION_PACK_02
status: active
lifecycle_stage: validation
topic_keys:
  - opt-trading
  - continuity
  - ide
  - decisions
  - execution_pack
surface: chantier
source_kind: canonical
updated_at: 2026-04-11
links:
  - docs/chantiers/GO_UNIFORM_CONTINUITY_IDE_EXECUTION_PACK_02/IDE_EXECUTION_PACK.md
---

# 03_decisions — GO_UNIFORM_CONTINUITY_IDE_EXECUTION_PACK_02

## Décision 1
- sujet : voie d’exécution du hardening restant
- option retenue : documenter précisément ce que l’IDE doit faire en Git natif
- raison du choix : le connecteur utilisé dans cette session cadre bien les créations, mais reste contraint pour certaines mises à jour en place des fichiers existants
- impact : le chantier devient un paquet de transmission opératoire plutôt qu’un simple constat de blocage

## Décision 2
- sujet : périmètre du pack IDE
- option retenue : finir d’abord `opt-trading` et `localcms`, garder `llm_wiki_minimal` et `hf_trading` en suites optionnelles ou différées
- raison du choix : ce sont les deux repos où des index existants restent effectivement à réaligner
- impact : l’IDE a une séquence courte et priorisée

## Décision 3
- sujet : modification des fichiers GO existants
- option retenue : ne pas les modifier dans ce lot documentaire
- raison du choix : respecter la contrainte explicite du chantier et transmettre un pack autonome
- impact : le dossier sert d’instruction, pas de réécriture rétrospective des GO déjà ouverts
