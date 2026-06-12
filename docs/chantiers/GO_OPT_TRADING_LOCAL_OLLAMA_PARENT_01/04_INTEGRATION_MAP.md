---
doc_id: GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01_INTEGRATION_MAP

doc_type: integration_map
repo: opt-trading
project: opt-trading
module: local-ai

go_id: GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01
status: draft
lifecycle_stage: integration_mapping
topic_keys:
  - ollama
  - openclaw
  - opencode
  - telegram
  - rag
  - trading-vision
  - python
  - agents
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-04-24
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/04_INTEGRATION_MAP.md
point_de_reprise: "17_RESUME_POINT"
links:
  - docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/00_PARENT_CADRAGE.md
  - docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/01_SYNTHESE_OLLAMA_LOCAL.md
  - docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/02_MACHINE_QUALIFICATION_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/03_SECURITY_BASELINE.md
---

# 04_INTEGRATION_MAP

## 1_MASTER_TARGET

Cartographier les intégrations Ollama pertinentes pour `opt-trading` : OpenClaw, OpenCode, Telegram, RAG documentaire, trading vision et scripts Python.

Ce document ne valide aucune intégration runtime. Il prépare les sous-GO d'application.

## 3_INITIAL_NEED

Relier Ollama à l'écosystème existant sans créer de couplage dangereux :

- ne pas remplacer les outils cloud haut de gamme sans benchmark ;
- ne pas exposer le serveur local ;
- ne pas donner de shell libre à un agent ;
- ne pas injecter secrets et logs sensibles ;
- garder les sorties exploitables et vérifiables.

## 4_MASTER_PROJECT_PLAN

Approche en couches :

```text
Ollama runtime
  -> API native / OpenAI-compatible
    -> clients locaux
      -> intégrations contrôlées
        -> artefacts opt-trading
```

Intégrations à prioriser :

1. scripts Python contrôlés ;
2. RAG documentaire local ;
3. OpenCode / IDE ;
4. OpenClaw ;
5. Telegram bot ;
6. trading vision.

## 7_CANONICAL_STATE

État initial :

- chantier parent ouvert ;
- aucune intégration appliquée ;
- sécurité baseline requise ;
- qualification machine requise ;
- API Ollama locale supposée sur `127.0.0.1:11434` seulement ;
- tous les usages actifs doivent passer par sous-GO.

## 8_VALIDATED_PLAN

Plan d'intégration :

1. choisir machine hôte ;
2. valider sécurité ;
3. tester API locale ;
4. tester script Python minimal ;
5. tester sortie JSON ;
6. intégrer un seul outil ;
7. journaliser ;
8. closeout ;
9. seulement ensuite étendre.

## 12_INVARIANTS

- Pas de multi-intégration en une seule passe.
- Pas d'agent shell libre.
- Pas de trading live.
- Pas d'exposition publique.
- Pas d'écriture repo automatique sans revue.
- Pas de RAG sans source traçable.
- Pas de vision trading sans validation humaine.
- Pas de dépendance à une seule machine sans fallback.

## 13_ESTABLISHED — Interfaces utiles

### API native Ollama

- `POST /api/chat` ;
- `POST /api/generate` ;
- `POST /api/embeddings` ;
- `GET /api/version` ;
- `GET /api/ps` ;
- `GET /api/tags`.

### API OpenAI-compatible

- `base_url=http://localhost:11434/v1/` ;
- `api_key=ollama` valeur factice pour certains clients ;
- utile pour clients qui attendent OpenAI.

## 20_INTEGRATION_OPENCLAW

### Objectif

Tester Ollama comme backend local ou provider local pour OpenClaw/gateway.

### Usage potentiel

- agent local privé ;
- exécution de tâches hors cloud ;
- lecture docs locales ;
- pairing avec outils élevés désactivés ou strictement contrôlés ;
- fallback local.

### Risques

- OpenClaw peut orchestrer des outils puissants ;
- risque d'accès fichiers/shell ;
- confusion entre modèle local et agent système ;
- charge machine ;
- port gateway + port Ollama à sécuriser.

### Conditions avant test

```text
MACHINE_QUALIFICATION=PASS
SECURITY_BASELINE=PASS
OLLAMA_LOCAL_API=PASS
OPENCLAW_NO_ELEVATED_TOOLS=CONFIRMED
LOGS=ENABLED
```

### Sous-GO proposé

`GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_OPENCLAW_PROVIDER_01`

## 21_INTEGRATION_OPENCODE

### Objectif

Utiliser Ollama comme provider local pour assistance code/terminal, selon compatibilité OpenAI ou provider spécifique.

### Usage potentiel

- aide au code offline ;
- génération de commandes ;
- lecture de petits fichiers ;
- explication de logs ;
- brouillons de patch ;
- smoke checklist.

### Risques

- mauvais patch si modèle faible ;
- commande shell dangereuse ;
- hallucination de chemins ;
- écriture non revue.

### Garde-fous

- mode suggestion d'abord ;
- pas d'auto-apply ;
- fichiers allowlist ;
- diff obligatoire ;
- tests obligatoires ;
- validation humaine.

### Sous-GO proposé

`GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_AGENT_IDE_01`

## 22_INTEGRATION_TELEGRAM

### Objectif

Permettre à un bot Telegram interne d'utiliser Ollama pour résumer, classifier ou pré-analyser des messages/images.

### Usage potentiel

- résumé de screenshot ;
- analyse rapide de contexte ;
- classification `trade_setup`, `log_error`, `system_status` ;
- retour JSON pour pipeline ;
- pré-analyse avant ChatGPT cloud.

### Risques

- Telegram comme entrée non fiable ;
- injection de prompt ;
- image mal interprétée ;
- déclenchement d'action non souhaitée ;
- fuite de contexte.

### Garde-fous

- bot read-only au départ ;
- pas de shell ;
- pas de write repo ;
- pas de trading live ;
- JSON Schema ;
- allowlist chat id ;
- logs filtrés ;
- taille image contrôlée.

### Sous-GO proposé

`GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_TELEGRAM_READONLY_01`

## 23_INTEGRATION_RAG_DOCUMENTAIRE

### Objectif

Créer un assistant local capable de chercher dans la documentation `opt-trading` et de répondre avec contexte.

### Corpus initial possible

- `docs/chantiers/` ;
- `docs/governance/` ;
- `docs/index/` ;
- `modules/*/README*` ;
- closeouts validés ;
- prompts workflow validés.

### Architecture proposée

```text
docs source
  -> chunker
    -> embeddings Ollama
      -> vector store local
        -> retriever
          -> chat model Ollama
            -> réponse avec citations locales
```

### Modèles

- embeddings : `nomic-embed-text` ou `mxbai-embed-large` ;
- chat : modèle stable selon benchmark machine.

### Sortie exigée

```json
{
  "answer": "...",
  "sources": ["path:line-range"],
  "confidence": "low|medium|high",
  "remaining_gap": ["..."]
}
```

### Risques

- vieux documents non filtrés ;
- contradiction canonique ;
- absence de citations ;
- contexte trop gros ;
- mélange docs actives et archives.

### Garde-fous

- prioriser `docs/governance` et `docs/index` ;
- respecter la hiérarchie documentaire ;
- citer chemins et lignes si possible ;
- exclure secrets/logs bruts ;
- séparer archive et actif.

### Sous-GO proposé

`GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_RAG_DOCS_01`

## 24_INTEGRATION_TRADING_VISION

### Objectif

Utiliser Ollama vision pour pré-analyser des screenshots TradingView ou captures Telegram, sans décision autonome.

### Usage potentiel

- détecter type de capture ;
- résumer structure visuelle ;
- extraire éléments grossiers : tendance, zone, bougie, annotation ;
- produire checklist de setup ;
- enrichir journal de trading.

### Sortie JSON recommandée

```json
{
  "image_type": "chart|screenshot|unknown",
  "symbol_guess": "string|null",
  "timeframe_guess": "string|null",
  "visible_bias": "bullish|bearish|range|unclear",
  "key_visual_elements": ["..."],
  "risk_notes": ["..."],
  "not_reliable_for": ["price_precision", "order_execution"],
  "human_review_required": true
}
```

### Risques

- lecture de prix incorrecte ;
- mauvaise reconnaissance timeframe ;
- hallucination de niveaux ;
- surconfiance ;
- confusion entre capture actuelle et ancienne.

### Garde-fous

- human review obligatoire ;
- pas d'ordre ;
- pas de signal final ;
- comparer avec données réelles si disponibles ;
- journaliser l'image source et l'heure.

### Sous-GO proposé

`GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_TRADING_VISION_01`

## 25_INTEGRATION_SCRIPTS_PYTHON

### Objectif

Créer des scripts Python simples pour appeler Ollama de façon contrôlée.

### Usages

- `ollama_chat.py` ;
- `ollama_json_extract.py` ;
- `ollama_embed_doc.py` ;
- `ollama_vision_describe.py` ;
- `ollama_log_analyze.py`.

### Client natif HTTP minimal

```python
import requests

payload = {
    "model": "llama3.2",
    "messages": [{"role": "user", "content": "Réponds en JSON."}],
    "format": "json",
    "stream": False,
    "options": {"temperature": 0},
}

r = requests.post("http://127.0.0.1:11434/api/chat", json=payload, timeout=120)
r.raise_for_status()
print(r.json())
```

### Client OpenAI-compatible minimal

```python
from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:11434/v1/", api_key="ollama")

response = client.chat.completions.create(
    model="llama3.2",
    messages=[{"role": "user", "content": "Réponds en une phrase."}],
)

print(response.choices[0].message.content)
```

### Garde-fous

- timeout obligatoire ;
- retries limités ;
- logs sans secrets ;
- JSON validation ;
- pas de shell depuis modèle ;
- dossiers input/output explicités.

### Sous-GO proposé

`GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_PYTHON_CLIENTS_01`

## 26_PRIORITY_MATRIX

| Intégration | Priorité | Risque | Valeur | Verdict initial |
|---|---:|---:|---:|---|
| Scripts Python | P0 | faible | haute | premier test recommandé |
| RAG documentaire | P0 | moyen | haute | très pertinent |
| OpenCode / IDE | P1 | moyen | moyen/haut | après machine benchmark |
| OpenClaw | P1 | élevé | haut | après sécurité stricte |
| Telegram | P2 | élevé | moyen/haut | read-only seulement |
| Trading vision | P2 | élevé | expérimental | lab only au départ |

## 27_NEXT_GO_CANDIDATES

1. `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_MACHINE_QUALIFICATION_01`
2. `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_PYTHON_CLIENTS_01`
3. `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_RAG_DOCS_01`
4. `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_AGENT_IDE_01`
5. `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_OPENCLAW_PROVIDER_01`
6. `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_TELEGRAM_READONLY_01`
7. `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_TRADING_VISION_01`

## 28_RECOMMENDED_SEQUENCE

Séquence recommandée :

```text
1. MACHINE_QUALIFICATION
2. SECURITY_BASELINE_CHECK
3. PYTHON_CLIENTS_MINIMAL
4. RAG_DOCS_LOCAL
5. AGENT_IDE
6. OPENCLAW_PROVIDER
7. TELEGRAM_READONLY
8. TRADING_VISION_LAB
```

Raison : commencer par faible risque et forte utilité avant agents/vision.

## 17_RESUME_POINT

Reprise :

- fichier : `04_INTEGRATION_MAP.md` ;
- état : cartographie intégrations créée ;
- prochain GO recommandé : `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_MACHINE_QUALIFICATION_01` ;
- première intégration recommandée après qualification : `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_PYTHON_CLIENTS_01` ;
- première intégration produit forte : `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_RAG_DOCS_01`.

## RISKS

- À qualifier.
