# OPT-TRADING — REPRISE DE SESSION (CANONIQUE)

Date (America/Montreal) : 2026-03-14
Dernière mise à jour (America/Montreal) : 2026-04-11

## 1. Objet
Fichier canonique de continuité pour reprendre une session Trae sur `opt-trading` sans rouvrir de chantier technique.

## 2. Continuité active (lot en cours)
- **Besoin initial** : Néant / <à renseigner>
- **Objectif final visé** : Néant / <à renseigner>
- **Plan validé** : Néant / <à renseigner>
- **État établi / obtenu** : Néant / <à renseigner>
- **Gap restant** : Néant / <à renseigner>
- **Prochain GO** : Néant / GO_<...>
- **Fils / rôles (séparation explicite)** :
  - **Machine** : <...>
  - **IA** : <...>
  - **IDE** : <...>
  - **Repo / Produit** : `opt-trading`

## 3. Chemins canoniques (sources de vérité)
- Kanban (source of truth) : `docs/ot/kanban/opt_trading_kanban_source_of_truth.md`
- Synthèse kanban : `docs/ot/kanban/opt_trading_kanban_operational_summary_2026-03-14.md`
- Workflow (doctrine gated) : `workflow_ai/WORKFLOW.md`
- Workflow sync Trae↔Kanban : `workflow_ai/WORKFLOW_TRAE_KANBAN_SYNC_2026-03-14.md`
- Point d’entrée mission (starter pack) : `docs/master_pack/mission_starter_pack/00_mission_start_guide.md`
- Standards projet (current state) : `docs/master_pack/00_current_state_and_standards.md`
- OT Trae (décisions / matrices) : `docs/ot/trae/`

Legacy conservé (ne pas promouvoir) :
- `opt_trading_kanban_source_of_truth_2026-03-13_updated.md` (racine, legacy)

## 4. Ce qui est établi dans cette session
### 4.1 Canonicalisation docs OT (OK)
- Kanban canonique + synthèse en place.
- Workflow gated + sync en place.

### 4.2 Migration OT_* hors de la racine (OK)
- Tous les `OT_*` précédemment à la racine ont été migrés vers :
  - `docs/ot/closings/`
  - `docs/ot/reports/`
  - `docs/ot/kanban/`
  - `docs/ot/trae/`
- Le legacy root est conservé uniquement pour traçabilité : `opt_trading_kanban_source_of_truth_2026-03-13_updated.md`.

### 4.3 Références non-OT repointées (OK)
- Les références documentaires non-OT prioritaires pointent désormais vers les chemins canoniques `docs/ot/*`.

### 4.4 Régularisations Trae stabilisées (OK)
Décisions canoniques produites :
- `trae_module_validator` : ACTIVE (FORMALISÉ)  
  - décision : `docs/ot/trae/OT_TRAE_MODULE_VALIDATOR_STATUS_DECISION_01.md`
- Adoption socle Trae : CONFIRMÉ PARTIELLEMENT  
  - décision : `docs/ot/trae/OT_TRAE_SOCLE_ADOPTION_DECISION_01.md`
  - closing : `docs/ot/closings/OT_TRAE_SOCLE_ADOPTION_PROOF_01_CLOSING.txt`
- Runtime / snapshot repo : NON CONFIRMÉ MAIS ACCEPTÉ COMME INVARIANT DOCUMENTÉ  
  - décision : `docs/ot/trae/OT_TRAE_RUNTIME_SNAPSHOT_ALIGNMENT_DECISION_01.md`
  - closing : `docs/ot/closings/OT_TRAE_RUNTIME_SNAPSHOT_ALIGNMENT_CHECK_01_CLOSING.txt`

### 4.5 Bloc CONTRADICTOIRE cadré (OK)
- Cadrage canonique (repo-first + grandfathering standard/legacy + pas de normalisation implicite + V1 non automatique) :  
  - décision : `docs/ot/trae/OT_TRAE_CONTRADICTOIRE_CADRAGE_DECISION_01.md`
  - closing : `docs/ot/closings/OT_TRAE_CONTRADICTOIRE_CADRAGE_01_CLOSING.txt`

### 4.6 Trae pré‑V1 — closeout (OK)
- Statut global pré‑V1 acté : `PRE_V1_COHERENT_AVEC_DELTAS_FINAUX` (sans surpromesse `V1_READY`).
- Décision : `docs/ot/trae/OT_TRAE_PRE_V1_CLOSEOUT_STATUS_DECISION_01.md`
- Closing : `docs/ot/closings/OT_TRAE_PRE_V1_CLOSEOUT_01_CLOSING.txt`

### 4.7 Continuité Trae par défaut (OK)
- Décision : `docs/ot/trae/OT_TRAE_CONTINUATION_DEFAULT_DECISION_01.md`
- Closing : `docs/ot/closings/OT_TRAE_CONTINUATION_DEFAULT_DECISION_01_CLOSING.txt`

### 4.8 Gating GO/STOP — borne canonique (OK)
- Preuve opposable d’une pratique “GO/STOP à chaque Gate” : non démontrée doc-only.
- Borne canonique documentée : oui.
- Closing : `docs/ot/closings/OT_TRAE_STARTERPACK_GATING_PROOF_01_CLOSING.txt`

### 4.9 Rules V1 — ouverture explicite (OK)
- Décision : `docs/ot/trae/OT_TRAE_RULES_V1_OPEN_DECISION_01.md`
- Closing : `docs/ot/closings/OT_TRAE_RULES_V1_OPEN_01_CLOSING.txt`

### 4.10 Agents V1 — ouverture explicite (OK)
- Décision : `docs/ot/trae/OT_TRAE_AGENTS_V1_OPEN_DECISION_01.md`
- Closing : `docs/ot/closings/OT_TRAE_AGENTS_V1_OPEN_01_CLOSING.txt`

### 4.11 Skills V1 — ouverture explicite (OK)
- Décision : `docs/ot/trae/OT_TRAE_SKILLS_V1_OPEN_DECISION_01.md`
- Closing : `docs/ot/closings/OT_TRAE_SKILLS_V1_OPEN_01_CLOSING.txt`

## 5. Ce qu’il ne faut pas rouvrir dans la reprise
- Ne pas ouvrir automatiquement Rules/Agents/Skills/MCP (V1) sans sélection explicite.
- Ne pas “normaliser” (déplacer/refactor) les couches runtime ou legacy sans mission dédiée.
- Ne pas réactiver des missions `CLOSE` sans besoin prouvé.
- Ne pas recréer des OT_* à la racine du repo.

## 6. Point de reprise global
- Point de reprise actuel : `GO_OT_TRAE_MCP_POLICY_V1_OPEN_01`

## 7. Procédure de reprise (checklist minimaliste)
0) Renseigner / vérifier le bloc **Continuité active** (besoin, objectif final, plan validé, état établi/obtenu, gap, prochain GO, fils)
1) Lire `docs/master_pack/00_current_state_and_standards.md`
2) Lire la dernière clôture pertinente sous `docs/ot/closings/` (dont `OT_TRAE_PRE_V1_CLOSEOUT_01_CLOSING.txt` si mission Trae)
3) Lire le kanban + la synthèse :
   - `docs/ot/kanban/opt_trading_kanban_source_of_truth.md`
   - `docs/ot/kanban/opt_trading_kanban_operational_summary_2026-03-14.md`
4) Relire les décisions Trae (si mission liée) :
   - `docs/ot/trae/OT_TRAE_*_DECISION_01.md`
5) Appliquer le point de reprise : `GO_OT_TRAE_MCP_POLICY_V1_OPEN_01`
