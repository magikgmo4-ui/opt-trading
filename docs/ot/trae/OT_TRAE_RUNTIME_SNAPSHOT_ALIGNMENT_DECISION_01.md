# GO_OT_TRAE_RUNTIME_SNAPSHOT_ALIGNMENT_CHECK_01 — DÉCISION CANONIQUE (ALIGNEMENT RUNTIME / SNAPSHOT REPO)

Date (America/Montreal) : 2026-03-14

## 1. Objet
Régulariser le statut canonique de l’alignement runtime / snapshot repo pour `opt-trading`, sans forcer artificiellement la formule “alignement exact” si les sources prouvent des divergences structurelles acceptées ou suivies.

## 2. Définitions retenues
- Aligné : le snapshot repo (docs/registry/module) est cohérent avec une preuve runtime récente, ou ne prétend pas couvrir ce périmètre.
- Divergent mais documenté / toléré : divergence prouvée, explicitement enregistrée dans une matrice ou une note de gel, avec une action canonique (“GELÉ”, “EXCEPTION”, “VALIDE”, “ne pas toucher”, etc.).
- Divergent non toléré : divergence prouvée qui contredit une règle opposable (ex. wrappers non déclarés en registry) ou qui n’est pas suivie comme dette documentée (absence de mapping/justification).

## 3. Matrice minimale des écarts prouvés (repo vs runtime)

| Élément | Repo / doc attendue | Runtime prouvé | Statut | Preuves |
|---|---|---|---|---|
| Student AI | runtime actif = `scripts/student/` (module `deepseek_student` incomplet) | Divergence structurelle (runtime ≠ module) | Divergent mais documenté / toléré (GELÉ) | `docs/master_pack/00_current_state_and_standards.md`, `docs/ot/trae/OT_OPS_05_RUNTIME_EXCEPTION_MATRIX.md` |
| Reseau SSH | runtime actif = `scripts/reseau_ssh/` | Divergence structurelle (runtime ≠ module) | Divergent mais documenté / toléré (EXCEPTION) | `docs/master_pack/00_current_state_and_standards.md`, `docs/ot/trae/OT_OPS_05_RUNTIME_EXCEPTION_MATRIX.md` |
| desk_retention.timer (fréquence) | repo = “10min” | live admin-trading = “daily 03:00” | Divergent mais documenté / toléré (override live) | `docs/ot/trae/OT_SVC_01_CANONICAL_RUNTIME_MAP.md`, `docs/ot/reports/OT_LIVE_01_REPORT.md`, `docs/ot/closings/OT_LIVE_01_CLOSING.txt` |
| shared_sshfs_permanent (wrappers) | wrappers attendus symlink-safe | bug symlink prouvé puis recheck PASS | Divergent mais documenté / toléré (écart fermé sur wrappers, réserve maintenue sur service/mount) | `docs/ot/closings/OT_PATCH_SSHFS_01_CLOSING.txt`, `docs/ot/closings/OT_RECHECK_SSHFS_01_CLOSING.txt`, `docs/ot/trae/OT_SVC_01_CANONICAL_RUNTIME_MAP.md` |
| Wrappers vs registry (ex. perf_engine) | règle : tout wrapper doit être déclaré | `cmd-perf_engine` prouvé live alors que non déclaré en registry dans le snapshot | Divergent non toléré (gouvernance) | `docs/ot/reports/OT_LIVE_01_REPORT.md`, `docs/master_pack/00_current_state_and_standards.md`, `registry/wrappers_registry.yaml` |
| Services tv-webhook / tv-bitget-runner | runtime map OT_SVC_01 ne les cartographie pas | services actifs observés (snapshot infra) | Divergent non toléré (doc incomplète sur ce périmètre) | `infra_context_sanitized/.../snapshot_2026-02-26...txt`, `docs/ot/trae/OT_SVC_01_CANONICAL_RUNTIME_MAP.md` |

## 4. Verdict canonique
VERDICT = NON CONFIRMÉ MAIS ACCEPTÉ COMME INVARIANT DOCUMENTÉ

## 5. Justification
- L’“alignement exact” est contredit par des divergences prouvées (fréquences live, services présents hors cartographie, écarts registry vs live).
- Le modèle documentaire du projet est explicitement “runtime = source de vérité finale” et les divergences structurelles sont déjà traitées par matrices/note de gel.
- L’invariant canonique retenu n’est pas “zéro divergence”, mais “divergences suivies, classifiées, et opposables”.

## 6. Point de reprise
- Suite recommandée : `GO_OT_TRAE_CONTRADICTOIRE_CADRAGE_01` (cadrer le bloc CONTRADICTOIRE, sans ouvrir la V1).
