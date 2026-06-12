# Mapping runtime student

## Etat machine retenu

- alias SSH `student` : `PASS`
- machine cible : `student`
- role retenu : machine `Local Ollama / lab`

## Preuves reelles issues du child `6572ae8`

| Champ | Valeur constatee | Statut |
| --- | --- | --- |
| SSH | `student` repond | `PASS` |
| hostname | `student` | `PASS` |
| user | `student` | `PASS` |
| repo | `/opt/trading` present | `PASS` |
| Ollama binaire | `/usr/local/bin/ollama` | `PASS` |
| version | `0.17.0` | `PASS` |
| process | `ollama serve` actif | `PASS` |
| ecoute | `127.0.0.1:11434` | `PASS` |
| API tags | reponse JSON | `PASS` |
| modele minimum prouve | `deepseek-r1:1.5b` | `PASS_LIMITED` |

## Lecture retenue

- `student` est maintenant la preuve machine la plus concrete de la ligne `Local Ollama`
- `Ollama` y tourne deja reellement
- la machine reste une surface lab locale, pas un runtime critique

## Limites

- machine modeste : `Intel i5-6500`, `4` coeurs, `7.5 GiB` RAM
- aucun GPU prouve dans ce lot
- aucun modele lourd n'est qualifie
- aucun changement runtime n'a ete applique pour obtenir ces preuves

## RISKS

- À qualifier.
