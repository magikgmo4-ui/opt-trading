# 20_PROMPT_AND_TOOLS_SIZE_AUDIT

## Taille system prompt avant slim

| Composant | Chars | % |
|-----------|-------|---|
| Tools (schemas + list) | ~28,000 | ~47% |
| Workspace files | ~13,000 | ~22% |
| Skills (9 entries) | ~4,837 | ~8% |
| OpenClaw internal | ~14,000 | ~23% |
| **Total** | **~30,000** | **100%** |

## Nombre de tools estime
- 24 tools injectes dans le system prompt
- Chaque tool a : summary + schema JSON avec properties
- Le total schema chars pour les 24 tools : ~25,570 chars

## Fichiers responsables du system prompt lourd
1. Tools (24 entries) — injectes par OpenClaw runtime, pas configurables directement
2. AGENTS.md (7809 chars) — instructions de comportement principales
3. Skills (9 built-in skills) — injectes par OpenClaw, non configurables directement
4. SOUL.md (1673 chars) — personnalite
5. BOOTSTRAP.md (1471 chars) — inutile apres premier setup

## Root cause confirmee
- qwen2.5:3b-instruct sur CPU student prend >300s pour evaluer ~30K chars de system prompt
- Ollama direct (sans system prompt OpenClaw) repond en 5.6s
- Le goulot est l'evaluation du prompt (prompt_eval), pas la generation

## Apres slim (iteration finale)

| Composant | Avant | Apres | Reduction |
|-----------|-------|-------|-----------|
| Tools | ~28,000 chars (24 tools) | ~270 chars (1 tool) | -99% |
| Workspace | ~13,000 chars | ~400 chars | -97% |
| Skills | ~4,837 chars | ~4,837 chars | 0% (non modifiable) |
| OpenClaw internal | ~14,000 chars | ~12,000 chars | 0% |
| **Total** | **~30,000 chars** | **~12,800 chars** | **-57%** |
