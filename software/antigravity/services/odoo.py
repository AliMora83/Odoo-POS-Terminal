"""
services/odoo.py — Async JSON-RPC client for Odoo.

Rules:
- This is the ONLY module that holds Odoo credentials.
- authenticate() must be called on startup before any other Odoo calls.
- call() refreshes the session automatically on 401.
- Never expose credentials or session cookies outside this module.
"""

import logging
from datetime import datetime, timezone

import httpx

from config import settings

logger = logging.getLogger(__name__)

# Module-level session state — this is internal to this service only.
_session_cookie: str = ""
_client: httpx.AsyncClient | None = None


def _get_client() -> httpx.AsyncClient:
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(timeout=10.0)
    return _client


async def authenticate() -> bool:
    """
    Authenticate against Odoo via /web/session/authenticate.
    Stores the session cookie for subsequent calls.
    Returns True on success, False on failure.
    """
    global _session_cookie
    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "id": 1,
        "params": {
            "db": settings.ODOO_DB,
            "login": settings.ODOO_USER,
            "password": settings.ODOO_PASSWORD,
        },
    }
    try:
        client = _get_client()
        response = await client.post(
            f"{settings.ODOO_BASE_URL}/web/session/authenticate",
            json=payload,
        )
        response.raise_for_status()
        data = response.json()

        # Odoo returns an error dict in result if credentials are wrong
        if data.get("error"):
            logger.error("Odoo authentication failed: %s", data["error"])
            return False

        # Extract session_id from Set-Cookie header
        session_id = response.cookies.get("session_id")
        if not session_id:
            logger.error("Odoo authentication succeeded but no session_id cookie returned.")
            return False

        _session_cookie = session_id
        logger.info("Odoo authentication successful. Session established.")
        return True

    except httpx.HTTPError as exc:
        logger.error("Odoo authentication HTTP error: %s", exc)
        return False
    except Exception as exc:
        logger.error("Odoo authentication unexpected error: %s", exc)
        return False


async def call(model: str, method: str, args: list, kwargs: dict | None = None) -> dict | list | None:
    """
    Call an Odoo model method via JSON-RPC /web/dataset/call_kw.
    Automatically re-authenticates once on 401.

    Args:
        model: Odoo model name e.g. "res.users"
        method: Method name e.g. "search_count"
        args: Positional arguments list
        kwargs: Keyword arguments dict

    Returns:
        The JSON-RPC "result" field, or raises RuntimeError on failure.
    """
    if kwargs is None:
        kwargs = {}

    result = await _call_raw(model, method, args, kwargs)

    # If None returned (e.g. 401), try re-auth once then retry
    if result is None:
        logger.warning("Odoo call failed — attempting re-authentication.")
        refreshed = await authenticate()
        if refreshed:
            result = await _call_raw(model, method, args, kwargs)
        if result is None:
            raise RuntimeError(f"Odoo call failed for {model}.{method} after session refresh.")

    return result


async def _call_raw(model: str, method: str, args: list, kwargs: dict) -> dict | list | None:
    """Internal: perform the raw JSON-RPC call. Returns None on transport/auth failure."""
    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "id": 1,
        "params": {
            "model": model,
            "method": method,
            "args": args,
            "kwargs": kwargs,
        },
    }
    try:
        client = _get_client()
        response = await client.post(
            f"{settings.ODOO_BASE_URL}/web/dataset/call_kw",
            json=payload,
            cookies={"session_id": _session_cookie},
        )

        if response.status_code == 401:
            logger.warning("Odoo returned 401 — session may have expired.")
            return None

        response.raise_for_status()
        data = response.json()

        if data.get("error"):
            logger.error("Odoo JSON-RPC error: %s", data["error"])
            return None

        return data.get("result")

    except httpx.HTTPError as exc:
        logger.error("Odoo HTTP error during call_kw: %s", exc)
        return None
