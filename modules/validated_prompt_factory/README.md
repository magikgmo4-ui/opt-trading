# Validated Prompt Factory

## Description
Ce module transforme une synthèse validée (format texte structuré) en un prompt final spécialisé, prêt à être utilisé avec une IA ou pour un transfert.

## Modes de génération
1. **chatgpt_session** : Prompt conversationnel pour ChatGPT (Expert Senior).
2. **trae_module** : Prompt structuré pour créer un nouveau module durable dans Trae.
3. **trae_patch** : Prompt strict pour appliquer un patch correctif dans Trae.
4. **bundle_transfer** : Prompt pour préparer une archive ZIP de transfert.

## Utilisation
```bash
# Générer un prompt
./scripts/cmd.sh generate <mode> [input_file]

# Exemple
./scripts/cmd.sh generate chatgpt_session inputs/synthesis_example.txt
```

## Structure
- `app/` : Logique Python.
- `inputs/` : Exemples de synthèses.
- `output/` : Prompts générés.
- `scripts/` : Scripts de commande et menus.
