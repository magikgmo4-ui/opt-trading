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

    local ctx_dir
    ctx_dir="$(cd "$(dirname "$file")" && pwd)"
    local module_dir
    module_dir="$(dirname "$ctx_dir")"

    # Loop to find N-th visible item
    while IFS='|' read -r id label desc cat order vis_mod_menu vis_ops_super freq type target; do
        if [[ "$vis_mod_menu" == "true" ]]; then
            if [[ "$i" -eq "$index" ]]; then
                echo "Executing: $label ($type -> $target)"
                execute_target "$type" "$target" "$ctx_dir" "$module_dir"
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
    local ctx_dir="${3:-}"
    local module_dir="${4:-}"

    # Clean up CRLF / whitespace noise
    target="$(printf '%s' "$target" | tr -d '\r' | xargs)"
    type="$(printf '%s' "$type" | tr -d '\r' | xargs)"

    case "$type" in
        script)
            if [ -f "$target" ]; then
                bash "$target"
                return 0
            fi

            if [ -f "./$target" ]; then
                bash "./$target"
                return 0
            fi

            if [ -n "$ctx_dir" ] && [ -f "$ctx_dir/$target" ]; then
                bash "$ctx_dir/$target"
                return 0
            fi

            if [ -n "$module_dir" ] && [ -f "$module_dir/$target" ]; then
                bash "$module_dir/$target"
                return 0
            fi

            echo "Error: Script file not found: $target" >&2
            echo "Checked: exact, ./$target, $ctx_dir/$target, $module_dir/$target" >&2
            return 1
            ;;
        function)
            if type -t "$target" > /dev/null; then
                "$target"
            else
                echo "Error: Function not defined in current scope: $target" >&2
                return 1
            fi
            ;;
        command)
            eval "$target"
            ;;
        *)
            echo "Error: Unknown action type: $type" >&2
            return 1
            ;;
    esac
}
