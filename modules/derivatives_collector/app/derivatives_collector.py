#!/usr/bin/env python3
"""
Derivatives Collector Module
Collects and normalizes derivatives data (OI, Funding, Liquidations) from various sources.

Usage:
    python -m modules.derivatives_collector.app.derivatives_collector [command] [args]

Commands:
    collect     Run collection and output data.
    status      Show module status and config.
    sample      Run a sample collection (mock).
    export      Export mock data to file.
"""
import sys
import logging
import os
import json
from dataclasses import dataclass, asdict
from typing import Optional
import csv
import argparse
import random
import time
import urllib.request
import urllib.error
import concurrent.futures
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)

# --- Retryable Error Classification ---
RETRYABLE_ERROR_PATTERNS = (
    "timeout",
    "timed out",
    "rate limit",
    "429",
    "network",
    "temporary",
    "temporarily",
    "connection reset",
    "connection refused",
    "dns",
)

NON_RETRYABLE_ERROR_PATTERNS = (
    "invalid return type",
    "internal error",
    "not retryable",
    "corruption",
    "mapping",
    "structure",
)

def is_retryable_error(error_msg):
    """Classify whether an error is transient/retryable.
    
    Returns True only for clearly transient errors:
    - timeout, temporary network errors, rate limits (429)
    
    Excludes non-transient errors:
    - invalid return type, internal mapping bugs, structural errors
    """
    if error_msg is None:
        return False
    error_lower = error_msg.lower()
    # Explicit non-retryable takes precedence
    if any(pat in error_lower for pat in NON_RETRYABLE_ERROR_PATTERNS):
        return False
    return any(pat in error_lower for pat in RETRYABLE_ERROR_PATTERNS)

# --- Configuration ---
MODULE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = MODULE_DIR.parent.parent
CONFIG_DIR = MODULE_DIR / "config"

def get_output_dir(path_str):
    """Resolve output directory relative to project root if not absolute."""
    p = Path(path_str)
    if p.is_absolute():
        return p
    return PROJECT_ROOT / p

OUTPUT_DIR = get_output_dir(os.getenv("OUTPUT_DIR", "data/derivatives"))

def load_config():
    """Load configuration from env or defaults."""
    config = {
        "DATA_SOURCE": os.getenv("DATA_SOURCE", "mock"),
        "SYMBOLS": os.getenv("SYMBOLS", "BTCUSDT,ETHUSDT").split(","),
        "OUTPUT_FORMAT": os.getenv("OUTPUT_FORMAT", "json"),
        "OUTPUT_DIR": OUTPUT_DIR
    }
    # Attempt to load from .env if present (simple parse)
    env_path = CONFIG_DIR / ".env"
    if env_path.exists():
        with open(env_path, "r") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    key, val = line.strip().split("=", 1)
                    if key in config:
                        if key == "SYMBOLS":
                            config[key] = val.split(",")
                        elif key == "OUTPUT_DIR":
                            config[key] = get_output_dir(val)
                        else:
                            config[key] = val
    return config


@dataclass
class DerivativesRow:
    symbol: str
    exchange: str
    timestamp: str
    open_interest: Optional[float] = None
    funding_rate: Optional[float] = None
    long_short_ratio: Optional[float] = None
    liquidations_long: Optional[float] = None
    liquidations_short: Optional[float] = None
    volume_futures: Optional[float] = None
    error: Optional[str] = None

# --- Adapters ---
class BaseAdapter:
    def __init__(self, exchange_name, max_workers=5, retries=3, backoff_factor=1.0):
        self.exchange_name = exchange_name
        self.max_workers = max_workers
        self.retries = retries
        self.backoff_factor = backoff_factor
        self.logger = logging.getLogger(self.__class__.__name__)

    def _fetch(self, url):
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        for attempt in range(self.retries):
            try:
                with urllib.request.urlopen(req, timeout=10) as response:
                    return json.loads(response.read().decode('utf-8'))
            except Exception as e:
                wait_time = self.backoff_factor * (2 ** attempt)
                error_msg = str(e)
                
                if isinstance(e, urllib.error.HTTPError):
                    if e.code == 429:
                        error_msg = "Rate limit exceeded (429)"
                        wait_time = max(wait_time, 2.0)
                    elif e.code == 418:
                        error_msg = "IP auto-banned (418)"
                        self.logger.error(f"{error_msg} for {url}. Aborting.")
                        return None
                    else:
                        error_msg = f"HTTP {e.code}"
                elif isinstance(e, urllib.error.URLError):
                    error_msg = f"Network/Timeout ({e.reason})"

                if attempt == self.retries - 1:
                    self.logger.error(f"Final fetch failure for {url} after {self.retries} attempts: {error_msg}")
                    return None
                    
                self.logger.warning(f"Fetch failed for {url} (attempt {attempt+1}/{self.retries}): {error_msg}. Retrying in {wait_time}s...")
                time.sleep(wait_time)

    def _collect_symbol(self, symbol, batch_timestamp):
        raise NotImplementedError

    def _safe_collect_symbol(self, symbol, batch_timestamp):
        try:
            row = self._collect_symbol(symbol, batch_timestamp)
            if not isinstance(row, DerivativesRow):
                self.logger.error(f"Invalid return type for {symbol}. Expected DerivativesRow, got {type(row).__name__}")
                return DerivativesRow(
                    symbol=symbol,
                    exchange=self.exchange_name,
                    timestamp=batch_timestamp,
                    error=f"Internal Error: Invalid return type {type(row).__name__}"
                )
            return row
        except Exception as e:
            self.logger.error(f"Critical failure collecting {symbol}: {str(e)}")
            return DerivativesRow(
                symbol=symbol,
                exchange=self.exchange_name,
                timestamp=batch_timestamp,
                error=str(e)
            )

    def collect(self, symbols):
        data = []
        batch_timestamp = datetime.now(timezone.utc).isoformat()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            results = executor.map(lambda sym: self._safe_collect_symbol(sym, batch_timestamp), symbols)
            for row in results:
                if row is not None:
                    data.append(asdict(row))
                
        return data

class MockAdapter(BaseAdapter):
    def __init__(self, max_workers=5, retries=3, backoff_factor=1.0):
        super().__init__("MOCK", max_workers=max_workers, retries=retries, backoff_factor=backoff_factor)

    def _collect_symbol(self, symbol, batch_timestamp):
        # Simulate derivatives data
        oi = random.uniform(10_000_000, 50_000_000)
        funding = random.uniform(-0.01, 0.05)
        ls_ratio = random.uniform(0.8, 1.2)
        liq_long = random.uniform(0, 1_000_000)
        liq_short = random.uniform(0, 1_000_000)
        
        return DerivativesRow(
            symbol=symbol,
            exchange="MOCK",
            timestamp=batch_timestamp,
            open_interest=round(oi, 2),
            funding_rate=round(funding, 6),
            long_short_ratio=round(ls_ratio, 4),
            liquidations_long=round(liq_long, 2),
            liquidations_short=round(liq_short, 2),
            volume_futures=round(random.uniform(50_000_000, 200_000_000), 2)
        )

# --- Core Logic ---
class DerivativesCollector:
    def __init__(self, config):
        self.config = config
        self.adapter = self._get_adapter()
        self.output_dir = self.config["OUTPUT_DIR"]
        if not self.output_dir.exists():
            try:
                self.output_dir.mkdir(parents=True, exist_ok=True)
            except Exception:
                pass # Might fail on read-only systems, handled later

    def _get_adapter(self):
        source = self.config["DATA_SOURCE"].lower()
        if source == "mock":
            return MockAdapter()
        elif source == "binance":
            from .binance_adapter import BinanceAdapter
            return BinanceAdapter()
        elif source == "bitget":
            from .bitget_adapter import BitgetAdapter
            return BitgetAdapter()
        # Add other adapters here
        logger.warning(f"Unknown data source '{source}', falling back to mock.")
        return MockAdapter()

    def run(self):
        logger.info(f"Collecting derivatives data for {self.config['SYMBOLS']} using {self.config['DATA_SOURCE']}...")
        start_time = time.perf_counter()
        data = self.adapter.collect(self.config["SYMBOLS"])
        duration_s = time.perf_counter() - start_time
        
        self._output(data, duration_s=duration_s)
        return data

    def _output(self, data, duration_s=0.0):
        fmt = self.config["OUTPUT_FORMAT"].lower()
        now = datetime.now()
        timestamp_str = now.strftime("%Y%m%d_%H%M%S")
        filename = f"derivatives_{timestamp_str}.{fmt}"
        filepath = self.output_dir / filename
        
        # Calculate stats for Sidecar
        stats = {
            "requested": len(data),
            "succeeded": len([r for r in data if r.get("error") is None]),
            "failed": len([r for r in data if r.get("error") is not None])
        }
        
        meta = {
            "batch_timestamp": now.astimezone().isoformat(),
            "source": self.config["DATA_SOURCE"],
            "stats": stats,
            "duration_s": round(duration_s, 3),
            "meta_schema_version": 1
        }

        # Console Output
        print(json.dumps(data, indent=2))

        # File Output (if directory writable)
        if self.output_dir.exists():
            try:
                if fmt == "json":
                    with open(filepath, "w") as f:
                        json.dump(data, f, indent=2)
                elif fmt == "csv":
                    if data:
                        keys = data[0].keys()
                        with open(filepath, "w", newline='') as f:
                            writer = csv.DictWriter(f, fieldnames=keys)
                            writer.writeheader()
                            writer.writerows(data)
                
                # Sidecar Meta JSON
                meta_filepath = filepath.with_suffix('.meta.json')
                with open(meta_filepath, "w") as f:
                    json.dump(meta, f, indent=2)
                
                logger.info(f"Data exported to: {filepath}")
                logger.info(f"Meta exported to: {meta_filepath}")
            except Exception as e:
                logger.error(f"Error writing output file: {e}")

# --- CLI ---
def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stderr)]
    )
    parser = argparse.ArgumentParser(description="Derivatives Collector")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Commands
    subparsers.add_parser("collect", help="Run collection")
    subparsers.add_parser("status", help="Show module status")
    subparsers.add_parser("sample", help="Run sample collection")
    subparsers.add_parser("export", help="Export sample data")

    args = parser.parse_args()
    config = load_config()

    if args.command == "collect":
        collector = DerivativesCollector(config)
        collector.run()
    elif args.command == "status":
        print("Derivatives Collector Status:")
        print(f"  Source: {config['DATA_SOURCE']}")
        print(f"  Symbols: {config['SYMBOLS']}")
        print(f"  Output: {config['OUTPUT_FORMAT']} -> {config['OUTPUT_DIR']}")
    elif args.command == "sample":
        # Force mock for sample
        config["DATA_SOURCE"] = "mock"
        collector = DerivativesCollector(config)
        collector.run()
    elif args.command == "export":
        # Force export mode
        collector = DerivativesCollector(config)
        collector.run()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
