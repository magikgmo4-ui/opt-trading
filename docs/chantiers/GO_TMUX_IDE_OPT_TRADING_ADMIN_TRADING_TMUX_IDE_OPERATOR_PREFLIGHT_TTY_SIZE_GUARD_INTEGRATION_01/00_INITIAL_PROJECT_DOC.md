# GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_OPERATOR_PREFLIGHT_TTY_SIZE_GUARD_INTEGRATION_01

## 1_MASTER_TARGET

Integrer durablement le guard TTY size dans le template operateur 	mux-ide.

## 3_INITIAL_NEED

	mux-ide@1.3.1 echoue lorsque la TTY distante retourne stty size = 0 0, car le lancement transmet -x 0 -y 0 a 	mux.

## 4_MASTER_PROJECT_PLAN

- Utiliser le diagnostic racine merge par PR #523.
- Utiliser le retry guard valide par PR #526.
- Modifier la surface canonique $targetRel.
- Ajouter un preflight conditionnel avant 	imeout 12s npx -y tmux-ide@1.3.1.

## 12_INVARIANTS

- Pas d'installation globale.
- Pas de ide.yml durable.
- Pas de 	mux kill-server global.
- Pas d'index global modifie.
- Cleanup operateur conserve.

## 17_RESUME_POINT

Surface canonique patchee : $targetRel.
