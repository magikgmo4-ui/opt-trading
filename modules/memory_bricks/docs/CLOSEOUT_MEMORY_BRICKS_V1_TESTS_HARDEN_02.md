# CLOSEOUT MEMORY_BRICKS V1 TESTS HARDEN 02

- etat de depart: module deja PASS sur `GO_MEMORY_BRICKS_V1_IMPL_HARDEN_01`, 4 tests `unittest` et sanity OK
- fragilites traitees: erreurs CLI brutes, dataset vide pour `export/merge/handoff`, couverture manquante sur frontmatter invalide, brick absente, doublon de fichiers, valeurs invalides, dataset incoherent
- hardening applique: messages `ERROR:` minimaux cote CLI, garde-fous sur IDs vides, tests limites supplementaires sans changer le perimetre V1
- validations attendues: `python3 -m unittest discover -s modules/memory_bricks/tests -p "test_*.py" -v` et `bash modules/memory_bricks/scripts/sanity_check.sh`
- point de reprise naturel: `GO_MEMORY_BRICKS_V1_CLOSEOUT_03`
