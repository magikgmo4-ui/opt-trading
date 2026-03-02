#!/usr/bin/env bash
set -euo pipefail

while true; do
  echo
  echo "=== Menu DeepSeek HUB (student) ==="
  echo "1) Sanity hub"
  echo "2) Status (ollama + api)"
  echo "3) Models (ollama list)"
  echo "4) Pull model"
  echo "5) THINKING (archive)"
  echo "6) RESPONSE (archive)"
  echo "7) Tail THINKING files"
  echo "8) Tail RESPONSE files"
  echo "9) Roadmap from events (student)"
  echo "10) Roadmap THINKING by module"
  echo "11) Roadmap RESPONSE by module"
  echo "12) Ollama logs (last 120)"
  echo "q) Quit"
  read -r -p "> " c

  case "$c" in
    1) sanity-deepseek_hub ;;
    2) cmd-deepseek_hub status ;;
    3) cmd-deepseek_hub models ;;
    4)
      read -r -p "Model [deepseek-r1:1.5b]: " m; m="${m:-deepseek-r1:1.5b}"
      # guard: si l'utilisateur colle un sujet ici, ça contient des espaces -> fallback
      if [[ "$m" =~ [[:space:]] ]]; then
        echo "WARN: model contient des espaces -> j'utilise deepseek-r1:1.5b"
        m="deepseek-r1:1.5b"
      fi
      # guard: si le modèle n'existe pas localement, fallback
      if command -v ollama >/dev/null 2>&1; then
        if ! ollama list 2>/dev/null | awk 'NR>1{print $1}' | grep -qx "$m"; then
          echo "WARN: model '$m' introuvable (ollama list) -> j'utilise deepseek-r1:1.5b"
          m="deepseek-r1:1.5b"
        fi
      fi
      cmd-deepseek_hub pull "$m"
      ;;
    5)
      read -r -p "Model [deepseek-r1:1.5b]: " m; m="${m:-deepseek-r1:1.5b}"
      # guard: si l'utilisateur colle un sujet ici, ça contient des espaces -> fallback
      if [[ "$m" =~ [[:space:]] ]]; then
        echo "WARN: model contient des espaces -> j'utilise deepseek-r1:1.5b"
        m="deepseek-r1:1.5b"
      fi
      # guard: si le modèle n'existe pas localement, fallback
      if command -v ollama >/dev/null 2>&1; then
        if ! ollama list 2>/dev/null | awk 'NR>1{print $1}' | grep -qx "$m"; then
          echo "WARN: model '$m' introuvable (ollama list) -> j'utilise deepseek-r1:1.5b"
          m="deepseek-r1:1.5b"
        fi
      fi
      read -r -p "Sujet: " s
      cmd-deepseek_hub think "$m" "$s"
      ;;
    6)
      read -r -p "Model [deepseek-r1:1.5b]: " m; m="${m:-deepseek-r1:1.5b}"
      # guard: si l'utilisateur colle un sujet ici, ça contient des espaces -> fallback
      if [[ "$m" =~ [[:space:]] ]]; then
        echo "WARN: model contient des espaces -> j'utilise deepseek-r1:1.5b"
        m="deepseek-r1:1.5b"
      fi
      # guard: si le modèle n'existe pas localement, fallback
      if command -v ollama >/dev/null 2>&1; then
        if ! ollama list 2>/dev/null | awk 'NR>1{print $1}' | grep -qx "$m"; then
          echo "WARN: model '$m' introuvable (ollama list) -> j'utilise deepseek-r1:1.5b"
          m="deepseek-r1:1.5b"
        fi
      fi
      read -r -p "Sujet: " s
      cmd-deepseek_hub response "$m" "$s"
      ;;
    7)
      read -r -p "N [10]: " n; n="${n:-10}"
      if ! [[ "$n" =~ ^[0-9]+$ ]]; then
        echo "WARN: N invalide -> 10"
        n=10
      fi
      cmd-deepseek_hub tail_think _ "$n"
      ;;
    8)
      read -r -p "N [10]: " n; n="${n:-10}"
      if ! [[ "$n" =~ ^[0-9]+$ ]]; then
        echo "WARN: N invalide -> 10"
        n=10
      fi
      cmd-deepseek_hub tail_response _ "$n"
      ;;
    9)
      read -r -p "Model [deepseek-r1:1.5b]: " m; m="${m:-deepseek-r1:1.5b}"
      # guard: si l'utilisateur colle un sujet ici, ça contient des espaces -> fallback
      if [[ "$m" =~ [[:space:]] ]]; then
        echo "WARN: model contient des espaces -> j'utilise deepseek-r1:1.5b"
        m="deepseek-r1:1.5b"
      fi
      # guard: si le modèle n'existe pas localement, fallback
      if command -v ollama >/dev/null 2>&1; then
        if ! ollama list 2>/dev/null | awk 'NR>1{print $1}' | grep -qx "$m"; then
          echo "WARN: model '$m' introuvable (ollama list) -> j'utilise deepseek-r1:1.5b"
          m="deepseek-r1:1.5b"
        fi
      fi
      read -r -p "N events [200]: " n; n="${n:-200}"
      cmd-deepseek_hub roadmap_events "$m" "$n"
      ;;
    10)
      read -r -p "Model [deepseek-r1:1.5b]: " m; m="${m:-deepseek-r1:1.5b}"
      # guard: si l'utilisateur colle un sujet ici, ça contient des espaces -> fallback
      if [[ "$m" =~ [[:space:]] ]]; then
        echo "WARN: model contient des espaces -> j'utilise deepseek-r1:1.5b"
        m="deepseek-r1:1.5b"
      fi
      # guard: si le modèle n'existe pas localement, fallback
      if command -v ollama >/dev/null 2>&1; then
        if ! ollama list 2>/dev/null | awk 'NR>1{print $1}' | grep -qx "$m"; then
          echo "WARN: model '$m' introuvable (ollama list) -> j'utilise deepseek-r1:1.5b"
          m="deepseek-r1:1.5b"
        fi
      fi
      read -r -p "Module [desk_pro]: " mod; mod="${mod:-desk_pro}"
      read -r -p "N events [40]: " n; n="${n:-40}"
      cmd-deepseek_hub roadmap_think_module "$m" "$mod" "$n"
      ;;
    11)
      read -r -p "Model [deepseek-r1:1.5b]: " m; m="${m:-deepseek-r1:1.5b}"
      # guard: si l'utilisateur colle un sujet ici, ça contient des espaces -> fallback
      if [[ "$m" =~ [[:space:]] ]]; then
        echo "WARN: model contient des espaces -> j'utilise deepseek-r1:1.5b"
        m="deepseek-r1:1.5b"
      fi
      # guard: si le modèle n'existe pas localement, fallback
      if command -v ollama >/dev/null 2>&1; then
        if ! ollama list 2>/dev/null | awk 'NR>1{print $1}' | grep -qx "$m"; then
          echo "WARN: model '$m' introuvable (ollama list) -> j'utilise deepseek-r1:1.5b"
          m="deepseek-r1:1.5b"
        fi
      fi
      read -r -p "Module [desk_pro]: " mod; mod="${mod:-desk_pro}"
      read -r -p "N events [40]: " n; n="${n:-40}"
      cmd-deepseek_hub roadmap_response_module "$m" "$mod" "$n"
      ;;
    12) cmd-deepseek_hub logs 120 ;;
    q) exit 0 ;;
    *) echo "Invalid" ;;
  esac
done
