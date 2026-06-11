---
doc_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_CHILD_TRADEMACHINEOFF_PILOT_01_GAPS_AND_NEXT_GO
go_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_CHILD_TRADEMACHINEOFF_PILOT_01
doc_type: gaps_next_go
status: draft_reference
created_at: 2026-06-11
---

# 40_GAPS_AND_NEXT_GO

## Gaps ouverts

| Gap | Statut | Commentaire |
|---|---|---|
| Source registry runtime | OPEN | `registry/youtube_sources.jsonl` n'existe pas encore comme artefact valide. |
| Collector YouTube | OPEN | Aucun collecteur runtime n'est valide dans ce patch. |
| Subtitle/transcript extraction | OPEN | Methode definie par le parent, non prouvee. |
| OCR | OPEN | Methode definie par le parent, non prouvee. |
| Parser runtime | OPEN | Profil defini, implementation non prouvee sur Shorts reels. |
| Fixtures | OPEN | 5 fixtures pilotes restent a annoter. |

## Risques

- OCR peut alterer les chiffres de prix.
- Audio peut contredire le texte ecran.
- Certains Shorts peuvent etre uniquement promotionnels ou educatifs.
- Le parser peut sur-detecter `long` / `short` dans du contexte historique.

## Garde-fous

- Conserver raw avant parser.
- Mettre `unknown` ou `null` au lieu d'inventer.
- Marquer explicitement les conflits.
- Ne pas promouvoir la source en active sans fixtures.

## Next GO candidates

```text
GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_CHILD_TRADEMACHINEOFF_PILOT_RUN_01
GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_CHILD_PARSER_RUNTIME_V1_01
GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_CHILD_SOURCE_REGISTRY_RUNTIME_01
```

## Reprise

Le prochain lot doit choisir entre :

1. appliquer ce patch d'ouverture child ;
2. lancer le run pilote sur `@trademachineoff` ;
3. extraire le parser runtime si le run montre que la logique doit etre codee avant annotation.

