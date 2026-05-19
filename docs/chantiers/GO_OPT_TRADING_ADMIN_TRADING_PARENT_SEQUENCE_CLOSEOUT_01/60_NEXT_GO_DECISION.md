---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_SEQUENCE_CLOSEOUT_01_NEXT_GO_DECISION
doc_type: next_go_decision
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_SEQUENCE_CLOSEOUT_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-06
---

# 60_NEXT_GO_DECISION - Next GO Decision

## Contexte

La séquence admin-trading producer/consumer est complète (8/8 PASS). Les contrats sont validés. L'adapter est implémenté. Le smoke est passé. La décision porte sur la prochaine étape.

## Options

### Option 1: PR Merge (RECOMMANDÉ)

```
GO_OPT_TRADING_ADMIN_TRADING_SEQUENCE_PR_MERGE_01
```

**But**: Canoniser toute la séquence vers `sot/mainline` via PR.

**Raison**: Les 8 branches sont publiées et validées. Le merge vers mainline stabilise le travail et permet aux autres chantiers de bénéficier des contrats et de l'adapter.

**Prérequis**: Aucun — tous les invariants sont respectés.

### Option 2: Desk Pro Automation Plan

```
GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_PLAN_01
```

**But**: Planifier l'automatisation de Desk Pro après preuve contractuelle.

**Raison**: Desk Pro est manuel. L'automation nécessite un plan séparé.

**Prérequis**: Merge de la séquence vers mainline.

### Option 3: Playwright Setup

```
GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_HEADLESS_PLAYWRIGHT_SETUP_01
```

**But**: Restaurer le pipeline headless pour capturer les 4 symboles nativement.

**Raison**: Playwright est absent, headless_capture failed à chaque trigger. Le fallback ShareX fonctionne mais ne capture qu'un layout 2x2.

**Prérequis**: Aucun.

### Option 4: Live Runtime Smoke

```
GO_OPT_TRADING_ADMIN_TRADING_LIVE_RUNTIME_SMOKE_GATED_01
```

**But**: Smoke runtime réel avec garde explicite (webhook + capture + Desk Pro).

**Raison**: Le smoke contractuel est local. Un smoke runtime réel valide l'intégration end-to-end.

**Prérequis**: Merge de la séquence vers mainline.

## Recommandation

1. **`GO_OPT_TRADING_ADMIN_TRADING_SEQUENCE_PR_MERGE_01`** en premier — canoniser la séquence
2. Puis choisir entre automation, Playwright, ou live smoke selon les priorités opérationnelles
