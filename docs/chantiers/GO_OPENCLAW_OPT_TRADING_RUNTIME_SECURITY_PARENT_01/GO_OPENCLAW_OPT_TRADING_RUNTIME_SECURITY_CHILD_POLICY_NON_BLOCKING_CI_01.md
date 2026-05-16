---
doc_id: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_NON_BLOCKING_CI_01
doc_type: chantier_child_closeout
repo: opt-trading
project: opt-trading
module: openclaw
go_id: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_NON_BLOCKING_CI_01
chantier_parent: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01
status: draft
lifecycle_stage: child_opening
surface: docs/chantiers
source_kind: canonical_child
updated_at: 2026-05-16
topic_keys:
  - openclaw
  - runtime_security
  - ci
  - warning_only
  - manual
  - no_runtime
  - why
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/SPEC_RUNTIME_SECURITY_PARENT_01.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_VALIDATOR_TESTS_01.md
  - tools/openclaw/validate_skill_policy_static.py
  - tests/openclaw/test_validate_skill_policy_static.py
---

# GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_NON_BLOCKING_CI_01

## 1_MASTER_TARGET

Ajouter une execution CI non bloquante ou manuelle pour le validateur OpenClaw skill policy, sans transformer les warnings en blocage.

## 3_INITIAL_NEED

Le validateur statique et ses tests existent deja et prouvent le mode `WARNING_ONLY`.

Le besoin courant est de rendre ce controle visible dans GitHub Actions sans en faire un garde bloquant pour les PR.

## 5_GO_PLAN

Parent :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01
```

Child courant :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_NON_BLOCKING_CI_01
```

Fichiers ajoutes :

```text
.github/workflows/openclaw-skill-policy-warning-only.yml
docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_NON_BLOCKING_CI_01.md
```

## 6_FINAL_TARGET

Ajouter une execution CI non bloquante ou manuelle qui verifie le validateur OpenClaw skill policy en mode warning-only, sans bloquer la CI principale ni activer de runtime.

## WHY

Ce child existe pour rendre visible l'etat warning-only de la policy OpenClaw dans GitHub Actions sans transformer la validation en garde bloquante prematuree.

Le but est d'observer, pas de bloquer.

## 7_CANONICAL_STATE

Etat valide :

- PR #448 mergee ;
- validateur statique disponible ;
- tests stdlib ajoutes ;
- mode warning-only etabli ;
- branche child dediee creee ;
- CI non bloquante demandee ;
- aucun runtime modifie ;
- aucun index global modifie.

## 8_VALIDATED_PLAN

- Ajouter un workflow manuel ou non bloquant.
- Executer le validateur statique.
- Executer les tests `unittest`.
- Ne pas utiliser `--strict-exit` par defaut.
- Ne pas modifier les fichiers sources.
- Ne pas introduire de runtime.
- Ne pas bloquer les PR.

## 9_SELECTED_SOLUTION

Workflow GitHub Actions manuel en mode warning-only.

| Element | Choix |
| --- | --- |
| Declencheur | `workflow_dispatch` manuel |
| But | Observabilite GitHub Actions |
| Sortie | warnings visibles, pas de gate bloquant |
| Commandes | `python tools/openclaw/validate_skill_policy_static.py` ; `python -m unittest tests.openclaw.test_validate_skill_policy_static` |

## 11_KEY_DECISIONS

- Le workflow ne doit pas bloquer les PR.
- Le workflow ne doit pas lancer de runtime OpenClaw.
- Le workflow ne doit pas utiliser `--strict-exit` par defaut.
- Le workflow doit garder le comportement `WARNING_ONLY` visible.
- Le child reste doc-only sauf workflow GitHub Actions explicitement demande.

## 12_INVARIANTS

- WARNING_ONLY
- aucun runtime
- aucun service
- aucun secret
- aucun auto-fix
- aucun index global
- aucune mutation de fichier
- aucune CI bloquante pour les PR
- aucune execution destructive

## 13_ESTABLISHED

- `tools/openclaw/validate_skill_policy_static.py` existe ;
- `tests/openclaw/test_validate_skill_policy_static.py` existe ;
- la policy warning-only est prouvee par tests ;
- le prochain pas logique est une execution CI manuelle ou non bloquante ;
- la verification doit rester sans `--strict-exit` par defaut.

## 14_HYPOTHESIS

À valider ensuite :

- si un workflow manual suffit pour la visibilite voulue ;
- si un job non bloquant sur PR doit venir plus tard ;
- si un rapport JSON sera utile pour les humains et l'automatisation ;
- si la policy doit etre repliquee dans d'autres surfaces OpenClaw.

## 15_REMAINING_GAP

- Pas encore de workflow CI manuel/non bloquant.
- Pas encore de rapport machine-readable.
- Pas encore de validation de policy dans GitHub Actions.
- Pas encore de point de reprise pour le rapport JSON.

## 16_TODO

Suite logique :

1. Reviewer le workflow ajoute.
2. Merger la PR du child.
3. Ouvrir le child suivant pour le rapport JSON.
4. N'activer aucune CI bloquante.

## 17_RESUME_POINT

Reprendre ici :

```text
.github/workflows/openclaw-skill-policy-warning-only.yml
```

Prochain GO logique :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_REPORT_01
```

Objectif prochain : produire un rapport machine-readable, toujours warning-only.
