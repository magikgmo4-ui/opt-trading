# 01_ENDPOINT_REVALIDATION_REPORT

doc_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01_REVALIDATION
go_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01
validated_at: 2026-05-14
endpoint: https://opencode.ai/zen/v1/models

## Revalidation endpoint

Endpoint interroge le 2026-05-14. 41 modeles retournes. Comparaison avec le registry actuel (20 modeles, date 2026-04-26).

## Changements detectes

### CONFIRMES — Toujours VERIFIED/VERIFIED_FREE (12)

| Modele | Statut precedent | Statut courant | Endpoint |
|--------|------------------|----------------|----------|
| glm-5.1 | VERIFIED | VERIFIED | present |
| glm-5 | VERIFIED | VERIFIED | present |
| kimi-k2.5 | VERIFIED | VERIFIED | present |
| kimi-k2.6 | VERIFIED | VERIFIED | present |
| minimax-m2.7 | VERIFIED | VERIFIED | present |
| minimax-m2.5 | VERIFIED | VERIFIED | present |
| minimax-m2.5-free | VERIFIED_FREE | VERIFIED_FREE | present |
| qwen3.6-plus | VERIFIED | VERIFIED | present |
| qwen3.5-plus | VERIFIED | VERIFIED | present |
| big-pickle | VERIFIED | VERIFIED | present |
| nemotron-3-super-free | VERIFIED_FREE | VERIFIED_FREE | present |
| gpt-5-nano | VERIFIED | VERIFIED | present |

### PROMUS — ABSENT → VERIFIED (1+)

| Modele | Statut precedent | Statut courant | Endpoint ID |
|--------|------------------|----------------|-------------|
| deepseek-v4-flash-free | ABSENT_CURRENT_ENDPOINT (ancien ID: `deepseek-v4-flash`) | VERIFIED_FREE | `deepseek-v4-flash-free` |

Note: le modele etait liste comme `deepseek-v4-flash` dans le registry precedent. L'endpoint renvoie `deepseek-v4-flash-free`. L'ancienne entree est remplacee.

### AJOUTES — Nouveaux dans l'endpoint (2)

| Modele | Statut | Autonomie | Endpoint ID |
|--------|--------|-----------|-------------|
| ring-2.6-1t-free | VERIFIED_FREE | A1 | `ring-2.6-1t-free` |
| trinity-large-preview-free | VERIFIED_FREE | A1 | `trinity-large-preview-free` |

Note: `ring-2.6-1t-free` pourrait etre le successeur de `ling-2.6-flash-free` (retire, voir ci-dessous).

### RETIRES — Disparus de l'endpoint (2)

| Modele | Statut precedent | Statut courant | Raison |
|--------|------------------|----------------|--------|
| hy3-preview-free | VERIFIED_FREE | RETIRED_CURRENT_ENDPOINT | absent endpoint 2026-05-14 |
| ling-2.6-flash-free | VERIFIED_FREE | RETIRED_CURRENT_ENDPOINT | absent endpoint 2026-05-14 |

Note: `ring-2.6-1t-free` semble etre le remplacant de `ling-2.6-flash-free` (nom similaire, meme famille free). Le registry le note comme successeur possible.

### INCHANGES — Toujours ABSENT (5)

| Modele | Statut |
|--------|--------|
| mimo-v2-pro | ABSENT_CURRENT_ENDPOINT |
| mimo-v2-omni | ABSENT_CURRENT_ENDPOINT |
| mimo-v2.5-pro | ABSENT_CURRENT_ENDPOINT |
| mimo-v2.5 | ABSENT_CURRENT_ENDPOINT |
| deepseek-v4-pro | ABSENT_CURRENT_ENDPOINT |

## Bilan

| Statut | Avant | Apres | Delta |
|--------|-------|-------|-------|
| VERIFIED | 10 | 10 | 0 |
| VERIFIED_FREE | 4 | 6 | +2 |
| RETIRED | 0 | 2 | +2 |
| ABSENT | 6 | 5 | -1 |
| TOTAL | 20 | 23 | +3 |

3 nouveaux modeles ajoutes (1 promu + 2 nouveaux). 2 retires. Pool net : +1 modele.

## Mise a jour tasks.index.json

Retraits des preferred_workers :
- `ling-2.6-flash-free` retire de READ_INVENTORY et FAST_TRIAGE
- `hy3-preview-free` retire de READ_INVENTORY et DOC_DRAFT

Ajouts aux preferred_workers :
- `deepseek-v4-flash-free` ajoute a READ_INVENTORY et FAST_TRIAGE
- `ring-2.6-1t-free` ajoute a READ_INVENTORY et FAST_TRIAGE
- `trinity-large-preview-free` ajoute a READ_INVENTORY (conservatif, A1)

## Verdict revalidation

Les changements sont documentes, motives (endpoint courant), et coherents avec la doctrine strict_workers. Aucun modele RETIRED n'est route. Aucun modele ABSENT n'est promu sans preuve endpoint. Le pool est etendu de maniere bornee et sure.

## RISKS

- À qualifier.
