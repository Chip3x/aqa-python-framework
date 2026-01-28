import random
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
