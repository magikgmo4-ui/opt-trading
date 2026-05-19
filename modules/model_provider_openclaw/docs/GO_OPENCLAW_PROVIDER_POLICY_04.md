# GO_OPENCLAW_PROVIDER_POLICY_04

## Classification
Type : module durable

## But

Faire passer `model_provider_openclaw` du statut de doctrine V1 au statut de maillon opératoire explicite dans la chaîne OpenClaw.

Ce GO borne ce que le module apporte réellement :
- lecture et validation de la policy providers ;
- lecture et validation de la matrice agent -> provider / modèle / fallback / limites ;
- export JSON relisible ;
- usage en amont de `configure_openclaw`, `doctor_openclaw` et `evidence_openclaw`.

Ce GO ne prétend pas que le module pilote encore directement la config live OpenClaw.

## Base réelle déjà établie

- le module existe dans la registry `install_module_openclaw`
- le module expose `status`, `sanity`, `show-agent`, `export-json`
- la doctrine V1 impose des providers autorisés, des fallbacks obligatoires et des limites par agent
- le code Python valide la lisibilité des YAML, la présence des agents requis et la conformité des bornes

## Politique V1 retenue

### Providers autorisés
- `openrouter`
- `openai_compatible_local`

### Provider refusé par défaut
- tout provider non listé ; dans le fichier courant, `unrestricted` est explicitement refusé

### Agents couverts
- `orchestrateur`
- `builder`
- `reviewer`
- `lab`

## Séquence minimale recommandée

### Passe lecture policy

```bash
cd /opt/trading
bash modules/model_provider_openclaw/scripts/sanity.sh
bash modules/model_provider_openclaw/scripts/cmd.sh status
bash modules/model_provider_openclaw/scripts/cmd.sh show-agent orchestrateur
bash modules/model_provider_openclaw/scripts/cmd.sh show-agent reviewer
bash modules/model_provider_openclaw/scripts/cmd.sh export-json
```

### Passe chaîne OpenClaw liée

```bash
sudo -iu openclaw
cd /opt/trading
bash modules/configure_openclaw/scripts/cmd.sh status
bash modules/doctor_openclaw/scripts/cmd.sh status
bash modules/evidence_openclaw/scripts/cmd.sh status
```

## Rôle dans la chaîne

Ordre pratique :
1. relire la policy via `model_provider_openclaw`
2. relire la façade opérateur via `configure_openclaw`
3. relire le runtime via `doctor_openclaw`
4. exporter la preuve via `evidence_openclaw`

`model_provider_openclaw` joue donc le rôle de couche de politique et de validation en amont des autres façades.

## Condition de close

Le GO est considéré clos si :
- la place du module dans la chaîne est écrite explicitement ;
- ses commandes et son périmètre sont relisibles ;
- il n est plus présenté comme simple doctrine flottante ;
- le point de reprise suivant est clair.

## Hors périmètre

- pas d appel provider réel ajouté par ce GO ;
- pas de mutation automatique de la config live OpenClaw ;
- pas d exposition réseau nouvelle ;
- pas de mélange avec le repo `openclaw` doc/gouvernance-only.

## Point de reprise suivant

Après ce GO :
- soit patch local si une liaison utilitaire manque réellement entre `model_provider_openclaw` et une façade existante ;
- soit poursuite normale de la chaîne avec preuves si un besoin terrain l exige.
