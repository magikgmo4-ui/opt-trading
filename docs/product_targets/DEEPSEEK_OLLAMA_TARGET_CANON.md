# DEEPSEEK / OLLAMA — TARGET CANON

## 1. OBJECTIF PRODUIT DESIRE (ETABLI)

Stack IA locale en duo:

- thinking model
- response model

Fonctions:
- analyse locale
- journalisation
- integration Student
- validation externe obligatoire

Acces via:
- API HTTP (/api/chat)
- hub/menu unifie

---

## 2. ROLE SYSTEME

Position:
- couche cognitive locale

Interactions:
- consomme donnees Student
- produit analyse
- expose resultats via API/menu

---

## 3. ETAT REPO REEL

- deepseek_hub (candidat)
- deepseek_student (operateur)
- scripts/student runtime actif
- runbook partiel

---

## 4. ECART EXACT

- separation thinking/response non generalisee
- hub/menu non completement unifie
- usage encore mixte (CLI / scripts)

---

## 5. CONTRAINTES

- eviter ollama run en SSH
- privilegier API HTTP
- validation externe obligatoire
- learning-only (pas decision autonome)

---

## 6. NON_OBJECTIFS

- ne devient pas:
  - systeme autonome de trading
  - decisionnaire final
  - moteur non valide
