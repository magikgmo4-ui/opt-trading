# GO_GITHUB_PARK_BRANCH_TRUNK_CROSS_AUDIT_01 — 02_journal_technique

## Besoin initial

Exécuter un audit croisé trunk / branches / rôle de fichiers du GitHub park, en partant du cadrage parent et en utilisant les supports externes uniquement comme matériaux de vérification secondaire.

## Cible finale locale GO

Produire une cartographie bornée permettant de répondre, repo par repo :
- trunk inspecté (oui/non) et sur quelle branche canonique
- branches observées (vue GitHub) et cohérence avec trunk/default branch
- rôle principal du repo (exécution / gouvernance / consumer / legacy) et signaux de mélange
- contradictions éventuelles entre supports

## Plan retenu

1. Établir l’état Git réel du repo canonique `opt-trading` (trunk `sot/mainline`).
2. Lire le cadrage parent `GO_GITHUB_PARK_AUDIT_EXPANSION_01`.
3. Extraire des supports secondaires les informations minimales utiles :
   - inventaire parc (repos, branches, trunk inspecté)
   - cartographie rôle des fichiers par repo
4. Établir la cohérence trunk vs branches vs rôle déclaré.
5. Écrire un résultat borné : ETABLI / HYPOTHESE / CONTRADICTION / GAP restant / TODO / REPRISE / Verdict.

## ETABLI

### Canon repo-first

- source canonique d’exécution : repo `opt-trading` (branche `sot/mainline`)
- supports secondaires (hors repo) : `C:\Users\ghost\bundle_zip\` (ZIP / inventaires)

### Parc visible (synthèse)

À partir de `github_repo_inventory_full.md` et `github_repo_inventory_full.json` :
- repos visibles : 8
- default branch + trunk inspecté (résumé) :
  - `opt-trading` : default `sot/mainline` ; trunk inspecté = oui ; branches = 98
  - `localcms` : default `main` ; trunk inspecté = oui ; branches = 2
  - `openclaw` : default `main` ; trunk inspecté = oui ; branches = 4
  - `hf_trading` : default `main` ; trunk inspecté = oui ; branches = 1
  - `Llm-wiki` : default `main` ; trunk inspecté = oui ; branches = 1
  - `Magikgmo` : default `main` ; trunk inspecté = non ; branches = 1
  - `algo_hf` : default `main` ; trunk inspecté = non ; branches = 1
  - `Llm-wiki-minimal` : default `main` ; trunk inspecté = non (support `full.json`)

### Cohérence trunk vs branches (constats bornés)

- cohérence triviale quand trunk inspecté = oui et default branch connue :
  - `opt-trading` : trunk inspecté `sot/mainline` cohérent avec default branch `sot/mainline`
  - `localcms`, `openclaw`, `hf_trading`, `Llm-wiki` : trunk inspecté `main` cohérent avec default branch `main`
- pour les repos trunk non inspecté, la cohérence “contenu trunk vs rôle” ne peut pas être conclue :
  - `Magikgmo`, `algo_hf`, `Llm-wiki-minimal` (selon `full.json`)

### Rôle de fichiers (cartographie ZIP)

À partir du bundle `github_park_file_role_cartography_01_bundle.zip` (repos couverts via ZIP : opt-trading, localcms, openclaw, hf_trading, Llm-wiki-minimal, Llm-wiki) :
- `opt-trading` : dominant `runtime` (682) + `gouvernance` (369) + `doc` (365) + `code` (285) ; `legacy` non nul (85)
- `openclaw` : dominant `gouvernance` (30) ; très faible `code` (1) ; `consumer` (8)
- `localcms` : mix `gouvernance` (34) / `code` (33) / `doc` (19)
- `hf_trading` : petit bootstrap, dominante `gouvernance`
- `Llm-wiki` : classé `legacy` (placeholder)

## HYPOTHESE

- `opt-trading` est un repo “canon d’exécution” qui contient aussi une gouvernance locale épaisse ; cela explique la densité d’indices, chantiers, closings et normes dans le même repo.
- la présence de 98 branches sur `opt-trading` suggère une stratégie “multi-lanes” (feat/integ/docs/save) qui doit être auditée pour séparation trunk vs branches (risque : branches gelées ou obsolètes maintenues).

## CONTRADICTION

- `Llm-wiki-minimal` :
  - `github_repo_inventory_full.md` et `github_repo_inventory_full.json` indiquent trunk inspecté = non
  - `github_repo_inventory_from_zips_v2.md` et la cartographie `github_park_file_role_cartography_01.md` le listent comme couvert via ZIP (34 fichiers) et donc trunk inspecté matériellement
- conséquence : statut “trunk inspecté” de `Llm-wiki-minimal` doit être revalidé (support secondaire incohérent).

## GAP restant

- manque de preuve repo-first sur le parc complet :
  - trunks ZIP manquants pour les repos non inspectés (`Magikgmo`, `algo_hf`) si l’objectif est une cartographie “contenu” complète
- incohérence à résoudre sur `Llm-wiki-minimal` (trunk inspecté oui/non).

## TODO

- trancher la contradiction `Llm-wiki-minimal` en vérifiant si un ZIP trunk existe réellement et a été utilisé (et si oui, corriger le support JSON à la source secondaire, sans le promouvoir en canon).
- si nécessaire, obtenir les ZIP trunk manquants (`Magikgmo`, `algo_hf`) pour une vue “contenu” comparable.
- préparer une passe 2 bornée : “classification par finalité des branches” de `opt-trading` (root/sot/integ/feat/docs/save) afin d’identifier les branches à geler/archiver.

## REPRISE

- reprise canonique : `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/00_cadrage.md`
- point de reprise immédiat : résoudre `Llm-wiki-minimal` (trunk inspecté oui/non), puis exécuter `GO_GITHUB_PARK_BRANCH_TRUNK_CROSS_AUDIT_01` sur un parc sans contradiction.

## Verdict PASS / FAIL / OPEN

OPEN
