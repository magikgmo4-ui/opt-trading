# 10_CONVERGENCE_COMPONENT_MAP

## Objectif

Definir les composants convergents de l'architecture WHY.

## Composants

| Composant | Role |
| --- | --- |
| WHY parser | lire les sections et gaps documentaires |
| WHY score generator | calculer une maturite WHY contextualisee |
| WHY worker audit | orchestrer les rapports d'audit |
| WHY runtime graph | cartographier surfaces, machines et relations |
| WHY governance dashboard | visualiser risques, gaps et reviews |
| WHY lint experiment | signaler warnings documentaires |

## Relations principales

| Source | Cible | Relation |
| --- | --- | --- |
| parser | score generator | fournit sections/gaps |
| score generator | worker audit | fournit score et penalites |
| runtime graph | worker audit | fournit relations runtime/governance |
| worker audit | dashboard | fournit rapports |
| lint experiment | dashboard | fournit warnings |
| dashboard | human review | prepare la review humaine |

## Regles

- Chaque composant doit rester explicable.
- Les composants critiques doivent rester audit-oriented.
- Les surfaces R4/R5 doivent garder review humaine.
- Aucun composant ne doit agir seul sur le runtime.

## Invariant

La convergence WHY ne doit jamais produire d'autorite runtime autonome.
