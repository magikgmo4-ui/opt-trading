---
doc_id: GO_OPT_TRADING_UI_LOCALCMS_PARENT_MOBILE_FIGMA_REFERENCE_01_STREAM_DECK_VISUAL_SUPPORT
doc_type: support_spec
repo: opt-trading
project: opt-trading
module: ui_localcms_figma
go_id: GO_OPT_TRADING_UI_LOCALCMS_PARENT_MOBILE_FIGMA_REFERENCE_01
status: open
lifecycle_stage: support_mapping
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-19
topic_keys:
  - stream-deck
  - unified-remote
  - rustdesk
  - rdp
  - web-cockpit
  - mobile
  - localcms
---

# 40_STREAM_DECK_AND_VISUAL_SUPPORT_SPEC

## Objectif

Documenter le rôle des surfaces cockpit/support autour de Figma et LocalCMS.

## Hiérarchie de contrôle

```text
LocalCMS Web Cockpit = supervision permanente read-only
Stream Deck = commandes safe bornées
Unified Remote = télécommande mobile secondaire
RustDesk = support visuel cross-machine
RDP / Bureau distant = intervention GUI complète
Desk Pro = trading actif séparé
```

## Stream Deck safe profile

Nom cible : `OPT_TRADING_SAFE_PROFILE_01`

Boutons recommandés :
1. `Open LocalCMS`
2. `Open Desk Pro`
3. `Open RustDesk admin-trading`
4. `Open RustDesk db-layer`
5. `Open Telegram Bot`
6. `Open ClickUp GO Board`
7. `Open Airtable Ops`
8. `Open Repo KG`
9. `Open Botpress Console`
10. `Healthcheck OpenClaw`
11. `Healthcheck TMUX`
12. `Current GO / Resume Point`
13. `Bot Vision Snapshot`
14. `Kill Switch Status READ_ONLY`
15. `Open Watchlist`

## Actions interdites Stream Deck

```text
git push
git merge
git reset --hard
git push --force-with-lease
trade live
order submit
kill process critical
edit .env
delete files
rotate secrets
```

Toute action destructive doit passer par un GO, un diff, une review et une validation explicite.

## Unified Remote

Rôle : appoint mobile pour contrôle souris/clavier/écran local.

Usage recommandé :
- piloter un PC depuis le téléphone ;
- naviguer dans LocalCMS ou Desk Pro ;
- appui dépannage court.

Usage exclu :
- cockpit canonique ;
- exécution trade ;
- remplacement Stream Deck ou LocalCMS.

## RustDesk

Rôle : support visuel cross-machine.

Usage recommandé :
- voir l'écran réel admin-trading ;
- dépanner db-layer/cursor-ai/student/fantome ;
- observer TradingView ou Desk Pro quand le web cockpit ne suffit pas.

Usage exclu :
- source de vérité ;
- monitoring continu ;
- exécution automatique.

## RDP / Bureau distant

Rôle : intervention GUI complète.

Usage recommandé :
- session Windows admin-trading ;
- TradingView graphique ;
- IDE/terminal GUI ;
- configuration longue.

Usage exclu :
- monitoring permanent ;
- action critique sans gate.

## Web cockpit

Rôle : supervision permanente via LocalCMS/Desk Pro.

Usage recommandé :
- mobile-first ;
- read-only ;
- healthchecks ;
- GO roadmap ;
- workers ;
- apps externes.

## Rôle de Figma dans cette couche

Figma sert à concevoir :
- le profil visuel Stream Deck ;
- les écrans mobile LocalCMS ;
- les écrans desktop LocalCMS ;
- les cartes support visuel ;
- les codes couleur de danger ;
- la séparation `voir / commander / intervenir`.
