#!/usr/bin/env python3
"""BTC COIN-M parameter sweep config generator."""
from __future__ import annotations

import hashlib
import json
import math
import random
from typing import Any


# ── sampling utilities ────────────────────────────────────────────────────

def _log_uniform(rng: random.Random, lo: float, hi: float) -> float:
    if lo <= 0:
        lo = 0.00000001
    return math.exp(rng.uniform(math.log(lo), math.log(hi)))


def _sample_dirichlet(rng: random.Random, n: int = 3) -> list[float]:
    xs = [rng.gammavariate(1.0, 1.0) for _ in range(n)]
    total = sum(xs)
    return [x / total for x in xs]


# ── tp simplex special cases ──────────────────────────────────────────────

_TP_EDGE_CASES = [
    (1.0, 0.0, 0.0),
    (0.0, 1.0, 0.0),
    (0.0, 0.0, 1.0),
    (0.5, 0.5, 0.0),
    (0.5, 0.0, 0.5),
    (0.0, 0.5, 0.5),
]


def sample_tp_triad(rng: random.Random) -> tuple[float, float, float]:
    if rng.random() < 0.20:
        return rng.choice(_TP_EDGE_CASES)
    a, b, c = _sample_dirichlet(rng, 3)
    return (round(a, 6), round(b, 6), round(1.0 - a - b, 6))


# ── single config generator ───────────────────────────────────────────────

def generate_one_config(rng: random.Random) -> dict[str, Any]:
    tp1, tp2, runner = sample_tp_triad(rng)

    q_add_raw = _log_uniform(rng, 0.00001, 500.0)
    q_add_native = max(0.0001, round(q_add_raw / 0.0001) * 0.0001)

    return {
        "z_dca": round(_log_uniform(rng, 0.0001, 0.20), 6),
        "z_short": round(_log_uniform(rng, 0.0001, 0.30), 6),
        "g_up": round(_log_uniform(rng, 0.0001, 0.30), 6),
        "g_down": round(_log_uniform(rng, 0.0001, 0.30), 6),
        "r_transfer": round(rng.uniform(0.0, 5.0), 4),
        "y_dca_usdt": round(_log_uniform(rng, 1.0, 100000.0), 2),
        "q_add_native": q_add_native,
        "leverage_target": round(_log_uniform(rng, 0.1, 200.0), 2),
        "tp1": tp1,
        "tp2": tp2,
        "runner": runner,
        "cooldown_dca_h": rng.randint(0, 336),
        "cooldown_short_h": rng.randint(0, 336),
        "D_min": round(rng.uniform(0.0, 1.5), 4),
        "MR_max": round(rng.uniform(0.0, 5.0), 4),
        "Q_max_native": round(_log_uniform(rng, 0.00001, 500.0), 8),
        "U_floor_usdt": round(_log_uniform(rng, 0.01, 100000.0), 2) if rng.random() < 0.9 else 0.0,
        "M_floor_btc": round(_log_uniform(rng, 0.00001, 10.0), 8) if rng.random() < 0.9 else 0.0,
        "funding_limit": round(rng.uniform(0.0, 5.0), 8),
        "fee_limit": round(rng.uniform(0.0, 5.0), 8),
        "slippage_max_bps": round(rng.uniform(0.0, 5000.0), 1),
        "weekly_structure_gate_mode": "off",
        "weekly_k": rng.randint(1, 12),
        "weekly_epsilon_lambda": round(rng.uniform(0.0, 0.10), 4),
        "max_pivot_gap_weeks": rng.randint(1, 52),
    }


# ── batch generator ───────────────────────────────────────────────────────

def generate_configs(space: dict[str, Any] | None = None,
                     count: int = 100,
                     method: str = "random",
                     seed: int = 0) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    configs: list[dict[str, Any]] = []
    for _ in range(count):
        cfg = generate_one_config(rng)
        cfg["_seed"] = seed
        cfg["_generator_method"] = method
        cfg["_generator_stage"] = space.get("stage", "") if space else ""
        configs.append(cfg)
    return configs


def serialize_config(config: dict[str, Any]) -> str:
    keys = sorted(k for k in config if not k.startswith("_"))
    obj = {k: config[k] for k in keys}
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, default=str)


def config_hash(config: dict[str, Any]) -> str:
    raw = serialize_config(config)
    return hashlib.sha256(raw.encode()).hexdigest()[:16]
