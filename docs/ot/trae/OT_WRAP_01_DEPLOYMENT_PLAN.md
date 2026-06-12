# OT-WRAP-01 — PLAN DE DÉPLOIEMENT WRAPPERS

## 1. OBJECTIF
Déployer les wrappers globaux pour les modules nouvellement intégrés au registry, garantissant leur accessibilité opérateur.

## 2. MODULES CIBLES (VALIDÉS)

### A. VALIDATED PROMPT FACTORY
| Wrapper | Cible | Statut |
| :--- | :--- | :--- |
| `/usr/local/bin/menu-validated_prompt_factory` | `modules/validated_prompt_factory/menu.sh` | **READY** |
| `/usr/local/bin/cmd-validated_prompt_factory` | `modules/validated_prompt_factory/cmd.sh` | **READY** |
| `/usr/local/bin/sanity-validated_prompt_factory` | `modules/validated_prompt_factory/sanity.sh` | **READY** |

### B. TRAE MODULE VALIDATOR
| Wrapper | Cible | Statut |
| :--- | :--- | :--- |
| `/usr/local/bin/menu-trae_module_validator` | `modules/trae_module_validator/menu.sh` | **READY** |
| `/usr/local/bin/cmd-trae_module_validator` | `modules/trae_module_validator/cmd.sh` | **READY** |
| `/usr/local/bin/sanity-trae_module_validator` | `modules/trae_module_validator/sanity.sh` | **READY** |

## 3. MODULES EXCLUS (VOLONTAIREMENT)
- **shared_sshfs_permanent** : Service systemd, pas d'interaction opérateur directe requise via wrapper global.
- **workflow_post_change_v2** : Hook interne, pas d'exposition CLI directe.

## 4. PROCÉDURE D'INSTALLATION
Exécution d'un script `ln -sf` ciblé sur `admin-trading`.

## 5. VALIDATION POST-DÉPLOIEMENT
- Vérification `ls -l /usr/local/bin/menu-*`
- Test d'exécution `sanity-*`

## RISKS

- À qualifier.
