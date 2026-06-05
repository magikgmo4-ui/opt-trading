---
doc_id: GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01_PARENT_CADRAGE

doc_type: chantier_parent_cadrage
repo: opt-trading
project: opt-trading
module: local-ai

go_id: GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01
status: open
lifecycle_stage: cadrage_parent
topic_keys:
  - opt-trading
  - local-ai
  - ollama
  - local-llm
  - agents
  - openclaw
  - opencode
  - trading-vision
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-04-24
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/00_PARENT_CADRAGE.md
point_de_reprise: "17_RESUME_POINT"
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
---

# GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01 — Chantier parent Ollama local

## 1_MASTER_TARGET

Créer un chantier parent dédié à l'étude, la qualification et l'intégration potentielle d'Ollama comme socle IA local dans `opt-trading`.

Le chantier doit produire une lecture stable des capacités, limites, usages, risques, intégrations et prochaines étapes autour d'Ollama en local, sans appliquer de patch runtime tant qu'aucun sous-GO technique n'est validé.

## 2_INITIAL_PROJECT_DOC

Ce document est le document transporteur initial du chantier parent.

Il fixe :
- la demande initiale ;
- le périmètre ;
- les invariants ;
- le plan de travail ;
- les sous-GO proposés ;
- les critères de validation ;
- le point de reprise.

Il reste la référence de démarrage du chantier sauf changement explicite ou implicite validé.

## 3_INITIAL_NEED

Demande utilisateur :

> Fais une synthèse complète de Ollama en local ... Les limites, les capacités, les utilisations... Tout ce que tu peux trouver.

Puis demande de cadrage repo :

> Commence par créer un chantier parent sur une branche dédiée, et documente ta réponse dans tous les détails ainsi que les étapes suivantes. @GitHub

## 4_MASTER_PROJECT_PLAN

Direction générale : qualifier Ollama comme composant possible du stack `opt-trading`, en distinguant clairement :

1. documentation et compréhension ;
2. qualification machine ;
3. sécurité réseau ;
4. intégration agent/IDE ;
5. intégration RAG documentaire ;
6. intégration vision/trading ;
7. décision finale d'adoption ou de rejet par usage.

Le chantier parent reste doc-first. Les actions machines et runtime doivent être ouvertes en sous-GO séparés.

## 5_GO_PLAN

### Phase A — Documentation / compréhension

Produire une fiche de synthèse complète :
- architecture Ollama ;
- API locale ;
- modèles ;
- capacités ;
- limites ;
- matériel ;
- sécurité ;
- cas d'usage ;
- critères de choix vs alternatives.

### Phase B — Qualification machine

Qualifier séparément les machines candidates :
- `student` ;
- `admin-trading` ;
- `db-layer` ;
- `cursor-ai` si nécessaire.

À valider : CPU, RAM, GPU, OS, stockage, réseau, port `11434`, modèles réalistes.

### Phase C — Sécurité locale

Établir une doctrine minimale :
- localhost par défaut ;
- pas d'exposition Internet directe ;
- firewall ;
- reverse proxy seulement si besoin ;
- permissions fichiers ;
- séparation agents/outils ;
- logs et audit.

### Phase D — Intégrations opt-trading

Étudier puis tester, sous-GO séparés :
- OpenClaw ;
- OpenCode ;
- Codex / IDE ;
- scripts Python ;
- Telegram bot ;
- RAG docs ;
- analyse screenshot/chart ;
- journalisation structurée.

### Phase E — Verdict produit

Classer les usages en :
- `ADOPT_NOW` ;
- `ADOPT_WITH_LIMITS` ;
- `LAB_ONLY` ;
- `REJECT_FOR_NOW`.

## 6_FINAL_TARGET

Livrable parent attendu : un dossier de chantier canonique permettant de reprendre et exécuter les sous-GO sans dépendre de la conversation.

Livrables cibles :
- `00_PARENT_CADRAGE.md` — présent document ;
- `01_SYNTHESE_OLLAMA_LOCAL.md` — fiche complète Ollama local ;
- `02_MACHINE_QUALIFICATION_PLAN.md` — plan de qualification par machine ;
- `03_SECURITY_BASELINE.md` — baseline sécurité ;
- `04_INTEGRATION_MAP.md` — cartographie intégrations ;
- `90_PARENT_CLOSEOUT.md` — à produire à la fermeture.

## 7_CANONICAL_STATE

État canonique au démarrage :

- Repo : `magikgmo4-ui/opt-trading`.
- Branche canonique source : `sot/mainline`.
- Branche dédiée ouverte : `go/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01`.
- Commit de base identifié : `4934eefcbc373e0f33167a24f35443fad46a8c80`.
- Nature du lot : documentation / cadrage parent.
- Aucun patch runtime autorisé par ce document.
- Aucune installation machine autorisée tant qu'un sous-GO technique n'est pas explicitement ouvert.

## 8_VALIDATED_PLAN

Plan validé pour ce commit :

1. confirmer le repo GitHub et la branche canonique ;
2. créer une branche dédiée parent ;
3. créer le dossier chantier parent ;
4. documenter le cadrage complet ;
5. proposer les étapes suivantes ;
6. ne pas modifier le runtime ;
7. ne pas ouvrir de PR avant validation explicite si non demandée.

## 9_SELECTED_SOLUTION

Approche retenue : chantier parent doc-first avec branche dédiée.

Raison : Ollama touche plusieurs surfaces possibles : local AI, machines, sécurité, agents, vision, RAG et trading. Une branche parent évite de mélanger cadrage, tests machines et intégrations runtime.

## 10_SELECTED_SETUP

Structure documentaire retenue :

```text
docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/
├── 00_PARENT_CADRAGE.md
├── 01_SYNTHESE_OLLAMA_LOCAL.md
├── 02_MACHINE_QUALIFICATION_PLAN.md
├── 03_SECURITY_BASELINE.md
├── 04_INTEGRATION_MAP.md
└── 90_PARENT_CLOSEOUT.md
```

Support Git :

```text
base: sot/mainline
branche: go/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01
```

## 11_KEY_DECISIONS

- Décision 1 : ouvrir un chantier parent, pas un GO simple.
- Décision 2 : utiliser une branche dédiée, car le sujet est multi-surface.
- Décision 3 : commencer par documentation et qualification, pas installation immédiate.
- Décision 4 : considérer Ollama comme serveur d'inférence local, pas comme simple interface de chat.
- Décision 5 : séparer les usages chat, agent code, RAG, vision, Telegram et trading.
- Décision 6 : maintenir `NO_RUNTIME_PATCH` au démarrage.
- Décision 7 : imposer une baseline sécurité avant exposition réseau.

## 12_INVARIANTS

- Ne pas exposer Ollama publiquement sans doctrine sécurité explicite.
- Ne pas supposer que local = sécurisé.
- Ne pas installer ou modifier une machine dans ce parent sans sous-GO dédié.
- Ne pas remplacer GPT/Claude/API cloud par Ollama sans comparaison par usage.
- Ne pas utiliser un modèle local pour décisions trading non vérifiées.
- Ne pas ouvrir de flux autonome sans logs, limites et garde-fous.
- Ne pas confondre modèle, runtime Ollama, interface WebUI et agent IDE.

## 13_ESTABLISHED

Établi au démarrage :

- Ollama peut servir de runtime local pour modèles LLM open-weight.
- Le port local usuel est `11434`.
- Les usages potentiels touchent : code, chat, embeddings, RAG, vision, agents, analyse de logs.
- Les limites dépendent fortement de la machine, du modèle, de la quantization et de la taille du contexte.
- La sécurité réseau est un point critique.
- Le chantier doit être découpé avant toute application machine.

## 14_HYPOTHESIS

Hypothèses à valider :

- `student` pourrait servir de laboratoire local AI léger/moyen.
- `db-layer` pourrait devenir cible pour OpenClaw/Ollama ou stockage RAG selon ressources.
- `admin-trading` ne devrait probablement pas porter des charges IA lourdes si cela menace les services trading.
- `cursor-ai` pourrait être meilleure surface d'orchestration IDE que surface d'inférence permanente.
- Ollama pourrait être utile pour RAG documentaire local et pré-analyse de logs, plus que pour décisions complexes autonomes.

## 15_REMAINING_GAP

Manques à combler :

- inventaire matériel réel des machines ;
- liste des modèles à tester ;
- mesure tokens/s par machine ;
- mesure RAM/VRAM ;
- décision CPU-only vs GPU ;
- baseline sécurité validée ;
- comparaison Ollama vs LM Studio vs llama.cpp direct vs cloud API ;
- choix d'un premier usage utile dans `opt-trading`.

## 16_TODO

Prochaines actions proposées :

1. créer `01_SYNTHESE_OLLAMA_LOCAL.md` avec la synthèse complète ;
2. créer `02_MACHINE_QUALIFICATION_PLAN.md` avec commandes Bash/PowerShell ;
3. créer `03_SECURITY_BASELINE.md` ;
4. créer `04_INTEGRATION_MAP.md` ;
5. ouvrir un sous-GO machine si validation : `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_MACHINE_QUALIFICATION_01` ;
6. ouvrir un sous-GO intégration si validation : `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_INTEGRATION_RAG_01` ou `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_AGENT_IDE_01` ;
7. produire un closeout parent après synthèse + plan.

## GO_PROMPT

Prompt de reprise recommandé :

```text
GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01

Reprendre le chantier parent Ollama local depuis :
docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/00_PARENT_CADRAGE.md

Contraintes :
- repo opt-trading ;
- branche go/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01 ;
- base sot/mainline ;
- doc-first ;
- NO_RUNTIME_PATCH ;
- aucun test machine sans sous-GO explicite ;
- produire ensuite 01_SYNTHESE_OLLAMA_LOCAL.md, 02_MACHINE_QUALIFICATION_PLAN.md, 03_SECURITY_BASELINE.md, 04_INTEGRATION_MAP.md.

Objectif immédiat : produire la synthèse Ollama local complète et actionnable, puis préparer les sous-GO de qualification.
```

## 17_RESUME_POINT

Reprendre ici :

- Branche : `go/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01`.
- Document principal : `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/00_PARENT_CADRAGE.md`.
- État : chantier parent ouvert, doc-first.
- Prochaine action : créer `01_SYNTHESE_OLLAMA_LOCAL.md`.
- Interdit courant : pas d'installation, pas de patch runtime, pas d'exposition réseau.

## 18_TO_DOCUMENT

À documenter dans les fichiers suivants :

- `01_SYNTHESE_OLLAMA_LOCAL.md` : synthèse complète des capacités, limites, usages.
- `02_MACHINE_QUALIFICATION_PLAN.md` : qualification par machine.
- `03_SECURITY_BASELINE.md` : sécurité réseau et usage agent.
- `04_INTEGRATION_MAP.md` : OpenClaw, OpenCode, Telegram, RAG, trading vision.
- `90_PARENT_CLOSEOUT.md` : verdict final du parent.

## 19_TO_REMEMBER

Memory Bricks candidates, à extraire plus tard si validé :

- `OLLAMA_LOCAL_PARENT_OPENED`
- `OLLAMA_NO_RUNTIME_PATCH_AT_PARENT_STAGE`
- `OLLAMA_SECURITY_BASELINE_REQUIRED_BEFORE_NETWORK_EXPOSURE`
- `OLLAMA_MACHINE_QUALIFICATION_REQUIRED_BEFORE_ADOPTION`

## RISKS

- À qualifier.
