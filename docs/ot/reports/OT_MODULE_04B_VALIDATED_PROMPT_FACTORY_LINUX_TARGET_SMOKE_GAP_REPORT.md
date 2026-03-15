# OT-MODULE-04B — VALIDATED_PROMPT_FACTORY (LINUX TARGET SMOKE) — GAP REPORT

Date (America/Montreal) : 2026-03-14

## ÉTABLI
- Smoke prouvé sur Linux réel (`admin-trading`) : `cmd.sh` et `sanity.sh` OK.

## ÉCARTS PROUVÉS (ET STATUT)

### GAP-01 — Inputs standard absents sur la cible Linux
- **Constat** : `inputs/synthesis_registry_central.txt`, `inputs/synthesis_bundle_transfer.txt`, `inputs/synthesis_failure_missing_section.txt` absents sur `/opt/trading/.../inputs/`.
- **Impact** : smoke “nominal” impossible sans ces inputs.
- **Statut** : contourné pour smoke en copiant les fichiers exacts (aucun contenu inventé).

### GAP-02 — CRLF sur scripts `.sh` après transfert
- **Constat** : exécution `./sanity.sh` → `/usr/bin/env: « bash\r »`.
- **Impact** : wrappers inopérants sur Linux si `.sh` en CRLF.
- **Statut** : corrigé (normalisation LF côté repo ; recommandation `.gitattributes`).

## À CONFIRMER
- `menu.sh` : interactif, à tester manuellement côté opérateur.
- Wrappers globaux `/usr/local/bin` (`cmd-validated_prompt_factory`, `sanity-validated_prompt_factory`, `menu-validated_prompt_factory`) : non testés ici.

