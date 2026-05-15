# Dependances et next GO

## Dependances retenues
- `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01`
  - `db-layer` reste la machine prioritaire actuelle.
  - Ce GO runtime ne remplace pas le parent machine.
- `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03`
  - Dependance transverse toujours ouverte.
  - Elle ne bloque pas les controles read-only de ce GO, car l'acces SSH a `db-layer` a reussi.
  - Elle reste toutefois necessaire avant des validations physiques multi-machines plus larges.
- `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01`
  - `admin-trading` reste la machine trading reelle future.
  - Aucun melange avec `bot_vision`, `deskpro`, `webhook`, `collectors` ou runtime trading n'est autorise ici.
- `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01`
  - Reference differee seulement.
  - Aucun dossier local prouve dans cette ligne.
  - A ne considerer qu'apres clarification du runtime local `db-layer`.

## Lecture de suite
- Le blocage principal n'est pas `reseau_ssh`, puisque la lecture distante a fonctionne.
- Le blocage principal est runtime local :
  - session `openclaw-gateway` arretee
  - port `18789` ferme
  - process `openclaw` absent
  - log historique prouvant des demarrages anterieurs mais pas d'activite courante

## Next GO recommande
- `GO_OPENCLAW_STATE_DIR_REPAIR_10`

## Pourquoi ce next GO
- Le repo porte deja un GO de reparation locale bornee pour ce cas exact.
- Son etat de depart attendu correspond au constat releve ici :
  - config `~/.openclaw/openclaw.json`
  - session `openclaw-gateway` arretee
  - loopback `ws://127.0.0.1:18789` non joignable
  - `ECONNREFUSED 127.0.0.1:18789`
- Il permet un GO d'application controlee sans ouvrir un nouveau parent ni rearchitecturer `OpenClaw`.

## Alternatives non retenues maintenant
- `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_CLOSEOUT_01`
  - non retenu comme priorite immediate, car SSH n'a pas bloque ce GO.
- `GO_OPT_TRADING_UI_LOCALCMS_DB_LAYER_CONSUMER_REALIGNMENT_01`
  - differe derriere la remise a plat runtime `OpenClaw`.
- `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01`
  - differe tant que le runtime local `db-layer` n'est pas clarifie.
