---
doc_id: GO_OPT_TRADING_RESEAU_SSH_TARGET_DECISION_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_TARGET_DECISION_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - reseau_ssh
  - target_decision
  - runtime
  - compat
  - rollback
surface: docs
source_kind: canonical
updated_at: 2026-04-20
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01/00_cadrage.md
  - docs/status/reseau_ssh_canonique.md
---

# GO_OPT_TRADING_RESEAU_SSH_TARGET_DECISION_01 — Cadrage

## Objet

Ouvrir un lot de décision technique doc-only pour figer la cible finale unique de `reseau_ssh`, avant tout GO physique.

Ce GO ne réalise aucune exécution machine. Il sert à transformer le cadrage documentaire et l'audit machine en décision préalable opposable.

---

## Règle de sécurité

Ce GO est strictement doc-only.

Interdits :
- aucun patch runtime
- aucun retrait
- aucun renommage
- aucun repointage
- aucune modification de symlink
- aucune modification liée à `fantome`
- aucune fusion physique `step1b` / `step2`
- aucune migration implicite “au passage”

Le verdict directeur reste :
- PASS documentaire
- NO_GO_PHYSICAL maintenu

---

## Références de départ

- `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01/00_cadrage.md`
- `docs/status/reseau_ssh_canonique.md`

État acquis :
- canon opérateur actuel : `scripts/reseau_ssh/`
- survivant de famille : `modules/reseau_ssh_step2`
- `modules/reseau_ssh_step2` n'est pas encore canon opérateur
- `modules/reseau_ssh_step1b` reste legacy / compat à risque
- wrappers racine présents sur les machines Linux auditées
- compat `*_reseau_ssh_step2` déployée sur `db-layer` et `student`, absente sur `admin-trading`

---

## Décision cible finale unique

### Cible module unique finale

La cible module unique retenue pour la trajectoire physique future est :

`modules/reseau_ssh_step2`

Décision :
- `modules/reseau_ssh_step2` devient la cible de convergence de la famille `reseau_ssh`
- `modules/reseau_ssh_step1b` ne devient pas cible finale
- `modules/reseau_ssh` ne devient pas cible finale
- aucune nouvelle cible unifiée n'est créée dans ce GO

### Runtime final

Le runtime final attendu, après GO physique séparé et validation machine, est :

- interface opérateur finale : alias courts `menu-reseau_ssh`, `cmd-reseau_ssh`, `sanity-reseau_ssh`
- implémentation cible finale : wrappers/scripts issus de `modules/reseau_ssh_step2`

Décision :
- les alias courts restent le contrat opérateur stable
- la cible d'implémentation future est `modules/reseau_ssh_step2`
- `scripts/reseau_ssh/` reste canon opérateur actuel jusqu'à migration explicite
- aucune bascule de `scripts/reseau_ssh/` vers `modules/reseau_ssh_step2` n'est autorisée dans ce GO

### Statuts finaux visés

| Surface | Statut actuel | Statut final visé | Décision |
| --- | --- | --- | --- |
| `scripts/reseau_ssh/` | canon opérateur actuel | compat runtime transitoire puis archive/legacy seulement après migration validée | ne pas retirer dans ce GO |
| `modules/reseau_ssh_step2` | survivant de famille / compat transitoire | cible module unique et implémentation finale | cible validée pour futur GO physique |
| `modules/reseau_ssh_step1b` | legacy / compat à risque | legacy gelé puis archive possible | retrait interdit avant convergence validée |
| `modules/reseau_ssh` | legacy / doc pré-step | archive / doc historique | retrait interdit avant décision archive dédiée |
| wrappers racine `scripts/reseau_ssh_cmd.sh`, `scripts/reseau_ssh_menu.sh` | candidate-retire-later | retrait différé possible | retrait seulement après stabilité prouvée |
| alias courts `menu-reseau_ssh`, `cmd-reseau_ssh`, `sanity-reseau_ssh` | canon opérateur actuel | interface opérateur finale | à conserver comme contrat utilisateur |
| alias `*_reseau_ssh_step2` | compat transitoire sur certaines machines | supprimés ou gelés après bascule alias courts | retrait différé, machine par machine |

---

## Politique machine par machine

| Machine | État actuel établi | Politique de migration future | Condition minimale avant action |
| --- | --- | --- | --- |
| `admin-trading` | alias courts canoniques présents ; compat `step2` absente ; wrappers racine présents | installer/valider la cible `step2` sans retirer l'existant, puis repointer alias courts si smoke OK | rollback des 3 alias courts + vérification `scripts/reseau_ssh/` disponible |
| `db-layer` | alias courts canoniques présents ; compat `step2` présente ; wrappers racine présents | utiliser la compat `step2` existante comme preuve de transition, puis repointer alias courts si smoke OK | smoke alias courts et `*_step2`, rollback symlink complet |
| `student` | alias courts canoniques présents ; compat `step2` présente ; historique `step1b` prouvé ; wrappers racine présents | traiter comme machine à plus fort risque ; ne retirer aucune compat avant stabilité prolongée | audit historique validé + smoke alias courts + rollback + conservation `step1b` |
| `cursor-ai` / WSL | aucune surface locale `reseau_ssh` détectée dans PATH/profils Windows ; WSL non exploité dans l'audit | pas de migration locale prévue sans preuve d'une surface Linux locale | audit WSL dédié seulement si une distribution devient pertinente |

---

## Mapping actuel vers final

| Surface actuelle | Cible finale | Action future admissible | Rollback attendu | Test obligatoire |
| --- | --- | --- | --- | --- |
| `/usr/local/bin/menu-reseau_ssh` | alias court conservé, cible future `modules/reseau_ssh_step2` | repointage en GO physique uniquement | restaurer cible précédente vers `scripts/reseau_ssh/reseau_ssh_menu.sh` | `menu-reseau_ssh` ouvre le menu |
| `/usr/local/bin/cmd-reseau_ssh` | alias court conservé, cible future `modules/reseau_ssh_step2` | repointage en GO physique uniquement | restaurer cible précédente vers `scripts/reseau_ssh/reseau_ssh_cmd.sh` | `cmd-reseau_ssh sanity` |
| `/usr/local/bin/sanity-reseau_ssh` | alias court conservé, cible future `modules/reseau_ssh_step2` | repointage en GO physique uniquement | restaurer cible précédente vers `scripts/reseau_ssh/sanity_reseau_ssh.sh` | `sanity-reseau_ssh` |
| `/usr/local/bin/*_reseau_ssh_step2` | compat temporaire | conserver pendant migration ; retirer seulement après stabilité | restaurer symlink `step2` si nécessaire | `*_reseau_ssh_step2` smoke avant/après |
| `/opt/trading/scripts/reseau_ssh/` | runtime actuel puis compat/archive | conserver pendant toute migration initiale | laisser intact pour retour arrière | smoke scripts directs |
| `/opt/trading/modules/reseau_ssh_step2/` | cible finale | installer/valider comme cible unique | revenir aux alias courts vers `scripts/reseau_ssh/` | sanity module + commandes WG/firewall non destructives |
| `/opt/trading/scripts/reseau_ssh_cmd.sh` | retrait différé possible | ne pas retirer dans le GO physique initial | restaurer fichier depuis backup si retrait futur validé | vérification absence de callers |
| `/opt/trading/scripts/reseau_ssh_menu.sh` | retrait différé possible | ne pas retirer dans le GO physique initial | restaurer fichier depuis backup si retrait futur validé | vérification absence de callers |
| `modules/reseau_ssh_step1b` | legacy gelé / archive future | geler, ne pas retirer dans le GO physique initial | conserver copie intacte | vérifier absence d'appel actif |

---

## Rollback attendu pour le futur GO physique

Le futur GO physique devra fournir, avant exécution :

- snapshot des symlinks `/usr/local/bin/menu-reseau_ssh`, `/usr/local/bin/cmd-reseau_ssh`, `/usr/local/bin/sanity-reseau_ssh`
- snapshot des symlinks `*_reseau_ssh_step2` quand présents
- liste des cibles `readlink -f` avant mutation
- copie ou hash des wrappers racine avant toute action
- commande de restauration par machine
- critère d'abandon si un smoke échoue

Rollback minimal attendu :
- restaurer les alias courts vers `scripts/reseau_ssh/`
- conserver `scripts/reseau_ssh/` intact
- conserver les wrappers racine
- conserver `step1b`
- annuler toute promotion de `step2` si smoke KO

---

## Smoke tests obligatoires

Par machine :
- `command -v menu-reseau_ssh`
- `command -v cmd-reseau_ssh`
- `command -v sanity-reseau_ssh`
- `readlink -f /usr/local/bin/menu-reseau_ssh`
- `readlink -f /usr/local/bin/cmd-reseau_ssh`
- `readlink -f /usr/local/bin/sanity-reseau_ssh`
- `sanity-reseau_ssh`
- `cmd-reseau_ssh sanity`
- test menu non destructif
- vérification de présence de `scripts/reseau_ssh/` pour rollback

Pour les machines avec compat `step2` :
- `command -v menu-reseau_ssh_step2`
- `command -v cmd-reseau_ssh_step2`
- `command -v sanity-reseau_ssh_step2`
- `sanity-reseau_ssh_step2`

---

## Critères de retrait différé

Un retrait futur ne devient admissible que si :

- alias courts fonctionnent sur la cible finale pendant une période de stabilité définie
- aucun caller actif des wrappers racine n'est prouvé
- historique `step1b` est classé historique seulement, sans usage actif
- rollback a été testé
- chaque machine a un état final documenté
- le parent `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03` accepte explicitement la suite physique

Retraits explicitement différés :
- wrappers racine
- alias `*_reseau_ssh_step2`
- surfaces `step1b`
- surfaces `modules/reseau_ssh`

---

## Conditions d'ouverture du futur GO physique

Le futur GO physique ne peut être ouvert que si les éléments suivants sont présents :

1. cible finale validée : `modules/reseau_ssh_step2`
2. runtime final validé : alias courts conservés, implémentation future issue de `modules/reseau_ssh_step2`
3. matrice machine validée pour `admin-trading`, `db-layer`, `student`
4. commandes de rollback écrites avant exécution
5. smoke tests écrits avant exécution
6. ordre machine par machine validé
7. interdiction de retrait dans la première phase physique

Nom naturel du futur GO physique :

`GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01`

---

## Point de reprise

Le vrai verrou n'est plus l'audit. Le verrou désormais levé côté décision est :

- cible module unique finale : `modules/reseau_ssh_step2`
- interface opérateur finale : alias courts `menu-reseau_ssh`, `cmd-reseau_ssh`, `sanity-reseau_ssh`
- migration physique : interdite dans ce GO, à ouvrir séparément

Ordre retenu :
1. clôturer ce GO de décision en PASS documentaire si accepté
2. ouvrir un GO physique séparé
3. déployer/valider `modules/reseau_ssh_step2` sans casser l'existant
4. repointer les alias courts machine par machine avec rollback
5. conserver compat et wrappers
6. retirer seulement dans une phase différée après stabilité

---

## Verdict

PASS documentaire attendu pour ce GO de décision.

NO_GO_PHYSICAL maintenu.

Ce GO ne donne aucun feu vert technique d'exécution.
