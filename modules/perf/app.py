"""Canonical compatibility entrypoint for the PERF FastAPI app.

This shim exposes `modules.perf.app:app` while preserving the historical
runtime path `perf.perf_app:app`.
"""

from perf.perf_app import *  # noqa: F401,F403
from perf.perf_app import app  # noqa: F401
