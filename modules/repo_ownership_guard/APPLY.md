# APPLY — repo_ownership_guard v1

## 1) Scan (read-only)
```bash
bash scripts/repo_ownership_guard_sanity.sh
```

## 2) Fix (si le scan montre des problèmes)
Dry-run:
```bash
bash scripts/repo_ownership_guard_cmd.sh fix --dry-run
```

Apply:
```bash
bash scripts/repo_ownership_guard_cmd.sh fix
```
