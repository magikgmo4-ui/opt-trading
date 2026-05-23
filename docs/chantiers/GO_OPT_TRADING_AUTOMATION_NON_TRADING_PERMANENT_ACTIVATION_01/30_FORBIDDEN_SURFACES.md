# 30_FORBIDDEN_SURFACES

## Surfaces absolument interdites

| Surface | Risque | Protection |
|---------|--------|------------|
| Gmail | Fuite données, write non tracé | Exclu de l'enum orchestration ; pas de module runtime ; pas de credentials |
| Calendar | Write non tracé | Exclu de l'enum orchestration ; pas de module runtime |
| trading | Risque financier | Non-trading only ; pas de module trading dans le scheduler |

## Restrictions par app externe (READ_ONLY autorisé, WRITE_GATED manuel seulement)

| App | READ_ONLY scheduler | WRITE_GATED manuel | Write autonome interdit |
|-----|:-------------------:|:------------------:|:-----------------------:|
| Airtable | Oui (health check) | Oui (canary) | Oui |
| ClickUp | Oui (health check) | Oui (canary) | Oui |
| Botpress | Oui (health check) | Oui (canary) | Oui |
| Google Sheets | Oui (health check) | Oui (canary) | Oui |
| Telegram | Oui (digest) | Non critique | Oui (commandes critiques) |
| Drive | Non (manuel seulement) | Oui (canary) | Oui |

## Vérification d'intégrité

Avant chaque activation de phase, vérifier :

```bash
# 1. Aucun timer Gmail/Calendar/trading actif
systemctl --user list-timers --all | grep -E 'gmail|calendar|trading' || echo "OK — aucun trouvé"

# 2. Aucun timer write-gated permanent (tous les WRITE_GATED doivent être manuels)
systemctl --user list-timers --all | grep -E 'write-gated\|canary\|WRITE_GATED' || echo "OK — aucun timer write-gated permanent"

# 3. Aucun write externe non autorisé dans les jobs planifiés
grep -rn 'WRITE_GATED\|write-gated' scripts/ai/workers/job_packets/ | grep -vE 'GO_DRIVE_CANARY|GO_AIRTABLE_CANARY|GO_CLICKUP_CANARY|GO_BOTPRESS_CANARY|GO_SHEETS_CANARY' || echo "OK — aucun write-gated non canary"

# 4. Aucun signal/trading dans les workflows CI
grep -rn 'trading\|signal\|order\|exchange\|broker' .github/workflows/ --include='*.yml' || echo "OK — aucun trading dans CI"

# 5. READ_ONLY seulement pour les apps externes schedulées (vérifier que le mode est READ_ONLY dans la config)
echo "Vérifier manuellement que non-trading-airtable-health.timer et similaires exécutent des jobs READ_ONLY"
echo "Les canary write-gated externes doivent être manuels, jamais des timers permanents"
```

## Réactivation future

Toute réactivation d'une surface interdite nécessite :
1. Nouveau GO dédié
2. Revue de sécurité
3. Test HITL
4. Activation progressive
5. Mise à jour de ce document
