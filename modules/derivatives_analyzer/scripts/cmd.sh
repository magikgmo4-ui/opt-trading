#!/usr/bin/env bash
set -euo pipefail

# Derivatives Analyzer - Command Wrapper

# Resolve paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODULE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
APP_DIR="$MODULE_ROOT/app"
CONFIG_DIR="$MODULE_ROOT/config"
OUTPUT_DIR="$MODULE_ROOT/output"

# Python check
PYTHON="python3"
if ! command -v $PYTHON &> /dev/null; then
    PYTHON="python"
fi

cmd="${1:-help}"

case "$cmd" in
    analyze)
        input_file="${2:-$CONFIG_DIR/sample_input.json}"
        $PYTHON "$APP_DIR/derivatives_analyzer.py" analyze --input "$input_file"
        ;;
        
    sample)
        $PYTHON "$APP_DIR/derivatives_analyzer.py" sample
        ;;
        
    explain)
        $PYTHON "$APP_DIR/derivatives_analyzer.py" explain
        ;;
        
    export)
        input_file="${2:-$CONFIG_DIR/sample_input.json}"
        output_file="${3:-$OUTPUT_DIR/derivatives_analysis.json}"
        $PYTHON "$APP_DIR/derivatives_analyzer.py" export --input "$input_file" --output "$output_file"
        ;;
        
    status)
        $PYTHON "$APP_DIR/derivatives_analyzer.py" status
        ;;
        
    *)
        echo "Usage: $0 {analyze|sample|explain|export|status}"
        exit 1
        ;;
esac
