# 20_INDEX_INSERTION_POLICY

## Safety rules
1. **--dry-run is the default**: no write happens without explicit `--apply`.
2. **Duplicate detection**: if an entry for the same GO_ID already exists in the index, `--apply` must refuse.
3. **Backup not required**: diff preview is sufficient before write.
4. **GO_INDEX.md not modified in this GO's PR**: the tool may be tested on a temporary copy only.

## Entry format
```
### GO_XXXX_XX
- repo : opt-trading
- type : <chantier type>
- statut : <entry-status>
- titre court : <short title from 1_MASTER_TARGET>
- dernier état connu : <summary>
- lien utile : `docs/chantiers/GO_XXXX_XX/00_INITIAL_PROJECT_DOC.md`
```

## Constraints
- Must not read or write outside `docs/` and test `tmp_path`.
- Must not modify workflows, runtime, modules, config, secrets.
- Must not modify `GO_INDEX.md` in the PR commit.
