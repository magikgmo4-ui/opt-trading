---
doc_id: GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module:
go_id: GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01
status: active
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - runtime
  - tmux
  - opencode
  - openclaw
  - telegram
surface: chantier
source_kind: canonical
updated_at: 2026-04-16
links:
  - docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/01_plan.md
  - docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/02_journal_technique.md
  - docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/03_decisions.md
---

# 00_cadrage — GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01

## Identité
- GO : GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01
- Repo : opt-trading
- Branche : sot/mainline
- Statut : active
- Type de travail : chantier parent runtime opératoire
- Classification retenue : module durable — architecture d’utilisation
- Rôle recommandé : architecte runtime + opérateur IA

## État de départ retenu
- besoin retenu : piloter `opt-trading` depuis n’importe où avec continuité de session, agents IA actifs et contrôle distant sans dépendre du SSH en continu
- état établi de la session : le plan logique du setup a été validé, mais il n’est pas encore figé dans la documentation Git du repo
- état technique retenu : la cible distingue explicitement `tmux`, `OpenCode`, `OpenClaw` et `Telegram` avec des rôles séparés
- contrainte de méthode : ce chantier ouvre le parent documentaire et borne les sous-chantiers sans lancer encore l’implémentation
- statut documentaire : parent ouvert pour figer le cadre de travail ; canonisation documentaire fine reportée à une passe ultérieure

## Objectif du lot
- objectif principal : figer dans `docs/chantiers/` le parent runtime et ses sous-chantiers directs afin d’avoir un point de reprise Git propre
- résultat attendu : un dossier parent contenant le cadrage, le plan, le journal initial et les décisions stabilisées sur la répartition des rôles et les sous-chantiers à ouvrir ensuite

## Cible finale retenue
Mettre en place une architecture d’utilisation où :
- `tmux` porte la persistance runtime
- `OpenCode` porte la production / code engine
- `OpenClaw` porte l’orchestration / control plane
- `Telegram` porte l’interface distante
- l’ensemble forme un système vivant en continu plutôt qu’une simple session locale

## Sous-chantiers pressentis
- `GO_TMUX_RUNTIME_CONVENTIONS_01`
- `GO_OPENCLAW_COMMAND_SCOPE_01`
- `GO_TMUX_RUNTIME_CONTRACT_01`
- `GO_TMUX_OPENCODE_OPENCLAW_MODES_01`
- `GO_RUNTIME_GUARDRAILS_01`

## Non-objectifs
- implémenter maintenant le setup sur machine
- verrouiller encore la canonisation documentaire finale
- ouvrir des patches techniques repo hors du périmètre runtime
- décrire l’installation détaillée des briques dans ce lot parent

## Critères PASS / FAIL
- PASS si : le parent fige clairement le besoin, la cible, la répartition des rôles et le découpage en sous-chantiers avec un point de reprise net
- FAIL si : les rôles restent ambigus, les sous-chantiers ne sont pas explicités ou le parent pousse déjà vers l’implémentation
