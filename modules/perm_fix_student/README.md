# perm_fix_student — Fix permissions (journal) + test Ollama API

## Objectif
- Corriger: "some journal files were not opened due to insufficient permissions"
- Ajouter un test rapide de **Ollama + API** (endpoint 127.0.0.1:11434)

## Installation (sur student)
1) Uploade ce zip sur `/srv/sftp/shared_files/shared/` (ou où tu veux)
2) Puis:

```bash
unzip perm_fix_student_bundle.zip -d /tmp/pfs
sudo bash /tmp/pfs/APPLY.sh
sanity-perm_fix_student
menu-perm_fix_student
```

## Commandes
- Fix journal (par défaut): `cmd-perm_fix_student fix_journal`
- Fix tout /opt/trading (optionnel): `cmd-perm_fix_student fix_all`
- Test Ollama + API: `cmd-perm_fix_student ollama_test`
