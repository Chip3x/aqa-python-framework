import json
import random
import re
import string
from datetime import datetime, timedelta


def generate_random_string(length: int = 10, chars: str | None = None) -> str:
    """Generate random string.

    Args:
        length: String length.
        chars: Character set to use. Defaults to letters and digits.

    Returns:
        Random string.
    """
    if chars is None:
        chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))


def generate_random_email(domain: str = "test.com") -> str:
    """Generate random email address.

    Args:
        domain: Email domain.

    Returns:
        Random email address.
    """
    username = generate_random_string(8).lower()
    return f"{username}@{domain}"


def generate_random_phone(country_code: str = "+1") -> str:
    """Generate random phone number.

    Args:
        country_code: Phone country code.

    Returns:
        Random phone number.
    """
    number = "".join(random.choices(string.digits, k=10))
    return f"{country_code}{number}"


def get_timestamp() -> str:
    """Get current timestamp string.

    Returns:
        ISO format timestamp.
    """
    return datetime.utcnow().isoformat()


def get_future_date(days: int = 30) -> datetime:
    """Get future date.

    Args:
        days: Number of days from now.

    Returns:
        Future datetime.
    """
    return datetime.utcnow() + timedelta(days=days)


def get_past_date(days: int = 30) -> datetime:
    """Get past date.

    Args:
        days: Number of days ago.

    Returns:
        Past datetime.
    """
    return datetime.utcnow() - timedelta(days=days)


def mask_sensitive_data(data: str, visible_chars: int = 4) -> str:
    """Mask sensitive data for logging.

    Args:
        data: Data to mask.
        visible_chars: Number of visible characters at start.

    Returns:
        Masked string.
    """
    if len(data) <= visible_chars:
        return "*" * len(data)
    return data[:visible_chars] + "*" * (len(data) - visible_chars)


SENSITIVE_KEYS = {
    "password",
    "pass",
    "secret",
    "token",
    "jwt-token",
    "access_token",
    "refresh_token",
    "client_secret",
    "authorization",
    "api_key",
    "apikey",
}


def _mask_value(value: object) -> object:
    if isinstance(value, str):
        return mask_sensitive_data(value)
    return "***"


def sanitize_payload(payload: object) -> object:
    """Sanitize dict/list payloads for safe logging."""
    if isinstance(payload, dict):
        sanitized: dict[object, object] = {}
        for key, value in payload.items():
            key_str = str(key).lower()
            if key_str in SENSITIVE_KEYS:
                sanitized[key] = _mask_value(value)
            else:
                sanitized[key] = sanitize_payload(value)
        return sanitized
    if isinstance(payload, list):
        return [sanitize_payload(item) for item in payload]
    if isinstance(payload, tuple):
        return tuple(sanitize_payload(item) for item in payload)
    return payload


_JSON_KV_RE = re.compile(
    r'(?i)("?(?:access_token|refresh_token|token|jwt-token|password|client_secret|authorization)"?\s*[:=]\s*")([^"]+)(")'
)
_BEARER_RE = re.compile(r"(?i)(Bearer\s+)([A-Za-z0-9\-\._~\+\/]+=*)")


def sanitize_text(text: str) -> str:
    """Sanitize sensitive values inside free-form text."""
    try:
        parsed = json.loads(text)
    except Exception:
        parsed = None

    if parsed is not None:
        return json.dumps(sanitize_payload(parsed))

    def _mask_json_kv(match: re.Match[str]) -> str:
        return f"{match.group(1)}{mask_sensitive_data(match.group(2))}{match.group(3)}"

    sanitized = _JSON_KV_RE.sub(_mask_json_kv, text)
    sanitized = _BEARER_RE.sub(
        lambda m: f"{m.group(1)}{mask_sensitive_data(m.group(2))}", sanitized
    )
    return sanitized
