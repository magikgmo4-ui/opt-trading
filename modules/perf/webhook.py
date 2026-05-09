"""Canonical compatibility entrypoint for webhook -> perf mapping.

This shim keeps the historical adapter path valid while exposing the family
surface under `modules.perf.webhook`.
"""

from adapters.webhook_to_perf import *  # noqa: F401,F403
