"""
routers/health.py — GET /health endpoint.

Logic:
- Attempts a lightweight Odoo call (res.users search_count) to verify connectivity.
- Always returns HTTP 200 — the ESP32 must always receive a response.
- odoo_reachable: true  → Odoo is up and session is valid.
- odoo_reachable: false → Odoo is unreachable or session failed; status = "degraded".
"""

import logging
from datetime import datetime, timezone

from fastapi import APIRouter

from services import odoo

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health", tags=["Health"])
async def health_check() -> dict:
    timestamp = datetime.now(timezone.utc).isoformat()
    try:
        # Lightweight call: count res.users records — just proves connectivity
        result = await odoo.call(
            model="res.users",
            method="search_count",
            args=[[]],
        )
        # result should be an int >= 0
        odoo_reachable = isinstance(result, (int, float)) and result >= 0
    except Exception as exc:
        logger.warning("Health check: Odoo unreachable — %s", exc)
        odoo_reachable = False

    if odoo_reachable:
        return {"status": "ok", "odoo_reachable": True, "timestamp": timestamp}
    else:
        return {"status": "degraded", "odoo_reachable": False, "timestamp": timestamp}
