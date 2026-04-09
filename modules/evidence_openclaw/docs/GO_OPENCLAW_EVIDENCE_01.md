# GO_OPENCLAW_EVIDENCE_01

## Classification
Type : diagnostic ponctuel

## But
Produire un état réel OpenClaw lisible et exportable avant toute revalidation documentaire du repo `openclaw`.

## Repo canonique
- repo d exécution : `opt-trading`
- branche canonique : `sot/mainline`
- périmètre : collecte de preuves seulement

## Préconditions
- exécuter sous l utilisateur `openclaw`
- la commande `openclaw` doit être disponible
- `python3` doit être disponible

Ces préconditions sont celles vérifiées par `modules/evidence_openclaw/scripts/sanity.sh`.

## Séquence opératoire exacte
```bash
sudo -iu openclaw
cd /opt/trading
bash modules/evidence_openclaw/scripts/sanity.sh
bash modules/evidence_openclaw/scripts/cmd.sh status
bash modules/evidence_openclaw/scripts/cmd.sh export-docs
bash modules/evidence_openclaw/scripts/cmd.sh show-files
bash modules/evidence_openclaw/scripts/cmd.sh print-doc-prompt
```

## Ce que fait `export-docs`
Le module :
- détecte le workspace du default agent ;
- crée `docs_evidence/openclaw_current_state/` dans ce workspace ;
- écrit :
  - `01_doctor_status.txt`
  - `02_configure_status.txt`
  - `03_doctor_quick.txt`
  - `04_workspace_context.txt`
  - `90_PROMPT_DOCS.txt`

## Sortie attendue
Répertoire cible :
`<workspace>/docs_evidence/openclaw_current_state/`

Fichiers attendus :
- `01_doctor_status.txt`
- `02_configure_status.txt`
- `03_doctor_quick.txt`
- `04_workspace_context.txt`
- `90_PROMPT_DOCS.txt`

## Conditions de close
Le GO est considéré clos si :
- `sanity.sh` passe ;
- `status` retourne un workspace et un evidence dir cohérents ;
- `export-docs` produit les 5 fichiers attendus ;
- `90_PROMPT_DOCS.txt` est lisible et prêt à être utilisé pour la passe documentaire suivante.

## Hors périmètre
- aucune modification de configuration runtime ;
- aucune exposition réseau nouvelle ;
- aucun compute standard sur `db-layer` ;
- aucune revalidation documentaire du repo `openclaw` dans ce GO.

## Point de reprise suivant
Une fois ce GO clos :
- ouvrir `GO_OPENCLAW_SYNC_02` ;
- relire les preuves exportées ;
- resynchroniser la documentation du repo `openclaw` avec ces preuves.
