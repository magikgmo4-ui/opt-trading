---
doc_id: GO_OPT_TRADING_OPENCLAW_AGENTS_PARENT_LONA_MCP_TMUX_EXEC_01_PARENT_CHECKPOINT
 doc_type: chantier_parent_checkpoint
repo: opt-trading
project: opt-trading
module: openclaw_agents
 go_id: GO_OPT_TRADING_OPENCLAW_AGENTS_PARENT_LONA_MCP_TMUX_EXEC_01
status: open
lifecycle_stage: cadrage
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-04-24
topic_keys:
  - openclaw
  - mcp
  - lona
  - tmux
  - strategy_lab
  - trading_assistant
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/index/BRANCH_STATE.md
---

# 00_PARENT_CHECKPOINT

## 1_MASTER_TARGET

Créer un chantier parent dédié pour cadrer, documenter et préparer une exécution réelle contrôlée de la combinaison :

```text
OpenClaw + MCP + LONA Trading Assistant + tmux + opt-trading
```

Le chantier vise une intégration de type **strategy lab / backtest / validation**, pas une exécution live autonome.

## 2_INITIAL_PROJECT_DOC

Document initial transporteur du chantier :

- `docs/chantiers/GO_OPT_TRADING_OPENCLAW_AGENTS_PARENT_LONA_MCP_TMUX_EXEC_01/00_PARENT_CHECKPOINT.md`

Ce document fixe le plan initial. Il reste la référence de démarrage.

## 3_INITIAL_NEED

Demande utilisateur :

- documenter l'intégralité des réponses de session pour ne plus dépendre du chat ;
- aiguiser les recherches sur LONA, OpenClaw, MCP et tmux ;
- établir une documentation d'exécution réelle ;
- créer un chantier parent sur une branche dédiée ;
- présenter et documenter un plan.

## 4_MASTER_PROJECT_PLAN

Axes du parent :

1. **Documentation indépendante de session**  
   Capturer toutes les conclusions déjà formulées : LONA ressemble au setup existant, mais doit être utilisé comme complément strategy lab / backtest.

2. **Recherche externe affinée**  
   Revalider les capacités LONA et OpenClaw MCP via sources publiques récentes.

3. **Architecture d'intégration**  
   Positionner :
   - tmux = cockpit opérateur Linux ;
   - OpenClaw = orchestrateur / agent local ;
   - MCP = bus d'outils ;
   - LONA = strategy lab / backtest ;
   - opt-trading = autorité canonique, validation, risk engine, journalisation.

4. **Plan d'exécution réel contrôlé**  
   Définir une séquence opératoire sans clé exchange live, sans skill tiers non audité, sans bypass risk engine.

5. **Indexation / continuité**  
   Branch state local + GAP_INDEXATION si les index globaux ne sont pas modifiés dans cette passe.

## 5_GO_PLAN

GO parent actif :

```text
GO_OPT_TRADING_OPENCLAW_AGENTS_PARENT_LONA_MCP_TMUX_EXEC_01
```

Sous-phases proposées :

- `GO_OPT_TRADING_OPENCLAW_AGENTS_CHILD_SESSION_DOC_01`
- `GO_OPT_TRADING_OPENCLAW_AGENTS_CHILD_RESEARCH_AUDIT_01`
- `GO_OPT_TRADING_OPENCLAW_AGENTS_CHILD_EXECUTION_PLAN_01`
- `GO_OPT_TRADING_OPENCLAW_AGENTS_CHILD_SANDBOX_SMOKE_01`
- `GO_OPT_TRADING_OPENCLAW_AGENTS_CHILD_CLOSEOUT_01`

## 6_FINAL_TARGET

Livrable final attendu :

- documentation autonome ;
- architecture validée ;
- procédure tmux/OpenClaw/MCP/LONA ;
- garde-fous sécurité ;
- plan de smoke test ;
- point de reprise opératoire.

## 7_CANONICAL_STATE

### 13_ESTABLISHED

- Le repo canonique reste `opt-trading`.
- La branche dédiée ouverte est :
  - `go/GO_OPT_TRADING_OPENCLAW_AGENTS_PARENT_LONA_MCP_TMUX_EXEC_01`
- La base de création est :
  - `sot/mainline` commit `254083c3716a3937912ee453fe7f5009feaa5620`
- LONA doit être traité comme un laboratoire de stratégie/backtest.
- OpenClaw ne doit pas recevoir de secrets trading ou wallet sans sandbox stricte.
- tmux est le cockpit Linux recommandé.

### 14_HYPOTHESIS

- LONA peut produire un gain réel comme accélérateur de prototypage Backtrader et comparaison de stratégies.
- OpenClaw peut orchestrer la couche agent/MCP si les permissions restent confinées.
- Le pont utile est un module futur `modules/lona_mcp_bridge/` ou `modules/openclaw_lona_lab/`.

### 15_REMAINING_GAP

- Pas encore de smoke réel sur la machine cible.
- Pas encore d'API key LONA validée.
- Pas encore de configuration OpenClaw auditée sur ce chantier.
- Pas encore de mapping exact vers scripts existants `opt-trading`.

## 8_VALIDATED_PLAN

Plan initial validé par la demande utilisateur :

1. créer branche dédiée ;
2. documenter la session ;
3. approfondir recherches ;
4. documenter l'exécution réelle ;
5. présenter le plan ;
6. conserver point de reprise.

## 11_KEY_DECISIONS

- Ne pas faire de live trading direct via LONA.
- Ne pas installer de skill OpenClaw tiers non audité.
- Ne pas exposer wallets, clés exchange, SSH keys, `.env`, tokens ou secrets à un MCP non confiné.
- Garder `risk_engine`, `webhook_server`, journalisation et validation `opt-trading` comme passage obligé.

## 12_INVARIANTS

- Source canonique : `opt-trading`.
- Branch dédiée obligatoire pour ce parent.
- Exécution réelle = sandbox / paper / backtest d'abord.
- Pas de bypass du risk engine.
- Pas d'accès credential par défaut.
- Pas de promotion live sans closeout PASS.

## 16_TODO

- Lire/maintenir `01_SESSION_DOCUMENTATION_INTEGRALE.md`.
- Lire/maintenir `02_RESEARCH_NOTES.md`.
- Lire/maintenir `03_EXECUTION_PLAN_REAL.md`.
- Produire smoke script tmux en lot enfant.
- Mettre à jour index globaux dans un lot dédié ou garder `GAP_INDEXATION.md` explicite.

## 17_RESUME_POINT

Reprendre depuis :

```text
branche: go/GO_OPT_TRADING_OPENCLAW_AGENTS_PARENT_LONA_MCP_TMUX_EXEC_01
chantier: docs/chantiers/GO_OPT_TRADING_OPENCLAW_AGENTS_PARENT_LONA_MCP_TMUX_EXEC_01/
prochaine action: vérifier docs, puis ouvrir enfant sandbox smoke
```
