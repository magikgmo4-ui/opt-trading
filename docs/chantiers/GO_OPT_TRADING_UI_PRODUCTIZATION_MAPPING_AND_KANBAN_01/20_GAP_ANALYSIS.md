# 20_GAP_ANALYSIS

Generated: 2026-05-19

## Gaps Desk Pro

| # | Gap | Symptôme | Impact | Priorité |
|---|-----|----------|--------|----------|
| D1 | Pas de badge état système sur `/desk/ui` | L'utilisateur doit lire le JSON brut pour savoir si tout va bien | Lisibilité produit | P0 |
| D2 | Pas de parcours utilisateur documenté | Que faire quand `health=down` ? Quel bouton ? | Utilisabilité | P0 |
| D3 | `/desk/status/enhanced` absent | Le bundle le référençait — crée confusion sur les capacités réelles | Clarté | P0 |
| D4 | Cards `/desk/ui` sans labels d'état clairs | "Pipeline Status" affiche JSON brut sans interprétation | UX | P0 |
| D5 | Pas de panel d'action rapide | Start/stop/restart/alert-test non accessibles depuis l'UI | Opérabilité | P1 |
| D6 | Pas de panel erreurs récentes dans l'UI | `/desk/errors` existe mais pas intégré dans `/desk/ui` | Diagnostic | P1 |
| D7 | Pas de lien vers `/desk/toolbox` visible depuis `/desk/ui` | Toolbox existe mais peu discoverabilité | Navigation | P1 |

## Gaps localcms

| # | Gap | Symptôme | Impact | Priorité |
|---|-----|----------|--------|----------|
| L1 | Port 8000 partagé avec webhook server | localcms et webhook server incompatibles en simultané | Architecture | P0 |
| L2 | Pas de page pont localcms ↔ Desk Pro | Deux surfaces sans lien — contexte docs/runtime fragmenté | Navigation | P1 |
| L3 | État visuel localcms non revalidé | Dernière validation historique — capture absente | Preuve produit | P1 |

## Gaps transverses

| # | Gap | Symptôme | Impact | Priorité |
|---|-----|----------|--------|----------|
| T1 | Captures visuelles absentes | Validation humaine difficile — rien dans le bundle | Preuve produit | P0 |
| T2 | Pas de checklist humaine d'acceptation | "produit fini" non mesurable objectivement | Livraison | P0 |
| T3 | Pas de matrice "expected UI state" | Régression visuelle non détectable | Qualité | P1 |
| T4 | Pas de smoke e2e navigateur | HTTP 200 ≠ UI correcte | Validation | P1 |
| T5 | Packaging final non standardisé | Bundle non réutilisable | Livraison | P1 |
| T6 | Critères de "produit fini" non documentés par surface | Acceptation subjective | Gouvernance | P0 |

## Critères "produit fini" par surface

Une surface UI est **produit fini** si :

| Critère | Desk Pro | localcms |
|---------|----------|----------|
| Premier écran explique l'état système | ✗ (JSON brut) | ~ (SPA sidebar) |
| Chaque badge a une signification documentée | ✗ | N/A |
| Chaque état `healthy/degraded/down` est visible | ✗ | N/A |
| Erreur propose une action | ✗ | ✗ |
| UI utilisable sans env secret | ✓ | ✓ |
| Tests passent | ✓ (172/172) | ✓ (intégration) |
| Screenshots présents | ✗ | ✗ |
| Revue humaine signée PASS | ✗ | ✗ |

## Découverte bloquante

**D3 + L1 sont les gaps les plus structurants :**
- D3 : clarifier que `/desk/status/enhanced` n'existe pas — supprimer de la doc ou implémenter
- L1 : documenter explicitement que localcms et webhook server ne peuvent pas coexister sur port 8000 — opérateur doit choisir
