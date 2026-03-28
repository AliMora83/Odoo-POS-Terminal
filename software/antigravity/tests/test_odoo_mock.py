"""
tests/test_odoo_mock.py — Unit tests for GET /health using a mocked Odoo backend.

Tests:
1. odoo_reachable: true when Odoo mock returns a valid search_count result.
2. odoo_reachable: false when Odoo mock raises a connection error.
"""

import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient


# ── Patch config BEFORE importing main so startup validation doesn't fail ──────
import os
os.environ.setdefaults = lambda *a, **kw: None  # no-op if called

# Set required env vars before any import of config.py
os.environ["ODOO_BASE_URL"] = "http://mock-odoo"
os.environ["ODOO_DB"] = "mock_db"
os.environ["ODOO_USER"] = "mock@test.com"
os.environ["ODOO_PASSWORD"] = "mock_password"
os.environ["API_SECRET_KEY"] = "mock_secret"

from main import app  # noqa: E402  (must come after env vars are set)

client = TestClient(app)


# ── Test 1: Odoo reachable ─────────────────────────────────────────────────────
def test_health_odoo_reachable():
    """When Odoo returns a valid search_count (int), health reports odoo_reachable: true."""
    with patch("routers.health.odoo.call", new_callable=AsyncMock) as mock_call:
        mock_call.return_value = 5  # res.users search_count returns an int

        response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["odoo_reachable"] is True
    assert data["status"] == "ok"
    assert "timestamp" in data


# ── Test 2: Odoo unreachable ───────────────────────────────────────────────────
def test_health_odoo_unreachable():
    """When Odoo call raises a connection error, health reports odoo_reachable: false."""
    with patch("routers.health.odoo.call", new_callable=AsyncMock) as mock_call:
        mock_call.side_effect = RuntimeError("Connection refused")

        response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["odoo_reachable"] is False
    assert data["status"] == "degraded"
    assert "timestamp" in data
