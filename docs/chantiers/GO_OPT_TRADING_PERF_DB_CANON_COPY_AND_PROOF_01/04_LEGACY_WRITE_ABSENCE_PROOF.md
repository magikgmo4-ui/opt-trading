---
doc_id: GO_OPT_TRADING_PERF_DB_CANON_COPY_AND_PROOF_01_LEGACY_WRITE_ABSENCE_PROOF
doc_type: proof_report
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_DB_CANON_COPY_AND_PROOF_01
status: final
lifecycle_stage: closeout
parent_go_id: GO_OPT_TRADING_PERF_RUNTIME_DEPLOY_SYNC_IMPL_01
topic_keys:
  - opt-trading
  - perf
  - legacy
  - proof
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_COPY_AND_PROOF_01/04_LEGACY_WRITE_ABSENCE_PROOF.md
point_de_reprise: "Prouver G4: absence d'écritures résiduelles sur perf/perf.db."
updated_at: 2026-05-11
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_COPY_AND_PROOF_01/00_CADRAGE.md
---

# 04_LEGACY_WRITE_ABSENCE_PROOF

## G4 — État des écritures sur `perf/perf.db`

Preuves collectées sur `/opt/trading` :

```text
legacy DB présente, mtime = 2026-04-09 11:55:46 -0400
pas de processus PERF actif pendant la collecte
pas de listener :8010 pendant la collecte

le résolveur de launchers préfère maintenant la DB canonique
```
**MAIS** :

```text
La preuve définitive de G4 exigerait :
- une observation runtime continue
- ou le retrait effectif de la DB legacy
- ou un flag de bascule stricte sans fallback

Aucune de ces trois options n'est dans le scope de ce GO.
Le legacy est conservé comme safety net.
```

Verdict G4 :

```text
PARTIAL
```

Lecture correcte :

```text
Le code et le chemin canoniques sont prêts.
Le legacy reste accessible comme fallback automatique, ce qui le protège
contre les régressions mais empêche la preuve formelle de G4.
```
