#!/usr/bin/env bash
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="$BASE/scripts/cmd.sh"

echo "=== openclaw_operator_bridge ==="
echo "  sanity    → sanity check complet"
echo "  health    → état gateway + CLI"
echo "  test      → tests mock (no gateway)"
echo "  ask       → envoyer une question au builder"
echo "  build     → générer une proposition"
echo "  evaluate  → évaluer un signal"
echo "  review    → revoir un trade"
echo ""
echo "Exemple: $CMD ask 'analyse ce signal BTC'"
