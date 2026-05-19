# doctor_openclaw

Facade standardisee de diagnostic et de reparation prudente pour OpenClaw.

## Role
- lancer les checks `doctor`
- executer des passes rapides ou profondes
- verifier `config validate`, `gateway health`, `gateway probe`
- proposer une reparation safe et la generation de token gateway

## Contenu
- `scripts/cmd.sh` : `quick`, `deep`, `repair-safe`, `generate-token`, `validate`, `health`, `probe`, `logs`, `status`, `dashboard`
- `scripts/menu.sh`, `sanity.sh`, `install_shortcuts.sh`
- `docs/README.md`, `RUNBOOK.txt`, `ETABLI.txt`

## Integration
- travaille avec `gateway_openclaw` et `configure_openclaw`
- sert de couche de verification avant et apres changements de config

## Statut
- actif
- facade de diagnostic de la suite OpenClaw

## Notes de consolidation
- ne remplace pas `gateway_openclaw` ni `configure_openclaw`
- `doctor_openclaw` reste centre sur le diagnostic et la verification de sante
