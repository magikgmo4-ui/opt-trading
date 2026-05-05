---
doc_id: GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_TEST_SAFE_01_50_ROLLBACK_PLAN
doc_type: chantier/rollback_plan
repo: opt-trading
machine: cursor-ai
status: active
---

# 50_ROLLBACK_PLAN — Plan de rollback

## Rollback niveau 2 (mock endpoint)

```powershell
# 1. Arreter le listener mock s'il est actif
try {
    $listener.Stop()
    $listener.Close()
    Write-Host "Mock listener stopped"
} catch {
    Write-Host "No active listener to stop"
}

# 2. Verifier que le port 9999 est libere
netstat -ano | findstr ":9999"
# Si toujours occupe, identifier le PID et le kill
# taskkill /PID <PID> /F

# 3. Aucun fichier a nettoyer (le mock est en memoire)
Write-Host "Rollback niveau 2 termine"
```

## Rollback niveau 1 (validation JSON)

Aucun rollback necessaire. La validation JSON est read-only, elle ne modifie rien.

## Rollback Git

Si un commit non desire a ete fait pendant le test :

```bash
# Revenir au dernier commit stable
git reset --hard HEAD~1

# Ou revenir a sot/mainline
git checkout sot/mainline
git branch -D go/GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_TEST_SAFE_01
```

## Rollback admin-trading

Aucun rollback admin-trading requis car admin-trading n'est pas touche.

## Points de verification post-rollback

- [ ] Aucun listener sur le port 9999.
- [ ] Aucun processus mock residuel.
- [ ] Aucun fichier temporaire.
- [ ] Git status clean sur la branche de travail.
- [ ] `trade_allowed=false` preserve dans le template.
- [ ] `admin_trading_runtime=false` preserve dans le template.

## Retour a l'etat initial

```bash
git checkout sot/mainline
git branch -D go/GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_TEST_SAFE_01
# Etat = identique a avant le test
```
