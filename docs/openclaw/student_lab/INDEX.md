---
doc_id: OPENCLAW_STUDENT_LAB_INDEX
doc_type: student_lab_status
repo: opt-trading
go_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_STUDENT_LAB_STATUS_01
updated_at: 2026-05-30
---

# docs/openclaw/student_lab — Statut lab OpenClaw sur student

Lab OpenClaw conditionnel sur la machine `student` (Local Ollama).
Distinct du runtime principal db-layer — isolation stricte.

---

## Statut global

```
E2E path   = PROUVÉ (chemin complet validé)
Opérationnel = NON (limitation modèle deepseek-r1:1.5b)
Phase 1    = hors scope — lab non actif en production
```

---

## Configuration lab

```
machine        : student
user           : openclaw-lab  (distinct de openclaw sur db-layer)
gateway port   : 18790         (distinct de 18789 sur db-layer)
gateway bind   : 127.0.0.1    (local only — pas d'exposition LAN)
ollama port    : 11434         (local)
modèle actuel  : deepseek-r1:1.5b
```

## Isolation stricte

```
Ne pas confondre avec le runtime principal :
  db-layer : user=openclaw, port=18789, gateway=ACTIF EN PRODUCTION
  student  : user=openclaw-lab, port=18790, gateway=LAB CONDITIONNEL

Règle : aucune dérive du lab student vers le runtime principal.
```

---

## Chemin E2E prouvé

Source : `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_E2E_SMOKE_01/40_E2E_SMOKE_RESULT.md`

```
Commande : openclaw agent --to +15555550123 --message "Reply exactly: OK" --json --timeout 40

Résultat :
  runId    : ca072168-7758-4fa4-9ffc-653eaf6fef21
  status   : ok
  provider : ollama
  model    : deepseek-r1:1.5b
  duration : 937ms

Chemin validé :
  OpenClaw agent → Gateway WebSocket 127.0.0.1:18790
    → provider ollama
    → Ollama 127.0.0.1:11434
    → deepseek-r1:1.5b
    → réponse reçue
```

Prérequis appliqués :
- `openclaw config set gateway.port 18790` (alignement port)
- `auth-profiles.json` créé avec profil ollama (api_key dummy — Ollama local sans auth)

---

## Limitation bloquante

```
deepseek-r1:1.5b ne supporte pas le function calling (tools).
OpenClaw envoie systématiquement des outils → réponse 400 :
  "does not support tools"

Conséquence : le chemin E2E est prouvé mais le lab n'est pas opérationnel.
Aucun agent OpenClaw ne peut accomplir de tâche structurée avec ce modèle.
```

---

## GOs historiques student lab

| GO | Statut | Contenu |
| --- | --- | --- |
| `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_WORKSPACE_SLIM_01` | CLOSED | Slim workspace, réduction prompt/timeouts |
| `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_E2E_SMOKE_01` | CLOSED | E2E smoke — chemin prouvé, limites identifiées |
| `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_WORKSPACE_SLIM_REALIGN_01` | REALIGN | Branches historiques trop divergentes — reprise depuis WORKSPACE_SLIM_01 |
| `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_MODEL_PULL_EVAL_04_RETRY` | inconnu | Évaluation pull modèle (retry) |

---

## Next step

```
GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_MODEL_EVALUATION_01

Objectif : identifier un modèle Ollama sur student compatible function calling
           pour une utilisation opérationnelle avec OpenClaw.

Candidats à évaluer :
  - llama3.1 (supporte tools via Ollama)
  - mistral-nemo (supporte tools)
  - qwen2.5 (supporte tools)

Condition de fermeture GAP 6 :
  Un modèle compatible function calling prouvé sur student
  → lab devient conditionnellement opérationnel
```

---

## Vérification locale (sur student)

```bash
# État OpenClaw lab
openclaw status
openclaw config get gateway.port   # doit retourner 18790

# Modèles disponibles
ollama list

# Health gateway lab
curl http://127.0.0.1:18790/health 2>/dev/null || echo "gateway non actif"
```
