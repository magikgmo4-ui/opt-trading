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
import os
import json
import csv
import argparse
import random
import time
import urllib.request
import urllib.error
import concurrent.futures
from datetime import datetime, timezone
from pathlib import Path

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

# --- Adapters ---
class BaseAdapter:
    def __init__(self, max_workers=5):
        self.max_workers = max_workers

    def _fetch(self, url, retries=3, backoff_factor=1.0):
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        for attempt in range(retries):
            try:
                with urllib.request.urlopen(req, timeout=10) as response:
                    return json.loads(response.read().decode('utf-8'))
            except Exception as e:
                wait_time = backoff_factor * (2 ** attempt)
                error_msg = str(e)
                
                if isinstance(e, urllib.error.HTTPError):
                    if e.code == 429:
                        error_msg = "Rate limit exceeded (429)"
                        wait_time = max(wait_time, 2.0)
                    elif e.code == 418:
                        error_msg = "IP auto-banned (418)"
                        print(f"[{self.__class__.__name__.replace('Adapter', '').upper()}][FATAL] {error_msg} for {url}. Aborting.", file=sys.stderr)
                        return None
                    else:
                        error_msg = f"HTTP {e.code}"
                elif isinstance(e, urllib.error.URLError):
                    error_msg = f"Network/Timeout ({e.reason})"

                if attempt == retries - 1:
                    print(f"[{self.__class__.__name__.replace('Adapter', '').upper()}][ERROR] Final fetch failure for {url} after {retries} attempts: {error_msg}", file=sys.stderr)
                    return None
                    
                print(f"[{self.__class__.__name__.replace('Adapter', '').upper()}][WARN] Fetch failed for {url} (attempt {attempt+1}/{retries}): {error_msg}. Retrying in {wait_time}s...", file=sys.stderr)
                time.sleep(wait_time)

    def _collect_symbol(self, symbol, batch_timestamp):
        raise NotImplementedError

    def collect(self, symbols):
        data = []
        batch_timestamp = datetime.now(timezone.utc).isoformat()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            results = executor.map(lambda sym: self._collect_symbol(sym, batch_timestamp), symbols)
            for row in results:
                data.append(row)
                
        return data

class MockAdapter(BaseAdapter):
    def collect(self, symbols):
        data = []
        for symbol in symbols:
            # Simulate derivatives data
            oi = random.uniform(10_000_000, 50_000_000)
            funding = random.uniform(-0.01, 0.05)
            ls_ratio = random.uniform(0.8, 1.2)
            liq_long = random.uniform(0, 1_000_000)
            liq_short = random.uniform(0, 1_000_000)
            
            data.append({
                "symbol": symbol,
                "exchange": "MOCK",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "open_interest": round(oi, 2),
                "funding_rate": round(funding, 6),
                "long_short_ratio": round(ls_ratio, 4),
                "liquidations_long": round(liq_long, 2),
                "liquidations_short": round(liq_short, 2),
                "volume_futures": round(random.uniform(50_000_000, 200_000_000), 2)
            })
        return data

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
        print(f"Warning: Unknown data source '{source}', falling back to mock.")
        return MockAdapter()

    def run(self):
        print(f"Collecting derivatives data for {self.config['SYMBOLS']} using {self.config['DATA_SOURCE']}...")
        data = self.adapter.collect(self.config["SYMBOLS"])
        self._output(data)
        return data

    def _output(self, data):
        fmt = self.config["OUTPUT_FORMAT"].lower()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"derivatives_{timestamp}.{fmt}"
        filepath = self.output_dir / filename

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
                print(f"Data exported to: {filepath}")
            except Exception as e:
                print(f"Error writing output file: {e}")

# --- CLI ---
def main():
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
