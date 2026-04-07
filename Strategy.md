# Strategy Document: Antigravity Integration
**Project:** Odoo POS Terminal — Africa Edition
**Version:** 1.0 — 2026-03-28
**Author:** Ali Mora — Odoo Certified Developer
**Framework:** FastAPI (Antigravity)
**Host:** Hostinger VPS — namka.cloud

---

## 1. Antigravity's Role

Antigravity is the **sole middleware layer** between all hardware terminals and the Odoo backend. It owns:

- All Odoo API credentials (never exposed to hardware).
- All payment provider integrations (SnapScan, M-Pesa).
- Transaction validation and error handling.
- Offline queue processing (replaying ESP32-held transactions on reconnect).
- Future: transaction data pipeline for embedded finance (MCA).

The ESP32 knows one thing: the base URL of Antigravity. Nothing else.

---

## 2. Integration Architecture

```
ESP32                    Antigravity (FastAPI)           Odoo 17
  |                             |                           |
  |-- POST /terminal/order ---> |                           |
  |                             |-- JSON-RPC /web/dataset/--|
  |                             |   call_kw (pos.order)     |
  |                             |<-- order_id --------------|
  |<-- { status, order_id } ----|                           |
  |                             |                           |
  |-- POST /terminal/payment -->|                           |
  |                             |-- Generate QR (SnapScan) -|
  |<-- { qr_payload } ----------|                           |
  |                             |                           |
  |-- POST /terminal/confirm -->|                           |
  |                             |-- JSON-RPC pos.payment ---|
  |<-- { success } -------------|                           |
```

---

## 3. Endpoint Specifications

### 3.1 `POST /terminal/order`
**Purpose:** Create a new POS order in Odoo.

**Request body:**
```json
{
  "terminal_id": "string",
  "session_id": "int",
  "lines": [
    {
      "product_id": "int",
      "qty": "float",
      "price_unit": "float"
    }
  ]
}
```

**Response:**
```json
{
  "status": "ok",
  "order_id": "int",
  "order_ref": "string",
  "amount_total": "float"
}
```

**Odoo call (JSON-RPC):**
- Model: `pos.order`
- Method: `create`
- Fields: `session_id`, `lines` (as `pos.order.line`)

---

### 3.2 `POST /terminal/payment`
**Purpose:** Initiate payment — generate QR code for SnapScan or M-Pesa.

**Request body:**
```json
{
  "order_id": "int",
  "amount": "float",
  "method": "snapscan | mpesa"
}
```

**Response:**
```json
{
  "status": "ok",
  "qr_payload": "string",
  "qr_image_base64": "string",
  "payment_ref": "string",
  "expires_at": "ISO8601"
}
```

**Notes:**
- SnapScan QR is generated via SnapScan merchant API (onboarding required — Phase 1).
- M-Pesa QR is generated via Vodacom M-Pesa SA API (Phase 2 only).
- `expires_at` is returned so the ESP32 display can show a countdown timer.

---

### 3.3 `POST /terminal/confirm`
**Purpose:** Confirm payment received — close the POS order in Odoo.

**Request body:**
```json
{
  "order_id": "int",
  "payment_ref": "string",
  "amount_paid": "float"
}
```

**Response:**
```json
{
  "status": "ok",
  "receipt_ref": "string"
}
```

**Odoo call (JSON-RPC):**
- Model: `pos.payment`
- Method: `create`
- Then: `pos.order` → `action_pos_order_paid`

---

### 3.4 `POST /terminal/sync`
**Purpose:** Replay offline-queued transactions from ESP32 flash storage on reconnect.

**Request body:**
```json
{
  "terminal_id": "string",
  "queued_transactions": [
    {
      "local_ref": "string",
      "timestamp": "ISO8601",
      "order_payload": { },
      "payment_payload": { }
    }
  ]
}
```

**Response:**
```json
{
  "results": [
    { "local_ref": "string", "status": "ok | failed", "order_id": "int | null", "error": "string | null" }
  ]
}
```

**Notes:**
- Antigravity processes in FIFO order.
- Failed transactions are logged and returned — the ESP32 does not retry automatically.
- Idempotency: use `local_ref` as a deduplication key.

---

### 3.5 `GET /terminal/session`
**Purpose:** Fetch active Odoo POS session for this terminal.

**Query params:** `terminal_id`

**Response:**
```json
{
  "session_id": "int",
  "session_state": "opened | closing_control | closed",
  "currency": "ZAR",
  "cashier": "string"
}
```

---

### 3.6 `GET /health`
**Purpose:** Heartbeat — ESP32 polls this every 60s to track connectivity.

**Response:**
```json
{
  "status": "ok",
  "odoo_reachable": true,
  "timestamp": "ISO8601"
}
```

---

## 4. Odoo JSON-RPC Pattern

All Odoo calls use the standard `/web/dataset/call_kw` endpoint.

```python
import httpx

async def odoo_call(model: str, method: str, args: list, kwargs: dict):
    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "id": 1,
        "params": {
            "model": model,
            "method": method,
            "args": args,
            "kwargs": kwargs
        }
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{ODOO_BASE_URL}/web/dataset/call_kw",
            json=payload,
            headers={"Cookie": f"session_id={ODOO_SESSION_ID}"}
        )
    return r.json()["result"]
```

**Authentication:** Odoo session cookie obtained via `/web/session/authenticate` at startup. Refresh on 401.

---

## 5. Project Structure (Recommended)

```
antigravity/
├── main.py                  # FastAPI app entry point
├── config.py                # Env vars (Odoo URL, credentials, SnapScan key)
├── routers/
│   ├── terminal.py          # All /terminal/* endpoints
│   └── health.py            # /health
├── services/
│   ├── odoo.py              # JSON-RPC client wrapper
│   ├── snapscan.py          # SnapScan QR generation
│   └── mpesa.py             # M-Pesa integration (Phase 2 stub)
├── models/
│   ├── order.py             # Pydantic request/response models
│   └── payment.py
├── utils/
│   ├── queue.py             # Offline queue processing logic
│   └── idempotency.py       # Deduplication using local_ref
└── tests/
    ├── test_order.py
    └── test_odoo_mock.py    # Mock Odoo for unit tests
```

---

## 6. Build Sequence

Build in this order — each step is independently testable:

| Step | Task | Test |
|---|---|---|
| 1 | `/health` endpoint + Odoo connection | Hit `/health` → confirm `odoo_reachable: true` |
| 2 | `/terminal/session` | Fetch active POS session from Odoo |
| 3 | `/terminal/order` | Create real POS order in Odoo dev instance |
| 4 | `/terminal/confirm` (cash payment) | Close order — no QR needed yet |
| 5 | `/terminal/payment` (SnapScan QR) | Generate QR — display in Postman |
| 6 | `/terminal/sync` | Replay a batch of simulated offline transactions |
| 7 | ESP32 firmware integration | Replace Postman with real hardware calls |

---

## 7. Environment Variables

```env
ODOO_BASE_URL=https://your-odoo-instance.com
ODOO_DB=your_db_name
ODOO_USER=api_user@yourdomain.com
ODOO_PASSWORD=your_api_password

SNAPSCAN_API_KEY=
SNAPSCAN_MERCHANT_ID=

MPESA_API_KEY=          # Phase 2
MPESA_SHORT_CODE=       # Phase 2

API_SECRET_KEY=         # Shared secret between ESP32 and Antigravity
```

---

## 8. Security Rules

- All ESP32 ↔ Antigravity communication over HTTPS only.
- Requests authenticated with `X-Terminal-Key` header (shared secret per device).
- Odoo credentials never leave Antigravity.
- `local_ref` deduplication prevents double-posting offline queue replays.
- Rate limit all `/terminal/*` endpoints (e.g. 30 req/min per terminal).

---

## 9. Open Items for Antigravity

| Item | Priority | Notes |
|---|---|---|
| SnapScan merchant onboarding | High | Required before Phase 1 live payments |
| Odoo session refresh logic | High | Handle expired sessions gracefully |
| Idempotency store | Medium | Redis or simple SQLite for `local_ref` dedup |
| M-Pesa stub | Low | Scaffold now, implement Phase 2 |
| Logging + alerting | Medium | Structured logs (JSON) to VPS for debugging |
