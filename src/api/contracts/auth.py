from jsonschema import validate

JWT_TOKEN_SCHEMA: dict[str, object] = {
    "type": "object",
    "required": ["jwt-token"],
    "properties": {
        "jwt-token": {"type": "string", "minLength": 1},
    },
    "additionalProperties": True,
}


def validate_jwt_token_payload(payload: dict[str, object]) -> None:
    """Validate JWT token payload against schema."""
    validate(instance=payload, schema=JWT_TOKEN_SCHEMA)
