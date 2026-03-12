import argparse
import os
import sys

# Canonical section names used in templates
REQUIRED_SECTIONS = [
    "CONTEXTE",
    "CLASSE",
    "OBJECTIF",
    "CONTRAINTES",
    "DEPENDANCES",
    "LIVRABLE",
    "VALIDATION",
    "SUITE",
    "POINT DE REPRISE"
]

# Mapping from possible input headers to canonical section names
HEADER_MAPPING = {
    "CONTEXTE": "CONTEXTE",
    "CLASSE": "CLASSE",
    "CLASSE CONFIRMÉE": "CLASSE",
    "OBJECTIF": "OBJECTIF",
    "CONTRAINTES": "CONTRAINTES",
    "DEPENDANCES": "DEPENDANCES",
    "RISQUES": "DEPENDANCES",
    "DEPENDANCES / RISQUES": "DEPENDANCES",
    "RISQUES / DEPENDANCES": "DEPENDANCES",
    "LIVRABLE": "LIVRABLE",
    "LIVRABLES": "LIVRABLE",
    "LIVRABLE ATTENDU": "LIVRABLE",
    "LIVRABLES ATTENDUS": "LIVRABLE",
    "VALIDATION": "VALIDATION",
    "VALIDATION ATTENDUE": "VALIDATION",
    "SUITE": "SUITE",
    "SUITE LOGIQUE": "SUITE",
    "POINT DE REPRISE": "POINT DE REPRISE"
}

# Templates for different modes
TEMPLATES = {
    "chatgpt_session": """
# PROMPT POUR SESSION CHATGPT

## CONTEXTE
{CONTEXTE}

## OBJECTIF
{OBJECTIF}

## CLASSE
{CLASSE}

## INSTRUCTIONS
Agis en tant qu'expert technique senior.
Tu dois analyser la demande et proposer une solution étape par étape.
Ne commence pas à coder immédiatement, valide d'abord ta compréhension.

## CONTRAINTES
{CONTRAINTES}

## RISQUES ET DEPENDANCES
{DEPENDANCES}

## LIVRABLES ATTENDUS
{LIVRABLE}

## VALIDATION
{VALIDATION}

## SUITE LOGIQUE
{SUITE}

## POINT DE REPRISE
{POINT DE REPRISE}
""",
    "trae_module": """
# PROMPT POUR CREATION DE MODULE TRAE

## INITIALISATION
Tu travailles dans le répertoire courant du projet.
Tu dois créer un NOUVEAU MODULE DURABLE.

## CLASSE CONFIRMÉE
{CLASSE}

## OBJECTIF PRINCIPAL
{OBJECTIF}

## CONTEXTE
{CONTEXTE}

## STRUCTURE ATTENDUE
Le module doit respecter la structure standard :
- README.md
- app/ (code source principal)
- scripts/ (cmd.sh, menu.sh, sanity_check.sh)
- contextuals/ (pour discovery V2)
- commands/ (pour discovery V2)

## CONTRAINTES TECHNIQUES
{CONTRAINTES}

## RISQUES A EVITER
{DEPENDANCES}

## LIVRABLES EXACTS
{LIVRABLE}

## VALIDATION OBLIGATOIRE
{VALIDATION}
Tu dois fournir les commandes de validation à exécuter à la fin.

## POINT DE REPRISE
{POINT DE REPRISE}
""",
    "trae_patch": """
# PROMPT POUR PATCH CORRECTIF TRAE

## MODE PATCH
Tu ne dois PAS créer de nouveau module.
Tu dois UNIQUEMENT modifier l'existant pour corriger un problème ou ajouter une petite fonctionnalité.

## CONTEXTE DU PATCH
{CONTEXTE}

## OBJECTIF DU FIX
{OBJECTIF}

## FICHIERS CONCERNÉS
Identifie précisément les fichiers à modifier.
Ne touche à rien d'autre.

## CONTRAINTES
{CONTRAINTES}

## VALIDATION DU PATCH
{VALIDATION}

## POINT DE REPRISE
{POINT DE REPRISE}
""",
    "bundle_transfer": """
# PROMPT POUR GENERATION DE BUNDLE (ZIP)

## OBJECTIF
Préparer une archive ZIP contenant les fichiers nécessaires pour un transfert ou une livraison ciblée.

## CONTEXTE
{CONTEXTE}

## CONTENU DU BUNDLE
Basé sur : {OBJECTIF}

## FICHIERS A INCLURE
{LIVRABLE}

## INSTRUCTIONS
1. Lister les fichiers exacts.
2. Créer une structure temporaire propre.
3. Copier les fichiers.
4. Créer l'archive ZIP.
5. Nettoyer les fichiers temporaires.

## VALIDATION
Vérifier que le ZIP contient bien les éléments attendus et rien d'autre.
{VALIDATION}
"""
}

def parse_synthesis(file_path):
    """Parses the synthesis file into a dictionary of sections."""
    if not os.path.exists(file_path):
        print(f"Error: Input file not found: {file_path}")
        sys.exit(1)

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    sections = {}
    current_section = None
    buffer = []

    for line in content.splitlines():
        line = line.strip()
        if not line:
            # Keep empty lines if we are inside a section, to preserve paragraphs
            if current_section:
                buffer.append("")
            continue
            
        upper_line = line.upper()
        # Remove trailing colon if present for matching
        clean_line = upper_line.rstrip(":")
        
        is_header = False
        
        # Exact match against known headers
        if clean_line in HEADER_MAPPING:
            canonical_sec = HEADER_MAPPING[clean_line]
            if current_section:
                sections[current_section] = "\n".join(buffer).strip()
            current_section = canonical_sec
            buffer = []
            is_header = True
        
        if not is_header:
            if current_section:
                buffer.append(line)

    # Capture the last section
    if current_section:
        sections[current_section] = "\n".join(buffer).strip()

    return sections

def validate_sections(sections):
    """Checks if all required sections are present."""
    missing = []
    for sec in REQUIRED_SECTIONS:
        if sec not in sections:
            missing.append(sec)
    
    if missing:
        print(f"Warning: Missing sections in synthesis: {', '.join(missing)}")
        return False
    return True

def generate_prompt(mode, sections, output_dir):
    """Generates the prompt file based on mode and sections."""
    if mode not in TEMPLATES:
        print(f"Error: Unknown mode '{mode}'")
        sys.exit(1)

    template = TEMPLATES[mode]
    
    # Prepare context dict for formatting, defaulting to "Non spécifié" if missing
    format_data = {}
    for sec in REQUIRED_SECTIONS:
        format_data[sec] = sections.get(sec, "Non spécifié")

    try:
        content = template.format(**format_data)
    except KeyError as e:
        print(f"Error formatting template: Missing key {e}")
        sys.exit(1)

    filename = f"prompt_{mode}.txt"
    output_path = os.path.join(output_dir, filename)

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Success: Generated {output_path}")
    except IOError as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Validated Prompt Factory")
    parser.add_argument("--input", "-i", required=True, help="Path to the validated synthesis file")
    parser.add_argument("--mode", "-m", required=True, choices=TEMPLATES.keys(), help="Generation mode")
    parser.add_argument("--output-dir", "-o", default="output", help="Output directory")

    args = parser.parse_args()

    # Ensure output dir exists
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    print(f"Reading synthesis from: {args.input}")
    sections = parse_synthesis(args.input)
    
    print("Validating synthesis structure...")
    validate_sections(sections)

    print(f"Generating prompt for mode: {args.mode}")
    generate_prompt(args.mode, sections, args.output_dir)

if __name__ == "__main__":
    main()
