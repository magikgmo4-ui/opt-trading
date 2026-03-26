# CLOSEOUT MEMORY_BRICKS V1 IMPL HARDEN 01

- etat de depart: bootstrap injecte sur `feat/memory-bricks-v1-impl-harden` depuis `8195cdf`, module absent avant extraction
- durcissements appliques: suppression de la dependance `yaml`, validation stricte `BrickModel`, sequence robuste, state root local configurable, link/status/index/export/merge/handoff fiabilises
- validation reelle attendue dans cette passe: CLI locale, `sanity_check.sh`, tests `unittest`
- limites restantes: pas d'API active, pas de LocalCMS, pas d'import navigateur/mobile/cloud
- point de reprise naturel: `GO_MEMORY_BRICKS_V1_TESTS_HARDEN_02`
