# 20_GRAPH_EXPORT_MAPPING_RULES

## 1_MASTER_TARGET

Formaliser les regles de mapping du Daily Journal vers les surfaces centrales du WHY graph export.

## WHY

Sans ancrage explicite des `run_id`, le futur export graph reel risque de produire des noeuds et edges runtime sans contexte d'execution ni ordre temporel verifiable.

## 7_CANONICAL_STATE

Modele de mapping retenu :

| Element journal | Cible graph | Sens retenu |
| --- | --- | --- |
| `run_id` | `RUN_CONTEXT` | identifiant canonique de reference |
| timestamp / sequence | `TIMELINE_EDGE` | ordre des etapes et des etats |
| reference session | `TMUX_SESSION` | rattachement a la spine runtime observee |
| reference vue | `LOCALCMS_VIEW` | rattachement a la lecture read-only eventuelle |
| reference machine | `MACHINE` ou `RUNTIME_SURFACE` | contexte d'hebergement ou de domaine |

Lecture canonique :

1. Un `run_id` ouvre un contexte de run unique.
2. La chronologie de journal ordonne les etapes observees.
3. Chaque etape doit pointer vers une surface ou un artefact explicitement nomme.
4. Le graph devra pouvoir traverser `run_id -> session -> preuve` sans inference implicite.

## 8_MAPPING_RULES

- Un `run_id` sans surface reliee reste incomplet.
- Une timeline sans ordre explicite ne doit pas etre reinterpretee artificiellement.
- Une vue `LocalCMS` referencee par journal reste une lecture, pas une commande.
- Une session `TMUX` referencee par journal reste une surface observee, pas un trigger automatique.

## 12_INVARIANTS

- Aucun mapping ici n'autorise un runtime live.
- Aucun mapping ici n'autorise un export reel immediat.
- Aucun mapping ici ne supprime les gates humains sur les preuves critiques.

## 17_RESUME_POINT

Le fichier suivant devra attacher snapshots et artefacts a ce modele `run_id -> timeline -> surface` avant toute readiness d'export reel.
