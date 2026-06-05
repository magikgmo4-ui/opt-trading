# Dependances et prochain GO

## Dependances restantes

- `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03` reste le parent transverse ouvert
- la reduction de compatibilite `scripts/reseau_ssh -> archive` reste un lot separe
- la convergence physique complete `step1b + step2` reste hors scope de ce closeout
- la divergence de chemin repo sur `fantome` doit etre gardee en tete avant toute automation multi-machine supposant `/opt/trading` litteral

## Impact par machine

### db-layer

- cycle recent deja clarifie
- aucune action runtime supplementaire necessaire dans ce closeout
- reste une machine de reference, pas le prochain chantier principal

### admin-trading

- connectivite et chemin repo verifies
- le parent machine reste ouvert mais differe
- rien n'impose de relancer `admin-trading` avant la prochaine reprise `cursor-ai`

### cursor-ai

- poste local Windows confirme
- alias `cursor-ai` present dans `~/.ssh/config`, mais la verification utile de ce lot est locale
- devient la prochaine machine productive logique pour l'orchestration multi-agents

### fantome

- connectivite OK
- attention : le repo reel est sous `/home/fantome/opt-trading`
- ce point n'est pas bloquant, mais doit etre documente avant toute reprise `AI Team` / `strict workers`

### student

- connectivite OK
- le flux `Ollama` reste differe
- aucun blocage `reseau_ssh` residuel n'interdit une reprise future de ce cote

## Next GO recommande

- `GO_OPT_TRADING_MULTI_AGENTS_CURSOR_AI_PARENT_ALIGNMENT_01`

## Justification

- `db-layer`, `OpenClaw` et `LocalCMS` ont deja ete clarifies
- les alias SSH Linux prioritaires sont verifies et le canonique `modules/reseau_ssh` est confirme physiquement
- `cursor-ai` est maintenant le prochain point logique de reprise productive pour garder la regle ideale de `1` chantier principal par machine
- `admin-trading`, `fantome` et `student` peuvent rester derriere ce passage d'alignement

## RISKS

- À qualifier.
