# 30_FORBIDDEN_SURFACES

## Surfaces absolument interdites

| Surface | Risque | Protection |
|---------|--------|------------|
| Gmail | Fuite données, write non tracé | Exclu de l'enum orchestration ; pas de module runtime ; pas de credentials |
| Calendar | Write non tracé | Exclu de l'enum orchestration ; pas de module runtime |
| clickup | Write masse non controlé | Non activé en scheduler permanent |
| airtable | Write datasheet non controlé | Non activé en scheduler permanent |
| botpress | Write conversationnel | Non activé en scheduler permanent |
| telegram | Write notification non controlé | Non activé en scheduler permanent |
| google_sheets | Write non tracé | Non activé en scheduler permanent |
| trading | Risque financier | Non-trading only ; pas de module trading dans le scheduler |

## Vérification d'intégrité

Avant chaque activation de phase, vérifier :

```bash
# Aucun timer Gmail/Calendar/trading actif
systemctl --user list-timers --all | grep -E 'gmail|calendar|trading' || echo "OK — aucun trouvé"

# Aucun write externe non autorisé dans les jobs planifiés
grep -rn 'WRITE_GATED\|write-gated' scripts/ai/workers/job_packets/ | grep -v 'GO_DRIVE_CANARY' || echo "OK — aucun write-gated non Drive"

# Aucun signal/trading dans les workflows CI
grep -rn 'trading\|signal\|order\|exchange\|broker' .github/workflows/ --include='*.yml' || echo "OK — aucun trading dans CI"
```

## Réactivation future

Toute réactivation d'une surface interdite nécessite :
1. Nouveau GO dédié
2. Revue de sécurité
3. Test HITL
4. Activation progressive
5. Mise à jour de ce document
