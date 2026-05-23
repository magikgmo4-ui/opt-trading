---
doc_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_RESIDUAL_WARNINGS_01_FIX_OR_ACCEPTANCE_PLAN
doc_type: plan
repo: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_RESIDUAL_WARNINGS_01
status: active
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 40_FIX_OR_ACCEPTANCE_PLAN

## Objectif

Converger vers l’un des deux états finaux :

- `STEP 5 = PASS`
ou
- `STEP 5 = WARN_ACCEPTED_WITH_EXPLICIT_POLICY`

## Pré-étape obligatoire : classification (sans patch)

Pour chaque warning (`ENV`, `PORTS`, `PATHS`, `stale_machines`) :

- identifier la source exacte (entrée `required_*` vs `optional_*`, path/port/clé)
- décider si l’élément est réellement requis pour le runtime “fleet utile”

Sortie attendue : une table “WARN → cause → action” conservée dans `20_...` et `30_...`.

## Stratégie A — Viser PASS (corriger ou reparamétrer)

### A1. ENV

- Si Telegram/OpenAI doivent être actifs pour le healthcheck : garantir présence via EnvironmentFiles + éventuellement promouvoir en `required_env`.
- Si les clés sont hors-scope pour `db-layer` : retirer les clés de `optional_env` dans la scope machine.

### A2. PORTS

- Garder uniquement les ports réellement attendus sur `db-layer`.
- Si `openclaw_gateway` est une condition de “fleet ok”, passer le port en `required_ports`.
- Si `algo_hf_api` n’est pas requis, le retirer de `optional_ports`.

### A3. PATHS

- Aligner les chemins attendus avec l’état réel :
  - si `/shared` n’est pas un mount standard, retirer ou remplacer par le chemin réellement retenu
  - si `/var/log/trading` n’est pas une surface voulue sur `db-layer`, retirer du check

### A4. stale_machines

Choisir l’une des options :

- restaurer la publication `latest.json` (timer + data_dir + collecte), ou
- retirer ces machines de la map, ou
- ajouter un flag d’exclusion fleet (nécessite patch code).

## Stratégie B — WARN_ACCEPTED_WITH_EXPLICIT_POLICY (accepter sans dégrader le signal)

Politique minimale opposable (doc-only) :

- lister précisément les warnings autorisés (par machine, par check, par cause)
- justifier : “optionnel / non-runtime / machine atelier”
- indiquer le critère de requalification en FAIL (ex: “gateway down”, “required_paths absents”, “unreachable non vide”)

Politique recommandée (si besoin d’automatisation) :

- introduire un artefact repo-first (YAML/JSON) décrivant les warnings acceptés
- patcher l’orchestrateur de validation (ou la lecture humaine STEP 5) pour convertir :
  - `WARN` → `WARN_ACCEPTED_WITH_EXPLICIT_POLICY`
  - sans masquer le détail (conserver les checks en WARN dans l’artefact)

## Critère de décision (PASS vs WARN_ACCEPTED)

PASS recommandé seulement si :

- aucun WARN utile n’est perdu (pas de “silencing” de défauts réels)
- l’état PASS correspond à un runtime réellement souhaité (services/ports/paths effectivement attendus)

Sinon : préférer `WARN_ACCEPTED_WITH_EXPLICIT_POLICY` (plus honnête et stable).

