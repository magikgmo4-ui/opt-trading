# PASSE D'AUDIT 2026-03-20 — CLÔTURE FORMELLE

```
Date de clôture : 2026-03-20
Mission         : GO_AUDIT_2026_03_20_FORMAL_CLOSE_01
Branche d'audit : audit/opt-trading-20260320a
Pivot canonique : opt-trading / sot/mainline
Statut          : CLÔTURÉ — passe documentaire terminée, chantiers différés explicitement listés
```

---

## 1. PÉRIMÈTRE CLÔTURÉ

Cette passe a cadré et qualifié les périmètres suivants, dans l'ordre de traitement :

| Ordre | Périmètre | Classification finale | Mission |
|---|---|---|---|
| 1 | `opt-trading / sot/mainline` + topologie transverse | repo pivot canonique + carte complète | `GO_CROSS_TOPLOGY_CANON_01` |
| 2 | `student` | sous-projet intégré à `opt-trading` | `GO_STUDENT_CANONICAL_SURFACE_01` |
| 3 | `student` — migration Phase 2 | état réel terrain documenté | `GO_STUDENT_PHASE2_MIGRATION_01` |
| 4 | `student` — doublons scripts | caller audit complet, risques classifiés | `GO_STUDENT_CLEANUP_DUPLICATES_01` |
| 5 | `api collector` (`derivatives_collector`) | module interne `opt-trading` | `GO_API_COLLECTOR_CANONICAL_MODULE_01` |
| 6 | `admin-trading`, `db-layer`, `cursor-ai` | machines / surfaces runtime | `GO_RUNTIME_SURFACES_CANONICAL_MAP_01` |
| 7 | `localcms` | projet séparé, 2 branches complémentaires | `GO_LOCALCMS_CANON_DECISION_01` |
| 8 | `algo_hf` | workstream séparé, service runtime prouvé | `GO_ALGO_HF_AUDIT_01` |

Hors périmètre de cette passe (intentionnel) : `openclaw`, `hf_trading`.

---

## 2. LIVRABLES CANONIQUES PRODUITS

### Bundle initial (pré-sessions cowork)

| Fichier | Rôle |
|---|---|
| `00_audit_plan.md` | Plan d'audit PM |
| `01_sot_mainline.md` | Rapport individuel du pivot `sot/mainline` |
| `90_convergence_matrix.md` | Matrice de convergence inter-branches |
| `95_repo_branch_pm_kanban.md` | Kanban PM aligné sur `sot/mainline` |
| `96_cross_project_inventory_kanban_archive_first.md` | Inventaire transversal archive-first |
| `97_cross_project_master_kanban.md` | Kanban maître transversal (maintenu vivant) |
| `98_claude_cowork_relaunch_pack.md` | Pack de reprise cowork Claude |
| `99_pm_decision.md` | Décision PM finale de la passe |

### Livrables sessions cowork (GO_XXX)

| Fichier | Contenu | Statut |
|---|---|---|
| `91_cross_topology_canon.md` | Carte minimale transverse — classification de tous les périmètres | LIVRÉ |
| `92_student_canonical_surface.md` | Fiche canonique `student` — racine, façades, wrappers, frontière | LIVRÉ |
| `93_student_phase2_migration.md` | Migration Phase 2 — état terrain, corrections déjà appliquées | PARTIEL |
| `94_student_cleanup_duplicates.md` | Caller audit doublons `student` — classification par risque | LIVRÉ |
| `A0_api_collector_canonical_module.md` | Fiche module `derivatives_collector` — structure, état, runbook | LIVRÉ |
| `A1_runtime_surfaces_canonical_map.md` | Carte machines runtime — admin-trading, db-layer, cursor-ai | LIVRÉ |
| `A2_localcms_canon_decision.md` | Décision canonique `localcms` — rôle des 2 branches | LIVRÉ |
| `A3_algo_hf_audit.md` | Qualification `algo_hf` — service prouvé, source non localisée | LIVRÉ (partiel) |
| `A4_audit_2026_03_20_formal_close.md` | Ce document — clôture formelle de la passe | LIVRÉ |

---

## 3. ÉTABLI / PARTIEL / DIFFÉRÉ

### ÉTABLI — décisions figées, non à rouvrir sans besoin explicite

| Périmètre | Ce qui est établi |
|---|---|
| `opt-trading / sot/mainline` | Pivot canonique unique. Branches `feat/*` absorbées. Archives classées. |
| `student` | Sous-projet intégré. Racine `/opt/trading/student/`. Façades canoniques. Wrappers. 4 items runtime Phase 2 déjà corrigés avant la passe. |
| `derivatives_collector` | Module interne `opt-trading`. Adapter mock fonctionnel. Structure saine. |
| `admin-trading` | Machine Debian 12, OPS/bastion. Services `tv-webhook` + `tv-bitget-runner` actifs. Repo `opt-trading` sur `/opt/trading/`. Couche pilote runtime : `scripts/admin_trading/`. |
| `db-layer` | Machine Ubuntu 24.04, backend persistant. `algo-hf-api.service` actif. `/opt/trading/` absent. |
| `cursor-ai` | Machine Windows 10, poste dev. Repo local `C:\Users\ghost\opt-trading\`. Tunnel WireGuard vers admin-trading. |
| `localcms` | Projet séparé. 2 branches complémentaires : `feature/...` = base produit (M1+M2), `tools/...` = surcouche dev host. Arbitrage host validé opérateur 2026-03-18. |
| `algo_hf` | Workstream séparé de `opt-trading`. Service runtime `algo-hf-api` actif sur db-layer. Absent de `/opt/trading/`. |
| `Magikgmo` | Historique absorbé. Pas de pilotage actif. |
| `openclaw` | Hors bundle pour cette passe. Pas de support canonique. |

### PARTIEL — livré mais validation live manquante

| Périmètre | Ce qui est partiel | Condition de résolution |
|---|---|---|
| `student` Phase 2 migration | 4 items corrigés avant la passe. 2 items non traités dans les scripts listés (`LEGACY_CALLERS_INVENTORY`). | Validation SSH live sur machine `student` requise. |
| `student` cleanup doublons | Risque principal identifié : alias `cmd-deepseek_student`. Aucun retrait physique appliqué. | `readlink -f /usr/local/bin/cmd-deepseek_student` à vérifier sur machine `student`. |
| `algo_hf` | Service runtime prouvé. Code source non localisé. GitHub non consulté. | SSH live db-layer + consultation repo GitHub. |

### DIFFÉRÉ — hors périmètre ou décision PM à prendre

| Périmètre | Ce qui est différé | Point de reprise |
|---|---|---|
| `derivatives_collector` | Adapters réels (Coinglass, Binance, Bitget) = placeholders. | `GO_DERIVATIVES_COLLECTOR_ADAPTERS_01` si besoin |
| `localcms` | Décision merge/consolidation des 2 branches. Reprise développement M3+. | `GO_LOCALCMS_NEXT_01` si reprise CMS |
| `algo_hf` | Chemin code sur db-layer, GitHub, relation avec `hf_trading`. | `GO_ALGO_HF_DEEP_AUDIT_01` |
| `hf_trading` | Non démarré. Relation avec `algo_hf` inconnue. | `GO_HF_TRADING_AUDIT_01` |
| `openclaw` | Hors bundle pour cette passe. | `GO_OPENCLAW_CANONICAL_REENTRY_01` |
| `cursor-ai` — fiche_machine.md | Fiche vide dans le repo — données manquantes. | Correction ponctuelle si besoin |

---

## 4. CHANTIERS RESTANT OUVERTS (INVENTAIRE COMPLET)

| Priorité suggérée | Mission | Périmètre | Condition |
|---|---|---|---|
| P1 | Validation live `student` Phase 2 + cleanup | `student` machine | SSH accès live requis |
| P2 | `GO_ALGO_HF_DEEP_AUDIT_01` | `algo_hf` | SSH db-layer + GitHub |
| P2 | `GO_HF_TRADING_AUDIT_01` | `hf_trading` | GitHub / exploration locale |
| P3 | `GO_OPENCLAW_CANONICAL_REENTRY_01` | `openclaw` | Décision PM d'entrée |
| P3 | `GO_LOCALCMS_NEXT_01` | `localcms` | Décision PM de reprise CMS |
| P4 | `GO_DERIVATIVES_COLLECTOR_ADAPTERS_01` | `derivatives_collector` | Décision technique |

---

## 5. DÉCISIONS PM FIGÉES — NE PAS ROUVRIR SANS BESOIN EXPLICITE

```
1. opt-trading / sot/mainline = pivot canonique unique
2. student = sous-projet intégré (pas un repo séparé)
3. derivatives_collector = module interne (pas un service déployé séparé à ce stade)
4. admin-trading / db-layer / cursor-ai = surfaces runtime (pas des repos)
5. localcms = projet séparé — ne pas fusionner dans opt-trading
6. Magikgmo = historique — pas de pilotage actif
7. branches feat/* auditées = absorbées — ne pas réactiver
8. openclaw = hors bundle pour cette passe
```

---

## 6. POINT DE REPRISE RECOMMANDÉ POUR LA PROCHAINE SESSION

### Reprise minimale (orientée live validation)

```
GO_STUDENT_LIVE_VALIDATION_01
  Objectif : valider live sur machine student :
    - readlink -f /usr/local/bin/cmd-deepseek_student
    - état des 2 items non traités dans LEGACY_CALLERS_INVENTORY
  Prérequis : accès SSH à machine student (192.168.16.103)
  Livrable : section §5 de 94_student_cleanup_duplicates.md mise à jour
             + 93_student_phase2_migration.md complété
```

### Reprise portefeuille (si nouveau chantier)

```
GO_ALGO_HF_DEEP_AUDIT_01
  Objectif : identifier le chemin code algo-hf-api sur db-layer
             + qualifier la relation algo_hf / hf_trading
  Prérequis : accès SSH à db-layer (192.168.16.179)
              accès GitHub repo algo_hf si disponible
```

### Pack de reprise cowork

Pour relancer une session Claude, lire dans l'ordre :
1. `audit/2026-03-20/A4_audit_2026_03_20_formal_close.md` (ce fichier)
2. `audit/2026-03-20/00_audit_master_index.md`
3. `audit/2026-03-20/97_cross_project_master_kanban.md`

---

## 7. RÈGLES DE NON-RÉGRESSION

Les règles suivantes sont à respecter dans toutes les sessions futures :

- ne pas pousser sur Git depuis Claude cowork
- ne pas committer depuis Claude cowork
- ne pas modifier la topologie canonique sans validation PM (ChatGPT)
- ne pas traiter `db-layer` comme un déploiement `opt-trading` (confirmé absent)
- ne pas mélanger la machine `student` (runtime) et le workstream `student` (sous-projet intégré)
- ne pas supprimer de doublon script `student` sans validation live du `readlink`
- ne pas fusionner `localcms` dans `opt-trading`

---

## 8. SIGNATURE DE CLÔTURE

```
Passe d'audit       : 2026-03-20
Branche d'audit     : audit/opt-trading-20260320a
Livrables produits  : 17 fichiers (bundle initial + 9 livrables cowork)
Chantiers clôturés  : 8 sur 8 dans le périmètre défini
Chantiers différés  : 6 (listés §4)
Décisions PM figées : 8 (listées §5)
Clôture formelle    : GO_AUDIT_2026_03_20_FORMAL_CLOSE_01 → LIVRÉ
```
