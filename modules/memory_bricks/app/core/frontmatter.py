from __future__ import annotations

import ast
import json


def dump_frontmatter(data: dict[str, object]) -> str:
    lines: list[str] = []
    for key, value in data.items():
        if isinstance(value, list):
            if not value:
                lines.append(f"{key}: []")
                continue
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {json.dumps(str(item), ensure_ascii=False)}")
            continue
        if value is None:
            value = ""
        lines.append(f"{key}: {json.dumps(str(value), ensure_ascii=False)}")
    return "\n".join(lines)


def parse_frontmatter(text: str) -> dict[str, object]:
    result: dict[str, object] = {}
    current_list_key: str | None = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line:
            continue
        if line.startswith("  - "):
            if current_list_key is None:
                raise ValueError(f"Invalid frontmatter list item: {raw_line}")
            result.setdefault(current_list_key, []).append(_parse_scalar(line[4:]))
            continue
        current_list_key = None
        if ":" not in line:
            raise ValueError(f"Invalid frontmatter line: {raw_line}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise ValueError(f"Invalid frontmatter key: {raw_line}")
        if not value:
            result[key] = []
            current_list_key = key
            continue
        result[key] = _parse_scalar(value)
    return result


def _parse_scalar(value: str) -> object:
    value = value.strip()
    if value == "[]":
        return []
    if value.startswith(("\"", "[", "{")):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return ast.literal_eval(value)
    return value
