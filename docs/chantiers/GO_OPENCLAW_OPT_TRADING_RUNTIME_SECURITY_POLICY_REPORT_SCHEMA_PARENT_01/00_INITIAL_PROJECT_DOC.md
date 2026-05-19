---
doc_id: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01_INITIAL
doc_type: chantier_parent_spec
repo: opt-trading
project: opt-trading
module: openclaw
go_id: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01
status: draft
lifecycle_stage: opening
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-16
topic_keys:
  - openclaw
  - runtime_security
  - policy_report
  - json_schema
  - warning_only
  - why
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_CLOSEOUT_01.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_ARTIFACT_REVIEW_01.md
  - docs/index/inbox/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01.md
---

# GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01

## 1_MASTER_TARGET

Formaliser un schema stable du rapport JSON produit par le validateur OpenClaw skill policy afin de rendre les artefacts warning-only comparables, validables et exploitables par CI, dashboard, registry ou collector.

## 2_INITIAL_PROJECT_DOC

Document initial transporteur du chantier :

`docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01/00_INITIAL_PROJECT_DOC.md`

Role :
- figer le cadrage parent ;
- separer ce chantier de la session conversationnelle ;
- poser le `FINAL_TARGET` ;
- integrer explicitement le `WHY` ;
- servir de reference de reprise locale.

Ce document reste la fiche de reference obligatoire du chantier tant qu'aucun changement explicite du projet ne le remplace.

## 3_INITIAL_NEED

La boucle OpenClaw warning-only est maintenant prouvee en execution reelle : workflow manuel, artefact JSON publie et revue de l'artefact `openclaw-skill-policy-report` avec `findings_count: 0`.

Le besoin suivant n'est plus de prouver l'existence du rapport, mais de transformer cette sortie reelle en contrat stable : champs requis, types, invariants, versioning, compatibilite future et exemples valides.

Sans schema formel, les futurs consommateurs du rapport risquent d'implementer des interpretations divergentes du meme JSON.

## 4_MASTER_PROJECT_PLAN

Plan parent valide :

1. Ouvrir un parent dedie au schema du rapport JSON policy.
2. Repartir de l'etat confirme `REAL_ARTIFACT_CONFIRMED` et `WARNING_ONLY_CONFIRMED`.
3. Rester en documentation et schema uniquement au demarrage.
4. Definir les champs obligatoires et optionnels.
5. Definir les types et contraintes de valeurs.
6. Definir les invariants warning-only et no-runtime.
7. Definir la strategie de versioning et de compatibilite.
8. Definir des exemples valides et cas limites cibles.
9. Ne modifier ni runtime, ni workflow, ni validateur, ni policy YAML, ni index globaux.

## WHY

Ce parent existe pour transformer le rapport JSON reel en contrat stable exploitable par CI, dashboard, registry ou collector sans activer de runtime ni bloquer les workflows.

Le but n'est pas d'ajouter une nouvelle execution, mais de stabiliser l'interface machine-readable issue de la boucle warning-only deja prouvee.

## 5_GO_PLAN

GO parent :

`GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01`

Branche dediee :

`go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01`

Flux initial :

1. Ouvrir le parent doc-only du schema de rapport.
2. Creer le document initial local.
3. Ajouter une inbox courte de continuite.
4. Ouvrir une PR doc-only.
5. Ouvrir ensuite des children bornes pour schema detaille, echantillons ou compatibilite si le parent est accepte.

## 6_FINAL_TARGET

**FINAL_TARGET : definir un schema stable du rapport JSON OpenClaw policy, incluant champs requis, types, invariants, compatibilite future, versioning, exemples valides et regles warning-only, afin de rendre les artefacts futurs validables et comparables sans activer de runtime ni rendre les workflows bloquants.**

## 7_CANONICAL_STATE

Etat valide a l'ouverture :

- `OPENCLAW_RUNTIME_SECURITY_POLICY_CHAIN: REAL_ARTIFACT_CONFIRMED` ;
- `OPENCLAW_RUNTIME_SECURITY_PARENT_STATUS: WARNING_ONLY_CONFIRMED` ;
- closeout parent precedent redige ;
- preuve reelle disponible via le run `25956668749` ;
- artefact reel disponible : `openclaw-skill-policy-report` ;
- JSON reel confirme avec `mode: WARNING_ONLY`, `runtime_execution: DISABLED`, `mutation: DISABLED`, `findings_count: 0` et `findings: []` ;
- scope initial doc-only ;
- aucun runtime a modifier ;
- aucun workflow a modifier ;
- aucun validateur a modifier ;
- aucune policy YAML a modifier ;
- aucun index global a modifier.

## 8_VALIDATED_PLAN

Etapes validees :

1. Ouvrir le parent.
2. Creer `00_INITIAL_PROJECT_DOC.md`.
3. Creer une inbox minimale de continuite.
4. Definir le contrat documentaire du rapport JSON.
5. Lister les consommateurs cibles sans les implementer.
6. Preparer les futurs children de schema detaille si necessaire.
7. Ne pas modifier `GO_INDEX`, `ACTIVE_STREAMS`, `NEXT_GO_CANDIDATES`, `REPRISE` ou `BRANCH_STATE` sans instruction explicite.

## 9_SELECTED_SOLUTION

Approche retenue : parent documentaire centre sur le contrat de sortie JSON, non sur son execution.

Le chantier commence par un cadre de schema afin de definir :

- les champs obligatoires du rapport ;
- les champs optionnels permis ;
- les types et formats attendus ;
- les valeurs enumerees stables ;
- les invariants warning-only ;
- les regles de compatibilite ascendante ;
- les regles de versioning du rapport ;
- les exemples minimaux valides ;
- les attentes pour des findings non nuls dans le futur.

## 11_KEY_DECISIONS

- Ouvrir un nouveau parent distinct du parent runtime security initial.
- Partir de la preuve reelle du rapport existant, pas d'un JSON theorique.
- Garder le scope initial strictement doc/schema-only.
- Traiter le schema comme contrat machine-readable stable avant tout lien plus large au skill registry.
- Garder `WARNING_ONLY` comme invariant de phase.

## 12_INVARIANTS

- aucun runtime OpenClaw execute par ce parent ;
- aucun workflow modifie ;
- aucun validateur modifie ;
- aucune policy YAML modifiee ;
- aucun service ;
- aucun secret ;
- aucun auto-fix ;
- aucune CI bloquante ajoutee ;
- aucun index global modifie.

## 13_ESTABLISHED

Etat etabli a la base de ce parent :

- la chaine parent precedente est consolidee jusqu'au closeout ;
- le workflow reel reference est `25956668749` ;
- l'artefact reel reference est `openclaw-skill-policy-report` ;
- le rapport JSON reel minimal confirme est :

```json
{
  "mode": "WARNING_ONLY",
  "runtime_execution": "DISABLED",
  "mutation": "DISABLED",
  "findings_count": 0,
  "findings": []
}
```

- les clarifications PR deja fixes dans la phase precedente restent valides :
- `#453` -> `GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_REPORT_01`
- `#454` -> `GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_CI_ARTIFACT_01`

## 14_HYPOTHESIS

Hypotheses a valider dans des children futurs :

- un schema formel de type JSON Schema stdlib-friendly est souhaitable ;
- un champ de version de rapport pourra devenir necessaire ;
- des exemples multi-samples avec findings non nuls seront utiles ;
- un lien futur au skill registry gagnera a consommer un schema deja stabilise ;
- un dashboard ou collector pourra s'appuyer sur les memes invariants warning-only.

## 15_REMAINING_GAP

Gaps restants :

- pas encore de schema formel du rapport JSON ;
- pas encore de politique explicite de versioning ;
- pas encore d'exemples valides/invalides normalises ;
- pas encore de contrat de compatibilite future ;
- pas encore de liste canonique de consommateurs cibles ;
- pas encore de child detaille pour le schema lui-meme.

## 16_TODO

Suite documentaire proposee :

1. Definir les champs et types obligatoires du rapport.
2. Formaliser les invariants warning-only et no-runtime.
3. Definir la strategie de versioning et de compatibilite.
4. Ajouter des exemples valides minimaux et etendus.
5. Ouvrir ensuite un child borne pour le schema detaille si le parent est accepte.

## 17_RESUME_POINT

Reprendre ici :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01
```

Point de reprise concret :

```text
docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01/00_INITIAL_PROJECT_DOC.md
```
