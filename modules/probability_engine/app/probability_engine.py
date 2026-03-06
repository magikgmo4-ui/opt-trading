#!/usr/bin/env python3
"""
Probability Engine Module
Calculates directional probability scores based on aggregated feature biases.

Usage:
    python -m modules.probability_engine.app.probability_engine [command] [args]
"""
import sys
import os
import json
import argparse
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

OUTPUT_DIR = get_output_dir(os.getenv("OUTPUT_DIR", "data/probability"))

def load_config():
    """Load configuration from env or defaults."""
    config = {
        "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
        "OUTPUT_DIR": OUTPUT_DIR,
        "WEIGHTS": {
            "trend_bias": float(os.getenv("WEIGHT_TREND", 0.3)),
            "momentum_bias": float(os.getenv("WEIGHT_MOMENTUM", 0.2)),
            "open_interest_bias": float(os.getenv("WEIGHT_OPEN_INTEREST", 0.1)),
            "funding_bias": float(os.getenv("WEIGHT_FUNDING", 0.1)),
            "liquidation_bias": float(os.getenv("WEIGHT_LIQUIDATION", 0.1)),
            "liquidity_bias": float(os.getenv("WEIGHT_LIQUIDITY", 0.1)),
            "regime_bias": float(os.getenv("WEIGHT_REGIME", 0.1)),
            "volatility_bias": float(os.getenv("WEIGHT_VOLATILITY", 0.0)) # Optional
        }
    }
    # Attempt to load from .env if present
    env_path = CONFIG_DIR / ".env"
    if env_path.exists():
        with open(env_path, "r") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    key, val = line.strip().split("=", 1)
                    if key in config:
                        pass # Env vars already loaded, simple override logic here if needed
                    elif key.startswith("WEIGHT_"):
                        feature = key.lower().replace("weight_", "") + "_bias"
                        config["WEIGHTS"][feature] = float(val)
    return config

# --- Core Logic ---
class ProbabilityEngine:
    def __init__(self, config):
        self.config = config
        self.weights = config["WEIGHTS"]
        self.output_dir = config["OUTPUT_DIR"]
        if not self.output_dir.exists():
            try:
                self.output_dir.mkdir(parents=True, exist_ok=True)
            except Exception:
                pass

    def score(self, features):
        """
        Calculate probability score from features.
        Features should be a dict with keys like 'trend_bias' (-1.0 to 1.0).
        """
        total_weight = 0.0
        weighted_sum = 0.0
        details = {}

        for feature, value in features.items():
            if feature in self.weights and isinstance(value, (int, float)):
                w = self.weights[feature]
                # Normalize value to -1.0 to 1.0 range if needed (assuming input is already normalized)
                # Clamp input just in case
                v = max(-1.0, min(1.0, float(value)))
                
                weighted_sum += v * w
                total_weight += w
                details[feature] = {"value": v, "weight": w, "contribution": v * w}

        if total_weight == 0:
            return self._empty_result(features)

        # Normalize score to -1.0 to 1.0
        final_score = weighted_sum / total_weight
        
        # Convert to probabilities (0.0 to 1.0)
        # Score 1.0 -> Prob Long 1.0
        # Score -1.0 -> Prob Short 1.0 (Prob Long 0.0)
        # Score 0.0 -> Prob Long 0.5
        prob_long = (final_score + 1.0) / 2.0
        prob_short = 1.0 - prob_long
        
        # Confidence is magnitude of the score (how strong is the signal?)
        confidence = abs(final_score)

        direction = "NEUTRAL"
        if final_score > 0.1: direction = "LONG"
        elif final_score < -0.1: direction = "SHORT"

        summary = self._generate_summary(features, direction, confidence)

        return {
            "symbol": features.get("symbol", "UNKNOWN"),
            "timestamp": features.get("timestamp", datetime.now(timezone.utc).isoformat()),
            "probability_long": round(prob_long, 2),
            "probability_short": round(prob_short, 2),
            "confidence": round(confidence, 2),
            "directional_bias": direction,
            "raw_score": round(final_score, 3),
            "summary": summary,
            "_details": details
        }

    def _empty_result(self, features):
        return {
            "symbol": features.get("symbol", "UNKNOWN"),
            "timestamp": features.get("timestamp", datetime.now(timezone.utc).isoformat()),
            "probability_long": 0.5,
            "probability_short": 0.5,
            "confidence": 0.0,
            "directional_bias": "NEUTRAL",
            "summary": "No valid features or weights found.",
            "raw_score": 0.0
        }

    def _generate_summary(self, features, direction, confidence):
        # Simple rule-based explanation
        drivers = []
        for k, v in features.items():
            if k.endswith("_bias") and abs(v) >= 0.3:
                desc = "bullish" if v > 0 else "bearish"
                name = k.replace("_bias", "").replace("_", " ")
                drivers.append(f"{name} ({desc})")
        
        conf_str = "High" if confidence > 0.6 else "Moderate" if confidence > 0.3 else "Low"
        
        if not drivers:
            return f"{conf_str} confidence {direction} bias. No strong individual drivers."
        
        return f"{conf_str} confidence {direction} bias driven by: {', '.join(drivers[:3])}."

    def run_sample(self):
        # Load sample input
        sample_path = CONFIG_DIR / "example_input.json"
        if sample_path.exists():
            with open(sample_path, "r") as f:
                features = json.load(f)
        else:
            # Fallback mock
            features = {
                "symbol": "BTCUSDT",
                "trend_bias": 0.5,
                "momentum_bias": 0.2
            }
        
        result = self.score(features)
        print(json.dumps(result, indent=2))
        return result

    def run_file(self, filepath, explain=False):
        p = Path(filepath)
        if not p.exists():
            print(f"Error: File not found: {filepath}")
            sys.exit(1)
        
        with open(p, "r") as f:
            features = json.load(f)
        
        result = self.score(features)
        
        if not explain:
            # Remove details for cleaner output unless requested
            result.pop("_details", None)
            
        print(json.dumps(result, indent=2))

# --- CLI ---
def main():
    parser = argparse.ArgumentParser(description="Probability Engine")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    subparsers.add_parser("status", help="Show module status")
    subparsers.add_parser("sample", help="Run with sample data")
    
    score_parser = subparsers.add_parser("score", help="Score input file")
    score_parser.add_argument("--input", required=True, help="Path to input JSON features")
    
    explain_parser = subparsers.add_parser("explain", help="Score and explain input file")
    explain_parser.add_argument("--input", required=True, help="Path to input JSON features")

    args = parser.parse_args()
    config = load_config()
    engine = ProbabilityEngine(config)

    if args.command == "status":
        print("Probability Engine Status:")
        print(f"  Weights: {json.dumps(config['WEIGHTS'], indent=2)}")
        print(f"  Output Dir: {config['OUTPUT_DIR']}")
    elif args.command == "sample":
        engine.run_sample()
    elif args.command == "score":
        engine.run_file(args.input, explain=False)
    elif args.command == "explain":
        engine.run_file(args.input, explain=True)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
