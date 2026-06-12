# 30_LOCALCMS_TMUX_LINKAGE_MODEL

## 1_MASTER_TARGET

Formaliser le modele canonique de liaison `LocalCMS <-> TMUX <-> WHY graph` pour les premieres surfaces runtime centrales.

## WHY

Le point cle n'est pas seulement que `LocalCMS` et `TMUX` existent, mais qu'ils peuvent etre relies sans confusion entre source runtime, consumer read-only, artefact de preuve et overlay documentaire.

## 7_CANONICAL_STATE

Modele de liaison retenu :

| Noeud source | Relation | Noeud cible | Sens documentaire |
| --- | --- | --- | --- |
| `TMUX_SESSION` | `HOSTS_OR_EXPOSES` | `RUNTIME_SURFACE` | la session rend visible une unite runtime nommee |
| `TMUX_PANE` | `PROVES` | `RUNTIME_STATE` | le pane et ses logs servent de preuve d'etat |
| `LOCALCMS_VIEW` | `READS_OR_SUMMARIZES` | `TMUX_SESSION` | `LocalCMS` lit ou synthetise les surfaces de session |
| `LOCALCMS_VIEW` | `READS_OR_SUMMARIZES` | `OBSERVABILITY_ARTIFACT` | `LocalCMS` peut afficher captures, indexations ou rapports lies |
| `HUMAN_REVIEW_GATE` | `GOVERNS` | `LOCALCMS_VIEW` | la lecture read-only reste sous gate humain si ambiguite |
| `HUMAN_REVIEW_GATE` | `GOVERNS` | `TMUX_SESSION` | la criticite runtime garde review humaine |

Lecture canonique :

1. `TMUX` fournit la structure runtime primaire.
2. `LocalCMS` fournit la surface de lecture et de navigation.
3. Le WHY graph relie ces deux couches en distinguant execution, lecture et preuve.
4. Les artefacts et journals viennent ensuite raffiner ces relations, sans les remplacer.

## 8_LINKAGE_RULES

- `READS_OR_SUMMARIZES` ne doit jamais etre relu comme `CONTROLS`.
- `PROVES` ne doit jamais etre relu comme `RUNS`.
- une vue `LocalCMS` doit pointer vers des surfaces `TMUX` nommees ou des artefacts relies ;
- une session `TMUX` critique doit rester sous review humaine explicite ;
- ce modele prepare le graph mais ne declenche aucun render reel a ce stade.

## 12_INVARIANTS

- Aucun edge n'autorise un pilotage `LocalCMS` des sessions `TMUX`.
- Aucun edge n'autorise un runtime live.
- Aucun edge n'ouvre un connecteur ou une CI.

## 17_RESUME_POINT

Le prochain GO daily journal devra accrocher `run_id`, snapshots et chronologies sur ce modele de liaison deja stabilise entre consumer et spine runtime.

## RISKS

- À qualifier.
