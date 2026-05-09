# GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01 — Validated operating plan

Date: 2026-05-05
Branch: `go/GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01`
Machine: `admin-trading`
Status: `VALIDATED_FOR_ADMIN_TRADING_FOLLOWUP`

## 1_MASTER_TARGET

Document and follow the validated `admin-trading` operational plan from the machine-specific work split, without mixing this branch with `cursor-ai`, `db-layer`, `student`, or `fantome` work.

## 2_INITIAL_PROJECT_DOC

Reference document:

- `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md`

Rule retained:

- Use only the `admin-trading` block for this work.
- Do not redo global arbitration unless the requested branch is absent from the machine map.
- New branches must remain associated with a machine in the machine split document.

## 3_INITIAL_NEED

User validated the operational plan and requested that it be documented and followed on `admin-trading`.

## 4_MASTER_PROJECT_PLAN

The active plan is to use `admin-trading` as the runtime review surface for the trading system, starting with a read-only parent review before selecting any child runtime action.

Primary branch:

```text
GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01
```

## 5_GO_PLAN

### Parent GO

```text
GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01
```

Purpose:

- Establish the real current state of `admin-trading`.
- Map runtime services, ports, live surfaces, dependencies, and gaps.
- Decide the next child GO only from verified evidence.

### Candidate child surfaces after parent review

- Webhook / `tv-webhook` runtime review.
- Webhook signal diagnostics.
- TradingView alert external check.
- Bot Vision headless review / implementation / systemd / desk bridge smoke.
- Vision inbox repair.
- Desk Pro runtime review / smoke / desk bridge retry.
- Bridge guard review.

No child GO is selected until parent review evidence is recorded.

## 6_FINAL_TARGET

Deliver a documented, read-only, evidence-based `admin-trading` parent review that can safely determine the next runtime child GO.

Expected chantier structure:

```text
docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01/
  00_START.md
  05_VALIDATED_OPERATING_PLAN.md
  10_MACHINE_STATE.md
  20_RUNTIME_SERVICES_AND_PORTS.md
  30_TRADING_SURFACE_MAP.md
  40_DEPENDENCIES_AND_GAPS.md
  50_NEXT_GO_DECISION.md
  90_CLOSEOUT.md
```

## 7_CANONICAL_STATE

Established at plan validation:

- The admin-trading branch already exists.
- The chantier has an existing `00_START.md`.
- The chantier has an existing inbox index entry.
- The validated next operating step is parent review, not child execution.

## 8_VALIDATED_PLAN

1. Work only on:

```text
go/GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01
```

2. On `admin-trading`, start with real-state verification:

```bash
set -Eeuo pipefail
trap 'echo "ERROR line $LINENO: $BASH_COMMAND" >&2' ERR
cd /opt/trading
git status --short --branch
git remote -v
git branch --show-current
git log --oneline -5
```

3. Confirm or checkout the expected branch:

```bash
set -Eeuo pipefail
trap 'echo "ERROR line $LINENO: $BASH_COMMAND" >&2' ERR
cd /opt/trading
git fetch origin
if git show-ref --verify --quiet refs/heads/go/GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01; then
  git checkout go/GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01
else
  git checkout -b go/GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01 origin/go/GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01
fi
git status --short --branch
```

4. Run read-only machine inventory. Suggested commands:

```bash
set -Eeuo pipefail
trap 'echo "ERROR line $LINENO: $BASH_COMMAND" >&2' ERR
cd /opt/trading
{
  echo "# MACHINE"
  hostnamectl || true
  echo
  echo "# GIT"
  git status --short --branch
  git log --oneline -8
  echo
  echo "# SYSTEMD TRADING SERVICES"
  systemctl list-units --type=service --all | grep -Ei 'trading|webhook|vision|desk|telegram|bot|uvicorn|collector|coinglass|tv' || true
  echo
  echo "# LISTENING PORTS"
  ss -ltnp || true
  echo
  echo "# TOP-LEVEL MODULES"
  find modules -maxdepth 2 -type f \( -name 'cmd.sh' -o -name 'menu.sh' -o -name 'sanity*.sh' -o -name '*.service' \) | sort || true
} | tee docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01/10_MACHINE_STATE.md
```

5. Map runtime surfaces without secrets:

```bash
set -Eeuo pipefail
trap 'echo "ERROR line $LINENO: $BASH_COMMAND" >&2' ERR
cd /opt/trading
{
  echo "# Runtime surface map"
  echo
  echo "## Bot vision / Telegram / ShareX"
  find modules desk scripts -maxdepth 4 -type f 2>/dev/null | grep -Ei 'vision|telegram|sharex|snapshot|inbox' | sort || true
  echo
  echo "## Webhook / TradingView"
  find . -maxdepth 4 -type f 2>/dev/null | grep -Ei 'webhook|tradingview|tv-|alert' | sort || true
  echo
  echo "## Desk / Desk Pro / Bridge"
  find modules desk -maxdepth 4 -type f 2>/dev/null | grep -Ei 'desk|bridge|analyze' | sort || true
  echo
  echo "## Collectors / Risk / Probability / Derivatives"
  find modules -maxdepth 4 -type f 2>/dev/null | grep -Ei 'collector|risk|probability|derivatives' | sort || true
} | tee docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01/30_TRADING_SURFACE_MAP.md
```

6. Record next GO decision only after evidence exists.

## 9_SELECTED_SOLUTION

Selected approach: read-only parent review first, child GO second.

No runtime mutation is authorized during the parent review.

## 10_SELECTED_SETUP

Machine setup:

- Host: `admin-trading`
- Repo root expected: `/opt/trading`
- Canonical base branch: `sot/mainline`
- Working branch: `go/GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01`

## 11_KEY_DECISIONS

- The plan is validated.
- The branch is already assigned to `admin-trading`.
- The parent review must precede any child GO.
- Evidence from the real machine state has priority over memory and branch names.

## 12_INVARIANTS

Do not do any of the following during parent review:

- Do not start, stop, restart, reload, or enable services.
- Do not trigger a real webhook.
- Do not send Telegram messages.
- Do not reveal or print secrets.
- Do not `cat .env` or display tokens.
- Do not place live JSON runtime data under git tracking.
- Do not mix `cursor-ai`, `db-layer`, `student`, or `fantome` changes in this branch.
- Do not open an OpenClaw integration on `admin-trading` from this GO.

## 13_ESTABLISHED

- `GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01` is the active admin-trading parent review branch.
- Existing start/index traces are present before this validated operating plan file.
- The next operational action is read-only verification from `/opt/trading` on `admin-trading`.

## 14_HYPOTHESIS

To validate from the real machine state:

- Which `tv-webhook` service is active, if any.
- Which bot vision service is active, if any.
- Which Desk Pro or desk bridge surfaces are active.
- Which ports are actually listening.
- Which runtime artifacts are generated locally and must stay untracked.

## 15_REMAINING_GAP

Missing until the machine audit is performed:

- Real service inventory.
- Real port inventory.
- Real module/sanity inventory.
- Real runtime surface map.
- Final child GO decision.

## 16_TODO

1. Run the read-only verification commands from `admin-trading`.
2. Fill `10_MACHINE_STATE.md`.
3. Fill `20_RUNTIME_SERVICES_AND_PORTS.md`.
4. Fill `30_TRADING_SURFACE_MAP.md`.
5. Fill `40_DEPENDENCIES_AND_GAPS.md`.
6. Decide the next child GO in `50_NEXT_GO_DECISION.md`.
7. Close parent review in `90_CLOSEOUT.md` with PASS/FAIL.

## 17_RESUME_POINT

Resume from:

```text
GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01
```

Operational restart:

```bash
cd /opt/trading
git fetch origin
git checkout go/GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01
git status --short --branch
```

Then continue by filling the next missing file in:

```text
docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01/
```

## 18_TO_DOCUMENT

Canonical documentation blocks to preserve:

- `7_CANONICAL_STATE`
- `8_VALIDATED_PLAN`
- `12_INVARIANTS`
- `16_TODO`
- `17_RESUME_POINT`

## 19_TO_REMEMBER

Memory Bricks candidate, project-level only:

- `admin-trading` parent review must start read-only from `/opt/trading` on branch `go/GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01`.
- Child GO selection must come after real service/port/runtime surface evidence, not before.
