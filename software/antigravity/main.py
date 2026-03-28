"""
main.py — Antigravity FastAPI application entry point.

Startup behaviour:
- Calls odoo.authenticate() and logs result.
- Includes health and terminal routers.

Error handling:
- Global exception handler catches unhandled errors.
- Never returns stack traces — logs server-side only.
"""

import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from routers import health, terminal
from services import odoo

# ── Logging setup ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("antigravity")


# ── Lifespan (replaces deprecated on_event) ────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Antigravity starting up...")
    authenticated = await odoo.authenticate()
    if authenticated:
        logger.info("Odoo session established successfully.")
    else:
        logger.warning(
            "Odoo authentication FAILED on startup. "
            "GET /health will report odoo_reachable: false until resolved."
        )
    yield
    logger.info("Antigravity shutting down.")


# ── App ────────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Antigravity",
    description="FastAPI middleware between ESP32 POS terminals and Odoo ERP.",
    version="0.1.0",
    lifespan=lifespan,
)

# ── Routers ────────────────────────────────────────────────────────────────────
app.include_router(health.router)
app.include_router(terminal.router)


# ── Global exception handler ───────────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(
        "Unhandled exception on %s %s: %s",
        request.method,
        request.url.path,
        exc,
        exc_info=True,
    )
    return JSONResponse(
        status_code=500,
        content={"error": "internal"},
    )
