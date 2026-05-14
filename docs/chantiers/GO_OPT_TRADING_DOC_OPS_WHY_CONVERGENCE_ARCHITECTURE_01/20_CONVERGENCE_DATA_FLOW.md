# 20_CONVERGENCE_DATA_FLOW

## Objectif

Definir les flux de donnees entre les couches WHY.

## Flux candidats

| Source | Destination | Donnees |
| --- | --- | --- |
| parser | score generator | sections, gaps, metadata |
| parser | lint experiment | structure documentaire |
| runtime graph | worker audit | relations runtime |
| score generator | worker audit | score WHY |
| lint experiment | worker audit | warnings |
| worker audit | dashboard | rapports audit |
| runtime graph | dashboard | visualisation runtime |
| dashboard | human review | preparation validation |

## Types de donnees

| Type | Usage |
| --- | --- |
| markdown | synthese humaine |
| json | sorties machine-readable |
| graph relations | visualisation runtime |
| review metadata | governance humaine |

## Regles

- Les flux doivent rester tracables.
- Les surfaces critiques doivent rester contextualisees.
- Les warnings doivent rester explicables.
- Les preuves runtime doivent rester auditables.

## Invariant

Les flux WHY ne doivent jamais devenir une orchestration runtime autonome.
