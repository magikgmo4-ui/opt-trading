from modules.data_center.schemas.registry import get_schema


def validate_schema(blob: dict, schema_name: str) -> tuple[bool, list[str]]:
    spec = get_schema(schema_name)
    if spec is None:
        return False, [f"unknown schema: {schema_name}"]

    errors = []

    for field in spec["required_fields"]:
        if field not in blob or blob[field] is None:
            errors.append(f"missing required field: {field}")

    for field in spec["optional_fields"]:
        pass

    for field, expected_type in spec["field_types"].items():
        if field in blob and blob[field] is not None:
            val = blob[field]
            if isinstance(expected_type, tuple):
                if not isinstance(val, expected_type):
                    errors.append(
                        f"field '{field}' expected one of {expected_type}, got {type(val).__name__}"
                    )
            elif not isinstance(val, expected_type):
                errors.append(
                    f"field '{field}' expected {expected_type.__name__}, got {type(val).__name__}"
                )

    return len(errors) == 0, errors


def validate_blob(blob: dict) -> tuple[bool, list[str]]:
    schema_name = blob.get("schema", "")
    if not schema_name:
        return False, ["missing 'schema' field"]
    return validate_schema(blob, schema_name)
