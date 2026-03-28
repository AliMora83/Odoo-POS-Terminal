# 🎯 Odoo POS Terminal – AI-Assisted Development

> **Template Version:** 1.0 | **Last Updated:** 2026-03-28 | **Owner:** Ali Mora
> **Mission Control:** [https://github.com/AliMora83/Namka-Mission-Control/blob/main/Master.md](https://github.com/AliMora83/Namka-Mission-Control/blob/main/Master.md)

---

## 📖 How to Use This File

**For Ali:** This is the single source of truth for the Odoo POS Terminal project. Keep the **Current Goal**, **Project Metadata**, and **Decision Log** up to date after each session.

**For AI Agents:** Before starting work on this project:
1. Read this `Master.md` file first
2. Check the **AI Reviews & Artifacts** section for existing architectural decisions
3. Follow the **Multi-Agent Context Protocol (MACP)** below
4. Commit your review to this file when done

---

## 🚀 Project Overview

**Description:** A decoupled, load-shedding-proof, Odoo-native customer-facing POS terminal built on ESP32 hardware — targeted at mid-to-high volume African retailers (coffee shops, pharmacies, franchises) who are existing Odoo users.

**Status:** In Progress

**Priority:** Priority 1 - Ship Now

**Stack:** ESP32 (FreeRTOS) / FastAPI (Antigravity) / Odoo JSON-RPC / Python / EasyEDA / PCBWay PCBA

**Repo:** [https://github.com/AliMora83/Odoo-POS-Terminal](https://github.com/AliMora83/Odoo-POS-Terminal)

**Live URL:** [https://namka.cloud](https://namka.cloud) _(middleware landing + API host)_

**AI Model Assigned:** Gemini _(internal orchestration only — not shipped in production)_

---

## 🎯 Current Goal

**Next Milestone:** Complete "Hello Odoo" Sprint — prove the full data path before touching hardware.

**Next Step:** Build Antigravity endpoint `POST /terminal/order` → simulate ESP32 with Python/Postman → confirm POS order appears in Odoo back-office.

**Blocker:** Payment acquiring entity / PSP licence unresolved — required before live transaction processing.

**Effort Estimate:** M

**Progress:** 20%

---

## 🏗 Tech Stack & Dependencies

### Hardware (On-Site Terminal)
| Component | Part | Role |
|---|---|---|
| Controller | ESP32-WROOM-32E | Main MCU — WiFi, task orchestration, offline queue |
| Display | 2.8″ SPI TFT (ILI9341) | Customer-facing UI |
| NFC | PN532 Module | Tap-to-pay reader |
| Power | TP4056 IC + 18650 Li-Ion | UPS battery backup — load-shedding resilience |
| Enclosure (local) | Creality K1 Max — PETG/ABS | Printed in Pretoria |
| Enclosure (outsourced) | PCBWay — Turnkey PCBA | Carrier boards only. **PCBWay is the sole approved PCBA vendor.** |

### Software Stack
- **Firmware:** C / FreeRTOS on ESP32
- **Middleware:** FastAPI (Antigravity) — hosted on Hostinger VPS (namka.cloud)
- **Backend ERP:** Odoo — POS module + Accounting module
- **Integration:** JSON-RPC via Antigravity (no direct ESP32 ↔ Odoo communication)
- **PCB Design:** EasyEDA (Gerber + BOM + CPL export)
- **Component Sourcing:** LCSC via PCBWay catalog
- **APIs:** SnapScan (Phase 1), M-Pesa (Phase 2), Banking-as-a-Service (Phase 3)

---

## 🏛 System Architecture

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

### Key Architectural Rules
1. The ESP32 **never** calls Odoo directly.
2. Antigravity is the **only** layer that holds Odoo API credentials.
3. The ESP32 queues transactions locally (flash storage) when offline and syncs on reconnect (FIFO).
4. One payment method goes live at a time — SnapScan first, M-Pesa second.

---

## ⚙️ ESP32 Firmware — FreeRTOS Task Architecture

| Task | Priority | Responsibility |
|---|---|---|
| `wifi_manager` | High | Connect, reconnect, signal status to other tasks |
| `api_client` | High | HTTP POST to Antigravity; retry with exponential backoff |
| `nfc_reader` | High | Poll PN532; parse NDEF/UID; trigger payment flow |
| `display_driver` | Medium | Render TFT screens via SPI (ILI9341) |
| `queue_manager` | Medium | Persist transactions to flash; sync when online |
| `battery_monitor` | Low | Read ADC; update display status bar; trigger low-power mode |

**Offline-first rule:** If `wifi_manager` reports no connection, `api_client` hands the transaction to `queue_manager`. On reconnect, `queue_manager` replays the queue to Antigravity in FIFO order.

---

## 💰 Unit Economics & Pricing Model

| Item | Value |
|---|---|
| Total Hardware BOM | ~$34.00 USD |
| Upfront Hardware Price | $150.00 USD |
| Monthly SaaS Fee | $50.00 USD / terminal |
| Transaction Fee | 1.0% flat |

**Year 1 merchant cost:** $150 + ($50 × 12) = $750
**Payback trigger:** TCO savings calculator must demonstrate payback within 3–4 months vs. competitors (2.75% baseline).

---

## 🏢 Business Model Canvas

### Value Propositions
- **Zero-Downtime:** Built-in battery handles Stage 6 load shedding; offline-first queue prevents data loss.
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

## 🏭 Manufacturing & Supply Chain

- **Local assembly capacity:** 10 units/month
- **PCBA vendor:** PCBWay only (turnkey). No alternative vendors approved.
- **PCB design tool:** EasyEDA (Gerber + BOM + CPL export)
- **Component sourcing preference:** LCSC via PCBWay catalog
- **Sub-modules (LCD, NFC):** Female headers on carrier board — through-hole, assembled locally or by PCBWay depending on quote
- **Initial prototype run:** 5 units
- **First commercial batch:** 50 units (subject to pilot validation)

> ⚠️ **PCBBasic (pcbasic.com) contact:** Treat as potential phishing — do not respond until verified.

---

## 🔭 Long-Term Vision — Embedded Finance (Phase 2+)

Once hardware footprint is established and Antigravity transaction data is flowing:
- Integrate Banking-as-a-Service (BaaS) APIs.
- Offer Merchant Cash Advances (MCA) using proprietary transaction history.
- Next-day wallet settlements inside the client's Odoo dashboard.

---

## 🤖 Multi-Agent Context Protocol (MACP)

> **Critical:** All agents must follow this protocol to prevent hallucinations and ensure coordination.

### Workflow for AI Agents

1. **Read Master.md first** — Check the **AI Reviews & Artifacts** section below for existing decisions.
2. **Review consensus states:**
   - `Unreviewed` → No agent has reviewed this yet
   - `Agent Reviewed` → One agent has reviewed (needs cross-check)
   - `Cross-Checked` → Two agents agree (pending Ali's ratification)
   - `Ratified` → **Locked truth** — do not re-architect without Ali's explicit approval
3. **Document your work:**
   - After completing a task or reviewing architecture, add an entry to **AI Reviews & Artifacts**
   - Commit the update to this `Master.md` file
   - Mark the entry as `Agent Reviewed`
4. **Cross-check other agents' work:**
   - If you see an `Agent Reviewed` entry, read it and either confirm or flag disagreements
   - Update the status to `Cross-Checked` if you agree
   - If you disagree, add your conflicting review and mark it `Needs Resolution`

---

## 🤖 AI Reviews & Artifacts

> This section is the shared context layer for all AI agents working on this project.
> Before starting work, read the relevant entries here to understand existing architectural decisions.

### Review Entry Format

```markdown
---

### YYYY-MM-DD — [Task/Feature Name] ([Agent Name] / [Provider])

**Status:** `[Unreviewed / Agent Reviewed / Cross-Checked / Ratified]`
**Reviewed by:** [Agent Name] ([Provider])
**Scope:** [Brief description of what was reviewed/built]

#### Key Decisions

- [Decision 1]
- [Decision 2]

#### Implementation Notes

[Any code snippets, architecture diagrams, or important technical details]

#### Next Step

[What the next agent should do, or what needs Ali's approval]

---

> 🔁 **Next:** [Agent name] to cross-check and mark as `Ratified`, or Ali to approve.
```

---

### 2026-03-28 — Initial Architecture & Master.md Reformat (Perplexity / Anthropic)

**Status:** `Agent Reviewed` — pending cross-check
**Reviewed by:** Perplexity (Anthropic)
**Scope:** Reformatted existing Master Document (v1.1) into Template-Master format. All existing content preserved and migrated into structured sections.

#### Key Decisions

1. `docs/Master.md` is the canonical project file — no content was changed, only structure applied.
2. System architecture rules (no direct ESP32 ↔ Odoo) preserved as `Ratified` constraints.
3. PCBWay sole-vendor rule and PCBBasic phishing warning preserved verbatim.
4. Gemini scoped to internal orchestration only — not part of any production component.

#### Next Step

Ali to review reformatted structure, then assign next development sprint (recommend "Hello Odoo" Sprint as first task).

---

> 🔁 **Next:** Ali to ratify structure, or next agent to cross-check and mark as `Ratified`.

---

## 📡 Integration with Mission Control

This project is tracked in **Mission Control** (the central hub for all Ali's projects).

- **Mission Control Master.md:** [https://github.com/AliMora83/Namka-Mission-Control/blob/main/Master.md](https://github.com/AliMora83/Namka-Mission-Control/blob/main/Master.md)
- **Live Dashboard:** `http://localhost:3000` _(when Mission Control is running)_

### Project Metadata (for Mission Control Dashboard)

**These fields are read by Mission Control — keep them updated:**

- **Status:** Active
- **Next Step:** Build `POST /terminal/order` Antigravity endpoint + simulate with Python/Postman
- **Blocker:** PSP / payment acquiring licence unresolved
- **AI Model:** Gemini (internal only)
- **Effort:** M
- **Progress:** 20%
- **Last Commit:** _(Auto-pulled from GitHub)_

---

## 📝 Notes & Decisions

### Decision Log

| Date | Decision | Rationale | Decided By |
|------|----------|-----------|------------|
| 2026-03-28 | ESP32 never calls Odoo directly | Security — only Antigravity holds Odoo credentials | Ali |
| 2026-03-28 | PCBWay is sole approved PCBA vendor | Quality control and supply chain consistency | Ali |
| 2026-03-28 | SnapScan Phase 1, M-Pesa Phase 2 | Prioritise locally-adopted QR payment first | Ali |
| 2026-03-28 | Transaction fee set at 1.0% flat | Disruptive vs. 2.75% competitor baseline | Ali |
| 2026-03-28 | Gemini used for internal orchestration only | Not to be shipped in any production component | Ali |

### Known Issues / Open Risks

| Item | Status |
|---|---|
| Payment acquiring entity / PSP licence | Unresolved — required before live transaction processing |
| SnapScan merchant onboarding (Masterpass/PSP) | Not started |
| M-Pesa SA API agreement (Vodacom) | Not started — Phase 2 |
| Odoo version upgrade strategy | Needs versioning plan in Antigravity |
| SARS import duties on PCBWay batches | Lead time: 6–10 weeks — buffer stock required |
| PCBBasic (pcbasic.com) contact | Potential phishing — do not respond until verified |

### Future Enhancements

- Embedded Finance: BaaS integration + Merchant Cash Advances
- Next-day wallet settlements inside Odoo dashboard
- Multi-currency support for cross-border African markets
- Cloud-managed firmware OTA updates via Antigravity

---

## 🔗 Quick Links

- **Repo:** [https://github.com/AliMora83/Odoo-POS-Terminal](https://github.com/AliMora83/Odoo-POS-Terminal)
- **Live URL:** [https://namka.cloud](https://namka.cloud)
- **Mission Control:** [https://github.com/AliMora83/Namka-Mission-Control/blob/main/Master.md](https://github.com/AliMora83/Namka-Mission-Control/blob/main/Master.md)
- **PCBWay (PCBA vendor):** [https://www.pcbway.com](https://www.pcbway.com)
- **EasyEDA (PCB design):** [https://easyeda.com](https://easyeda.com)

---

_Last updated by: Perplexity (Anthropic) on 2026-03-28_
