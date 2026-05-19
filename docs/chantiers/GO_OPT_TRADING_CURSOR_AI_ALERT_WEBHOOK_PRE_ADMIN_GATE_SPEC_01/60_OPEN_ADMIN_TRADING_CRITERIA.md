---
doc_id: GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_PRE_ADMIN_GATE_SPEC_01_60_OPEN_CRITERIA
doc_type: chantier/open_criteria
repo: opt-trading
machine: cursor-ai
status: active
links:
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
  - docs/chantiers/GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_PRE_ADMIN_GATE_SPEC_01/40_VALIDATION_MATRIX.md
---

# 60_OPEN_ADMIN_TRADING_CRITERIA

Criteres explicites avant toute ouverture future d'admin-trading depuis cursor-ai.

## Phrase d'activation

```text
chantiers pour admin-trading
```

Tant que cette phrase exacte n'est pas prononcee par l'operateur, admin-trading reste **FERME**.

## Critere 1 — Demande explicite

- [ ] L'operateur a dit "chantiers pour admin-trading".
- [ ] La demande est documentee dans le GO courant.

## Critere 2 — Validation matrix PASSEE

- [ ] Tous les checks 1-9 de `40_VALIDATION_MATRIX.md` sont PASS.
- [ ] Aucun FAIL sur les checks bloquants.

## Critere 3 — Sequence cursor-ai complete

- [ ] Position 1 : Claude artifacts operator pack merge.
- [ ] Position 2 : Bundles workflow actif merge.
- [ ] Position 3 : Pre-admin gate spec (ce GO) merge.
- [ ] Position 4 : Operateur reprise packet (futur) close.

## Critere 4 — Contexte machine valide

- [ ] La machine actuelle est explicitement passee de `cursor-ai` a `admin-trading`.
- [ ] Le bloc `ADMIN_TRADING` de `MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md` est le contexte cible.
- [ ] Les invariants cursor-ai sont preserves.

## Critere 5 — Etat Bundles

- [ ] Bundles workflow actif disponible pour documenter le passage.
- [ ] Aucun bundle admin-trading cree prematurement.
- [ ] `NO_RUNTIME_NO_SENSITIVE_RULES.md` applique.

## Ce qui n'est pas ouvert meme apres la gate

- `webhook_server.py` — necessite une decision separee.
- `systemd` — necessite une decision separee.
- `risk engine` — necessite une decision separee.
- `trade_allowed: true` — necessite une decision separee.
- Alertes reelles — necessite une decision separee.

La gate ouvre le droit de travailler sur admin-trading. Chaque action runtime reste soumise a decision explicite.

## Limites tant que la demande n'existe pas

- Aucun fichier admin-trading modifie.
- Aucune branche admin-trading creee par cursor-ai.
- Aucune PR touchant admin-trading.
- Aucune reference runtime a admin-trading dans les bundles cursor-ai.

## Exemple de reprise post-gate

```text
Operateur : "chantiers pour admin-trading"
→ Verification : criteria 1-5 PASS
→ Action : ouvrir GO admin-trading specifique
→ Machine : passer a admin-trading
→ Runtime : soumis a decisions explicites
```
