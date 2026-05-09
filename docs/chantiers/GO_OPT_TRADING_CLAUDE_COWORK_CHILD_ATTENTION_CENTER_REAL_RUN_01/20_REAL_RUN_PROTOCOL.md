---
doc_id: GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01_20_REAL_RUN_PROTOCOL
doc_type: chantier/protocol
repo: opt-trading
machine: cursor-ai
go_id: GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01
status: active
scope: doc-only
links:
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_PROMPT_01/70_FINAL_PROMPT.md
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01/10_SOURCE_STATE.md
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01/30_CLAUDE_OUTPUT_CAPTURE.md
---

# 20_REAL_RUN_PROTOCOL

## Protocole d'exécution

### Étape 1 — Création de la branche

```bash
git checkout sot/mainline
git checkout -b go/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01
```

Résultat : branche créée depuis `sot/mainline` — ETAT_VERIFIE (session active).

### Étape 2 — Lecture des sources

Sources lues en séquence (voir `10_SOURCE_STATE.md` pour la liste complète) :

1. `70_FINAL_PROMPT.md` — prompt final tel que committé dans le trunk
2. `20_ATTENTION_CENTER_SPEC.md` — spec du cockpit
3. `30_READONLY_SOURCES_MATRIX.md` — matrice des sources autorisées
4. `40_SCORING_P0_P1_P2.md` — grille de scoring
5. `50_MACHINE_STATE_RULES.md` — taxonomie machine states
6. `60_EXPORT_FORMAT.md` — format d'export journalisé
7. `bundles/claude-artifacts/README.md`, `NO_COMMIT_RULES.md`, `CHECKLIST_EXECUTION.md`
8. `docs/index/ACTIVE_STREAMS.md`, `REPRISE.md`, `NEXT_GO_CANDIDATES.md`, `BRANCH_STATE.md`
9. `git log --oneline`, `git branch -r --no-merged` — mesures live

### Étape 3 — Exécution du prompt en mode Cowork

Le prompt `OPT_TRADING_ATTENTION_CENTER_01` est exécuté dans la session Claude Cowork active.

Surface d'exécution : Claude Cowork (session locale, pas de Live Artifact HTML externe dans ce run — voir `50_GAPS_AND_ADJUSTMENTS.md`).

Mode opératoire retenu : Claude lit les sources repo en read-only strict, synthétise et produit le dashboard dans le contexte de la session.

### Étape 4 — Capture de la sortie

La sortie complète du run est documentée dans `30_CLAUDE_OUTPUT_CAPTURE.md`.

### Étape 5 — Classement P0/P1/P2

Le classement structuré est dans `40_P0_P1_P2_RESULTS.md`.

### Étape 6 — Vérification des critères

Vérification des 6 critères du prompt :

| Critère | Vérifié ? | Observation |
| --- | --- | --- |
| Read-only strict | ✓ | Aucun fichier modifié hors docs/ chantier courant |
| Sources autorisées | ✓ | Repo docs/ + git live — aucune source interdite utilisée |
| Repo/docs/Git comme vérité canonique | ✓ | Toutes les assertions sourcées sur fichiers lus ou commandes git |
| Machine states avec preuve | ✓ | Taxonomie ETAT_DECLARE / ETAT_VERIFIE / HYPOTHESE appliquée |
| Export journalisé | ✓ | Défini dans `60_EXPORT_REPORT.md`, non écrit automatiquement |
| Diff limité à docs/ | ✓ | Aucun runtime, aucun modules/, aucun secret |

### Étape 7 — Gaps et ajustements

Documentés dans `50_GAPS_AND_ADJUSTMENTS.md`.

### Étape 8 — Export local

Contenu proposé défini dans `60_EXPORT_REPORT.md`.

### Étape 9 — Fermeture du GO

Verdict dans `90_CLOSEOUT.md`.

## Notes de contexte d'exécution

- Connecteur GitHub API : non activé → états PR/branches depuis docs et git local uniquement
- Snapshot repo read-only dédié : non configuré → repo actif utilisé en lecture seule par convention
- Live Artifact HTML : non généré dans ce run (gap documenté)
- Machine states : tous ETAT_DECLARE sauf cursor-ai (ETAT_VERIFIE partiel via session active)
