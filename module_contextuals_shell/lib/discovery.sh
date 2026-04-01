#!/usr/bin/env bash

# Discovery Library for module_contextuals_shell V2
# Implements discovery of modules and their assets (scripts, contextuals, commands)

# Core discovery function
discover_modules() {
    local modules_root="$1"
    if [ -z "$modules_root" ]; then
        # Default to ../../modules relative to this lib file if not provided
        # Assuming this lib is in modules/module_contextuals_shell/lib/
        local current_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        modules_root="$(dirname "$(dirname "$current_dir")")"
    fi

    if [ ! -d "$modules_root" ]; then
        echo "Error: Modules root not found at $modules_root"
        return 1
    fi

    for d in "$modules_root"/*/; do
        if [ -d "$d" ]; then
            local dirname=$(basename "$d")
            
            # Filter out hidden directories and technical folders like __pycache__
            # Also explicitly exclude 'scripts' which is a top-level technical folder
            if [[ "$dirname" == .* ]] || [[ "$dirname" == __* ]] || [[ "$dirname" == "scripts" ]]; then
                continue
            fi

            # Check if it's a discoverable module (must contain at least one key asset)
            if [ -f "$d/sanity.sh" ] || \
               [ -f "$d/cmd.sh" ] || \
               [ -f "$d/menu.sh" ] || \
               [ -d "$d/scripts" ] || \
               [ -d "$d/contextuals" ] || \
               [ -d "$d/commands" ]; then
                echo "$dirname"
            fi
        fi
    done
}

# Inspect a specific module structure
inspect_module() {
    local module_name="$1"
    local modules_root="$2"
    
    if [ -z "$modules_root" ]; then
        local current_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        modules_root="$(dirname "$(dirname "$current_dir")")"
    fi
    
    local module_path="$modules_root/$module_name"
    
    if [ ! -d "$module_path" ]; then
        echo "Error: Module '$module_name' not found in $modules_root"
        return 1
    fi

    # Detect root assets
    local has_sanity="no"
    local has_cmd="no"
    local has_menu="no"
    
    [ -f "$module_path/sanity.sh" ] && has_sanity="yes"
    [ -f "$module_path/cmd.sh" ] && has_cmd="yes"
    [ -f "$module_path/menu.sh" ] && has_menu="yes"
    
    # Count sub-assets
    local script_count=0
    if [ -d "$module_path/scripts" ]; then
        script_count=$(find "$module_path/scripts" -maxdepth 1 -name "*.sh" 2>/dev/null | wc -l)
    fi
    
    local contextual_count=0
    if [ -d "$module_path/contextuals" ]; then
        contextual_count=$(find "$module_path/contextuals" -maxdepth 1 -name "*.ctx" 2>/dev/null | wc -l)
    fi
    
    local commands_count=0
    if [ -d "$module_path/commands" ]; then
        # Count non-hidden files in commands directory (excluding .*)
        commands_count=$(find "$module_path/commands" -maxdepth 1 -type f -not -name ".*" 2>/dev/null | wc -l)
    fi
    
    # Output simple structured view
    echo "module_name: $module_name"
    echo "module_path: $module_path"
    echo "has_sanity: $has_sanity"
    echo "has_cmd: $has_cmd"
    echo "has_menu: $has_menu"
    echo "script_count: $script_count"
    echo "contextual_count: $contextual_count"
    echo "commands_count: $commands_count"
}

# List executable scripts in a module
list_module_scripts() {
    local module_name="$1"
    local modules_root="$2"
    
    if [ -z "$modules_root" ]; then
        local current_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        modules_root="$(dirname "$(dirname "$current_dir")")"
    fi
    
    local scripts_dir="$modules_root/$module_name/scripts"
    
    if [ -d "$scripts_dir" ]; then
        find "$scripts_dir" -maxdepth 1 -name "*.sh" -exec basename {} \;
    else
        echo "No scripts directory found."
    fi
}

# List contextual files in a module
list_module_contextuals() {
    local module_name="$1"
    local modules_root="$2"
    
    if [ -z "$modules_root" ]; then
        local current_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        modules_root="$(dirname "$(dirname "$current_dir")")"
    fi
    
    local ctx_dir="$modules_root/$module_name/contextuals"
    
    if [ -d "$ctx_dir" ]; then
        find "$ctx_dir" -maxdepth 1 -name "*.ctx" -exec basename {} \;
    else
        echo "No contextuals directory found."
    fi
}

# List command files in a module
list_module_commands() {
    local module_name="$1"
    local modules_root="$2"
    
    if [ -z "$modules_root" ]; then
        local current_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        modules_root="$(dirname "$(dirname "$current_dir")")"
    fi
    
    local cmds_dir="$modules_root/$module_name/commands"
    
    if [ -d "$cmds_dir" ]; then
        find "$cmds_dir" -maxdepth 1 -type f -not -name ".*" -exec basename {} \;
    else
        echo "No commands directory found."
    fi
}
