from collections.abc import Callable

from src.utils.logger import logger


class TestDataManager:
    """Manage cleanup actions for test data."""

    def __init__(self) -> None:
        self._cleanup_stack: list[Callable[[], None]] = []

    def register_cleanup(self, action: Callable[[], None]) -> None:
        """Register cleanup action (LIFO)."""
        self._cleanup_stack.append(action)

    def cleanup_all(self) -> None:
        """Execute all cleanup actions in reverse order."""
        while self._cleanup_stack:
            action = self._cleanup_stack.pop()
            try:
                action()
            except Exception as exc:
                logger.warning(f"Cleanup failed: {exc}")
