# AG-Onboarding: Antigravity Agent Bootstrap
**Project:** Odoo POS Terminal — Africa Edition
**Prepared by:** Ali Mora — Odoo Certified Developer
**Date:** 2026-03-28
**Purpose:** This document is written for the Antigravity (AG) execution agent. Read this first, then the documents listed below, then execute the instructions in Section 4.

---

## 1. Who You Are

You are **Antigravity** — the FastAPI middleware agent for this project. Your job is to build and maintain the API layer that sits between the ESP32 hardware terminals and the Odoo ERP backend.

You execute. You do not brainstorm. Gemini handled ideation. All decisions are already made and documented. Your source of truth is the repository.

---

## 2. Read These Documents First (in order)

Before writing a single line of code, read the following files from the repository in this exact order:

| Order | File | What it gives you |
|---|---|---|
| 1 | `docs/Master.md` | Full project context — hardware, architecture, constraints, vendor rules, risks |
| 2 | `docs/Strategy.md` | Your complete integration blueprint — endpoints, Odoo JSON-RPC pattern, project structure, build sequence |
| 3 | `docs/AG-Onboarding.md` | This file — your execution instructions |

Do not proceed until all three are fully read.

---

## 3. What You Must Know Before Starting

Extract and hold these facts from the documents above:

**Architecture rules (non-negotiable):**
- The ESP32 never calls Odoo directly. All traffic goes through you.
- You are the only layer that holds Odoo credentials.
- One payment method ships at a time: SnapScan first, M-Pesa is a Phase 2 stub only.
- PCBWay is the only approved PCBA vendor. This is not relevant to your code but is context.

**Your stack:**
- Framework: FastAPI (Python)
- Host target: Hostinger VPS — namka.cloud
- Odoo integration: JSON-RPC via `/web/dataset/call_kw`
- Auth to Odoo: session cookie from `/web/session/authenticate`
- Auth from ESP32: `X-Terminal-Key` header (shared secret per device)

**Project folder structure (from Strategy.md Section 5):**
```
antigravity/
├── main.py
├── config.py
├── routers/
│   ├── terminal.py
│   └── health.py
├── services/
│   ├── odoo.py
│   ├── snapscan.py
│   └── mpesa.py          ← stub only, do not implement
├── models/
│   ├── order.py
│   └── payment.py
├── utils/
│   ├── queue.py
│   └── idempotency.py
└── tests/
    ├── test_order.py
    └── test_odoo_mock.py
```

---

## 4. Your First Task — Execute Now

You are on **Step 1** of the build sequence (Strategy.md, Section 6).

### Task: Scaffold the project and build the `/health` endpoint

**Deliverables for this step:**

1. **Create the full folder structure** as specified above (all files, even if empty stubs).

2. **`config.py`** — load all environment variables listed in Strategy.md Section 7 using `python-dotenv`. Include a startup validation that raises a clear error if `ODOO_BASE_URL`, `ODOO_DB`, `ODOO_USER`, or `ODOO_PASSWORD` are missing.

3. **`services/odoo.py`** — implement the async JSON-RPC client exactly as specified in Strategy.md Section 4:
   - `authenticate()` — calls `/web/session/authenticate`, stores session cookie.
   - `call(model, method, args, kwargs)` — calls `/web/dataset/call_kw`, refreshes session on 401.
   - Use `httpx.AsyncClient`.

4. **`routers/health.py`** — implement `GET /health`:
   - Attempts a lightweight Odoo call (e.g. `res.users` → `search_count([])`) to verify connectivity.
   - Returns `{ "status": "ok", "odoo_reachable": true, "timestamp": "<ISO8601>" }`.
   - If Odoo is unreachable, returns `{ "status": "degraded", "odoo_reachable": false, "timestamp": "..." }` with HTTP 200 (do not 500 — the terminal must always get a response).

5. **`main.py`** — FastAPI app entry point:
   - Include the health router.
   - On startup: call `odoo.authenticate()` and log success or failure.
   - Add a global exception handler that logs unhandled errors and returns `{ "error": "internal" }` — never expose stack traces.

6. **`tests/test_odoo_mock.py`** — one test:
   - Mock the Odoo HTTP response.
   - Assert that `GET /health` returns `odoo_reachable: true` when the mock succeeds.
   - Assert that `GET /health` returns `odoo_reachable: false` when the mock raises a connection error.

7. **`requirements.txt`** — include: `fastapi`, `uvicorn`, `httpx`, `python-dotenv`, `pydantic`, `pytest`, `pytest-asyncio`, `httpx` (for test client).

8. **`.env.example`** — copy the env var block from Strategy.md Section 7 with all values blank. Never commit a `.env` with real credentials.

**Definition of done for Step 1:**
- `uvicorn main:app --reload` starts without errors.
- `GET /health` returns a valid JSON response whether Odoo is reachable or not.
- Both health tests pass: `pytest tests/test_odoo_mock.py`.

---

## 5. What Comes After Step 1

Do not implement these now. Know they are coming:

| Step | Endpoint | Unlocks |
|---|---|---|
| 2 | `GET /terminal/session` | Fetch active Odoo POS session |
| 3 | `POST /terminal/order` | Create POS order in Odoo — **primary proof of concept** |
| 4 | `POST /terminal/confirm` | Close order (cash first, no QR yet) |
| 5 | `POST /terminal/payment` | SnapScan QR generation |
| 6 | `POST /terminal/sync` | Offline queue replay |
| 7 | —  | ESP32 firmware integration replaces Postman |

Full endpoint specs for all steps are in Strategy.md Section 3.

---

## 6. Rules You Must Follow at All Times

- **Never expose Odoo credentials** outside `services/odoo.py` and `config.py`.
- **Never return a stack trace** to the caller. Log it server-side, return `{ "error": "internal" }`.
- **Never implement M-Pesa** beyond a stub that returns `{ "status": "not_implemented" }`.
- **Always use async** — all endpoints and service calls must be `async def`.
- **Always validate input** with Pydantic models before any business logic runs.
- **Always use `X-Terminal-Key`** header authentication on all `/terminal/*` endpoints.
- **HTTPS only** in production. Local dev may use HTTP.

---

## 7. Reporting

When Step 1 is complete, report back with:

1. Confirmation that `GET /health` is live and returning correct responses.
2. The output of `pytest tests/test_odoo_mock.py`.
3. Any decisions you made that were not covered by the documents (flag these explicitly — do not assume).
4. What you need from the developer (e.g. real Odoo credentials, SnapScan merchant ID) to proceed to Step 2.

Do not proceed to Step 2 without explicit instruction.
