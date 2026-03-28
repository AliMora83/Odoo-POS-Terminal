"""
utils/idempotency.py — Deduplication using local_ref keys (Step 6).
Prevents double-posting when the ESP32 replays the offline queue.
"""

# In-memory store for dev/testing. Replace with Redis or SQLite for production.
_processed_refs: set[str] = set()


def is_already_processed(local_ref: str) -> bool:
    """Return True if this local_ref has already been processed."""
    return local_ref in _processed_refs


def mark_as_processed(local_ref: str) -> None:
    """Record that this local_ref has been successfully processed."""
    _processed_refs.add(local_ref)
