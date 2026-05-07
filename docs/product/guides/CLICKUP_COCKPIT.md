---
doc_id: OPT_TRADING_GUIDE_CLICKUP_COCKPIT
doc_type: user_guide
repo: opt-trading
status: reference
lifecycle_stage: product_usage
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_EXECUTION_01/90_CLOSEOUT.md
  - docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_MANUAL_UI_COMPLETION_01/90_CLOSEOUT.md
  - docs/index/GO_INDEX.md
  - docs/index/BRANCH_STATE.md
---

# Guide utilisateur - ClickUp Cockpit

## Ce que c'est

Le cockpit ClickUp est la couche UI humaine pour suivre les GO, leurs branches, leurs preuves et leurs points de reprise.

## A quoi ca sert

Il sert a piloter rapidement un lot actif sans remplacer les preuves repo.

## Quand l'utiliser

- pour voir les GO actifs ;
- pour retrouver un lot par tache ;
- pour lire ou mettre a jour les champs GO visibles par humain ;
- pour suivre un pilotage multi-machine borne.

## Quand ne pas l'utiliser

- comme source canonique ;
- pour conclure seul sur un statut produit ;
- pour inventer un GO absent du repo.

## Prerequis

- acces au workspace ClickUp concerne ;
- acces au repo pour recroiser `GO_INDEX.md`, `BRANCH_STATE.md` et le closeout du GO ;
- aucune ecriture de secret dans le repo.

## Commandes / acces

- Workspace : `https://app.clickup.com/90141225112`
- Space CANON_GOVERNANCE : `https://app.clickup.com/90141225112/v/s/90145495925`
- List GO_ACTIVE : `https://app.clickup.com/90141225112/v/li/901416183794`

## Procedure simple

1. Ouvrir `GO_INDEX.md` ou le closeout canonique du lot cible.
2. Ouvrir la tache ClickUp correspondante dans `GO_ACTIVE`.
3. Verifier que `GO_ID`, `BRANCH`, `DOC_PATH`, `NEXT_GO` et `RESUME_POINT` pointent bien vers le repo.
4. Utiliser ClickUp pour suivre ou annoter l'avancement humain.
5. Revenir au repo pour toute preuve, verdict ou decision produit.

## Verification PASS

- la tache existe et pointe vers le bon GO ;
- les custom fields utiles sont remplis ;
- la navigation vers la preuve repo est immediate ;
- aucune conclusion produit n'est prise sans closeout repo.

## Limites

- le plan gratuit bloque encore des usages cibles ;
- statuses personnalises, dashboards et template restent limites ;
- ClickUp n'est pas la preuve de fond.

## Depannage

- Si un champ ClickUp contredit le repo : le repo gagne.
- Si une tache manque : partir du closeout repo avant toute recreation.
- Si une limite UI bloque un besoin : ouvrir un child dedie seulement si le besoin est reel.

## Source canonique

- `docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_EXECUTION_01/90_CLOSEOUT.md`
- `docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_MANUAL_UI_COMPLETION_01/90_CLOSEOUT.md`
- `docs/index/GO_INDEX.md`
- `docs/index/BRANCH_STATE.md`

## NEXT_GO

Pas de GO obligatoire a court terme.
Ouvrir un child dedie seulement si un besoin reel ou un upgrade plan doit fermer les limites UI restantes.
