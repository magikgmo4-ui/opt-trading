---
doc_id: GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01_DECISION_LAB_STUDENT_OPENCLAW_ORCHESTRATION

doc_type: decision_record
repo: opt-trading
project: opt-trading
module: local-ai

go_id: GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01
status: accepted
lifecycle_stage: decision
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-04-24
topic_keys:
  - ollama
  - student
  - lab
  - openclaw
  - orchestration
  - local-ai
  - decision
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/06_DECISION_LAB_STUDENT_OPENCLAW_ORCHESTRATION.md
point_de_reprise: "17_RESUME_POINT"
links:
  - docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/00_PARENT_CADRAGE.md
  - docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/01_SYNTHESE_OLLAMA_LOCAL.md
  - docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/02_MACHINE_QUALIFICATION_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/03_SECURITY_BASELINE.md
  - docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/04_INTEGRATION_MAP.md
  - docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/05_INFRA_RANKING_AND_USAGE.md
---

# 06_DECISION_LAB_STUDENT_OPENCLAW_ORCHESTRATION

## 1_MASTER_TARGET

Canoniser la décision corrigée : Ollama doit être considéré comme une capacité locale portée par une machine lab/student, avec documentation complète de ses possibilités actuelles, et avec OpenClaw comme orchestrateur potentiel.

## 3_INITIAL_NEED

Correction utilisateur :

> L'important est que Ollama est pour une machine et qu'on documente ses possibilité actuel comme lab/student orchestrer par Openclaw.

## 7_CANONICAL_STATE

État canonique corrigé :

- Ollama est destiné à une machine dédiée de type `student` / laboratoire.
- La machine lab porte l'exploration locale des capacités Ollama.
- OpenClaw est la couche d'orchestration à étudier pour ce lab.
- Le périmètre exact d'usage reste plus large que trading / dual stack : il inclut aussi documentation, agents, scripts, RAG, analyse locale et exploration des modèles.
- `admin-trading` reste protégé et non cible serveur par défaut.
- `db-layer` n'est pas la cible initiale, mais peut rester une option future si le lab démontre une valeur claire.
- `cursor-ai` peut rester client/opérateur, pas cible serveur initiale.

## 11_KEY_DECISIONS

1. Ollama est associé à une seule machine lab au démarrage.
2. La machine de référence est `student` ou équivalent lab/student.
3. L'objectif est de documenter les possibilités actuelles réelles d'Ollama dans ce contexte.
4. OpenClaw devient l'orchestrateur potentiel à qualifier autour d'Ollama.
5. Le chantier ne se limite pas à trading dual stack, même si le trading lab reste un usage possible.
6. L'approche reste non-production au démarrage.
7. La sécurité reste bloquante avant toute exposition réseau ou agent outillé.
8. Les capacités doivent être prouvées par tests réels sur la machine lab.

## 12_INVARIANTS

- Une machine lab dédiée porte Ollama au démarrage.
- Pas de dispersion multi-machine avant validation.
- Pas d'installation ou serveur Ollama lourd sur `admin-trading`.
- Pas d'exposition publique.
- Pas d'agent shell libre.
- OpenClaw doit être étudié comme orchestrateur, pas activé en mode dangereux par défaut.
- Les capacités actuelles doivent être documentées par preuves : version, modèles, API, performance, limites.
- Le trading live reste hors périmètre.

## 13_ESTABLISHED

Usages à documenter dans le lab :

- exécution de modèles locaux ;
- API native Ollama ;
- compatibilité OpenAI ;
- sorties JSON structurées ;
- embeddings ;
- RAG documentaire local ;
- vision si modèle disponible ;
- scripts Python ;
- orchestration OpenClaw ;
- interactions agent/outils sous contraintes ;
- analyse de logs ;
- interrogation de scénarios trading ou dual stack ;
- aide à la documentation et à la reprise de GO.

## 14_HYPOTHESIS

Hypothèses à valider :

- OpenClaw peut servir de couche d'orchestration au-dessus d'Ollama pour le lab.
- Ollama peut servir de provider local pour des tâches simples à moyennes.
- La valeur principale initiale sera probablement : scripts + RAG + interrogation + orchestration contrôlée.
- Les limites matérielles de `student` détermineront les modèles réalistes.

## 15_REMAINING_GAP

À combler :

- mesure réelle de `student` ;
- état actuel d'Ollama sur la machine si déjà installé ;
- version OpenClaw et mode de connexion ;
- provider local supporté ;
- modèle(s) disponibles ;
- performance ;
- niveau d'orchestration acceptable ;
- garde-fous pour outils ;
- format des preuves à journaliser.

## 16_TODO

Prochaines actions :

1. ouvrir un sous-GO lab/student ;
2. qualifier la machine ;
3. vérifier si Ollama est installé ;
4. vérifier API locale ;
5. tester modèle minimal ;
6. tester JSON strict ;
7. tester embeddings si possible ;
8. qualifier OpenClaw comme orchestrateur ;
9. documenter les possibilités réelles observées ;
10. classer les usages en `READY`, `LIMITED`, `LAB_ONLY`, `REJECT`.

## 20_OPENCLAW_ORCHESTRATION_SCOPE

### Rôle OpenClaw envisagé

OpenClaw doit être étudié comme orchestrateur local au-dessus d'Ollama :

```text
user / operator
  -> OpenClaw
    -> provider Ollama local
      -> modèle local
        -> réponse / JSON / tool proposal
```

### Capacités à vérifier

- connexion à Ollama ;
- choix du modèle ;
- mode OpenAI-compatible ou provider natif ;
- gestion contexte ;
- logs ;
- outils disponibles ;
- désactivation outils élevés ;
- sécurité des commandes ;
- stabilité session.

### Garde-fous

- pas de shell libre ;
- pas d'accès secrets ;
- pas de modification repo automatique ;
- pas de trading live ;
- pas d'exposition publique ;
- localhost d'abord ;
- logs activés.

## 21_USAGE_SCOPE_CORRIGE

### Autorisé au démarrage

```text
machine lab/student
localhost
Ollama local
OpenClaw orchestration à qualifier
scripts contrôlés
RAG local read-only
JSON structuré
analyse/logs/docs
questionnement trading/dual stack
```

### Non autorisé au démarrage

```text
multi-machine production
admin-trading server
exposition publique
agent shell libre
trading live
ordre exchange
écriture repo automatique
```

## 22_SELECTED_SOLUTION

Solution retenue :

```text
Ollama = moteur local sur machine lab/student
OpenClaw = orchestrateur potentiel à qualifier
But = documenter les possibilités actuelles et limites réelles
Mode = lab, non-production, sécurisé, prouvé par tests
```

## 23_NEXT_GO

Sous-GO immédiat recommandé :

```text
GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01
```

Objectif : qualifier la machine lab/student, Ollama local et OpenClaw comme orchestration potentielle.

## 24_GO_PROMPT

```text
GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01

Objectif : qualifier Ollama sur machine lab/student et documenter ses possibilités actuelles, avec OpenClaw comme orchestrateur potentiel.

Sources :
- docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/01_SYNTHESE_OLLAMA_LOCAL.md
- docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/02_MACHINE_QUALIFICATION_PLAN.md
- docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/03_SECURITY_BASELINE.md
- docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/04_INTEGRATION_MAP.md
- docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/05_INFRA_RANKING_AND_USAGE.md
- docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/06_DECISION_LAB_STUDENT_OPENCLAW_ORCHESTRATION.md

Contraintes :
- machine unique lab/student ;
- localhost d'abord ;
- OpenClaw à qualifier comme orchestrateur ;
- pas admin-trading server ;
- pas exposition publique ;
- pas shell libre ;
- pas trading live ;
- documenter version, modèles, API, JSON, embeddings, vision si disponible, limites et verdicts.

Sortie attendue :
- état réel machine ;
- état réel Ollama ;
- état réel OpenClaw ;
- possibilités confirmées ;
- limites confirmées ;
- classement READY / LIMITED / LAB_ONLY / REJECT ;
- prochain GO logique.
```

## 17_RESUME_POINT

Reprise :

- fichier : `06_DECISION_LAB_STUDENT_OPENCLAW_ORCHESTRATION.md` ;
- état : décision corrigée canonisée ;
- cible : machine unique lab/student ;
- orchestrateur à qualifier : OpenClaw ;
- objectif : documenter possibilités actuelles Ollama ;
- prochain GO : `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01`.
