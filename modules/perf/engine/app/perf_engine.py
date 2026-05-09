"""Compatibility wrapper around the historical PERF engine entrypoint.

This keeps the old module path working while exposing a canonical family path:
`modules.perf.engine.app.perf_engine`.
"""

from modules.perf_engine.app.perf_engine import *  # noqa: F401,F403
from modules.perf_engine.app.perf_engine import main  # noqa: F401


if __name__ == "__main__":
    main()
