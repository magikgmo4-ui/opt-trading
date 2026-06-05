---
doc_id: GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01_LAB_USAGE_SCOPE

doc_type: lab_usage_scope
repo: opt-trading
project: opt-trading
module: local-ai

go_id: GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01
status: accepted
lifecycle_stage: scope_definition
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-04-24
topic_keys:
  - ollama
  - lab
  - student
  - openclaw
  - local-models
  - api
  - openai-compatible
  - json
  - embeddings
  - rag
  - vision
  - python
  - logs
  - trading-dual-stack
  - go-reprise
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/07_LAB_USAGE_SCOPE.md
point_de_reprise: "17_RESUME_POINT"
links:
  - docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/00_PARENT_CADRAGE.md
  - docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/01_SYNTHESE_OLLAMA_LOCAL.md
  - docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/02_MACHINE_QUALIFICATION_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/03_SECURITY_BASELINE.md
  - docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/04_INTEGRATION_MAP.md
  - docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/05_INFRA_RANKING_AND_USAGE.md
  - docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/06_DECISION_LAB_STUDENT_OPENCLAW_ORCHESTRATION.md
---

# 07_LAB_USAGE_SCOPE

## 1_MASTER_TARGET

Définir le périmètre exact des usages à documenter dans le laboratoire Ollama sur machine `student` / lab, avec OpenClaw comme orchestrateur potentiel.

Ce document sert de grille de test et de documentation pour le prochain sous-GO :

```text
GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01
```

## 3_INITIAL_NEED

Usages à documenter dans le lab :

- modèles locaux ;
- API Ollama ;
- compatibilité OpenAI ;
- JSON structuré ;
- embeddings ;
- RAG local read-only ;
- vision si disponible ;
- scripts Python ;
- orchestration OpenClaw ;
- analyse de logs/docs ;
- interrogation trading ou dual stack ;
- aide à la reprise GO.

## 7_CANONICAL_STATE

État retenu :

- machine cible : `student` ou machine lab équivalente ;
- mode : laboratoire local ;
- serveur : Ollama local ;
- exposition : localhost par défaut ;
- orchestration : OpenClaw à qualifier ;
- statut : non-production ;
- objectif : documenter capacités réelles et limites observées.

## 12_INVARIANTS

- Pas de production.
- Pas de trading live.
- Pas d'exposition publique.
- Pas d'agent shell libre.
- Pas de modification automatique du repo.
- Pas de secrets dans prompts/logs.
- Pas d'accès `admin-trading` comme serveur Ollama.
- Chaque capacité doit être prouvée par commande, sortie ou capture de statut.
- Les résultats doivent être classés : `READY`, `LIMITED`, `LAB_ONLY`, `REJECT`.

## 13_ESTABLISHED — Grille de documentation des usages

Chaque usage doit être documenté avec :

```text
USAGE_ID=
OBJECTIF=
COMMANDE_OU_TEST=
SORTIE_ATTENDUE=
LIMITES=
RISQUES=
OPENCLAW_IMPACT=
VERDICT=READY|LIMITED|LAB_ONLY|REJECT
NEXT_STEP=
```

## 20_USAGE_01_MODELES_LOCAUX

### Objectif

Documenter les modèles localement disponibles, ceux qui peuvent être téléchargés raisonnablement, et ceux qui sont adaptés à la machine lab.

### Tests minimaux

```bash
ollama --version
ollama list
ollama ps
ollama show <model>
```

### À documenter

- nom modèle ;
- taille ;
- famille ;
- type : chat, code, embedding, vision ;
- contexte ;
- vitesse approximative ;
- stabilité ;
- usage recommandé.

### Verdict possible

- `READY` si modèle fluide et utile ;
- `LIMITED` si lent ou trop petit ;
- `LAB_ONLY` si utile pour tests ;
- `REJECT` si inutilisable.

## 21_USAGE_02_API_OLLAMA

### Objectif

Valider l'API native Ollama en local.

### Tests minimaux

```bash
curl -sS http://127.0.0.1:11434/api/version
curl -sS http://127.0.0.1:11434/api/tags
curl -sS http://127.0.0.1:11434/api/chat -d '{
  "model": "<model>",
  "messages": [{"role":"user","content":"Réponds en une phrase."}],
  "stream": false
}'
```

### À documenter

- API répond ou non ;
- endpoint utilisé ;
- modèle testé ;
- latence ;
- erreurs ;
- charge système.

### Verdict

`READY` seulement si API stable en localhost.

## 22_USAGE_03_COMPATIBILITE_OPENAI

### Objectif

Valider si les outils compatibles OpenAI peuvent utiliser Ollama via `base_url` local.

### Test Python minimal

```python
from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:11434/v1/", api_key="ollama")

response = client.chat.completions.create(
    model="<model>",
    messages=[{"role": "user", "content": "Réponds OK."}],
)
print(response.choices[0].message.content)
```

### À documenter

- endpoint `/v1` fonctionnel ;
- client Python OK ;
- modèle compatible ;
- erreurs éventuelles ;
- intérêt pour OpenClaw/OpenCode.

### OpenClaw impact

Fort : la compatibilité OpenAI peut simplifier la connexion d'OpenClaw à Ollama.

## 23_USAGE_04_JSON_STRUCTURE

### Objectif

Valider les sorties structurées pour pipelines et analyse fiable.

### Test minimal

```bash
curl -sS http://127.0.0.1:11434/api/chat -d '{
  "model": "<model>",
  "messages": [{"role":"user","content":"Retourne un JSON avec status, risk, next_action."}],
  "format": "json",
  "stream": false,
  "options": {"temperature": 0}
}'
```

### Sortie attendue

```json
{
  "status": "...",
  "risk": "...",
  "next_action": "..."
}
```

### Usages opt-trading

- classifier logs ;
- extraire décisions ;
- résumer GO ;
- préparer outputs pour scripts ;
- piloter OpenClaw avec contrats stricts.

## 24_USAGE_05_EMBEDDINGS

### Objectif

Tester les embeddings pour recherche documentaire locale.

### Test minimal

```bash
ollama pull <embedding-model>
curl -sS http://127.0.0.1:11434/api/embeddings -d '{
  "model": "<embedding-model>",
  "prompt": "GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01 lab usage scope"
}'
```

### À documenter

- modèle embeddings ;
- dimension si disponible ;
- temps de réponse ;
- stabilité ;
- taille corpus possible ;
- stockage recommandé.

### Verdict

Priorité haute si stable, car base du RAG local.

## 25_USAGE_06_RAG_LOCAL_READ_ONLY

### Objectif

Tester un RAG local en lecture seule sur les docs `opt-trading`.

### Corpus initial recommandé

```text
docs/governance/
docs/index/
docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/
```

### Architecture

```text
docs -> chunker -> embeddings -> vector store -> retriever -> Ollama chat -> réponse citée
```

### Sortie attendue

```json
{
  "answer": "...",
  "sources": ["path#section"],
  "confidence": "low|medium|high",
  "remaining_gap": ["..."]
}
```

### Limites

- pas d'écriture repo ;
- pas de sources non citées ;
- pas d'archives mélangées au canon sans signalement ;
- pas de décision automatique.

## 26_USAGE_07_VISION_SI_DISPONIBLE

### Objectif

Valider si un modèle vision local peut décrire ou classifier des images utiles en lab.

### Tests possibles

- screenshot TradingView ;
- capture terminal ;
- capture dashboard ;
- image annotée simple.

### Sortie attendue

```json
{
  "image_type": "chart|terminal|dashboard|unknown",
  "visible_elements": ["..."],
  "uncertainties": ["..."],
  "not_reliable_for": ["..."],
  "human_review_required": true
}
```

### Verdict

`LAB_ONLY` par défaut tant que la précision n'est pas mesurée.

## 27_USAGE_08_SCRIPTS_PYTHON

### Objectif

Créer des clients Python simples et contrôlés pour interroger Ollama.

### Scripts cibles

```text
ollama_chat.py
ollama_json_extract.py
ollama_embed_doc.py
ollama_rag_query.py
ollama_vision_describe.py
ollama_log_analyze.py
```

### Règles

- timeout obligatoire ;
- erreurs explicites ;
- aucun secret ;
- aucun shell libre ;
- outputs JSON si pipeline ;
- logs filtrés.

### Verdict

Probablement `READY` après API stable.

## 28_USAGE_09_ORCHESTRATION_OPENCLAW

### Objectif

Qualifier OpenClaw comme orchestrateur au-dessus d'Ollama.

### Questions à vérifier

- OpenClaw peut-il pointer vers Ollama local ?
- Utilise-t-il l'API OpenAI-compatible ?
- Quel modèle est configuré ?
- Les outils élevés sont-ils désactivables ?
- Les logs sont-ils lisibles ?
- Les actions sont-elles contrôlables ?
- Peut-il rester en mode lab sans écrire/modifier ?

### Architecture attendue

```text
user
  -> OpenClaw
    -> Ollama provider local
      -> modèle local
        -> réponse / JSON / proposition d'action
```

### Garde-fous

- aucun shell libre ;
- aucun accès secrets ;
- aucun push Git ;
- aucun patch automatique ;
- aucune action trading ;
- validation humaine obligatoire.

### Verdict

`LIMITED` ou `LAB_ONLY` tant que la sécurité outil n'est pas prouvée.

## 29_USAGE_10_ANALYSE_LOGS_DOCS

### Objectif

Utiliser Ollama pour analyser logs et documents copiés dans un périmètre lab.

### Usages

- résumer erreur ;
- classer incident ;
- proposer smoke checks ;
- extraire commandes pertinentes ;
- générer closeout brouillon ;
- comparer document avec matrice.

### Sortie recommandée

```text
ETABLI=
HYPOTHESE=
RISQUE=
TEST_A_FAIRE=
NEXT_STEP=
```

### Limites

- logs filtrés ;
- pas de secrets ;
- pas d'application automatique ;
- vérifier contre source réelle.

## 30_USAGE_11_INTERROGATION_TRADING_DUAL_STACK

### Objectif

Utiliser Ollama pour questionner les scénarios trading lab / dual stack sans décision automatique.

### Usages

- comparer LAB vs REALTIME ;
- structurer hypothèses ;
- préparer backtests ;
- analyser sortie de backtest ;
- journaliser incertitudes ;
- générer checklist de validation.

### Sortie recommandée

```text
SETUP_OR_QUESTION=
ETABLI=
HYPOTHESE=
INVALIDATION=
TEST_REQUIRED=
RISK=
NEXT_CHECK=
```

### Limites

- pas de signal final ;
- pas d'ordre ;
- pas de confiance sans données ;
- validation humaine requise.

## 31_USAGE_12_AIDE_REPRISE_GO

### Objectif

Utiliser Ollama pour aider à reprendre un chantier sans dépendre de la conversation.

### Entrées

- fichier `00_PARENT_CADRAGE.md` ;
- fichiers `90_CLOSEOUT` ;
- `docs/index/REPRISE.md` ;
- `GO_INDEX.md` ;
- matrice de gouvernance.

### Sortie attendue

```text
1_MASTER_TARGET=
7_CANONICAL_STATE=
11_KEY_DECISIONS=
12_INVARIANTS=
13_ESTABLISHED=
14_HYPOTHESIS=
15_REMAINING_GAP=
16_TODO=
17_RESUME_POINT=
GO_PROMPT=
```

### Verdict

Très pertinent en RAG read-only, après validation embeddings + citations.

## 40_PRIORITE_DE_TEST

| Rang | Usage | Priorité | Risque | Verdict initial |
|---:|---|---:|---:|---|
| 1 | API Ollama | P0 | faible | à tester en premier |
| 2 | modèles locaux | P0 | faible | inventaire obligatoire |
| 3 | JSON structuré | P0 | faible | base pipeline |
| 4 | scripts Python | P0 | faible | meilleur premier client |
| 5 | embeddings | P0 | moyen | base RAG |
| 6 | RAG local read-only | P1 | moyen | haute valeur |
| 7 | analyse logs/docs | P1 | moyen | utile rapidement |
| 8 | aide reprise GO | P1 | moyen | très aligné projet |
| 9 | compatibilité OpenAI | P1 | moyen | nécessaire OpenClaw |
| 10 | OpenClaw orchestration | P2 | élevé | après sécurité |
| 11 | trading dual stack | P2 | élevé | lab seulement |
| 12 | vision | P2 | élevé | si modèle disponible |

## 41_ACCEPTANCE_MATRIX

Un usage est accepté seulement si :

```text
API_LOCAL=PASS
SECURITY_BASELINE=PASS
OUTPUT_VALIDATED=PASS
NO_SECRET_LEAK=PASS
NO_UNCONTROLLED_TOOL=PASS
HUMAN_REVIEW=PASS_WHEN_REQUIRED
```

## 42_NEXT_GO

GO recommandé :

```text
GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01
```

Objectif : exécuter cette grille sur la machine lab/student, puis produire un rapport réel.

## 43_GO_PROMPT

```text
GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01

Objectif : qualifier les usages lab Ollama sur machine student/lab et préparer l'orchestration OpenClaw.

Fichier de référence principal :
docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/07_LAB_USAGE_SCOPE.md

Tester/documenter :
- modèles locaux ;
- API Ollama ;
- compatibilité OpenAI ;
- JSON structuré ;
- embeddings ;
- RAG local read-only ;
- vision si disponible ;
- scripts Python ;
- orchestration OpenClaw ;
- analyse logs/docs ;
- interrogation trading ou dual stack ;
- aide reprise GO.

Contraintes :
- localhost d'abord ;
- lab only ;
- pas de shell libre ;
- pas d'exposition publique ;
- pas de trading live ;
- pas d'écriture repo automatique ;
- verdict par usage : READY / LIMITED / LAB_ONLY / REJECT.
```

## 17_RESUME_POINT

Reprise :

- fichier : `07_LAB_USAGE_SCOPE.md` ;
- état : périmètre des usages lab documenté ;
- prochain GO : `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01` ;
- première preuve à produire : API Ollama locale + inventaire modèles ;
- première valeur à viser : JSON structuré + scripts Python ;
- valeur produit suivante : RAG read-only + aide reprise GO ;
- OpenClaw : à qualifier après compatibilité OpenAI et sécurité.

## RISKS

- À qualifier.
