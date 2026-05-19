# WHY lint static validator

## Objectif

`why_lint_static_validator.py` est un outil local read-only/report-only pour le
corpus Markdown WHY lint et, en V1, pour un scan borne des documents reels du
chantier parent WHY lint.

Il lit les fixtures, extrait les blocs de regles fences en Markdown, valide les
champs attendus, calcule un verdict statique et compare ce verdict au verdict
attendu par la fixture.

Le mode `--scan-docs` lit uniquement des fichiers Markdown dans le dossier parent
WHY lint autorise. Il produit un rapport, sans modifier les sources.

## Usage local

Commande principale fixtures :

```bash
python tools/why_lint_static_validator/why_lint_static_validator.py \
  --fixtures docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_FIXTURE_CORPUS_01.md
```

Rapport JSON fixtures :

```bash
python tools/why_lint_static_validator/why_lint_static_validator.py \
  --fixtures docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_FIXTURE_CORPUS_01.md \
  --format json
```

Scan V1 des documents reels du parent WHY lint :

```bash
python tools/why_lint_static_validator/why_lint_static_validator.py \
  --scan-docs docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01
```

Rapport JSON scan V1 :

```bash
python tools/why_lint_static_validator/why_lint_static_validator.py \
  --scan-docs docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01 \
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
- aucune modification des documents scannes ;
- aucun patch automatique ;
- aucun runtime ;
- aucun MCP live ;
- aucun trade ;
- aucun secret reel recherche ou lu ;
- aucune CI bloquante.

## Mode `--scan-docs` V1

Le mode V1 est volontairement borne au dossier :

```text
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01
```

Il scanne les fichiers `*.md` de ce dossier seulement.

Il ignore explicitement le corpus de fixtures :

```text
GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_FIXTURE_CORPUS_01.md
```

Il signale notamment :

- section `WHY` manquante sur les docs GO structures ;
- `FINAL_TARGET` manquant sur les docs GO structures ;
- `12_INVARIANTS` manquant sur les docs GO structures ;
- `17_RESUME_POINT` manquant sur les docs GO structures ;
- implication runtime interdite dans un document read-only/report-only ;
- implication autofix interdite ;
- implication CI bloquante interdite ;
- motif secret-like inattendu.

Les checks de marqueurs GO numerotes s'appliquent uniquement aux documents qui
portent deja une structure GO numerotee via des headings H2 du type
`## 1_MASTER_TARGET`.

Les docs thematiques legacy hors squelette GO restent scannes pour les
implications runtime/autofix/secret, mais ne sont pas forces sur les marqueurs
GO numerotes.

Les checks d'implication interdite ne remontent que sur des lignes de champs
actives hors code-fences Markdown ; les exemples fences ou les listes negatives
documentees ne sont pas traites comme une configuration vivante.

Ce mode ne scanne pas tout le repo et ne modifie aucun fichier.

## Limites

- Le parseur accepte seulement le sous-ensemble YAML utilise dans les fences du
  corpus Markdown.
- La detection secret-like est limitee a des motifs factices ou structurels dans
  les fixtures et a des motifs prudents dans le scan doc.
- Le scan de documents reels est limite au parent WHY lint.
- Le rapport est texte ou JSON imprime sur stdout, sans fichier de sortie.
- Aucun scan repo-wide n'est inclus.

## Non-objectifs

- Pas de runtime OpenClaw.
- Pas de runtime trading.
- Pas d'autofix.
- Pas d'integration MCP.
- Pas de workflow GitHub Actions.
- Pas de CI bloquante.
- Pas de scan repo-wide.
- Pas de recherche de vrais secrets.

## Exit codes

| Code | Sens |
| --- | --- |
| 0 | Validation/scan complete sans echec bloquant. |
| 1 | Validation/scan complete avec findings ou mismatch. |
| 2 | Fichier fixture illisible, format invalide ou root scan hors scope. |
| 3 | Risque secret-like ou champ interdit non attendu. |
| 4 | Erreur interne controlee. |

## Avertissement

Cet outil est strictement local, statique, read-only et report-only.

Il ne lance aucun runtime, n'applique aucun autofix, ne modifie aucune source, ne
cherche aucun secret reel et ne bloque aucune CI.
