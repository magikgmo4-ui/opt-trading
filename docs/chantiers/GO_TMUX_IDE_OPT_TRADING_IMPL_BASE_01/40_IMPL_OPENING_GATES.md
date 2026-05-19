---
doc_id: GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01_40_IMPL_OPENING_GATES
doc_type: chantier/gates
repo: opt-trading
machine: cursor-ai
go_id: GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01
status: active
scope: doc-only
---

# 40_IMPL_OPENING_GATES

## Gates obligatoires avant implementation reelle

1. Verifier que la cible de test est bien `admin-trading`, pas `db-layer`.
2. Verifier le chemin reel du repo `opt-trading` sur `admin-trading`.
3. Verifier la branche active et l'etat Git local sur la machine cible.
4. Verifier la presence de `tmux`, `node`, `npm` et `tmux-ide`.
5. Poser un `ide.yml` minimal adapte au role machine.
6. Executer `tmux-ide doctor`.
7. Executer `tmux-ide validate`.
8. Ne pas toucher a `openclaw-gateway` sur `db-layer`.

## Gates de refus

- si la seule machine disponible est `db-layer`, ne pas forcer l'implementation
- si la topologie reelle contredit `admin-trading` sans preuve meilleure, arreter et requalifier
- si le repo local n'est pas prouve sur la cible, ne pas passer a `ide.yml`
- si le besoin derive vers OpenClaw ou runtime, ouvrir un autre GO

## Gate de suite

La suite implementation peut commencer seulement si:

- `admin-trading` est confirmee comme machine cible reelle
- la separation `cursor-ai` operateur / `db-layer` runtime reste intacte
- aucun changement runtime n'est necessaire pour demarrer `tmux-ide`
