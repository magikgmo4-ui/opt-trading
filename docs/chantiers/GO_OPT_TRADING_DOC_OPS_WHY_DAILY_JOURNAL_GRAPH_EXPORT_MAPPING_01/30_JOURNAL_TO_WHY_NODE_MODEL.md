# 30_JOURNAL_TO_WHY_NODE_MODEL

## 1_MASTER_TARGET

Definir comment les entrees du Daily Journal deviennent des noeuds, preuves et liens du WHY graph sans etre promues en surfaces runtime primaires.

## WHY

Le futur graph doit distinguer clairement la surface observee, le contexte de run et l'artefact de preuve. Sans cette frontiere, un snapshot ou un rapport risque d'etre confondu avec la source runtime elle-meme.

## 7_CANONICAL_STATE

Modele de rattachement retenu :

| Artefact ou snapshot | Noeud cible | Relation | Lecture retenue |
| --- | --- | --- | --- |
| snapshot session | `TMUX_SESSION` | `PROVES` | preuve ponctuelle d'etat ou de presence |
| snapshot vue | `LOCALCMS_VIEW` | `PROVES` | preuve de lecture ou d'exposition read-only |
| rapport ou log reference | `RUN_CONTEXT` | `LINKS_TO` | preuve associee a un `run_id` |
| artefact de synthese | `OBSERVABILITY_ARTIFACT` | `LINKS_TO` | trace secondaire, pas source primaire |

Regle generale :

- la surface runtime ou consumer garde la priorite semantique ;
- le snapshot reste une preuve ponctuelle ;
- l'artefact relie le journal au graphe sans prendre le controle du modele.

## 8_LINKAGE_RULES

- Un snapshot doit conserver sa provenance et sa date.
- Un artefact sans `run_id` ou sans surface reliee reste insuffisant.
- Un snapshot ne doit jamais etre relu comme une commande runtime.
- Un artefact de synthese ne remplace pas une preuve source si elle existe deja.

## 12_INVARIANTS

- Aucun snapshot n'autorise un render/export reel a lui seul.
- Aucun artefact n'autorise une escalation automatique.
- Aucun rattachement n'ouvre un connecteur live.

## 17_RESUME_POINT

La readiness finale du GO devra verifier que ces rattachements suffisent pour ouvrir un export graph reel sans perdre provenance, chronologie ni review humaine.

## RISKS

- À qualifier.
