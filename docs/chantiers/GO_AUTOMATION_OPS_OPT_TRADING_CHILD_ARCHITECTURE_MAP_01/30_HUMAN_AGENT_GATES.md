---
doc_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_ARCHITECTURE_MAP_01_GATES
doc_type: human_agent_gates
repo: opt-trading
go_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_ARCHITECTURE_MAP_01
updated_at: 2026-05-28
---

# 30_HUMAN_AGENT_GATES

## Définition

Un gate humain est un point où l'exécution doit s'arrêter et attendre une décision ou action de l'opérateur.
Aucun agent ne peut franchir un gate humain de manière autonome.

---

## Gates par flux

### Flux 1 — Signal trading

| Gate | Moment | Décision humaine |
|---|---|---|
| G1.1 | Configuration risk_engine | définir seuils, guardrails, TRADE_ALLOWED |
| G1.2 | Alerte Telegram hors-norme | investiguer + intervention manuelle si besoin |

### Flux 2 — Desk Pro

| Gate | Moment | Décision humaine |
|---|---|---|
| G2.1 | Lancement desk_pro_runner | déclenchement manuel opérateur |
| G2.2 | Décision sur données dashboard | toute action de trading reste humaine |

### Flux 3 — OpenClaw ops

| Gate | Moment | Décision humaine |
|---|---|---|
| G3.1 | Validation GO_PROMPT config | lire + approuver le changement config avant apply_safe |
| G3.2 | apply_safe.sh | exécution confirmée par opérateur |
| G3.3 | Résultat gateway start | vérification session tmux active |
| G3.4 | rollback.sh | déclenchement sur décision opérateur uniquement |

### Flux 4 — CI/CD GHA

| Gate | Moment | Décision humaine |
|---|---|---|
| G4.1 | PR review | lecture diff + validation |
| G4.2 | PR merge | `gh pr merge` — jamais automatique sans instruction |
| G4.3 | CI failure | investigation + correction avant re-merge |

### Flux 5 — AI Workers (critique)

| Gate | Moment | Décision humaine |
|---|---|---|
| G5.1 | Validation GO_PROMPT | opérateur lit et approuve le prompt + contraintes + livrables |
| G5.2 | Revue PR produite | opérateur lit le diff |
| G5.3 | Merge PR | instruction explicite requise |
| G5.4 | Post-merge audit | opérateur fournit 7_CANONICAL_STATE + screenshot |
| G5.5 | Décision next GO | opérateur valide NEXT_GO ou redirige |
| G5.6 | Stop condition | si test fail inattendu → agent s'arrête et demande |

### Flux 6 — Fleet health

| Gate | Moment | Décision humaine |
|---|---|---|
| G6.1 | Alerte Telegram machine down | investigation + action corrective |
| G6.2 | Lancement healthcheck manuel | déclenchement opérateur |

---

## Ce qui NE peut PAS être automatisé

| Action | Raison |
|---|---|
| Merge PR | risque régression production |
| apply_safe.sh OpenClaw | risque config gateway |
| Suppression fichier hors scope | irréversible sans validation |
| Changement guardrails trading | impact production direct |
| Lancement trading en mode autonome | risque financier |
| Décision rollback post-merge | contexte humain requis |

---

## Ce qui PEUT être automatisé (avec gate amont)

| Action | Condition |
|---|---|
| Création PR | après GO_PROMPT validé |
| Commit + push | scope limité, confirmé par GO_PROMPT |
| Création docs chantier | toujours doc-only |
| Tests CI | déclenchés par git event |
| Smoke checks | non-destructif |
| Telegram notify | sur seuil défini |
| Healthcheck fleet | lecture seule |
