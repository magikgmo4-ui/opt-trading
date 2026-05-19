---
doc_id: OPT_TRADING_GO_GITHUB_PARK_FILE_ROLE_CARTOGRAPHY_01
doc_type: chantier_report
repo: opt-trading
project: opt-trading
go_id: GO_GITHUB_PARK_FILE_ROLE_CARTOGRAPHY_01
status: closed
lifecycle_stage: audit
topic_keys:
  - github
  - file_role
  - cartography
  - trunks
  - governance
  - runtime
surface: park
source_kind: canonical
updated_at: 2026-04-14
links:
  - docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/00_cadrage.md
  - docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/01_branch_trunk_cross_audit.md
  - docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/02_module_family_consolidation_audit.md
  - docs/governance/GITHUB_PARK_CONSOLIDATION_DECISION_02.md
  - docs/governance/GITHUB_PARK_CONSOLIDATION_DECISION_02B.md
  - docs/governance/GITHUB_PARK_CONSOLIDATION_DECISION_02C.md
---

# GO_GITHUB_PARK_FILE_ROLE_CARTOGRAPHY_01

## Objet

Cartographier fichier par fichier les trunks ZIP reçus selon les rôles canoniques suivants :

- `gouvernance`
- `doc`
- `code`
- `runtime`
- `consumer`
- `legacy`

---

## Besoin initial

Après :

- l’inventaire complet des trunks ZIP
- l’audit croisé `branches ↔ trunks`
- l’audit des familles de modules dans `opt-trading`

il manquait une couche stable permettant de relire le parc non plus seulement par repo ou par famille, mais par **rôle réel des fichiers**.

---

## Cible finale

Obtenir une cartographie canonique exploitable pour :

- la reprise
- la consolidation future
- la distinction entre documentation descriptive, gouvernance opposable, code, runtime, surfaces consumer et reliquats legacy

---

## Méthode retenue

### Source réelle utilisée
- trunks ZIP réellement reçus et inspectés durant la session

### Repos couverts
- `opt-trading`
- `localcms`
- `openclaw`
- `hf_trading`
- `Llm-wiki-minimal`
- `Llm-wiki`

### Taille du corpus
- fichiers cartographiés : **1984**

### Méthode de classement
Classement primaire heuristique mais systématique, fondé sur :

- le rôle déjà établi du repo
- le chemin réel du fichier
- les emplacements canoniques du parc (`docs/governance`, `docs/chantiers`, `docs/ot/closings`, `registry`, `workflow_ai`, `modules/*/app`, `modules/*/scripts`, etc.)
- les marqueurs de legacy (`archive`, `backup`, `deprecated`, `obsolete`, etc.)

---

## Règles canoniques appliquées

### `gouvernance`
Décisions, kanban, closings, cadrages, registry, workflow, transmission, index canoniques.

### `doc`
Documentation descriptive, README, architecture, runbooks non normatifs, références.

### `code`
Implémentation applicative, librairies, API, sources, tests.

### `runtime`
Scripts opérateur, wrappers, services, timers, configs d’exécution, entrypoints installables.

### `consumer`
Surfaces consommées par un humain ou par un autre système sans être le cœur d’implémentation :
- UI HTML
- examples / launchables
- fiches / exports / index de consommation

### `legacy`
Archives, backups, reliquats obsolètes, lanes gelées.

---

## État établi — vue globale par repo

| Repo | Total | Gouvernance | Doc | Code | Runtime | Consumer | Legacy |
|---|---:|---:|---:|---:|---:|---:|---:|
| `opt-trading` | 1794 | 369 | 365 | 285 | 682 | 8 | 85 |
| `localcms` | 91 | 34 | 19 | 33 | 3 | 2 | 0 |
| `openclaw` | 51 | 30 | 12 | 1 | 0 | 8 | 0 |
| `hf_trading` | 13 | 6 | 2 | 3 | 1 | 1 | 0 |
| `Llm-wiki-minimal` | 34 | 4 | 4 | 16 | 4 | 6 | 0 |
| `Llm-wiki` | 1 | 0 | 0 | 0 | 0 | 0 | 1 |

---

## Lectures structurantes

### 1. `opt-trading`
Le repo n’est pas monolithique.
Il cumule :

- une couche `runtime` dominante
- une couche `gouvernance` très épaisse
- une couche `doc` importante
- une couche `code` réelle mais proportionnellement moins dominante
- une couche `legacy` encore visible

Conclusion :
`opt-trading` est à la fois :
- repo canonique d’exécution
- repo de gouvernance locale
- repo opérateur
- repo encore porteur de reliquats historiques

### 2. `localcms`
Répartition plus équilibrée entre :
- `gouvernance`
- `code`
- `doc`

Le repo reste un repo produit avec gouvernance locale explicite.

### 3. `openclaw`
Dominante `gouvernance` très nette.
Les éléments `consumer` restent bornés aux examples/launchables.

Conclusion :
`openclaw` confirme pleinement son rôle de repo documentaire/gouvernance dédié.

### 4. `hf_trading`
Petit repo bootstrap, peu ambigu.

### 5. `Llm-wiki-minimal`
Petit repo mixte mais réel, confirmant une vraie boucle de pré-consolidation documentaire.

### 6. `Llm-wiki`
Entièrement `legacy`, conformément à la décision de parc validée.

---

## Lecture structurante côté `opt-trading`

Le lot confirme que la dette active principale n’est pas un simple problème de “trop de modules”.

La dette active est un mélange de :

- couches `runtime` très denses
- gouvernance locale importante
- familles de modules où se mélangent code, runtime, doc et parfois legacy
- écart entre parc réel et couche canonique registry

---

## Effet sur les familles déjà auditées

La cartographie renforce les constats du lot précédent :

### Famille prioritaire nette
- `reseau_ssh*`
  - vraie lignée versionnée
  - survivant cible déjà connu : `reseau_ssh_step2`

### Familles à clarifier plus qu’à fusionner aveuglément
- `desk_pro*`
- `desk_*`
- `openclaw*`
- `registry*`
- `vision*`
- `journal*`
- `perf*`

### Famille déjà suffisamment fixée côté continuité
- `workflow_post_change_v2*`

---

## Ce qui est établi à ce stade

1. La lecture par rôles confirme les décisions de parc déjà validées.
2. `opt-trading` est le seul repo dont la complexité interne justifie des GO de consolidation ciblés.
3. `openclaw`, `localcms`, `hf_trading` et `Llm-wiki-minimal` ont des profils beaucoup plus lisibles à ce niveau.
4. La cartographie fichier par fichier fournit désormais une base suffisante pour choisir des consolidations physiques ciblées.

---

## Limites réelles

Cette cartographie :

- est primaire et heuristique
- n’assigne pas de rôle secondaire
- ne remplace pas une revue humaine commit par commit
- ne met pas à jour physiquement la registry ou les dossiers

---

## Next GO

### GO retenu
`GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03`

### Pourquoi
Parce que :

- la famille `reseau_ssh*` est une vraie lignée versionnée
- la cible de continuité est déjà connue (`reseau_ssh_step2`)
- le lot précédent et la cartographie actuelle convergent pour en faire le candidat de consolidation le plus net

---

## Verdict

**PASS — cartographie canonique fichier par fichier établie ; suite logique = consolidation ciblée `reseau_ssh*`**
