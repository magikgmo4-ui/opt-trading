# UI URLs — Source of Truth

## Access from db-layer / MSI (wg-mgmt)
- Perf UI: http://10.66.66.1:8010/perf/ui
- Desk Pro UI: http://10.66.66.1:8010/desk/ui
- Desk Pro Toolbox UI: http://10.66.66.1:8010/desk/toolbox

## Notes
- `curl -I` (HEAD) may return **405 Method Not Allowed**. Use GET:
  - `curl http://10.66.66.1:8010/perf/ui`
- Port `8000` is `tv-webhook` (Swagger docs), not the UI host.
- Port `8501` is not used in this stack.
