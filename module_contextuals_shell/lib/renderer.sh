#!/usr/bin/env bash

# Library: Context Renderer
# Role: Displays menus from context data

render_menu() {
    local file="$1"
    local title="${2:-Menu}"
    local i=1
    
    echo "========================================="
    echo " $title"
    echo "========================================="
    
    while IFS='|' read -r id label desc cat order vis_mod_menu vis_ops_super freq type target; do
        # Filter visibility
        if [[ "$vis_mod_menu" == "true" ]]; then
            printf "%2d) [%-5s] %s\n" "$i" "$cat" "$label"
            ((i++))
        fi
    done < <(read_context_file "$file")
    
    echo " 0) Exit"
    echo "========================================="
}
