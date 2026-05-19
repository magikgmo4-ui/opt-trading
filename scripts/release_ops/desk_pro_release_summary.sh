# Desk Pro - Release Ops Summary
# Displays Git HEAD and recent tags

# Resolve root
if command -v readlink >/dev/null 2>&1; then
    SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
else
    SCRIPT_PATH="${BASH_SOURCE[0]}"
fi
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$ROOT_DIR" || exit 1

echo "=== Desk Pro Release Summary ==="
echo "Repo Root: $ROOT_DIR"
echo "Current Branch: $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'Unknown')"
echo "Current HEAD:   $(git rev-parse --short HEAD 2>/dev/null || echo 'Unknown')"
echo ""
echo "Recent Tags:"
git tag -n1 --sort=-v:refname | head -n 5 || echo "No tags found."
echo "================================"
