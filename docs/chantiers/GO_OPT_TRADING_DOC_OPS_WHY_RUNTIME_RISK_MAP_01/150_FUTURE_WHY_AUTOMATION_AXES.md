# 150_FUTURE_WHY_AUTOMATION_AXES

## Objectif

Cadrer les futurs axes possibles apres la cartographie WHY runtime.

Ce document reste doc-only. Il n'ouvre aucune implementation active.

## Axes candidats

| Axe | But | Precondition |
| --- | --- | --- |
| parser WHY markdown reel | lire les sections WHY dans les docs | conventions markdown stables |
| worker d'audit WHY | scanner les GO et produire un rapport | parser disponible |
| dashboard governance | visualiser scores, gaps et risques | donnees d'audit fiables |
| scoring automatique | calculer maturite WHY par GO | grille stabilisee |
| lint documentaire experimental | verifier sections critiques | politique de lint validee |
| graph runtime multi-machine | cartographier dependances runtime | surfaces et machines stabilisees |

## Ordre recommande

1. Parser WHY markdown reel.
2. Scoring automatique.
3. Worker d'audit WHY.
4. Lint documentaire experimental.
5. Graph runtime multi-machine.
6. Dashboard governance.

## Pourquoi cet ordre

Le parser doit preceder le score.

Le score doit preceder le worker.

Le worker doit preceder le lint.

Le graph runtime doit s'appuyer sur la cartographie R0-R5.

Le dashboard doit venir en dernier, une fois les donnees produites de maniere stable.

## Invariants

- Aucun APPLY automatique.
- Aucun runtime sans review humaine.
- Aucune CI bloquante sans phase experimentale.
- Aucun score WHY ne remplace une review humaine.
- Le graph runtime doit rester une aide d'audit, non une source unique de verite.

## 17_RESUME_POINT

Apres merge de la PR runtime WHY, le premier chantier recommande est:

`GO_OPT_TRADING_DOC_OPS_WHY_MARKDOWN_PARSER_01`

But:
- lire les blocs WHY,
- detecter les sections manquantes,
- preparer le scoring automatique.
