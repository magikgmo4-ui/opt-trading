# 20_IMPLEMENTATION_NOTES

## Modifications à `capture_headless.js`

### Nouveaux blocs

1. **Constantes de statut** : `STATUS_READY`, `STATUS_BLOCKED`, `STATUS_INVALID_VISUAL`
2. **Blocked reasons** : `PAGE_GOTO_TIMEOUT`, `PAGE_GOTO_ERROR`, `SCREENSHOT_ERROR`, `OUTPUT_WRITE_ERROR`
3. **Visual status** : `unchecked`, `pass`, `possible_spinner`, `blank_or_uniform`, `too_small`, `loading_state_detected`
4. **Fonction `classifyVisual()`** : checks non destructifs sur le PNG + DOM
5. **Fonction `writeBlockedSidecar()`** : écrit un JSON blocked sans PNG
6. **Options profil** : `visual_check_enabled`, `dom_loading_selectors`

### Comportement

| Condition                          | Statut          | PNG | JSON |
| ---------------------------------- | --------------- | --- | ---- |
| page.goto timeout                  | `blocked`       | non | oui  |
| page.goto error                    | `blocked`       | non | oui  |
| screenshot error                   | `blocked`       | non | oui  |
| PNG < 1KB                          | `invalid_visual`| non | oui  |
| PNG valide mais checks visuels KO  | `invalid_visual`| oui | oui  |
| Tout OK                            | `ready`         | oui | oui  |

### Non modifié

- `profiles.example.json`
- Les profils existants restent compatibles (backward compatible)
- Les defaults restent inchangés
- Aucune suppression des PNG invalides
