---
doc_id: OPT_TRADING_GUIDE_DEEPSEEK_STUDENT
doc_type: user_guide
repo: opt-trading
status: reference
lifecycle_stage: product_usage
source_kind: canonical
updated_at: 2026-05-18
links:
  - docs/student_deepseek_runbook.md
  - docs/status/deepseek_student_canonique.md
  - docs/product_targets/DEEPSEEK_OLLAMA_TARGET_CANON.md
  - docs/chantiers/GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_IMPL_03/90_CLOSEOUT.md
  - docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/90_CLOSEOUT.md
---

# Guide - Deepseek Student

## 1_MASTER_TARGET

Surface locale DeepSeek/Ollama stable cote `student`, avec wrappers operateur, sorties archivees et validation externe obligatoire.

## FINAL_TARGET

Duo local thinking/response stable avec un workspace canonique unique, wrappers utilisables a distance et frontiere claire avec les integrations plus larges.

## CURRENT_STATE

`USABLE_LIMITED` -- La surface est exploitable via `deepseek-student`, `menu-deepseek-student` et `sanity-deepseek-student`. Le workspace canonique est clarifie, mais le legacy `scripts/student/` reste preserve pour compatibilite.

## USAGE_ALLOWED_NOW

- Executer des analyses locales via les wrappers `deepseek-student`.
- Lire les logs et les sorties archivees.
- Produire un rapport quotidien ou relire le dernier rapport.
- Utiliser la surface cote `student` comme outil d'analyse locale borne.

## USAGE_FORBIDDEN_NOW

- Utiliser la surface comme moteur de decision autonome.
- Retirer `scripts/student/` sans verification de `post_change.sh`.
- Conclure que le lab OpenClaw cote `student` est deja qualifie.
- Contourner la validation externe obligatoire.

## IMPLEMENTATION_PATH

1. Verifier les callers `post_change.sh` avant tout retrait legacy.
2. Decider si `scripts/student/` peut etre retire ou doit rester en compatibilite.
3. Reprendre la qualification `OpenClaw lab` seulement si un besoin explicite reapparait.
4. Fermer un closeout de stabilisation avant toute promotion au-dessus de `USABLE_LIMITED`.

## CONTINUITY_STATE

Actif -- workspace canonique clarifie, legacy preserve, OpenClaw lab differe.

## MACHINE / SURFACE

`student` (analyse locale / wrappers DeepSeek)

## REPRISE_POINT

```text
docs/student_deepseek_runbook.md
docs/chantiers/GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_IMPL_03/90_CLOSEOUT.md
docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/90_CLOSEOUT.md
```

## TODO

1. Verifier les callers `post_change.sh`.
2. Confirmer si le legacy `scripts/student/` peut etre retire.
3. Garder la frontiere learning-only explicite.
4. Reprendre le lab OpenClaw seulement si un GO dedie le justifie.

## REMAINING_GAP

Dual-layout `student/scripts/` vs `scripts/student/`, verification des callers avant retrait legacy, OpenClaw lab toujours differe.

## NEXT_GO

Verifier `post_change.sh` avant tout retrait de `scripts/student/` ; ne rouvrir `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01` que si l'integration lab doit reprendre.

## PROMOTION_CONDITIONS

`USABLE_LIMITED` -> `USABLE_NOW` quand :
- le workspace unique est valide,
- les callers legacy sont audites,
- la stabilisation operateur est closee,
- la surface reste explicitement non autonome.

## Ce que c'est

Surface locale DeepSeek/Ollama cote `student`, exposee via wrappers operateur et archive de sorties.

## A quoi ca sert

Lancer des analyses locales, consulter les sorties thinking/response, relire des rapports quotidiens et preparer des lectures techniques bornees.

## Quand l'utiliser

- Pour lancer une analyse locale `think` ou `response`.
- Pour verifier l'etat de la surface avec `sanity-deepseek-student`.
- Pour lire les derniers logs ou rapports archives.
- Pour un usage d'analyse locale learning-only.

## Quand ne pas l'utiliser

- Pour une decision de trading autonome.
- Pour conclure que l'integration OpenClaw lab est active.
- Pour retirer le legacy sans verification.

## Prerequis

- Acces SSH a `student`.
- Wrappers `deepseek-student`, `menu-deepseek-student`, `sanity-deepseek-student` disponibles.
- Module `deepseek_hub` present.
- Comprendre que la validation externe reste obligatoire.

## Commandes / acces

- Sanity : `sanity-deepseek-student`
- Think : `deepseek-student think "Analyser le module market_scanner"`
- Response : `deepseek-student response "Expliquer la strategie de risque"`
- Rapport quotidien : `deepseek-student daily-log-report`
- Derniere reponse : `deepseek-student show-latest-response`

## Procedure simple

1. Se connecter a `student`.
2. Lancer `sanity-deepseek-student`.
3. Executer un `think` ou un `response` via le wrapper.
4. Lire les sorties archivees ou le dernier rapport.
5. Garder une validation externe pour toute decision aval.

## Verification PASS

- Les wrappers repondent.
- Les sorties sont bien archivees.
- Les logs sont lisibles.
- Aucune decision autonome n'est deployee.

## Limites

- Legacy encore present pour compatibilite.
- Frontiere OpenClaw lab encore differee.
- Surface learning-only, pas decisionnelle.

## Depannage

- Wrapper absent : verifier l'installation cote `student`.
- Log introuvable : verifier `data/logs/deepseek_student/`.
- Resultat manquant : relancer une commande `think` ou `response` puis consulter les liens latest.
- Doute sur le layout canonique : relire `DEEPSEEK_IMPL_03` avant toute action structurelle.

## Source canonique

- `docs/student_deepseek_runbook.md`
- `docs/status/deepseek_student_canonique.md`
- `docs/chantiers/GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_IMPL_03/90_CLOSEOUT.md`
- `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/90_CLOSEOUT.md`

## RISKS

- À qualifier.
