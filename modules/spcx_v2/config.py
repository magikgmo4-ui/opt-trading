"""SPCX V2 — Centralized configuration and setup catalog."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# --- Paths ---
MODULE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = MODULE_DIR.parent.parent
OUTPUT_DIR = PROJECT_ROOT / "data" / "ipo" / "spacex" / "paper_log"
REJECTS_FILE = "rejects.jsonl"
CANDIDATES_FILE = "candidates.jsonl"
RESULTS_FILE = "results.jsonl"
SUMMARY_FILE = "summary.json"

# --- Gate thresholds ---
GATE_0_THRESHOLDS = {
    "min_bars_count": 1,
    "min_volume": 1,
    "min_price_trust": 1,
    "min_source_count": 1,
}

GATE_1_THRESHOLDS = {
    "max_spread_pct": 2.0,
    "min_dollar_volume": 500000,
}

GATE_3_THRESHOLDS = {
    "trade_ready_A_plus": 75,
    "trade_ready_A": 60,
    "trade_ready_B": 40,
    "liquidity_A": 65,
    "liquidity_B": 40,
    "risk_max_for_trade": 60,
    "smart_money_A": 60,
    "catalyst_A": 55,
}

# --- Setup catalog ---
# Each setup has: id, category, timeframe, logic (english description)
SETUP_CATALOG = [
    {"id": "FIRST_PRINT_OBSERVATION", "category": "ipo", "timeframes": ["1m"], "priority": "P0"},
    {"id": "IPO_ORB_5M", "category": "ipo", "timeframes": ["1m", "5m"], "priority": "P0"},
    {"id": "IPO_ORB_15M", "category": "ipo", "timeframes": ["1m", "5m", "15m"], "priority": "P0"},
    {"id": "IPO_ORB_30M", "category": "ipo", "timeframes": ["5m", "15m", "30m"], "priority": "P1"},
    {"id": "IPO_PRICE_RECLAIM", "category": "ipo", "timeframes": ["1m", "5m"], "priority": "P0"},
    {"id": "IPO_PRICE_LOSS", "category": "ipo", "timeframes": ["5m", "15m"], "priority": "P0"},
    {"id": "GAP_AND_GO", "category": "ipo", "timeframes": ["5m", "15m"], "priority": "P1"},
    {"id": "FAILED_BREAKOUT_TRAP", "category": "ipo", "timeframes": ["5m", "15m"], "priority": "P1"},
    {"id": "VWAP_HOLD_LONG", "category": "vwap", "timeframes": ["5m", "15m"], "priority": None},
    {"id": "VWAP_RECLAIM", "category": "vwap", "timeframes": ["1m", "5m"], "priority": None},
    {"id": "VWAP_REJECT", "category": "vwap", "timeframes": ["1m", "5m"], "priority": None},
    {"id": "VWAP_DISTANCE_EXTREME", "category": "vwap", "timeframes": ["5m", "15m"], "priority": None},
    {"id": "FVG_BULLISH_RECLAIM", "category": "smc", "timeframes": ["5m", "15m"], "priority": None},
    {"id": "FVG_BEARISH_REJECT", "category": "smc", "timeframes": ["5m", "15m"], "priority": None},
    {"id": "BOS_CONTINUATION", "category": "smc", "timeframes": ["5m", "15m"], "priority": None},
    {"id": "CHOCH_REVERSAL", "category": "smc", "timeframes": ["5m", "15m"], "priority": None},
    {"id": "LIQUIDITY_SWEEP_LOW_RECLAIM", "category": "smc", "timeframes": ["1m", "5m"], "priority": None},
    {"id": "LIQUIDITY_SWEEP_HIGH_REJECT", "category": "smc", "timeframes": ["1m", "5m"], "priority": None},
    {"id": "ORDER_BLOCK_RETEST", "category": "smc", "timeframes": ["5m", "15m"], "priority": None},
    {"id": "RELATIVE_VOLUME_BREAKOUT", "category": "momentum", "timeframes": ["5m"], "priority": None},
    {"id": "VOLUME_ACCELERATION", "category": "momentum", "timeframes": ["1m", "5m"], "priority": None},
    {"id": "HIGH_VOLUME_PULLBACK", "category": "momentum", "timeframes": ["5m"], "priority": None},
    {"id": "LOW_VOLUME_FADE", "category": "momentum", "timeframes": ["5m"], "priority": None},
    {"id": "DOLLAR_VOLUME_FILTER", "category": "momentum", "timeframes": ["5m"], "priority": None},
    {"id": "NEWS_CATALYST_BREAKOUT", "category": "news", "timeframes": ["5m", "15m"], "priority": None},
    {"id": "SEC_FILING_REACTION", "category": "news", "timeframes": ["15m", "30m"], "priority": None},
    {"id": "CONTRACT_NEWS_REACTION", "category": "news", "timeframes": ["5m", "15m"], "priority": None},
    {"id": "NEGATIVE_HEADLINE_RISK_OFF", "category": "news", "timeframes": ["5m", "15m"], "priority": None},
    {"id": "NEWS_SPIKE_FADE", "category": "news", "timeframes": ["1m", "5m"], "priority": None},
    {"id": "BUY_ZONE", "category": "accumulation", "timeframes": ["1d"], "priority": None},
    {"id": "ACCUMULATE_ZONE", "category": "accumulation", "timeframes": ["1d"], "priority": None},
    {"id": "WAIT_ZONE", "category": "accumulation", "timeframes": ["1d"], "priority": None},
    {"id": "DANGER_ZONE", "category": "accumulation", "timeframes": ["1d"], "priority": None},
]

SETUP_IDS = {s["id"] for s in SETUP_CATALOG}
SETUPS_BY_CATEGORY = {}
for s in SETUP_CATALOG:
    SETUPS_BY_CATEGORY.setdefault(s["category"], []).append(s["id"])


# --- Data structures ---
@dataclass
class MarketSnapshot:
    symbol: str
    timestamp: str
    price: float
    price_status: str           # "live" | "delayed" | "stale" | "missing"
    bars_count: int
    volume: int
    price_trust: int            # 0-100
    source_count: int
    spread_pct: float
    dollar_volume: float
    vwap: Optional[float] = None
    halt_active: bool = False
    nasdaq_contradiction: bool = False
    yahoo_contradiction: bool = False
    news_headline: Optional[str] = None
    news_sentiment: Optional[str] = None
    smc_structures: list = field(default_factory=list)
    orderflow_score: Optional[float] = None
    ownership_pressure_score: Optional[float] = None
    orderflow_source: Optional[str] = None
    large_prints_count: int = 0


@dataclass
class GateResult:
    gate_name: str
    passed: bool
    reason_codes: list = field(default_factory=list)
    details: dict = field(default_factory=dict)


@dataclass
class SetupMatch:
    setup_id: str
    category: str
    confidence: int       # 0-100
    trigger_event: str    # e.g. "break above ORB high"


@dataclass
class ScoreSet:
    trade_ready: int = 0
    liquidity: int = 0
    risk: int = 0
    smart_money: int = 0
    catalyst: int = 0


@dataclass
class SetupCandidate:
    symbol: str
    ts: str
    setup_type: str
    grade: str                 # "A+" | "A" | "B" | "reject"
    status: str                # "paper_only"
    gates: dict = field(default_factory=dict)
    scores: ScoreSet = field(default_factory=ScoreSet)
    entry_zone: str = ""
    invalidation: str = ""
    tp_logic: list = field(default_factory=list)
    reason_codes: list = field(default_factory=list)
    candidate_id: Optional[str] = None
    entry_price: Optional[float] = None
    stop_loss: Optional[float] = None
    tp1: Optional[float] = None
    tp2: Optional[float] = None
    risk_r: Optional[float] = None
    result_15m: Optional[dict] = None
    result_30m: Optional[dict] = None
    result_1h: Optional[dict] = None
    result_eod: Optional[dict] = None
    mfe: Optional[float] = None
    mae: Optional[float] = None
    r_multiple: Optional[float] = None
    hit_tp1: bool = False
    hit_tp2: bool = False
    hit_sl: bool = False
