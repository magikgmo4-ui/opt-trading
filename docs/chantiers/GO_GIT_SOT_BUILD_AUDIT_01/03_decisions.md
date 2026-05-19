---
doc_id: GO_GIT_SOT_BUILD_AUDIT_01_DECISIONS
doc_type: chantier_decisions
repo: opt-trading
project: opt-trading
go_id: GO_GIT_SOT_BUILD_AUDIT_01
status: pass
lifecycle_stage: audit
updated_at: 2026-04-22
topic_keys:
  - git
  - branches
  - sot-build
  - audit
  - keep-reference
surface: docs
source_kind: canonical
links:
  - docs/chantiers/GO_GIT_SOT_BUILD_AUDIT_01/00_cadrage.md
  - docs/index/BRANCH_STATE.md
---

# GO_GIT_SOT_BUILD_AUDIT_01 - Decisions

## 1_VERIF_GIT_REELLE

### Branche auditee

```text
origin/sot/build
SHA: 2c9cfb2c8aeaec9d657b21f439d538f20d8df02f
```

### Statut face a `origin/sot/mainline`

Verification retenue :

```text
git log --oneline origin/sot/mainline..origin/sot/build
```

Resultat : vide.

```text
git merge-base --is-ancestor origin/sot/build origin/sot/mainline
```

Resultat : `ABSORBED`

Conclusion Git :
- la branche est absorbee dans `origin/sot/mainline`
- elle n'a plus de commit propre hors canon

## 2_ROLE_REEL_ET_UTILITE_RESIDUELLE

### Tip audite

```text
2c9cfb2 module: repo_hygiene v1 (remove leading '\', untrack _student_archive, purge *.bak_*; ignore WAL/SHM)
```

### Nature du contenu

Le tip porte un chantier de hygiene repo a large surface :
- nettoyage massif de sauvegardes et archives
- ajout du module `repo_hygiene`
- rationalisation de scripts de post-change et de sanitation
- retouche de surfaces techniques transverses du repo

### Lecture de risque

`sot/build` n'est pas une branche documentaire banale. C'est une branche technique nommee dans la famille `sot/*` avec un historique de consolidation outillage/hygiene.

Constat retenu :
- le contenu utile est deja absorbe dans `origin/sot/mainline`
- mais la branche garde une valeur de reference technique et historique superieure a une branche absorbée standard
- le bundle et les gardes precedents demandaient une preuve technique dediee avant toute suppression de `sot/build`

## 3_DECISION

Decision retenue :

`KEEP_REFERENCE`

Motifs :
1. branche sensible de famille `sot/*`
2. historique de hygiene repo transversal et non trivial
3. utilite residuelle de reference technique/historique
4. absence de necessite immediate de suppression pour le menage courant

## 4_VERDICT

`KEEP_REFERENCE`

`origin/sot/build` reste absorbee du point de vue Git, mais est conservee comme reference technique plutot que reclassifiee en suppression remote.

Ce passage reste strictement doc-only.

Aucun delete Git n'est execute ici.
