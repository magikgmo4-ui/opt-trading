# GO_OPT_TRADING_TERMUX_ANDROID_SETUP_01

| Champ | Valeur |
|---|---|
| GO | `GO_OPT_TRADING_TERMUX_ANDROID_SETUP_01` |
| Objet | Bootstrap Termux Android : clé SSH, SSH config, aliases fleet, authorize script |
| Déclencheur | Session mobile Android + SSH matrix 12/12 validée |
| Branche | `go/GO_OPT_TRADING_TERMUX_ANDROID_SETUP_01` |

## Livrables

| Fichier | Description |
|---|---|
| `modules/termux_operator/scripts/bootstrap.sh` | Script bootstrap one-shot Termux |
| `modules/termux_operator/scripts/authorize_termux_key.sh` | Propager clé Termux sur la flotte |
| `modules/termux_operator/docs/README.md` | Guide complet |

## Usage

```bash
# Sur Android Termux
bash bootstrap.sh
# → génère ~/.ssh/id_ed25519_termux
# → écrit ~/.ssh/config (5 machines)
# → ajoute aliases fleet/health/sessions/matrix

# Sur db-layer
bash modules/termux_operator/scripts/authorize_termux_key.sh "<clé pub>"
```
