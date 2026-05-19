# 20_WHY_PARSER_OUTPUT_SCHEMA

## Objectif

Definir le schema de sortie normalise du futur parser WHY.

## Schema conceptuel

```json
{
  "document_path": "string",
  "document_type": "string",
  "detected_sections": [],
  "missing_sections": [],
  "risk_level": "R0-R5",
  "why_score_candidate": 0,
  "gaps": [],
  "warnings": [],
  "resume_point_present": true
}
```

## Champs

| Champ | Role |
| --- | --- |
| document_path | fichier source |
| document_type | type documentaire |
| detected_sections | sections trouvees |
| missing_sections | sections absentes |
| risk_level | criticite runtime candidate |
| why_score_candidate | score preliminaire |
| gaps | problemes critiques |
| warnings | problemes mineurs |
| resume_point_present | reprise detectee |

## Regles

- Le parser ne doit pas inventer une section.
- Les champs absents doivent rester absents.
- Les warnings ne doivent pas etre promus en FAIL automatique.
- Le score reste indicatif tant que la governance WHY n'est pas stabilisee.

## Invariant

La sortie du parser est une aide documentaire et non une source unique de verite.
