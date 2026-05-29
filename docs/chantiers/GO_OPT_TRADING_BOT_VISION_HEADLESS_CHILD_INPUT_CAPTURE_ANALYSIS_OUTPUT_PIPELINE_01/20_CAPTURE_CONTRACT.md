# 20_CAPTURE_CONTRACT

## Objectif

Definir le contrat de capture pour rendre les screenshots reproductibles et
utilisables par la couche d'analyse.

## Points a valider

- viewport
- frequence
- sections
- full-page vs crop
- multi-capture
- reproductibilite
- fichiers 0-byte / `.uploading` interdits

## Preuves attendues

- captures identiques sur runs comparables
- zones d'interet conformes au mapping source
- sortie exploitable par OCR / vision sans retraitement manuel
