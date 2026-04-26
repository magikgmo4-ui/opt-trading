---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: openclaw_operator_bridge
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
status: open
lifecycle_stage: cadrage
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-04-26
topic_keys:
  - openclaw
  - orchestrator
  - opt-trading
  - gateway
  - security
  - telegram
  - tmux
  - ssh
reference_canonique_principale: docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/SESSION_REPRISE.txt
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/01_RESEARCH_OPENCLAW_DEEP_DIVE.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/02_SECURITY_MODEL.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/03_RUNTIME_TOPOLOGY_AND_IMPLEMENTATION_PLAN.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/BRANCH_STATE.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/GAP_INDEXATION.md
---

# 00_INITIAL_PROJECT_DOC — GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01

## 1_MASTER_TARGET

Préparer un chantier parent indépendant de la session pour cadrer OpenClaw comme couche opérateur sécurisée autour de l'orchestrateur `opt-trading`.

OpenClaw est étudié comme interface, agent runner et Gateway local ou self-hosted. Le chantier doit éviter de confondre OpenClaw avec l'orchestrateur canonique. L'orchestrateur canonique reste dans `opt-trading` : gouvernance, GO_XXXX, validations, logs, sécurité, modules, preuves repo et continuité.

## 2_INITIAL_PROJECT_DOC

Ce fichier est le document transporteur initial du projet. Il fige la réponse initiale complète produite dans la session, sous une forme documentaire sûre et réutilisable.

## 3_INITIAL_NEED

Demande initiale : recherche très approfondie de tout ce qui comporte les mots OpenClaw pour préparer l'orchestrateur.

Demande suivante : ouvrir un chantier parent dans une branche dédiée, documenter l'intégralité de la réponse pour rendre le chantier indépendant de la session, approfondir les recherches et affiner la documentation.

## 4_MASTER_PROJECT_PLAN

1. Ouvrir un chantier parent dans une branche dédiée.
2. Documenter l'intégralité de la réponse initiale pour rendre le chantier indépendant de la session.
3. Approfondir les recherches publiques sur OpenClaw par axe : Gateway, installation, remote access, auth, sandbox, nodes, Telegram, skills, sécurité.
4. Traduire les résultats en architecture `opt-trading` : OpenClaw comme opérateur, pas comme source souveraine.
5. Définir une topologie cible multi-machines : `db-layer`, `admin-trading`, `student`, Android Termux.
6. Définir le futur module `modules/openclaw_operator_bridge/`.
7. Poser les invariants de sécurité avant toute exécution réelle.
8. Préparer un point de reprise opératoire clair.

## 5_GO_PLAN

GO parent : `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01`

Branche dédiée : `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01`

Rattachement produit / surface : famille de soutien `openclaw / agents / prompt factory` dans `opt-trading`.

## 6_FINAL_TARGET

Livrable attendu au démarrage : dossier chantier complet contenant la réponse initiale, la recherche approfondie, le modèle de sécurité, la topologie runtime, le plan d'implémentation, l'état branche, la trace d'indexation et le point de reprise.

## Réponse initiale complète conservée

### 1_MASTER_TARGET — OpenClaw pour notre orchestrateur

OpenClaw est un assistant IA local ou self-hosted, centré autour d’un Gateway qui connecte modèles IA, canaux de chat, outils système, skills, mémoire, navigateur, fichiers et automatisations. Son intérêt pour notre orchestrateur : devenir une couche opérateur 24/7 pilotable via Telegram, SSH et tmux, avec exécution locale contrôlée, sandbox et routage multi-agent.

### 13_ESTABLISHED — Ce qui est établi

| Axe | Données utiles |
|---|---|
| Nature | Assistant personnel open source exécuté sur tes machines. |
| Gateway | Port par défaut 18789 ; contrôle, routage, dashboard, sessions. |
| Runtime | Node 24 recommandé, Node 22.14+ supporté. |
| Canaux | Telegram, WhatsApp, Slack, Discord, Signal, Matrix, Teams, etc. |
| Setup recommandé | `openclaw onboard --install-daemon`. |
| Docker | Optionnel ; utile pour Gateway isolé ou déploiement serveur. |
| Sandbox | Optionnel ; utile pour limiter le rayon d'impact des outils. |
| Auth | Accès distant à protéger par token, password, tunnel, tailnet ou proxy de confiance. |
| Telegram | Canal rapide : token bot, pairing et allowlist. |
| Skills | Écosystème utile, mais à traiter comme surface de risque jusqu'à audit. |

### 14_HYPOTHESIS — Lecture pour notre orchestrateur

OpenClaw ne devrait pas être traité comme l’orchestrateur canonique lui-même.

Meilleur rôle probable :

```text
OpenClaw = opérateur / interface / agent runner
Notre orchestrateur = gouvernance, routage, sécurité, GO_XXXX, repo, logs, validation
```

Donc :

```text
Telegram / Android / SSH / tmux
        ↓
OpenClaw Gateway
        ↓
Orchestrateur opt-trading
        ↓
Modules: repo, GitHub, trading, LocalCMS, bot vision, logs, ClickUp, Ace KG
```

### 12_INVARIANTS — Sécurité à ne pas rouvrir

1. Ne pas exposer `18789` publiquement.
2. Pas de skills non audités dans le setup trading.
3. Sandbox obligatoire pour sessions non-main, groupes ou agents secondaires.
4. API keys plus stables que OAuth/subscriptions pour serveur 24/7.
5. Séparer les frontières de confiance.

### 15_REMAINING_GAP — Points à valider avant implémentation

| Sujet | À valider |
|---|---|
| db-layer | État réel OpenClaw : service, port, logs, config, auth, permissions. |
| Android Termux | Rôle exact : client SSH/tmux seulement, ou node OpenClaw local. |
| Multi-postes | 1 Gateway central vs 2 Gateways spécialisés. |
| Sécurité | Tailscale/SSH tunnel/token/password/firewall. |
| Skills | Liste blanche minimale pour repo/trading uniquement. |
| Logs | Format journalisable dans `opt-trading`. |

### 16_TODO — Plan préparatoire orchestrateur

#### Phase 1 — Inventaire réel

```bash
openclaw --version
openclaw gateway status
openclaw doctor
openclaw channels list
openclaw models status --probe
```

#### Phase 2 — Architecture cible

Créer une doc chantier :

```text
docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/
  00_INITIAL_PROJECT_DOC.md
  01_RESEARCH_OPENCLAW_DEEP_DIVE.md
  02_SECURITY_MODEL.md
  03_RUNTIME_TOPOLOGY_AND_IMPLEMENTATION_PLAN.md
  BRANCH_STATE.md
  GAP_INDEXATION.md
  SESSION_REPRISE.txt
```

#### Phase 3 — Décision topologie

Option recommandée actuelle :

```text
db-layer = Gateway OpenClaw principal
admin-trading = exécution trading / modules sensibles
student = lab / sandbox / tests
Android Termux = terminal mobile SSH/tmux uniquement
```

#### Phase 4 — Orchestrateur

Créer une couche `openclaw_operator_bridge` dans `opt-trading` :

```text
modules/openclaw_operator_bridge/
  app/
  scripts/
  config/
  commands/
  docs/
  sanity_check.sh
  cmd.sh
  menu.sh
```

Rôle : transformer les demandes OpenClaw en commandes contrôlées `GO_XXXX`, pas en shell libre.

### 17_RESUME_POINT

```text
GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
Objectif : cadrer OpenClaw comme couche opérateur sécurisée pour l’orchestrateur opt-trading.
Prochaine action : audit réel de db-layer + enrichissement recherche + plan d'implémentation.
```

### 18_TO_DOCUMENT

Blocs à extraire :

- `OPENCLAW_DEEP_RESEARCH_PUBLIC_01`
- `OPENCLAW_SECURITY_INVARIANTS_01`
- `OPENCLAW_ORCHESTRATOR_TOPOLOGY_01`
- `OPENCLAW_OPERATOR_BRIDGE_PLAN_01`

### 19_TO_REMEMBER

Memory Bricks projet, pas mémoire bio :

- OpenClaw = opérateur/interface/agent runner, pas orchestrateur canonique.
- `18789` ne doit pas être exposé publiquement.
- Android Termux = client SSH/tmux par défaut.
- Gateway principal pressenti : `db-layer`.
- Exécution sensible trading reste côté `admin-trading`.

## Sources publiques à suivre

- Documentation officielle OpenClaw : `https://docs.openclaw.ai/`
- Documentation Getting Started : `https://docs.openclaw.ai/start/getting-started`
- Documentation Docker : `https://docs.openclaw.ai/install/docker`
- Documentation sandboxing : `https://docs.openclaw.ai/gateway/sandboxing`
- Documentation remote access : `https://docs.openclaw.ai/gateway/remote`
- Documentation authentication : `https://docs.openclaw.ai/gateway/authentication`
- Documentation pairing : `https://docs.openclaw.ai/pairing`
- Dépôt GitHub officiel à valider : `https://github.com/openclaw/openclaw`
- Listes communautaires de skills à traiter comme non auditées jusqu'à preuve contraire.

## 7_CANONICAL_STATE

- Branche dédiée ouverte : `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01`.
- Base déclarée : `sot/mainline` au commit `79b54f6f004ccb9b637a18d3ae02966e1afca07c`.
- Statut : `OPEN / CADRAGE`.
- Ce fichier est la référence initiale figée.
- Les documents suivants portent l'affinage : `01`, `02`, `03`.

## 8_VALIDATED_PLAN

1. Lire la documentation officielle OpenClaw.
2. Lire les signaux de risque publics récents.
3. Séparer `ETABLI`, `HYPOTHESIS`, `TODO`.
4. Préparer une topologie sûre.
5. Reporter toute exécution réelle à un GO enfant après audit machine.

## 9_SELECTED_SOLUTION

Solution retenue : OpenClaw comme couche opérateur et interface agentique, sous contrôle d'un bridge `opt-trading`, avec restrictions fortes.

## 10_SELECTED_SETUP

```text
db-layer      -> Gateway OpenClaw principal pressenti
admin-trading -> modules trading sensibles et exécution réelle
student       -> lab / sandbox / validation
Android       -> Termux SSH/tmux client, pas runtime critique par défaut
```

## 11_KEY_DECISIONS

- Ne pas traiter OpenClaw comme source souveraine.
- Ne pas exposer Gateway directement sur Internet.
- Ne pas installer de skills tiers non audités.
- Préférer API key pour serveur long-lived.
- Mettre les opérations sensibles derrière `GO_XXXX` et bridge contrôlé.

## 12_INVARIANTS

- Pas de shell libre depuis Telegram vers `admin-trading`.
- Pas de commande trading réelle sans garde `GO_XXXX` + validation.
- Pas de skills marketplace non vérifiés.
- Pas de Gateway public sans auth forte.
- Pas de confusion entre chat mobile et exécution canonique.

## 13_ESTABLISHED

Voir la réponse initiale conservée et le document `01_RESEARCH_OPENCLAW_DEEP_DIVE.md`.

## 14_HYPOTHESIS

- `db-layer` est probablement le meilleur hôte Gateway.
- Deux Gateways peuvent être utiles seulement si on sépare production et lab.
- Android doit rester client SSH/tmux sauf preuve contraire.

## 15_REMAINING_GAP

- État réel OpenClaw sur `db-layer`.
- État réel Docker / permission runtime.
- Auth réelle configurée.
- Canaux réellement actifs.
- Logs et fichiers config exacts.

## 16_TODO

1. Auditer `db-layer`.
2. Auditer `student`.
3. Auditer `admin-trading` côté exposition réseau.
4. Créer `modules/openclaw_operator_bridge/` dans un GO enfant seulement après cadrage.
5. Écrire une whitelist de commandes.
6. Définir les contrats JSON d'entrée/sortie.

## 17_RESUME_POINT

Repartir de `SESSION_REPRISE.txt`, puis lire ce fichier `00_INITIAL_PROJECT_DOC.md`, puis `01`, `02`, `03`.
