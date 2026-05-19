# Desk Pro - Verify Tag (Linux)
# Checks if a tag exists and displays its details

TAG="${1:-}"

if [ -z "$TAG" ]; then
    echo "Usage: $0 <tag_name>"
    echo "Example: $0 desk_pro_ops_v1.0"
    exit 1
fi

echo "=== Verifying Tag: $TAG ==="

# Ensure we have latest tags
echo "Fetching tags..."
git fetch --tags >/dev/null 2>&1 || echo "Warning: Fetch failed (offline?)"

if git rev-parse "$TAG" >/dev/null 2>&1; then
    echo "PASS: Tag '$TAG' exists locally."
    echo "----------------------------------------"
    git show "$TAG" --no-patch --format="%h %cd %s"
    echo "----------------------------------------"
else
    echo "FAIL: Tag '$TAG' not found."
    echo "Try: git fetch --tags"
    exit 1
fi

echo "Verification Complete."
