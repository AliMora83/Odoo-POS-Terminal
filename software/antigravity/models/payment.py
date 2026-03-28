"""
models/payment.py — Pydantic models for payment requests and responses.
Used by POST /terminal/payment and POST /terminal/confirm (Steps 4–5).
"""

from typing import Literal
from pydantic import BaseModel, Field


class InitiatePaymentRequest(BaseModel):
    order_id: int
    amount: float = Field(..., gt=0)
    method: Literal["snapscan", "mpesa"]


class InitiatePaymentResponse(BaseModel):
    status: str
    qr_payload: str
    qr_image_base64: str
    payment_ref: str
    expires_at: str  # ISO8601


class ConfirmPaymentRequest(BaseModel):
    order_id: int
    payment_ref: str
    amount_paid: float = Field(..., gt=0)


class ConfirmPaymentResponse(BaseModel):
    status: str
    receipt_ref: str
