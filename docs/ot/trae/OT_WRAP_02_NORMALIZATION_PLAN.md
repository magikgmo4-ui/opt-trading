# OT-WRAP-02 — PLAN DE NORMALISATION

## 1. CONVENTION RETENUE
`[type]-[module_name]`
- `menu-...`
- `cmd-...`
- `sanity-...`

## 2. ACTIONS RÉALISÉES
- Suppression des doublons `validated_prompt_factory_cmd/menu`.
- Patch des scripts `trae_module_validator` pour supporter l'invocation via symlink.

## 3. PROCHAINES ÉTAPES (HORS MISSION)
- Renommer `menu-desk-pro` en `menu-desk_pro` (si possible).
- Normaliser les wrappers `deepseek_*`.
