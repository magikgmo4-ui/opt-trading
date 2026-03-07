#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
BASE="$(cd "$SCRIPT_DIR/.." && pwd)"
CMD="$BASE/scripts/cmd.sh"

# Colors (if terminal supports)
if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    BLUE='\033[0;34m'
    CYAN='\033[0;36m'
    YELLOW='\033[1;33m'
    NC='\033[0m' # No Color
else
    RED=''
    GREEN=''
    BLUE=''
    CYAN=''
    YELLOW=''
    NC=''
fi

header() {
    clear
    echo -e "${BLUE}=================================================${NC}"
    echo -e "${BLUE}   Desk Pro - MSI Operator Hub (V1)             ${NC}"
    echo -e "${BLUE}=================================================${NC}"
    echo -e "Host: $(hostname) | User: $(whoami)"
    echo -e "-------------------------------------------------"
}

show_group() {
    local title="$1"
    local color="$2"
    echo -e "${color}[ $title ]${NC}"
}

run_wrapper() {
    local wrapper="$1"
    # Support arguments in wrapper call (e.g. "cmd-probability_engine sample")
    local cmd_name=$(echo "$wrapper" | awk '{print $1}')
    
    if command -v "$cmd_name" >/dev/null 2>&1; then
        echo -e "${GREEN}Running: $wrapper ...${NC}"
        $wrapper
        echo
        read -p "Press Enter to continue..."
    else
        echo -e "${RED}Error: Wrapper '$cmd_name' not found in PATH.${NC}"
        read -p "Press Enter to continue..."
    fi
}

while true; do
    header
    
    echo -e "${CYAN}1. Operator Tools${NC}"
    echo "   (Runner, Capture, Dashboard)"
    echo -e "${CYAN}2. Analysis Engines${NC}"
    echo "   (Derivatives, Probability, Risk, Market)"
    echo -e "${CYAN}3. Monitoring & Performance${NC}"
    echo "   (Perf, State, Vision, Retention)"
    echo -e "${CYAN}4. Maintenance & Sanity${NC}"
    echo "   (Sanity Checks, Wrapper Mgmt)"
    echo
    echo -e "${YELLOW}0. Exit${NC}"
    echo -e "-------------------------------------------------"
    read -p "Select Group [0-4]: " choice
    
    case "$choice" in
        1)
            while true; do
                header
                show_group "OPERATOR TOOLS" "$CYAN"
                echo "1. Run Desk Pro (cmd-desk_pro_runner)"
                echo "2. Capture Inputs (cmd-desk_capture_inputs)"
                echo "3. Run Analysis (cmd-desk_analyze)"
                echo "4. Show Dashboard (cmd-desk_pro_dashboard)"
                echo "0. Back"
                read -p "Select Tool: " op_choice
                case "$op_choice" in
                    1) run_wrapper "cmd-desk_pro_runner" ;;
                    2) run_wrapper "cmd-desk_capture_inputs" ;;
                    3) run_wrapper "cmd-desk_analyze" ;;
                    4) run_wrapper "cmd-desk_pro_dashboard status" ;; # Default to status
                    0) break ;;
                    *) ;;
                esac
            done
            ;;
        2)
            while true; do
                header
                show_group "ANALYSIS ENGINES" "$CYAN"
                echo "1. Derivatives Collector"
                echo "2. Derivatives Analyzer"
                echo "3. Probability Engine"
                echo "4. Market Scanner"
                echo "5. Opportunity Ranker"
                echo "6. Liquidation Analyzer"
                echo "7. Decision Engine"
                echo "8. Risk Engine"
                echo "0. Back"
                read -p "Select Engine: " an_choice
                case "$an_choice" in
                    1) run_wrapper "cmd-derivatives_collector" ;;
                    2) run_wrapper "cmd-derivatives_analyzer analyze" ;; # Default to analyze
                    3) run_wrapper "cmd-probability_engine sample" ;; # Default to sample
                    4) run_wrapper "cmd-market_scanner" ;;
                    5) run_wrapper "cmd-opportunity_ranker" ;;
                    6) run_wrapper "cmd-liquidation_analyzer" ;;
                    7) run_wrapper "cmd-decision_engine" ;;
                    8) run_wrapper "cmd-risk_engine" ;;
                    0) break ;;
                    *) ;;
                esac
            done
            ;;
        3)
            while true; do
                header
                show_group "MONITORING" "$CYAN"
                echo "1. Perf Menu (menu-perf)"
                echo "2. Desk State (cmd-desk_state)"
                echo "3. Vision Bot (menu-vision_bot)"
                echo "4. Retention Clean (cmd-desk_retention)"
                echo "0. Back"
                read -p "Select Tool: " mon_choice
                case "$mon_choice" in
                    1) run_wrapper "menu-perf" ;;
                    2) run_wrapper "cmd-desk_state" ;;
                    3) run_wrapper "menu-vision_bot" ;;
                    4) run_wrapper "cmd-desk_retention" ;;
                    0) break ;;
                    *) ;;
                esac
            done
            ;;
        4)
            while true; do
                header
                show_group "MAINTENANCE" "$CYAN"
                echo "1. Check Wrappers (cmd-ops_wrappers)"
                echo "2. Sanity: Runner"
                echo "3. Sanity: Probability"
                echo "4. Sanity: Derivatives Analyzer"
                echo "5. Sanity: Menu Hub"
                echo "0. Back"
                read -p "Select Tool: " maint_choice
                case "$maint_choice" in
                    1) run_wrapper "cmd-ops_wrappers" ;; # Assuming wrapper for check_desk_pro_wrappers.sh exists or direct call
                    2) run_wrapper "sanity-desk_pro_runner" ;;
                    3) run_wrapper "sanity-probability_engine" ;;
                    4) run_wrapper "sanity-derivatives_analyzer" ;;
                    5) run_wrapper "sanity-ops_menu_hub" ;;
                    0) break ;;
                    *) ;;
                esac
            done
            ;;
        0)
            echo "Exiting MSI Hub."
            exit 0
            ;;
        *)
            ;;
    esac
done
