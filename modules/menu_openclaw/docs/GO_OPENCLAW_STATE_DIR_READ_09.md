# GO_OPENCLAW_STATE_DIR_READ_09

## Classification

diagnostic ponctuel
lecture-only
machine-sourcé

## Objectif

Lire et qualifier l état réel OpenClaw sur db-layer, sans rien modifier.

## Questions à trancher

1. Quel est le state dir réellement actif maintenant ?
2. Quelle est la config réellement active maintenant ?
3. Quels logs sont réellement actifs maintenant ?
4. Quel est l état réel de doctor / gateway / dashboard ?
5. Le double state dir crée-t-il un écart réel, un risque neutre, ou un blocage ?
6. L état réel respecte-t-il déjà la baseline visée, ou non ?

## Contraintes strictes

- ne rien modifier
- ne lancer aucun repair
- ne lancer aucun set / unset / wizard / fix
- ne pas corriger le state dir
- ne pas muter la policy
- ne pas exposer la gateway
- ne pas ouvrir de patch dans ce GO
- lire uniquement les faits réellement observés

## Interdits explicites

- GO_OPENCLAW_STATE_DIR_REPAIR_10
- GO_OPENCLAW_ALIGNMENT_RUNTIME_PATCH_11
- GO_OPENCLAW_POLICY_V2_12

tant que READ_09 n est pas fermé

## Séquence opératoire exacte

Bloc 1
```bash
sudo -iu openclaw
cd /opt/trading
CFG="$(bash modules/configure_openclaw/scripts/cmd.sh config-file)"
echo "$CFG"
bash modules/configure_openclaw/scripts/cmd.sh validate
bash modules/configure_openclaw/scripts/cmd.sh agents-list
bash modules/doctor_openclaw/scripts/cmd.sh status
bash modules/doctor_openclaw/scripts/cmd.sh logs
bash modules/gateway_openclaw/scripts/cmd.sh status
```

Bloc 2
```bash
sudo -iu openclaw
cd /opt/trading
bash modules/evidence_openclaw/scripts/cmd.sh status
bash modules/evidence_openclaw/scripts/cmd.sh detect-workspace
bash modules/evidence_openclaw/scripts/cmd.sh export-docs
bash modules/evidence_openclaw/scripts/cmd.sh show-files
```

Critères de close

Le GO est clos quand :

- les 6 questions de diagnostic ont une réponse factuelle
- l état réel est documenté sans interprétation
- l impact du double state dir est qualifié
- la conformité ou non à la baseline est établie

## Types de verdict possibles

- NO-OP
- REPAIR LOCAL
- PATCH RUNTIME
- PATCH POLICY

## Point de reprise suivant

Selon verdict :

- NO-OP → GO_OPENCLAW_USAGE_EXAMPLES_09
- REPAIR LOCAL → GO_OPENCLAW_STATE_DIR_REPAIR_10
- PATCH RUNTIME → GO_OPENCLAW_ALIGNMENT_RUNTIME_PATCH_11
- PATCH POLICY → GO_OPENCLAW_POLICY_V2_12