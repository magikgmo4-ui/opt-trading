from __future__ import annotations
import logging
import os
from typing import Optional

def setup_logger(name: str = "trading", level: Optional[str] = None) -> logging.Logger:
    """
    Central logger with env-controlled level.
    LOG_LEVEL default: INFO
    """
    if level is None:
        level = os.environ.get("LOG_LEVEL", "INFO")

    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # already configured

    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    h = logging.StreamHandler()
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    h.setFormatter(fmt)
    logger.addHandler(h)
    logger.propagate = False
    return logger
