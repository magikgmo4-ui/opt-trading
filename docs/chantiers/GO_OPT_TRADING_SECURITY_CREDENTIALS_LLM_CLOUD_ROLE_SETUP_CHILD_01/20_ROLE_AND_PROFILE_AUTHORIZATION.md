# Role and Profile Authorization

Le rôle `llm_cloud` est destiné aux machines effectuant des tâches de raisonnement complexe ou de génération de contenu via des APIs externes.

## Statuts d'Autorisation

| Profil Machine | Statut | Action |
|----------------|--------|--------|
| `cursor-ai` | **AUTHORIZED_ACTIVE** | Activé par défaut (développement assisté). |
| `fantome` | **ELIGIBLE_DISABLED_BY_DEFAULT** | Éligible pour tâches d'IA autonomes. |
| `admin-trading` | **ELIGIBLE_DISABLED_BY_DEFAULT** | Éligible pour analyse de sentiment prod. |
| `db-layer` | **FORBIDDEN** | Interdit. |
| `student` | **FORBIDDEN** | Interdit (utilisation de LLM local recommandée). |
