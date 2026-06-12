---
doc_id: GO_TMUX_IDE_OPT_TRADING_CADRAGE_01_PLAN
doc_type: chantier_plan
repo: opt-trading
project: opt-trading
module:
go_id: GO_TMUX_IDE_OPT_TRADING_CADRAGE_01
status: active
lifecycle_stage: plan
topic_keys:
  - opt-trading
  - tmux
  - tmux-ide
  - ssh
  - ide
  - continuity
surface: chantier
source_kind: canonical
updated_at: 2026-04-14
links:
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_CADRAGE_01/00_cadrage.md
  - docs/governance/SESSION_DOCUMENTATION_GATE.md
  - docs/index/GO_INDEX.md
  - docs/index/REPRISE.md
---

# 01_plan — GO_TMUX_IDE_OPT_TRADING_CADRAGE_01

## But du plan
- but : transformer le cadrage `tmux-ide` en base d’exécution réellement exploitable sur machine cible
- ordre d’exécution retenu : cadrage -> plan -> validation machine -> réglage `ide.yml` -> doctor / validate -> reprise vers implémentation

## Étapes
1. vérifier la machine cible réelle et son rôle
2. vérifier le chemin repo réel et la branche active
3. vérifier les prérequis `tmux`, `node`, `npm`, `tmux-ide`
4. poser un `ide.yml` minimal aligné sur le rôle machine
5. tester `tmux-ide doctor`
6. tester `tmux-ide validate`
7. ajuster les panes utiles : shell / git / journal / tests / logs
8. ouvrir le GO d’implémentation réelle si la base est validée

## Zones de travail pressenties
- `docs/chantiers/GO_TMUX_IDE_OPT_TRADING_CADRAGE_01/`
- racine repo `opt-trading`
- futur `ide.yml` sur machine cible ou dans zone de transfert adaptée
- scripts de bundle / installation déjà préparés dans la session courante

## Validations prévues
- cohérence entre machine cible, repo réel et usage IDE
- absence de confusion entre remote GitHub et repo local d’exécution
- session `tmux-ide` reattachable et compréhensible
- point de reprise explicite vers `GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01`

## Limites du lot
- pas d’implémentation machine réelle dans ce fichier
- pas de closeout tant que `doctor` / `validate` ne sont pas exécutés sur l’environnement cible

## RISKS

- À qualifier.
