# OPT-TRADING — REPRISE DE SESSION (CANONIQUE)

```
Date origine  : 2026-03-14
Mis à jour    : 2026-03-20 (GO_TRAE_SESSION_REPRISE_SYNC_01)
Vérifié       : 2026-03-21 (GO_TRAE_SESSION_REPRISE_SYNC_01 — passe de vérification)
Pivot         : opt-trading / sot/mainline
```

---

## 1. Objet

Fichier canonique de continuité pour reprendre une session sur `opt-trading` — Trae ou Claude Cowork — sans rouvrir de chantier technique.

**Mise à jour 2026-03-20** : la passe d'audit 2026-03-20 a introduit une couche canonique supplémentaire (kanban maître, clôture formelle, index livrables). Cette couche est désormais prioritaire pour les chantiers issus de cette passe. Elle coexiste avec le socle Trae V1 sans le remplacer.

Pour le protocole complet de convergence et l'ordre de lecture obligatoire :
→ `docs/ot/trae/OT_TRAE_DOC_CONVERGENCE_PROTOCOL_V1.md`
→ `docs/ot/trae/OT_TRAE_DOC_CONVERGENCE_CHECKLIST_V1.md`

---

## 2. Sources de vérité

### 2.1 Couche audit 2026-03-20 (prioritaire pour chantiers issus de cette passe)

| Source | Rôle |
|---|---|
| `audit/2026-03-20/A4_audit_2026_03_20_formal_close.md` | Décisions figées, ÉTABLI / PARTIEL / DIFFÉRÉ |
| `audit/2026-03-20/97_cross_project_master_kanban.md` | **Kanban maître actif** — statut de tous les chantiers courants |
| `audit/2026-03-20/00_audit_master_index.md` | Index des livrables produits et points de reprise |

Règle de priorité : le kanban maître `97_*` prime sur le kanban Trae pour tout ce qui concerne `student`, `api collector`, surfaces runtime, `localcms`, `algo_hf`, `hf_trading`, `openclaw`.

### 2.2 Couche socle Trae V1 (pour chantiers Trae internes `GO_OT_*`)

- Kanban (source of truth) : `docs/ot/kanban/opt_trading_kanban_source_of_truth.md`
- Synthèse kanban : `docs/ot/kanban/opt_trading_kanban_operational_summary_2026-03-14.md`
- Workflow sync Trae↔Kanban : `workflow_ai/WORKFLOW_TRAE_KANBAN_SYNC_2026-03-14.md`
- Point d'entrée mission (starter pack) : `docs/master_pack/mission_starter_pack/00_mission_start_guide.md`
- Standards projet (current state) : `docs/master_pack/00_current_state_and_standards.md`
- OT Trae (décisions / matrices) : `docs/ot/trae/`

Legacy conservé (ne pas promouvoir) :
- `opt_trading_kanban_source_of_truth_2026-03-13_updated.md` (racine, legacy)

---

## 3. Ce qui est établi

### 3.1 Canonicalisation docs OT (OK — 2026-03-14)
- Kanban canonique + synthèse en place.
- Workflow sync en place.

### 3.2 Migration OT_* hors de la racine (OK — 2026-03-14)
- Tous les `OT_*` précédemment à la racine ont été migrés vers :
  - `docs/ot/closings/`
  - `docs/ot/reports/`
  - `docs/ot/kanban/`
  - `docs/ot/trae/`
- Le legacy root est conservé uniquement pour traçabilité : `opt_trading_kanban_source_of_truth_2026-03-13_updated.md`.

### 3.3 Références non-OT repointées (OK — 2026-03-14)
- Les références documentaires non-OT prioritaires pointent désormais vers les chemins canoniques `docs/ot/*`.

### 3.4 Régularisations Trae stabilisées (OK — 2026-03-14)
Décisions canoniques produites :
- `trae_module_validator` : ACTIVE (FORMALISÉ)
  - décision : `docs/ot/trae/OT_TRAE_MODULE_VALIDATOR_STATUS_DECISION_01.md`
- Adoption socle Trae : CONFIRMÉ PARTIELLEMENT
  - décision : `docs/ot/trae/OT_TRAE_SOCLE_ADOPTION_DECISION_01.md`
- Runtime / snapshot repo : NON CONFIRMÉ MAIS ACCEPTÉ COMME INVARIANT DOCUMENTÉ
  - décision : `docs/ot/trae/OT_TRAE_RUNTIME_SNAPSHOT_ALIGNMENT_DECISION_01.md`

### 3.5 Bloc CONTRADICTOIRE cadré (OK — 2026-03-14)
- Cadrage canonique (repo-first + grandfathering standard/legacy + pas de normalisation implicite + V1 non automatique) :
  - décision : `docs/ot/trae/OT_TRAE_CONTRADICTOIRE_CADRAGE_DECISION_01.md`

### 3.6 Passe d'audit 2026-03-20 clôturée (OK — 2026-03-20)
- 8 périmètres qualifiés, 8 décisions PM figées.
- Protocole de convergence documentaire produit.
- Détail complet : `audit/2026-03-20/A4_audit_2026_03_20_formal_close.md`

---

## 4. Ce qu'il ne faut pas rouvrir dans la reprise

- Ne pas ouvrir automatiquement Rules/Agents/Skills/MCP (V1) sans sélection explicite.
- Ne pas "normaliser" (déplacer/refactor) les couches runtime ou legacy sans mission dédiée.
- Ne pas réactiver des missions `CLOSE` sans besoin prouvé.
- Ne pas recréer des OT_* à la racine du repo.
- Ne pas rouvrir les 8 décisions PM figées de la passe 2026-03-20 sans besoin PM explicite.
- Ne pas traiter `db-layer` comme un déploiement `opt-trading` (confirmé absent).
- Ne pas mélanger la machine `student` (runtime) et le workstream `student` (sous-projet intégré).

---

## 5. Points de reprise actifs

### 5.1 Chantiers issus de la passe 2026-03-20 (kanban maître `97_*`)

```
P1 — GO_STUDENT_LIVE_VALIDATION_PACK_01
     Statut    : LIVRÉ — pack prêt, validation live en attente
     Prérequis : SSH vers machine Linux cible où /opt/trading/student est déployé
     Action    : bash /opt/trading/student/validation/validate_student_live.sh

P2 — GO_ALGO_HF_DEEP_AUDIT_01
     Statut    : DIFFÉRÉ
     Prérequis : SSH db-layer (192.168.16.179) + GitHub algo_hf
```

Kanban de référence : `audit/2026-03-20/97_cross_project_master_kanban.md` §12

### 5.2 Chantiers Trae V1 internes (kanban Trae)

```
GO_OT_NEXT_MISSION_SELECTION_01
Point candidat logique : GO_OT_TRAE_RULES_V1_01
```

Kanban de référence : `docs/ot/kanban/opt_trading_kanban_source_of_truth.md`

---

## 6. Procédure de reprise

### 6a — Reprise Claude Cowork (chantier issu de la passe 2026-03-20)

```
Ordre de lecture obligatoire (conforme OT_TRAE_DOC_CONVERGENCE_PROTOCOL_V1 §2.2) :

1) Lire audit/2026-03-20/A4_audit_2026_03_20_formal_close.md   ← décisions figées
2) Lire audit/2026-03-20/97_cross_project_master_kanban.md      ← état courant des chantiers
3) Lire audit/2026-03-20/00_audit_master_index.md               ← localiser les livrables
4) Lire le document canonique du périmètre visé (92/93/94/A0/A1/...)
5) Appliquer le point de reprise §5.1

Outil de contrôle (cocher avant production) :
→ docs/ot/trae/OT_TRAE_DOC_CONVERGENCE_CHECKLIST_V1.md
```

### 6b — Reprise session Trae V1 (chantier interne GO_OT_*)

```
1) Lire docs/master_pack/00_current_state_and_standards.md
2) Lire la dernière clôture pertinente sous docs/ot/closings/
3) Lire le kanban + la synthèse :
   - docs/ot/kanban/opt_trading_kanban_source_of_truth.md
   - docs/ot/kanban/opt_trading_kanban_operational_summary_2026-03-14.md
4) Relire les décisions Trae (si mission liée) :
   - docs/ot/trae/OT_TRAE_*_DECISION_01.md
5) Appliquer le point de reprise §5.2
```

En cas de doute sur le track à suivre : lire `audit/2026-03-20/97_cross_project_master_kanban.md` §12 (point actif).
