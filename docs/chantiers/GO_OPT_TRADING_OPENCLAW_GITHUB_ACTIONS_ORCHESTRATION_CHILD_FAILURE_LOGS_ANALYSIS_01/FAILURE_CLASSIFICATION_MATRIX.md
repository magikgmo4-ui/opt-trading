# FAILURE_CLASSIFICATION_MATRIX

| Classification | Pattern Examples | Confidence | Next Action Example |
| :--- | :--- | :--- | :--- |
| **TEST_FAILURE** | `FAILED tests/`, `pytest`, `AssertionError` | High | Fix code or update tests. |
| **YAML_WORKFLOW_FAILURE** | `invalid workflow`, `yaml: line`, `syntax error` | High | Correct YAML syntax in `.github/workflows/`. |
| **PERMISSION_FAILURE** | `Permission denied`, `403`, `resource not accessible` | Medium | Check GITHUB_TOKEN permissions or secrets. |
| **TIMEOUT** | `timed_out`, `Job exceeded time limit` | High | Optimize job performance or increase timeout. |
| **MISSING_FILE** | `No such file`, `File not found`, `ENOENT` | Medium | Verify file existence or build artifact creation. |
| **FILE_SCOPE_FAILURE** | `FAIL: file outside GO scope`, `gate/file-scope` | High | Update `FILE_SCOPE.txt` for the current GO. |
| **NO_LOCK_OVERLAP_FAILURE** | `FAIL: changed file is also claimed`, `gate/no-lock-overlap` | High | Release scope from previous GO or resolve conflict. |
| **NETWORK_OR_API_FAILURE** | `Connection timeout`, `Rate limit exceeded`, `API error` | Medium | Retry later or check external service status. |
| **UNKNOWN_FAILURE** | No recognized pattern | Low | Human review of full logs required. |
