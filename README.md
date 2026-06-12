# SpaceX Super Desk V2 Bundle

Implémentation sérieuse et monitor-only pour `GO_SPACEX_SUPER_DESK_PARENT_01`.

## Ce bundle ajoute

- Config complète `configs/ipo/spacex_super_desk.yaml`.
- Profil Bot Vision SpaceX.
- Schéma d'alerte TradingView.
- Package Python `modules/ipo_tracking`.
- Collecteurs publics/fallback : Yahoo chart, SEC EDGAR, Yahoo RSS.
- Scoring : momentum, news velocity, risk, trade ready, accumulation.
- Data Center view : `data/data_center/views/spacex_super_desk/latest.json`.
- Scripts : collect once, watch loop, report daily, smoke.
- UI statique : `ui/spacex_desk/index.html` générée au run.
- Documentation chantier + source inventory.

## Application par bundle

```bash
cd /opt/trading
git checkout sot/mainline
git pull --rebase
git checkout -b go/spacex-super-desk-v2
unzip /path/to/spacex_super_desk_v2_bundle.zip -d /tmp/spacex_v2
rsync -a /tmp/spacex_v2/spacex_super_desk_v2_bundle/ ./
bash scripts/ipo/spacex_smoke.sh
```

## Application par patch

```bash
cd /opt/trading
git checkout sot/mainline
git pull --rebase
git checkout -b go/spacex-super-desk-v2
git apply /path/to/GO_SPACEX_SUPER_DESK_V2_IMPL.patch
bash scripts/ipo/spacex_smoke.sh
```

## Commit

```bash
git add docs configs schemas modules scripts ui tradingview RUNBOOK_SPACEX_SUPER_DESK_V2.md
git commit -m "feat: add SpaceX super desk v2 implementation"
git push -u origin go/spacex-super-desk-v2
```

Monitor-only. Aucun ordre réel.
