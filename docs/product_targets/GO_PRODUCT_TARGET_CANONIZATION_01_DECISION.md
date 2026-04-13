# GO_PRODUCT_TARGET_CANONIZATION_01

## 1. QUESTION

Quelle cible produit canonique finale doit etre retenue pour:

- Student
- DeepSeek/Ollama
- OpenClaw

---

## 2. OPTIONS

1. maintenir scripts/student comme runtime durable
2. basculer vers deepseek_hub
3. officialiser deepseek-student comme surface canonique
4. combinaison structuree (hub + operator + runtime)

---

## 3. ETAT ACTUEL

- aucune cible finale unique figee repo-sourcee
- convergence partielle visible
- dependance forte au runtime existant

---

## 4. DECISION

Statut:
A_REVALIDER

---

## 5. CONDITIONS DE CLOTURE

- doc canon produit validee
- mapping runtime stabilise
- choix explicite:
  - hub
  - runtime
  - operator

- plan de migration defini
- retrait explicite de l'exception runtime si applicable

---

## 6. POINT CRITIQUE

Ne pas:
- casser scripts/student
- forcer unification prematuree
- perdre tracabilite runtime reel
