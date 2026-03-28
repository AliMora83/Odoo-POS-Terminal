"""
routers/terminal.py — All /terminal/* endpoints (Steps 2–6 stubs).
Each endpoint is stubbed with a 501 Not Implemented response.
Implement in build sequence order per Strategy.md Section 6.

Auth: All /terminal/* endpoints require X-Terminal-Key header.
"""

from fastapi import APIRouter, Header, HTTPException

router = APIRouter(prefix="/terminal", tags=["Terminal"])


def _verify_key(x_terminal_key: str | None) -> None:
    """Verify the shared terminal secret. Placeholder until config is wired."""
    if not x_terminal_key:
        raise HTTPException(status_code=401, detail="Missing X-Terminal-Key header.")
    # TODO: compare against settings.API_SECRET_KEY when Step 2 begins


@router.get("/session")
async def get_session(
    terminal_id: str,
    x_terminal_key: str | None = Header(default=None),
) -> dict:
    """Step 2 — Fetch active Odoo POS session. Not yet implemented."""
    _verify_key(x_terminal_key)
    raise HTTPException(status_code=501, detail="Not implemented — Step 2.")


@router.post("/order")
async def create_order(
    x_terminal_key: str | None = Header(default=None),
) -> dict:
    """Step 3 — Create POS order in Odoo. Not yet implemented."""
    _verify_key(x_terminal_key)
    raise HTTPException(status_code=501, detail="Not implemented — Step 3.")


@router.post("/confirm")
async def confirm_payment(
    x_terminal_key: str | None = Header(default=None),
) -> dict:
    """Step 4 — Close order (cash payment). Not yet implemented."""
    _verify_key(x_terminal_key)
    raise HTTPException(status_code=501, detail="Not implemented — Step 4.")


@router.post("/payment")
async def initiate_payment(
    x_terminal_key: str | None = Header(default=None),
) -> dict:
    """Step 5 — SnapScan QR generation. Not yet implemented."""
    _verify_key(x_terminal_key)
    raise HTTPException(status_code=501, detail="Not implemented — Step 5.")


@router.post("/sync")
async def sync_offline_queue(
    x_terminal_key: str | None = Header(default=None),
) -> dict:
    """Step 6 — Replay offline-queued transactions. Not yet implemented."""
    _verify_key(x_terminal_key)
    raise HTTPException(status_code=501, detail="Not implemented — Step 6.")
