#!/usr/bin/env python3
"""Benchmark baseline for pro desk registry access — B01-B08.

Measures raw JSON parse vs compiled index dict lookup performance.
Produces outputs/benchmarks/pro_desk_runtime_index_baseline.json.

Usage: python3 scripts/benchmarks/bench_pro_desk_registry_access.py
"""

from __future__ import annotations
import json
import time
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

OUTPUT_DIR = REPO_ROOT / "outputs" / "benchmarks"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

INVENTORY_PATH = REPO_ROOT / "modules" / "data_center" / "registry" / "pro_desk_data_inventory.json"
CANDIDATES_PATH = REPO_ROOT / "modules" / "data_center" / "registry" / "source_candidates.json"
PRODUCERS_PATH = REPO_ROOT / "modules" / "data_center" / "registry" / "producers.json"

ITERATIONS = 1000
WARMUP = 50

# --- Helpers ---

def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def now_us() -> int:
    return time.perf_counter_ns() // 1000


def bench(name: str, func, iterations=ITERATIONS, warmup=WARMUP):
    for _ in range(warmup):
        func()
    latencies = []
    for _ in range(iterations):
        t0 = now_us()
        result = func()
        t1 = now_us()
        latencies.append(t1 - t0)
    latencies.sort()
    p50 = latencies[len(latencies) // 2]
    p99 = latencies[int(len(latencies) * 0.99)]
    mean = sum(latencies) / len(latencies)
    return {
        "name": name,
        "iterations": iterations,
        "p50_us": p50,
        "p99_us": p99,
        "mean_us": round(mean, 2),
        "min_us": latencies[0],
        "max_us": latencies[-1],
        "result_type": type(result).__name__ if result is not None else "None",
    }


# --- B01: resolve() single call with JSON parse ---

def bench_b01_json():
    def call():
        inventory = load_json(INVENTORY_PATH)
        candidates = load_json(CANDIDATES_PATH)
        producers = load_json(PRODUCERS_PATH)
        # simulate resolve: find data_key across all files
        key = "open_interest"
        for item in inventory["data_items"]:
            for f in item["fields"]:
                if f["data_key"] == key:
                    _ = f["description"]
        _ = candidates["source_candidates"].get("P10", {}).get("sources", {}).get("existing", [])
        _ = producers["producers"][0]["producer_id"]
        return True
    return bench("B01_resolve_json_parse", call)


# --- B02: throughput baseline ---

def bench_b02_throughput():
    inventory = load_json(INVENTORY_PATH)
    candidates = load_json(CANDIDATES_PATH)
    producers = load_json(PRODUCERS_PATH)
    t0 = now_us()
    count = 0
    while (now_us() - t0) < 1_000_000:  # 1 second
        key = "open_interest"
        for item in inventory["data_items"]:
            for f in item["fields"]:
                if f["data_key"] == key:
                    pass
        _ = producers["producers"]
        count += 1
    return {
        "name": "B02_json_throughput",
        "calls_per_second": count,
        "duration_s": 1.0,
    }


# --- B03: cold start ---

def bench_b03_cold_start():
    def call():
        inventory = load_json(INVENTORY_PATH)
        candidates = load_json(CANDIDATES_PATH)
        producers = load_json(PRODUCERS_PATH)
        return sum([len(inventory["data_items"]), len(candidates["source_candidates"]), len(producers["producers"])])
    return bench("B03_cold_start_json", call, iterations=30, warmup=3)


# --- B04: memory baseline ---

def bench_b04_memory():
    import tracemalloc
    tracemalloc.start()
    inventory = load_json(INVENTORY_PATH)
    candidates = load_json(CANDIDATES_PATH)
    producers = load_json(PRODUCERS_PATH)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {
        "name": "B04_memory_json",
        "parsed_data_kb": round(peak / 1024, 1),
        "note": "Peak memory after loading all registry JSONs",
    }


# --- B07: stale fallback ---

def bench_b07_stale():
    def call():
        return {"stale": True, "canonical_value": None, "reason": "no_candidates"}
    return bench("B07_stale_fallback_baseline", call)


# --- B08: JSON parse vs dict lookup ---

def bench_b08_compare():
    inventory = load_json(INVENTORY_PATH)

    # Build a minimal dict index for comparison
    index = {}
    for item in inventory["data_items"]:
        for f in item["fields"]:
            index[f["data_key"]] = {
                "P_class": item["priority_class"],
                "description": f["description"],
            }

    key = "open_interest"

    def json_scan():
        for item in inventory["data_items"]:
            for f in item["fields"]:
                if f["data_key"] == key:
                    return f["description"]
        return None

    def dict_lookup():
        return index.get(key, {}).get("description")

    r_json = bench("B08_json_scan", json_scan)
    r_dict = bench("B08_dict_lookup", dict_lookup)

    speedup = r_json["mean_us"] / max(r_dict["mean_us"], 0.001)
    return {
        "name": "B08_json_vs_dict",
        "json_scan_mean_us": r_json["mean_us"],
        "dict_lookup_mean_us": r_dict["mean_us"],
        "speedup": round(speedup, 1),
        "json_detail": r_json,
        "dict_detail": r_dict,
    }


# --- Main ---

def main():
    results = {
        "benchmark_version": "v1",
        "run_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "inventory_fields": 0,
        "results": [],
    }

    # Count fields
    inventory = load_json(INVENTORY_PATH)
    results["inventory_fields"] = sum(len(item["fields"]) for item in inventory["data_items"])

    print(f"=== PRO DESK REGISTRY BENCHMARK ===")
    print(f"Inventory: {results['inventory_fields']} fields")
    print(f"Iterations: {ITERATIONS} (warmup: {WARMUP})")
    print()

    benchmarks = [
        ("B01", bench_b01_json),
        ("B03", bench_b03_cold_start),
        ("B04", bench_b04_memory),
        ("B07", bench_b07_stale),
        ("B08", bench_b08_compare),
        ("B02", bench_b02_throughput),
    ]

    for name, func in benchmarks:
        try:
            r = func()
            results["results"].append(r)
            if isinstance(r, dict) and "p50_us" in r:
                print(f"  {name}: p50={r['p50_us']}us p99={r['p99_us']}us mean={r['mean_us']}us")
            else:
                print(f"  {name}: {r}")
        except Exception as e:
            print(f"  {name}: ERROR — {e}")
            results["results"].append({"name": name, "error": str(e)})

    out_path = OUTPUT_DIR / "pro_desk_runtime_index_baseline.json"
    out_path.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    print(f"\nResults written to {out_path}")


if __name__ == "__main__":
    main()
