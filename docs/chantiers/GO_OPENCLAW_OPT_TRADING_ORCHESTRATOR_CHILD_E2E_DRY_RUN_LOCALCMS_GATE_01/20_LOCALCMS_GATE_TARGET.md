---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_DRY_RUN_LOCALCMS_GATE_01_GATE_TARGET
doc_type: design_target
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_DRY_RUN_LOCALCMS_GATE_01
updated_at: 2026-05-26
---

# 20_LOCALCMS_GATE_TARGET

## Décisions de conception

### Fix 1 — Dispatcher import gracieux

```python
# main() — avant step 1
class _NoOpDispatcher:
    def dispatch(self, *_, **__):
        return {"ok": False, "skipped": "dispatcher_unavailable"}

try:
    from modules.notification_dispatcher.app.dispatcher import NotificationDispatcher
    from modules.notification_dispatcher.app.events import PipelineEvent
    dispatcher = NotificationDispatcher()
except ImportError:
    dispatcher = _NoOpDispatcher()
    class PipelineEvent: ...  # fallback minimal
```

Plus de crash si `requests` absent. Dispatch retourne `{"skipped": "dispatcher_unavailable"}`.

### Fix 2 — Gate LocalCMS structurée

```python
@dataclass
class E2ELocalCMSGateResult:
    status: str   # PASS | WARN_SKIPPED | BLOCKED
    reason: str
    url: str
    mode: str     # default | require | skip

def check_localcms_available(url, timeout=2.0) -> tuple[bool, str]: ...
def classify_localcms_gate(require, skip, url) -> E2ELocalCMSGateResult: ...
```

### Fix 3 — Exit code

```python
all_ok = report.get("all_ok", False)
gate_blocked = report.get("localcms_gate", {}).get("status") == "BLOCKED"
sys.exit(0 if (all_ok and not gate_blocked) else 1)
```

Seul BLOCKED affecte le rc. WARN_SKIPPED → rc=0.

### Backward compat

Les clés `localcms` et `localcms_ok` sont conservées dans le rapport pour les tests existants.

## Variables d'environnement

| Var | Valeur | Effet |
|-----|--------|-------|
| `REQUIRE_LOCALCMS_E2E` | `1` | gate = BLOCKED si absent, rc=1 |
| `SKIP_LOCALCMS_E2E` | `1` | gate = WARN_SKIPPED sans probe, rc=0 |
| `LOCALCMS_URL` | `http://...` | URL custom (défaut 127.0.0.1:8700) |

## Rapport gate

```json
{
  "localcms_gate": {
    "status": "WARN_SKIPPED",
    "reason": "LocalCMS not reachable (optional in default mode): ...",
    "url": "http://127.0.0.1:8700",
    "mode": "default"
  },
  "e2e_status": "PASS"
}
```
