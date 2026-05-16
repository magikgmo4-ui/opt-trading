# 20_TMUX_RUNTIME_SESSION_SURFACE_ROLE

## 1_MASTER_TARGET

Definir `TMUX` comme premiere surface runtime/session canonique a exposer au WHY runtime graph.

## WHY

Le runtime graph doit s'ancrer sur des surfaces d'execution reelles et nommees. La spine `TMUX` apporte justement les sessions, panes, logs, placements machine et restart semantics qui rendent le runtime lisible sans l'activer.

## 7_CANONICAL_STATE

Role retenu pour `TMUX` :

| Dimension | Position retenue |
| --- | --- |
| Nature | spine runtime/session |
| Fonction graph | surface d'execution et d'observabilite primaire |
| Unites canoniques | session, pane, machine placement, restart semantics, logs |
| Relation canonique | `HOSTS_OR_EXPOSES` des surfaces runtime et `PROVES` via traces associees |
| Criticite candidate | `R4/R5` pour la spine, selon surface observee |

Lectures structurantes deja etablies :

- `TMUX = colonne vertebrale runtime` ;
- chaque process long-running doit etre lie a un pane nomme ;
- chaque session doit representer un domaine fonctionnel isole ;
- `LocalCMS` est decrit comme UI centrale qui lit l'etat des sessions `TMUX` ;
- les sessions canoniques, panes, restart policy et logs sont deja des preuves documentaires utiles au graph.

## 8_EXPECTED_PROOFS

- nomenclature des sessions et panes ;
- placement machine documente ;
- restart semantics ;
- logs nommes par session/pane ;
- healthchecks, snapshots ou traces de session si cites ;
- review humaine pour toute surface critique ou ambiguite d'hebergement.

## 12_INVARIANTS

- Ce GO ne lance aucune commande `TMUX`.
- Ce GO ne transforme pas `TMUX` en connecteur live.
- Les preuves `TMUX` restent documentaires et auditables.

## 17_RESUME_POINT

La surface `TMUX` definie ici devra etre reliee a `LocalCMS` comme consumer read-only, puis completee par le mapping daily journal avant tout render reel.
