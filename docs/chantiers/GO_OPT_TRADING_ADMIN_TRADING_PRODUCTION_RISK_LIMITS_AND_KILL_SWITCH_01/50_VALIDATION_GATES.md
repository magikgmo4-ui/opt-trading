# 50_VALIDATION_GATES

## Validation Gates Before Production

| Gate | Check | Pass | Fail |
|------|-------|------|------|
| G1 | Risk limits implemented | Proceed | BLOCKED |
| G2 | Kill switch tested | Proceed | BLOCKED |
| G3 | Rollback tested | Proceed | BLOCKED |
| G4 | TRADE_ALLOWED=false confirmed | Proceed | BLOCKED |
| G5 | No live orders in history | Proceed | BLOCKED |
| G6 | Secrets audited | Proceed | BLOCKED |
| G7 | Human approval | Proceed | BLOCKED |

## Gate Details

### G1: Risk Limits Implemented

```bash
# Verify limits in .env
ssh admin-trading "grep RISK_ /opt/trading/.env"
# Should show: RISK_MAX_NOTIONAL, RISK_MAX_POSITION_SIZE, etc.
```

### G2: Kill Switch Tested

```bash
# Test soft stop
ssh admin-trading "curl -X POST http://127.0.0.1:8000/api/kill-switch -d '{\"level\": 1}'"
# Verify: TRADE_ALLOWED=false in response

# Test service stop
ssh admin-trading "sudo systemctl stop tv-webhook.service"
# Verify: service inactive
```

### G3: Rollback Tested

```bash
# Execute rollback procedure
# Verify: paper mode, no live orders, positions manageable
```

### G4: TRADE_ALLOWED=false

```bash
ssh admin-trading "grep TRADE_ALLOWED /opt/trading/.env"
# Must show: TRADE_ALLOWED=false
```

### G5: No Live Orders

```bash
ssh admin-trading "grep -c LIVE /opt/trading/state/events.jsonl"
# Must show: 0
```

### G6: Secrets Audited

```bash
# Check .env for secrets
ssh admin-trading "cat /opt/trading/.env"
# Verify: no exposed keys

# Check git history
git log --all --diff-filter=D -- "*.env" "*.key" "*.pem"
# Should be empty
```

### G7: Human Approval

Document explicit human approval with:
- Approver name/ID
- Timestamp
- Scope approved
- Conditions/waivers

## Gate Status

| Gate | Status | Action |
|------|--------|--------|
| G1 | NOT CHECKED | Implement risk limits |
| G2 | NOT CHECKED | Implement kill switch |
| G3 | NOT CHECKED | Test rollback |
| G4 | NOT CHECKED | Verify TRADE_ALLOWED |
| G5 | NOT CHECKED | Audit events log |
| G6 | NOT CHECKED | Audit secrets |
| G7 | NOT CHECKED | Obtain approval |

## Decision

All gates must PASS before production GO. Current status: NOT CHECKED.
