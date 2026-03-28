"""
models/order.py — Pydantic models for POS order requests and responses.
Used by POST /terminal/order (Step 3).
Defined now so the complete data shapes are locked in early.
"""

from pydantic import BaseModel, Field


class OrderLine(BaseModel):
    product_id: int = Field(..., description="Odoo product.product ID")
    qty: float = Field(..., gt=0, description="Quantity — must be positive")
    price_unit: float = Field(..., ge=0, description="Unit price in ZAR")


class CreateOrderRequest(BaseModel):
    terminal_id: str = Field(..., description="Unique terminal identifier")
    session_id: int = Field(..., description="Active Odoo POS session ID")
    lines: list[OrderLine] = Field(..., min_length=1, description="At least one order line required")


class CreateOrderResponse(BaseModel):
    status: str
    order_id: int
    order_ref: str
    amount_total: float
