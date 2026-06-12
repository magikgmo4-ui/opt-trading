# 10_DAILY_JOURNAL_SOURCE_MODEL

## 1_MASTER_TARGET

Definir le Daily Journal comme modele source de contexte temporel et de preuve de run pour le WHY graph.

## WHY

`LocalCMS` et `TMUX` definissent deja qui lit et ou le runtime s'expose. Il manque maintenant la couche qui dit quand un run a eu lieu, sous quel `run_id`, dans quelle chronologie et avec quelles preuves attachees.

## 7_CANONICAL_STATE

Role retenu pour le Daily Journal :

| Dimension | Position retenue |
| --- | --- |
| Nature | trace documentaire de run |
| Fonction graph | contexte temporel, sequencing, provenance de preuve |
| Relation canonique | `RECORDS` des runs, `PROVES` des chronologies, `LINKS_TO` des artefacts |
| Frontiere | ne devient ni orchestrateur runtime ni export graph lui-meme |

Elements structurants attendus :

- `run_id` comme identifiant canonique de run ;
- chronologie d'execution ;
- references de snapshots ;
- references vers sessions, vues ou artefacts lies ;
- review humaine si la preuve est incomplete ou ambigue.

## 8_ROLE_RULES

- Le journal decrit un run ; il ne lance pas un run.
- Une entree de journal doit pointer vers des surfaces ou artefacts nommes.
- Un `run_id` doit etre reutilisable comme ancrage documentaire commun.
- Une chronologie partielle doit rester visible comme partielle.

## 12_INVARIANTS

- Le Daily Journal reste doc-only dans ce GO.
- Le Daily Journal ne remplace ni `TMUX`, ni `LocalCMS`, ni les artefacts source.
- Le Daily Journal n'autorise aucun export reel a lui seul.

## 17_RESUME_POINT

Le mapping suivant devra transformer ce role en liaisons explicites entre `run_id`, sessions `TMUX`, vues `LocalCMS` et snapshots documentes.

## RISKS

- À qualifier.
