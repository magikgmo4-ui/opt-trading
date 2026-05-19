#!/usr/bin/env python3
"""
Derivatives Analyzer V1
Analyzes raw derivatives data to produce actionable market structure signals.
"""

import sys
import json
import argparse
import os
from datetime import datetime, timezone
from pathlib import Path

# Paths
MODULE_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = MODULE_ROOT / "config"
OUTPUT_DIR = MODULE_ROOT / "output"
DEFAULT_SAMPLE_INPUT = CONFIG_DIR / "sample_input.json"
DEFAULT_EXPORT_OUTPUT = OUTPUT_DIR / "derivatives_analysis.json"

def analyze_symbol(data):
    """
    Analyzes a single symbol's derivatives data.
    """
    symbol = data.get("symbol", "UNKNOWN")
    funding = data.get("funding_rate", 0.0)
    oi_change = data.get("open_interest_change_pct", 0.0)
    ls_ratio = data.get("long_short_ratio", 1.0)
    
    # 1. Funding State
    funding_state = "NEUTRAL"
    if funding > 0.03:
        funding_state = "EXTREME_POSITIVE"
    elif funding > 0.01:
        funding_state = "POSITIVE"
    elif funding < -0.03:
        funding_state = "EXTREME_NEGATIVE"
    elif funding < -0.01:
        funding_state = "NEGATIVE"
        
    # 2. OI State
    oi_state = "FLAT"
    if oi_change > 2.0:
        oi_state = "RISING"
    elif oi_change < -2.0:
        oi_state = "FALLING"
        
    # 3. Leverage Buildup
    # Simple proxy: if OI is rising and funding is non-neutral, leverage is building
    leverage_state = "LOW"
    if oi_state == "RISING":
        if funding_state in ["POSITIVE", "NEGATIVE"]:
            leverage_state = "MODERATE"
        elif funding_state in ["EXTREME_POSITIVE", "EXTREME_NEGATIVE"]:
            leverage_state = "HIGH"
            
    # 4. Squeeze Risk
    squeeze_risk = "LOW"
    if leverage_state == "HIGH":
        if funding_state == "EXTREME_POSITIVE":
            squeeze_risk = "LONG_SQUEEZE_RISK"
        elif funding_state == "EXTREME_NEGATIVE":
            squeeze_risk = "SHORT_SQUEEZE_RISK"
            
    # 5. Crowding Risk
    # High LS ratio + High OI = Crowded Longs
    crowding_risk = "LOW"
    if ls_ratio > 2.0 and oi_state == "RISING":
        crowding_risk = "HIGH (LONGS)"
    elif ls_ratio < 0.5 and oi_state == "RISING":
        crowding_risk = "HIGH (SHORTS)"
    elif ls_ratio > 1.5 or ls_ratio < 0.7:
        crowding_risk = "MEDIUM"
        
    # 6. Bias
    bias = "NEUTRAL"
    if funding_state in ["POSITIVE", "EXTREME_POSITIVE"]:
        if oi_state == "RISING":
            bias = "BULLISH_LEVERAGE"
        elif oi_state == "FALLING":
            bias = "BEARISH_UNWIND"
    elif funding_state in ["NEGATIVE", "EXTREME_NEGATIVE"]:
        if oi_state == "RISING":
            bias = "BEARISH_LEVERAGE"
        elif oi_state == "FALLING":
            bias = "BULLISH_UNWIND"
            
    # 7. Confidence & Summary
    confidence = 0.5
    if leverage_state == "HIGH" or squeeze_risk != "LOW":
        confidence = 0.8
    elif leverage_state == "MODERATE":
        confidence = 0.6
        
    summary = f"{symbol}: {bias} | Risk: {squeeze_risk} | Crowding: {crowding_risk}"
    
    return {
        "symbol": symbol,
        "analysis_timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        "derivatives_bias": bias,
        "oi_state": oi_state,
        "funding_state": funding_state,
        "leverage_buildup_state": leverage_state,
        "crowding_risk": crowding_risk,
        "squeeze_risk": squeeze_risk,
        "confidence": confidence,
        "summary": summary
    }

def run_analysis(input_path, output_path=None):
    if not os.path.exists(input_path):
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)
        
    try:
        with open(input_path, 'r') as f:
            data = json.load(f)
            
        results = []
        if isinstance(data, list):
            for item in data:
                results.append(analyze_symbol(item))
        elif isinstance(data, dict):
            results.append(analyze_symbol(data))
            
        if output_path:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            with open(output_path, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"Analysis saved to {output_path}")
        else:
            print(json.dumps(results, indent=2))
            
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Derivatives Analyzer V1")
    
    # Create subparsers
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Status command
    parser_status = subparsers.add_parser("status", help="Show module status")
    
    # Sample command
    parser_sample = subparsers.add_parser("sample", help="Show sample input")
    
    # Explain command
    parser_explain = subparsers.add_parser("explain", help="Explain analysis logic")
    
    # Analyze command
    parser_analyze = subparsers.add_parser("analyze", help="Run analysis")
    parser_analyze.add_argument("--input", help="Path to input JSON file")
    parser_analyze.add_argument("--output", help="Path to output JSON file")
    
    # Export command
    parser_export = subparsers.add_parser("export", help="Export analysis to file")
    parser_export.add_argument("--input", help="Path to input JSON file")
    parser_export.add_argument("--output", help="Path to output JSON file")

    # Backward compatibility for --action
    parser.add_argument("--action", choices=["analyze", "sample", "explain"], help="Deprecated: Use positional subcommands instead")
    parser.add_argument("--input", dest="global_input", help="Deprecated: Use with analyze subcommand")
    parser.add_argument("--output", dest="global_output", help="Deprecated: Use with analyze/export subcommand")

    args = parser.parse_args()
    
    # Handle backward compatibility
    if args.command is None:
        if args.action:
            args.command = args.action
            # Map global args to command args if command args are not set (though they won't be if parsed as global)
            # Since analyze/export subcommands have their own input/output, we need to manually pass them if we are in compatibility mode
            # But argparse handles them separately.
            # Simple hack: if command is None and action is set, we treat it as that command.
            # We need to access global_input and global_output.
            pass
        else:
            parser.print_help()
            sys.exit(1)

    # Command implementation
    if args.command == "status":
        print(f"Module: derivatives_analyzer")
        print(f"Default Sample Input: {DEFAULT_SAMPLE_INPUT}")
        print(f"Default Export Output: {DEFAULT_EXPORT_OUTPUT}")
        print(f"Ready: {DEFAULT_SAMPLE_INPUT.exists()}")
        
    elif args.command == "sample":
        if DEFAULT_SAMPLE_INPUT.exists():
            with open(DEFAULT_SAMPLE_INPUT, 'r') as f:
                print(f.read())
        else:
            print(f"Error: Sample file not found at {DEFAULT_SAMPLE_INPUT}")
            sys.exit(1)
            
    elif args.command == "explain":
        print("=== Derivatives Analyzer Logic ===")
        print("1. Funding: >0.01% (Pos), >0.03% (Extreme)")
        print("2. OI: >2% change (Rising)")
        print("3. Squeeze: Extreme Funding + Rising OI")
        print("4. Crowding: L/S Ratio extremes")
        
    elif args.command == "analyze":
        # Handle input path preference: args.input (subcommand) > args.global_input (backward compat) > default
        input_path = args.input if hasattr(args, 'input') and args.input else getattr(args, 'global_input', None)
        if not input_path:
            input_path = str(DEFAULT_SAMPLE_INPUT)
            
        output_path = args.output if hasattr(args, 'output') and args.output else getattr(args, 'global_output', None)
        
        run_analysis(input_path, output_path)
        
    elif args.command == "export":
        input_path = args.input if args.input else str(DEFAULT_SAMPLE_INPUT)
        output_path = args.output if args.output else str(DEFAULT_EXPORT_OUTPUT)
        
        run_analysis(input_path, output_path)

if __name__ == "__main__":
    main()
