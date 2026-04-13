# STUDENT — TARGET CANON

## 1. OBJECTIF PRODUIT DESIRE (ETABLI)

Student est un hub leger / archiviste central dans opt-trading.

Fonctions:
- journaling
- ingest HTTP
- archivage
- events append-only
- services de collecte
- IA locale de soutien

Contrainte forte:
- pas de DB layer lourd

---

## 2. ROLE SYSTEME

Position:
- machine de continuite (3e machine)

Interactions:
- recoit donnees (ingest)
- archive evenements
- alimente IA locale
- support analyse DeepSeek/Ollama

---

## 3. ETAT REPO REEL

- runtime reel: `scripts/student/`
- runbook operateur existant
- logique ingest partielle
- journal actif

---

## 4. ECART EXACT

- objectif produit clair (journal)
- mais:
  - pas de doc canon opposable unique
  - pas d'architecture explicitee
  - pas de contrat formel ingest / archive

---

## 5. CONTRAINTES

- runtime gele (exception)
- pas de refactor lourd
- append-only obligatoire

---

## 6. NON_OBJECTIFS

- ne devient pas:
  - DB layer
  - moteur analytics lourd
  - cluster distribue
