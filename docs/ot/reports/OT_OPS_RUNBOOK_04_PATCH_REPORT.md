# OT-OPS-RUNBOOK-04 — PATCH REPORT

## 1. OBJET
Correction de la commande `last-run` vers `last-run-info`.

## 2. RAISON
L'audit du script `scripts/admin_trading/desk_pro_cmd.sh` (Ligne 42) confirme que la commande exacte est `last-run-info`.
Le runbook mentionnait implicitement ou omettait cette commande utile pour l'étape 4.

## 3. CORRECTION
Ajout explicite de l'étape de vérification :
```bash
bash scripts/admin_trading/desk_pro_cmd.sh last-run-info
```

**Status : CORRIGÉ.**
