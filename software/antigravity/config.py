"""
config.py — Environment variable loading and startup validation.
All configuration is loaded once here. Import `settings` wherever needed.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # ── Odoo ──────────────────────────────────────────────────────────────────
    ODOO_BASE_URL: str = ""
    ODOO_DB: str = ""
    ODOO_USER: str = ""
    ODOO_PASSWORD: str = ""

    # ── SnapScan (Phase 1) ────────────────────────────────────────────────────
    SNAPSCAN_API_KEY: str = ""
    SNAPSCAN_MERCHANT_ID: str = ""

    # ── M-Pesa (Phase 2 stub — unused for now) ────────────────────────────────
    MPESA_API_KEY: str = ""
    MPESA_SHORT_CODE: str = ""

    # ── Shared secret (ESP32 ↔ Antigravity) ───────────────────────────────────
    API_SECRET_KEY: str = ""

    @model_validator(mode="after")
    def validate_required_odoo_vars(self) -> "Settings":
        required = {
            "ODOO_BASE_URL": self.ODOO_BASE_URL,
            "ODOO_DB": self.ODOO_DB,
            "ODOO_USER": self.ODOO_USER,
            "ODOO_PASSWORD": self.ODOO_PASSWORD,
        }
        missing = [k for k, v in required.items() if not v]
        if missing:
            raise ValueError(
                f"Antigravity startup failed — missing required environment variables: "
                f"{', '.join(missing)}. "
                f"Copy .env.example to .env and fill in the values."
            )
        return self

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
