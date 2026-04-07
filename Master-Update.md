# Master Document: Rugged Odoo POS Terminal
**Project Name:** Odoo POS Customer Terminal (Africa Edition)
**Version:** 1.1 — Updated 2026-03-28
**Author:** Ali Mora — Odoo Certified Developer
**Target Market:** Mid-to-High Volume African Retailers (Coffee shops, pharmacies, franchises) & Current Odoo Users
**Core Value Proposition:** A decoupled, load-shedding-proof, Odoo-native hardware solution with a disruptive hybrid pricing model.

---

## 1. Technology Stack

### Hardware (On-Site Terminal)
| Component | Part | Role |
|---|---|---|
| Controller | ESP32-WROOM-32E | Main MCU — WiFi, task orchestration, offline queue |
| Display | 2.8" SPI TFT (ILI9341) | Customer-facing UI |
| NFC | PN532 Module | Tap-to-pay reader |
| Power | TP4056 IC + 18650 Li-Ion | UPS battery backup — load-shedding resilience |
| Enclosure (local) | Creality K1 Max — PETG/ABS | Printed in Pretoria |
| Enclosure (outsourced) | PCBWay — Turnkey PCBA | Carrier boards only. **PCBWay is the sole approved PCBA vendor.** |

### Middleware
- **Framework:** FastAPI (Antigravity)
- **Hosting:** Hostinger VPS — namka.cloud
- **Role:** Single source of truth between hardware and Odoo. All ESP32 calls terminate here. No direct hardware-to-Odoo communication permitted.

### Backend
- **ERP:** Odoo (POS module + Accounting module)
- **Integration method:** JSON-RPC via Antigravity
- **Odoo modules in scope:** Point of Sale, Accounting

### AI / Orchestration (Internal — not part of end product)
- **Gemini:** Used for internal brainstorming and project orchestration only. Not shipped in any production component.

---

## 2. System Architecture

```
[ESP32 Terminal]
    |
    | HTTPS / WiFi
    v
[Antigravity — FastAPI — namka.cloud]
    |                        |
    | JSON-RPC               | Payment QR / callback
    v                        v
[Odoo Backend]         [SnapScan / M-Pesa]
  - POS module
  - Accounting module
```

### Key architectural rules
1. The ESP32 never calls Odoo directly.
2. Antigravity is the only layer that holds Odoo API credentials.
3. The ESP32 queues transactions locally (flash storage) when offline and syncs on reconnect.
4. One payment method goes live at a time — SnapScan first, M-Pesa second.

---

## 3. ESP32 Firmware — Key Task Architecture

The firmware runs FreeRTOS with the following concurrent tasks:

| Task | Priority | Responsibility |
|---|---|---|
| `wifi_manager` | High | Connect, reconnect, signal status to other tasks |
| `api_client` | High | HTTP POST to Antigravity; retry with exponential backoff |
| `nfc_reader` | High | Poll PN532; parse NDEF/UID; trigger payment flow |
| `display_driver` | Medium | Render TFT screens via SPI (ILI9341) |
| `queue_manager` | Medium | Persist transactions to flash; sync when online |
| `battery_monitor` | Low | Read ADC; update display status bar; trigger low-power mode |

### Offline-first rule
If `wifi_manager` reports no connection, `api_client` hands the transaction to `queue_manager` for local storage. On reconnect, `queue_manager` replays the queue to Antigravity in FIFO order.

---

## 4. Unit Economics & Pricing Model

| Item | Value |
|---|---|
| Total Hardware BOM | ~$34.00 USD |
| Upfront Hardware Price | $150.00 USD |
| Monthly SaaS Fee | $50.00 USD / terminal |
| Transaction Fee | 1.0% flat |

**Year 1 merchant cost:** $150 + ($50 × 12) = $750
**Payback trigger:** TCO savings calculator must demonstrate payback within 3–4 months via transaction fee savings vs. competitors (2.75% baseline).

---

## 5. Business Model Canvas

### Value Propositions
- **Zero-Downtime:** Built-in battery handles Stage 6 grid failures; offline-first queue prevents data loss.
- **Radical Cost Savings:** 1% transaction fee saves high-volume merchants thousands annually.
- **Native Odoo Integration:** Hardware talks directly to the client's ERP — no third-party sync.
- **Mobile Money Ready:** Dynamic QR codes for SnapScan (Phase 1) and M-Pesa (Phase 2).

### Customer Segments
- Local retail franchises processing >$10k/month.
- Existing Odoo enterprise clients needing a modern customer-facing terminal.
- DIS (Digital Information Solutions) client base — official Odoo partner, warm pipeline.

### Channels & Sales
- Direct B2B outbound via TCO Savings Calculator.
- DIS partnership — leverage existing Odoo client relationships.
- Landing page: namka.cloud.

### Key Resources & Activities
- Odoo Developer Certification (held).
- Antigravity API development and maintenance.
- PCBWay supply chain management (PCBA) + SARS importer clearance.
- Local hardware assembly & QA (Pretoria).

---

## 6. Manufacturing & Supply Chain

- **Local assembly capacity:** 10 units/month.
- **PCBA vendor:** PCBWay only (turnkey). No alternative vendors approved.
- **PCB design tool:** EasyEDA (Gerber + BOM + CPL export).
- **Component sourcing preference:** LCSC via PCBWay catalog.
- **Sub-modules (LCD, NFC):** Female headers on carrier board — through-hole, assembled locally or by PCBWay depending on quote.
- **Initial prototype run:** 5 units.
- **First commercial batch:** 50 units (subject to pilot validation).

---

## 7. Prototype Milestone — "Hello Odoo" Sprint

**Goal:** Prove the full data path before touching hardware.

1. Spin up Odoo 17 dev instance (Docker).
2. Build one Antigravity endpoint: `POST /terminal/order` — takes `{amount, product_id}`, creates a real POS order via Odoo JSON-RPC.
3. Simulate the ESP32 with Python or Postman.
4. Confirm the order appears in Odoo POS back-office.

This single working loop (simulated hardware → Antigravity → real Odoo order) is the proof of concept. All hardware development follows.

---

## 8. Long-Term Vision — Embedded Finance (Phase 2)

Once hardware footprint is established and Antigravity transaction data is flowing:
- Integrate Banking-as-a-Service (BaaS) APIs.
- Offer Merchant Cash Advances (MCA) using proprietary transaction history.
- Next-day wallet settlements inside the client's Odoo dashboard.

---

## 9. Open Decisions / Risks

| Item | Status |
|---|---|
| Payment acquiring entity / PSP licence | Unresolved — required before live transaction processing |
| SnapScan merchant onboarding (Masterpass/PSP) | Not started |
| M-Pesa SA API agreement (Vodacom) | Not started — Phase 2 |
| Odoo version upgrade strategy | Needs versioning plan in Antigravity |
| SARS import duties on PCBWay batches | Lead time: 6–10 weeks — buffer stock required |
| PCBBasic (pcbasic.com) contact | Treat as potential phishing — do not respond until verified |
