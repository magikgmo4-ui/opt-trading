---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_OBSERVATION_TO_PRODUCT_ROADMAP_01
doc_type: next_child_go_decision
repo: opt-trading
status: open
created_at: 2026-05-17
---

# 40_NEXT_CHILD_GO_DECISION

---

## Objectif

Choisir le prochain child GO à ouvrir après que les seuils Phase 1 sont atteints.

**Contrainte principale : aucun child GO suivant ne s'ouvre avant l'éligibilité multi-signal.**

```text
ELIGIBLE = runs >= 30 AND fail_count == 0 AND jours_observation >= 14
Éligible au plus tôt : 2026-05-30
```

---

## Table des options

| Option | Child GO | Axe | Condition |
| --- | --- | --- | --- |
| A | `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_WAIT_OBSERVATION_THRESHOLD_01` | Attendre — ne rien ouvrir | toujours disponible |
| B | `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_LOCALCMS_OBSERVATION_VIEW_01` | UI — LocalCMS lit db-layer | seuil atteint |
| C | `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_OBSERVATION_EVENT_SCHEMA_01` | Data — schéma canonique événement | seuil atteint |
| D | `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_RUNTIME_READINESS_AFTER_OBSERVATION_01` | Runtime — évaluer readiness post-seuil | seuil atteint |
| E | `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_EXTERNAL_JOURNAL_SYNC_DECISION_01` | External — Sheets sync décision | seuil atteint + besoin prouvé |
| F | `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_CLOSEOUT_AFTER_OBSERVATION_01` | Parent closeout | seuil atteint + parent épuisé |

---

## Analyse des options

### Option A — WAIT_OBSERVATION_THRESHOLD

```text
Continuer l'observation sans ouvrir de nouveau child.
La branche Phase 1 reste active.
Ce child GO est fermé après avoir documenté la roadmap.
```

- Quand choisir : si aucune urgence produit n'émerge pendant l'observation.
- Risque : dérive par inertie si aucune revue n'est programmée.
- Recommandé si : l'observation révèle des anomalies à traiter d'abord.

### Option B — OPEN_LOCALCMS_OBSERVATION_VIEW

```text
Ouvrir un child dédié à exposer l'état db-layer dans LocalCMS.
Objectif : LocalCMS lit les métriques d'observation sans dépendre des logs bruts.
```

- Quand choisir : si LocalCMS est le prochain consommateur naturel.
- Valeur : dashboard opérateur cohérent, lisible sans tooling custom.
- Condition : seuil Phase 1 atteint, LocalCMS accessible et stable.

### Option C — OPEN_OBSERVATION_EVENT_SCHEMA

```text
Formaliser le schéma canonique événement db-layer.
Objectif : normaliser les journaux de runs en structure persistable.
```

- Quand choisir : si la priorité est la structure de données avant l'UI.
- Valeur : fondation pour persistence, query, et export cohérents.
- Condition : seuil Phase 1 atteint, volume de runs suffisant pour qualifier le schéma.

### Option D — OPEN_RUNTIME_READINESS_AFTER_OBSERVATION

```text
Évaluer si les conditions sont réunies pour ouvrir un runtime réel après Phase 1.
Objectif : audit readiness — pas d'exécution, seulement évaluation des conditions.
```

- Quand choisir : si l'objectif principal est de qualifier la suite runtime.
- Valeur : décision documentée, non inertielle.
- Condition : seuil Phase 1 atteint, kill switch et guards stables.

### Option E — OPEN_EXTERNAL_JOURNAL_SYNC_DECISION

```text
Décider du rôle de Google Sheets dans le dispositif.
Objectif : clarifier si Sheets reste rail externe ou devient archive canonique.
```

- Quand choisir : seulement si un besoin audit externe explicite est identifié.
- Valeur : évite de relancer Sheets par inertie.
- Condition : besoin réel prouvé — ne pas ouvrir par défaut.

### Option F — PREPARE_PARENT_CLOSEOUT_AFTER_OBSERVATION

```text
Préparer la clôture du parent GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01.
Objectif : évaluer si le parent a atteint sa cible ou doit rester ancre.
```

- Quand choisir : si l'observation prouve que le parent a épuisé son rôle.
- Valeur : gouvernance propre, sans ancre zombie.
- Condition : seuil Phase 1 atteint + tous les sous-GO orphelins résolus.

---

## Décision recommandée (à valider par l'opérateur)

```text
DECISION_COURANTE : A — WAIT_OBSERVATION_THRESHOLD
```

**Pourquoi A maintenant** :
- Les seuils Phase 1 ne sont pas atteints (14/30 runs, 2/14 jours).
- Aucune urgence produit ne justifie d'anticiper un child.
- Ce child GO (roadmap) a documenté la trajectoire — c'est suffisant pour cette passe.

**Suite logique après seuil** :
- Relire ce document à l'éligibilité (≥2026-05-30).
- Choisir entre B (LocalCMS view), C (event schema), ou D (runtime readiness) selon l'état observé.
- Ne pas ouvrir E (Sheets) sans besoin prouvé.
- Ne pas ouvrir F (parent closeout) sans audit complet du parent.

---

## Tableau de statut (à tenir à jour)

| Surface | Statut | Décision |
| --- | --- | --- |
| Observation Phase 1 | Active | Continuer jusqu'au seuil |
| Orchestrator parent | Open | Garder comme ancre |
| LocalCMS view | Candidat produit | À cadrer après seuil |
| Runtime readiness | Candidat après observation | Attendre seuil |
| Google Sheets | Support externe | Ne pas relancer par inertie |
| Remote exec | Dormant | Ne rouvrir que si besoin produit |
| Cleanup | Closed | Ne pas rouvrir |

## RISKS

- À qualifier.
