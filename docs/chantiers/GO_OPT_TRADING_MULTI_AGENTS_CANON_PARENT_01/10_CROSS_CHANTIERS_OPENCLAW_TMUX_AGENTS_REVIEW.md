---
doc_id: OPT_TRADING_MULTI_AGENTS_CROSS_CHANTIERS_OPENCLAW_TMUX_AGENTS_REVIEW_01
doc_type: cross_review
repo: opt-trading
project: opt-trading
module: multi_agents
go_id: GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
status: open
lifecycle_stage: cross_review
topic_keys:
  - opt-trading
  - multi_agents
  - openclaw
  - tmux
  - opencode
  - hermes
  - provider_policy
  - gateway
  - agents
  - runtime_guardrails
search_tags:
  - surface:chantier
  - doc_role:cross_review
  - cross:openclaw
  - cross:tmux
  - cross:agents
  - boundary:runtime_vs_doctrine
  - governance:multi_agents_doctrine
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section 12 - Décisions de recroisement"
updated_at: 2026-04-26
links:
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/PARENT_STATE.md
  - docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md
  - docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/03_decisions.md
  - docs/product_targets/OPENCLAW_TARGET_CANON.md
  - docs/hermes/GO_HERMES_OPENCLAW_BRIDGE_05.md
  - docs/hermes/HERMES_OPENCLAW_BRIDGE_RUNBOOK_V1.md
  - modules/menu_openclaw/docs/GO_OPENCLAW_CHAIN_03.md
  - modules/model_provider_openclaw/docs/GO_OPENCLAW_PROVIDER_POLICY_04.md
  - modules/model_provider_openclaw/docs/GO_OPENCLAW_POLICY_RUNTIME_ALIGNMENT_05.md
  - modules/menu_openclaw/docs/GO_OPENCLAW_STATE_DIR_REPAIR_10/00_cadrage.md
---

# 10_CROSS_CHANTIERS_OPENCLAW_TMUX_AGENTS_REVIEW

## 1. Objet

Recroiser le chantier parent multi-agents avec les chantiers et surfaces déjà existants autour de :

- OpenClaw ;
- tmux / OpenCode ;
- agents ;
- providers ;
- Hermes bridge ;
- gateway / runtime ;
- garde-fous.

But : éviter de reconstruire ou de contredire des chantiers parents déjà actifs.

## 2. Chantier courant

### GO courant

```text
GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
```

### Rôle

Doctrine transverse multi-agents.

### Nature

Doc-only. Ne doit pas devenir chantier runtime OpenClaw.

### Surfaces déjà produites

- `PARENT_STATE.md`
- `02_AGENT_SKILL_PROVIDER_MATRIX.md`
- `03_FRONTMATTER_SEARCH_TAGS_NAMING_DOCTRINE.md`
- `08_PARENT_CONTINUITY_WITHOUT_GLOBAL_INDEX_METHOD.md`
- `09_INDEX_INBOX_ATOMIC_ENTRY_CONVENTION.md`

## 3. Chantier runtime tmux / OpenCode / OpenClaw

### Source principale

```text
docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md
docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/03_decisions.md
```

### État établi

Ce parent runtime est actif. Il vise une architecture d'utilisation où :

- `tmux` porte la persistance ;
- `OpenCode` porte la production / code engine ;
- `OpenClaw` porte l'orchestration / control plane ;
- `Telegram` porte l'interface distante.

Il établit un système vivant continu, distinct d'une simple session locale IDE.

### Sous-chantiers structurants établis

- `GO_TMUX_RUNTIME_CONVENTIONS_01`
- `GO_OPENCLAW_COMMAND_SCOPE_01`
- `GO_TMUX_RUNTIME_CONTRACT_01`
- `GO_TMUX_OPENCODE_OPENCLAW_MODES_01`
- `GO_RUNTIME_GUARDRAILS_01`
- `GO_RUNTIME_SUPERVISION_POLICY_01`
- `GO_RUNTIME_REMOTE_CONTROL_POLICY_01`
- `GO_RUNTIME_REMOTE_CONTROL_TOOLING_01`
- `GO_RUNTIME_REMOTE_CONTROL_IMPL_01`

### Recouvrement avec le chantier multi-agents

| Sujet | Parent runtime | Parent multi-agents |
| --- | --- | --- |
| tmux | persistance runtime | pas propriétaire |
| OpenCode | production / code engine | agent/outillage à classer, pas à implémenter |
| OpenClaw | orchestration/control plane runtime | orchestrateur expérimental borné dans la matrice |
| Telegram | interface distante | hors périmètre sauf rôle remote-control |
| garde-fous | runtime guardrails | invariants généraux multi-agents |

### Décision de recroisement

Le chantier multi-agents ne doit pas remplacer `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01`.

Il doit seulement fournir une taxonomie transverse : agent / skill / provider / orchestrateur / deployer / bridge.

## 4. OpenClaw target canon

### Source principale

```text
docs/product_targets/OPENCLAW_TARGET_CANON.md
```

### État établi

OpenClaw est :

- labo Linux cloisonné ;
- gouverné ;
- installé sur `db-layer` ;
- environnement isolé ;
- couche expérimentale / provider ;
- non exposé directement aux flux critiques.

### Contraintes fortes

- Linux natif uniquement ;
- environnement cloisonné ;
- pas d'ouverture `tools/channels/nodes` ;
- pas runtime principal ;
- pas produit user-facing ;
- pas système ouvert non contrôlé.

### Recroisement

Le chantier multi-agents doit reprendre cette borne :

```text
OpenClaw = orchestrateur expérimental / provider layer
OpenClaw != runtime principal libre
OpenClaw != gouvernance souveraine
OpenClaw != agent autonome non borné
```

## 5. Chaine opérateur OpenClaw

### Source principale

```text
modules/menu_openclaw/docs/GO_OPENCLAW_CHAIN_03.md
```

### Chaine standard retenue

1. `install_module_openclaw`
2. `openclaw_config_modulaire`
3. `gateway_openclaw`
4. `configure_openclaw`
5. `doctor_openclaw`
6. `evidence_openclaw`

### Recroisement

Cette chaîne est une chaîne opérateur OpenClaw. Elle ne devient pas une doctrine multi-agents générale.

Dans la matrice multi-agents :

- `install_module_openclaw` = installation / registry OpenClaw ;
- `openclaw_config_modulaire` = config prudente + backup/rollback ;
- `gateway_openclaw` = gateway local ;
- `configure_openclaw` = relecture config ;
- `doctor_openclaw` = checks ;
- `evidence_openclaw` = preuve/export.

## 6. Provider policy / agents OpenClaw

### Sources principales

```text
modules/model_provider_openclaw/docs/GO_OPENCLAW_PROVIDER_POLICY_04.md
modules/model_provider_openclaw/docs/GO_OPENCLAW_POLICY_RUNTIME_ALIGNMENT_05.md
```

### État établi

Policy V1 couvre :

- `orchestrateur`
- `builder`
- `reviewer`
- `lab`

Providers autorisés :

- `openrouter`
- `openai_compatible_local`

Stratégie :

- `deny_unlisted`

Runtime relu :

- `orchestrateur`
- `builder`
- `reviewer`
- `lab`
- `codexoauth`

Alignements observés :

- `orchestrateur` aligné ;
- `builder` aligné.

Écarts observés :

- `reviewer` non aligné dans l'état observé ;
- `lab` sur fallback ;
- `codexoauth` visible runtime mais hors policy V1 observée.

### Recroisement

Le chantier multi-agents doit distinguer :

- agents génériques externes : Codex, Claude, Trae ;
- agents OpenClaw runtime : `orchestrateur`, `builder`, `reviewer`, `lab`, `codexoauth` ;
- provider policy : module `model_provider_openclaw` ;
- runtime state : état observé, pas cible normative automatique.

### Décision

Ne pas intégrer `codexoauth` comme agent canonique global sans GO de qualification.

Le noter comme :

```text
runtime-visible, policy-gap, à qualifier
```

## 7. Hermes -> OpenClaw bridge

### Sources principales

```text
docs/hermes/03_bridge_openclaw.md
docs/hermes/HERMES_OPENCLAW_BRIDGE_RUNBOOK_V1.md
docs/hermes/GO_HERMES_OPENCLAW_BRIDGE_05.md
```

### État établi

Flux visé :

```text
Hermes -> génération
OpenClaw -> exécution ou relecture contrôlée
Validation humaine -> repo
```

Garde-fous :

- pas d'auto-commit ;
- pas d'exécution non contrôlée ;
- validation humaine obligatoire ;
- pas de preuve unique lue comme maturité générale ;
- pas de framework bridge complet déclaré établi sans preuves convergentes.

### Recroisement

Dans la matrice multi-agents :

- Hermes bridge = bridge expérimental ;
- pas agent principal ;
- pas orchestrateur souverain ;
- pas preuve d'automatisation globale.

## 8. Gateway / state dir / runtime repair

### Source principale

```text
modules/menu_openclaw/docs/GO_OPENCLAW_STATE_DIR_REPAIR_10/00_cadrage.md
```

### État établi

GO vise une réparation locale bornée du gateway sur `db-layer`.

État de départ :

- config lue et validée : `~/.openclaw/openclaw.json` ;
- workspace : `/home/openclaw/.openclaw/workspace-orchestrateur` ;
- session `openclaw-gateway` arrêtée ;
- cible gateway attendue : `ws://127.0.0.1:18789` ;
- erreur observée : `ECONNREFUSED 127.0.0.1:18789`.

Hors périmètre :

- patch runtime large ;
- patch policy ;
- exposition WAN ;
- réarchitecture multi-machine ;
- conclusion causale non prouvée sur double state dir.

### Recroisement

Le chantier multi-agents ne doit pas utiliser l'indisponibilité gateway comme preuve d'échec global OpenClaw.

Il doit lire cette surface comme :

```text
runtime repair local, borné, séparé de la doctrine multi-agents
```

## 9. Tmux / OpenCode / OpenClaw vs Multi-agents

### Séparation proposée

| Couche | Propriétaire documentaire | Rôle |
| --- | --- | --- |
| tmux runtime | `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01` | persistance et session vivante |
| OpenCode | parent runtime / futur sous-GO | production / code engine |
| OpenClaw runtime | parents OpenClaw / runtime | control plane, gateway, provider layer |
| Multi-agents canon | `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` | taxonomie et doctrine transverse |
| Provider policy | `model_provider_openclaw` | mapping agents -> providers/models |
| Bridge Hermes | docs/hermes | preuve bornée generation/execution |
| Remote control | parent runtime | télécommande distante |

## 10. Conflits potentiels

### C-01 — OpenClaw runtime vs doctrine multi-agents

Risque : le chantier multi-agents pourrait être lu comme une autorisation d'implémenter OpenClaw.

Décision : refusé. Ce chantier reste doctrine transverse.

### C-02 — Agent OpenClaw vs agent externe

Risque : confondre `builder` OpenClaw avec Claude/Codex.

Décision : distinguer agent runtime OpenClaw et agent externe.

### C-03 — Provider policy vs orchestration

Risque : lire `model_provider_openclaw` comme orchestrateur.

Décision : c'est une policy provider/model, pas un orchestrateur.

### C-04 — Bridge Hermes comme automatisation générale

Risque : extrapoler une preuve bridge en framework général.

Décision : interdit sans preuves convergentes.

### C-05 — Gateway indisponible comme décision produit

Risque : transformer une réparation locale en décision d'architecture.

Décision : garder `STATE_DIR_REPAIR_10` comme runtime repair local.

## 11. Alignements confirmés

- Le parent runtime distingue déjà tmux / OpenCode / OpenClaw / Telegram.
- Le parent multi-agents distingue doctrine / agent / skill / provider / orchestrateur / deployer / bridge.
- Le target canon OpenClaw borne OpenClaw comme labo/provider cloisonné.
- La policy provider OpenClaw définit agents et providers autorisés.
- Hermes bridge impose validation humaine, pas d'auto-commit.
- Les garde-fous runtime et la doctrine multi-agents sont compatibles.

## 12. Décisions de recroisement

### D-01 — Ne pas fusionner les parents

`GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` et `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01` restent distincts.

### D-02 — Le parent multi-agents est transversal

Il fournit taxonomie, metadata, indexation, rôle des outils et garde-fous généraux.

### D-03 — Le parent runtime reste propriétaire de tmux/OpenCode/OpenClaw/Telegram runtime

Toute implémentation de persistance, gateway, remote control ou tmux appartient au parent runtime ou à ses sous-GO.

### D-04 — OpenClaw reste borné

Aucun document multi-agents ne doit lever les restrictions du target canon OpenClaw.

### D-05 — codexoauth à qualifier

`codexoauth` est visible runtime mais hors policy V1 observée. Ne pas le promouvoir sans GO dédié.

### D-06 — Provider policy ne corrige pas le runtime

`GO_OPENCLAW_POLICY_RUNTIME_ALIGNMENT_05` est diagnostic. Toute correction policy/runtime doit avoir un GO séparé.

## 13. Recommandations

### R-01 — Ajouter un lien dans le parent multi-agents vers le parent runtime

Déjà effectué via ce document.

### R-02 — Ajouter un futur GO de qualification codexoauth si besoin

Nom possible :

```text
GO_OPENCLAW_CODEXOAUTH_POLICY_QUALIFICATION_01
```

### R-03 — Ouvrir un GO méthode séparé pour parent-continuity/inbox

Nom proposé :

```text
GO_OPT_TRADING_PARENT_CONTINUITY_INDEX_INBOX_METHOD_01
```

### R-04 — Garder OpenClaw runtime hors bundle multi-agents

Le bundle multi-agents peut inclure les docs comme références, mais ne doit pas inclure scripts runtime d'exécution comme cible d'application.

### R-05 — Future carte architecture

Si la doctrine multi-agents est promue, créer une carte dans :

```text
docs/architecture/MULTI_AGENTS_SURFACE_MAP_01.md
```

## 14. Mise à jour recommandée de la matrice agents

Dans `02_AGENT_SKILL_PROVIDER_MATRIX.md`, ajouter si besoin :

```text
codexoauth = runtime-visible / policy-gap / à qualifier
```

Ne pas le classer comme agent canonique tant que policy V1 ne l'inclut pas.

## 15. Point de reprise

Reprendre depuis :

```text
docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/10_CROSS_CHANTIERS_OPENCLAW_TMUX_AGENTS_REVIEW.md
```

Prochaine action possible :

- mettre à jour `02_AGENT_SKILL_PROVIDER_MATRIX.md` pour ajouter la note `codexoauth` ;
- ou préparer `90_CLOSEOUT_DRAFT.md` du parent multi-agents ;
- ou ouvrir `GO_OPT_TRADING_PARENT_CONTINUITY_INDEX_INBOX_METHOD_01`.
