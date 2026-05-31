---
doc_id: OPENCLAW_LOOP_CONTRACT_INDEX
doc_type: loop_contract_index
repo: opt-trading
go_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_LOOP_CONTRACT_01
updated_at: 2026-05-30
---

# docs/openclaw/loop_contract — Boucle ChatGPT ↔ OpenClaw ↔ IDE

Formalisation contractuelle des 5 segments de la boucle d'orchestration OpenClaw.

## Architecture de la boucle

```
ChatGPT (gouvernance / conversationnel)
    │
    │──[ FORMAT 1 ]──────────────────────────────────────────────────────▶
    │                 job spec : intent + scope + contraintes + output attendu
    ▼
OpenClaw (orchestrateur)
    │
    │──[ FORMAT 2 ]──────────────────────────────────────────────────────▶
    │                 instruction structurée : commande + fichiers + opérations autorisées
    ▼
IDE / agent / job (exécution)
    │
    │──[ FORMAT 3 ]──────────────────────────────────────────────────────▶
    │                 résultat structuré : status + diff + evidence + artefacts
    ▼
OpenClaw (orchestrateur)
    │
    │──[ FORMAT 4 ]──────────────────────────────────────────────────────▶
    │                 synthèse : verdict + next + question gate humain
    ▼
ChatGPT (gouvernance)
    │
    │──[ FORMAT 5 ]──────────────────────────────────────────────────────▶
    │                 gate humain : APPROVE / REJECT / RESTART + motif
    ▼
[relance ou clôture]
```

## Formats

| Format | Segment | Fichier |
| --- | --- | --- |
| FORMAT 1 | ChatGPT → OpenClaw | [01_chatgpt_to_openclaw.md](01_chatgpt_to_openclaw.md) |
| FORMAT 2 | OpenClaw → IDE | [02_openclaw_to_ide.md](02_openclaw_to_ide.md) |
| FORMAT 3 | IDE → OpenClaw | [03_ide_to_openclaw.md](03_ide_to_openclaw.md) |
| FORMAT 4 | OpenClaw → ChatGPT | [04_openclaw_to_chatgpt.md](04_openclaw_to_chatgpt.md) |
| FORMAT 5 | Gate humain | [05_human_gate.md](05_human_gate.md) |

## Règles générales de la boucle

```
1. ChatGPT ne déclenche jamais directement un IDE — passe toujours par OpenClaw.
2. OpenClaw ne merge jamais sans gate humain explicite (FORMAT 5).
3. Un résultat PARTIAL ou FAIL stoppe la boucle — pas de relance automatique.
4. Chaque segment produit un artefact horodaté loggable.
5. Le gate humain peut APPROVE / REJECT / RESTART avec motif obligatoire.
```

## Statut

```
5 formats définis — doc-only — aucun runtime modifié
```
