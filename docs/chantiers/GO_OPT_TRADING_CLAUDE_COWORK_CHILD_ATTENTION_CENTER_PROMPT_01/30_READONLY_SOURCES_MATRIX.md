---
doc_id: GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_PROMPT_01_30_READONLY_SOURCES_MATRIX
doc_type: chantier/readonly_sources_matrix
repo: opt-trading
machine: cursor-ai
go_id: GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_PROMPT_01
status: active
scope: doc-only
links:
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01/02_REMAINING_GAP.md
---

# 30_READONLY_SOURCES_MATRIX

## Principe

Surface preferee :

```text
snapshot repo read-only
```

Le repo actif peut servir de reference locale pour definir le prompt, mais le Live Artifact cible doit preferer une surface de lecture dediee et bornee.

## Matrice des sources autorisees

| Source | Lecture | Ecriture | Priorite | Statut |
| --- | --- | --- | --- | --- |
| Snapshot repo read-only (`repo-readonly/opt-trading-snapshot`) | oui | non | P0 | autorise |
| Docs canoniques (`docs/index/*`, `docs/chantiers/*`, `docs/governance/*`) via snapshot | oui | non | P0 | autorise |
| GitHub PR / branches / issues si connecteur disponible | oui | non par defaut | P0 | autorise |
| Fichiers de reprise exportes dans `reports/` | oui | non | P1 | autorise |
| Google Drive docs | oui si explicitement connecte | non par defaut | P2 | optionnel |
| Calendar | oui si explicitement connecte | non | P2 | optionnel |
| Asana / ClickUp | oui si explicitement connecte | non | P2 | optionnel |
| Repo actif complet | a eviter | non | P2 | tolere seulement si snapshot indisponible |
| Fichiers sensibles / secrets / `.env` | non | non | interdit | interdit |
| Runtime, services, payloads reels | non | non | interdit | interdit |

## Regle read-only stricte

```text
MODE READ-ONLY STRICT
Tu peux lire et synthetiser.
Tu ne modifies aucun fichier, aucune branche, aucune PR, aucun document Drive, aucun calendrier, aucune tache.
Toute action d'ecriture doit etre proposee comme TODO et attendre un GO explicite.
```

## Preuve de source

Chaque signal du dashboard doit pouvoir indiquer au moins :
- la source consultee ;
- le type de preuve ;
- le niveau de confiance ;
- la date ou le dernier point connu si pertinent.
