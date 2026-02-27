# Roadmap - desk_pro (module: desk_pro)

## Contexte
- Le projet est sur son premier ét stage (MVP)
- Les changements actuels incluent l'adhésion à des liens @api pour la section de commands et l'implémentation d'un système de notes de score avec les macro.
- Les actions réalisées : "Patch UI", "Add scoring rule" et "Test pipeline"

---

## Actions réalisées
1. **Patch UI**  
   - Ajout de la section de commandes et des @api calls pour l'interface de navigateur.

2. **Add scoring rule**  
   - Implementation d'un système de notes de score avec les macro weights.

3. **Test pipeline**  
   - Premise : Pusher pour l'application, then log un event à la régie du système de students.

---

## Roadmap

### [2026-02-26T17:10:15 UTC+1] MVP -> V1
- Ajout de la section de commandes et des @api calls.
- Implémentation d'un système de notes de score avec les macro weights.

### [2026-02-26T17:10:33 UTC+1] V1 -> V2  
- Testation du test pipeline.
- Validation et vérification des rate limits API.
- Découpage des erreurs d'erreur pendant la mise en place.

---

## Risques
- **Rate limit sur API** : Impossible de gérer à l'instant.
- **Problèmes avec le système de scores** : Comprendre les interactions avec les macro weights.

---

## Checklist (session prochaine)
1. **Section de commandes** : Ajout des liens @api pour l'interface.
2. **System de notes de score** : Tester la fonctionnalité des macro weights.
3. **Test pipeline** : Déposer les événements de test dans la régie du système de students.

---

## Vérification et Validation
Tous les changements doivent être validés par le team pour prévenir les erreurs et gérer les retours du système.

--- 

Ce projet a été forward en suivant un roadmap claire et structuré.
