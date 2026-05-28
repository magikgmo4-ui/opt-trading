# Implementation Spec

## Change
Introduce a tiny compat layer that imports real `pydantic` when available and falls back to a minimal `BaseModel` / `Field` shim when it is absent.

## Intended Use
- unblock local tests and module imports in lightweight environments
- preserve real `pydantic` behavior automatically when the dependency is installed
