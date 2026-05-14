"""Small fail-closed YAML subset parser for policy test inputs.

The validator intentionally avoids a network-installed YAML dependency. This
parser accepts the simple block YAML used by OpenClaw policy drafts and rejects
features that could hide structure, such as anchors, aliases, tabs, and complex
flow maps.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any


class PolicyParseError(ValueError):
    """Raised when the local policy YAML subset cannot be parsed safely."""


@dataclass(frozen=True)
class _Line:
    number: int
    indent: int
    text: str


_KEY_RE = re.compile(r"^[A-Za-z0-9_ .\-/]+$")


def parse_policy_yaml(text: str) -> Any:
    lines = _prepare_lines(text)
    if not lines:
        raise PolicyParseError("policy input is empty")
    parser = _Parser(lines)
    value, index = parser.parse_block(0, lines[0].indent)
    if index != len(lines):
        line = lines[index]
        raise PolicyParseError(f"unexpected content at line {line.number}")
    if not isinstance(value, dict):
        raise PolicyParseError("top-level YAML value must be a map")
    return value


def _prepare_lines(text: str) -> list[_Line]:
    prepared: list[_Line] = []
    for number, raw_line in enumerate(text.splitlines(), start=1):
        if "\t" in raw_line:
            raise PolicyParseError(f"tabs are not allowed at line {number}")
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("---") or stripped.startswith("..."):
            continue
        if stripped.startswith("&") or stripped.startswith("*"):
            raise PolicyParseError(f"anchors and aliases are not allowed at line {number}")
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        if indent % 2 != 0:
            raise PolicyParseError(f"indentation must use two-space steps at line {number}")
        prepared.append(_Line(number=number, indent=indent, text=stripped))
    return prepared


class _Parser:
    def __init__(self, lines: list[_Line]) -> None:
        self.lines = lines

    def parse_block(self, index: int, indent: int) -> tuple[Any, int]:
        if index >= len(self.lines):
            return {}, index
        line = self.lines[index]
        if line.indent < indent:
            return {}, index
        if line.indent != indent:
            raise PolicyParseError(f"unexpected indentation at line {line.number}")
        if line.text.startswith("- "):
            return self._parse_list(index, indent)
        return self._parse_map(index, indent)

    def _parse_map(self, index: int, indent: int) -> tuple[dict[str, Any], int]:
        result: dict[str, Any] = {}
        while index < len(self.lines):
            line = self.lines[index]
            if line.indent < indent:
                break
            if line.indent > indent:
                raise PolicyParseError(f"unexpected nested map line {line.number}")
            if line.text.startswith("- "):
                break
            key, raw_value = _split_key_value(line)
            if key in result:
                raise PolicyParseError(f"duplicate key at line {line.number}: {key}")
            if raw_value == "":
                next_index = index + 1
                if next_index >= len(self.lines) or self.lines[next_index].indent <= indent:
                    result[key] = {}
                    index = next_index
                    continue
                result[key], index = self.parse_block(next_index, self.lines[next_index].indent)
            else:
                result[key] = _parse_scalar(raw_value, line.number)
                index += 1
        return result, index

    def _parse_list(self, index: int, indent: int) -> tuple[list[Any], int]:
        result: list[Any] = []
        while index < len(self.lines):
            line = self.lines[index]
            if line.indent < indent:
                break
            if line.indent > indent:
                raise PolicyParseError(f"unexpected nested list line {line.number}")
            if not line.text.startswith("- "):
                break
            item_text = line.text[2:].strip()
            index += 1
            if item_text == "":
                if index >= len(self.lines) or self.lines[index].indent <= indent:
                    result.append({})
                    continue
                item, index = self.parse_block(index, self.lines[index].indent)
                result.append(item)
                continue
            if _looks_like_key_value(item_text):
                key, raw_value = _split_inline_key_value(item_text, line.number)
                item: dict[str, Any] = {}
                item[key] = {} if raw_value == "" else _parse_scalar(raw_value, line.number)
                if index < len(self.lines) and self.lines[index].indent > indent:
                    nested, index = self.parse_block(index, self.lines[index].indent)
                    if not isinstance(nested, dict):
                        raise PolicyParseError(f"list item mapping expected at line {line.number}")
                    for nested_key, nested_value in nested.items():
                        if nested_key in item:
                            raise PolicyParseError(
                                f"duplicate key in list item at line {line.number}: {nested_key}"
                            )
                        item[nested_key] = nested_value
                result.append(item)
                continue
            result.append(_parse_scalar(item_text, line.number))
        return result, index


def _split_key_value(line: _Line) -> tuple[str, str]:
    return _split_inline_key_value(line.text, line.number)


def _split_inline_key_value(text: str, line_number: int) -> tuple[str, str]:
    if ":" not in text:
        raise PolicyParseError(f"expected key/value pair at line {line_number}")
    key, raw_value = text.split(":", 1)
    key = key.strip()
    if not key or not _KEY_RE.match(key):
        raise PolicyParseError(f"unsupported key at line {line_number}")
    return key, raw_value.strip()


def _looks_like_key_value(text: str) -> bool:
    if ":" not in text:
        return False
    key = text.split(":", 1)[0].strip()
    return bool(key and _KEY_RE.match(key))


def _parse_scalar(raw_value: str, line_number: int) -> Any:
    value = _strip_inline_comment(raw_value).strip()
    if value == "":
        return ""
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered in {"null", "none", "~"}:
        return None
    if value == "{}":
        return {}
    if value == "[]":
        return []
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [_parse_scalar(part.strip(), line_number) for part in inner.split(",")]
    if value.startswith("{") or value.endswith("}"):
        raise PolicyParseError(f"flow maps are limited to empty maps at line {line_number}")
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?\d+\.\d+", value):
        return float(value)
    if "&" in value or value.startswith("*"):
        raise PolicyParseError(f"anchors and aliases are not allowed at line {line_number}")
    return value


def _strip_inline_comment(value: str) -> str:
    in_single = False
    in_double = False
    for index, char in enumerate(value):
        if char == "'" and not in_double:
            in_single = not in_single
        elif char == '"' and not in_single:
            in_double = not in_double
        elif char == "#" and not in_single and not in_double:
            if index == 0 or value[index - 1].isspace():
                return value[:index]
    return value
