# 02 — TEST_PLAN_REPO_KG

## 1_MASTER_TARGET

Valider concrètement, dans l'IDE, que le système Repo Knowledge Graph décrit dans le chantier parent peut être testé contre le repo réel `opt-trading`.

## 7_CANONICAL_STATE

- Branche de travail : `go/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01`
- Dossier chantier : `docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/`
- Surface `/bundles/` : absente
- Bundle IDE courant : `docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/ide_bundle/`

## 8_VALIDATED_PLAN

### TEST_01 — Repo baseline

But : prouver l'état Git réel avant test.

Commandes :

```bash
git status --short --branch
git branch -vv
git remote -v
```

Sortie attendue : état propre ou changements explicitement listés.

---

### TEST_02 — Docs du chantier parent

But : vérifier que les documents 01 à 13 existent.

Commandes :

```bash
ls -la docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01
find docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01 -maxdepth 2 -type f | sort
```

Sortie attendue : présence du cadrage, schema, producer, consumer, views, indexation gap, note `/bundles/`, bundle IDE.

---

### TEST_03 — GO_INDEX non corrompu

But : vérifier que `GO_INDEX.md` reste lisible et contient son tableau canonique.

Commandes :

```bash
grep -n "Tableau canonique des chantiers" docs/index/GO_INDEX.md
grep -n "| PARENT | CHANTIER | SOUS_CHANTIER | STATUT | DOSSIER_PRESENT | SOURCE |" docs/index/GO_INDEX.md
```

Sortie attendue : deux lignes trouvées.

---

### TEST_04 — Schema V1 lisible

But : vérifier que le contrat nodes/edges est présent.

Commandes :

```bash
grep -n "Types de nodes autorisés V1" docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/06_graph_schema_v1.md
grep -n "Types de edges autorisés V1" docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/06_graph_schema_v1.md
grep -n "Niveaux de confiance" docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/06_graph_schema_v1.md
```

Sortie attendue : trois preuves présentes.

---

### TEST_05 — Producer Spec lisible

But : vérifier que le pipeline Producer est exploitable.

Commandes :

```bash
grep -n "SCAN SOURCES" docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/07_producer_spec_v1.md
grep -n "BUILD NODES" docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/07_producer_spec_v1.md
grep -n "EXPORT" docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/07_producer_spec_v1.md
```

Sortie attendue : pipeline complet visible.

---

### TEST_06 — Consumer Ace KG lisible

But : vérifier que la méthode consumer est autonome.

Commandes :

```bash
grep -n "Ace KG" docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/08_consumer_ace_kg_method_v1.md
grep -n "Format d'entrée recommandé" docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/08_consumer_ace_kg_method_v1.md
grep -n "Prompt" docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/08_consumer_ace_kg_method_v1.md
```

Sortie attendue : usage ACE KG documenté.

---

### TEST_07 — Graph Views V1

But : vérifier que les 8 vues sont présentes.

Commandes :

```bash
for v in GO_MAP DOC_CANON_MAP MODULE_SURFACE_MAP MACHINE_RUNTIME_MAP BRANCH_WORK_MAP RESUME_MAP RISK_GAP_MAP PRODUCER_CONSUMER_MAP; do
  grep -n "$v" docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/09_graph_views_v1.md || exit 1
done
```

Sortie attendue : toutes les vues trouvées.

---

### TEST_08 — Bundle IDE autonome

But : vérifier que le bundle IDE contient ses fichiers attendus.

Commandes :

```bash
find docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/ide_bundle -maxdepth 1 -type f | sort
```

Sortie attendue : README, prompt, plan, checklist, outputs, notes.

## 17_RESUME_POINT

Après exécution, produire :

```text
docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/ide_bundle/REPORT_TESTS_ULTRA_CONCRETS.md
docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/ide_bundle/GAP_REPORT_TESTS_ULTRA_CONCRETS.md
```

## RISKS

- À qualifier.
