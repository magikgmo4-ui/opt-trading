---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_EXECUTION_01_50_ROLLBACK
doc_type: chantier/rollback
repo: opt-trading
machine: admin-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_EXECUTION_01
status: closed
scope: doc-only
checked_at: 2026-05-13
verdict: NO_RUNTIME_ROLLBACK_REQUIRED
---

# 50_ROLLBACK

## Etat

Aucun rollback runtime n'a ete applique.

Raison: aucun payload `PAPER_TEST` n'a ete envoye, aucun service n'a ete modifie, aucun fichier runtime n'a ete cree par ce GO.

## Rollback pret si un futur test paper cree un side effect

1. Arreter immediatement le processus de test si le payload est en cours.
2. Ne pas arreter les services live sans GO explicite separe.
3. Capturer:

```bash
cd /opt/trading
git status --short
systemctl is-active tv-webhook.service tv-bitget-runner.service ngrok-tv.service tv-perf.service
ls -l /opt/trading/state/ledger_live.json /opt/trading/state/ledger_paper.json /data/ledger_live.json /data/ledger_paper.json 2>/dev/null || true
journalctl --no-pager --since '15 minutes ago' -u tv-webhook.service -u tv-bitget-runner.service
```

4. Si un `ledger_live.json` apparait, classer l'incident en FAIL critique avant toute relance.
5. Si seul un artefact paper apparait et que le test est autorise, le conserver comme preuve, ne pas l'effacer sans decision de cleanup.
6. Si `state/positions.json` change a cause d'un test paper autorise, documenter le delta et restaurer depuis backup ou git uniquement si la position paper doit etre annulee.

## Rollback documentaire de cette PR

Cette PR est doc-only. Rollback Git:

```bash
git revert <commit-docs-paper-test-execution>
```

ou fermeture de la PR sans merge.

## RISKS

- À qualifier.
