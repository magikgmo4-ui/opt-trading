# GO_OPENCLAW_CHAIN_03

## Classification
Type : module durable

## But

Consolider la chaine operateur standard OpenClaw dans `opt-trading` en un parcours lisible, reproductible et borne.

Ce GO ne change pas la doctrine OpenClaw :
- `openclaw` reste doc/gouvernance-only ;
- `opt-trading` porte les modules operatoires ;
- aucun compute standard nouveau n est autorise sur `db-layer`.

## Chaine standard retenue

1. `install_module_openclaw`
2. `openclaw_config_modulaire`
3. `gateway_openclaw`
4. `configure_openclaw`
5. `doctor_openclaw`
6. `evidence_openclaw`

## Role de chaque maillon

### 1. install_module_openclaw

But : installer ou relire les modules OpenClaw declares dans la registry projet.

### 2. openclaw_config_modulaire

But : appliquer une config modulaire prudente avec backup, validate, probe et rollback si necessaire.

### 3. gateway_openclaw

But : garantir le pilotage du gateway local via `tmux` sous l utilisateur `openclaw`.

### 4. configure_openclaw

But : relire l etat de config et utiliser les commandes natives OpenClaw les plus sures.

### 5. doctor_openclaw

But : lancer les checks standardises `doctor`, `validate`, `health`, `probe`.

### 6. evidence_openclaw

But : exporter les preuves actuelles et generer le prompt documentaire associe.

## Sequence operatoire minimale

### Passe lecture / reprise

```bash
cd /opt/trading
bash modules/menu_openclaw/scripts/sanity.sh
bash modules/menu_openclaw/scripts/cmd.sh status
bash modules/menu_openclaw/scripts/cmd.sh list-menus
```

### Passe operateur OpenClaw

```bash
sudo -iu openclaw
cd /opt/trading
bash modules/install_module_openclaw/scripts/cmd.sh status
bash modules/openclaw_config_modulaire/scripts/cmd.sh status
bash modules/gateway_openclaw/scripts/cmd.sh status
bash modules/configure_openclaw/scripts/cmd.sh status
bash modules/doctor_openclaw/scripts/cmd.sh status
bash modules/evidence_openclaw/scripts/cmd.sh status
```

### Passe preuve

```bash
sudo -iu openclaw
cd /opt/trading
bash modules/gateway_openclaw/scripts/cmd.sh start
bash modules/doctor_openclaw/scripts/cmd.sh quick
bash modules/evidence_openclaw/scripts/cmd.sh export-docs
bash modules/evidence_openclaw/scripts/cmd.sh show-files
```

## Condition de close

Le GO devient relisible si :
- la chaine standard est ecrite dans un document unique ;
- `menu_openclaw` est reconnu comme hub de reprise ;
- l ordre logique des modules est explicite ;
- le point de reprise suivant peut s ouvrir sans reconstruire la chaine a la main.

## Hors perimetre

- pas de serving expose ;
- pas de cloud GPU actif ;
- pas de runtime large deduit du seul gateway loopback ;
- pas de migration des modules runtime dans le repo `openclaw`.

## Point de reprise suivant

Une fois ce GO fige cote documentation de chaine :
- soit ouvrir un patch utilitaire sur `menu_openclaw` si un raccourci manque reellement ;
- soit passer a `GO_OPENCLAW_PROVIDER_POLICY_04` si la chaine actuelle suffit pour la suite.
