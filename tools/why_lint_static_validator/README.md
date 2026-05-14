# WHY lint static validator

## Objectif

`why_lint_static_validator.py` est un outil local read-only/report-only pour le
corpus Markdown WHY lint.

Il lit les fixtures, extrait les blocs de regles fences en Markdown, valide les
champs attendus, calcule un verdict statique et compare ce verdict au verdict
attendu par la fixture.

## Usage local

Commande principale :

```bash
python tools/why_lint_static_validator/why_lint_static_validator.py \
  --fixtures docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_FIXTURE_CORPUS_01.md
```

Rapport JSON :

```bash
python tools/why_lint_static_validator/why_lint_static_validator.py \
  --fixtures docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_FIXTURE_CORPUS_01.md \
  --format json
```

Aide :

```bash
python tools/why_lint_static_validator/why_lint_static_validator.py --help
```

## Garanties

- local only ;
- read-only ;
- report-only ;
- deterministic ;
- aucune modification des fixtures ;
- aucun patch automatique ;
- aucun runtime ;
- aucun MCP live ;
- aucun trade ;
- aucun secret reel recherche ou lu ;
- aucune CI bloquante.

## Limites

- Le parseur accepte seulement le sous-ensemble YAML utilise dans les fences du
  corpus Markdown.
- La detection secret-like est limitee a des motifs factices ou structurels dans
  les fixtures.
- La validation reste bornee au corpus de fixtures, pas aux documents reels du
  repo.
- Le rapport est texte ou JSON imprime sur stdout, sans fichier de sortie.

## Non-objectifs

- Pas de runtime OpenClaw.
- Pas de runtime trading.
- Pas d'autofix.
- Pas d'integration MCP.
- Pas de workflow GitHub Actions.
- Pas de CI bloquante.
- Pas de scan des documents reels hors fixtures.
- Pas de recherche de vrais secrets.

## Exit codes

| Code | Sens |
| --- | --- |
| 0 | Toutes les fixtures passent selon leurs verdicts attendus. |
| 1 | Au moins un verdict obtenu ne correspond pas au verdict attendu. |
| 2 | Fichier fixture illisible ou format invalide. |
| 3 | Risque secret-like ou champ interdit non attendu. |
| 4 | Erreur interne controlee. |

## Avertissement

Cet outil est strictement local, statique, read-only et report-only.

Il ne lance aucun runtime, n'applique aucun autofix, ne modifie aucune source, ne
cherche aucun secret reel et ne bloque aucune CI.
