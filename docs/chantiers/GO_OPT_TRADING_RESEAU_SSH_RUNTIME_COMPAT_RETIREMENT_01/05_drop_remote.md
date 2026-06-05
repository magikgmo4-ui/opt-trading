---
doc_id: GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01_DROP_REMOTE
doc_type: chantier_closeout
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01
status: open
lifecycle_stage: drop_remote_candidate
topic_keys:
  - opt-trading
  - reseau_ssh
  - isolation
  - drop-remote
  - closeout
surface: docs
source_kind: canonical
updated_at: 2026-04-22
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01/04_closeout_isolation.md
---

# GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01 - Drop remote candidate

## Contexte

La branche d'isolation `origin/codex/reseau-ssh-runtime-compat-retirement-01-isolate` a ete creee pour separer la publication du cadrage.

Cette branche a rempli son role : elle a permis de verifier le bornage et de publier le cadrage de facon isolee.

## Motif de suppression

La branche `origin/codex/reseau-ssh-runtime-compat-retirement-01-isolate` est maintenant :

- publiee (commit `8749e30`)
- non-fusionnee (jamais mergee dans `sot/mainline`)
- inutilisee apres isolation

Conclusion : `DROP_REMOTE_CANDIDATE`

## Commande de suppression

```bash
git push origin --delete codex/reseau-ssh-runtime-compat-retirement-01-isolate
```

## Verification post-suppression

Apres suppression, verifier que la branche n'apparait plus dans les refs distantes :

```bash
git ls-remote --refs origin codex/reseau-ssh-runtime-compat-retirement-01-isolate
```

Resultat attendu : vide (pas de sortie)

## Verdict final

`DROP_REMOTE_CANDIDATE`

La branche est candidate a suppression distante car :
- elle a ete publiee et verifiee
- elle n'a pas ete fusionnee dans `sot/mainline`
- elle ne fait plus partie du flux de travail actif

## RISKS

- À qualifier.
