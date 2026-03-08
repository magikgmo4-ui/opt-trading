#!/usr/bin/env bash

# Library: Context Reader
# Role: Reads and sanitizes .ctx files for processing

read_context_file() {
    local file="$1"
    
    if [ ! -f "$file" ]; then
        echo "Error: Context file not found: $file" >&2
        return 1
    fi
    
    # Read file, ignore comments (#) and empty lines
    grep -vE '^\s*#|^\s*$' "$file"
}

get_field() {
    local line="$1"
    local field_index="$2"
    
    echo "$line" | cut -d'|' -f"$field_index"
}

count_actions() {
    local file="$1"
    read_context_file "$file" | wc -l
}
