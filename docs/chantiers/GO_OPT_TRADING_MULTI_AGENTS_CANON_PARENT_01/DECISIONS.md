---
doc_id: OPT_TRADING_MULTI_AGENTS_DECISIONS_01
doc_type: decisions
repo: opt-trading
project: opt-trading
module: multi_agents
go_id: GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
status: open
lifecycle_stage: decisions
topic_keys:
  - opt-trading
  - multi_agents
  - decisions
  - invariants
  - parent_continuity
  - indexation
search_tags:
  - surface:chantier
  - doc_role:decisions
  - governance:parent_continuity
  - governance:indexation
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "INDEX_PATCH.md"
updated_at: 2026-04-26
links:
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/PARENT_STATE.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/ACTIVE.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/INDEX_PATCH.md
---

# DECISIONS — GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01

## Décisions retenues

### D-01 — Continuité parent locale prioritaire

Chaque parent doit pouvoir être repris depuis son propre dossier sans dépendre d'une modification immédiate des index globaux.

### D-02 — Index globaux par agrégation

Les quatre index globaux restent canoniques, mais ne sont pas des fichiers de travail quotidien pour chaque chantier.

### D-03 — INDEX_PATCH local obligatoire

Chaque parent actif qui doit être visible globalement prépare un `INDEX_PATCH.md` local.

### D-04 — Inbox atomique recommandée

Chaque parent peut créer une entrée courte sous :

```text
docs/index/inbox/<GO_ID>.md
```

Cette entrée sert de file d'attente pour le batch d'agrégation.

### D-05 — Aucun runtime touché

Ce chantier reste strictement doc-only.

### D-06 — Séparation des rôles multi-agents

La séparation suivante est retenue :

```text
Doctrine != Agent != Skill != Provider != Orchestrateur != Deployer != Prompt Generator != Bridge
```

## Décisions refusées

### R-01 — Modifier systématiquement les quatre index globaux

Refusé, car crée friction Git, conflits et risques de troncature.

### R-02 — Faire des bundles une source de vérité

Refusé. Les bundles restent supports secondaires.

### R-03 — Promouvoir OpenClaw en runtime principal

Refusé dans ce chantier. OpenClaw reste orchestrateur expérimental borné / provider cloisonné.

## Hypothèses non validées

- Une registry YAML pourrait devenir la meilleure solution long terme.
- Une génération automatique des index globaux pourrait être introduite plus tard.
- `docs/index/inbox/` pourrait devenir une surface canonique générale après validation du prochain GO méthode.

## Invariants

- Repo Git reste source de vérité.
- Les index globaux restent vues consolidées officielles.
- Le parent local porte la continuité de travail.
- Les fichiers locaux ne remplacent pas indéfiniment la propagation globale.
- Toute agrégation doit produire diff et closeout.
- Aucun tag ne remplace une décision ou un frontmatter.

## Prochaine action

Créer et maintenir `INDEX_PATCH.md`.
