# OT_TRAE_DOC_CONVERGENCE_CHECKLIST_V1

```
Date     : 2026-03-20
Mission  : GO_TRAE_DOC_CONVERGENCE_01
Référence: docs/ot/trae/OT_TRAE_DOC_CONVERGENCE_PROTOCOL_V1.md
```

---

## CHECKLIST — OUVERTURE DE SESSION CLAUDE COWORK

```
[ ] 1. Lire A4_audit_2026_03_20_formal_close.md
[ ] 2. Lire 97_cross_project_master_kanban.md
[ ] 3. Lire 00_audit_master_index.md
[ ] 4. Lire le document canonique du périmètre visé (92 / 93 / 94 / A0 / A1 / ...)
[ ] 5. (si chantier Trae V1) Lire OT_TRAE_SESSION_REPRISE.md
```

---

## CHECKLIST — AVANT PRODUCTION

```
[ ] La mission a un MISSION_ID nommé
[ ] Le contexte établi est clair — décisions figées identifiées
[ ] Le scope est borné (liste explicite de ce qui est autorisé)
[ ] Le hors-scope est explicite (liste de ce qui ne doit pas être touché)
[ ] Les sources ont été lues dans l'ordre
```

---

## CHECKLIST — COMPTE-RENDU D'EXÉCUTION (OBLIGATOIRE)

```
[ ] 1. État réel observé localement
[ ] 2. Fichiers produits / modifiés (liste avec chemins)
[ ] 3. Corrections / décisions appliquées (formulation exacte)
[ ] 4. Scripts modifiés ou non (confirmation explicite)
[ ] 5. Limites réelles observées (SSH inaccessible, GitHub non consulté, etc.)
[ ] 6. Statut final proposé (ÉTABLI / PARTIEL / DIFFÉRÉ)
[ ] 7. Point de reprise suivant (MISSION_ID + prérequis + action concrète)
```

---

## CHECKLIST — NON-RÉGRESSION (TOUJOURS)

```
[ ] Pas de git push
[ ] Pas de commit
[ ] Pas de modification statut kanban sans mandat PM
[ ] ÉTABLI et HYPOTHÈSE clairement séparés
[ ] Aucune contradiction entre sources lissée silencieusement
[ ] Aucun nouveau fichier OT_* à la racine du repo
```

---

## CLASSIFICATION RAPIDE D'UN CHANTIER

```
ÉTABLI     → décision figée + preuve documentée + closing ou kanban mis à jour
PARTIEL    → livrable produit + validation live manquante ou cleanup non exécuté
DIFFÉRÉ    → cadré + intentionnellement hors actif + point de reprise nommé
HORS PÉRIM → pas de MISSION_ID actif + pas de support canonique
```
