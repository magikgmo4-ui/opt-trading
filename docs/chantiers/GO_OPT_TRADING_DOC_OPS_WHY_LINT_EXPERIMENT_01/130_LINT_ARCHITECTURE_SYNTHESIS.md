# 130_LINT_ARCHITECTURE_SYNTHESIS

## Objectif

Synthetiser l'architecture du WHY lint experimental.

## Synthese

Le chantier definit un lint WHY:
- non destructif,
- warning-only,
- lecture seule,
- audit-oriented,
- explicable,
- compatible governance runtime,
- compatible worker WHY futur,
- compatible CI experimentale non bloquante.

## Architecture retenue

| Couche | Role |
| --- | --- |
| lint scope | definir le perimetre |
| warning levels | definir severites warning-only |
| document targets | cibler surfaces documentaires |
| gap detection | detecter manques WHY |
| runtime governance rules | verifier coherence runtime/governance |
| human review rules | preserver review humaine |
| observability rules | verifier preuves runtime |
| runtime class alignment | relier R0-R5 |
| autonomy limits | limiter derive autonome |
| reporting architecture | preparer sorties audit |
| CI experiment preparation | cadrer CI non bloquante |
| worker integration roadmap | preparer integration worker WHY |

## Resultat structurel

Le repo dispose maintenant d'un cadrage lint WHY capable de:
- signaler des gaps documentaires,
- exposer des warnings,
- verifier la coherence runtime/governance,
- preparer une CI governance experimentale,
- alimenter un futur worker WHY reel.

## Invariant final

Le WHY lint doit rester lecture seule, warning-only, non destructif, sans validation runtime autonome et sans remplacement de review humaine.
