# KIL V1

## Description
KIL V1 est un noyau minimal de campagne d'interrogation, comparaison, evaluation et capitalisation.

Le module respecte le cadrage canonique suivant :
- `Student Lab` = orchestrateur sequentiel
- `Memory Bricks` = memoire durable promue et source de verite finale
- `Journal` = continuite operatoire
- stockage V1 = `JSONL + SQLite + exports TXT/MD`

## Perimetre V1 livre
- topic -> framing audit -> question -> reponse -> evaluation -> comparaison eventuelle -> capitalisation -> journal -> export
- policies minimales de framing, evaluation et promotion
- promotion controlee `LAB / STANDARD / STRICT`
- tests minimaux contre les risques canoniques

## Hors scope
- LocalCMS
- UI / dashboard
- embeddings
- recherche semantique avancee
- multi-provider massif

## Arborescence utile
- `src/kil_v1/` : logique Python du noyau
- `tests/` : tests canoniques minimaux
- `examples/sample_campaign.json` : campagne d'exemple
- `cmd.sh` : entree CLI
- `sanity.sh` : smoke minimal du module

## CLI minimale
Depuis la racine du repo :

```bash
bash modules/kil_v1/cmd.sh run modules/kil_v1/examples/sample_campaign.json --workspace /tmp/kil_v1_demo
```

Autres commandes :

```bash
bash modules/kil_v1/cmd.sh audit /tmp/kil_v1_demo KIL-...
bash modules/kil_v1/cmd.sh sample --workspace /tmp/kil_v1_demo
bash modules/kil_v1/cmd.sh help
```

## Artefacts produits
- `jsonl/*.jsonl`
- `sqlite/kil_v1.db`
- `exports/<campaign_id>/*`

## Frontiere Memory Bricks
- KIL prend la decision de promotion et persiste le suivi de sync technique.
- Memory Bricks porte la creation reelle de la brique `MB-*` via CLI externe.
- Config minimale requise pour la sync reelle : variable d'environnement `KIL_V1_MEMORY_BRICKS_CMD` pointant vers une CLI compatible.
- En cas d'echec de sync, la decision de promotion KIL est conservee et le module renseigne `memory_sync_status=SYNC_FAILED` avec l'erreur.

## Gates portes par le module
- Gate 0 : cadre et policies presentes
- Gate 1 : question standardisee
- Gate 2 : capture et normalisation de reponse
- Gate 3 : evaluation explicite et traquee
- Gate 4 : promotion memoire controlee
