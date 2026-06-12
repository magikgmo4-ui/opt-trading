# OT-REG-02 — RAPPORT DE MISE À JOUR REGISTRY

## 1. CONTEXTE
Mise à jour du référentiel officiel suite à l'audit OT-OPS-01 (V2). Objectif : aligner le registry sur la réalité terrain observée.

## 2. MODIFICATIONS MODULES (`modules_registry.yaml`)

### A. AJOUTS (REGISTRY-READY)
| Module | Domaine | Statut | Justification |
| :--- | :--- | :--- | :--- |
| **validated_prompt_factory** | Tools | ACTIVE | Présence prouvée, scripts complets, wrapper actif. |
| **trae_module_validator** | Tools | ACTIVE | Outil CI/CD fonctionnel, scripts complets. |
| **shared_sshfs_permanent** | Infra | ACTIVE | Service système prouvé, scripts de gestion présents. |

### B. MISES À JOUR (STATUTS)
| Module | Ancien Statut | Nouveau Statut | Justification |
| :--- | :--- | :--- | :--- |
| **workflow_post_change_v2** | (Non listé) | **BROKEN** | Contient `sudo` incompatible avec l'env actuel. |
| **workflow_post_change_v2_fix3** | (Non listé) | **ACTIVE_CANDIDATE** | Version corrigée (no-sudo) observée active. |

## 3. MODIFICATIONS WRAPPERS (`wrappers_registry.yaml`)

### A. AJOUTS
- **validated_prompt_factory** :
  - `menu-validated_prompt_factory`
  - `cmd-validated_prompt_factory`
  - `sanity-validated_prompt_factory`
- **trae_module_validator** :
  - `menu-trae_module_validator`
  - `cmd-trae_module_validator`
  - `sanity-trae_module_validator`

### B. NON-AJOUTS VOLONTAIRES
- Pas de wrapper global pour `shared_sshfs_permanent` (Service background).
- Pas de wrapper global pour `workflow_post_change_v2` (Hook interne).

## 4. IMPACT
Le registry couvre désormais ~60% des modules réels (vs 50% avant). Les modules critiques de production sont tous couverts.

## RISKS

- À qualifier.
