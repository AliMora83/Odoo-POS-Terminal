"""
services/snapscan.py — SnapScan QR generation service (Phase 1).
Onboarding with SnapScan merchant API required before this is live.
"""

import logging

logger = logging.getLogger(__name__)


async def generate_qr(order_id: int, amount: float, payment_ref: str) -> dict:
    """
    Generate a SnapScan QR payload for the given order and amount.
    Requires SNAPSCAN_API_KEY and SNAPSCAN_MERCHANT_ID to be set.

    Returns a dict with qr_payload, qr_image_base64, payment_ref, expires_at.
    Raises NotImplementedError until merchant onboarding is complete.
    """
    # TODO: implement when SnapScan merchant onboarding is complete
    raise NotImplementedError(
        "SnapScan integration is not yet live. Merchant onboarding required."
    )
