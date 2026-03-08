#!/usr/bin/env bash

# Library: Context Router
# Role: Routes user selection to target execution

route_action() {
    local file="$1"
    local index="$2"
    local i=1
    local found=0
    
    # Need reader loaded
    if ! type -t read_context_file > /dev/null; then
        echo "Error: Reader library not loaded" >&2
        return 1
    fi

    # Loop to find N-th visible item
    while IFS='|' read -r id label desc cat order vis_mod_menu vis_ops_super freq type target; do
        if [[ "$vis_mod_menu" == "true" ]]; then
            if [[ "$i" -eq "$index" ]]; then
                echo "Executing: $label ($type -> $target)"
                execute_target "$type" "$target"
                found=1
                break
            fi
            ((i++))
        fi
    done < <(read_context_file "$file")
    
    if [[ "$found" -eq 0 ]]; then
        echo "Error: Invalid selection index: $index" >&2
        return 1
    fi
}

execute_target() {
    local type="$1"
    local target="$2"
    
    case "$type" in
        script)
            if [ -f "$target" ]; then
                bash "$target"
            else
                echo "Error: Script file not found: $target" >&2
            fi
            ;;
        function)
            if type -t "$target" > /dev/null; then
                "$target"
            else
                echo "Error: Function not defined in current scope: $target" >&2
            fi
            ;;
        command)
            eval "$target"
            ;;
        *)
            echo "Error: Unknown action type: $type" >&2
            ;;
    esac
}
